# Bullet-Journal-Python
Ce projet consiste à développer une bibliothèque Python fiable et réutilisable permettant de gérer l'organisation personnelle selon la méthode du Bullet Journal (BuJo), créée par Ryder Carroll.   
--

## Architecture du projet

```
Bullet-Journal-PY/
  bujo/                  # package principal de la bibliothèque
    __init__.py          # API publique : exports des classes et exceptions, __version__
    __main__.py          # point d'entrée : python -m bujo
    entry.py             # modèle des entrées : Entry (classe abstraite), Task, Event, Note, TaskState
    journal.py           # organisation du journal : Journal (entrées indexées par id), setup_logging
    exceptions.py        # exceptions personnalisées : BujoError, EntryNotFoundError, EmptyNameError,
                         #   InvalidDateError, InvalidStateTransitionError
    cli.py               # interface en ligne de commande : main(), show_choice(), take_choice()
                         #   et affichage des logs avec les symboles du rapid logging
  tests/                 # tests unitaires pytest
  docs/                  # documentation Sphinx (autodoc des modules)
  requirements.txt       # dépendances (environnement Anaconda)
```

## Installation

Avec Anaconda (ou tout autre gestionnaire d'environnement) :

```bash
conda create -n bujo python=3.12
conda activate bujo
pip install -r requirements.txt
```

### Symboles du rapid logging (utilisés par l'affichage CLI)

| Symbole | Signification |
|---|---|
| • | Tâche à faire |
| × | Tâche terminée |
| > | Tâche migrée (reportée à un autre jour ou mois) |
| < | Tâche planifiée dans le Future Log |
| ~~tâche~~ | Tâche abandonnée, devenue sans objet |
| ○ | Événement |
| – | Note |
| * | Signifiant : priorité |
| ! | Signifiant : idée, inspiration |

### Utilisation

```bash
python -m bujo
```

### Avec Docker

```bash
docker build -t bujo .
docker run --rm -it bujo
```

L'image est basée sur `python:3.12-slim` : c'est elle qui fournit Python
(Python n'est pas une dépendance pip et ne figure donc pas dans `requirements.txt`).

## Documentation

Générer la documentation HTML avec Sphinx (autodoc de tous les modules) :

```bash
sphinx-build -b html docs docs/_build/html
```

Puis ouvrir `docs/_build/html/index.html`.

## Journalisation (logging)

Chaque exécution alimente deux fichiers inclus dans le dépôt :

- `bujo_debug.log` : toutes les actions (DEBUG et plus)
- `bujo_error.log` : uniquement les erreurs (ERROR et CRITICAL)

## CI/CD

Le pipeline (`.gitlab-ci.yml`, exécuté à chaque push) vérifie :

1. le respect de PEP 8 (`flake8`) ;
2. la présence des docstrings (`pydocstyle`) ;
3. l'exécution de tous les tests unitaires (`pytest`).

Un workflow GitHub Actions équivalent (`.github/workflows/ci.yml`) est
fourni si le dépôt est répliqué sur GitHub.

## Statut — Niveau 1 (socle obligatoire)

- ✅ Ajouter une tâche (nom + description) dans le journal du jour
- ✅ Marquer une tâche comme terminée
- ✅ Supprimer une entrée
- ✅ Afficher les tâches en cours (symboles du rapid logging)
- ✅ Cycle de vie : à faire, terminée, migrée, planifiée, abandonnée
- ✅ Trois types d'entrées : tâches, événements (date/heure), notes
- ✅ Identifiant unique par entrée, recherche par nom secondaire
- ✅ POO : classe abstraite `Entry`, héritage, encapsulation
- ✅ Type hinting, PEP 8, docstrings sur modules/classes/méthodes
- ✅ Exceptions personnalisées (introuvable, nom vide, date invalide,
  transition d'état interdite)
- ✅ Logs debug + erreurs dédiés
- ✅ Tests pytest (cycle de vie, cas d'erreur)
- ✅ Documentation Sphinx
- ✅ Pipeline CI à chaque push

## To-do 
### Fonctionnalités
1. Bibliothèque Python de Bullet Journal permettant d'**ajouter une tâche** au journal du jour (nom + description minimum), la **marquer terminée**, la **supprimer**, et **afficher les tâches en cours**
2. **Cycle de vie des tâches** : à faire, terminée, migrée, planifiée, abandonnée
3. **Trois types d'entrées** : tâches, événements (date/heure), notes
4. **Identifiant unique** par entrée (le nom n'est qu'une recherche secondaire)

### Exigences techniques
1. Structure en packages/modules (modèle, journal, persistance, affichage, exceptions), README.md
2. Environnement Anaconda + requirements.txt
3. Git avec commits explicites, branches et Merge Requests
4. POO : classe abstraite d'entrée + classes dérivées + classe Journal, encapsulation/héritage
5. Type hinting, PEP 8, exceptions personnalisées (entrée introuvable, nom vide, transition d'état interdite…)
6. Module logging : fichier de debug + fichier dédié aux erreurs
7. Tests unitaires pytest approfondis (cycle de vie, migration, cas d'erreur)
8. Docstrings + commentaires, documentation (Sphinx possible)
9. Pipeline CI à chaque push : PEP 8, vérification des docstrings, tests

### Livrable :
Dépôt GitLab du projet (code source, documentation Sphinx, fichiers de
logs, tests unitaires, pipeline CI).