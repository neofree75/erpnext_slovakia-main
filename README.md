# ERPNext Slovakia

Frappe/ERPNext aplikácia pre slovenské legislatívne požiadavky.

## Čo aplikácia poskytuje

- **Slovenská účtová osnova** – štruktúra účtov podľa slovenských účtovných predpisov (triedy 0–9)
- **DPH sadzby** – validácia platných slovenských sadzieb DPH (0 %, 5 %, 10 %, 23 %) pri každej faktúre
- **IČO a IČ DPH** – vlastné polia na Spoločnostiach, Zákazníkoch a Dodávateľoch
- **Formát adresy** – šablóna adresy podľa slovenského štandardu
- **Automatická aktivácia** – všetky polia a šablóny sa nastavia automaticky pri vytvorení spoločnosti so štátom „Slovakia"

## Požiadavky

- Frappe 16+
- ERPNext 16+
- Python 3.14+

## Inštalácia

Aplikáciu nainštalujte štandardným spôsobom cez `bench`:

```bash
bench get-app https://github.com/neofree75/erpnext_slovakia
bench --site <site> install-app erpnext_slovakia
```

Po inštalácii spustite migráciu:

```bash
bench --site <site> migrate
```

## Aktivácia pre spoločnosť

1. Vytvorte novú Spoločnosť (Company) a ako krajinu nastavte **Slovakia**
2. Aplikácia automaticky pridá polia IČO a IČ DPH na Spoločnosť, Zákazníkov a Dodávateľov
3. Pri výbere účtovej osnovy zvoľte **Slovak – Slovenská účtovná osnova**

## Vývoj

Po klonovaní do adresára `apps/` bench-u:

```bash
bench migrate          # nasadí účtovú osnovu a šablónu adresy
bench restart          # načíta zmeny v kóde
```

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
