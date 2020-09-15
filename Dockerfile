FROM fedora:latest
RUN dnf -y install fedora-messaging pip beaker-client git gcc python-devel 
RUN useradd --create-home --no-log-init --shell /bin/bash lnie
RUN echo 'lnie:redhattest' | chpasswd
COPY conf/data/client.conf  /etc/beaker/client.conf
COPY conf/data/RedHatInternalCA.pem /etc/beaker/RedHatInternalCA.pem
COPY fedora_release_autotest /fedora-release-autotest/fedora_release_autotest
COPY conf /fedora-release-autotest/conf
COPY setup.py /fedora-release-autotest/
COPY install.requires /fedora-release-autotest/
RUN mkdir /.openidc/
RUN touch /.openidc/oidc_wikitcms.json
WORKDIR /fedora-release-autotest
RUN cp conf/data/oidc_wikitcms.json /.openidc/oidc_wikitcms.json
RUN chmod 777 /.openidc/oidc_wikitcms.json
RUN sed -e "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" conf/fedora-release-autotest.toml > /tmp/my.toml
RUN pip install --force-reinstall  .
ENTRYPOINT ["fedora-messaging", "--conf", "/tmp/my.toml", "consume"]
