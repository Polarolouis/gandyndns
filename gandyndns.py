#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lordof20th

import requests

class GanDynDns:
    def __init__(self, fqdn, rrset_name, rrset_type, apikey) -> None:
        self.fqdn = fqdn
        self.rrset_name = rrset_name
        self.rrset_type = rrset_type
        self.domain_record_string = f"DNS {self.rrset_type} record for {self.rrset_name}.{self.fqdn}"
        self.apiUrl = f"https://api.gandi.net/v5/livedns/domains/{fqdn}/records/{rrset_name}/{rrset_type}"
        self.headers = {"Authorization": f"Apikey {apikey}", 'User-Agent': 'Mozilla/5.0', "Content-Type": "application/json"}
        self.update_dns_IP()

    def retrieve_dns_IP(self):
        """Retrieves the IP in the DNS record using the fqdn, rrset_name (for instance subdomain like www etc) and rrset_type (the DNS record type A, CNAME ...).
        
        The function uses requests library and connect to Gandi.net API
        
        Returns:
                retrievedDnsIp (str): string of the IP address in the DNS record"""
        
        response = requests.get(self.apiUrl, headers=self.headers)

        responseJson = response.json()  # IPs are stored in a list as string
        try:
            retrievedDnsIp = responseJson['rrset_values'][0]
        except KeyError as key_error:
            print(f"{key_error} means the record doesn't exist, we'll return an empty string instead")
            retrievedDnsIp =""
        return retrievedDnsIp

    def retrieve_public_IP(self):
        """Retrieves the public IP by connecting to ipinfo.io API
        
        Returns:
                data['ip'] (str) : string of the public IP address"""
        endpoint = "https://ipinfo.io/json"
        response = requests.get(endpoint, verify = True)
        
        data = response.json()
        return data['ip']

    def ips_are_equals(self):
        """The method compares both IPs and returns a boolean for the equality test
        
        Returns:
                (bool) : result of the IP equality test"""
        self.currentPublicIP = self.retrieve_public_IP()
        self.dnsIP = self.retrieve_dns_IP()
        return self.currentPublicIP == self.dnsIP

    def update_dns_IP(self):
        """Updates the IP in the DNS record using the IP provided (acquired by retrieve_public_IP) if it is different from the DNS IP"""
        
        if not self.ips_are_equals():
            data = {
            "rrset_values": [self.currentPublicIP]
            }
            print(f"{self.domain_record_string : <40} | Old IP : {self.dnsIP} replaced -> by New IP : {self.currentPublicIP}")
            requests.put(url=self.apiUrl, headers=self.headers, json=data)
        else:
            print(f"{self.domain_record_string : <40} | {'IPs are the same.':<17}")

main = GanDynDns("example.org", "@", "A", "your-api-key")