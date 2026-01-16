# Društvena Kuharica (TBP Projekt)

Ovaj projekt predstavlja web aplikaciju za preporuku recepata temeljenu na graf bazi podataka **Neo4j**. 
Aplikacija koristi hibridni sustav preporuka (Social & Content-based filtering).


## Tehnologije
- **Baza podataka:** Neo4j (Graph Database)
- **Backend:** Python + Flask
- **Frontend:** HTML5, Bootstrap 5, Jinja2

## Instalacija i pokretanje
1. **Preduvjeti:** Instaliran Python 3.x i Neo4j (Desktop ili Docker).
2. **Biblioteke:** Instalirajte potrebne pakete naredbom:
   `pip install flask neo4j`
3. **Baza podataka:** - Provjerite je li Neo4j pokrenut.
   - U datoteci `setup_db.py` prilagodite lozinku baze.
   - Pokrenite instalacijsku skriptu: `python setup_db.py`
4. **Pokretanje aplikacije:**
   - Pokrenite `python app.py`
   - Otvorite `http://127.0.0.1:5000` u pregledniku.

## Autor
Domagoj Lovosević
Fakultet organizacije i informatike, Varaždin

## Licenca
Ovaj projekt je licenciran pod GPLv3 licencom.
