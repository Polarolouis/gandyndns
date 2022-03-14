# gandyndns
The purpose of this script is to change *on execution* the IP address of a Gandi.net DNS record (default is to change the DNS @.example.com A record) 
and replacing the IP with the public IP of the machine of execution. The goal is to provide a dynamic change of DNS record like DynDNS, DuckDNS, etc for Gandi.net domains.

This script was inspired by matt1's gandi-ddns script : [matt1/gandi-ddns](https://github.com/matt1/gandi-ddns)

## Usage
The script was designed to be run using a cron task :

```
sudo crontab -e
```

And then to execute every *15 minutes* write in the crontab :  

```
 */15 * * * * python /opt/services/scripts/gandyndns.py
```
