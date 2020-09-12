DEFAULT_KS_APPEND = ""


class Settings:
    EXTRA_BEAKER_NS_MAP = {
        '{https://beaker.engineering.redhat.com/keys/NR_DISKS#}key': {
            'name': 'disk-number',
            'type': int,
        },
        '{https://beaker.engineering.redhat.com/keys/DISKSPACE#}key': {
            'name': 'disk-total_size',
            'type': int,
        },
        '{https://beaker.engineering.redhat.com/keys/HVM#}key': {
            'name': 'hvm',
            'type': bool,
        },
        '{https://beaker.engineering.redhat.com/keys/VIRT_IOMMU#}key': {
            'name': 'iommu',
            'type': bool,
        },
        '{https://beaker.engineering.redhat.com/keys/MODEL#}key': {
            'name': 'system_model',
            'type': str,
        },
    }

    BEAKER_JOB_DEFAULTS = {
        'job-group': 'libvirt-ci',
        'job-whiteboard': 'fedora-release-autotest',
        'job-packages': ['libselinux-python', 'gmp-devel', 'xz-devel'],
        'job-ksappend': DEFAULT_KS_APPEND
    }  # TODO: Shouldn't be here, will move it to a better place later

    BEAKER_URL = 'https://beaker.engineering.redhat.com/'
