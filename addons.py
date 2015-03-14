
_BEAM_ = ["service.subtitles.titulky.com","service.subtitles.serialzone.cz"]
# list of addons that we are releasing

__ADDONS__ = [
    "plugin.video.barrandov.tv",
    "plugin.video.befun.cz",
    "plugin.video.gordon.ura.cz",
    "plugin.video.hejbejse.tv",
    "plugin.video.jaksetodela.cz",
    "plugin.video.joj.sk",
    "plugin.video.koukni.cz",
    "plugin.video.markiza.sk",
    "plugin.video.mixer.cz",
    "plugin.video.mtr.sk",
    "plugin.video.online-files",
    "plugin.video.pohadkar.cz",
    "plugin.video.rtvs.sk",
    "plugin.video.sosac.ph",
    "plugin.video.sledujuserialy.cz",
    "plugin.video.ta3.com",
    "plugin.video.teevee.sk",
    "plugin.video.tv.sosac.ph",
    "plugin.video.videacesky.cz",
    "plugin.video.zkouknito.cz",
    "script.module.stream.resolver",
    "repository.xbmc.doplnky",
    "repository.dmd-xbmc.googlecode.com",
    "repository.kodi-czsk"
    ] + _BEAM_

import os
import requests
import xml.etree.ElementTree as ET
from addons import __ADDONS__

# this function asks our repository and returns addons with different versions than in our local repo = candidates to be
# released
def find():
    released_addons = requests.get('http://kodi-czsk.github.io/repository/repo/addons.xml').text
    try:
        root = ET.XML( released_addons.encode('utf-8') )
    except: # initially there are no addons.xml
        print 'Failed to parse remove addons.xml - releasing everything'
        return __ADDONS__    
    to_release = []
    for id in __ADDONS__:
        released = root.find('addon[@id=\"%s\"]' % id)
        if released == None:
            to_release.append(id)
            continue
        released_version = released.get('version')
        xmldoc = ET.parse(os.path.join(id,'addon.xml'))
        new_version =xmldoc.getroot().get('version')
        if not released_version == new_version:
            to_release.append(id)
    return to_release

if __name__ == "__main__":
    for id in find():
        print "Addon %s " % id
