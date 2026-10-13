# TaskFlow — dépôt fil rouge CI/CD

TaskFlow est une petite API de gestion de tâches écrite en Python avec FastAPI.
C'est le projet fil rouge du module CI/CD (Mastère DevOps M1, Sup de Vinci) :
pendant trois jours, vous allez construire autour d'elle un pipeline complet
qui teste, construit, sécurise et livre l'application.

## Lancer l'API en local

Prérequis : Python 3.10 ou plus récent.

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

L'API répond sur http://localhost:8000 et sa documentation interactive est sur
http://localhost:8000/docs.

## Vérifier le code

```bash
pytest           # tests automatiques
ruff check .     # lint
ruff format .    # mise en forme
```

## Lancer avec Docker

```bash
docker build -t taskflow .
docker run --rm -p 8000:8000 taskflow
```

## Endpoints

| Méthode | Chemin                | Rôle                                              |
| ------- | --------------------- | ------------------------------------------------- |
| GET     | `/health`             | État de l'API et version                          |
| GET     | `/tasks`              | Liste des tâches                                  |
| GET     | `/tasks/search?q=...` | Recherche dans les titres                         |
| POST    | `/tasks`              | Crée une tâche (`{"title": "..."}`)               |
| GET     | `/tasks/{id}`         | Détail d'une tâche                                |
| PATCH   | `/tasks/{id}/done`    | Marque une tâche comme faite                      |
| DELETE  | `/tasks/{id}`         | Supprime une tâche (en-tête `X-API-Token` requis) |

## Configuration

| Variable             | Rôle                                      | Défaut                        |
| -------------------- | ----------------------------------------- | ----------------------------- |
| `APP_VERSION`        | Version affichée par `/health`            | `0.1.0`                       |
| `DB_PATH`            | Fichier SQLite                            | `taskflow.db`                 |
| `API_TOKEN`          | Jeton exigé pour supprimer une tâche      | vide (suppression désactivée) |
| `NOTIFY_WEBHOOK_URL` | Webhook appelé à chaque création de tâche | vide (désactivé)              |

## Équipe

<!-- Lab J1 : remplacez par les noms du binôme -->

- Nicolas, Rayen

## Gouvernance du dépôt

<!-- Lab J1 : listez les règles activées sur main, pourquoi chacune, et ajoutez la capture du push refusé -->

Voici la liste des règles activées sur la branche main d'après ton exercice GitHub :

1. Require a pull request before merging : obliger à passer par une Pull Request (PR) pour fusionner du code dans main.
2. Require status checks to pass : obliger les vérifications automatiques à réussir avant la fusion :
   - ✅ lint : vérifie la qualité du code avec Ruff.
   - ✅ test : exécute les tests avec pytest.
3. Require a pull request review : demander l'approbation d'un autre contributeur (ton binôme) avant la fusion.

Résultat attendu : la fusion dans main est bloquée si les tests échouent, si le lint échoue ou si l'approbation obligatoire manque.

LAB 1 :

1. Forker le dépôt (public), cloner, inviter son binöme
2. Ruleset sur main: PR, 1 approbation, ni force push ni suppression
3. Tenter un push direct sur main et capturer le refus
   ![Refus](<captures/Capture d’écran 2026-10-13 à 12.16.45.png>)
   ![Refus 2](<captures/Capture d’écran 2026-10-13 à 12.17.20.png>)
   Refus capturé car le push est tenté sur main mais empêcher par le rulset
4. Branche feat/readme-equipe, PR approvée par le binôme, merge
   ![Merge en attente](<captures/Capture d’écran 2026-10-13 à 12.22.28.png>)
   Merge en attente de validation
   ![Merge validé par le binome](<captures/Capture d’écran 2026-10-13 à 12.31.33.png>)
   Merge validé par le binome
5. CODEOWNERS sur github/workflows/ + « Require review from Code
   Owners »
   ![Ajout du Ruleset](<captures/Capture d’écran 2026-10-13 à 14.41.22.png>)
   Ajout du Ruleset code owners

Bonus: signer ses commits avec sa clé SSH
![Commit avec SSH](<captures/Capture d’écran 2026-10-13 à 14.44.05.png>)
Commit avec l'ajout d'un SSH dédié

1. Activer GitHub Actions sur votre fork (onglet Actions)
   Projet récupérer ajout des membres de l'équipe

2. Branche feat/ci : .github/workflows/ci.yml avec deux jobs en parallèle, lint (ruff) et test (pytest)

3. PR, checks verts, approbation du binôme, merge
   ![Erreur test](<captures/Capture d’écran 2026-10-13 à 15.15.41.png>)
   ![Ajout test et lint](<captures/Capture d’écran 2026-10-13 à 15.15.38.png>)
   ![Validation de la MR](<captures/Capture d’écran 2026-10-13 à 15.20.23.png>)
   Ajout des jobs test et lint
   Erreur dans le job test mais on peut quand même validé la merge request

4. Ruleset : Require status checks → lint et test

5. Branche fix/casse-test : cassez un test, capturez le merge bloqué

![Merge bloqué](<captures/Capture d’écran 2026-10-13 à 15.39.20.png>)
La marge est bloqué et il est impossible de l'outre-passé

Lab 3 :

1. Branche feat/ci-rapide : cache pip, matrice 3.11 / 3.12 / 3.13, rapport de tests en artefact, concurrency

![Résolution des conflits](<captures/Image 13-10-2026 à 16.28.png>)
Résolution des conflits

2. Ouvrez la PR. Tout est vert... pourquoi est-elle bloquée ?

![Pipeline bloqué](<captures/Image 13-10-2026 à 16.39.png>)
La pipeline est bloqué car le "status checks" de **test** est toujours requis

![test toujours la](<captures/Capture d’écran 2026-10-13 à 16.40.53.png>)

3. Corrigez avec un job « CI OK », seul check obligatoire

![Remplacement par CI OK](<captures/Capture d’écran 2026-10-13 à 16.42.58.png>)

![Merge validé](<captures/Capture d’écran 2026-10-13 à 16.43.00.png>)

Apres le changement de test à CI OK la merge a été validé

4. Comparez la durée d'installation avec et sans cache

![Github action](<captures/Capture d’écran 2026-10-13 à 17.02.49.png>)
La durée du pipeline augmente après l'optimisation ?

5. Téléchargez l'artefact du run
6. Bonus : badge de statut dans le README
