# swift-archive

![](https://github.com/kevincoakley/swift-archive/workflows/Python%20package/badge.svg)
![](https://github.com/kevincoakley/swift-archive/workflows/Docker%20Image%20CI/badge.svg)
[![Code Coverage](https://codecov.io/gh/kevincoakley/swift-archive/branch/master/graph/badge.svg)](https://codecov.io/gh/kevincoakley/swift-archive/)

Install swift-archive from source:

    $ git clone https://github.com/kevincoakley/swift-archive.git
    $ cd swift-archive
    $ pip install -r requirements.txt
    $ python setup.py install
    
Command line options and environment variables:

    $ swift-archive
    --debug
    --os-username [OS_USERNAME] - OpenStack Keystone Username. (Required)
    --os-password [OS_PASSWORD] - OpenStack Keystone Password. (Required)
    --os-project-name [OS_PROJECT_NAME] - OpenStack Keystone Project Name. (Required)
    --os-auth-url [OS_AUTH_URL] - OpenStack Keystone Auth URL. (Required)
    --container [CONTAINER] - OpenStack Swift Container. (Required)
    --archive-path [ARCHIVE_PATH] - Local Path to Archive to OpenStack Swift. (Required)
    --delete [LOCAL_DELETE] - Delete Local Files Once Uploaded to Swift. (Default False)
    --seconds-since-updated [SECONDS_SINCE_UPDATED] - Archive All Files That Haven't Been Updated Since in Seconds. (Default 0)

Build swift-archive into a Docker container:

    $ git clone https://github.com/kevincoakley/swift-archive.git
    $ cd swift-archive
    $ docker build . --file Dockerfile --tag swift-archive
    
Run swift-archive from a Docker container:

    docker run --name swift-archive --rm \
    -e OS_USERNAME='username' \
    -e OS_PASSWORD='password' \
    -e OS_PROJECT_NAME='project-name' \
    -e OS_AUTH_URL='https://keystone:5000' \
    -e CONTAINER='container' \
    -e ARCHIVE_PATH='/swift-archive/' \
    -e LOCAL_DELETE='/False/' \
    -e SECONDS_SINCE_UPDATED='600' \
    -v '/local/path:/swift-archive/' \
    swift-archive