#!/usr/bin/python3

# ./tally.py | tee /dev/tty | pandoc -f markdown -t pdf > results.pdf

import json
from sys import stderr

cands = {169: {'name': 'Vsevolod Jürgenson', 'id': 169, 'list': 'Üksikkandidaadid', 'votes': 0}, 170: {'name': 'Andres Inn', 'id': 170, 'list': 'Üksikkandidaadid', 'votes': 0}, 168: {'name': 'Mike Calamus', 'id': 168, 'list': 'Üksikkandidaadid', 'votes': 0}, 167: {'name': 'Tanel Talve', 'id': 167, 'list': 'Üksikkandidaadid', 'votes': 0}, 171: {'name': 'Kalle Grünthal', 'id': 171, 'list': 'Üksikkandidaadid', 'votes': 0}, 140: {'name': 'Urmas Paet', 'id': 140, 'list': 'Eesti Reformierakond', 'votes': 0}, 141: {'name': 'Yoko Alender', 'id': 141, 'list': 'Eesti Reformierakond', 'votes': 0}, 142: {'name': 'Luukas Kristjan Ilves', 'id': 142, 'list': 'Eesti Reformierakond', 'votes': 0}, 143: {'name': 'Maria Jufereva-Skuratovski', 'id': 143, 'list': 'Eesti Reformierakond', 'votes': 0}, 144: {'name': 'Marko Mihkelson', 'id': 144, 'list': 'Eesti Reformierakond', 'votes': 0}, 145: {'name': 'Hanah Lahe', 'id': 145, 'list': 'Eesti Reformierakond', 'votes': 0}, 146: {'name': 'Karmen Joller', 'id': 146, 'list': 'Eesti Reformierakond', 'votes': 0}, 147: {'name': 'Maarja Metstak', 'id': 147, 'list': 'Eesti Reformierakond', 'votes': 0}, 148: {'name': 'Hanno Pevkur', 'id': 148, 'list': 'Eesti Reformierakond', 'votes': 0}, 102: {'name': 'Martin Helme', 'id': 102, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 103: {'name': 'Anti Poolamets', 'id': 103, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 104: {'name': 'Helle-Moonika Helme', 'id': 104, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 105: {'name': 'Henn Põlluaas', 'id': 105, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 106: {'name': 'Siim Pohlak', 'id': 106, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 108: {'name': 'Rain Epler', 'id': 108, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 109: {'name': 'Arvo Aller', 'id': 109, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 110: {'name': 'Jaak Madison', 'id': 110, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 107: {'name': 'Merle Kivest', 'id': 107, 'list': 'Eesti Konservatiivne Rahvaerakond', 'votes': 0}, 126: {'name': 'Riina Sikkut', 'id': 126, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 129: {'name': 'Vootele Päi', 'id': 129, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 128: {'name': 'Natalie Mets', 'id': 128, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 122: {'name': 'Marina Kaljurand', 'id': 122, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 123: {'name': 'Sven Mikser', 'id': 123, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 127: {'name': 'Ivari Padar', 'id': 127, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 130: {'name': 'Jevgeni Ossinovski', 'id': 130, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 125: {'name': 'Tanel Kiik', 'id': 125, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 124: {'name': 'Katri Raik', 'id': 124, 'list': 'Sotsiaaldemokraatlik Erakond', 'votes': 0}, 149: {'name': 'Mihhail Kõlvart', 'id': 149, 'list': 'Eesti Keskerakond', 'votes': 0}, 156: {'name': 'Aivar Riisalu', 'id': 156, 'list': 'Eesti Keskerakond', 'votes': 0}, 151: {'name': 'Erki Savisaar', 'id': 151, 'list': 'Eesti Keskerakond', 'votes': 0}, 157: {'name': 'Jana Toom', 'id': 157, 'list': 'Eesti Keskerakond', 'votes': 0}, 152: {'name': 'Anneli Ott', 'id': 152, 'list': 'Eesti Keskerakond', 'votes': 0}, 154: {'name': 'Janek Mäggi', 'id': 154, 'list': 'Eesti Keskerakond', 'votes': 0}, 155: {'name': 'Monika Haukanõmm', 'id': 155, 'list': 'Eesti Keskerakond', 'votes': 0}, 153: {'name': 'Andrei Korobeinik', 'id': 153, 'list': 'Eesti Keskerakond', 'votes': 0}, 150: {'name': 'Lauri Laats', 'id': 150, 'list': 'Eesti Keskerakond', 'votes': 0}, 158: {'name': 'Lavly Perling', 'id': 158, 'list': 'Erakond Parempoolsed', 'votes': 0}, 159: {'name': 'Rainer Saks', 'id': 159, 'list': 'Erakond Parempoolsed', 'votes': 0}, 160: {'name': 'Ilmar Raag', 'id': 160, 'list': 'Erakond Parempoolsed', 'votes': 0}, 161: {'name': 'Annela Anger-Kraavi', 'id': 161, 'list': 'Erakond Parempoolsed', 'votes': 0}, 162: {'name': 'Marti Aavik', 'id': 162, 'list': 'Erakond Parempoolsed', 'votes': 0}, 164: {'name': 'Kadri Kullman', 'id': 164, 'list': 'Erakond Parempoolsed', 'votes': 0}, 165: {'name': 'Andres Kaarmann', 'id': 165, 'list': 'Erakond Parempoolsed', 'votes': 0}, 166: {'name': 'Kristjan Vanaselja', 'id': 166, 'list': 'Erakond Parempoolsed', 'votes': 0}, 163: {'name': 'Eero Raun', 'id': 163, 'list': 'Erakond Parempoolsed', 'votes': 0}, 131: {'name': 'Riho Terras', 'id': 131, 'list': 'ISAMAA Erakond', 'votes': 0}, 132: {'name': 'Urmas Reinsalu', 'id': 132, 'list': 'ISAMAA Erakond', 'votes': 0}, 133: {'name': 'Urve Paris Palo', 'id': 133, 'list': 'ISAMAA Erakond', 'votes': 0}, 134: {'name': 'Riina Solman', 'id': 134, 'list': 'ISAMAA Erakond', 'votes': 0}, 135: {'name': 'Tõnis Lukas', 'id': 135, 'list': 'ISAMAA Erakond', 'votes': 0}, 136: {'name': 'Virve Linder', 'id': 136, 'list': 'ISAMAA Erakond', 'votes': 0}, 137: {'name': 'Üllar Saaremäe', 'id': 137, 'list': 'ISAMAA Erakond', 'votes': 0}, 138: {'name': 'Ahti Kallikorm', 'id': 138, 'list': 'ISAMAA Erakond', 'votes': 0}, 139: {'name': 'Jüri Ratas', 'id': 139, 'list': 'ISAMAA Erakond', 'votes': 0}, 117: {'name': 'Igor Taro', 'id': 117, 'list': 'Erakond Eesti 200', 'votes': 0}, 118: {'name': 'Irja Lutsar', 'id': 118, 'list': 'Erakond Eesti 200', 'votes': 0}, 115: {'name': 'Grigore-Kalev Stoicescu', 'id': 115, 'list': 'Erakond Eesti 200', 'votes': 0}, 116: {'name': 'Liisa-Ly Pakosta', 'id': 116, 'list': 'Erakond Eesti 200', 'votes': 0}, 114: {'name': 'Kristina Kallas', 'id': 114, 'list': 'Erakond Eesti 200', 'votes': 0}, 113: {'name': 'Margus Tsahkna', 'id': 113, 'list': 'Erakond Eesti 200', 'votes': 0}, 121: {'name': 'Indrek Tarand', 'id': 121, 'list': 'Erakond Eesti 200', 'votes': 0}, 119: {'name': 'Hendrik Johannes Terras', 'id': 119, 'list': 'Erakond Eesti 200', 'votes': 0}, 120: {'name': 'Kadri Tali', 'id': 120, 'list': 'Erakond Eesti 200', 'votes': 0}, 101: {'name': 'Aivo Peterson', 'id': 101, 'list': 'KOOS organisatsioon osutab suveräänsusele', 'votes': 0}, 111: {'name': 'Evelyn Sepp', 'id': 111, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 172: {'name': 'Alina Lerner-Vilu', 'id': 172, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 173: {'name': 'Olev-Andres Tinn', 'id': 173, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 174: {'name': 'Riin Ehin', 'id': 174, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 175: {'name': 'Kaia Konsap', 'id': 175, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 176: {'name': 'Liina Freivald', 'id': 176, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 177: {'name': 'Tuula Raidna', 'id': 177, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 178: {'name': 'Marko Kaasik', 'id': 178, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}, 112: {'name': 'Rasmus Lahtvee', 'id': 112, 'list': 'Erakond Eestimaa Rohelised', 'votes': 0}}

pseudonyms = set(open("pseudonüümid.txt", "rt").read().split())
bb = json.load(open("bulletin.json", "rt"))

print(f"# {bb['title']}")
print()

invalid = 0
parties = {}

for nr, p, c in bb["votes"]:
    if p not in pseudonyms:
        stderr.write(f"INELIGIBLE: '{p}'\n")
    elif not c.isnumeric() or int(c) not in cands:
        stderr.write(f"INVALID: '{c}'\n")
        invalid += 1
    else:
        cands[int(c)]['votes'] += 1
        l = cands[int(c)]['list']
        p = l if l != "Üksikkandidaadid" else cands[int(c)]['name']
        parties[p] = 1 if p not in parties else parties[p] + 1

print("## Kandidaadid")

for c in sorted(cands.values(), key = lambda x: x['votes'], reverse = True):
    if c['votes'] > 0:
        print(f"{c['name']}, {c['votes']}  ")
print(f"_Kehtetuid sedeleid_, {invalid}  ")

print()
print("## Erakonnad")

for p in sorted(parties, key = lambda x: parties[x], reverse = True):
    print(f"{p}, {parties[p]}  ")

print()
print(f"_Need on tulemused {bb['timestamp']} seisuga._")