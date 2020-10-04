FROM fedora-base
RUN dnf -y install fedora-messaging pip beaker-client git gcc python-devel systemd 
COPY . /fedora-release-autotest/
WORKDIR /fedora-release-autotest
RUN sed -e "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" conf/fedora-release-autotest.toml > /tmp/my.toml
RUN pip install --force-reinstall  .
RUN pip install resultsdb_conventions
ENTRYPOINT ["fedora-messaging", "--conf", "/tmp/my.toml", "consume"]
