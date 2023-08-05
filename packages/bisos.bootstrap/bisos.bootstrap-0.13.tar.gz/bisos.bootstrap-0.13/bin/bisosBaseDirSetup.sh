#! /bin/bash

#
# Running user should have sudo privileges
# 
#

function bisosBaseDirSetup {
    local currentUser=$(id -un)
    local currentUserGroup=$(id -g -n ${currentUser})

    local bisosRoot="/bisos"

    if [ "$( type -t deactivate )" == "function" ] ; then
	deactivate
    fi

    sudo -H pip install --no-cache-dir --upgrade pip

    sudo -H pip install --no-cache-dir --upgrade virtualenv

    sudo -H pip install --no-cache-dir --upgrade --force-reinstall bisos.bx-bases

    sudo mkdir -p "${bisosRoot}"
    sudo chown -R ${currentUser}:${currentUserGroup} "${bisosRoot}"
    bx-bases -v 20 --baseDir="${bisosRoot}" -i pbdUpdate all

    sudo mkdir -p "/de"
    sudo chown -R ${currentUser}:${currentUserGroup} "/de"
    bx-bases -v 20 --baseDir="/de" --pbdName="deRunRoot"  -i pbdUpdate all

    sudo mkdir -p "/bxo"
    sudo chown -R ${currentUser}:${currentUserGroup} "/bxo"
    bx-bases -v 20 --baseDir="/bxo" --pbdName="bxoRoot"  -i pbdUpdate all
}

bisosBaseDirSetup
