#!/usr/bin/env python3

import json

ENCRYPT_CAPABLE_CERTS = {"Identity card of Estonian citizen", "Identity card of European Union citizen", "Digital identity card", "Diplomatic identity card"}

def get_certs(isikukood):
    auth_certs = []

    fail = f"res/{isikukood}.json"
    with open(fail, 'r') as infile:
        certs = json.load(infile)
        
    cert_set = set(certs.keys()) - {'isikukood'}
    
    for cert_list in ENCRYPT_CAPABLE_CERTS.intersection(cert_set):
        if "Authentication" in certs[cert_list]:
            for cert in certs[cert_list]["Authentication"]:
                #if datetime.fromisoformat(cert["to"]) < datetime.now():
                #    continue
                auth_cert = bytes(cert["cert"], "utf-8")
                auth_certs.append(auth_cert)
    assert(len(auth_certs) > 0)
    
    return auth_certs

