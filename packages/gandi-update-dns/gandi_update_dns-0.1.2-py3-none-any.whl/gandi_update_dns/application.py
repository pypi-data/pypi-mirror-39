#!/usr/bin/env python3

import configparser
import json
import logging
import os
import socket
import sys
import textwrap
import urllib.error
import urllib.request
from xdg import XDG_CACHE_HOME, XDG_CONFIG_HOME, XDG_RUNTIME_DIR

logging.basicConfig(level=logging.DEBUG)

IP_GETTER_URL = "https://api.ipify.org"
GANDI_API_URL = "https://dns.api.gandi.net/api/v5/"
DEFAULT_TIME_TO_LIVE = 1800


class GandiDNSApi:
    def __init__(self, domain, api_key):
        self.api = GANDI_API_URL
        self.domain = domain
        self.api_key = api_key

    def get_records(self):
        """Get all DNS records for the current domain"""
        
        url = "{}/domains/{}/records".format(self.api, self.domain)
        logging.debug("Gandi: {}".format(url))
        
        request = urllib.request.Request(url)
        request.add_header("X-Api-Key", self.api_key)
        
        with urllib.request.urlopen(request) as response:
            data = response.read().decode()
        
        return json.loads(data)

    def change_ip(self, old_ip, new_ip):
        """Change an old IP to a newest one"""
        
        logging.debug("Change current ip for {}: {}".format(self.domain, new_ip))
        records = self.get_records()
        
        # for every record found on that domain
        for r in records:
            rName = r["rrset_name"]
            rType = r["rrset_type"]
            rValues = r["rrset_values"]
            
            # if record type is A and old ip appears in values
            if rType == 'A' and old_ip in rValues:
                
                url = "{}/domains/{}/records/{}/{}".format(self.api, self.domain, rName, rType)
                logging.debug("Gandi: {}".format(url))
                
                request = urllib.request.Request(
                    url,
                    method="PUT",
                    headers={
                        "Content-Type": "application/json",
                        "X-Api-Key": self.api_key
                    },
                    data=json.dumps({
                        "rrset_ttl": DEFAULT_TIME_TO_LIVE,
                        "rrset_values": [new_ip],
                    }).encode()
                )
                
                with urllib.request.urlopen(request) as response:
                    data = response.read().decode()
                    logging.debug(json.loads(data))
                    

class Application:
    def __init__(self):
        runtime_dir = XDG_RUNTIME_DIR or "/tmp"
        self._pid_file = os.path.join(runtime_dir, "gandi-update-dns.pid")
        self._save_file = os.path.join(XDG_CACHE_HOME, "my-public-ip")
        self._config_file = os.path.join(XDG_CONFIG_HOME, "gandi-update-dns.conf")
        self._hostname = socket.getfqdn()
        
    def lock(self):
        """Create PID file"""
        if os.path.isfile(self._pid_file):
            raise Exception("Application already launched!")
        
        pid = str(os.getpid())
        open(self._pid_file, 'w').write(pid)
        logging.debug(self._pid_file + " locked")
        
    def unlock(self):
        """Unlock PID file"""
        os.unlink(self._pid_file)
        logging.debug(self._pid_file + " unlocked")
        
    def create_config(self):
        """Create a basic configuration file"""
        logging.debug("Init config file")
        print("You don't have any configuration at the moment. Please enter some information to continue.")
        fqdn = input("FQDN: ")
        api_key = input("Gandi API key: ")
        
        config = configparser.ConfigParser()
        config[fqdn] = {
            'GandiAPIKey': api_key
        }
        
        with open(self._config_file, 'w') as config_file:
            config.write(config_file)
            
        os.chmod(self._config_file, 0o600)
        
    def read_config(self):
        """Read the configuration file"""
        logging.debug("Looking for config file: {}". format(self._config_file))
        if not os.path.isfile(self._config_file):
            self.create_config()
            
        config = configparser.ConfigParser()
        config.read(self._config_file)
        return config
        
    def get_last_known_ip(self):
        """Read the last known IP from the save file"""
        if not os.path.isfile(self._save_file):
            logging.debug("No last IP found")
            return None
        
        with open(self._save_file, 'r') as f:
            ip = f.read()
        return ip.strip()
        
    def get_current_ip(self, provider_url=IP_GETTER_URL):
        """Get current IP from external service"""
        try:
            request = urllib.request.urlopen(provider_url)
            return request.read().decode().strip()
        except urllib.error.URLError as e:
            logging.error("Could not retrieve public IP: " + e.reason)
            return None
    
    def save_current_ip(self, ip):
        """Save current IP into the save file"""
        logging.debug("Save current ip: {}".format(ip))
        with open(self._save_file, 'w') as f:
            f.write(ip)

    def send_message(self, msg):
        """Send a message"""
        try:
            from send_sms_freemobile.client import FreeClient
        except ImportError:
            logging.warn("Could not send message, package send-sms-freemobile is not installed.")
            return
            
        client = FreeClient()
        client.load_default_config_file()
        status, value = client.send_sms(msg)

        if status != 200:
            logger.warn("Message not sent: {}".format(msg))
        
    def run(self):
        self.lock()
        
        try:
            config = self.read_config()
            logging.debug("{} domain(s) found in configuration".format(len(config.sections())))

            domains = config.sections()
            if not domains:
                logging.error("No domains known")
                return
            
            last_ip = self.get_last_known_ip()
            current_ip = self.get_current_ip()
            
            if not current_ip:
                logging.error("No current IP is known.")
                return
            
            logging.debug("{} == {}".format(last_ip, current_ip))
            if last_ip == current_ip:
                logging.debug("IP didn't change, quit here")
                return
                
            print("Last IP: {}, current IP: {}".format(last_ip, current_ip))
            
            # for every domain in config file
            updated_domains = []
            for domain in domains:
                
                logging.debug("Apply changes to {}...".format(domain))
                
                try:
                    
                    # looking for a gandi api key
                    gandi_key = config[domain].get("GandiAPIKey", None)
                    if gandi_key:
                        api = GandiDNSApi(domain, gandi_key)
                        api.change_ip(last_ip, current_ip)
                        updated_domains.append(domain)
                        logging.debug("Domain {} done!".format(domain))
                    
                    else:
                        logging.warning("Could not change IP for domain {}".format(domain))
                
                except Exception as ex:
                    logging.error("Error when changing IP to domain {}".format(domain))
                    logging.exception(ex)

            # save current ip only if at least if one domain is updated
            if updated_domains:
                self.save_current_ip(current_ip)

            msg = "Adresse IP modifiée !\n"
            msg += "\n"
            msg += "Domaine(s): {}\n".format(", ".join(domains))
            msg += "Ancienne IP: {}\n".format(last_ip)
            msg += "Nouvelle IP: {}\n".format(current_ip)
            msg += "\n"

            if not updated_domains:
                msg += "Aucun domaine n'a été mis à jour ! Merci de faire le nécessaire !\n"
                msg += "\n"

            msg += "Biz !\n"
            msg += self._hostname

            if msg:
                logging.debug("Send message to administrator...")
                self.send_message(msg)
            
        finally:
            self.unlock()
    
    
if __name__ == '__main__':
    print("Try to run `gandi-update-dns` or `poetry run gandi-update-dns` if you are a developer!")
    sys.exit(1)
