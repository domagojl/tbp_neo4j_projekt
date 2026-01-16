from neo4j import GraphDatabase

# --- KONFIGURACIJA ---
# Prilagodi URI i AUTH svojim postavkama u Neo4j-u
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "lozinka123") 

class DatabaseSetup:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

    def run_setup(self):
        with self.driver.session() as session:
            print("--- 1. Brisanje starih podataka... ---")
            session.run("MATCH (n) DETACH DELETE n")

            print("--- 2. Postavljanje Constraints-a i Indeksa... ---")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:Recept) REQUIRE r.naslov IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (k:Korisnik) REQUIRE k.email IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Sastojak) REQUIRE s.naziv IS UNIQUE")

            print("--- 3. Ubacivanje 30 recepata (Full Data)... ---")
            
            recepti_data = [
                {
                    "n": "Špageti Carbonara", "v": 20, "t": "Lako", "k": "Talijanska",
                    "o": "Autentični talijanski klasik s kremastim umakom od jaja i hrskavom pancetom.",
                    "p": "Priprema prave carbonare zahtijeva brzinu i preciznost kako jaja ne bi postala kajgana. Prvo zakuhajte veliku količinu posoljene vode i skuhajte špagete al dente. Dok se tjestenina kuha, na hladnu tavu stavite narezanu guanciale ili pancetu i polako zagrijavajte dok masnoća ne postane prozirna, a meso hrskavo. U maloj posudi umutite cijela jaja s puno svježe naribanog Pecorino Romano sira i crnog papra. Ključni trenutak je spajanje: tjesteninu prebacite izravno u tavu s pancetom, maknite s vatre i ulijte smjesu od jaja. Energično miješajte dodajući žlicu po žlicu vode od kuhanja dok ne dobijete baršunastu, sjajnu emulziju. Poslužite odmah s dodatnim paprom.",
                    "s": [{"n": "Špageti", "q": "400g"}, {"n": "Jaja", "q": "3 kom"}, {"n": "Panceta", "q": "150g"}, {"n": "Pecorino", "q": "50g"}]
                },
                {
                    "n": "Rižoto s kozicama", "v": 40, "t": "Srednje", "k": "Mediteranska",
                    "o": "Elegantan i kremast rižoto s okusom mora i svježim začinskim biljem.",
                    "p": "Temelj svakog dobrog rižota je kvalitetan temeljac. Prvo na maslinovom ulju kratko popržite repove kozica, izvadite ih, pa na istoj masnoći dinstajte sitno sjeckanu ljutiku dok ne postane staklasta. Dodajte Arborio rižu i tostirajte je dok rubovi zrna ne postanu prozirni. Podlijte suhim bijelim vinom i miješajte dok alkohol ne ispari. Zatim kreće proces polaganog dodavanja vrućeg temeljca, kutlaču po kutlaču, uz stalno miješanje kako bi riža otpustila škrob. Pred sam kraj vratite kozice u tavu. Kada je riža kuhana al dente, maknite s vatre i napravite mantekaturu – umiješajte kockicu hladnog maslaca i malo peršina. Pustite da odmori dvije minute prije posluživanja.",
                    "s": [{"n": "Riža Arborio", "q": "300g"}, {"n": "Kozice", "q": "400g"}, {"n": "Bijelo vino", "q": "100ml"}, {"n": "Maslac", "q": "30g"}]
                },
                {
                    "n": "Pileći Curry", "v": 45, "t": "Srednje", "k": "Azijska",
                    "o": "Bogato i aromatično jelo s mješavinom indijskih začina i kokosovim mlijekom.",
                    "p": "Započnite mariniranjem pilećih prsa u jogurtu i malo kurkume. U dubokoj tavi zagrijte ulje i popržite luk, češnjak i svježi đumbir dok ne zamirišu. Dodajte mješavinu začina: korijander, kumin, kurkumu i malo čilija. Tostirajte začine minutu, pa dodajte meso. Kada se piletina zapeče, ulijte pasiranu rajčicu i lagano krčkajte deset minuta. Ključni korak je dodavanje gustog kokosovog mlijeka koje će ublažiti ljutinu i dati jelu prepoznatljivu teksturu. Kuhajte na laganoj vatri dok umak ne postane gust. Na samom kraju dodajte šaku svježeg špinata da samo uvene u umaku. Poslužite uz kuhanu basmati rižu koju ste prethodno isprali nekoliko puta kako bi zrna ostala odvojena.",
                    "s": [{"n": "Piletina", "q": "500g"}, {"n": "Kokosovo mlijeko", "q": "400ml"}, {"n": "Kurkuma", "q": "1 žličica"}, {"n": "Đumbir", "q": "20g"}]
                },
                {
                    "n": "Goveđi Gulaš", "v": 120, "t": "Srednje", "k": "Domaća",
                    "o": "Tradicionalno jelo na žlicu koje zahtijeva dugo kuhanje za savršenu mekoću mesa.",
                    "p": "Tajna vrhunskog gulaša je u omjeru luka i mesa – trebalo bi ih biti podjednako. Kilogram luka narežite na sitno i dinstajte na masti uz prstohvat soli barem 30 minuta dok se potpuno ne raspadne. Govedinu narežite na kocke, posušite je i dodajte na luk. Pecite meso dok ne dobije smeđu boju sa svih strana. Dodajte mljevenu slatku i ljutu papriku, koncentrat rajčice, lovorov list i malo kima. Podlijte crnim vinom i toplom vodom tek toliko da pokrije meso. Poklopite i kuhajte na minimalnoj vatri dva do tri sata. Povremeno protresite lonac, ali izbjegavajte previše miješanja. Gulaš je gotov kada se meso raspada na pritisak vilice, a umak je prirodno gust bez dodavanja brašna.",
                    "s": [{"n": "Govedina", "q": "1kg"}, {"n": "Crveni luk", "q": "800g"}, {"n": "Crno vino", "q": "200ml"}, {"n": "Paprika mljevena", "q": "2 žlice"}]
                },
                {
                    "n": "Grčka Salata", "v": 15, "t": "Lako", "k": "Mediteranska",
                    "o": "Osvježavajuća ljetna salata s autentičnim feta sirom i maslinama.",
                    "p": "Iako se čini jednostavnom, grčka salata zahtijeva vrhunske sastojke. Krastavce narežite na deblje polumjesece, a rajčice na veće kocke. Crveni luk narežite na vrlo tanke kolutove i namočite ih kratko u hladnoj vodi kako bi izgubili oštrinu. Papriku očistite i narežite na kolute. Sve povrće stavite u veliku zdjelu i dodajte kalamata masline. Za dresing koristite isključivo ekstra djevčansko maslinovo ulje, sušeni origano i malo crvenog vinskog octa. Najvažnije: feta sir nemojte miješati u salatu već ga stavite u jednom komadu na vrh. Pospite s još malo origana i maslinovog ulja. Poslužite uz topli domaći kruh kojim možete toćati sokove koji ostanu na dnu zdjele.",
                    "s": [{"n": "Feta sir", "q": "200g"}, {"n": "Rajčica", "q": "3 kom"}, {"n": "Krastavac", "q": "1 kom"}, {"n": "Masline", "q": "50g"}]
                },
                {
                    "n": "Wok s Piletinom", "v": 20, "t": "Lako", "k": "Azijska",
                    "o": "Brza priprema povrća i mesa na visokoj temperaturi koja čuva nutrijente.",
                    "p": "Pripremite sve sastojke unaprijed jer sam proces pečenja traje svega nekoliko minuta. Piletinu narežite na tanke trakice i marinirajte u soja umaku i malo sezamovog ulja. Povrće – mrkvu, papriku, brokulu i mladi luk – narežite na podjednake komade. Wok zagrijte do točke dimljenja, dodajte ulje i prvo pecite meso dok ne postane zlatno. Izvadite meso, dodajte još malo ulja i ubacite povrće. Neprestano miješajte i tresite wok kako povrće ne bi izgorjelo, ali bi ostalo hrskavo. Vratite piletinu, ulijte mješavinu soja umaka, naribanog đumbira i malo škrobnog brašna razmućenog u vodi. Sve skupa promiješajte još minutu dok se umak ne zgusne i postane sjajan. Poslužite uz staklene rezance.",
                    "s": [{"n": "Piletina", "q": "300g"}, {"n": "Miješano povrće", "q": "400g"}, {"n": "Soja umak", "q": "50ml"}]
                },
                {
                    "n": "Lasagne Bolognese", "v": 90, "t": "Teško", "k": "Talijanska",
                    "o": "Složeni klasik s domaćim bešamelom i polagano kuhanim mesnim umakom.",
                    "p": "Prvi korak je priprema ragua: dinstajte luk, mrkvu i celer (sofrito) na maslacu dok ne omekšaju. Dodajte mljeveno meso i pržite ga dok potpuno ne posmeđi. Podlijte vinom, a zatim dodajte pasiranu rajčicu i kuhajte na laganoj vatri barem sat vremena. Za bešamel otopite maslac, dodajte brašno i postupno ulijevajte mlijeko uz stalno miješanje dok ne dobijete gusti umak bez grudica. Začinite ga muškatnim oraščićem. Slaganje lasagni započnite slojem ragua na dnu vatrostalne posude, zatim red tijesta, pa ragu, pa bešamel i obilno parmezana. Ponovite barem četiri sloja. Završite s bešamelom i puno sira. Pecite na 180 stupnjeva oko 35 minuta dok se na vrhu ne stvori zlatna hrskava korica.",
                    "s": [{"n": "Mljeveno meso", "q": "600g"}, {"n": "Tijesto za lasagne", "q": "500g"}, {"n": "Mlijeko", "q": "1L"}, {"n": "Parmezan", "q": "100g"}]
                },
                {
                    "n": "Burger s Cheddarom", "v": 30, "t": "Srednje", "k": "Američka",
                    "o": "Sočna govedina u mekanom pecivu s rastopljenim sirom i karameliziranim lukom.",
                    "p": "Za savršen burger koristite goveđi vrat s barem 20% masnoće. Meso oblikujte u pljeskavice težine 150g, pazeći da ne stišćete previše kako bi ostale sočne. Luk narežite na tanke listiće i dinstajte na laganoj vatri s malo maslaca i šećera dok ne postane taman i ljepljiv. Pljeskavice pecite na jako zagrijanoj grill tavi 3-4 minute po strani. Minutu prije kraja, na svaku stavite listu debelog cheddara i poklopite tavu da se sir otopi. Peciva prerežite i tostirajte na unutrašnjoj strani. Donji dio peciva premažite umakom od majoneze i senfa, stavite list salate, rajčicu, pljeskavicu sa sirom i na kraju karamelizirani luk. Čvrsto pritisnite i poslužite uz domaće pržene krumpiriće.",
                    "s": [{"n": "Mljevena govedina", "q": "450g"}, {"n": "Cheddar sir", "q": "3 lista"}, {"n": "Peciva", "q": "3 kom"}, {"n": "Luk", "q": "2 kom"}]
                },
                {
                    "n": "Sushi Rolice", "v": 60, "t": "Teško", "k": "Azijska",
                    "o": "Precizno pripremljena riža i svježa riba umotani u nori algu.",
                    "p": "Najvažniji dio sushija je riža. Koristite rižu kratkog zrna, dobro je isperite i skuhajte prema uputama. Još toplu rižu začinite mješavinom rižinog octa, šećera i soli te je hladite mahanjem lepezom. Nori algu stavite na podlogu od bambusa, rasporedite tanak sloj riže ostavljajući rub praznim. Na sredinu stavite trakice svježe tunjevine ili lososa, tanke kriške krastavca i malo wasabija. Pomoću podloge čvrsto zarolajte algu oko punjenja. Rub alge navlažite s malo vode kako bi se zalijepio. Oštrim nožem koji ste umočili u vodu narežite rolicu na šest ili osam dijelova. Poslužite uz soja umak, ukiseljeni đumbir i wasabi pastu. Kvaliteta sushija ovisi isključivo o svježini ribe i teksturi riže koja ne smije biti gnjecava.",
                    "s": [{"n": "Sushi riža", "q": "300g"}, {"n": "Nori alge", "q": "5 kom"}, {"n": "Tuna", "q": "200g"}, {"n": "Krastavac", "q": "1 kom"}]
                },
                {
                    "n": "Čokoladni Fondant", "v": 25, "t": "Srednje", "k": "Francuska",
                    "o": "Topli desert s tekućom čokoladnom sredinom poznat i kao lava cake.",
                    "p": "Ovaj desert zahtijeva precizno tempiranje pećnice. Na pari otopite kvalitetnu tamnu čokoladu s barem 70% kakaa i maslac. U drugoj posudi pjenasto umutite jaja sa šećerom dok ne postanu svijetla i gusta. Lagano špatulom sjedinite čokoladu s jajima, a zatim prosijte malo brašna i prstohvat soli. Kalupe za pečenje dobro namažite maslacem i pospite kakaom u prahu kako se kolač ne bi zalijepio. Ulijte smjesu do 3/4 visine kalupa. Pecite točno 10-12 minuta na 200 stupnjeva. Rubovi moraju biti pečeni i čvrsti, ali sredina mora ostati mekana na dodir. Ostavite minutu u kalupu, pa pažljivo preokrenite na tanjur. Poslužite s kuglicom sladoleda od vanilije ili svježim malinama koje će dati kiselost.",
                    "s": [{"n": "Tamna čokolada", "q": "200g"}, {"n": "Maslac", "q": "100g"}, {"n": "Jaja", "q": "4 kom"}, {"n": "Šećer", "q": "80g"}]
                },
                {
                    "n": "Tortilje s junetinom", "v": 35, "t": "Srednje", "k": "Meksička",
                    "o": "Pikantne tortilje punjene sočnom junetinom, grahom i kukuruzom.",
                    "p": "Priprema meksičkih tortilja započinje mariniranjem junećih odrezaka u mješavini limete, kumina i dimljene paprike. Meso narežite na tanke trakice i pecite na jako zagrijanoj tavi dok ne dobije hrskavu vanjštinu. U istoj tavi popržite luk, papriku narezanu na trakice, crveni grah i kukuruz šećerac. Ključno je dodati malo soka od rajčice kako bi smjesa bila sočna. Tortilje kratko zagrijte na suhoj tavi da postanu savitljive. Svaku tortilju premažite kiselim vrhnjem, stavite izdašan sloj mesnog punjenja, pospite ribanim sirom i svježim korijanderom. Zarolajte ih čvrsto i po želji kratko zapecite u pećnici dok se sir ne otopi. Poslužite uz pikantnu salsu i domaći guacamole od zrelog avokada.",
                    "s": [{"n": "Junetina", "q": "500g"}, {"n": "Tortilje", "q": "6 kom"}, {"n": "Grah", "q": "200g"}, {"n": "Kukuruz", "q": "100g"}]
                },
                {
                    "n": "Losos s parmezanom", "v": 25, "t": "Lako", "k": "Mediteranska",
                    "o": "Pečeni fileti lososa s hrskavom koricom od parmezana i češnjaka.",
                    "p": "Ovaj recept za losos idealan je za brzu, ali elegantnu večeru. Filete lososa očistite od ljuskica, osušite kuhinjskim papirom i posolite. U maloj posudi pomiješajte naribani parmezan, krušne mrvice, protisnuti češnjak, svježi peršin i malo limunove korice. Gornju stranu svakog fileta premažite tankim slojem senfa koji će poslužiti kao ljepilo za hrskavu smjesu. Obilno pritisnite smjesu od sira na losos. Pecite u pećnici zagrijanoj na 200 stupnjeva oko 12 do 15 minuta, ovisno o debljini fileta. Losos unutra mora ostati blago ružičast i sočan, dok korica mora postati zlatna i hrskava. Poslužite uz blanširane mahune ili pečene šparoge pokapane s par kapi vrhunskog maslinovog ulja.",
                    "s": [{"n": "Losos", "q": "400g"}, {"n": "Parmezan", "q": "50g"}, {"n": "Krušne mrvice", "q": "30g"}]
                },
                {
                    "n": "Francuska juha od luka", "v": 60, "t": "Srednje", "k": "Francuska",
                    "o": "Bogata juha s karameliziranim lukom i zapečenim sirom.",
                    "p": "Tajna vrhunske juhe od luka leži u dugotrajnoj karamelizaciji luka na laganoj vatri. Kilogram crvenog luka narežite na tanke polumjesece i dinstajte na maslacu barem 40 minuta dok ne dobije tamnu boju jantara i slatkast okus. Dodajte žličicu šećera za bolju boju i žlicu brašna za gustoću. Podlijte s malo bijelog vina, a zatim dodajte litu kvalitetnog goveđeg temeljca i lovorov list. Kuhajte još 20 minuta. Juhu ulijte u vatrostalne zdjelice, na vrh stavite prepečenu krišku kruha i obilno pospite sirom Gruyere. Zdjelice stavite pod gornji grijač pećnice na par minuta dok sir ne počne mjehurati i poprimi smećkastu boju. Ova juha je nevjerojatno hranjiva i pruža dubinu okusa.",
                    "s": [{"n": "Crveni luk", "q": "1kg"}, {"n": "Temeljac", "q": "1L"}, {"n": "Gruyere sir", "q": "150g"}]
                },
                {
                    "n": "Ratatouille", "v": 50, "t": "Srednje", "k": "Francuska",
                    "o": "Provansalsko povrtno varivo koje slavi ljetne plodove vrta.",
                    "p": "Ratatouille se može pripremati kao varivo ili kao vizualno atraktivno složeno jelo. Narežite patlidžane, tikvice, paprike i rajčice na kockice podjednake veličine. Svako povrće zasebno kratko popržite na maslinovom ulju kako bi zadržalo svoju teksturu i boju. U velikom loncu dinstajte luk i češnjak, dodajte koncentrat rajčice i majčinu dušicu. Zatim sjedinite svo poprženo povrće i lagano krčkajte oko 15 minuta. Važno je ne prekuhati povrće kako se ne bi pretvorilo u kašu. Na kraju dodajte svježi bosiljak i još malo maslinovog ulja. Ratatouille se može poslužiti topao kao prilog uz meso ili hladan uz prepečeni baget i kozji sir, što ga čini izuzetno svestranim ljetnim jelom.",
                    "s": [{"n": "Patlidžan", "q": "2 kom"}, {"n": "Tikvica", "q": "2 kom"}, {"n": "Paprika", "q": "3 kom"}, {"n": "Rajčica", "q": "4 kom"}]
                },
                {
                    "n": "Njoki u gorgonzoli", "v": 20, "t": "Lako", "k": "Talijanska",
                    "o": "Brzi i kremasti njoki za ljubitelje snažnih okusa sira.",
                    "p": "Ovaj recept je savršen za dane kada želite nešto luksuzno u vrlo kratkom vremenu. Njoke skuhajte u slanoj vodi, pazeći da ih izvadite čim isplivaju na površinu. U širokoj tavi zagrijte vrhnje za kuhanje na laganoj vatri i dodajte nasjeckanu gorgonzolu. Miješajte dok se sir potpuno ne otopi i umak ne postane gladak. Dodajte malo papra i prstohvat muškatnog oraščića, ali budite oprezni sa solju jer je sir sam po sebi slan. Kuhane njoke prebacite izravno u umak i lagano promiješajte. Za dodatnu teksturu, u umak možete dodati šaku krupno sjeckanih oraha koji su prethodno lagano tostirani na suhoj tavi. Poslužite odmah uz svježu rikolu koja će balansirati bogatstvo sira.",
                    "s": [{"n": "Njoki", "q": "500g"}, {"n": "Gorgonzola", "q": "150g"}, {"n": "Vrhnje za kuhanje", "q": "200ml"}]
                },
                {
                    "n": "Piletina Tikka Masala", "v": 50, "t": "Srednje", "k": "Indijska",
                    "o": "Aromatična piletina u bogatom, začinjenom umaku od rajčice.",
                    "p": "Tikka Masala počinje mariniranjem piletine u mješavini jogurta, limuna i indijskih začina poput garam masale, kurkume i đumbira. Meso bi trebalo odležati barem sat vremena kako bi omekšalo. Piletinu zatim ispecite na grill tavi dok ne dobije tamne rubove. Umak pripremite dinstanjem luka, češnjaka i đumbira, dodajući pasirane rajčice i preostale začine. Ključna je duga redukcija umaka na laganoj vatri dok ne postane gust i intenzivan. Na kraju umiješajte malo slatkog vrhnja za prepoznatljivu narančastu boju. Vratite piletinu u umak i kratko prokuhajte. Poslužite uz topli naan kruh ili kuhanu basmati rižu, ukrašeno svježim listićima korijandera koji daju potrebnu svježinu.",
                    "s": [{"n": "Piletina", "q": "600g"}, {"n": "Jogurt", "q": "150g"}, {"n": "Pasirana rajčica", "q": "400ml"}]
                },
                {
                    "n": "Domaće okruglice", "v": 40, "t": "Srednje", "k": "Domaća",
                    "o": "Sočne mesne okruglice u klasičnom crvenom umaku uz pire.",
                    "p": "Domaće polpete ili okruglice rade se od miješanog mljevenog mesa, natopljenog kruha u mlijeku, jaja i peršina. Sve sastojke dobro sjedinite rukama, oblikujte kuglice veličine oraha i uvaljajte ih u malo brašna. Okruglice prvo kratko popržite na ulju sa svih strana da zadrže sokove, a zatim ih izvadite. Na istoj masnoći popržite malo koncentrata rajčice i podlijte pasiranom rajčicom i vodom. Vratite okruglice u umak, dodajte lovorov list i malo šećera da neutralizirate kiselost rajčice. Kuhajte na laganoj vatri oko pola sata dok umak ne postane gust. Poslužite uz pire krumpir u koji ste dodali dosta maslaca i malo mlijeka za savršenu kremastu teksturu. Ovo jelo uvijek budi uspomene.",
                    "s": [{"n": "Mljeveno meso", "q": "500g"}, {"n": "Pasirana rajčica", "q": "500ml"}, {"n": "Krumpir", "q": "800g"}]
                },
                {
                    "n": "Špageti Aglio e Olio", "v": 15, "t": "Lako", "k": "Talijanska",
                    "o": "Minimalistički klasik od samo nekoliko vrhunskih sastojaka.",
                    "p": "Aglio e Olio je dokaz da vrhunsko jelo ne mora biti komplicirano. Dok se špageti kuhaju u slanoj vodi, u hladnu tavu stavite obilnu količinu maslinovog ulja i pet režnja češnjaka narezanih na najtanje listiće. Dodajte i sitno sjeckanu čili papričicu. Polako zagrijavajte tavu; češnjak ne smije izgorjeti već samo postati zlatno-žut. Čim tjestenina postane al dente, prebacite je u tavu uz dodatak pola šalice vode od kuhanja. Energično miješajte na vatri dok se voda i ulje ne emulgiraju u lagani umak koji oblaže tjesteninu. Maknite s vatre, dodajte šaku sjeckanog peršina i poslužite odmah. Ovo jelo je esencija talijanske filozofije kuhanja gdje kvaliteta ulja igra glavnu ulogu.",
                    "s": [{"n": "Špageti", "q": "400g"}, {"n": "Češnjak", "q": "5 režnja"}, {"n": "Maslinovo ulje", "q": "80ml"}]
                },
                {
                    "n": "Prebranac", "v": 90, "t": "Srednje", "k": "Balkanska",
                    "o": "Gusto, polagano pečeno jelo od graha i puno luka.",
                    "p": "Prebranac započinje kuhanjem krupnog bijelog graha dok ne postane mekan, ali se ne raspadne. Istovremeno, u drugoj posudi dinstajte veliku količinu luka narezanog na rebarca dok potpuno ne uvene i ne postane sladak. U luk dodajte dosta mljevene crvene paprike, sol i papar. U vatrostalnu posudu slažite red graha, pa red dinstanog luka. Ponovite dok ne potrošite sastojke, završavajući slojem graha. Podlijte s malo vode u kojoj se kuhao grah, tek toliko da sve bude pokriveno. Pecite u pećnici na 180 stupnjeva dok tekućina skoro potpuno ne ispari, a na vrhu se ne uhvati fina, lagano zapečena korica. Poslužite uz pečene kobasice i svježi domaći kruh.",
                    "s": [{"n": "Grah tetovac", "q": "500g"}, {"n": "Luk", "q": "600g"}, {"n": "Paprika mljevena", "q": "20g"}]
                },
                {
                    "n": "Tortellini s kaduljom", "v": 20, "t": "Lako", "k": "Talijanska",
                    "o": "Elegantna tjestenina u umaku od spaljenog maslaca i kadulje.",
                    "p": "Burro e Salvia je klasičan način pripreme punjene tjestenine. Tortelline skuhajte u posoljenoj vodi. Dok se kuhaju, u širokoj tavi rastopite 100 grama maslaca. Kada se maslac zapjeni, dodajte desetak svježih listića kadulje. Maslac zagrijavajte dok ne počne poprimati smećkastu boju i miris lješnjaka, a listići kadulje ne postanu hrskavi. Budite oprezni da maslac ne izgori. Dodajte par žlica vode od kuhanja tjestenine da zaustavite proces pečenja maslaca. Kuhane tortelline ubacite u tavu, ugasite vatru i protresite da se umak ravnomjerno rasporedi. Poslužite uz puno svježe naribanog parmezana koji će se lagano otopiti i povezati sve okuse u savršenu cjelinu.",
                    "s": [{"n": "Tortellini", "q": "500g"}, {"n": "Maslac", "q": "100g"}, {"n": "Kadulja", "q": "10 listova"}]
                },
                {
                    "n": "Meksički Tacos", "v": 30, "t": "Lako", "k": "Meksička",
                    "o": "Male kukuruzne tortilje punjene mesom, lukom i svježim korijanderom.",
                    "p": "Tacos al pastor ili obični tacosi zahtijevaju tanko narezano meso pečeno na jakoj vatri. Meso posolite i začinite čilijem. Kukuruzne tortilje kratko zagrijte na tavi dok ne dobiju boju. Na svaku tortilju stavite meso, sitno sjeckani bijeli luk, listiće rotkvice i jako puno svježeg korijandera. Ključni dodatak je svježa limeta koju istisnete preko mesa neposredno prije konzumacije. Možete dodati i malo pikantne salse od zelenih rajčica. Ovo jelo se jede isključivo rukama i predstavlja samu srž meksičke ulične hrane koja se bazira na balansu masnoće, kiseline i ljutine začina.",
                    "s": [{"n": "Svinjetina", "q": "400g"}, {"n": "Kukuruzne tortilje", "q": "8 kom"}, {"n": "Korijander", "q": "1 vezica"}]
                },
                {
                    "n": "Piletina s limunom", "v": 30, "t": "Lako", "k": "Mediteranska",
                    "o": "Lagana piletina u osvježavajućem umaku od limuna i kapara.",
                    "p": "Pileća prsa narežite na tanje šnicle, istucite ih batom i lagano pobrašnite. Pecite na mješavini maslaca i ulja dok ne porumene. Izvadite meso, a u tavu ulijte sok dva limuna, malo pilećeg temeljca i žlicu kapara. Pustite da umak proključa i malo se reducira. Vratite piletinu u tavu kako bi upila sokove i kako bi se brašno s mesa povezalo s tekućinom u lagani kremasti umak. Na kraju dodajte kockicu hladnog maslaca za sjaj. Poslužite uz kuhanu rižu ili pečene mlade krumpiriće. Ovo jelo je idealno za lagani ručak jer je istovremeno zasićujuće i osvježavajuće zbog visoke koncentracije citrusa.",
                    "s": [{"n": "Piletina", "q": "500g"}, {"n": "Limun", "q": "2 kom"}, {"n": "Kapari", "q": "1 žlica"}]
                },
                {
                    "n": "Falafel u lepinji", "v": 45, "t": "Srednje", "k": "Azijska",
                    "o": "Pržene kuglice od slanutka s puno začina, poslužene u toplom kruhu.",
                    "p": "Slanutak za falafel mora se namakati preko noći, nikako nemojte koristiti onaj iz konzerve. Namočeni slanutak sameljite u blenderu s lukom, češnjakom, puno peršina, kuminom i korijanderom u prahu. Smjesa mora biti zrnata, ne kašasta. Dodajte malo sode bikarbone kako bi kuglice bile prozračne. Oblikujte male polpete i pržite ih u dubokom ulju dok ne postane tamno smeđe i hrskave. Poslužite ih u toploj pita lepinji uz dodatak humusa, svježih krastavaca, rajčice i obaveznog tahini umaka (namaz od sezama). Falafel je jedan od najpopularnijih vegetarijanskih obroka na svijetu zbog svoje bogate teksture i začinjenosti.",
                    "s": [{"n": "Slanutak", "q": "400g"}, {"n": "Pita kruh", "q": "4 kom"}, {"n": "Tahini", "q": "50g"}]
                },
                {
                    "n": "Goveđi Steak", "v": 15, "t": "Teško", "k": "Američka",
                    "o": "Vrhunski komad junetine pečen do savršenstva uz maslac i ružmarin.",
                    "p": "Steak izvadite iz hladnjaka barem sat vremena prije pečenja kako bi postigao sobnu temperaturu. Dobro ga posušite i obilno posolite. Pecite na jako zagrijanoj tavi (najbolje od lijevanog željeza) 3 minute sa svake strane za medium-rare. U zadnjoj minuti pečenja dodajte veliku kocku maslaca, dva režnja češnjaka i grančicu ružmarina. Žlicom prelijevajte rastopljeni aromatični maslac preko mesa (basting). Najvažniji korak: ostavite steak da odmori barem 5-7 minuta na toplom tanjuru prije rezanja. To omogućuje sokovima da se redistribuiraju kroz meso, umjesto da iscure na dasku. Poslužite uz krupnu sol i svježe mljeveni papar.",
                    "s": [{"n": "Rib-eye steak", "q": "400g"}, {"n": "Maslac", "q": "50g"}, {"n": "Ružmarin", "q": "1 grančica"}]
                },
                {
                    "n": "Penne Arrabbiata", "v": 15, "t": "Lako", "k": "Talijanska",
                    "o": "Pikantna tjestenina u umaku od rajčice, češnjaka i čilija.",
                    "p": "Arrabbiata na talijanskom znači 'ljutita', što opisuje karakter ovog umaka. Na maslinovom ulju popržite dosta protisnutog češnjaka i barem dvije narezane ljute papričice. Pazite da češnjak ne zagori. Dodajte konzerviranu pelat rajčicu koju ste prethodno usitnili rukama. Kuhajte na jakoj vatri desetak minuta dok se umak ne zgusne. Penne skuhajte u puno slane vode, ocijedite i ubacite u umak. Sve dobro promiješajte i pospite svježim peršinom. Iako mnogi dodaju sir, autentična arrabbiata se često jede bez sira kako bi ljutina čilija ostala u prvom planu. Ovo je osnovno jelo rimske kuhinje koje se oslanja na snagu jednostavnih, ali moćnih sastojaka.",
                    "s": [{"n": "Penne tjestenina", "q": "400g"}, {"n": "Pelati", "q": "400g"}, {"n": "Čili papričica", "q": "2 kom"}]
                },
                {
                    "n": "Sataraš", "v": 40, "t": "Lako", "k": "Balkanska",
                    "o": "Ljetni klasik od paprike, rajčice i luka, idealan uz rižu.",
                    "p": "Sataraš je jelo koje slavi sezonsko povrće. Na ulju dinstajte puno luka narezanog na polumjesece dok ne omekša. Dodajte paprike narezane na trakice i pržite ih dok ne postanu smežurane. Zatim dodajte oguljene i narezane rajčice. Kuhajte bez poklopca na srednjoj vatri kako bi višak tekućine ispario, a okusi se koncentrirali. Povrće se treba gotovo 'pržiti' u vlastitom soku. Začinite solju, paprom i s malo šećera ako su rajčice kisele. Sataraš možete poslužiti kao samostalno jelo uz kuhanu rižu, kao prilog mesu ili s umućenim jajima na kraju. Najbolji je kada odstoji par minuta kako bi se sokovi smirili. Ovo je esencijalno balkansko ljetno jelo.",
                    "s": [{"n": "Paprika", "q": "1kg"}, {"n": "Rajčica", "q": "500g"}, {"n": "Luk", "q": "300g"}]
                },
                {
                    "n": "Quiche Lorraine", "v": 60, "t": "Srednje", "k": "Francuska",
                    "o": "Slana pita s prhkim tijestom, slaninom i bogatim nadjevom od jaja.",
                    "p": "Prhko tijesto zamijesite od brašna, hladnog maslaca i malo ledene vode. Ostavite ga u hladnjaku pola sata. Razvaljajte tijesto i stavite u kalup, izbodite vilicom i 'slijepo' pecite 15 minuta. Za nadjev popržite kockice slanine dok ne postanu hrskave. U zdjeli umutite jaja, slatko vrhnje i malo kiselog vrhnja. Začinite paprom i muškatnim oraščićem (sol obično nije potrebna zbog slanine). Na dno pečenog tijesta rasporedite slaninu i naribani ementaler sir, pa prelijte smjesom od jaja. Pecite na 180 stupnjeva još 30 minuta dok nadjev ne postane čvrst i zlatno žut. Quiche je najbolji kada se posluži mlak uz laganu zelenu salatu s oštrim dresingom.",
                    "s": [{"n": "Brašno", "q": "250g"}, {"n": "Slanina", "q": "200g"}, {"n": "Jaja", "q": "3 kom"}, {"n": "Vrhnje", "q": "250ml"}]
                },
                {
                    "n": "Gulaš od gljiva", "v": 35, "t": "Lako", "k": "Domaća",
                    "o": "Gusti vegetarijanski gulaš s miješanim šumskim gljivama.",
                    "p": "Na ulju dinstajte crveni luk i malo mrkve dok ne omekšaju. Dodajte narezane gljive (šampinjone, bukovače, vrganje) i pržite ih dok ne puste vodu i ponovno je ne upiju. Dodajte češnjak, majčinu dušicu, lovorov list i mljevenu papriku. Podlijte s malo bijelog vina i povrtnog temeljca. Kuhajte na laganoj vatri 20-ak minuta. Kako bi gulaš bio gust, dio gljiva možete izvaditi, izblendati i vratiti u lonac. Na kraju umiješajte žlicu kiselog vrhnja za dodatnu kremoznost. Poslužite uz široke rezance ili palentu. Ovaj gulaš pruža nevjerojatnu dubinu okusa ('umami') i dokazuje da jela bez mesa mogu biti jednako zasićujuća i bogata kao i tradicionalni mesni klasici.",
                    "s": [{"n": "Gljive", "q": "600g"}, {"n": "Luk", "q": "2 kom"}, {"n": "Bijelo vino", "q": "100ml"}]
                },
                {
                    "n": "Paella", "v": 50, "t": "Teško", "k": "Mediteranska",
                    "o": "Španjolski klasik s rižom, šafranom, piletinom i plodovima mora.",
                    "p": "Paella se tradicionalno priprema u širokoj plitkoj tavi. Prvo na maslinovom ulju popržite piletinu narezanu na manje komade. Dodajte narezanu papriku i mahune. Ubacite rižu (bombu ili arborio) i kratko je tostirajte. Dodajte šafran koji ste prethodno namočili u malo tople vode – on daje ključnu žutu boju i miris. Podlijte temeljcem i nemojte više miješati! Na vrh poslažite kozice, dagnje i kolutiće liganja. Pecite na laganoj vatri dok riža ne upije svu tekućinu. Na dnu bi se trebala stvoriti lagano zapečena kora zvana 'socarrat', koja se smatra najboljim dijelom paelle. Pokrijte krpom i pustite da odmori 5 minuta. Poslužite uz kriške limuna za istiskivanje preko morskih plodova.",
                    "s": [{"n": "Riža", "q": "400g"}, {"n": "Piletina", "q": "300g"}, {"n": "Dagnje", "q": "300g"}, {"n": "Šafran", "q": "0.5g"}]
                },
                {
                    "n": "Piletina s Indijskim oraščićima", "v": 25, "t": "Lako", "k": "Azijska",
                    "o": "Hrskava piletina i povrće u slatko-slanom umaku s orašastim plodovima.",
                    "p": "Piletinu narežite na kockice, uvaljajte u malo škroba i popržite u woku dok ne postane hrskava. Izvadite meso. U istu tavu dodajte indijske oraščiće i tostirajte ih dok ne postanu tamno zlatni. Dodajte luk, paprike i narezani celer. Vratite piletinu i prelijte umakom napravljenim od soja umaka, umaka od ostriga (oyster sauce), malo meda i češnjaka. Brzo miješajte na visokoj temperaturi dok umak ne postane gust i ne obloži svaki komad mesa i povrća. Indijski oraščići daju jelu specifičnu teksturu i bogatstvo okusa. Poslužite uz bijelu rižu dugog zrna. Ovo je standardno jelo azijske 'fusion' kuhinje koje balansira različite teksture u jednom tanjuru.",
                    "s": [{"n": "Piletina", "q": "400g"}, {"n": "Indijski oraščići", "q": "100g"}, {"n": "Soja umak", "q": "3 žlice"}]
                }
            ]

            cypher_recepti = """
            UNWIND $data AS recept
            MERGE (r:Recept {naslov: recept.n})
            SET r.vrijeme = recept.v, 
                r.tezina = recept.t, 
                r.kuhinja = recept.k, 
                r.opis = recept.o, 
                r.postupak = recept.p
            WITH r, recept
            UNWIND recept.s AS sastojak
            MERGE (s:Sastojak {naziv: sastojak.n})
            MERGE (r)-[rel:SADRŽI]->(s)
            SET rel.kolicina = sastojak.q
            """
            session.run(cypher_recepti, data=recepti_data)

            print("--- 4. Kreiranje Korisnika i Društvenog Grafa... ---")
            users_query = """
            MERGE (d:Korisnik {ime: 'Domagoj', email: 'domagoj@foi.hr', grad: 'Zagreb'})
            MERGE (m:Korisnik {ime: 'Marko', email: 'marko@foi.hr', grad: 'Varaždin'})
            MERGE (l:Korisnik {ime: 'Lucija', email: 'lucija@foi.hr', grad: 'Zagreb'})
            MERGE (p:Korisnik {ime: 'Petra', email: 'petra@foi.hr', grad: 'Split'})
            MERGE (k:Korisnik {ime: 'Kevin', email: 'kevin@foi.hr', grad: 'Čakovec'})
            MERGE (a:Korisnik {ime: 'Ana', email: 'ana@foi.hr', grad: 'Osijek'})

            // Praćenja (Follows)
            MERGE (d)-[:PRATI]->(m)
            MERGE (d)-[:PRATI]->(l)
            MERGE (d)-[:PRATI]->(p)
            MERGE (m)-[:PRATI]->(l)
            MERGE (l)-[:PRATI]->(k)
            MERGE (k)-[:PRATI]->(m)
            MERGE (p)-[:PRATI]->(a)
            MERGE (a)-[:PRATI]->(d)

            // Lajkovi (Voli) - Kreiranje osnove za preporuke
            WITH d, m, l, p, k, a
            MATCH (r1:Recept {naslov: 'Špageti Carbonara'})
            MATCH (r2:Recept {naslov: 'Burger s Cheddarom'})
            MATCH (r3:Recept {naslov: 'Sushi Rolice'})
            MATCH (r4:Recept {naslov: 'Pileći Curry'})
            MATCH (r5:Recept {naslov: 'Goveđi Steak'})
            MATCH (r6:Recept {naslov: 'Lasagne Bolognese'})
            
            MERGE (d)-[:VOLI]->(r1)
            MERGE (d)-[:VOLI]->(r6)
            
            MERGE (m)-[:VOLI]->(r1)
            MERGE (m)-[:VOLI]->(r2) // Domagoj prati Marka, pa će mu sustav preporučiti Burger
            
            MERGE (l)-[:VOLI]->(r3)
            MERGE (l)-[:VOLI]->(r4) // Domagoj prati Luciju, pa će mu sustav preporučiti Sushi i Curry
            
            MERGE (p)-[:VOLI]->(r5)
            """
            session.run(users_query)

            print("\n--- INSTALACIJA USPJEŠNA! ---")
            print("Baza podataka 'Društvena Kuharica' je spremna.")
            print("Sadrži: 30 recepata, 6 korisnika i kompletan društveni graf.")

if __name__ == "__main__":
    setup = DatabaseSetup(URI, AUTH)
    try:
        setup.run_setup()
    except Exception as e:
        print(f"Greška tijekom instalacije: {e}")
    finally:
        setup.close()