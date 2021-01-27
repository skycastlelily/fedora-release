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
    if data["ts_name"] == "QA:Testcase_arm_image_deployment":
        subvariant = data.get('real-distro_variant') or 'Server'
    else:
        subvariant = data.get('beaker-distro_variant') or 'Server'
    if data.get('boot_description') == 'BIOS':
        bootmethod = 'x86_64 BIOS'
        firmware = 'BIOS'
    elif data.get('boot_description') == 'UEFI':
        bootmethod = 'x86_64 UEFI'
        firmware = 'UEFI'
    if data.get('cpu-arch') == 'aarch64':
        bootmethod = 'aarch64'
        firmware = 'aarch64'
    vm_hw = data.get('vm_hw') or 'HW'
    if do_report:
        testcases = []
        if 'upgrade_dnf' in data["ts_name"] or data["ts_name"] == 'QA:Testcase_Install_to_Previous_KVM':
            cid = data["real-distro"]
        else:
            cid = data["beaker-distro"]
        for key, value in conf_test_cases.TESTCASES.items():
            if key == data["ts_name"]:
                changed = {}
                for k, v in value.items():
                    v = v.replace('$FIRMWARE$', firmware)
                    v = v.replace('$RUNARCH$', arch)
                    v = v.replace('$BOOTMETHOD$', bootmethod)
                    v = v.replace('$SUBVARIANT$', subvariant)
                    v = v.replace('$IMAGETYPE$', imagetype)
                    v = v.replace('$VM_HW$', vm_hw)
                    changed[k] = v
                testcase = key
                testtype = changed["type"]
                section = changed["section"]
                env = changed["env"]
                testname = changed.get('name', '')
                if 'Testcase_upgrade_dnf_current' in key:
                    value_any = conf_test_cases.TESTCASES['QA:Testcase_upgrade_dnf_current_any']
                    changed_any = {}
                    for k, v in value_any.items():
                        v = v.replace('$FIRMWARE$', firmware)
                        v = v.replace('$RUNARCH$', arch)
                        v = v.replace('$BOOTMETHOD$', bootmethod)
                        v = v.replace('$SUBVARIANT$', subvariant)
                        v = v.replace('$IMAGETYPE$', imagetype)
                        v = v.replace('$VM_HW$', vm_hw)
                        changed_any[k] = v
                    testcase_any = 'QA:Testcase_upgrade_dnf_current_any'
                    testtype_any = changed_any["type"]
                    section_any = changed_any["section"]
                    env_any = changed_any["env"]
                    testname_any = changed_any.get('name', '')
                    testcase_any = ResTuple(
                        testtype=testtype, testcase=testcase_any, testname=testname, section=section,
                        env=env, status=result, bot=True, cid=cid)
                    testcases.append(testcase_any)
                    logger.info("reporting test %s passes to %s", testcase_any, wiki_hostname)
                if 'Testcase_upgrade_dnf_previous' in key:
                    value_any = conf_test_cases.TESTCASES['QA:Testcase_upgrade_dnf_previous_any']
                    changed_any = {}
                    for k, v in value_any.items():
                        v = v.replace('$FIRMWARE$', firmware)
                        v = v.replace('$RUNARCH$', arch)
                        v = v.replace('$BOOTMETHOD$', bootmethod)
                        v = v.replace('$SUBVARIANT$', subvariant)
                        v = v.replace('$IMAGETYPE$', imagetype)
                        v = v.replace('$VM_HW$', vm_hw)
                        changed_any[k] = v
                    testcase_any = 'QA:Testcase_upgrade_dnf_previous_any'
                    testtype_any = changed_any["type"]
                    section_any = changed_any["section"]
                    env_any = changed_any["env"]
                    testname_any = changed_any.get('name', '')
                    testcase_any = ResTuple(
                        testtype=testtype, testcase=testcase_any, testname=testname, section=section,
                        env=env, status=result, bot=True, cid=cid)
                    testcases.append(testcase_any)
                    logger.info("reporting test %s passes to %s", testcase_any, wiki_hostname)
                break
                # we only pass one testcase each time,so we break here to save time

        testcase = ResTuple(
            testtype=testtype, testcase=testcase, testname=testname, section=section,
            env=env, status=result, bot=True, cid=cid)
        testcases.append(testcase)
        logger.info("reporting test %s passes to %s", testcase, wiki_hostname)

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

