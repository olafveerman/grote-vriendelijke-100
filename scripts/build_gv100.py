import csv, re, unicodedata
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

# (rank, title as listed, author, goodreads_book_id)
D = {}

D[2021] = """1|Lampje|Annet Schaap|34684344
2|De brief voor de koning (De brief voor de koning, #1)|Tonke Dragt|1835829
3|Kruistocht in spijkerbroek|Thea Beckman|3114666
4|Pluk van de Petteflet|Annie M.G. Schmidt|2854614
5|Koning van Katoren (Katoren, #1)|Jan Terlouw|1165759
6|De gebroeders Leeuwenhart|Astrid Lindgren|6262236
7|Harry Potter en de Steen der Wijzen (Harry Potter, #1)|J.K. Rowling|1033918
8|Hier is de boze heks (De boze Heks #8)|Hanna Kraan|8192274
9|Matilda|Roald Dahl|39988
10|Ronja de roversdochter|Astrid Lindgren|6891198
11|Gozert (De wereld van Gozert, #1)|Pieter Koolwijk|50361357
12|De GVR|Roald Dahl|5094631
13|Meester van de zwarte molen|Otfried Preußler|6034016
14|De kleine kapitein|Paul Biegel|634518
15|Kinderen van Moeder Aarde (De Toekomsttrilogie, #1)|Thea Beckman|3418598
16|Sjakie en de chocoladefabriek|Roald Dahl|4821094
17|Alleen op de wereld|Hector Malot|2977918
18|Het grote boek van Madelief|Guus Kuijer|6351760
19|Het sleutelkruid|Paul Biegel|5943825
20|Hasse Simonsdochter|Thea Beckman|1551211
21|Oorlogswinter|Jan Terlouw|2859279
22|Het oneindige verhaal|Michael Ende|3153563
23|Pippi Langkous|Astrid Lindgren|55459211
24|Harry Potter en de Gevangene van Azkaban (Harry Potter, #3)|J.K. Rowling|871319
25|De Zevensprong|Tonke Dragt|2594251
26|Harry Potter en de Geheime Kamer (Harry Potter, #2)|J.K. Rowling|2954426
27|Alfabet|Charlotte Dematons|53557513
28|De Heksen|Roald Dahl|5037819
29|Achtste-groepers huilen niet|Jacques Vriens|8050771
30|De jongen, de mol, de vos en het paard|Charlie Mackesy|51522027
31|De Gruffalo|Julia Donaldson|20761304
32|De tuinen van Dorr|Paul Biegel|3216174
33|Torenhoog en mijlen breed: een toekomstverhaal|Tonke Dragt|254103
34|Lennox en de gouden sikkel|Zindzi Zevenbergen|58372819
35|Briefjes voor Pelle|Marlies Slegers|55210688
36|Ik ben Krik, Krik ben ik|Hanna Kraan|28396692
37|De Gorgels|Jochem Myjer|26258898
38|Blauwe plekken|Anke de Vries|5505028
39|Het verlangen van de prins|Marco Kunst|54142013
40|Geef me de ruimte! (Trilogie over de 100 jarige oorlog, #1)|Thea Beckman|4951108
41|Heksenkind|Monica Furlong|8050857
42|Over een kleine mol die wil weten wie er op zijn kop gepoept heeft|Werner Holzwarth|2854757
43|Zonder titel|Erna Sassen|57597009
44|De geheime tuin|Frances Hodgson Burnett|44297948
45|Minoes|Annie M.G. Schmidt|1795353
46|De zweetvoetenman: Over rechtszaken & regels [en een hoop gedoe]|Annet Huizing|36180421
47|Rupsje Nooitgenoeg|Eric Carle|5505274
48|De Griezels|Roald Dahl|13047146
49|De kinderen van Bolderburen|Astrid Lindgren|6891221
50|De meisjes: zeven sprookjes|Annet Schaap|58765674
51|Otje|Annie M.G. Schmidt|2854606
52|Daantje de Wereldkampioen|Roald Dahl|4914286
53|Luna (De wereld van Gozert, #2)|Pieter Koolwijk|58246250
54|De tunnel|Anna Woltz|54714008
55|Een groene bloem trilogie|Floortje Zwigtman|25675755
56|Ik geef je de zon|Jandy Nelson|25146347
57|Alle verhalen van Kikker en Pad|Arnold Lobel|11449132
58|Wat je moet doen als je over een nijlpaard struikelt|Edward van de Vendel|46040367
59|Morrigan Crow en het Wondergenootschap (Nevermoor, #1)|Jessica Townsend|36628833
60|Jij mag alles zijn|Griet Op de Beeck|58910636
61|Harry Potter en de Vuurbeker (Harry Potter, #4)|J.K. Rowling|1079278
62|Levende bezems|Lisa Tetzner|8409660
63|Dromer|Mark Janssen|59144707
64|Geheimen van het Wilde Woud (De brief voor de koning, #2)|Tonke Dragt|254108
65|Spinder|Simon van der Geest|16025508
66|Films die nergens draaien|Yorick Goldewijk|59007349
67|Honderd uur nacht|Anna Woltz|21903699
68|De Veger|Jonathan Auxier|45014592
69|Momo en de tijdspaarders|Michael Ende|5592552
70|De Tillermans: de zwerftocht van vier kinderen op zoek naar een thuis|Cynthia Voigt|9738710
71|Negen open armen|Benny Lindelauf|8088579
72|Alaska|Anna Woltz|32506287
73|De torens van februari|Tonke Dragt|6660038
74|Wiplala en Wiplala weer (Wiplala #1-2)|Annie M.G. Schmidt|1758589
75|Je moet dansen op mijn graf|Aidan Chambers|8214198
76|Lepelsnijder|Marjolijn Hof|43187703
77|Doodgewoon|Bette Westera|24035558
78|Winnie de Poeh: De complete verzameling verhalen en gedichten|A.A. Milne|24348748
79|De kinderkaravaan|An Rutgers van der Loeff|8061173
80|Hele verhalen voor een halve soldaat|Benny Lindelauf|55659338
81|Hart van Inkt|Cornelia Funke|7556418
82|Kruimeltje|Chris van Abkoude|13040977
83|Allemaal willen we de hemel|Els Beerten|3836891
84|Het Gulden Vlies van Thule (De Toekomsttrilogie, #3)|Thea Beckman|2282658
85|Koningskind|Selma Noort|55434569
86|Nachtverhaal|Paul Biegel|2182814
87|Spijt|Carry Slee|1699435
88|Dit is geen dagboek|Erna Sassen|10416398
89|Kleine Sofie en Lange Wapper|Els Pelgrom|675259
90|Het Ministerie van Oplossingen (Het Ministerie van Oplossingen, #1)|Sanne Rooseboom|30625199
91|Wij gaan op berenjacht|Michael Rosen|12971006
92|Max en de Maximonsters|Maurice Sendak|6015198
93|Avonturen van de dappere ridster|Janneke Schotveld|53972382
94|Polleke|Guus Kuijer|12825370
95|Nederland|Charlotte Dematons|16035468
96|Floddertje|Annie M.G. Schmidt|1466832
97|Gips|Anna Woltz|25389557
98|Zeb.|Gideon Samson|38331882
99|Wonderbos|Jan Paul Schutten|55587367
100|Monkie|Dieter Schubert|4345257"""

# 2022: Goodreads mirror is incomplete and mis-ordered. Only verified positions included.
D[2022] = """1|Lampje|Annet Schaap|
2|Films die nergens draaien|Yorick Goldewijk|
3|Gozert|Pieter Koolwijk|
4|De brief voor de koning|Tonke Dragt|
5|Harry Potter en de Steen der Wijzen|J.K. Rowling|
6|Kruistocht in spijkerbroek|Thea Beckman|
7|Matilda|Roald Dahl|
8|Pluk van de Petteflet|Annie M.G. Schmidt|
9|Mot en de metaalvissers|Sanne Rooseboom|
10|Koning van Katoren|Jan Terlouw|
12|De gebroeders Leeuwenhart|Astrid Lindgren|
14|Ronja de roversdochter|Astrid Lindgren|
15|Hier is de boze heks|Hanna Kraan|"""

D[2023] = """1|Lampje|Annet Schaap|34684344
2|Films die nergens draaien|Yorick Goldewijk|63005893
3|Mot en de metaalvissers|Sanne Rooseboom|60772880
4|Misjka|Edward van de Vendel|62096324
5|De brief voor de koning (De brief voor de koning, #1)|Tonke Dragt|1835829
6|Pluk van de Petteflet|Annie M.G. Schmidt|2854614
7|Gozert (De wereld van Gozert, #1)|Pieter Koolwijk|50361357
8|De jongen die van de wereld hield|Tjibbe Veldkamp|197502517
9|Briefjes voor Pelle|Marlies Slegers|55210688
10|Kruistocht in spijkerbroek|Thea Beckman|3114666
11|Harry Potter en de Steen der Wijzen (Harry Potter, #1)|J.K. Rowling|1033918
12|Vandaag houd ik mijn spreekbeurt over de anaconda|Bibi Dumon Tak|63205347
13|Het weeshuis in de azuurblauwe zee (Cerulean Chronicles, #1)|T.J. Klune|60145242
14|Matilda|Roald Dahl|5037376
15|Koning van Katoren (Katoren, #1)|Jan Terlouw|1165759
16|De GVR|Roald Dahl|5094631
17|De gebroeders Leeuwenhart|Astrid Lindgren|6262236
18|Missie afbreken (De wereld van Gozert, #3)|Pieter Koolwijk|153554520
19|Ronja de roversdochter|Astrid Lindgren|6891198
20|De grote boze heks|Hanna Kraan|184768371
21|Alfabet|Charlotte Dematons|53557513
22|Kinderen van Moeder Aarde (De Toekomsttrilogie, #1)|Thea Beckman|3418598
23|De tunnel|Anna Woltz|54714008
24|Meester van de zwarte molen|Otfried Preußler|6034016
25|Alleen op de wereld|Hector Malot|2977918
26|Luna (De wereld van Gozert, #2)|Pieter Koolwijk|58246250
27|Sinterklaas|Charlotte Dematons|7692635
28|Zolang de citroenbomen bloeien|Zoulfa Katouh|62909947
29|De kleine kapitein|Paul Biegel|634518
30|Jij mag alles zijn|Griet Op de Beeck|58910636
31|Jip en Janneke (Jip en Janneke, #1-5)|Annie M.G. Schmidt|1484848
32|We moeten je iets vertellen|Marlies Slegers|122289309
33|Ik denk dat ik ontvoerd ben en andere gedichten|Pim Lammers|62677523
34|Een zee van liefde|Pieter Gaudesaboos|59479437
35|Het oneindige verhaal|Michael Ende|3153563
36|Het boomhuis in het bos|T.J. Klune|194070072
37|Sjakie en de chocoladefabriek|Roald Dahl|4821094
38|Hasse Simonsdochter|Thea Beckman|1551211
39|Wat je moet doen als je over een nijlpaard struikelt|Edward van de Vendel|46040367
40|Hart van staal|Simon van der Geest|177142001
41|Het grote boek van Madelief|Guus Kuijer|6351760
42|Oorlogswinter|Jan Terlouw|4812236
43|De Gorgels|Jochem Myjer|26258898
44|Over een kleine mol die wil weten wie er op zijn kop gepoept heeft|Werner Holzwarth|2854757
45|Allemaal willen we de hemel|Els Beerten|3836891
46|De Gruffalo|Julia Donaldson|20761304
47|Patroon|Marco Kunst|61092730
48|Dodo|Mohana van den Kroonenberg|61180820
49|Alaska|Anna Woltz|32506287
50|Het Ministerie van Oplossingen (Het Ministerie van Oplossingen, #1)|Sanne Rooseboom|30625199
51|Momo en de tijdspaarders|Michael Ende|5592552
52|De geheime tuin|Frances Hodgson Burnett|44297948
53|Lennox en de gouden sikkel|Zindzi Zevenbergen|58372819
54|Heel de wereld wordt wakker|Jaap Robben|62989111
55|IJzerkop|Jean-Claude van Rijckeghem|45731329
56|Hele verhalen voor een halve soldaat|Benny Lindelauf|55659338
57|Tori|Brian Elstak|36340366
58|Mus & kapitein Kwaadbaard en De 5 slangen (Mus en kapitein Kwaadbaard, #1)|Kevin Hassing|55790993
59|De tuinen van Dorr|Paul Biegel|3216174
60|Het sleutelkruid|Paul Biegel|5943825
61|De Zevensprong|Tonke Dragt|2594251
62|Lepelsnijder|Marjolijn Hof|43187703
63|Ik geef je de zon|Jandy Nelson|25146347
64|Daantje de Wereldkampioen|Roald Dahl|4914286
65|Jefferson|Jean-Claude Mourlevat|60778600
66|Pippi Langkous (Pippi Langkous, #1)|Astrid Lindgren|13446134
67|Gelukkig en blij|Edward van de Vendel|179103167
68|Quotum: Project Z|Marloes Morshuis|121167206
69|Harry Potter en de Gevangene van Azkaban (Harry Potter, #3)|J.K. Rowling|871319
70|Robin: alle verhalen|Sjoerd Kuyper|61227889
71|Het kleine heelal|Annejan Mieras|126110740
72|Heksenkind|Monica Furlong|8050857
73|Terra ultima: De ontdekkingsreis van een onbekend continent|Raoul Deleo|58202355
74|Iep!|Joke van Leeuwen|2493376
75|Alle verhalen van Kikker en Pad|Arnold Lobel|11449132
76|De kinderen van Bolderburen|Astrid Lindgren|6891221
77|De jongen, de mol, de vos en het paard|Charlie Mackesy|51522027
78|Minoes|Annie M.G. Schmidt|1795353
79|Monkie|Dieter Schubert|4345257
80|De reis van Manie Schaafijs|Zindzi Zevenbergen|195802877
81|Torenhoog en mijlen breed: een toekomstverhaal|Tonke Dragt|254103
82|Winterijs|Peter van Gestel|8331367
83|Zonder titel|Erna Sassen|57597009
84|Achtste-groepers huilen niet|Jacques Vriens|8050771
85|Spinder|Simon van der Geest|16025508
86|Jona|Anna van Praag|122850498
87|De Veger|Jonathan Auxier|45014592
88|Otje|Annie M.G. Schmidt|2854606
89|Floddertje|Annie M.G. Schmidt|1466832
90|Wij gaan op berenjacht|Michael Rosen|12971006
91|De Heksen|Roald Dahl|5037819
92|De zoon van de berentemmer|Xavier-Laurent Petit|114195099
93|De weg naar terug (Pluk en Pluis #1)|Mathilde Stein|62847777
94|De allergrootste|Davide Morosinotto|61855794
95|In het vervloekte hart (Bloedmaan, #1)|Rima Orie|61301265
96|Avonturen van de dappere ridster|Janneke Schotveld|53972382
97|Een kleine geschiedenis van de mens door dierenogen|Joukje Akveld|75521022
98|Het pad van de Roverkoning (De Zeven Sleutels, #1)|Tom Rijpert|180072082
99|Morris|Bart Moeyaert|62344373
100|Bob Popcorn|Maranke Rinck|50223074"""

D[2024] = """1|Films die nergens draaien|Yorick Goldewijk|63005893
2|Mot en de metaalvissers|Sanne Rooseboom|60772880
3|Lampje|Annet Schaap|34684344
4|Gozert (De wereld van Gozert, #1)|Pieter Koolwijk|50361357
5|De jongen die van de wereld hield|Tjibbe Veldkamp|197502517
6|Briefjes voor Pelle|Marlies Slegers|55210688
7|De brief voor de koning (De brief voor de koning, #1)|Tonke Dragt|1835829
8|Kruistocht in spijkerbroek|Thea Beckman|3114666
9|Pluk van de Petteflet|Annie M.G. Schmidt|2854614
10|Vandaag houd ik mijn spreekbeurt over de anaconda|Bibi Dumon Tak|63205347
11|Harry Potter en de Steen der Wijzen (Harry Potter, #1)|J.K. Rowling|1033918
12|De zomer die alles was|Mariska Overman|211171082
13|Koning van Katoren (Katoren, #1)|Jan Terlouw|1165759
14|Misjka|Edward van de Vendel|62096324
15|Oever|Ludwig Volbeda|209749885
16|Kinderen van Moeder Aarde (De Toekomsttrilogie, #1)|Thea Beckman|3418598
17|Het weeshuis in de azuurblauwe zee (Cerulean Chronicles, #1)|T.J. Klune|60145242
18|Luna (De wereld van Gozert, #2)|Pieter Koolwijk|58246250
19|Ronja de roversdochter|Astrid Lindgren|6891198
20|Het kleine heelal|Annejan Mieras|126110740
21|De GVR|Roald Dahl|5094631
22|Missie afbreken (De wereld van Gozert, #3)|Pieter Koolwijk|153554520
23|Matilda|Roald Dahl|5037376
24|De gebroeders Leeuwenhart|Astrid Lindgren|6262236
25|We moeten je iets vertellen|Marlies Slegers|122289309
26|Vandaag komen we niet meer thuis|Enne Koens|125659234
27|De tunnel|Anna Woltz|54714008
28|Welkom thuis, chrononauten|Dirk Weber|206465154
29|De kleine kapitein|Paul Biegel|634518
30|Zolang de citroenbomen bloeien|Zoulfa Katouh|62909947
31|De grote boze heks|Hanna Kraan|184768371
32|Jij mag alles zijn|Griet Op de Beeck|58910636
33|Alleen op de wereld|Hector Malot|2977918
34|De lijst van Violet Sopjes|David Vlietstra|202580313
35|Meester van de zwarte molen|Otfried Preußler|6034016
36|Alfabet|Charlotte Dematons|53557513
37|Het pad van de Roverkoning (De Zeven Sleutels, #1)|Tom Rijpert|180072082
38|Sjakie en de chocoladefabriek|Roald Dahl|4821094
39|Achtste-groepers huilen niet|Jacques Vriens|8050771
40|Oorlogswinter|Jan Terlouw|4812236
41|Hart van staal|Simon van der Geest|177142001
42|De weg naar terug (Pluk en Pluis #1)|Mathilde Stein|62847777
43|Wat je moet doen als je over een nijlpaard struikelt|Edward van de Vendel|46040367
44|Mus en kapitein Kwaadbaard en De laatste sirene (Mus en kapitein Kwaadbaard #5)|Kevin Hassing|213571695
45|Alaska|Anna Woltz|32506287
46|Hasse Simonsdochter|Thea Beckman|1551211
47|De trein van vier over twaalf|Conny Palmkvist|205530850
48|Mus & kapitein Kwaadbaard en De 5 slangen (Mus en kapitein Kwaadbaard, #1)|Kevin Hassing|55790993
49|De spin en de sleutel|Anna Woltz|199061267
50|De boom die een wereld was|Yorick Goldewijk|205786873
51|De reis van Manie Schaafijs|Zindzi Zevenbergen|195802877
52|Dodo|Mohana van den Kroonenberg|61180820
53|Jefferson|Jean-Claude Mourlevat|60778600
54|Neem nooit een beste vriend|Erna Sassen|83298095
55|Ik geef je de zon|Jandy Nelson|25146347
56|De Gorgels|Jochem Myjer|26258898
57|Een zee van liefde|Pieter Gaudesaboos|59479437
58|Het oneindige verhaal|Michael Ende|3153563
59|Ik denk dat ik ontvoerd ben en andere gedichten|Pim Lammers|62677523
60|De toch niet zo eenzame tocht van Torre|Annekarijn Overduin|57881872
61|Ghost (Track, #1)|Jason Reynolds|102191279
62|Struikmeisje|Tineke Honingh|137182390
63|Zoef!|Janneke Schotveld|213916443
64|Het grote boek van Madelief|Guus Kuijer|6351760
65|De Zevensprong|Tonke Dragt|2594251
66|Het sleutelkruid|Paul Biegel|5943825
67|Het Ministerie van Oplossingen (Het Ministerie van Oplossingen, #1)|Sanne Rooseboom|30625199
68|Umbrador|Marieke Smithuis|198971741
69|IJzerkop|Jean-Claude van Rijckeghem|45731329
70|Prutje|Pieter Koolwijk|41968643
71|Jip en Janneke (Jip en Janneke, #1-5)|Annie M.G. Schmidt|1484848
72|Spinder|Simon van der Geest|16025508
73|Harry Potter en de Gevangene van Azkaban (Harry Potter, #3)|J.K. Rowling|871319
74|Torenhoog en mijlen breed: een toekomstverhaal|Tonke Dragt|254103
75|Momo en de tijdspaarders|Michael Ende|5592552
76|Pippi Langkous (Pippi Langkous, #1)|Astrid Lindgren|13446134
77|De geheime tuin|Frances Hodgson Burnett|44297948
78|Jij bent de liefste|Hans Hagen|6709646
79|Lennox en de gouden sikkel|Zindzi Zevenbergen|58372819
80|Kauw van jou|Kris Terwindt|220078478
81|Gelukkig en blij|Edward van de Vendel|179103167
82|Alle verhalen van Kikker en Pad|Arnold Lobel|11449132
83|De torens van februari|Tonke Dragt|6660038
84|Lepelsnijder|Marjolijn Hof|43187703
85|Blauwe plekken|Anke de Vries|5505028
86|De kinderen van Bolderburen|Astrid Lindgren|6891221
87|De allergrootste|Davide Morosinotto|61855794
88|Roversjong|Jef Aerts|209446724
89|Patroon|Marco Kunst|61092730
90|Geef me de ruimte! (Trilogie over de 100 jarige oorlog, #1)|Thea Beckman|4951108
91|Als de wereld wankelt|Jandy Nelson|215035331
92|Heel de wereld wordt wakker|Jaap Robben|62989111
93|Hele verhalen voor een halve soldaat|Benny Lindelauf|55659338
94|De Veger|Jonathan Auxier|45014592
95|Zonder titel|Erna Sassen|57597009
96|De Gruffalo|Julia Donaldson|20761304
97|Minoes|Annie M.G. Schmidt|1795353
98|Over een kleine mol die wil weten wie er op zijn kop gepoept heeft|Werner Holzwarth|2854757
99|Allemaal willen we de hemel|Els Beerten|3836891
100|Een slijmzoen voor je oma|Matthijs Meeuwsen|175319065"""

D[2025] = """1|Films die nergens draaien|Yorick Goldewijk|63005893
2|Krekel|Annet Schaap|227898061
3|Lampje|Annet Schaap|34684344
4|Mot en de metaalvissers|Sanne Rooseboom|60772880
5|Gozert (De wereld van Gozert, #1)|Pieter Koolwijk|50361357
6|Briefjes voor Pelle|Marlies Slegers|55210688
7|De brief voor de koning (De brief voor de koning #1)|Tonke Dragt|57828433
8|Pluk van de Petteflet|Annie M.G. Schmidt|2854614
9|Nog 27 dagen leven|Maren Stoffels|215149885
10|Koning van Katoren (Katoren, #1)|Jan Terlouw|1165759
11|Kruistocht in spijkerbroek|Thea Beckman|3114666
12|Een rugzak vol|Pieter Koolwijk|227781613
13|Harry Potter en de Steen der Wijzen (Harry Potter, #1)|J.K. Rowling|1033918
14|De zomer die alles was|Mariska Overman|211171082
15|De jongen die van de wereld hield|Tjibbe Veldkamp|197502517
16|Kinderen van Moeder Aarde (De Toekomsttrilogie, #1)|Thea Beckman|3418598
17|Matilda|Roald Dahl|5037376
18|De wonderverteller|Lida Dijkstra|216836755
19|Vandaag komen we niet meer thuis|Enne Koens|125659234
20|De gebroeders Leeuwenhart|Astrid Lindgren|6262236
21|De lijst van Violet Sopjes|David Vlietstra|202580313
22|De Heksenkind trilogie|Monica Furlong|216501307
23|De GVR|Roald Dahl|25468265
24|Albatros|Yorick Goldewijk|241646754
25|Ronja de roversdochter|Astrid Lindgren|6891198
26|Luna (De wereld van Gozert, #2)|Pieter Koolwijk|58246250
27|Vandaag houd ik mijn spreekbeurt over de anaconda|Bibi Dumon Tak|63205347
28|Zolang de citroenbomen bloeien|Zoulfa Katouh|62909947
29|19|91|Tom Rijpert|222207570
30|Schildpadmeisje|Marlies Slegers|229015199
31|De kleine kapitein|Paul Biegel|13564914
32|Misjka|Edward van de Vendel|62096324
33|Het weeshuis in de azuurblauwe zee (Cerulean Chronicles, #1)|T.J. Klune|60145242
34|De glazenwasser van het Rijksmuseum|Astrid Sy|218129911
35|Oever|Ludwig Volbeda|209749885
36|Mus en kapitein Kwaadbaard en De laatste sirene (Mus en kapitein Kwaadbaard #5)|Kevin Hassing|213571695
37|Mus & kapitein Kwaadbaard en De 5 slangen (Mus en kapitein Kwaadbaard, #1)|Kevin Hassing|55790993
38|We moeten je iets vertellen|Marlies Slegers|122289309
39|De grote boze heks|Hanna Kraan|184768371
40|De toch niet zo eenzame tocht van Torre|Annekarijn Overduin|57881872
41|Hasse Simonsdochter|Thea Beckman|1551211
42|Oorlogswinter|Jan Terlouw|4812236
43|Duizend stukjes overal|Mariska Overman|223461349
44|De tunnel|Anna Woltz|54714008
45|Het meisje dat er niet mocht zijn|Wilma Geldof|230317922
46|Umbrador|Marieke Smithuis|198971741
47|Jij mag alles zijn|Griet Op de Beeck|58910636
48|De Raadselbreker (Oerbloed #1)|Rob Koops|192564474
49|De Gorgels|Jochem Myjer|26258898
50|Alleen op de wereld|Hector Malot|34201607
51|Het grote boek van Madelief|Guus Kuijer|6351760
52|Missie afbreken (De wereld van Gozert, #3)|Pieter Koolwijk|153554520
53|Sjakie en de chocoladefabriek|Roald Dahl|4821094
54|Meester van de zwarte molen|Otfried Preußler|6034016
55|Alfabet|Charlotte Dematons|53557513
56|De weg naar terug (Pluk en Pluis #1)|Mathilde Stein|62847777
57|Prutje|Pieter Koolwijk|41968643
58|Achtste-groepers huilen niet|Jacques Vriens|8050771
59|De geheime tuin|Frances Hodgson Burnett|44297948
60|Alaska|Anna Woltz|32506287
61|Welkom thuis, chrononauten|Dirk Weber|206465154
62|De Gruffalo|Julia Donaldson|20761304
63|Hart van staal|Simon van der Geest|177142001
64|De Zevensprong|Tonke Dragt|2594251
65|De Kronieken van Narnia|C.S. Lewis|2962328
66|Blauwe plekken|Anke de Vries|5505028
67|De allergrootste|Davide Morosinotto|61855794
68|Het oneindige verhaal|Michael Ende|3153563
69|Jip en Janneke (Jip en Janneke, #1-5)|Annie M.G. Schmidt|1484848
70|Het sleutelkruid|Paul Biegel|21518496
71|Ik geef je de zon|Jandy Nelson|25146347
72|De reis van Manie Schaafijs|Zindzi Zevenbergen|195802877
73|Wat je moet doen als je over een nijlpaard struikelt|Edward van de Vendel|46040367
74|Zoef!|Janneke Schotveld|213916443
75|Momo en de tijdspaarders|Michael Ende|5592552
76|Het Ministerie van Oplossingen (Het Ministerie van Oplossingen, #1)|Sanne Rooseboom|30625199
77|Wat ons nog rest|Aline Sax|199332224
78|Een zee van liefde|Pieter Gaudesaboos|59479437
79|Jij bent de liefste|Hans Hagen|6709646
80|Roversjong|Jef Aerts|209446724
81|Het pad van de Roverkoning (De Zeven Sleutels, #1)|Tom Rijpert|180072082
82|Kauw van jou|Kris Terwindt|220078478
83|Het kleine heelal|Annejan Mieras|126110740
84|Torenhoog en mijlen breed: een toekomstverhaal|Tonke Dragt|254103
85|Over een kleine mol die wil weten wie er op zijn kop gepoept heeft|Werner Holzwarth|2854757
86|Otje|Annie M.G. Schmidt|2854606
87|Harry Potter en de Gevangene van Azkaban (Harry Potter, #3)|J.K. Rowling|871319
88|Alle verhalen van Kikker en Pad|Arnold Lobel|11449132
89|Als de wereld wankelt|Jandy Nelson|215035331
90|De kinderen van Bolderburen|Astrid Lindgren|6891221
91|Minoes|Annie M.G. Schmidt|1795353
92|Ik denk dat ik ontvoerd ben en andere gedichten|Pim Lammers|62677523
93|Allemaal willen we de hemel|Els Beerten|3836891
94|Geef me de ruimte! (Trilogie over de 100 jarige oorlog, #1)|Thea Beckman|4951108
95|Pippi Langkous (Pippi Langkous, #1)|Astrid Lindgren|13446134
96|Ik ben Vincent en ik ben niet bang|Enne Koens|34928621
97|De ruïnes van Gorlan (De Grijze Jager, #1)|John Flanagan|9437985
98|Spinder|Simon van der Geest|16025508
99|Complot: De spannendste samenzweringstheorieën (en zijn ze waar?)|Jan Paul Schutten|235371180
100|Het laatste jaar|Matt Goodfellow|230094719"""

SRC = {
    2021: "https://www.goodreads.com/list/show/169403.De_Grote_Vriendelijke_100_2021",
    2022: "https://www.dekinderboekenwinkel.nl/de-grote-vriendelijke-100/",
    2023: "https://www.goodreads.com/list/show/223552.De_Grote_Vriendelijke_100_2023",
    2024: "https://www.goodreads.com/list/show/223554.De_Grote_Vriendelijke_100_2024",
    2025: "https://www.goodreads.com/list/show/237563.De_Grote_Vriendelijke_100_2025",
}

def split_series(t):
    m = re.match(r"^(.*?)\s*\(([^()]*#[^()]*)\)\s*$", t)
    return (m.group(1), m.group(2)) if m else (t, "")

def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def work_key(title, author):
    return norm(title) + " | " + norm(author.split()[-1])

rows = []
for year, block in D.items():
    for line in block.strip().splitlines():
        parts = line.split("|")
        rank, gid = int(parts[0]), parts[-1]
        author = parts[-2]
        raw = "|".join(parts[1:-2])  # handles '19|91'
        title, series = split_series(raw)
        rows.append(dict(year=year, rank=rank, title=title, series=series, author=author,
                         work_key=work_key(title, author),
                         goodreads_id=gid, source=SRC[year]))

# sanity checks
for y in D:
    rs = sorted(r["rank"] for r in rows if r["year"] == y)
    assert len(rs) == len(set(rs)), y
    if y != 2022:
        assert rs == list(range(1, 101)), (y, len(rs))
    keys = [r["work_key"] for r in rows if r["year"] == y]
    dup = {k for k in keys if keys.count(k) > 1}
    assert not dup, (y, dup)

with open(OUT / "gv100_long.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# wide: one row per work
years = sorted(D)
works = {}
for r in rows:
    w_ = works.setdefault(r["work_key"], {"work_key": r["work_key"], "title": r["title"], "author": r["author"]})
    w_[f"rank_{r['year']}"] = r["rank"]
wide = []
for w_ in works.values():
    full = [y for y in years if y != 2022]
    w_["editions_present"] = sum(1 for y in years if f"rank_{y}" in w_)
    ranks = [w_[f"rank_{y}"] for y in full if f"rank_{y}" in w_]
    w_["best_rank"] = min(ranks) if ranks else ""
    wide.append(w_)
wide.sort(key=lambda w_: (-w_["editions_present"], w_.get("rank_2025", 999)))
fields = ["work_key", "title", "author"] + [f"rank_{y}" for y in years] + ["editions_present", "best_rank"]
with open(OUT / "gv100_wide.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, restval="")
    w.writeheader(); w.writerows(wide)

ed = [
    dict(year=2021, entries=100, complete="yes", voters="~2500", voting_closed="2021-11-07", announced="2021-11-24", source=SRC[2021]),
    dict(year=2022, entries=13, complete="no (top 10 + ranks 12, 14, 15 only)", voters="3000+", voting_closed="2022-11-06", announced="2022-11-23", source=SRC[2022]),
    dict(year=2023, entries=100, complete="yes", voters="", voting_closed="2023-11-05", announced="", source=SRC[2023]),
    dict(year=2024, entries=100, complete="yes", voters="~4000", voting_closed="2024-11-03", announced="2024-11-23", source=SRC[2024]),
    dict(year=2025, entries=100, complete="yes", voters="5500", voting_closed="", announced="2025-11-23", source=SRC[2025]),
]
with open(OUT / "gv100_editions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(ed[0].keys()))
    w.writeheader(); w.writerows(ed)

print(len(rows), "rows;", len(wide), "distinct works")
