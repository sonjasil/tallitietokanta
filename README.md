# Tallitietokanta
Kurssin Tietokantasovellus harjoitustyö

Sovellus on tarkoitettu ratsastuskoulujen käyttöön. Käyttäjät ovat joko oppilaita, opettajia tai ylläpitäjiä. Sovelluksessa voidaan järjestää tuntien toimintaa ja tallentaa tietoa yksittäisistä hevosista.

Ominaisuuksia:
- Sovellukseen kirjaudutaan sisään (tehty)
- Ylläpitäjä voi lisätä tunteja, joilla on taso, hinta, paikkojen määrä ja ajankohta (tehty)
- Opettaja voi lisätä asiakkaan tunnille ja jakaa tälle hevosen (tehty)
- Ylläpitäjä voi lisätä talliin hevosia ja hevosille tietoja (syntymäaika, ruokintamäärä, maksimituntien määrä päivässä) (tehty)
- Ylläpitäjä voi poistaa hevosia (tehty)
- Ylläpitäjä voi suodattaa hevosia rehun mukaan ja laskea yhteisen rehumäärän (tehty)
- Asiakas voi lisätä itsensä tunnille ja näkee omat tuntinsa (tehty)
- Asiakas näkee tilastoja omista tunneistaan (tehty)

Sovellus ei ole saatavilla Fly.io:ssa. 

Käynnistysohje paikallisesti (Linux):
- Sovellus vaati PostgreSQL:n asennuksen erikseen
- Tietokannan tulee olla käynnissä toisessa terminaalissa, jotta sovellus toimii. Jos PostgreSQL on asennettu kurssin ohjeen mukaan, tietokannan saa käyntiin komennolla:
  - start-pg.sh
- Lataa repositorio koneellesi
- Luo repositorion juurihakemistoon tiedosto .env ja aseta sen sisällöksi
    - DATABASE_URL=postgresql+psycopg2:///tietokannan-paikallinen-osoite
    - SECRET_KEY=salainen-avain
- Aktivoi virtuaaliympäristö komennoilla:
  - python3 -m venv venv
  - source venv/bin/activate
- Asenna seuraavalla komennolla riippuvuudet virtuaaliympäristössä:
  - pip install -r requirements.txt
- Määritä sovelluksen skeema komennolla psql < schema.sql
- Sovelluksen saa käyntiin komennolla flask run

- Sovellukseen luodaan valmiiksi ylläpitäjäkäyttäjä:
    - Käyttäjänimi: admin_user
    - Salasana: admin1234