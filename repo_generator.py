""" iownloaded from http://xbmc-addons.googlecode.com/svn/addons/ """
""" addons.xml generator """

import os
import hashlib

from addons import __ADDONS__


class Generator:
    """
    Generates a new addons.xml file from each addons addon.xml file
    and a new addons.xml.md5 hash file. Must be run from the root of
    the checked-out repo. Only handles single depth folder structure.
    """

    def __init__(self):
        # generate files
        self._generate_addons_file()
        self._generate_md5_file()
        # notify user
        print(f"Finished updating addons xml and md5 files")

    def _generate_addons_file(self):
        # final addons text
        addons_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n'
        # loop thru and add each addons addon.xml file
        for addon in __ADDONS__:
            try:
                # skip any file or .git folder
                if not os.path.isdir(addon):
                    print(f"Addon {addon} does not exist")
                    continue
                # create path
                _path = os.path.join(addon, "addon.xml")
                # split lines for stripping
                xml_lines = open(_path, "r").read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if line.find("<?xml") >= 0:
                        continue
                    # add line
                    addon_xml += line.rstrip() + "\n"
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception as e:
                # missing or poorly formatted addon.xml
                print(f"Excluding {_path} for {e}")
        # clean and add closing tag
        addons_xml = addons_xml.strip() + "\n</addons>\n"
        # save file
        self._save_file(addons_xml, file="tmp/addons.xml")

    def _generate_md5_file(self):
        # create a new md5 hash
        m = hashlib.md5(open("tmp/addons.xml").read().encode("utf-8")).hexdigest()
        self._save_file(m, file="tmp/addons.xml.md5")

    def _save_file(self, data, file):
        with open(file, "w") as fp:
            fp.write(data)


if __name__ == "__main__":
    # start
    Generator()
