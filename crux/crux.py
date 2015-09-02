
import requests
import xml.etree.ElementTree as ElementTree
from tempfile import TemporaryFile


class CrxPackageClient:

    def __init__(self, endpoint, userid, password):
        self.endpoint = endpoint
        self.userid = userid
        self.password = password
        self.session = requests.Session()
        self.session.auth = (self.userid, self.password)

    def _package_list_xml_to_dict(self, package_list_xml):
        packages = {}
        root = ElementTree.fromstring(package_list_xml)
        # root = tree.getroot()
        for package in root.iter('package'):
            package_name = package.find('name').text
            packages[package_name] = {}
            for element in package:
                packages[package_name][element.tag] = element.text
        return packages

    def package_list(self):
        endpoint = self.endpoint
        s = self.session
        url = '/'.join([endpoint, 'crx/packmgr/service.jsp?cmd=ls'])
        r = s.post(url)
        return self._package_list_xml_to_dict(r.text)

    def export_package(self, group, zipname):
        endpoint = self.endpoint
        s = self.session
        f = TemporaryFile()
        url = '/'.join([endpoint, 'crx/packmgr/download.jsp?_charset_=utf-8&' +
                        'path=/etc/packages', group, zipname])
        r = s.get(url, stream=True)
        for bytes in r.iter_content(chunk_size=4096):
            f.write(bytes)
        return f
