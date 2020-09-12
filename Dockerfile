FROM fedora:latest
RUN dnf -y install fedora-messaging pip beaker-client git gcc python-devel 
COPY conf /fedora-release-autotest/conf
COPY fedora_release_autotest /fedora-release-autotest/fedora_release_autotest
COPY setup.py /fedora-release-autotest/
COPY install.requires /fedora-release-autotest/
WORKDIR /fedora-release-autotest
RUN pip install --force-reinstall .
RUN sed -e "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" conf/fedora-release-autotest.toml > /var/my.toml
Run cp conf/data/client.conf /etc/beaker/client.conf
Run cp conf/data/RedHatInternalCA.pem /etc/beaker/RedHatInternalCA.pem
ENTRYPOINT ["fedora-messaging", "--conf", "/var/my.toml", "consume"]
