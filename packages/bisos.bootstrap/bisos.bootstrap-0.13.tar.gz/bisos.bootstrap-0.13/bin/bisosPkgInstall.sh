#! /bin/bash

function echoErr { echo "E: $@" 1>&2; }
function echoAnn { echo "A: $@" 1>&2; }
function echoOut { echo "$@"; }


function bisosFoundationPkgsInstall {
    pip install --no-cache-dir --upgrade unisos.common
    pip install --no-cache-dir --upgrade bisos.common
    pip install --no-cache-dir --upgrade bisos.bx-bases    
}

function bisosPkgInstall {

    if [ $# -ne 2 ] ; then
	echoErr "Bad Nu Of Args -- Expected 2 -- Got $#"
	return
    fi

    local virtEnv="$1"
    local pkgName="$2"

    
    if [ "$( type -t deactivate )" == "function" ] ; then
	echoAnn "Deactivating"
	deactivate
    fi

    source ${virtEnv}/bin/activate

    bisosFoundationPkgsInstall    
    
    pip install --no-cache-dir --upgrade "${pkgName}"
}

bisosPkgInstall $@

