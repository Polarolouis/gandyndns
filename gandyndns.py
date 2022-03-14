#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lordof20th

import requests

# Defines the URL to access the API and the resource
fqdn = "example.com"
rrset_name = "@"
rrset_type = "A"
apiUrl = f"https://api.gandi.net/v5/livedns/domains/{fqdn}/records/{rrset_name}/{rrset_type}"

# Define the headers to use for the API
apikey = "account-api-key"
headers={"Authorization": f"Apikey {apikey}", 'User-Agent': 'Mozilla/5.0', "Content-Type": "application/json"}


def retrieve_dns_IP(headers, apiUrl):
    """Retrieves the IP in the DNS record using the fqdn, rrset_name (for instance subdomain like www etc) and rrset_type (the DNS record type A, CNAME ...).
    
    The function uses requests library and connect to Gandi.net API
    
    Returns:
            retrievedDnsIp (str): string of the IP address in the DNS record"""
    
    response = requests.get(apiUrl, headers=headers)

    responseJson = response.json()  # IPs are stored in a list as string
    retrievedDnsIp = responseJson['rrset_values'][0]
    return retrievedDnsIp

def retrieve_public_IP():
    """Retrieves the public IP by connecting to ipinfo.io API
    
    Returns:
            data['ip'] (str) : string of the public IP address"""
    endpoint = "https://ipinfo.io/json"
    response = requests.get(endpoint, verify = True)
    
    data = response.json()
    return data['ip']

def update_dns_IP(apiUrl, headers, currentPublicIP):
    """Updates the IP in the DNS record using the IP provided (acquired by retrieve_public_IP)"""
    data = {
    "rrset_values": [currentPublicIP]
    }

    requests.put(url=apiUrl, headers=headers, json=data)

def main():
    dnsIP = retrieve_dns_IP(headers, apiUrl)

    currentPublicIP = retrieve_public_IP()

    if dnsIP != currentPublicIP: # We need to update the A record to match our IP
        update_dns_IP(apiUrl, headers, currentPublicIP)
        print(f"Old IP : {dnsIP} replaced -> by New IP : {currentPublicIP}")
    else:
        print("IPs are the same.")

if __name__ == "__main__":
    main()