# Copyright (C) 2015 Red Hat
#
# This file is part of fedora-openqa-schedule.
#
# fedora-openqa-schedule is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Jan Sedlak <jsedlak@redhat.com>
#            Josef Skladanka <jskladan@redhat.com>
#            Adam Williamson <awilliam@redhat.com>

"""This module contains data for mapping openQA jobs to Wikitcms test
instances.
"""

Ks_List = [
    { "QA:Testcase_Boot_default_install": {
        "beaker-distro_variant": "Server",
        "device_description": "UEFI",
        "packages": ["beakerlib", ],
        }},
    {"QA:Testcase_Boot_default_install": {
        "beaker-distro_variant": "Server",
        "device_description": "BIOS",
        }},
    {"QA:Testcase_Boot_default_install": {
        "beaker-distro_variant": "Everything",
        "packages": ["beakerlib", ],
        "device_description": "UEFI",
        }},
    { "QA:Testcase_Boot_default_install": {
        "beaker-distro_variant": "Everything",
        "device_description": "BIOS",
        }},
    {"QA:Testcase_Boot_Methods_Pxeboot": {
        "cpu-arch": "x86_64",
        }},
    {"QA:Testcase_Boot_Methods_Pxeboot": {
        "cpu-arch": "aarch64",
        }},
    {"QA:Testcase_install_to_NVMe": {
        "cpu-arch": "aarch64",
        }},
    {"QA:Testcase_Install_to_Previous_KVM": {
        "cpu-arch": "x86_64",
        "cpu-flags": ["vmx", ],
        "device_description": "BIOS",
        "packages": ["wget", "beakerlib"],
        "disk-total_size": {"$gt": "50G"}
        }},
    {"QA:Testcase_Install_to_Previous_KVM": {
        "cpu-flags": ["vmx", ],
        "cpu-arch": "x86_64",
        "device_description": "UEFI",
        "packages": ["wget", "beakerlib"],
        "disk-total_size": {"$gt": "50G"}
        }},
    {"QA:Testcase_Install_to_Previous_KVM": {
        "cpu-arch": "aarch64",
        "packages": ["wget", "beakerlib"],
        "disk-total_size": {"$gt": "50G"}
        }},
    {"QA:Testcase_Install_to_Current_KVM": {
        "cpu-flags": ["vmx", ],
        "cpu-arch": "x86_64",
        "device_description": "BIOS",
        "packages": ["wget", "beakerlib"],
        "disk-total_size": {"$gt": "50G"}
        }},
    {"QA:Testcase_Install_to_Current_KVM": {
        "cpu-flags": ["vmx", ],
        "cpu-arch": "x86_64",
        "device_description": "UEFI",
        "packages": ["wget", "beakerlib"],
        "disk-total_size": {"$gt": "50G"}
        }},
    {"QA:Testcase_Install_to_Current_KVM": {
        "cpu-arch": "aarch64",
        "packages": ["wget", "beakerlib"],
        "disk-total_size": {"$gt": "50G"}
        }},
    {"QA:Testcase_partitioning_guided_delete_all": {
        "ks_meta": "no_autopart",
        "ks_append": "autopart --type lvm",
        "device_description": "BIOS",
        }},
    {"QA:Testcase_partitioning_guided_delete_all": {
        "ks_meta": "no_autopart",
        "packages": ["beakerlib", ],
        "ks_append": "autopart --type lvm",
        "device_description": "UEFI",
        }},
    {"QA:Testcase_partitioning_guided_delete_all": {
        "ks_meta": "no_autopart",
        "ks_append": "autopart --type lvm",
        "cpu-arch": "aarch64",
        }},
    {"QA:Testcase_partitioning_guided_multi_select_pre": {
        "disk-number": {"$gt": "2"},
        "ks_meta": "no_autopart",
        "device_description": "BIOS",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     part /boot --fstype="xfs" --size=1024 --ondisk=sda
                     part / --fstype="xfs" --grow --ondisk=sda
                     """
        }},
    {"QA:Testcase_partitioning_guided_multi_select_pre": {
        "disk-number": {"$gt": "2"},
        "ks_meta": "no_autopart",
        "device_description": "UEFI",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     part /boot/efi --fstype="xfs"  --size=1024 --ondisk=sda
                     part /boot --fstype="xfs" --size=1024 --ondisk=sda
                     part / --fstype="xfs" --grow --ondisk=sda
                     """
        }},
    {"QA:Testcase_partitioning_guided_multi_select_pre": {
        "disk-number": {"$gt": "2"},
        "ks_meta": "no_autopart",
        "cpu-arch": "aarch64",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     part /boot/efi --fstype="xfs"  --size=1024 --ondisk=sda
                     part /boot --fstype="xfs" --size=1024 --ondisk=sda
                     part / --fstype="xfs" --grow --ondisk=sda
                     """
        }},
    {"QA:Testcase_partitioning_guided_free_space_pre": {
        "ks_meta": "no_autopart",
        "disk-total_size": {"$gt": "50G"},
        "device_description": "BIOS",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     part /boot --fstype="xfs" --size=1024 --ondisk=sda
                     part / --fstype="xfs" --size=10240 --ondisk=sda
                     """
        }},
    {"QA:Testcase_partitioning_guided_free_space_pre": {
        "ks_meta": "no_autopart",
        "disk-total_size": {"$gt": "50G"},
        "device_description": "UEFI",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     part /boot/efi --fstype="xfs"  --size=1024 --ondisk=sda
                     part /boot --fstype="xfs" --size=1024 --ondisk=sda
                     part / --fstype="xfs" --size=10240 --ondisk=sda
                     """
        }},
    {"QA:Testcase_partitioning_guided_free_space_pre": {
        "ks_meta": "no_autopart",
        "cpu-arch": "aarch64",
        "disk-total_size": {"$gt": "50G"},
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     part /boot/efi --fstype="xfs"  --size=1024 --ondisk=sda
                     part /boot --fstype="xfs" --size=1024 --ondisk=sda
                     part / --fstype="xfs" --size=10240 --ondisk=sda
                     """
        }},
    {"QA:Testcase_partitioning_guided_encrypted": {
        "ks_meta": "no_autopart",
        "ks_append": "autopart --encrypted --passphrase fedoratest123",
        "device_description": "BIOS",
        }},
    {"QA:Testcase_partitioning_guided_encrypted": {
        "ks_meta": "no_autopart",
        "ks_append": "autopart --encrypted --passphrase fedoratest123",
        "device_description": "UEFI",
        }},
    {"QA:Testcase_partitioning_guided_encrypted": {
        "ks_meta": "no_autopart",
        "ks_append": "autopart --encrypted --passphrase fedoratest123",
        "cpu-arch": "aarch64",
        }},
    {"QA:Testcase_partitioning_guided_multi_empty_all": {
        "disk-number": {"$gt": "2"},
        "ks_meta": "no_autopart",
        "packages": ["wget", "beakerlib"],
        "ks_append": "autopart --type lvm",
        "device_description": "BIOS",
        }},
    {"QA:Testcase_partitioning_guided_multi_empty_all": {
        "disk-number": {"$gt": "2"},
        "ks_meta": "no_autopart",
        "packages": ["wget", "beakerlib"],
        "ks_append": "autopart --type lvm",
        "device_description": "UEFI",
        }},
    {"QA:Testcase_partitioning_guided_multi_empty_all": {
        "disk-number": {"$gt": "2"},
        "ks_meta": "no_autopart",
        "packages": ["wget", "beakerlib"],
        "ks_append": "autopart --type lvm",
        "cpu-arch": "aarch64",
        }},
    {"QA:Testcase_partitioning_custom_btrfs": {
        "device_description": "BIOS",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype="xfs"  --size=1024
                     part btrfs.355 --fstype="btrfs"  --size=15360
                     btrfs none --label=fedora_fedora00 btrfs.355
                     btrfs / --subvol --name=root LABEL=fedora_fedora00
                     """
        }},
    {"QA:Testcase_partitioning_custom_btrfs": {
        "device_description": "UEFI",
        "packages": ["beakerlib", ],
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype="xfs"  --size=1024
                     part /boot/efi --fstype="xfs"  --size=1024
                     part btrfs.355 --fstype="btrfs"  --size=15360
                     btrfs none --label=fedora_fedora00 btrfs.355
                     btrfs / --subvol --name=root LABEL=fedora_fedora00
                     """
        }},
    {"QA:Testcase_partitioning_custom_btrfs": {
        "cpu-arch": "aarch64",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype="xfs"  --size=1024
                     part /boot/efi --fstype="xfs"  --size=1024
                     part btrfs.355 --fstype="btrfs"  --size=15360
                     btrfs none --label=fedora_fedora00 btrfs.355
                     btrfs / --subvol --name=root LABEL=fedora_fedora00
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_ext4": {
        "device_description": "BIOS",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=ext4 --size=1024
                     part / --fstype=ext4 --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_ext4": {
        "device_description": "UEFI",
        "packages": ["beakerlib", ],
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=ext4  --size=1024
                     part /boot/efi --fstype=ext4  --size=1024
                     part / --fstype=ext4 --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_ext4": {
        "cpu-arch": "aarch64",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=ext4  --size=1024
                     part /boot/efi --fstype=ext4  --size=1024
                     part / --fstype=ext4 --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_lvm_ext4": {
        "device_description": "BIOS",
        "ks_meta": "no_autopart",
        "ks_append": """
                     autopart --type lvm --fstype=ext4
                     """
        }},
    {"QA:Testcase_partitioning_custom_lvm_ext4": {
        "packages": ["beakerlib", ],
        "device_description": "UEFI",
        "ks_meta": "no_autopart",
        "ks_append": """
                     autopart --type lvm --fstype=ext4
                     """
        }},
    {"QA:Testcase_partitioning_custom_lvm_ext4": {
        "cpu-arch": "aarch64",
        "ks_meta": "no_autopart",
        "ks_append": """
                     autopart --type lvm --fstype=ext4
                     """
        }},
    {"QA:Testcase_partitioning_custom_lvmthin": {
        "device_description": "BIOS",
        "ks_meta": "no_autopart",
        "ks_append": "autopart --type thinp",
        }},
    {"QA:Testcase_partitioning_custom_lvmthin": {
        "device_description": "UEFI",
        "packages": ["beakerlib", ],
        "ks_meta": "no_autopart",
        "ks_append": "autopart --type thinp",
        }},
    {"QA:Testcase_partitioning_custom_lvmthin": {
        "cpu-arch": "aarch64",
        "ks_meta": "no_autopart",
        "ks_append": "autopart --type thinp",
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_ext3": {
        "device_description": "BIOS",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=xfs
                     part / --fstype=ext3 --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_ext3": {
        "device_description": "UEFI",
        "packages": ["beakerlib", ],
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=xfs --size=1024
                     part /boot/efi --fstype="xfs"  --size=1024
                     part / --fstype=ext3 --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_ext3": {
        "cpu-arch": "aarch64",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=xfs --size=1024
                     part /boot/efi --fstype="xfs"  --size=1024
                     part / --fstype=ext3 --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_xfs": {
        "device_description": "BIOS",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=xfs
                     part / --fstype=xfs --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_xfs": {
        "device_description": "UEFI",
        "packages": ["beakerlib", ],
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=xfs --size=1024
                     part /boot/efi --fstype="xfs"  --size=1024
                     part / --fstype=xfs --grow
                     """
        }},
    {"QA:Testcase_partitioning_custom_standard_partition_xfs": {
        "cpu-arch": "aarch64",
        "ks_meta": "no_autopart",
        "ks_append": """
                     part /boot --fstype=xfs --size=1024
                     part /boot/efi --fstype="xfs"  --size=1024
                     part / --fstype=xfs --grow
                     """
        }},
    {"QA:Testcase_install_repository_HTTP/FTP_variation": {
        "kernel_options": "",
        }},
    {"QA:Testcase_install_repository_NFS_variation": {
        "kernel_options": "",
        }},
    {"QA:Testcase_install_repository_NFSISO_variation": {
        "kernel_options": "",
        }},
    {"QA:Testcase_Package_Sets_Minimal_Package_Install": {
        "beaker-distro_variant": "Everything",
        "ks_append": """
                     %packages
                     @^minimal-environment
                     %end
                     """
        }},
    {"QA:Testcase_upgrade_dnf_current_workstation": {
        "cpu-arch": "x86_64",
        "beaker-distro_variant": "Everything",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     %packages
                     @^workstation-product-environment
                     %end
                     """
        }},
    {"QA:Testcase_upgrade_dnf_previous_workstation": {
        "cpu-arch": "x86_64",
        "beaker-distro_variant": "Everything",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     %packages
                     @^workstation-product-environment
                     %end
                     """
        }},
    {"QA:Testcase_upgrade_dnf_current_server": {
        "cpu-arch": "x86_64",
        "beaker-distro_variant": "Server",
        "packages": ["wget", "beakerlib"],
        }},
    {"QA:Testcase_upgrade_dnf_previous_server": {
        "cpu-arch": "x86_64",
        "beaker-distro_variant": "Server",
        "packages": ["wget", "beakerlib"],
        }},
    {"QA:Testcase_upgrade_dnf_current_minimal": {
        "cpu-arch": "x86_64",
        "beaker-distro_variant": "Everything",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     %packages
                     @^minimal-environment
                     %end
                     """
        }},
    {"QA:Testcase_upgrade_dnf_current_minimal": {
        "cpu-arch": "aarch64",
        "beaker-distro_variant": "Everything",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     %packages
                     @^minimal-environment
                     %end
                     """
        }},
    {"QA:Testcase_upgrade_dnf_previous_minimal": {
        "cpu-arch": "x86_64",
        "beaker-distro_variant": "Everything",
        "packages": ["wget", "beakerlib"],
        "ks_append": """
                     %packages
                     @^minimal-environment
                     %end
                     """
        }},
    {"QA:Testcase_Asian_Language_Install": {
        "beaker-distro_variant": "Everything",
        "ks_append": """
                     lang zh_CN.UTF-8
                     %packages
                     @^workstation-product-environment
                     %end
                     """
        }},
    {"QA:Testcase_Anaconda_updates.img_via_URL": {
        "kernel_options": "",
        }},
    ]

Ks_List_Two = [
    {"ts_name": "QA:Testcase_partitioning_guided_multi_select",
     "ks_meta": "no_autopart",
     "packages": ["wget", "beakerlib"],
     "target-host": "",
     "cpu-arch": "",
     "beaker-distro": "",
     "system-type": "baremetal",
     "do_report": "True",
     "wiki_hostname": "fedoraproject.org",
     "resultsdb_url": "http://resultsdb01.qa.fedoraproject.org/resultsdb_api/api/v2.0/",
     "recent_release": "",
     "ks_append": """
                  clearpart --all --initlabel
                  ignoredisk --only-use=sda
                  autopart --type lvm
                  """
    },
    {"ts_name": "QA:Testcase_partitioning_guided_free_space",
     "packages": ["wget", "beakerlib"],
     "target-host": "",
     "cpu-arch": "",
     "beaker-distro": "",
     "system-type": "baremetal",
     "do_report": "True",
     "ks_kickstart": "REPLACE_THIS",
     "wiki_hostname": "fedoraproject.org",
     "resultsdb_url": "http://resultsdb01.qa.fedoraproject.org/resultsdb_api/api/v2.0/",
    },

]

Driver_List = ["nvme", "pata", "sata", "raid", "scsi", "sas"]


Hw_TestCase = {
    "nvme": "QA:Testcase_install_to_NVMe",
    "pata": "QA:Testcase_install_to_PATA",
    "sata": "QA:Testcase_install_to_SATA",
    "scsi": "QA:Testcase_install_to_SCSI",
    "sas": "QA:Testcase_install_to_SAS",
    "raid": "QA:Testcase_install_to_RAID",
}

TESTCASES = {
    # the following strings in values will be replaced with strings
    # derived from openQA job settings, this is used for e.g. to get
    # the correct 'environment' or 'testname'.
    #
    #   special value       replacement
    #
    #   $RUNARCH$             - "i386", "x86_64", "arm"
    #   $BOOTMETHOD$          - "x86_64 BIOS", "x86_64 UEFI"
    #   $FIRMWARE$            - "BIOS", "UEFI"
    #   $SUBVARIANT$          - productmd 'subvariant': "Server", "KDE"... "_Base" is stripped
    #   $SUBVARIANT_OR_ARM$   - productmd 'subvariant' as above, or "ARM" when running on ARM architecture
    #   $SUBVARIANT_OR_LOCAL$ - productmd 'subvariant' as above, or "Local" when subvariant contains "Cloud"
    #   $CLOUD_OR_BASE$ -     - 'Cloud' when subvariant contains 'Cloud', 'Base' otherwise
    #   $IMAGETYPE$           - pungi 'type': "boot", "live"... "boot" -> "netinst"
    #   $FS$                  - filesystem: "ext3", "btrfs"... expected to be last element of openQA test name
    #   $DESKTOP$             - desktop: just the DESKTOP openQA setting

    "QA:Testcase_Mediakit_Repoclosure": {
        "env": "$SUBVARIANT$",
        "type": "Installation",
    },
    "QA:Testcase_Mediakit_FileConflicts": {
        "env": "$SUBVARIANT$",
        "type": "Installation",
    },
    "QA:Testcase_Boot_default_install": {
        "name": "$SUBVARIANT$_$IMAGETYPE$",
        "section": 'Default boot and install',
        "env": "VM $FIRMWARE$",
        "type": "Installation",
    },
    "QA:Testcase_arm_image_deployment": {
        "name": "$SUBVARIANT$",
        "section": "ARM disk images",
        "env": "Ext boot",
        "type": "Installation"
    },
    "QA:Testcase_install_to_VirtIO": {
        "section": "Storage devices",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_empty": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_User_Interface_Graphical": {
        "section": "User interface",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_User_Interface_Text": {
        "section": "User interface",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_User_Interface_VNC": {
        "section": "User interface",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_User_Interface_VNC_Vncconnect": {
        "section": "User interface",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_User_Interface_serial_console": {
        "section": "User interface",
        "env": "$RUNARCH$",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_user_creation": {
        "section": "Miscellaneous",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_Install_to_Previous_KVM": {
        "section": "Virtualization",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_Install_to_Current_KVM": {
        "section": "Virtualization",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_install_to_NVMe": {
        "section": "Storage devices",
        "env": "$RUNARCH$",
        "type": "Installation",
    },
    "QA:Testcase_install_to_PATA": {
        "section": "Storage devices",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_install_to_SATA": {
        "section": "Storage devices",
        "env": "$RUNARCH$",
        "type": "Installation",
    },
    "QA:Testcase_install_to_SCSI": {
        "section": "Storage devices",
        "env": "$RUNARCH$",
        "type": "Installation",
    },
    "QA:Testcase_install_to_SAS": {
        "section": "Storage devices",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_delete_all": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_multi_select": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_install_to_SCSI": {
        "section": "Storage devices",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_updates.img_via_URL": {
        "section": "Miscellaneous",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_kickstart_user_creation": {
        "section": "Kickstart",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Kickstart_Http_Server_Ks_Cfg": {
        "section": "Kickstart",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_Mirrorlist_graphical": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_HTTP/FTP_graphical": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_HTTP/FTP_variation": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_NFS_graphical": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_NFS_variation": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_NFSISO_variation": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_repository_Hard_drive_variation": {
        "section": "Installation repositories",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Package_Sets_Minimal_Package_Install": {
        "section": "Package sets",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_encrypted": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_delete_partial": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_free_space": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_multi_empty_all": {
        "section": "Guided storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_software_RAID": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_btrfs": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_standard_partition_ext4": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_lvm_ext4": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_lvmthin": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_standard_partition_ext3": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_standard_partition_xfs": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_custom_no_swap": {
        "section": "Custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_blivet_software_RAID": {
        "section": "Advanced custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_blivet_btrfs": {
        "section": "Advanced custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_blivet_lvmthin": {
        "section": "Advanced custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_blivet_standard_partition_ext3": {
        "section": "Advanced custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_blivet_standard_partition_xfs": {
        "section": "Advanced custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_blivet_no_swap": {
        "section": "Advanced custom storage configuration",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_Kickstart_File_Path_Ks_Cfg": {
        "section": "Kickstart",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Kickstart_Hd_Device_Path_Ks_Cfg": {
        "section": "Kickstart",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Kickstart_Nfs_Server_Path_Ks_Cfg": {
        "section": "Kickstart",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_current_minimal": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_current_workstation": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_current_workstation_encrypted": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_current_server": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_current_kde": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_current_any": {
        "section": "Upgrade",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_previous_minimal": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_previous_workstation": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_previous_workstation_encrypted": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_previous_server": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_previous_kde": {
        "section": "Upgrade",
        "env": "x86_64",
        "type": "Installation",
    },
    "QA:Testcase_upgrade_dnf_previous_any": {
        "section": "Upgrade",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_updates.img_via_local_media": {
        "section": "Miscellaneous",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_partitioning_guided_shrink": {
        "section": "Guided storage shrinking",
        "env": "$FS$",
        "type": "Installation",
    },
    "QA:Testcase_Non-English_European_Language_Install": {
        "section": "Internationalization and Localization",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Package_Sets_KDE_Package_Install": {
        "section": "Package sets",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_install_to_iSCSI_no_authentication": {
        "section": "Storage devices",
        "env": "$RUNARCH$",
        "type": "Installation",
    },
    "QA:Testcase_Cyrillic_Language_Install": {
        "section": "Internationalization and Localization",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Arabic_Language_Install": {
        "section": "Internationalization and Localization",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Asian_Language_Install": {
        "section": "Internationalization and Localization",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_updates.img_via_installation_source": {
        "section": "Miscellaneous",
        "env": "Result",
        "type": "Installation",
    },
    "QA:Testcase_Boot_Methods_Pxeboot": {
        "section": "PXE boot",
        "env": "$RUNARCH$",
        "type": "Installation",
    },
    "QA:Testcase_Anaconda_rescue_mode": {
        "section": "Miscellaneous",
        "env": "$BOOTMETHOD$",
        "type": "Installation",
    },
    "QA:Testcase_base_initial_setup": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT$",
        "type": "Base",
    },
    "QA:Testcase_base_startup": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_reboot_unmount": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_system_logging": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_update_cli": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_edition_self_identification": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_services_start": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_selinux": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_base_service_manipulation": {
        "section": "$RUNARCH$",
        "env": "$SUBVARIANT_OR_LOCAL$",
        "type": "$CLOUD_OR_BASE$",
    },
    "QA:Testcase_kickstart_firewall_disabled": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_kickstart_firewall_configured": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_freeipa_trust_server_installation": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_freeipa_trust_server_uninstallation": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_freeipa_replication": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_postgresql_server_installation": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_realmd_join_kickstart": {
        # the section name here is pretty funky and I might change it,
        # so we'll intentionally use an inexact match
        "section": "FreeIPA",
        "env": "Result",
        "type": "Server",
    },
    "QA:Testcase_realmd_join_cockpit": {
        "section": "FreeIPA",
        "env": "Result",
        "type": "Server",
    },
    "QA:Testcase_realmd_join_sssd": {
        "section": "FreeIPA",
        "env": "Result",
        "type": "Server",
    },
    "QA:Testcase_domain_client_authenticate": {
        "env": "Result",
        "type": "Server",
        "name": "(FreeIPA)",
    },
    "QA:Testcase_FreeIPA_realmd_login": {
        "env": "Result",
        "type": "Server",
    },
    "QA:Testcase_database_server_remote_client": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_Remote_Logging": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_upgrade_dnf_current_server_domain_controller": {
        "section": "Upgrade tests",
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_upgrade_dnf_previous_server_domain_controller": {
        "section": "Upgrade tests",
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_desktop_app_basic": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
        # FIXME: this is just hard-coded for now as we do not test
        # any other applications, but we should really use a sub to
        # derive this 'intelligently'
        "name": "terminal",
    },
    "QA:Testcase_desktop_browser": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
    },
    "QA:Testcase_desktop_login": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
    },
    "QA:Testcase_desktop_update_graphical": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
    },
    "QA:Testcase_desktop_update_notification": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
    },
    "QA:Testcase_desktop_error_checks": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
    },
    "QA:Testcase_workstation_core_applications": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
    },
    "QA:Testcase_Printing_New_Printer": {
        "env": "$SUBVARIANT$",
        "type": "Desktop",
        "section": "Release-blocking desktops: <b>x86 / x86_64</b>",
        "name": "virtual printer",
    },
    "QA:Testcase_Server_firewall_default": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_Server_cockpit_default": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_Server_cockpit_basic": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_Server_filesystem_default": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_FreeIPA_web_ui": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_FreeIPA_password_change": {
        "env": "$RUNARCH$",
        "type": "Server",
    },
    "QA:Testcase_Modularity_module_list": {
        "section": "Modularity",
        "env": "Result",
        "type": "Base",
    },
    "QA:Testcase_Modularity_enable-disable_module": {
        "section": "Modularity",
        "env": "Result",
        "type": "Base",
    },
    "QA:Testcase_Modularity_install_module": {
        "section": "Modularity",
        "env": "Result",
        "type": "Base",
    },
    "QA:Testcase_Modularity_update_without_repos": {
        "section": "Modularity",
        "env": "Result",
        "type": "Base",
    },
    "QA:Testcase_Podman": {
        "env": "$RUNARCH$",
        # if we run this on anything but IoT, we may need to change this
        "type": "General",
    },
    "QA:Testcase_Greenboot": {
        "env": "$RUNARCH$",
        "type": "General",
    },
    "QA:Testcase_RpmOstree_Rebase": {
        "env": "$RUNARCH$",
        "type": "General",
    },
    "QA:Testcase_RpmOstree_Package_Layering": {
        "env": "$RUNARCH$",
        "type": "General",
    },
    "QA:Testcase_Clevis": {
        "env": "$RUNARCH$",
        "type": "General",
    },
    "QA:Testcase_Zezere_Ignition": {
        "env": "$RUNARCH$",
        "type": "General",
    },
    #        "": {
    #            "name": "", # optional, use when same testcase occurs on multiple rows with different link text
    #            "section": "", # optional, some result pages have no sections
    #            "env": "x86",
    #            "type": "Installation",
    #            },
}

