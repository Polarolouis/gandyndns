#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lordof20th

import requests
import argparse

parser = argparse.ArgumentParser(
    description="A script which connect to Gandi.net API to change IP associated to a DNS record")
parser.add_argument("-v", "--verbose",
                    help="Enable verbose mode", action="store_true")
parser.add_argument("domain", metavar="DOMAIN",
                    help="The domain for which you want to write a DNS record. Example: example.com")
parser.add_argument("subdomain", metavar="SUBDOMAIN",
                    help="The subdomain to point to. Examples: 'sub' or '@'")
parser.add_argument("apikey", metavar="APIKEY", help="Your Gandi.net API key")
parser.add_argument("--type", metavar="TYPE", default='A',
                    help="The type of DNS record to create. Default: A")

args = parser.parse_args()
print(args)

verbose = args.verbose
domain = args.domain
apikey = args.apikey
subdomain = args.subdomain
type = args.type

domain_record_string = f"DNS {type} record for {subdomain}.{domain}"

domain_record_string_lenght = len(domain_record_string)

apiUrl = f"https://api.gandi.net/v5/livedns/domains/{domain}/records/{subdomain}/{type}"

headers = {"Authorization": f"Apikey {apikey}",
           'User-Agent': 'Mozilla/5.0', "Content-Type": "application/json"}


def retrieve_public_IP():
    """Retrieves the public IP by connecting to ipinfo.io API

    Returns:
            data['ip'] (str) : string of the public IP address"""
    endpoint = "https://ipinfo.io/json"
    response = requests.get(endpoint, verify=True)

    data = response.json()
    return data['ip']


def retrieve_dns_IP(apiUrl, headers):
    """Retrieves the IP in the DNS record using the domain, rrset_name (for instance subdomain like www etc) and rrset_type (the DNS record type A, CNAME ...).

    The function uses requests library and connect to Gandi.net API

    Returns:
            retrievedDnsIp (str): string of the IP address in the DNS record"""
    if verbose:
        print("Retrieving the DNS IP")
    response = requests.get(apiUrl, headers=headers)

    responseJson = response.json()  # IPs are stored in a list as string
    try:
        retrievedDnsIp = responseJson['rrset_values'][0]
    except KeyError as key_error:
        print(
            f"{key_error} means the record doesn't exist, we'll return an empty string instead")
        retrievedDnsIp = ""
    return retrievedDnsIp


def update_dns_IP(apiUrl, headers):
    """Updates the IP in the DNS record using the IP provided (acquired by retrieve_public_IP) if it is different from the DNS IP"""
    publicIP = retrieve_public_IP()
    dnsIP = retrieve_dns_IP(apiUrl, headers)
    if verbose:
        print(f"Public IP is : {publicIP}")
        if dnsIP:
            print(f"DNS IP is : {dnsIP}")
        else:
            print("The subdomain doesn't exist, no DNS IP associated")
    if not publicIP == dnsIP:
        if verbose:
            print("IPs do not match, setting DNS IP")
        data = {
            "rrset_values": [publicIP]
        }
        print(f"{domain_record_string : <{domain_record_string_lenght}} | Old IP : {dnsIP} replaced -> by New IP : {publicIP}")
        response = requests.put(url=apiUrl, headers=headers, json=data)
        if verbose:
            print(f"Request exited with status code : {response.status_code}")
    else:
        print(
            f"{domain_record_string : <{domain_record_string_lenght}} | {'IPs are the same.':<17}")


if __name__ == '__main__':
    update_dns_IP(apiUrl, headers)
