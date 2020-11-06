import re
import asyncio
import logging
import datetime
import copy

from asyncio.subprocess import PIPE, STDOUT
from .settings import Settings
from .utils import wiki_report
from wikitcms.wiki import ResTuple
from lxml import etree
from .convertor import convert_query_to_beaker_xml

logger = logging.getLogger(__name__)


BEAKER_URL = Settings.BEAKER_URL.rstrip('/')


async def bkr_command(*args, input=None):
    p = await asyncio.create_subprocess_exec(
        *(['bkr'] + list(args)),
        stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout, stderr = await p.communicate(input=bytes(input, 'utf8') if input else None)
    if stderr:
        logger.error("Failed calling bkr with error:", stderr)
    return stdout.decode('utf8')


async def cancel_beaker_job(job_id: str):
    logger.info('Cancel beaker job %s', job_id)
    await bkr_command('job-cancel', job_id)


def query_to_xml(sanitized_query: dict) -> str:
    """
    Convert a query to XML that could be recognized by beaker
    """
    return convert_query_to_beaker_xml(sanitized_query)


async def fetch_job_recipes(job_id: str):
    """
    Fetch job status, return set of recipes in XML Element format
    return None on failure
    """
    recipes = []
    for _ in range(1440):  # Try to fetch for one day
        try:
            active_job_xml_str = await bkr_command('job-results', job_id)
            active_job_xml = etree.fromstring(active_job_xml_str)
            recipes = list(map(lambda x: dict(x.attrib), active_job_xml.xpath('//recipe')))
            if not recipes:
                raise RuntimeError('bkr job-results command failure, may caused by: beaker is down, network'
                                   'issue or some interface changes, can\''
                                   't find valid recipe, xml result is {}'.format(active_job_xml_str))
            else:
                break
        except Exception as error:
            if _ != 1440:
                logger.exception('Error while fetching beaker job-results, keep trying in 120s...')
                await asyncio.sleep(120)
            else:
                raise
    return recipes[0]


async def extend_task_watchdog(job_id: str):
    active_job_xml_str = await bkr_command('job-results', job_id)
    active_job_xml = etree.fromstring(active_job_xml_str)
    task_childs = active_job_xml.xpath('//task[@name="/distribution/reservesys"]')
    if len(task_childs) != 1:
        raise RuntimeError('bkr job-results xml unexpected: reservesys task number {} is not equal 1'.format(len(task_childs)))
    task_id = task_childs[0].get('id')

    # beaker not support specify time right now
    logger.info('Extend beaker job %s watchdog time 2h', task_id)
    await bkr_command('watchdog-extend', task_id)


def is_recipes_failed(recipes):
    if not recipes:
        logger.error("Invalid recipes")
        return True
    elif any(info['result'] in ['Warn', 'Fail', 'Panic'] for info in recipes):
        logger.error("Beaker job ended with Warn, Fail or Panic")
        return True
    elif any(info['status'] in ['Aborted'] for info in recipes):
        logger.error("Beaker job Aborted")
        return True
    else:
        return False


def is_recipes_finished(recipes):
    if all(info['status'] == 'Running' for info in recipes):
        logger.info("Beaker job finished")
        return True


async def submit_beaker_job(job_xml: str):
    """
    Return job_id on success
    """
    logger.info("Submitting with beaker Job XML:\n%s", job_xml)
    #print("Submitting with beaker Job XML:\n%s", job_xml)
    try:
        task_id_output = await bkr_command('job-submit', input=job_xml)
        job_id = re.match("Submitted: \['(J:[0-9]+)'(?:,)?\]", task_id_output).groups()[0]
    except (ValueError, TypeError, AttributeError):
        logger.error('Expecting one job id, got: %s', task_id_output)
        return None
    else:
        return job_id


async def pull_beaker_job(job_id: str):
    """
    Keep pulling a beaker job and cancel it if the loop is interupted
    """
    success = False
    bkr_task_url = "{}/jobs/{}".format(BEAKER_URL, job_id[2:])
    try:
        while True:
            await asyncio.sleep(60)
            recipes = await fetch_job_recipes(job_id)
            logger.debug("Job recipses:%s"%recipes)
            failure = is_recipes_failed([recipes,])
            if failure:
                return None
            elif is_recipes_finished([recipes,]):
                success = True
                return recipes
            else:
                pass  # recipes pending, keep pulling

    finally:
        if not success:
            logger.error("Provisioning aborted abnormally. Cancellling beaker job %s", bkr_task_url)
            await cancel_beaker_job(job_id)
            return None
        else:
            return recipes


async def parse_machine_info(recipe: str):
    """
    Parse recipe xml to get machine info
    """
    DEFAULT_LIFE_SPAN = 86400

    NS_INV = 'https://fedorahosted.org/beaker/rdfschema/inventory#'
    NS_INV = '{%s}' % NS_INV

    NS_RDF = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
    NS_RDF = '{%s}' % NS_RDF

    ret = {}

    system_tag_map = {
        '{}cpuSpeed'.format(NS_INV): {
            'name': 'cpu-speed',
            'type': float,
        },
        '{}cpuVendor'.format(NS_INV): {
            'name': 'cpu-vendor',
            'type': str,
        },
        '{}cpuFamilyId'.format(NS_INV): {
            'name': 'cpu-family',
            'type': int,
        },
        '{}cpuModelId'.format(NS_INV): {
            'name': 'cpu-model',
            'type': int,
        },
        '{}cpuCount'.format(NS_INV): {
            'name': 'cpu-core_number',
            'type': int,
        },
        '{}cpuSocketCount'.format(NS_INV): {
            'name': 'cpu-socket_number',
            'type': int,
        },
        '{}cpuFlag'.format(NS_INV): {
            'name': 'cpu-flags',
            'type': list,
        },
        '{}cpuStepping'.format(NS_INV): {
            'name': 'cpu-stepping',
            'type': list,
        },
        '{}cpuModelName'.format(NS_INV): {
            'name': 'cpu-model_name',
            'type': str,
        },
        '{}numaNodes'.format(NS_INV): {
            'name': 'numa-node_number',
            'type': int,
        },
        '{}model'.format(NS_INV): {
            'name': 'system-model',
            'type': str,
        },
        '{}vendor'.format(NS_INV): {
            'name': 'system-vendor',
            'type': str,
        },
        '{}memory'.format(NS_INV): {
            'name': 'memory-total_size',
            'type': int,
        },
        '{}macAddress'.format(NS_INV): {
            'name': 'net-mac_address',
            'type': str,
        },
        # TODO
        # '{}hasDevice'.format(NS_INV): {
        # },
    }

    system_tag_map.update(Settings.EXTRA_BEAKER_NS_MAP)

    ret['lifespan'] = DEFAULT_LIFE_SPAN
    # This start time is not right, will update right value later
    ret['start_time'] = datetime.datetime.strptime(recipe['start_time'], '%Y-%m-%d %H:%M:%S')
    ret['cpu-arch'] = recipe['arch']
    ret['beaker-distro'] = recipe['distro']
    ret['beaker-distro_family'] = recipe['family']
    ret['beaker-distro_variant'] = recipe['variant']
    ret['hostname'] = recipe['system']

    for _ in range(5):  # retry 5 times
        try:
            recipe_detail_xml_str = await bkr_command('system-details', recipe['system'])
            logger.info(recipe_detail_xml_str)
            recipe_detail = etree.fromstring(bytes(recipe_detail_xml_str, 'utf8'))
            break
        except Exception as error:
            logger.exception("Get error while processing recipe result")
            await asyncio.sleep(10)

    system = recipe_detail.find('{}System'.format(NS_INV))
    controlled_by = system.find('{}controlledBy'.format(NS_INV))
    lab_controller = controlled_by.find('{}LabController'.format(NS_INV))
    lab_controller_url = lab_controller.get('{}about'.format(NS_RDF))
    lab_controller = lab_controller_url.split('/')[-1].split('#')[0]

    ret['lab_controller'] = lab_controller

    if lab_controller in ('lab-01.rhts.eng.pek2.redhat.com', ):
        ret['location'] = 'CN'
    elif lab_controller in ('lab-02.rhts.eng.bos.redhat.com', 'lab-02.rhts.eng.rdu.redhat.com'):
        ret['location'] = 'US'

    for tag, meta in system_tag_map.items():
        key = meta['name']
        type_ = meta['type']
        values = system.findall(tag)
        if not values:
            continue
        if type_ == list:
            ret[key] = [str(v.text) for v in values]
        else:
            if len(values) > 1:
                logger.error('Expectin only one element for %s, got multiple.', tag)
            ret[key] = type_(values[0].text)

    system_type = ret.get('system-type')
    if not system_type or system_type == 'None':
        ret['system-type'] = 'baremetal'

    return ret


async def get_beaker_job_real_start_time(job_id: str):
    start_time = None
    for _ in range(720):
        try:
            active_job_xml_str = await bkr_command('job-results', job_id)
            active_job_xml = etree.fromstring(active_job_xml_str)
            start_time = active_job_xml.xpath('//task[@name="/distribution/reservesys"]/@start_time')
            if not start_time:
                raise RuntimeError('bkr job-results command failure, may caused by: beaker is down, network'
                                   'issue or some interface changes, can\''
                                   't find valid recipe, xml result is {}'.format(active_job_xml_str))
            else:
                start_time = start_time[0]
                break
        except Exception as error:
            if _ != 720:
                logger.exception('Error while fetching beaker job-results, keep trying in 120s...')
                await asyncio.sleep(120)
            else:
                raise
    return datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')

async def provision_loop(sanitized_query):
        job_xml = query_to_xml(sanitized_query)
        recipes = None
        for failure_count in range(6):
            job_id = await submit_beaker_job(job_xml)
            recipes = await pull_beaker_job(job_id)
            if recipes is None and failure_count != 6:
                logger.error("Provision failed, retrying")
            else:
                break
        return (recipes, job_id)

async def process(data):
    (recipe ,job_id) = await provision_loop(data)
    if is_recipes_failed([recipe,]):
        bkr_job_url = "{}/jobs/{}".format(BEAKER_URL, job_id[2:])
        logger.error("Testcase %s failed!"%data["ts_name"])
        logger.error("Job failed,check %s for more information"%bkr_job_url)
    else:

        logger.info("Job succeed,reporting %s result to wiki page."%data["ts_name"])
        try:
            wiki_report(data=data, result='pass')
        except Exception as e:
            logger.error("wiki_report failed:%s"%e)
    return True
