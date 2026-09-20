
# --- structure --- #

# 1. bevezetés

arisztotelész és wittgenstein

arisztotelész: lényegi és esetleges tulajdonságok

leegyszerűsítve ember kétlábú tollatlan szárazföldi élőlény, az mindegy hogy férfi vagy orvos vagy hetven éves

wittgenstein: a kategóriákat hasonlóságok szervezik

rosch, labov: a kategóriába tartozás gradiens, a kategória középpontjához közelebb levő dolgok jobban a kategória részei

Diagnostic and Statistical Manual of Mental Disorders
DSM: bizonyos számú jelentős tünet, amelyek alapján. 

betegségek nemzetközi osztályozására szolgáló kódrendszer (BNO) 
BNO kódok alcsoportja

köznyelv: szomorúság, közöny

szkizofrén: még nem is hasonlít az orvosi diagnózisra

alkoholista: nincs is ilyen


references

Arisztotelész??

Taylor, John R. Linguistic categorization. Oxford University Press, 2003.

Wittgenstein, Ludwig. 1958. Philosophical investigations. Trans. by G. E. M. Anscombe. New
York:Macmillan.

Rosch, Eleanor H. "Natural categories." Cognitive psychology 4, no. 3 (1973): 328-350.

Labov 1973, "The boundaries of words and their meanings", in Bailey and Shuy, eds, New Ways of Analyzing Variation in English

# 2. szóvektorok

közös kontextusok: szemantikai hasonlóság

kutya macska atomreaktor

sentiment analysis / véleménybányászat: pozitív és negatív szavak meghatározása

references

Firth, John R. 1957. Modes of meaning. In Papers in linguistics, 1934–1951. Oxford: Oxford
UniversityPress.

Church, Kenneth Ward. 2017.Word2vec. NaturalLanguageEngineering 23(1). 155–162.


# 3. klinikai és egyéb szavak: kérdésfelvetés

references

broader case???

Putnam 1975, "The meaning of 'meaning'"

word embeddings and culture / semantics

Kozlowski, Austin C., Matt Taddy & James A. Evans. 2019. The geometry of
culture: Analyzing the meanings of class through word embeddings. *American
Sociological Review* 84(5). 905–949. doi:10.1177/0003122419877135.

diagnostic words are not used in an aristotelian way

Cantor, Smith, French and Mezzich 1980, "Psychiatric diagnosis as prototype categorization", Journal of Abnormal Psychology 89(2), 181–193

followup

Kendler, Zachar and Craver 2011, "What kinds of things are psychiatric disorders?", Psychological Medicine 41(6), 1143–1150

concept creep

Beeker et al. 2021, "Psychiatrization of society", Frontiers in Psychiatry 12:645556

average similarity among contexts

Hoffman, Lambon Ralph and Rogers 2013, "Semantic diversity", Behavior Research Methods 45(3), 718–730

de mi azt csinaljuk hogy:

negy szolista etc

# 4. módszertan

négy szólista

The published
   description of `hunembed0.0` says word2vec, 600 dimensions, frequency
   cut-off 10, trained on the concatenation of the *Hungarian Webcorpus*
   (Halácsy et al. 2004) and the *Hungarian National Corpus* (Váradi 2002).

webcorpus 1 

Kornai, András, Péter Halácsy, Viktor Nagy, Csaba Oravecz, Viktor Trón, and Dániel Varga. "Web-based frequency dictionaries for medium density languages." In Proceedings of the 2nd International Workshop on Web as Corpus. 2006.

hungarian natural corpus (apparently:)

Oravecz Csaba, Váradi Tamás, Sass Bálint: The Hungarian Gigaword Corpus. In: Proceedings of LREC 2014, 2014. 

hunembed0.0 has no publication, so 

http://corpus.nytud.hu/efnilex-vect/

# 5. eredmények

valence_map_hu

mit latunk az abran

ebben az adathalmazban a legtobb diagnosztikus szo a klinikumban marad, meg olyanok is, mint...
az orult bolond pedig a masik oldalon landolt.
van egy koztes kategoria, ahol mar megjelenik az, hogy koznyelviesek kicsit a szavak:
depresszios, kenyszeres, traumatizalt, paranoias
elmebeteg/beszamithatatlan valszeg jogi hasznalat.
paranoias, orult, bolond -> nagyon koznyelvi
- de autista, szkizofren NEM
- manias, fobias SEM

az intuicionak megfelelo eredmenyek szulettek

# 6. diszkusszio

nem drift, hanem statikus
regi adatok, formalis irott szovegek dominalnak
meg ami meg eszunkbe jut

# --- raw transcript of my first dictated text draft --- #

Az emberi megismerés kategóriákra osztja a világot és erre szavakat használ, mint amilyen a pogácsa vagy az elefánt. A jelentések klasszikus osztályozását arisztotelész adta meg, aki azt mondta, hogy a dolgoknak a dolgokat úgy tesszük kategóriába, hogy vannak tulajdonságaik, amik alapján el lehet dönteni, hogy melyik kategóriába tartoznak. Minden dolognak vannak. Lényegi tulajdonságai és esetleges tulajdonságai az ember mondja arisztotelész. Egy kétlábú tollatlan szárazföldi élőlény. Ezek az ő lényegi tulajdonságai. Az meg, hogy ő férfi vagy orvos vagy 70 éves, azok esetleges tulajdonságok, és azok nem számítanak akkor, amikor elhelyezed a kategóriájába, ami az ember ezt a paradigmát a 20. Században sikerült megváltoztatni. Amikor wittgenstein azt mondta, hogy a kategóriákat azokat láthatóan. Hasonlóságok szervezik, ezért lehet arról beszélni, hogy valami kevésbé vagy jobban a kategória része és a kategóriában 6-os gradiens a kategória középpontjához közelebb lévő dolgok jobban a kategória részei később elenoros és labov megerősítették ezt kísérletes úton. Ma már az a konszenzus, hogy a kategóriák azok nem lényegi és esetleges tulajdonságokra épülnek, hanem gradiensek és összetettek és különböző leírási szintjeik vannak. De ha megnézzük AA nyelvet, akkor azt látjuk, hogy megmaradt ez a fajta arisztotelészi kategorizáció, méghozzá a hivatalos és a klinikai nyelvhasználatban. Az, hogy valaki állampolgár vagy kiskorú, annak van-e törvényi meghatározása, és azt, hogy ez a meghatározás az, hogy valaki kiskorú vagy nem kiskorú és állampolgár vagy nem állampolgár, azt nem. Hasonló alapján döntjük el, hanem megnézzünk egy leírást. Ráíresszük az illetőre, és eldöntjük, hogy igaz e vagy sem hasonló a jogi kategóriákhoz a klinikai kategóriáknak a csoportja. Ha megnézzük azt, hogy például különféle lelki zavaroknak mi a nevük, akkor azt fogjuk látni, hogy van egy d. s. m. egy diagnosztical estetical statistical menu of mental disorders és van egy b. n. o., ami a betegségek nemzetközi osztályozására szolgál. Egy ódrendszer és ebben megnézzük, hogy mi az, hogy depresszió, akkor találni fogunk a b. n. o. kódokat, amelyek a depresszió különféle válfajait leírják meghatároznak hozzá a tüneteket, amik alapján szakember eldönti, hogy valaki depressziós vagy sem. Ezzel viszont szemben áll egy köznyelvi használat, amikor valaki azt mondja, hogy nagyon depressziós vagyok ma, mert eleve a fokozással azt jelöli, hogy ő. Ezt a szót valamilyen általánosabb értelemben használni nem ABNO lebeg a szeme előtt. Úgy értjük, hogy ő nagyon fáradt, hogy nagyon közönyös, hogy nagyon szomorú. Nagyon hasonló, hogy vannak olyan szavaink is, mint a szkizofrén, amelyeknek szintén van köznyelvi használatuk, és ezeknek már nem, hogy nem a precíz diagnosztikai izé alapján használják az emberek. Érdekes lenne azt megnézni, hogy a magyar nyelvben a klinikai szavak, mint a depresszió, meg a meg a szkizofrénia, illetve ezeknek a melléknévi változatai, hogy valaki depresszív, depressziós vagy szkizofrén vagy szkizoid azoknak a használata mennyire köznyelvi és mennyire klinikai vége az 1. fejezetnek. Például, ha megnézzük a magyar wikipédiát, akkor azt fogjuk látni, hogy a kutya és a macska szavak azok nagyon sokszor fordulnak elő. Ugyanazon ugyanazokon az oldalakon, például a háziállatokról szóló oldalakon vagy a domesztikációról szóló oldalakon. Ehhez képest a kutya meg az atomerőműszavak azok ritkábban fognak előfordulni ugyanazokon az oldalakon. Bár elképzelhető, hogy a paks nevezetességei oldala, amire a 2 szerepel ez. És elég sok ilyen szövegrészünk. Van valamilyen internetes korpuszból, akkor tudunk ebből csinálni egy nagy összehasonlítást a szóvektorok között, és ezt használhatjuk arra, hogy megállapítsuk azt, hogy szavak azok milyen fajta környezetekben fordulnak elő. 3. fejezet kérdés felvetés az a kérdésünk, hogy. Az olyan szavak, mint a szkizofrén meg a depresszió azok a magyarban a ha megnézzük, hogy jelentésükben, ha megnézünk magyar nyelvű nyelvhasználatból származó adatokat és ezekből szavak közti hasonlóságokat számolunk, akkor ezek a szavak ezek hol lesznek inkább klinikai szavakként fognak viselkedni, klinikai szavak fogják őket körbevenni, vagy pedig inkább köznyelvi szavakként fognak viselkedni. Köznyelvi szavak fogják őket körbevenni. Itt jöhet egy rész a hivatkozzuk a cheer merfy of culture című cikket, és aztán elmondom, hogy annak ellenére, hogy az 1. Fejezetben arról beszéltünk, hogy ezeknek a szavaknak, hogy depresszió, meg paranoid szkizofrénia, ezeknek van valamilyen definíciójuk az emberek ezeket használják arra, hogy diagnosztizálják őket. A szakemberek. Tudjuk, hogy ez nagyjából nem igaz. Ne hivatkozzuk meg a what kind of things a psychiatry disorders és a psychiatry diagnosis az protocy categorisation című cikkeket. Ezek megmutatják azt, hogy amikor emberek pszichiátriai betegségeket diagnosztizálnak, akkor ugyanolyan hasonlóság alapon csinálják ezt, mint amikor mi eldöntjük azt, hogy valami pogácsa vagy elefánt vagy pingvin. Mit csinálunk? Mi megnézzük azt a kérdést, hogyha fogunk ilyen szavakat, olyanokat is, amelyek egyértelműen köznyelviesedtek, mint a bolond vagy az őrült, amelyek lehet, hogy eredetileg valamilyen pszichiátriai szakszavak voltak a tizenkilencedik században, de már nem úgy használjuk őket meg olyan szavakat is, mint a depresszív meg a szkizoid, amelyik elsősorban klinikai jelentésük. Van de elképzelhető, hogy köznyelviesen is használják őket és szavak az a 2 között, mint az elmebeteg és ezeket össze fogjuk hasonlítani különféle horgony szavakkal, amiket arra használunk, hogy azokról nagyjából tudjuk, hogy hol vannak a szavak közötti hasonlósági térben 4. fejezet módszertan 4 4 szólistát állítottam össze ez a 4 szólista. Ebben vannak egyrészt klinikai horgonyszavak, hétköznapi használatú horgonyszavak, amiknek nincs klinikai jelentésük. Ezek közül vannak pozitív és negatív szavak, és végül vannak célszavaink, mindegyik melléknév, mert szeretnénk egyforma szófajú szavakat használni, mert ezek lesznek egymáshoz. Hasonló, akit nem érdemes keverni a főnevet az igért meg a melléknevet 1. kategória. Klinikai hormonszavak ezek olyan diagnosztikus klinikai technikai szavak, amelyeknek nem igazán van jól érthető köznyelvű megfelelőjük, például komorbiditás, remisszió, etiológia, kórkép türettan nozológia, kritérium, vissza például terápiarezisztens, dekompenzált patológiás szubklinikai. Multifaktoriális benignus malignus neurodegeneratív ezek klinikai szavak ezeket nem használjuk köznapi értelemben akkor vannak olyan szavaink, amik csak köznapi értelemben használjuk. Nincsen klinikai jelentésük, ezek közül használunk pozitív berakunk ide pozitív szavakat, jó remek, nagyszerű, kiváló, kitűnő, fantasztikus isteni mennyei, boldog vidám és negatív szavakat. Rossz szörnyű, borzasztó, rémes, förtelmes, unalmas, szomorú, satöbbi és végül az utolsó kategória. Célszavaink ezek azok a szavak, amikről azt gondoljuk, hogy lehet klinikai jelentésük is, meg lehet köznapi jelentésük is, és meg akarjuk mondani, hogy hol vannak körülbelül ilyenek a depressziós, traumatizált fóbiás, mániás, paranoiás, neurotikus autista szkizofrén addikt bipoláris toxikus. Valamint az őrült bolond elmebeteg szó különféle erősen köznyelvi vagy erősen klinikai változatai elmebeteg, beszámíthatatlan, dilis hibbant, abnormális zakkandeszelős habókos van a hun ember nulla pont nulla, ami egy world to back. A dathalmaz, amit a web corpus egyből és a hangarian netsora corpus magyar nemzeti szövegtárból raktunk össze. Nem mi raktuk össze, meg kell ezt majd hivatkozni, és egyszerűen azt fogjuk megnézni, hogy ha csinálunk egy kétdimenziós teret, akkor ebben ezek a szavak hol lesznek 5. fejezet eredmények az ábrán egy kétdimenziós tér látható itt az x. tengelyen. Ha azt látjuk, hogy egy szó az elsősorban a klinikai szavak között fordul elő, vagy a köznyelvi szavak között látjuk, hogy a kékkel jelölt pontok azok a klinikai szavak, amiknek nem nagyon van köznyelvi jelentésük, és ők valóban ennek a ennek a tengelynek a baloldalán helyezkednek el nagyjából egy halomban és. A lila és a sárga szavak pedig azok a szavak, amiknek valamilyen köznyelv jelentésük van. Ezek hogy láthatóan hogy csak köznyelvű jelentésük van, ezek láthatóan a jobb oldalán helyezkednek el. Ennek a tengelynek az y. tengely a merőleges tengely, azon pedig egy pozitív negatív dimenzióban. Egyrészt látjuk azt, hogy azok a klinikai szavak, amiknek nincs köznyelvi jelentésük ezek a horgon szavak ezek nem nagyon van pozitív vagy negatív jelentésük semleges a klinikai használat. És ehhez képest AA köznyelvi semleges vagy pozitív horgony szavaink azok elég szépen a felső részén vannak ennek az eloszlásnak a köznyelvi, de inkább negatív, pejoratív horgony szavaink pedig az alján. Tehát ez a 3 szóhalmaz ez jól kijelöli ezt a 2 dimenziós ábrát, és azt látjuk, hogy középen vannak azok a szavak, amiket megvizsgáltunk, és ezeknek a szavaknak van egy ilyen eloszlásuk, ami kezdődik. Nagyjából a háromszög alakú kezdődik azokkal a szavakkal, amelyek meglehetősen klinikai használhatóak, és ezek jellemzően vagy semleges vagy pozitív értelműek. Tehát nem nagyon szólnak negatív tartományba, és ahogy haladunk a köznyelvies jelentés felé, úgy egyre inkább szórnak a szavak. Egyre inkább tudnak felvenni pejoratív vagy pozitív jelentéstartományokat, főleg egyébként pejoratívakat azt látjuk kezdjük balról. Hogy olyan szavak, mint a traumás, a pszichotikus vagy a bipoláris azok nagyon egyértelműen a klinikai oldalon vannak. Ezek elsősorban klinikai jelentésben vannak használva, és ehhez képest az autista az addikt, a függő, a hiperaktív, a traumatizált, a kényszeres, a depressziós és a neurotikus. Azok már kezdenek haladni a közgyelvi szavak felé. És aztán van egy olyan osztály ami már meglehetősen a köznyelvi oldalon van és kimondottan negatív jelentések van itt vannak olyan szavak, amik nem túl meglepőek, mint az őrült. A tboi út meg az sz l. és ezeknek nem nagyon van klinikai jelentésük. Az őrültnek volt valaha és vannak olyan szavak is mint az elmebeteg, a beszámíthatatlan és a paranoiás. Ezek kimondottan klinikai szavak az elmebeteg meg a beszámíthatatlan. Azok nem elsősorban pszichiátriai szavak, hanem inkább a jogban. Van jelentőségük ezek valamilyen fajta korlátozottságot írnak le, ami releváns akkor, amikor valaki ellen eljárást folytatnak, vagy valamilyen jogait akarja gyakorolni, szavazni akar vagy birtokolni valamit. Itt van a paranoiás is, mint erősen negatív szó, és akkor van néhány olyan szó, ami nem nagyon mondható klinikai szónak. Ez a flúgos, a megszállott és a habókos, ezeknek pozitív. Jelentésük van inkább, de ezek nem annyira valamilyenek. Azt látjuk tehát, hogy a háromfajta horgonyszó osztályunk az viszonylag jól kijelol egy kétdimenziós teret, ami a klinikaitól a köznyelvig terjed az x tengelyen és a payorative tól a semleges pozitívig az y tengelyen és AA kiválasztott célszavaink. Azok ezen szóródnak elég szépen nagyjából az intuícióinak megfelelően azt lehet látni, hogy például a az olyan szavak, mint az autista vagy a neurotikus, azok ugyan köznyelviesebbek, mint gondolnánk, de jóval kevésbé vannak ennek a jobb oldalán. Tehát itt ebből az derül ki, hogy az autista szó például. Az adat halmaz szerint nem használják általános pejoratív jelzőként az emberek, sokkal inkább van egy klinikai használata, és ugyanez igaz a szkizofrén, vagy akár a mániás szóra is. Az is azért látszik, hogy elkezdenek szóródni ezek a pozitív negatív tartományban, ahogyan egyre inkább köznyelvi használatuk. Érdekes módon az autista szónak aránylag semleges a használata. Úgy tűnik, hogy az autizmusról szóló diskurzust ebben az adathalmazban dominálja ez a klinikai vagy nevelési vagy oktatási réteg, ami használja ezt a szót és az egymást autistának hívó ilyen módon pejoratívan szót használó szöveg használatok azok kevésbé láthatóak. Míg mondjuk AA neuratikus meg a depressziós, bár azok sem teljesen köznyelvi esetek annyira, mint a tébolygult meg a megszállott, de láthatóan negatívabbak pejoratívabbak. Itt már megjelenik az a fajta használat ebben az olt halmazban, ami köznevesíti őket, és ezzel együtt pejoratívak lesznek. Nem tudom hányadik fejezet diszkusszió elismételjük a lényeget. És elmondjuk a korlátokat. Fontos, hogy itt nem egy drift van. Ez egy statikus adathalmaz. Nem azt állítom, hogy ezek a szavak mennek balról, jobbról, fentről lefelé, hanem hogy ott vannak az adatok, amiket használunk. Azok aránylag régiek a webcort, plusz az például kilencvenhetesekben. A legtöbb informális köznyelvi használat van a magyar nemzeti szövegtár az elsősorban formális szövegeket tömörít. Tehát, hogyha ha volt egy nagyon nagy therapy speak elmozdulás az elmúlt 15 évben azért nem fog látszani máshogy is lehetne ezt mérni. Meg lehetne például azt nézni, hogy mennyire konzisztens konzisztens egyes szavak használata meg lehetne nézni, hogy a depresszív szót azt konzisztensebben használják-e, mint AAA az őrült szót. És még mindenféle másképp is meg lehetne mérni ezeknek a szavaknak AA köznyelviesedését. Ez csak egy igazából illusztratív módszer, amelyet választottunk. Ettől függetlenül ez az egész egy kicsit érdekes lehet valakinek néha. 

 