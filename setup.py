from setuptools import setup, Command



setup(
    name="fedora-release-autotest",
    version="1.0",
    description="Listens to ci messages for compose complete and"
    "trigger beaker jobs",
    author="Lili Nie",
    author_email="lnie@fedoraproject.org",
    license="GPLv2+",
    url="https://pagure.io/fedora-release-autotest",
    packages=["fedora_release_autotest"],
    include_package_data=True,
    install_requires=open('install.requires').read().splitlines(),
)
