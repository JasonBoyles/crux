
import json
import logging
import os
import requests
import subprocess
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
        url = '/'.join([endpoint, 'crx/packmgr/download.jsp'])
        params = {'_charset': 'utf-8',
                  'path': '/etc/packages/{}/{}'.format(group, zipname)}
        r = s.get(url, params=params, stream=True)
        for bytes in r.iter_content(chunk_size=4096):
            f.write(bytes)
        f.seek(0)
        return f

    def upload_package(self, package_file, name, force=True, install=False):
        endpoint = self.endpoint
        session = self.session
        logging.debug('endpoint is {}'.format(endpoint))
        url = '/'.join([endpoint, 'crx/packmgr/service.jsp'])
        logging.debug('url is {}'.format(url))
        force = (force and 'true' or 'false')
        install = (install and 'true' or 'false')
        form = {
            'file':
                (package_file,
                 open(package_file, 'rb'),
                 'application/zip',
                 {}),
            'name': name,
            'force': force,
            'install': install
        }
        logging.debug('install is {} and force is {}'.format(install, force))
        response = session.post(url, files=form)
        logging.debug(
            'response status_code is:\n{}'.format(response.status_code))
        logging.debug('response text is:\n{}'.format(response.text))
        return True
