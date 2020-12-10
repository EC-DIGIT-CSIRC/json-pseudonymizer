#!/usr/bin/env python


import argparse
import sys
import json

import gocept.pseudonymize
# one alternative:
# from cryptopan import CryptoPan
from yacryptopan import CryptoPAn


debug=False

config = dict()
replace_keys = []
cp = None


def load_config_and_init(filename: str):
    global replace_keys
    global cp
    with open(filename) as f:
        data = json.load(f)
        replace_keys = [i["name"] for i in data["fields"]]
    if debug:
        print("replace_keys = %r" % replace_keys)
    cp = CryptoPAn(bytes(data['secret'], 'utf-8'))
    return data


def enc_cryptopan(ip):
    return cp.anonymize(ip)


def enc_normal(s):
    return gocept.pseudonymize.text(s, config["secret"])


def encrypt(k, v) -> str:
    for f in config["fields"]:
        if k == f["name"]:
            if f["type"] == "inet":
                return enc_cryptopan(v)
            elif f["type"] == "string":
                return enc_normal(v)
            else:
                print("ooops, unkown type. skipping (not replacing anything)", file=sys.stderr)
                return v
    return v  # in case we can't find the key


def process_input():
    jsonl = []
    try:
        json_list = list(sys.stdin)
        for json_str in json_list:
            j = json.loads(json_str)    # I wish it could load JSONL natively
            jsonl.append(j)
        for d in jsonl:
            if debug:
                print("before: %r" % (d))
                print(80 * "=")
            d.update((k, encrypt(k, v)) for k, v in d.items() if k in replace_keys)
            if debug:
                print("after: %r" % d)
                print()
                print()
            print(d)
    except Exception as ex:
        print("could not parse input. Reason: %s" % str(ex))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='turn on debugging', action="store_true")
    parser.add_argument('--config', nargs=1, required=True, help='path to the config.json file', default='config.json')
    args = parser.parse_args()

    if args.debug:
        debug = True
    config = load_config_and_init(args.config[0])
    if debug:
        print(80 * "=")
        print(config)
        print(80 * "=")
    process_input()
