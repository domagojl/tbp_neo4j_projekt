from flask import Flask, render_template, request, redirect, url_for
from neo4j import GraphDatabase

app = Flask(__name__)

# --- POSTAVKE BAZE ---
# Prilagodi URI i lozinku svojim postavkama u Neo4j Desktopu/Dockeru
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "lozinka123"))

def get_db():
    return driver.session()

# --- RUTAMA UPRAVLJA DOMAGOJ (Hardkodirani aktivni korisnik za demo) ---
MOJE_IME = "Domagoj"

@app.route('/')
def index():
    with get_db() as session:
        # 1. Svi recepti za glavni popis
        svi_result = session.run("MATCH (r:Recept) RETURN r.naslov AS naslov, r.vrijeme AS vrijeme, r.tezina AS tezina, r.kuhinja AS kuhinja")
        svi_recepti = [record for record in svi_result]

        # 2. Naslovi koje je korisnik lajkao (zbog boje srca)
        lajkovi_result = session.run("MATCH (:Korisnik {ime: $ime})-[:VOLI]->(r:Recept) RETURN r.naslov AS naslov", ime=MOJE_IME)
        lajkani_naslovi = [record['naslov'] for record in lajkovi_result]

        # 3. Ljudi koje pratim (za kartice profila na vrhu)
        ljudi_query = """
        MATCH (me:Korisnik {ime: $ime})-[:PRATI]->(p:Korisnik)
        OPTIONAL MATCH (p)-[:VOLI]->(r:Recept)
        RETURN p.ime AS ime, count(r) AS broj_recepta
        """
        ljudi_koje_pratim = [record for record in session.run(ljudi_query, ime=MOJE_IME)]

        # 4. Otkrij nove ljude (Discovery) - ISPRAVLJENO
        otkrij_query = """
        MATCH (me:Korisnik {ime: $ime}), (ostali:Korisnik)
        WHERE ostali.ime <> $ime AND NOT (me)-[:PRATI]->(ostali)
        RETURN ostali.ime AS ime LIMIT 6
        """
        prijedlozi_za_pracenje = [record for record in session.run(otkrij_query, ime=MOJE_IME)]

        # 5. Social Preporuke - ISPRAVLJENO (isto dodan 'me' u MATCH)
        social_query = """
        MATCH (me:Korisnik {ime: $ime})-[:PRATI]->(prijatelj)-[:VOLI]->(recept:Recept)
        WHERE NOT (me)-[:VOLI]->(recept)
        RETURN recept.naslov AS naslov, collect(DISTINCT prijatelj.ime) AS imena_prijatelja
        LIMIT 4
        """
        prep_prijatelji = [record for record in session.run(social_query, ime=MOJE_IME)]

        # 6. Content Preporuke (Recepti sa sličnim sastojcima kao oni koje volim)
        content_query = """
        MATCH (me:Korisnik {ime: $ime})-[:VOLI]->(lajkano:Recept)-[:SADRŽI]->(s:Sastojak)<-[:SADRŽI]-(preporuka:Recept)
        WHERE NOT (me)-[:VOLI]->(preporuka) AND lajkano <> preporuka
        RETURN DISTINCT preporuka.naslov AS naslov, collect(DISTINCT s.naziv)[0] AS jedan_sastojak
        LIMIT 5
        """
        prep_sastojci = [record for record in session.run(content_query, ime=MOJE_IME)]

    return render_template('index.html', 
                           recepti=svi_recepti, 
                           lajkani_naslovi=lajkani_naslovi,
                           ljudi_koje_pratim=ljudi_koje_pratim,
                           prijedlozi_za_pracenje=prijedlozi_za_pracenje,
                           prep_prijatelji=prep_prijatelji, 
                           prep_sastojci=prep_sastojci, 
                           ime=MOJE_IME)

@app.route('/recept/<naslov>')
def recept_detalji(naslov):
    with get_db() as session:
        # Podaci o receptu i sastojci
        recept_data = session.run("""
            MATCH (r:Recept {naslov: $naslov})
            OPTIONAL MATCH (r)-[rel:SADRŽI]->(s:Sastojak)
            RETURN r.naslov AS naslov, r.opis AS opis, r.vrijeme AS vrijeme, 
                   r.tezina AS tezina, r.kuhinja AS kuhinja, r.postupak AS postupak,
                   collect({naziv: s.naziv, kolicina: rel.kolicina}) AS sastojci
        """, naslov=naslov).single()

        # Tko od mojih prijatelja voli ovaj recept
        social_data = session.run("""
            MATCH (me:Korisnik {ime: $ime})-[:PRATI]->(prijatelj)-[:VOLI]->(r:Recept {naslov: $naslov})
            RETURN collect(prijatelj.ime) AS imena_prijatelja
        """, ime=MOJE_IME, naslov=naslov).single()
        imena_prijatelja = social_data['imena_prijatelja'] if social_data else []

        # Provjera je li recept već lajkan
        je_lajkan = session.run("""
            MATCH (k:Korisnik {ime: $ime})-[:VOLI]->(r:Recept {naslov: $naslov})
            RETURN count(r) > 0 AS status
        """, ime=MOJE_IME, naslov=naslov).single()['status']

    return render_template('recept_detalji.html', r=recept_data, imena_prijatelja=imena_prijatelja, je_lajkan=je_lajkan)

@app.route('/profil/<ime>')
def profil(ime):
    with get_db() as session:
        # Podaci o profilu, pratitelji i praćenja
        stats = session.run("""
            MATCH (u:Korisnik {ime: $ime})
            OPTIONAL MATCH (p_od:Korisnik)-[:PRATI]->(u)
            OPTIONAL MATCH (u)-[:PRATI]->(p_koje_on:Korisnik)
            RETURN u.ime AS ime, 
                   collect(DISTINCT p_od.ime) AS imena_pratitelja, 
                   collect(DISTINCT p_koje_on.ime) AS imena_koje_prati
        """, ime=ime).single()
        
        # Recepti koje taj korisnik voli
        recepti = list(session.run("""
            MATCH (u:Korisnik {ime: $ime})-[:VOLI]->(r:Recept) 
            RETURN r.naslov AS naslov, r.kuhinja AS kuhinja
        """, ime=ime))
        
        # Provjera prati li ga Domagoj
        pratim = session.run("""
            MATCH (me:Korisnik {ime: $me})-[:PRATI]->(target:Korisnik {ime: $ime}) 
            RETURN count(target) > 0 AS status
        """, me=MOJE_IME, ime=ime).single()['status']

    return render_template('profil.html', stats=stats, recepti=recepti, pratim=pratim, moje_ime=MOJE_IME)

@app.route('/lajkaj/<naslov>')
def lajkaj(naslov):
    with get_db() as session:
        session.run("""
            MATCH (k:Korisnik {ime: $ime}), (r:Recept {naslov: $naslov})
            OPTIONAL MATCH (k)-[rel:VOLI]->(r)
            FOREACH (ignore IN CASE WHEN rel IS NOT NULL THEN [1] ELSE [] END | DELETE rel)
            FOREACH (ignore IN CASE WHEN rel IS NULL THEN [1] ELSE [] END | CREATE (k)-[:VOLI]->(r))
        """, ime=MOJE_IME, naslov=naslov)
    return redirect(request.referrer or url_for('index'))

@app.route('/zaprati/<ime>')
def zaprati(ime):
    with get_db() as session:
        session.run("MATCH (me:Korisnik {ime: $me}), (t:Korisnik {ime: $target}) MERGE (me)-[:PRATI]->(t)", 
                    me=MOJE_IME, target=ime)
    return redirect(request.referrer or url_for('index'))

@app.route('/otprati/<ime>')
def otprati(ime):
    with get_db() as session:
        session.run("MATCH (:Korisnik {ime: $me})-[r:PRATI]->(:Korisnik {ime: $target}) DELETE r", 
                    me=MOJE_IME, target=ime)
    return redirect(request.referrer or url_for('index'))

@app.route('/trazi', methods=['POST'])
def trazi():
    pojam = request.form.get('sastojak').strip().lower()
    query = """
    MATCH (r:Recept) WHERE toLower(r.naslov) CONTAINS $pojam
    RETURN DISTINCT r.naslov AS naslov, r.vrijeme AS vrijeme, r.tezina AS tezina
    UNION
    MATCH (r:Recept)-[:SADRŽI]->(s:Sastojak) WHERE toLower(s.naziv) CONTAINS $pojam
    RETURN DISTINCT r.naslov AS naslov, r.vrijeme AS vrijeme, r.tezina AS tezina
    """
    with get_db() as session:
        rezultati = [record for record in session.run(query, pojam=pojam)]
    return render_template('rezultati.html', rezultati=rezultati, sastojak=pojam)

if __name__ == '__main__':
    app.run(debug=True)