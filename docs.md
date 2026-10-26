# Structure et configuration

- Création d'un environnement pour le projet

- Création
```bash
python -m venv .venv
```

- Activation de l'environnement virtuel
```bash
.venv\Scripts\Activate.ps1
```

- Désactivation de l'environnement virtuel
```bash
deactivate
```

### Configuration de psycopg

- Configuration pour la communication avec la db

1. Installer les dépendances (listées dans `requirements.txt`)
```bash
pip install -r requirements.txt
```
- `psycopg[binary]` : le driver PostgreSQL (la version binaire évite d'installer libpq à la main)
- `python-dotenv` : charge les variables du fichier `.env`

2. Créer un fichier `.env` à la racine avec les infos de connexion
```env
DB_NAME=nom_de_la_base
DB_USER=utilisateur
DB_PASSWORD=mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```
> Ne jamais commit le `.env` : l'ajouter au `.gitignore`.

3. Créer la table `users` dans PostgreSQL
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    last_name VARCHAR(100),
    role VARCHAR(50)
);
```

## Implémentation

### Structure du projet
```
demo-psycopg/
├── .env
├── requirements.txt
├── main.py                        # menu console
├── db/
│   └── db.py                      # connexion à la db
└── repository/
    └── users_repository.py        # requêtes SQL (CRUD)
```

### 1. La connexion : `db/db.py`
- `load_dotenv()` charge le `.env`, puis `os.getenv(...)` lit chaque variable
- `get_connection()` retourne une connexion via `psycopg.connect(...)`
- `autocommit=True` : chaque requête est validée directement, pas besoin de `conn.commit()`

```python
def get_connection():
    return psycopg.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        autocommit=True
    )
```

### 2. Le repository : `repository/users_repository.py`
Chaque fonction reçoit la connexion, ouvre un curseur avec `with conn.cursor() as cursor:` (fermé automatiquement), exécute la requête et renvoie le résultat.

| Fonction | Requête | Retour |
|---|---|---|
| `get_all_users(conn)` | `SELECT * FROM users` | liste de tuples (`fetchall()`) |
| `get_user_by_id(conn, id)` | `SELECT ... WHERE id = %s` | un tuple ou `None` (`fetchone()`) |
| `create_user(conn, email, lastname, role)` | `INSERT ... RETURNING id` | l'id créé |
| `update_user(conn, email, lastname, id)` | `UPDATE ... WHERE id = %s` | nombre de lignes (`rowcount`) |
| `delete_user(conn, id)` | `DELETE ... WHERE id = %s` | nombre de lignes (`rowcount`) |

- Requêtes paramétrées : on utilise `%s` et on passe les valeurs dans un tuple → protège contre l'injection SQL
```python
cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
```
> Attention : `(id,)` avec la virgule, sinon ce n'est pas un tuple.
- Ne jamais construire la requête avec une f-string (`f"... WHERE id = {id}"`)
- `RETURNING id` permet de récupérer l'id généré par PostgreSQL lors de l'`INSERT`

### 3. Le menu : `main.py`
- `with get_connection() as conn:` ouvre la connexion une seule fois et la ferme à la sortie
- Une boucle `while` affiche le menu, `match choice:` appelle la bonne fonction du repository
- Le choix `6` passe `continue_app` à `False` pour quitter

## Lancer la démo

1. Démarrer PostgreSQL et vérifier que la table `users` existe
2. Activer l'environnement virtuel
```bash
.venv\Scripts\Activate.ps1
```
3. Lancer l'application
```bash
python main.py
```
4. Scénario de démo :
   - `3` créer un utilisateur → affiche l'id créé
   - `1` lister les utilisateurs → le nouvel utilisateur apparaît
   - `2` chercher par id
   - `4` modifier l'email / le nom → affiche le nombre de lignes modifiées
   - `5` supprimer → affiche le nombre de lignes supprimées
   - `6` quitter
