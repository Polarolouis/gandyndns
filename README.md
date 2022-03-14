# gandyndns
The purpose of this script is to change *on execution* the IP address of a Gandi.net DNS record (default is to change the DNS @.example.com A record) 
and replacing the IP with the public IP of the machine on which the code is executed. The goal is to provide a dynamic change of DNS record like DynDNS, DuckDNS, etc for Gandi.net domains.

This script was inspired by matt1's gandi-ddns script : [matt1/gandi-ddns](https://github.com/matt1/gandi-ddns)

## Usage
1. **Define an object of class GanDynDns at the end of the file** : 
```
main = GanDynDns("example.org", "@", "A", "your-api-key")
```
Or if you want to define multiple domains to update :

```
domain = "example.org"
apikey = "your-api-key"

main = GanDynDns(domain, "@", "A", apikey)
mail = GanDynDns(domain, "mail", "A" apikey)
```
Each time the script runs and the objects are created they check if *the IPs in the DNS record* match the *current public IP*.

2. **Run the script using a cron task** :

```
sudo crontab -e
```

And then to execute *every 15 minutes* write in the crontab :  

```
 */15 * * * * python /opt/services/scripts/gandyndns.py
```
