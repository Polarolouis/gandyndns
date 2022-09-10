#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: polarolouis

import argparse
import requests

parser = argparse.ArgumentParser(
    description="A script which connect to Gandi.net API to change IP associated to a DNS record")
parser.add_argument("-v", "--verbose",
                    help="Enable verbose mode", action="store_true")
parser.add_argument("domain", metavar="DOMAIN",
                    help="The domain for which you want to write a DNS record. Example: example.com")
parser.add_argument("subdomain", metavar="SUBDOMAIN",
                    help="The subdomain to point to. Examples: 'sub' or '@'")
parser.add_argument("apikey", metavar="APIKEY", help="Your Gandi.net API key")
parser.add_argument("--destination", metavar="DESTINATION", default="public_ip",
                    help="The destination to point the subdomain to. Might be an IP, for instance 10.0.0.1, might be a subdomain, for instance @. Default: public_ip, which retrieves the machine public ip")
parser.add_argument("--type", metavar="TYPE", default='A',
                    help="The type of DNS record to create. Default: A", choices=['A', 'CNAME'])
parser.add_argument("--ttl", metavar="TTL", default=10800,
                    help="The Time To Live in seconds. This is the number of seconds the record must be stored in cache. Default value is 10800s (3hrs).", type=int)
args = parser.parse_args()
print(args)

verbose = args.verbose
domain = args.domain
apikey = args.apikey
subdomain = args.subdomain
record_type = args.type
ttl = args.ttl
destination = args.destination

domain_record_string = f"DNS {record_type} record for {subdomain}.{domain}"

domain_record_string_lenght = len(domain_record_string)

api_url = f"https://api.gandi.net/v5/livedns/domains/{domain}/records/{subdomain}/{record_type}"

headers = {"Authorization": f"Apikey {apikey}",
           'User-Agent': 'Mozilla/5.0', "Content-Type": "application/json"}


def retrieve_public_ip():
    """Retrieves the public IP by connecting to ipinfo.io API

    Returns:
            data['ip'] (str) : string of the public IP address"""
    endpoint = "https://ipinfo.io/json"
    response = requests.get(endpoint, verify=True)

    data = response.json()
    return data['ip']


def retrieve_dns_ip(api_url, headers):
    """Retrieves the IP in the DNS record using the domain, rrset_name (for instance subdomain like www etc) and rrset_type (the DNS record type A, CNAME ...).

    The function uses requests library and connect to Gandi.net API

    Returns:
            retrieved_dns_ip (str): string of the IP address in the DNS record"""
    if verbose:
        print("Retrieving the DNS IP")
    response = requests.get(api_url, headers=headers)

    response_json = response.json()  # IPs are stored in a list as string
    try:
        retrieved_dns_ip = response_json['rrset_values'][0]
        retrieved_ttl = response_json['rrset_ttl']
    except KeyError as key_error:
        print(
            f"{key_error} means the record doesn't exist, we'll return an empty string instead")
        retrieved_dns_ip = ""
    return retrieved_dns_ip, retrieved_ttl


def update_dns_ip(api_url, headers):
    """Updates the IP in the DNS record using the IP provided (acquired by retrieve_public_ip) if it is different from the DNS IP"""
    if destination == "public_ip":
        public_ip = retrieve_public_ip()
    else:
        public_ip = destination
    dns_ip, dns_ttl = retrieve_dns_ip(api_url, headers)
    if verbose:
        print(f"Public IP is : {public_ip}")
        if dns_ip:
            print(f"DNS IP is : {dns_ip}")
        else:
            print("The subdomain doesn't exist, no DNS IP associated")
        print(f"DNS TTL is {dns_ttl}")
    if public_ip != dns_ip or dns_ttl != ttl:

        data = dict()

        data["rrset_values"] = [public_ip]
        print(f"{domain_record_string : <{domain_record_string_lenght}} | Old IP : {dns_ip} replaced -> by New IP : {public_ip}")
        print(f"{domain_record_string : <{domain_record_string_lenght}} | Old TTL : {dns_ttl} replaced -> by New IP : {ttl}")

        if dns_ttl != ttl:
            data["rrset_ttl"] = ttl
            if verbose:
                print(
                    f"TTL are differents. DNS TTL {dns_ttl} where wanted TTL is {ttl}")

        if verbose:
            print(f"The data to be sent is : {data}")
        response = requests.put(url=api_url, headers=headers, json=data)
        if verbose:
            print(f"Request exited with status code : {response.status_code}")
    else:
        if public_ip == dns_ip:
            print(
                f"{domain_record_string : <{domain_record_string_lenght}} | {'IPs are the same.':<17}")
        if dns_ttl == ttl:
            print(
                f"{domain_record_string : <{domain_record_string_lenght}} | {'TTL are the same':<17}")


if __name__ == '__main__':
    update_dns_ip(api_url, headers)
