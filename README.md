# Tallitietokanta
Kurssin Tietokantasovellus harjoitustyö

Sovellus on tarkoitettu ratsastuskoulujen käyttöön. Käyttäjät ovat joko oppilaita, opettajia tai ylläpitäjiä. Sovelluksessa voidaan järjestää tuntien toimintaa ja tallentaa tietoa yksittäisistä hevosista.

Ominaisuuksia:
- Sovellukseen kirjaudutaan sisään
- Ylläpitäjä voi lisätä tunteja, joilla on taso, hinta ja paikkojen määrä
- Opettaja voi lisätä asiakkaan tunnille ja jakaa tälle hevosen
- Ylläpitäjä voi lisätä talliin hevosia ja hevosille tietoja (syntymäaika, ruokintamäärä, maksimituntien määrä päivässä)
- Ylläpitäjä voi hakea hevosia tiettyjen kriteerien perusteella ja laskea esim. yhteisen ruokintamäärän
- Asiakas voi lisätä itsensä tunnille ja näkee omat tuntinsa 
- Asiakas voi hakea tilastoja omista tunneistaan
- Talleja voi olla useita

Toteutetut toiminnot:
- Ylläpitäjän on mahdollista lisätä tunteja ja hevosia listoihin ja tarkastella listoja
- Opettaja voi tarkastella tunti- ja hevoslistoja

Sovellus ei ole saatavilla Fly.io:ssa. 

Käynnistysohje paikallisesti (Linux):
- Sovellus vaati PostgreSQL:n asennuksen erikseen
- Tietokannan tulee olla käynnissä toisessa terminaalissa, jotta sovellus toimii. Jos PostgreSQL on asennettu kurssin ohjeen mukaan, tietokannan saa käyntiin komennolla:
  - start-pg.sh
- Lataa repositorio koneellesi
- Luo repositorion juurihakemistoon tiedosto .env ja aseta sen sisällöksi DATABASE_URL=postgresql+psycopg2:///tietokannan-paikallinen-osoite
- Aktivoi virtuaaliympäristö komennoilla:
  - python3 -m venv venv
  - source venv/bin/activate
- Asenna seuraavalla komennolla riippuvuudet virtuaaliympäristössä:
  - pip install -r requirements.txt
- Määritä sovelluksen skeema komennolla psql < schema.sql
- Sovelluksen saa käyntiin komennolla flask run
