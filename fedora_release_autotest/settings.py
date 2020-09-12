import os
from pathlib import Path


DEFAULT_KS_APPEND = """
%post
# Fill your custom ks append here in cuvette
%end
"""


class Required:
    def __init__(self, v_type=None):
        self.v_type = v_type


class Settings(object):
    """
    Any setting defined here can be overridden by:

    Settings the appropriate environment variable, eg. to override FOOBAR, `export APP_FOOBAR="whatever"`.
    This is useful in production for secrets you do not wish to save in code and
    also plays nicely with docker(-compose). Settings will attempt to convert environment variables to match the
    type of the value here. See also activate.settings.sh.

    Or, passing the custom setting as a keyword argument when initialising settings (useful when testing)
    """
    _ENV_PREFIX = 'APP_'

    EXTRA_BEAKER_NS_MAP = {
    }

    BEAKER_JOB_DEFAULTS = {
    }  # TODO: Shouldn't be here, will move it to a better place later

    BEAKER_URL = 'https://beaker.engineering.redhat.com'

    DB_NAME = Required(str)
    DB_USER = Required(str)
    DB_PASSWORD = Required(str)
    DB_HOST = 'localhost'
    DB_PORT = '27017'
    
    Ks_List = { 
        "QA:Testcase_Boot_default_install": {
            "beaker-distro_variant": "Server",
            "device_description": "UEFI",
            },
        "QA:Testcase_Boot_default_install": {
            "beaker-distro_variant": "Server",
            "device_description": "BIOS",
            },
        "QA:Testcase_Boot_default_install": {
            "beaker-distro_variant": "Everything",
            "device_description": "UEFI",
            },
        "QA:Testcase_Boot_default_install": {
            "beaker-distro_variant": "Everything",
            "device_description": "BIOS",
            },
        "QA:Testcase_Boot_Methods_Pxeboot": {
            "cpu-arch": "x86_64",
            },
        "QA:Testcase_Boot_Methods_Pxeboot": {
            "cpu-arch": "aarch64",
            },
        "QA:Testcase_Install_to_Previous_KVM": {
            "cpu-arch": "x86_64",
            "cpu-flags": ["vmx", ]
            "device_description": "BIOS",
            "packages": ["wget", "libvirt", "qemu-kvm", "virt-install"],
            },
        "QA:Testcase_Install_to_Previous_KVM": {
            "cpu-flags": ["vmx", ]
            "cpu-arch": "x86_64",
            "device_description": "UEFI",
            "packages": ["wget", "libvirt", "qemu-kvm", "virt-install"],
            },
        "QA:Testcase_Install_to_Previous_KVM": {
            "cpu-flags": ["vmx", ]
            "cpu-arch": "aarch64",
            "packages": ["wget", "libvirt", "qemu-kvm", "virt-install"],
            },
        "QA:Testcase_Install_to_Current_KVM": {
            "cpu-flags": ["vmx", ]
            "cpu-arch": "x86_64",
            "device_description": "BIOS",
            "packages": ["wget", "libvirt", "qemu-kvm", "virt-install"],
            },
        "QA:Testcase_Install_to_Current_KVM": {
            "cpu-flags": ["vmx", ]
            "cpu-arch": "x86_64",
            "device_description": "UEFI",
            "packages": ["wget", "libvirt", "qemu-kvm", "virt-install"],
            },
        "QA:Testcase_Install_to_Current_KVM": {
            "cpu-flags": ["vmx", ]
            "cpu-arch": "aarch64",
            "packages": ["wget", "libvirt", "qemu-kvm", "virt-install"],
            },
        "QA:Testcase_partitioning_guided_delete_all": {
            "ks_meta": "no_autopart",
            "ks_append": "autopart --type lvm",
            "device_description": "BIOS",
            },
        "QA:Testcase_partitioning_guided_delete_all": {
            "ks_meta": "no_autopart",
            "ks_append": "autopart --type lvm",
            "device_description": "UEFI",
            },
        "QA:Testcase_partitioning_guided_encrypted": {
            "ks_meta": "no_autopart",
            "ks_append": "autopart --encrypted --passphrase fedoratest123",
            "device_description": "BIOS",
            },
        "QA:Testcase_partitioning_guided_encrypted": {
            "ks_meta": "no_autopart",
            "ks_append": "autopart --encrypted --passphrase fedoratest123",
            "device_description": "UEFI",
            },
        "QA:Testcase_partitioning_guided_encrypted": {
            "ks_meta": "no_autopart",
            "ks_append": "autopart --encrypted --passphrase fedoratest123",
            "cpu-arch": "aarch64",
            },
        "QA:Testcase_partitioning_custom_btrfs": {
            "device_description": "BIOS",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype="xfs"  --size=1024
                         part btrfs.355 --fstype="btrfs"  --size=15360
                         btrfs none --label=fedora_fedora00 btrfs.355
                         btrfs / --subvol --name=root LABEL=fedora_fedora00
                         """
            },
        "QA:Testcase_partitioning_custom_btrfs": {
            "device_description": "UEFI",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype="xfs"  --size=1024
                         part btrfs.355 --fstype="btrfs"  --size=15360
                         btrfs none --label=fedora_fedora00 btrfs.355
                         btrfs / --subvol --name=root LABEL=fedora_fedora00
                         """
            },
        "QA:Testcase_partitioning_custom_btrfs": {
            "cpu-arch": "aarch64",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype="xfs"  --size=1024
                         part btrfs.355 --fstype="btrfs"  --size=15360
                         btrfs none --label=fedora_fedora00 btrfs.355
                         btrfs / --subvol --name=root LABEL=fedora_fedora00
                         """
            },
        "QA:Testcase_partitioning_custom_lvmthin": {
            "device_description": "BIOS",
            "ks_meta": "no_autopart",
            "ks_append": "autopart --type thinp",
            },
        "QA:Testcase_partitioning_custom_lvmthin": {
            "device_description": "UEFI",
            "ks_meta": "no_autopart",
            "ks_append": "autopart --type thinp",
            },
        "QA:Testcase_partitioning_custom_lvmthin": {
            "cpu-arch": "aarch64",
            "ks_meta": "no_autopart",
            "ks_append": "autopart --type thinp",
            },
        "QA:Testcase_partitioning_custom_standard_partition_ext3": {
            "device_description": "BIOS",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype=xfs
                         part / --fstype=ext3 --grow
                         """
            },
        "QA:Testcase_partitioning_custom_standard_partition_ext3": {
            "device_description": "UEFI",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype=xfs
                         part / --fstype=ext3 --grow
                         """
            },
        "QA:Testcase_partitioning_custom_standard_partition_ext3": {
            "cpu-arch": "aarch64",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype=xfs
                         part / --fstype=ext3 --grow
                         """
            },
        "QA:Testcase_partitioning_custom_standard_partition_xfs": {
            "device_description": "BIOS",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype=xfs
                         part / --fstype=xfs --grow
                         """
            },
        "QA:Testcase_partitioning_custom_standard_partition_xfs": {
            "device_description": "UEFI",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype=xfs
                         part / --fstype=xfs --grow
                         """
            },
        "QA:Testcase_partitioning_custom_standard_partition_xfs": {
            "cpu-arch": "aarch64",
            "ks_meta": "no_autopart",
            "ks_append": """
                         part /boot --fstype=xfs
                         part / --fstype=xfs --grow
                         """
            },
        "QA:Testcase_install_repository_HTTP/FTP_variation": {
            "kernel_options": "",
            },
        "QA:Testcase_install_repository_NFS_variation": {
            "kernel_options": "",
            },
        "QA:Testcase_install_repository_NFSISO_variation": {
            "kernel_options": "",
            },
        "QA:Testcase_Package_Sets_Minimal_Package_Install": {
            "beaker-distro_variant": "Everything",
            "ks_append": """
                         %packages
                         @^minimal-environment
                         %end
                         """
            },
        "QA:Testcase_Asian_Language_Install": {
            "ks_append": "lang zh_CN.UTF-8",
            },
        "QA:Testcase_Anaconda_updates.img_via_URL": {
            "kernel_options": "",
            },
        }

    Driver_List = ["pata", "sata", "raid", "scsi", "sas"]

    Hw_TestCase = {
    "pata": "QA:Testcase_install_to_PATA",
    "sata": "QA:Testcase_install_to_SATA",
    "scsi": "QA:Testcase_install_to_SCSI",
    "sas": "QA:Testcase_install_to_SAS",
    "raid": "QA:Testcase_install_to_RAID",
    }

    Log_Dir = "/tmp"
    Log_Level = "1"
    Env = "x86_64"

    def __init__(self, **custom_settings):
        """
        :param custom_settings: Custom settings to override defaults, only attributes already defined can be set.
        """
        self._custom_settings = custom_settings
        self.substitute_environ()
        for name, value in custom_settings.items():
            if not hasattr(self, name):
                raise TypeError('{} is not a valid setting name'.format(name))
            setattr(self, name, value)

    def substitute_environ(self):
        """
        Substitute environment variables into settings.
        """
        for attr_name in dir(self):
            if attr_name.startswith('_') or attr_name.upper() != attr_name:
                continue

            orig_value = getattr(self, attr_name)
            is_required = isinstance(orig_value, Required)
            orig_type = orig_value.v_type if is_required else type(orig_value)
            env_var_name = self._ENV_PREFIX + attr_name
            env_var = os.getenv(env_var_name, None)
            if env_var is not None:
                if issubclass(orig_type, bool):
                    env_var = env_var.upper() in ('1', 'TRUE')
                elif issubclass(orig_type, int):
                    env_var = int(env_var)
                elif issubclass(orig_type, Path):
                    env_var = Path(env_var)
                elif issubclass(orig_type, bytes):
                    env_var = env_var.encode()
                # could do floats here and lists etc via json
                setattr(self, attr_name, env_var)
            elif is_required and attr_name not in self._custom_settings:
                raise RuntimeError('The required environment variable "{0}" is currently not set, '
                                   'you\'ll need to run `source activate.settings.sh` '
                                   'or you can set that single environment variable with '
                                   '`export {0}="<value>"`'.format(env_var_name))


try:
    from .settings_overlay import Settings as ExtraSettings
    for name in dir(ExtraSettings):
        if name.startswith('_'):
            continue
        setattr(Settings, name, getattr(ExtraSettings, name))
except ImportError:
    pass
