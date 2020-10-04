import logging
import time
import threading
import copy
from fedora_messaging import config
import asyncio
from . import beaker
from . import exceptions as exc
from . import log
from . import conf_test_cases
from .log import logger
from .settings import Settings
#config.conf.setup_logging()
import os
import re

def _find_true_body(message):
    """Currently the ZMQ->AMQP bridge produces a message with the
    entire fedmsg as the 'body'. When the publisher is converted to
    AMQP it will likely only include the 'msg' dict as the 'body'. So
    let's try and make sure we work either way...
    https://github.com/fedora-infra/fedmsg-migration-tools/issues/20
    """
    body = message.body
    if 'msg' in body and 'msg_id' in body:
        # OK, pretty sure this is a translated fedmsg, take 'msg'
        body = body['msg']
    return body

def consume_message(message):

    body = _find_true_body(message)
    location = body.get('location')
    status = body.get('status')
    compstr = body.get('compose_id', location)
    release_arch = config.conf["consumer_config"]["release_arch"]
    do_report = config.conf["consumer_config"]["do_report"]
    wiki_hostname = config.conf["consumer_config"]["wiki_hostname"]

    if 'Fedora-Modular' in compstr:
        logger.info("Not scheduling jobs for modular compose %s", compstr)
        return []
    if 'Fedora-Cloud' in compstr:
        logger.info("Not scheduling jobs for cloud compose %s", compstr)
        return []
    if 'Fedora-Epel' in compstr:
        logger.info("Not scheduling jobs for Epel compose %s", compstr)
        return []
    if 'Fedora-IoT' in compstr:
        logger.info("Not scheduling jobs for IoT compose %s", compstr)
        return []
    if 'updates-testing' in compstr:
        logger.info("Not scheduling jobs for updates-testing %s", compstr)
        return []
    if 'updates' in compstr:
        logger.info("Not scheduling jobs for updates %s", compstr)
        return []
    if 'Fedora-Container' in compstr:
        logger.info("Not scheduling jobs for Fedora-Container %s", compstr)
        return []
    if 'FINISHED' in status and location:
        data = { 
            "cpu-arch": release_arch,
            "beaker-distro": body["compose_id"],
            "system-type": "baremetal",
            "do_report": do_report,
            "wiki_hostname": wiki_hostname,
            }
        return data

def populate_data(data):

    driver_list = conf_test_cases.Driver_List
    ks_list = conf_test_cases.Ks_List
    hw_testcases = conf_test_cases.Hw_TestCase
    data_list = []
    base_http_url = "http://download.eng.brq.redhat.com/pub/fedora/fedmsg/dumpdata/"
    base_nfs_url = "nfs://ntap-brq2-c01-eng01-nfs-a.storage.eng.brq2.redhat.com:/pub/fedora/fedmsg/dumpdata/"
    base_released_url = "http://download.eng.bos.redhat.com/released/fedora"
    base_branched_url = "https://kojipkgs.fedoraproject.org/compose/branched/"
    release_number = re.split('-', data["beaker-distro"])[1]
    compose_name = re.split('-', data["beaker-distro"])[1]
    for driver in driver_list:
        temp = copy.deepcopy(data)
        temp["device_drivers"] = driver
        temp["ts_name"] = hw_testcases[driver]
        data_list.append(temp)
    for ks_data in ks_list:
        (ts_name , params), = ks_data.items()
        temp = copy.deepcopy(data)
        arch = temp["cpu-arch"]
        temp["ts_name"] = ts_name
        for key, value in params.items():
            temp[key] = value
        if ts_name == "QA:Testcase_Install_to_Previous_KVM":
            previous = int(release_number) - 1 
            repo_url = os.path.join(base_released_url, "F-%s", "GOLD/Server", "%s", "os")%(previous, arch)
            temp['kernel_options'] = "inst.repo=%s"%repo_url
            download_url = os.path.join(base_branched_url, temp["beaker-distro"], "compose/Server", temp["cpu-arch"], 
                        "iso", "Fedora-Server-dvd-%s-%s-%s")%(arch, release_number, compose_name)

            temp['ks_appends'] = """
                                 %%post
                                 wget %s
                                 %%end 
                                 """%download_url
        if ts_name == "QA:Testcase_Anaconda_updates.img_via_URL":
            temp['kernel_options'] = "inst.updates=https://fedorapeople.org/groups/qa/updates/updates-openqa.img"
        if ts_name == "QA:Testcase_install_repository_HTTP/FTP_variation":
            repo_url = os.path.join(base_http_url, data["beaker-distro"], 'Server', data["cpu-arch"], 'os')
            temp['kernel_options'] = "inst.repo=%s"%repo_url
            # choose servers in bos so that we can make sure inst.repo dose work
            temp['location'] = "US"
        elif ts_name == "QA:Testcase_install_repository_NFS_variation":
            repo_url = os.path.join(base_nfs_url, data["beaker-distro"], 'Server', data["cpu-arch"], 'os')
            temp['kernel_options'] = "inst.repo=%s"%repo_url
            # choose servers in bos so that we can make sure inst.repo dose work
            temp['location'] = "US"
        data_list.append(temp)
    return data_list

async def process_data(data):

    data_list = populate_data(data)
    tasks = [beaker.process(data) for data in data_list]
    await asyncio.gather(*tasks)


class Consumer:

    def __init__(self):
        """ Initialize the consumer, sets up processor.
        """
        pass

    def __call__(self, message):

        try:
            log.logger_init()
            logger.info(message)
            data = consume_message(message)

            if data:

                #We have to give beaker some time to sync the repo
                time.sleep(4800)
                asyncio.run(process_data(data))
        except Exception as e:
            logger.error("consumer failed: %s"%e)
