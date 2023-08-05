#! /bin/bash

#
# Running user should have sudo privileges
# 
#

function bisosBaseDirSetup {
    local currentUser=$(id -un)
    local currentUserGroup=$(id -g -n ${currentUser})

    local bisosRoot="/bisos"

    if [ $( type -t deactivate ) == "function" ] ; then
	deactivate
    fi

    sudo -H pip install --no-cache-dir --upgrade pip

    sudo -H pip install --no-cache-dir --upgrade virtualenv

    sudo mkdir -p "${bisosRoot}"
    sudo chown -R ${currentUser}:${currentUserGroup} "${bisosRoot}"

    sudo -H pip install --no-cache-dir --upgrade bisos.bx-bases

    bx-bases -v 20 --baseDir="${bisosRoot}" -i pbdUpdate all
}

bisosBaseDirSetup
