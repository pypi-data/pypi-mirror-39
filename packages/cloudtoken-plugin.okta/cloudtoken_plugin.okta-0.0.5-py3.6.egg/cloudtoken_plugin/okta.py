# OKTA plugin for cloudtoken.
#
# You will need to add the key 'okta_url' with the value being the URL for your OKTA IdP, for example:
#
# okta_url: !!str 'https://{{example}}.okta.com
#
# Author: Andy Loughran (andy@lockran.com)

import argparse
import json
import re
import tkinter
import tkinter.simpledialog
import xml.etree.ElementTree as Et
from os import system
from platform import system as platform

import requests
from botocore.compat import urlsplit
from bs4 import BeautifulSoup


def grabFocus():
    if platform() == 'Darwin':  # How Mac OS X is identified by Python
        system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')
    else:
        # Explicity ignore other OS versions.
        pass

class Plugin(object):
    def __init__(self, config):
        self._config = config
        self._name = 'okta'
        self._description = 'Authenticate against OKTA.'
        self._authurl = "api/v1/authn"
        self._headers = {
            'Accept': 'application/json', 
            'Content-Type': 'application/json'
        }
        self._content_options = {
            'multiOptionalFactorEnroll': 'true',
            'warnBeforePasswordExpired': 'true'
            }
        try:
            self._gui = config['gui']
        except KeyError:
            self._gui = False
        try:
            self._url = config['okta_url']
            host = re.search(r'(https?://[\w\-.]+)/', url).group(1)
        except KeyError:
            print("Configuration key 'okta_url' not found. Exiting.")
            exit(1)
        except AttributeError:
            print("Configuration key 'okta_url' value does not seem to be a http(s) URL. Exiting.")
            exit(1)
        

    def __str__(self):
        return __file__

    @staticmethod
    def unset(args):
        pass

    @staticmethod
    def arguments(defaults):
        parser = argparse.ArgumentParser()
        return parser

    def execute(self, data, args, flags):
        url = self._url
        
        if self._gui == True:
            root = tkinter.Tk()
            root.title("CloudToken")
            root.withdraw()
            root.overrideredirect(True)
            root.geometry('0x0+0+0')
            if platform() == 'Darwin':  # How Mac OS X is identified by Python
                    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        requests.packages.urllib3.disable_warnings()  # Disable warning for self signed certs.
        session = requests.session()

        content = {}
        content['username'] = args.username
        content['password'] = args.password
        content['options'] = self._content_options

        fullurl = "https://{}/{}".format(urlsplit(url).netloc, self._authurl)

        r = session.post(fullurl, headers=self._headers, data=json.dumps(content))
        response = json.loads(r.text)
        try:
            token = response['stateToken']
            id = response['_embedded']['factors'][0]['id']
        except KeyError:
            print("There has been an authentication error")
            exit(1);

        verifyurl = "{}/factors/{}/verify".format(fullurl, id)
        vcontent = {}
        vcontent['stateToken'] = token

        # GET MFA Code
        if not gui:
            selection = input("Please enter your MFA code: ")
            vcontent['passCode'] = selection
        elif gui == True:
            root.call('wm', 'attributes', '.', '-topmost', '1')
            grabFocus()
            vcontent['passCode'] = tkinter.simpledialog.askstring(
                "MFA Code", "Enter your MFA code"
            )
        # Post MFA code to get Token.
        v = session.post(verifyurl, headers=headers, data=json.dumps(vcontent)) 
        sToken = json.loads(v.text)['sessionToken']
        saml_url = "{}?sessionToken={}".format(url, sToken)
        response = session.get(saml_url)
        soup = BeautifulSoup(response.text, "html.parser")
        saml = soup.find("input", attrs={"name": "SAMLResponse"})
        r = saml['value']
        data.append({'plugin': self._name, 'data': r})
        return data
