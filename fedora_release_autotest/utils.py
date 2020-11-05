from wikitcms.wiki import Wiki, ResTuple
import mwclient.errors
from .log import logger
from . import conf_test_cases
def wiki_report(data, result):
    wiki_hostname= data["wiki_hostname"]
    do_report=data["do_report"]
    name = ''
    firmware = 'BIOS'
    imagetype = 'netinst'
    testtype = ''
    testname = ''
    testcase = ''
    bootmethod = 'x86_64 BIOS'
    section = ''
    env = ''
    arch = data.get('cpu-arch') or 'x86_64'
    subvariant = data.get('beaker-distro_variant') or 'Server'
    if data.get('device_description') == 'BIOS':
        bootmethod = 'x86_64 BIOS'
        firmware = 'BIOS'
    elif data.get('device_description') == 'UEFI':
        bootmethod = 'x86_64 UEFI'
        firmware = 'UEFI'
    if data.get('cpu-arch') == 'aarch64':
        bootmethod = 'aarch64'
        firmware = 'aarch64'
    if do_report:
        for key, value in conf_test_cases.TESTCASES.items():
            if key == data["ts_name"]:
                changed = {}
                for k, v in value.items():
                    v = v.replace('$FIRMWARE$', firmware)
                    v = v.replace('$RUNARCH$', arch)
                    v = v.replace('$BOOTMETHOD$', bootmethod)
                    v = v.replace('$SUBVARIANT$', subvariant)
                    v = v.replace('$IMAGETYPE$', imagetype)
                    changed[k] = v
                testcase = key
                testtype = changed["type"]
                section = changed["section"]
                env = changed["env"]
                testname = changed.get('name', '')
                break
                # we only pass one testcase each time,so we break here to save time
        testcases = []
        testcase = ResTuple(
            testtype=testtype, testcase=testcase, testname=testname, section=section,
            env=env, status=result, bot=True, cid=data["beaker-distro"])
        testcases.append(testcase)
        logger.info("reporting test passes to %s", wiki_hostname)

    #todo put this to config file
        wiki = Wiki(wiki_hostname, max_retries=40)
        if not wiki.logged_in:
            # This seems to occasionally throw bogus WrongPass errors
            try:
                wiki.login()
            except mwclient.errors.LoginError:
                wiki.login()
            if not wiki.logged_in:
                logger.error("could not log in to wiki")
                raise LoginError

        # Submit the results
        (insuffs, dupes) = wiki.report_validation_results(testcases)
        for dupe in dupes:
            tmpl = "already reported result for test %s, env %s! Will not report dupe."
            logger.info(tmpl, dupe.testcase, dupe.env)
            logger.debug("full ResTuple: %s", dupe)
        for insuff in insuffs:
            tmpl = "insufficient data for test %s, env %s! Will not report."
            logger.info(tmpl, insuff.testcase, insuff.env)
            logger.debug("full ResTuple: %s", insuff)

    else:
        logger.warning("no reporting is done")

