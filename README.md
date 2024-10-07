# real_interval
## Az *interval* modul *Interval* osztálya egy valós értékkészletű korlátos folytonos intervallumot modellez.

Az intervallum típusát, vagyis, hogy mely végpointjain nyitott vagy zárt, az *interval* modul **IntervalType** felsorolástípus megfelelő konstansával lehet megadni az __Interval__ példányosításakor, a végpontok értékeinek megadását követően. Az IntervalType helyett a rövidebb **IType** vagy **IvType** is használható.

**Interval** példányt létrehozni nem csak konstruktorral lehet, hanem az erre szolgáló osztálymetódusokkal is a dokumentációs karakterláncukban leírt módon. 

Egy intervallum matematikailag egy speciális halmaznak tekinthető, ezért az alapvető halmazműveletek mint az unió, metszet, részintervallum és tartalmazásvizsgálat értelmezhetők. Ugyanakkor az intervallum el is tér a halmazoktól, mert sorbarendezhetők hiszen nagyság szerinti sorrendben meghatározott alsó és felső korláttal rendelkeznek, amelyek az intervallum végpontjai. A számegyenesen való ábrázoláskor az alsó korlát az intervallum értékkészeletének bal oldalán, a felső korlát annak jobb oldalán van. Ezért az alsó és felső végpontot, bal illetve jobb oldali végpontnak is nevezik.

Az intervallumot a végpontjai még nem teljesen definiálják. Ugyanis azonos végpontértékekkel rendelkező két intervallum különbözhet egymástól attól függően, hogy a végpontértékeket az intervallum értékkészlete tartalmazza vagy sem. Ha az adott végpontot nem tartalmazza, akkor azon az oldalon az intervallum nyitott, ha tartalmazza akkor zárt. Ennek kombinációi (mindkét oldalon zárt, mindkét oldalon nyitott, bal oldalon zárt és jobb oldalon nyitott, bal oldalon nyitott és jobb oldalon zárt) határozzák meg az intervallum típusát. Ezért egy intervallumot két végpontjának értékei és típusa együttesen definiál.

Ebből következik, hogy az intervallum típusát a műveleteknél figyelembe kell venni. Ez az, ami a halmazokhoz képest összetettebbé teszi az intervallumokkal végzett műveleteket. Az **Interval** metódusai ennek megfelelően működnek.

Az Interval osztály, illetve példányai minden olyan feladatnál és alkalmazásnál hasznosak lehetnek, ahol intervallumok merülnek fel, vagy konkrétan azokkal kell dolgozni. Többek között ilyenek az intervallumfelezést használó eljárások, vagy statisztikai alkalmazások mint például relatív gyakoriságok számítása, hisztogramok készítése, vagy osztályközös gyakorisági sorok statisztikai jellemzőinek (pl. átlag, medián) számítása.

Az *application_examples* mappa az említett három felhasználási esetre ad egy-egy konkrét példát. A négyzetgyökvonás intervallumfelezéssel való megvalósítása nem gyakorlati alkalmazásra készült, hanem inkább csak azt szemlélteti, hogy a felezéses eljárás hogyan valósítható meg az Interval példányokat használva. 
