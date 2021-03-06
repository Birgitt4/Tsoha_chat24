Tämä repositorio on luotu Helsingin yliopiston Tietokantasovellus kurssia varten.

## Keskustelusovellus Chat24
Löydät sovelluksen osoitteesta : https://tsoha-chat24.herokuapp.com/

#### Keskustelut on jaettu alueisiin, joilla on viestejä sisältäviä viestiketjuja
Uutta keskustelua luodessa käyttäjä voi valita, mihin aihealueeseen aloitus kuuluu. Sovelluksen etusivulla käyttäjä voi valita, näkeekö käyttäjä kaikki aloitukset vai vaikka esim. opiskeluun liittyvät aloitukset.

#### Käyttäjä voi olla peruskäyttäjä tai ylläpitäjä
Käyttäjiä on kahta eri tasoa normaaleja käyttäjiä ja ylläpitäjiä. Normaalit käyttäjät voivat aloittaa ketjuja ja muokata omaa aloitusta tai poistaa oman aloituksen. Ylläpitäjä pystyy omien aloitusten ja viestien lisäksi poistamaan toisten viestejä tai koko aloituksen.

#### Käyttäjä voi luoda tunnuksen, lähettää viestejä ja luoda uusia ketjuja
Sivustolle voi luoda tunnuksen. Käyttäjänimen pitää olla uniikki, eli samaa käyttäjänimeä ei voi olla kahdella eri käyttäjällä. Salasanassa on oltava vähintään 6 merkkiä.

Kun käyttäjä on kirjautunut sisään, voi käyttäjä vastata muiden aloituksiin, ketjun alhaalla olevasta viestikentästä. Etusivulla on mahdollisuus aloittaa myös uusi keskustelu klikkaamalla sivun vasemmalla olevaa "Uusi keskustelu" linkkiä. Käyttäjä voi valita, onko keskustelu julkinen vai yksityinen ja mihin aihealueeseen aloitus kuuluu.

#### Käyttäjä pystyy muokkaamaan viestiä ja poistamaan sen myöhemmin
Käyttäjä pystyy ketjussa muokkaamaan tai poistamaan omia viestejään. Muokkaus/poisto mahdollisuus löytyy oman viestin oikealta puolelta lähettäjän käyttäjänimen vierestä.

#### Viestejä voi etsiä hakutoiminnolla
Etusivulla on hakutoiminto, johon voi antaa hakusanan sekä valita etsiikö tuloksia aloituksista vastauksista vai kummastakin. Jos käyttäjä ei valitse kumpaakaan tuloksia ei tule. Aloituksista etsimällä toiminto hakee otsikoista sekä aloittajan ensimmäisestä viestistä. Viesteistä etsimällä hakutulokset tulevat luonnollisesti vastauksista, jos käyttäjä löytää etsimäänsä hän pääsee kyseiseen ketjuun klikkaamalla tulosta.

Kun käyttäjä hakee aloituksista ja viesteistä tulokset tulevat eri "sivuille". Näiden välillä voi vaihtaa tulosten ylläolevista napeista.

#### Sovellukseen voi luoda myös salaisia alueita, jolle on pääsy vain tietyillä käyttäjillä
Salaiset alueet on toteutettu kavereiden väilinä yksityis/ryhmä keskusteluina. Jos käyttäjä pyytää toista käyttäjää kaveriksi, ja tämä toinen käyttäjä hyväksyy pyynnön, voi käyttäjä luoda yksityisen keskustelut ja lisätä tähän omia kavereitaa. Käyttäjän omat yksityiset aloitukset ja yksityiset aloitukset, johon käyttäjä on lisätty löytyvät käyttäjän omasta profiilistaan kohdasta yksityiset keskustelut.


### Testaajalle
Voit testata sovellusta normaaleilla käyttäjillä testi1 ja testi2 (salasanat ovat sama kuin käyttäjätunnus "testi1" ja "testi2"). Admin ominaisuuksia pääset testaamaan käyttäjä salasana parilla admin-admin1.
