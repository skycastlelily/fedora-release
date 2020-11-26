"""
Translate query dict into beaker xml
Raise ValidateError if any query param is illegal
"""

import os

from lxml import etree
from xml.dom import minidom
from xml.etree.ElementTree import Element

from .exceptions import ValidateError
from .settings import Settings


DEFAULTS = Settings.BEAKER_JOB_DEFAULTS
UPGRADE_LIST = ["QA:Testcase_upgrade_dnf_current_workstation",
                "QA:Testcase_upgrade_dnf_previous_workstation",
                "QA:Testcase_upgrade_dnf_current_server",
                "QA:Testcase_upgrade_dnf_previous_server",
                "QA:Testcase_upgrade_dnf_current_minimal",
                "QA:Testcase_upgrade_dnf_previous_minimal"
                ]


ACCEPT_PARAMS = {
    'system-type': {
        'type': str,
        'ops': [None],
    },
    'cpu-arch': {
        'type': str,
        'ops': [None],
    },
    'cpu-vendor': {
        'type': str,
        'ops': [None],
    },
    'cpu-model': {
        'description': 'CPU model',
        'ops': ['$eq', '$in'],
    },
    'cpu-flags': {
        'description': 'CPU Flase need to be supported',
        'type': list,
        'ops': [None]
    },
    'memory-total_size': {
        'type': int,
        'ops': ['$eq', '$lt', '$gt', '$lte', '$gte'],
        'description': 'Size in MB',
    },
    'disk-total_size': {
        'type': int,
        'ops': ['$eq', '$lt', '$gt', '$lte', '$gte'],
        'description': 'Size in GB',
    },
    'disk-number': {
        'type': int,
        'ops': ['$eq', '$lt', '$gt', '$lte', '$gte'],
    },
    'numa-node_number': {
        'type': int,
        'ops': ['$eq', '$lt', '$gt', '$lte', '$gte'],
    },
    'hvm': {
        'type': bool,
        'ops': [None],
    },
    'sriov': {
        'type': bool,
        'ops': [None],
    },
    'npiv': {
        'type': bool,
        'ops': [None],
    },
    'device_drivers': {
        'type': list,
        'ops': [None],
    },
    'location': {
        'type': str,
        'ops': [None],
    },
    'beaker-distro': {
        'type': str,
        'ops': [None],
    },
    'beaker-distro_variant': {
        'type': str,
        'ops': [None],
    },
}


def boilerplate_job(query: dict):
    """
    Build a boilerplate beaker job xml with no recipe
    """
    job = etree.Element('job')

    """
    retention tags:
    scratch: preserve logs for 30 days
    60days: preserve logs for 60 days
    120days: preserve logs for 120 days
    active: preserve as long as associated product is active
    audit: preserve indefinitely (no automatic deletion)
    """
    job.set('retention_tag', 'scratch')

    # Group up jobs for better tracking and management

    whiteboard = etree.SubElement(job, 'whiteboard')
    if query.get('device_description'):
        whiteboard.text = query.get('ts_name')+' '+query.get('cpu-arch')+' '+query.get('device_description')
    else:
        whiteboard.text = query.get('ts_name')+' '+query.get('cpu-arch')

    return job


def fill_location(host_requires: Element, sanitized_query: dict):
    # FIXME: move to right place
    controllers = {'CN': ['lab-01.rhts.eng.pek2.redhat.com'],
                   'US': ['lab-02.rhts.eng.bos.redhat.com',
                          'lab-02.rhts.eng.rdu.redhat.com',
                          'lab-02.rhts.eng.brq.redhat.com',
                          'lab-02.rhts.eng.pnq.redhat.com',
                          'lab-02.eng.tlv.redhat.com']}
    location = sanitized_query.get('location')
    if not location or location == 'ANY':
        return

    and_op = etree.SubElement(host_requires, 'and')

    if controllers.get(location):
        or_op = etree.SubElement(and_op, 'or')
        for controller_name in controllers[location]:
            controller = etree.SubElement(or_op, 'labcontroller')
            controller.set('op', '=')
            controller.set('value', controller_name)
    else:
        raise KeyError('Not support %s location', location)


def fill_machine_type(host_requires: Element, sanitized_query: dict):
    # Always baremetal
    system_type = etree.SubElement(host_requires, 'system_type')
    system_type.set("value", "Machine")

def fill_kickstart(root: Element, sanitized_query: dict):
    root.text = etree.CDATA(sanitized_query.get('ks_kickstart'))

def fill_ks_appends(root: Element, sanitized_query: dict):
    """
    Fill ks appends element for beaker job XML according to parameters
    """
    ks_append = etree.SubElement(root, 'ks_append')
    ks_default_txt = """
                     %post
                     mkdir -p /root/.ssh
                     cat >>/root/.ssh/authorized_keys <<"__EOF__"
                     ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCrszUwqjVzrY63uACIPSZZaFVwhtdENKH4RV/VqZ2+gX6rEYHHdpI4bN4QhDDWJQMGscda2U3sKfznaCyMjicC8hEdsJJgECLJ9nirb1xMt1hR9ib1bC6QVLK+8ya5z0g2W/Kc/WkRsOS9N3WMEvajG7DQe2LqudBlV7jcmAoDN5DJfugbKFh63OabaMmgU1H41m7eidghuH2yEyCuWh/eDFnoKFAlvzOgk2g8z4ZQF94r6HIwDRcWvfYsbSovESOvxqZbB0AWhaLQIvP/z2EQUmyxRM2hpqKolN09C0BMbBck4v8WUayCzzUPpWeWgGBwuRwlHi7widzHJN6tU7+l root@dhcp-128-28.nay.redhat.com
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDPt5PFhuDW6t9o+P9s+K1SnsNiSVQI/XZTwcicT8MvwBywOApYnZRUcFDLwrKoaQKw9XM8f37FLrv4ATPoOxloZKBJc5tDmHvdqDsk/+PrbHjIe084qZm9MB3vYCeLipp1vzOAsTfcDB9LQNOVdjHpdJPtWZtPiOXll6Wptb+l05nsbyoQdEgcT+2qsY5eOq9AezEF5eQtmpRr1kKCtPOiwctJor385Fj9sQP+Gu9JxnHAyaejIfPkBWSAuf2qZye/bFiOOxG1V227HfZYGPB+nP8GT011z7g7eCWwi9gwlxymZZMbTqaPHNtzLQXENNZxsv3O2pDOuAW4zMYEPh8D lnie@localhost.localdomain
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNsTH/PFfjfLLiHq19Rm9KZIOaOp56qMDLmJ1AoZJ+H3D0ux37XsxafCbT6Hcs9A2XnGLv/vnPMlAQ4ZZB1ZXlv82e43N1DVwROZd3ocbX8AylM1nYX0Lu/RHvyegRa4abeJ4pwvaX7FfABaJA0YTTnpOXBjmmbDkNbZpV+SMpJdLloEm+onaKgkWVts97q0DKRlpDXvYQRWPcoPo/OzG569eQ6shrV48VUW2vPDPkoFu9wz2cX4AZCNMdXadqSDtI9eE18Q03Qe0w6YvqnL0vhqncKktfjBJ/EVLGof3cnStvgvG+oB/IjFCd/rTjSAgTAmwDBOSNmchdnCLgRkKH root@dhcp-128-196.nay.redhat.com
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDBk+jcz8XU4Z2b23yo1AblYZiZm+elHtA9UzwwYa47fBop1yW2Mq3BtTCESYnX75uy5yF0RoQO2Q1oq5buhk5DJpE+nHniSBan//nleRPf06llpu2s8G4Qo0SWJ929gvEK6TlIxgD9wKljeieKTSi8cgtO7XD/RHrwvKJGCNUwhtPnjQQxUrcZDItRYycjJYN+Z8JBj21+R84fkpcr+f/HpYge5o3aBUS2PRdwc+82aHGTIdQ9p2JuNMyseOPfXfANJH0vQkAKWXnT7WNSSGaQs5QdsABYu0mHwsqlem/eoyCydzF8Lh8g8mPFTvs6Op3mI8iVU9noQRSrVXAhcAbn root@192.168.1.10
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC5tLd4HtMCv8pnycEPP/DTDo+jST29UJnSNUad1OEkRHGMlyFVXv2eHGpKgQxlDa2MH7R2kO+EPI8ThvYRF/kHSZdYtzsfCxzYDewuWJo9JrKbcUN0WGIdNJ3+1U8/4G43CLmMg2i6OTXr9n6rGAf1FpNDOe2wm5DbhQY7UKF6OgLPOy6Dz7CAd8jAxLi2KngWx/z7LqOS40Y/lC/cMXqaX5i3xHNQLMjAdVqw65fLgdQBCHuR1ltJ94BLsrxF1i7Bs138WmSVQS8WIXdPJLLbPRQ8VbJYoFRM5zrkVAnmPcl/w7GyQ1OfU1zm3FAsUByAQCaI5gHtjpb0r5NbXL8vj9zwGVdUKOnx/5Cd2HH0JkdBRxCv8hwTW9+H8XAm4qSbVN3mR+lH95rl6u8XdfPzUiwmkpSjWtYlJVS1RHZLtCmK5jE+jd3L8/zeN9HP0lCH+nbqUyfDTrTuUOjVHR/0xSglnOpR6OuEbQsD34yenPOTweMtoLrMYS+j9m1N9aM= root@bogon
__EOF__
                     restorecon -R /root/.ssh
                     chmod go-w /root /root/.ssh /root/.ssh/authorized_keys
                     sed -i '/^#PermitRootLogin /s/^#//' /etc/ssh/sshd_config
                     sed -i 's|PermitRootLogin .*|PermitRootLogin yes|' /etc/ssh/sshd_config
                     systemctl restart sshd
                     %end
                     """

    if sanitized_query.get('ks_append'):
        ks_append.text = etree.CDATA(sanitized_query['ks_append'] + ks_default_txt)
    else:
        ks_append.text = etree.CDATA(ks_default_txt)


def fill_repos(repos: Element, query: dict):
    """
    Fill repos element for beaker job XML according to parameters
    """
    repo_list = query.get('yum_repos') or []
    if repo_list and isinstance(repo_list, list):
        for repo_dict in repo_list:
            repo = etree.SubElement(repos, 'repo')
            repo.set('name', repo_dict['name'])
            repo.set('url', repo_dict['baseurl'])


def fill_distro_requires(root: Element, query: dict):
    """
    Fill distro requires element for beaker job XML according to parameters
    """
    and_op = etree.SubElement(root, 'and')
    requirements = []

    if query.get('cpu-arch'):
        requirements.append('distro_arch = ' + query.get('cpu-arch'))

    if query.get('beaker-distro'):
        requirements.append('distro_name = ' + query.get('beaker-distro'))

    if query.get('beaker-family'):
        requirements.append('distro_family = ' + query.get('beaker-family'))

    requirements.append('distro_variant = ' + (query.get('beaker-distro_variant') or 'Server'))

    for requirement in requirements:
        key, op, value = requirement.split()
        require = etree.SubElement(and_op, key)
        require.set("op", op)
        require.set("value", value)


def fill_packages(root: Element, query: dict):
    """
    Fill packages element for beaker job XML according to parameters
    """
    pkg_names = []
    packages = query.get('packages')
    if packages:
        if isinstance(packages, list):
            pkg_names.extend(packages)
        else:
            raise ValidateError('Packages must be a list of package names')
    for pkg_name in pkg_names:
        package_ele = etree.SubElement(root, 'package')
        package_ele.set('name', pkg_name)


def fill_cpu(root: Element, sanitized_query: dict):
    # Process CPU models filter
    cpu_model_alias = {
        'westmere': ['47', '44', '37'],
        'power8': ['4915712', '4915713', '4980992', '5046784'],
        'power9': ['5116416', '5116417', '5116418'],
    }

    cpu_vendor_alias = {
        'amd': 'AuthenticAMD',
        'ibm': 'IBM',
        'intel': 'GenuineIntel',
    }

    cpu_models = []
    cpu_models_query = sanitized_query.get('cpu-model')
    if cpu_models_query:
        for op, value in cpu_models_query.items():
            if type(value) is str:
                cpu_models.extend(cpu_model_alias.get(value, [value]))
            elif type(value) in (tuple, list):
                for sub_val in value:
                    cpu_models.extend(cpu_model_alias.get(sub_val, [sub_val]))
            else:
                raise TypeError('Unsupported type {}'.format(type(value)))

    cpu_vendor = None
    if sanitized_query.get('cpu-vendor'):
        cpu_vendor = cpu_vendor_alias.get(value, value)

    if cpu_models:
        or_op = etree.SubElement(root, 'or')
        for model_name in cpu_models:
            cpu = etree.SubElement(or_op, 'cpu')
            model = etree.SubElement(cpu, 'model')
            model.set('op', '=')
            model.set('value', model_name)

    if cpu_vendor:
        or_op = etree.SubElement(root, 'or')
        cpu = etree.SubElement(or_op, 'cpu')
        vendor = etree.SubElement(cpu, 'vendor')
        vendor.set('op', '=')
        vendor.set('value', cpu_vendor)


def fill_devices(root: Element, sanitized_query: dict):
    if sanitized_query.get('device_drivers'):
        device = etree.SubElement(root, 'device')
        device_drivers = sanitized_query.get('device_drivers')
        device.set('op', 'like')
        device.set('driver', '%'+device_drivers+'%')


def fill_host_requirements(host_requires: Element, sanitized_query: dict):
    """
    Fill host requires element for beaker job XML according to query
    """
    op_map = {
        '$eq': '=', '$gt': '>', '$lt': '<', '$lte': '<=', '$gte': '>=',
    }

    # Prepare requirements according to parameters
    def add_requirement(key, op, value, is_extra=False):
        if is_extra:
            require = etree.SubElement(host_requires, 'key_value')
            require.set("key", key)
        else:
            require = etree.SubElement(host_requires, key)
        require.set("op", op)
        require.set("value", str(value))

    if sanitized_query.get('system-type', 'baremetal') == 'baremetal':
        add_requirement('hypervisor', '=', '')
    else:
        raise ValidateError('System type other that baremetal is not supported yet.')

    if sanitized_query.get('device_description'):
        add_requirement('device_description', '=', sanitized_query.get('device_description'))

    if sanitized_query.get('cpu-arch'):
        add_requirement('arch', '=', sanitized_query.get('cpu-arch'))

    for op, value in sanitized_query.get('memory-total_size', {}).items():
        add_requirement('memory', op_map[op], value)

    for flag in sanitized_query.get('cpu-flags', []):
        add_requirement('CPUFLAGS', '=', flag, is_extra=True)

    if sanitized_query.get('hvm'):
        add_requirement('HVM', '=', '1', is_extra=True)

    for op, value in sanitized_query.get('disk-total_size', {}).items():
        add_requirement("DISKSPACE", op_map[op], value, is_extra=True)

    for op, value in sanitized_query.get('disk-number', {}).items():
        add_requirement("NR_DISKS", op_map[op], value, is_extra=True)

    for op, value in sanitized_query.get('numa-node_number', {}).items():
        add_requirement("numa_node_count", op_map[op], value, is_extra=True)

    # TODO: add this in params
    excluded_hosts = os.environ.get('EXCLUDED_HOSTS')
    if excluded_hosts:
        host_list = excluded_hosts.split(',')
        for host in host_list:
            add_requirement('hostname', '!=', host)

    fill_cpu(host_requires, sanitized_query)
    fill_devices(host_requires, sanitized_query)
    fill_machine_type(host_requires, sanitized_query)


def add_reserve_task(recipe: Element, sanitized_query: dict):
    """
    Use a reserve task to reserve a machine.
    """
    task = etree.SubElement(recipe, 'task')
    task.set('name', '/distribution/check-install')
    task.set('role', 'STANDALONE')
    task_params = etree.SubElement(task, 'params')
    task_param = etree.SubElement(task_params, 'param')
    task_param.set('name', 'RSTRNT_DISABLED')
    task_param.set('value', '01_dmesg_check 10_avc_check')

    if sanitized_query.get("device_description") == "UEFI":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/check/uefi')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] == "QA:Testcase_Install_to_Previous_KVM":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/virt/kvm-install')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] == "QA:Testcase_Install_to_Current_KVM":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/virt/kvm-install')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] in UPGRADE_LIST:
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/upgrade/dnf')
        task.set('role', 'STANDALONE')
        task_params = etree.SubElement(task, 'params')
        task_param = etree.SubElement(task_params, 'param')
        task_param.set('name', 'RSTRNT_DISABLED')
        task_param.set('value', '01_dmesg_check 10_avc_check')
    if sanitized_query["ts_name"] == "QA:Testcase_partitioning_guided_multi_select_pre":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/multi/prepare')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] == "QA:Testcase_partitioning_guided_multi_select":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/multi/select')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] == "QA:Testcase_partitioning_guided_free_space_pre":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/freespace/prepare')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] == "QA:Testcase_partitioning_guided_free_space":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/freespace/task')
        task.set('role', 'STANDALONE')
    if sanitized_query["ts_name"] == "QA:Testcase_partitioning_guided_multi_empty_all":
        task = etree.SubElement(recipe, 'task')
        task.set('name', '/fedora/multi/empty')
        task.set('role', 'STANDALONE')
    
    #reserve = etree.SubElement(recipe, 'reservesys')
    #reserve.set('duration', '86400')
    #reserve.set('when', 'onfail')



def fill_boilerplate_recipe(recipe: Element, sanitized_query: dict):
    # Some default params
    if sanitized_query.get('device_description'):
        whiteboard_sum = sanitized_query.get('ts_name')+' '+sanitized_query.get('cpu-arch')+' '+sanitized_query.get('device_description')
    else:
        whiteboard_sum = sanitized_query.get('ts_name')+' '+sanitized_query.get('cpu-arch')

    recipe.set('whiteboard', whiteboard_sum)  # TODO
    recipe.set('role', 'None')

    # Some default params
    if sanitized_query.get('ks_meta'):
        recipe.set('ks_meta', sanitized_query["ks_meta"])
    if sanitized_query.get('kernel_options'):
        recipe.set('kernel_options', sanitized_query['kernel_options'])

    # Don't autopick
    autopick = etree.SubElement(recipe, 'autopick')
    autopick.set('random', 'false')

    # Don't autoreboot
    watchdog = etree.SubElement(recipe, 'watchdog')
    watchdog.set('panic', 'ignore')

    host_requires = etree.SubElement(recipe, 'hostRequires')

    ks_appends = etree.SubElement(recipe, 'ks_appends')
    ks_kickstart = etree.SubElement(recipe, 'kickstart')
    repos = etree.SubElement(recipe, 'repos')
    distro_requires = etree.SubElement(recipe, 'distroRequires')
    packages = etree.SubElement(recipe, 'packages')
    if sanitized_query.get('ks_kickstart'):
        fill_kickstart(ks_kickstart, sanitized_query)
    else:
        fill_ks_appends(ks_appends, sanitized_query)
    fill_packages(packages, sanitized_query)
    fill_repos(repos, sanitized_query)
    fill_distro_requires(distro_requires, sanitized_query)
    fill_location(host_requires, sanitized_query)

    if sanitized_query.get('target-host'):
        host_requires.set('force', sanitized_query.get('target-host'))
    else:
        fill_host_requirements(host_requires, sanitized_query)


def convert_query_to_beaker_xml(sanitized_query: dict):
    job = boilerplate_job(sanitized_query)

    # Use normal priority by default
    recipe_set = etree.SubElement(job, 'recipeSet')
    recipe_set.set('priority', 'Normal')

    # Always only one recipe
    for _ in range(sanitized_query.get('provision-count', 1)):
        recipe = etree.SubElement(recipe_set, 'recipe')
        fill_boilerplate_recipe(recipe, sanitized_query)
        add_reserve_task(recipe, sanitized_query)

    pretty_xml = minidom.parseString(etree.tostring(job)).toprettyxml(indent="  ")
    return pretty_xml
