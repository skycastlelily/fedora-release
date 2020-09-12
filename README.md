Fedora release autotest tools
================================
1) Installing 

 $git clone https://pagure.io/fedora-release-autotest
 $cd fedora-release-autotest
 $pip install .

2) How to use it
 First, you should install fedora-messaging and beaker-client 
 $sudo dnf install -y fedora-messaging beaker-client

 Second,modify /etc/beaker/client.conf to make sure that you have access to beaker server,
 and check if it works with: 
 $bkr whoami

 Then,create a configuration file called my_config.toml with a unique queue name for your consumer
 $sed -e "s/[0-9a-f]\{8\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{4\}-[0-9a-f]\{12\}/$(uuidgen)/g" \
    conf/fedora-release-autotest.toml > my_config.toml

 Last,start the service
 $fedora-messaging --conf my_config.toml consume
