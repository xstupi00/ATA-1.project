Pokiaľ je požadované premiestnenie nákladu z jedného miesta do druhého, vozík si materiál vyzdvihne do 1 minúty.

    - Unnecessary Aliases: "náklad" => "materiál" - zjednotenia názvoslovia naprieč celou špecifikáciou
    - Unnecessary Aliases: "požadované premiestnenie" => "požiadavka na presun" - viacznačný výraz pre synonymá

*Pokiaľ vznikne požiadavka na presun materiálu z jedného miesta do druhého, vozík si materiál vyzdvihne do 1 minúty.*

Pokiaľ sa to nestihne, materiálu sa nastavuje prioritná vlastnosť.

    - Ambiguity of Reference: "to" - nešpecifikované označenie spôsobuje neurčitosť, ktorú je potrebné definovať
    - Unnecessary Aliases: "prioritná vlastnosť" => "prioritný materiál - zjednotenie názvoslovia naprieč celou špecifikáciou

*Pokiaľ vozík nevyzdvihne materiál do 1 minúty od vzniku požiadavky na presun, materiál sa stáva prioritným.*

Každý prioritný materiál musí byť vyzdvinhnutý vozíkom do 1 minúty od nastavenia prioritnej požiadavky.

    - Ambiguous Adjectives: "každý" - označenie nejednoznačne vymedzuje skupinu prioritných materiálov
    - Dangling Else: "musí" - nedefinovaný prípad, ak nedôjde k včasnému požadovanému vyzdvihnutie materiálu
    - Unnecessary Aliases: "nastavenie prioritnej požiadavky" => "materiál sa stal prioritným" - viacznačný výraz pre synonymá
    - Missing Causes: chýbajúca príčina, ktorá spôsobuje vyzdvihnutie prioritného materiálu v stanovenom čase

*Pokiaľ je materiál prioritný, vozík vyzdvihne tento materiál do 1 minúty od kedy sa tento materiál stal prioritným.*
*Pokiaľ nedôjde k vyzdvihnutiu prioritného materiálu do 1 minúty od kedy sa tento materiál stal prioritným, bude vyvolaná výnimka.*

Pokiaľ vozík nakladá prioritný materiál, prepína sa do režimu iba-vykládka.

    - Unnecessary Aliases: "nakladá" => "vyzdvihne" - zjednotenia názvoslovia naprieč celou špecifikáciou

*Pokiaľ vozík vyzdvihuje prioritný materiál, prepína sa do režímu iba-vykládka.*

V tomto režíme ostáva, dokiaľ nevyloží všetok takýto materiál.

    - Ambiguity of Reference: "tomto" - nie je definované v akom režíme má vozik ostať z pohľadu kladenej žiadosti
    - Ambiguity of Reference: "takýto" - nie je definované na aký materiál je kladený požiadavok o jeho vyložení
    - Ambiguous Adjectives: všetok - nie je definované aká kategória materiálu spadá pod požiadavku vyloženia
    - Complete omissions: chýba prepnutie vozíka do pôvodného režimu pri vyskutnutí žiadanej príčiny

*Pokiaľ vozík nevyloží vyzdvihnutý prioritný materiál, ostáva v režíme iba-vykládka.*
*Pokiaľ vozík vyloží vyzdvihnutý prioritný materiál, prepína sa do režímu nákladka+vykládka.*

Normálne vozík behom svojej jazdy môže naberať a vykladať dalšie materiály v iných zastávkách.

    - Ambiguous Adverbs: "normálne" - nie je špecifikované pre aký režím sú definované povolené aktivity vozíka
    - Ambiguous logical operators: and - spojenie dvoch aktivít v jednej vete môže byť matúce a viacznazčné
    - Complete omissions: chýbajúca činnosť o vyjadrení povoleného vykladania materiálu v režíme iba-vykládka
    - Dangling Else: "môže" - vozík si túto činnosť nemá voliť, ale ak je to v súlade s ostatnými podmienkami nakladá a vykladá materiál
    
*Pokiaľ je vozík v režime nákladka+vykládka, behom svojej jazdy vyzdvihuje nevyzdvihnuté materiály v iných miestách.*
*Pokiaľ je vozík v režíme nákladka+vykládka alebo iba-výkladka, vykladá vyzdvihnuté materiály v iných miestách.*

Na jednom mieste môže vozík akceptovať alebo vyložiť jeden aj viac materiálov.

    - Unnecessary Aliases: "akceptovať" => "vyzdvihnúť" - vozík materiál vyzdvihuje v rámci celej špecifikácie
    - Ambiguous logical operators: alebo => a súčasne - s touto spojkou nie je zrejmé, či vozík môže vykonať obe činnosti
    - Dangling Else: "môže" - táto činnost vozíka nie je voliteľná a musí byť v súlade s ostatnými definovanými požiadavkami
    
*Na jednom mieste vozík vyzdvihuje nevyzdvihnuté materiály a súčasne vykladá vyzdvihnuté materiály určené na toto miesto.*

Poradie vyzdvihnutia materiálov nesúvisí s poradím vytvárania požiadaviek.

    - Ambiguity: nie je definované o vytváranie akých požiadaviek sa jedná, musia to buť požiadavky na presun materiálov
    
*Poradie vyzdvihnutia materiálov nesúvisí s poradím vytvárania požiadaviek na presun materiálov.*

Vozík neakceptuje materiál, pokiaľ sú všetky jeho sloty obsadené alebo by jeho prevzatím bola prekročená maximálna nosnosť.

    - Unnecessary Aliases: "neakceptuje" => "nevyzdvihne", "prevzatím" => "vyzdvihnutím" - viacznačný výrazy pre synonymá
    - Ambiguity of Reference: "jeho", "jeho" - je neurčité na aké subjekty sa tieto odkazy vzťahujú a navyše pôsobia spolu mätúco
    - Negation: negácie nejasne definujú kladené požiadavky a obmedzenia a preto je lepšie ich vyjadriť v kladnom spôsobe

*Pokiaľ je voľný dostatočný počet slotov vozíka a vyzdvihnutím materiálu nebude prekročená maximálna nosnosť vozíka, vozík materiál vyzdvihne.*
