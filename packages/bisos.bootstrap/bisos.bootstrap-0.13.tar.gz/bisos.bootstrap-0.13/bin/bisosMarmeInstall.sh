#! /bin/bash

PATH="$PATH:."

bisosRoot="/bisos"
bisosVirtEnvBase="${bisosRoot}/venv/py2-bisos-3"

pkgName=unisos.marme

if [ ! -d "${bisosVirtEnvBase}" ] ; then
    bisosBaseDirSetup.sh
fi
    
bisosPkgInstall.sh "${bisosVirtEnvBase}" ${pkgName}

