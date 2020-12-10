# JSON Pseudonymizer

This little script takes JSON files as input and for every fieldname given on the command line, 
it will pseudonymize the value of that field name in the JSON file. 


Example:

JSON:

```json

{ 



# Configuration

All config is stored in config.yaml

Example config.yaml:
```json

{ secret: "air8eXogh1pohvi8eeyaivae8icesh2EaCh7ichoosair9geyeez6iigee5eiruk",
  fields:  [ 
	{ name: "process_guid",
      type: "string"
    },  
	{ name: "device_external_ip",
	  type: "inet"
    }
  ]
}
```

Meaning: the secret key to encrypt/pseudonymize is given by "secret".
The list of JSON fields to encrypt/pseudonymize is given by the list "fields" where 
the field called "process_guid" should be treated as text (string) and 
the field "device_external_ip" should be treated as IP address and encrypted by the module 
for pseudonymizing IP addresses.



# Testing

use the supplied test data in tests/

```bash
python pseudonymize.py -c tests/config.sample.json < tests/data.json
```


# Known bugs
does not work on OS X , can't find the Crypto lib
