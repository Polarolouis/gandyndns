# gandyndns
The purpose of this script is to change *on execution* the IP address of a Gandi.net DNS record (default is to change the DNS @.example.com A record) 
and replacing the IP with the public IP of the machine on which the code is executed. The goal is to provide a dynamic change of DNS record like DynDNS, DuckDNS, etc for Gandi.net domains.

This script was inspired by matt1's gandi-ddns script : [matt1/gandi-ddns](https://github.com/matt1/gandi-ddns)

## Usage

```
usage: gandyndns.py [-h] [-v] [--type TYPE] DOMAIN SUBDOMAIN APIKEY

A script which connect to Gandi.net API to change IP associated to a DNS record

positional arguments:
  DOMAIN         The domain for which you want to write a DNS record. Example: example.com
  SUBDOMAIN      The subdomain to point to. Examples: 'sub' or '@'
  APIKEY         Your Gandi.net API key

options:
  -h, --help     show this help message and exit
  -v, --verbose  Enable verbose mode
  --type TYPE    The type of DNS record to create. Default: A
```

Each time the script runs it check if *the IPs in the DNS record* match the *current public IP* and if they dont use a PUT request to apply the new IP to the DNS.

## Automation : **Run the script using a cron task**

```bash
sudo crontab -e
```

And then to execute *every X minutes* (where X should be an integer between 1 and 59) write in the crontab :  

```
 */X * * * * python /path/to/script/gandyndns.py example.com @ my-api-key
```
