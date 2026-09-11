# ERPNext Slovakia

Frappe/ERPNext aplikácia pre slovenské legislatívne požiadavky.

## Čo aplikácia poskytuje

- **Slovenská účtová osnova** – účtová osnova pre podnikateľov účtujúcich v sústave
  podvojného účtovníctva, triedy 0–6
- **Predvolené účty spoločnosti** – pohľadávky 311, záväzky 321, pokladnica 211,
  bankové účty 221, zásoby, kurzové rozdiely a ďalšie sa nastavia na konkrétne
  syntetické účty namiesto toho, aby si ich ERPNext vybral podľa typu účtu
- **Šablóny DPH** – predajné, nákupné aj položkové šablóny pre sadzby 23 %, 19 % a 5 %
  platné od 1. 1. 2025; zastarané šablóny 20 % a 10 % z ERPNext core sa odstránia,
  ak neboli použité v žiadnom doklade
- **Kontrola sadzieb DPH** – upozornenie pri faktúre s inou ako platnou slovenskou sadzbou
- **Súvaha Úč POD 1-01** – report so stĺpcami Brutto / Korekcia / Netto a porovnaním
  s predchádzajúcim obdobím, podľa vzoru Opatrenia MF SR č. 23054/2002-92
- **Odpisové skupiny** – Stavby, Samostatné hnuteľné veci, Softvér a Oceniteľné práva
  s korektnými účtami oprávok a dobou odpisovania
- **IČO a IČ DPH** – vlastné polia na Spoločnostiach, Zákazníkoch a Dodávateľoch
- **Formát adresy** – šablóna adresy podľa slovenského štandardu
- **Automatická aktivácia** – polia, šablóny aj predvolené účty sa nastavia automaticky
  pri vytvorení spoločnosti so štátom „Slovakia“

## Požiadavky

- Frappe 16+
- ERPNext 16+
- Python 3.14+

## Inštalácia

Aplikáciu nainštalujte štandardným spôsobom cez `bench`. Prvý argument určuje názov
adresára v `apps/` – musí byť `erpnext_slovakia`, inak sa aplikácia nenačíta:

```bash
bench get-app erpnext_slovakia https://github.com/neofree75/erpnext_slovakia-main
bench --site <site> install-app erpnext_slovakia
```

Po inštalácii spustite migráciu:

```bash
bench --site <site> migrate
```

## Aktivácia pre spoločnosť

1. Vytvorte novú Spoločnosť (Company) a ako krajinu nastavte **Slovakia**
2. Pri výbere účtovej osnovy zvoľte **Slovakia - Účtová osnova pre podnikateľov**
3. Aplikácia automaticky pridá polia IČO a IČ DPH, nastaví predvolené účty,
   vytvorí šablóny DPH a odpisové skupiny a namapuje účty na položky súvahy

Pri spoločnosti, ktorá už existovala pred inštaláciou aplikácie, doplníte predvoľby ručne:

```bash
bench --site <site> execute erpnext_slovakia.setup.install.setup_slovak_defaults \
  --kwargs "{'company': 'Názov spoločnosti'}"
```

Bez parametra `company` sa spracujú všetky spoločnosti so štátom Slovakia.

## Súvaha

Report nájdete pod názvom **Balance Sheet SK** (v slovenskom rozhraní
*Súvaha Úč POD 1-01*). Mapovanie účtu na položku súvahy sa ukladá do poľa
`sk_suvaha_riadok` na Účte a dá sa pri neštandardných analytických účtoch upraviť ručne.

## Vývoj

Po klonovaní do adresára `apps/` bench-u:

```bash
bench --site <site> migrate   # nasadí účtovú osnovu, polia IČO/IČ DPH a mapovanie súvahy
bench restart                 # načíta zmeny v kóde
```

Adresová šablóna sa vytvára len pri inštalácii (`after_install`), nie pri každej migrácii.

## Upozornenie

Aplikácia je pomôcka pre vedenie účtovníctva, nie náhrada účtovníka ani daňového
poradcu. Autor neposkytuje žiadnu záruku, že účtová osnova, sadzby DPH, výkazy
a ďalšie výstupy zodpovedajú aktuálne platným slovenským právnym predpisom, ani
že sú vhodné pre konkrétnu účtovnú jednotku.

Za správnosť účtovných zápisov, daňových priznaní a účtovnej závierky zodpovedá
výlučne používateľ. Pred použitím v ostrej prevádzke si výstupy overte s vlastným
účtovníkom alebo daňovým poradcom.

## Licencia

Copyright (C) 2026 Code Way, s.r.o. <info@codeway.sk>

Tento program je slobodný softvér: môžete ho šíriť a upravovať podľa podmienok
GNU General Public License verzie 3, alebo (podľa vášho uváženia) ktorejkoľvek
neskoršej verzie, tak ako ju zverejnila Free Software Foundation.

Program je šírený v nádeji, že bude užitočný, avšak BEZ AKEJKOĽVEK ZÁRUKY.
Plný text licencie nájdete v súbore [license.txt](license.txt).

Aplikácia je rozšírením [ERPNext](https://erpnext.com) (GPL-3.0) a beží na
[Frappe Framework](https://frappeframework.com) (MIT).
