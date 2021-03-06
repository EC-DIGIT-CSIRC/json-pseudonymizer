# JSON Pseudonymizer

This little script takes JSON files as input and for every fieldname given on the command line, 
it will pseudonymize the value of that field name in the JSON file. 


**Example:**

JSON:

```json
{
  "type": "endpoint.event.netconn",
  "process_guid": "N3VAPZL7-003046fe-000005d0-00000000-1d6a5f302512c5c",
  "parent_guid": "N3VAPZL7-003046fe-00000204-00000000-1d6a5f2fba96c86",
  "device_external_ip": "8.8.8.8",
  "device_os": "WINDOWS",
  "device_timestamp": "2019-10-22 11:19:02.2652876 +0000 UTC",
  "remote_port": 63704,
  "remote_ip": "9.9.9.9",
  "local_port": 33354,
  "local_ip": "10.1.2.3",
  "netconn_domain": "",
  "netconn_inbound": true,
  "netconn_protocol": "PROTO_UDP"
}

```

gets pseudonomyized to:

```json
{
  "type": "endpoint.event.netconn",
  "process_guid": "x5wGr064Cd21Th0wzKvahwH zM8P0SEu6HJMtn1Ce7vI 44q6I ",
  "parent_guid": "N3VAPZL7-003046fe-00000204-00000000-1d6a5f2fba96c86",
  "device_external_ip": "70.37.199.247",
  "device_os": "WINDOWS",
  "device_timestamp": "2019-10-22 11:19:02.2652876 +0000 UTC",
  "remote_port": 63704,
  "remote_ip": "71.215.121.114",
  "local_port": 33354,
  "local_ip": "69.199.117.159",
  "netconn_domain": "",
  "netconn_inbound": true,
  "netconn_protocol": "PROTO_UDP"
}
```


Observe the changes in the fields: ``process_guid``, ``remote_ip``, ``local_ip``, ``device_external_ip``.

In general, you can specify which fields you want to have pseudonymized via a config file.



# Configuration

All config is stored in in a config file.

Example config.json:

```json
{ "secret": "ootahdooTah5tai2etaghu5Oo3oKia5n",
  "fields":  [ 
	{ "name": "process_guid",
      "type": "string"
    },  
	{ "name": "device_external_ip",
	  "type": "inet"
    },
	{ "name": "local_ip",
	  "type": "inet"
    },
	{ "name": "remote_ip",
	  "type": "inet"
    }
  ]
}
```

**Note**: the secret MUST be 32 characters long (not less, not more). This is a limit of the CryptPAN library 
we are using. It should not matter much tough. You can easily generate a random 32 character string via:

```bash
apt install pwgen 
pwgen 32 1 
```

**Interpretation of the config file**:

The secret key to encrypt/pseudonymize is given by ``secret``. As said, this MUST be 32 characters long. Not more not less.
The list of JSON fields to encrypt/pseudonymize is given by the list ``fields`` where 
the field called ``process_guid`` should be treated as text (string) and 
the field ``device_external_ip`` should be treated as IP address and encrypted by the cryptoPAN module 
for pseudonymizing IP addresses. This is distinctly differnt to encrypting regular strings.




# Testing

use the supplied test data in tests/

```bash
cp config-sample.json config.json
# adapt it to your need, change the secret!! 
python pseudonymize.py --debug --config config.json < tests/data.json
```


# Known bugs and limitations

* Was only tested on Debian Linux 10.
* For sure does not work on OS X , can't find the Crypto lib
* The CryptoPAN library in use is slow. We could use https://github.com/certtools/cryptopanwrapper/ and especially https://github.com/certtools/cryptopanlib
* We only accept 32 characters secrets
* Does not retain the syntax of GUIDs
* Only supports [JSONL](https://jsonlines.org/) files where each line is a **flat** JSON dict. No deeper nesting supported for now.

All bug reports should go to Aaron Kaplan <leon-aaron.kaplan@ext.ec.europa.eu>





