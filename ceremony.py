#!/usr/bin/env python3

import secrets
import time, datetime

from cdoc_tools import encrypt_cdoc
from cert_store import get_certs
from voter_card import create_pdf

from hashlib import sha256
from base64 import b64encode

from multiprocessing import Manager, Lock
from multiprocessing.pool import Pool

import progressbar

VOTERLIST = "voterlist.txt"
VOTER_COUNT = 933599

URL = "https://euro24.pseudovote.net"

manager = Manager()
processed_voters = manager.list()
cert_count = manager.Value('i', 0)
container_count = manager.Value('i', 0)
lock = Lock()

def create_voting_credential(pseudonym):
    with lock:
        voter = processed_voters.pop()
    certs = get_certs(voter)
    assert(len(certs) > 0)
    encrypt_cdoc("hääletustunnus.pdf", create_pdf(URL, pseudonym), certs, f"con/{voter}.cdoc")
    with lock:
        cert_count.value += len(certs)
        container_count.value += 1

if __name__ == "__main__":
    start_time = time.time()

    print(f"Starting pseudonym ceremony at {datetime.datetime.now()}")
    print()

    with open(VOTERLIST, "r") as infile:
        voters = list(set(infile.read().split()))

    print("Eligible voters", len(voters))
    assert(len(voters) == VOTER_COUNT)

    print("Creating pseudonyms...")

    pseudonyms = set()
    created = 0
    while len(pseudonyms) < VOTER_COUNT:
        if len(pseudonyms) != created:
            print(f"COLLISION at {created}!")
            created=len(pseudomyms)
        pseudonyms.add(secrets.token_urlsafe())
        created += 1

    print("Generating pseudonym hashes...")

    pseudonym_hashes = set()
    for pseudonym in pseudonyms:
        pseudonym_hash = sha256(bytes(pseudonym, "utf-8"))
        if pseudonym_hash in pseudonym_hashes:
            print(f"COLLISION with {pseudonym_hash}!")
            continue
        pseudonym_hashes.add(pseudonym_hash)

    print("Shuffling pseudonyms...")

    pseudonyms = list(pseudonyms)
    shuffled_pseudonyms = []
    while(pseudonyms):
        shuffled_pseudonyms.append(pseudonyms.pop(secrets.randbelow(len(pseudonyms))))

    print("Shuffling and writing pseudonym hashes...")

    pseudonym_hashes = list(pseudonym_hashes)
    shuffled_pseudonym_hashes = []
    while(pseudonym_hashes):
        hash_in_b64 = b64encode(pseudonym_hashes.pop(secrets.randbelow(len(pseudonym_hashes))).digest())
        shuffled_pseudonym_hashes.append(hash_in_b64.decode("utf-8"))

    pseudonym_hashes_list = "\n".join(shuffled_pseudonym_hashes) + "\n"
    pseudonym_hashes_list_hash = sha256(bytes(pseudonym_hashes_list, "utf-8"))

    with open("pseudonüümide_räsid.txt", 'wt') as outfile:
        outfile.write(pseudonym_hashes_list)
    
    print(f"Wrote {len(shuffled_pseudonym_hashes)} pseudonym hashes to `pseudonüümide_räsid.txt` ({pseudonym_hashes_list_hash.hexdigest()}).")

    print("Shuffling voters...")

    while(voters):
        processed_voters.append(voters.pop(secrets.randbelow(len(voters))))

    assert(len(processed_voters) == len(shuffled_pseudonyms))

    print("Encrypting pseudonyms...")

    bar = progressbar.ProgressBar(100).start()
    
    with Pool() as p:
        for i, _ in enumerate(p.imap(create_voting_credential, shuffled_pseudonyms), 1):
            processed = i/VOTER_COUNT*100
            bar.update(100 if processed >= 100 else int(round(processed)))

    assert(not processed_voters)

    print()
    print(f"Encrypted {container_count.value} containers for {cert_count.value} certs.")
    
    print(f"Shuffling {len(shuffled_pseudonyms)} pseudonyms for quarantine...")

    pseudonym_list = []
    while(shuffled_pseudonyms):
        index = secrets.randbelow(len(shuffled_pseudonyms))
        pseudonym_list.append(shuffled_pseudonyms.pop(index))

    end_time = time.time()
    tstr = time.strftime("%H:%M:%S", time.gmtime(end_time-start_time))

    print(f"Time since start {tstr} / {end_time-start_time}" )

    pseudonym_list = "\n".join(pseudonym_list) + "\n"

    encrypted = 0
    while((decryptor := input("encrypt> ")) != "end"):
        try:
            if len(decryptor) != 11 or not decryptor.isnumeric():
                continue
            if not encrypted:
                pseudonyms_hash = sha256(bytes(pseudonym_list, "utf-8"))
                print(f"Encrypting {len(pseudonym_list)} bytes in `pseudonüümid.txt` ({pseudonyms_hash.hexdigest()})...")
                karantiin = encrypt_cdoc(f"pseudonüümid.txt", bytes(pseudonym_list, "utf-8"), get_certs(decryptor))
            else:
                print(f"Reencrypting {len(karantiin)} bytes in `karantiin_{last_decryptor}.cdoc` ({sha256(karantiin).hexdigest()})...")
                karantiin = encrypt_cdoc(f"karantiin_{last_decryptor}.cdoc", karantiin, get_certs(decryptor))
            encrypted += 1
            last_decryptor = decryptor
            print(f"ENCRYPTED x{encrypted}")
        except:
            pass

    with open(f"karantiin_{last_decryptor}.cdoc", 'wb') as outfile:
        outfile.write(karantiin)

    print(f"Wrote final quarantine file in `karantiin_{last_decryptor}.cdoc` ({sha256(karantiin).hexdigest()}).")

    print(f"Pseudonym ceremony ended at {datetime.datetime.now()}")
        
    print()

    print("Thanks for taking digital democracy seriously!")
