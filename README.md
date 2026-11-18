# Bullet-Journal-Python

Ce projet consiste à développer une bibliothèque Python fiable et réutilisable
permettant de gérer l'organisation personnelle selon la méthode du Bullet
Journal (BuJo), créée par Ryder Carroll.

## Architecture du projet

```
Bullet-Journal-PY/
├── bujo/                         # package principal de la bibliothèque
│   ├── __init__.py               # API publique : exports, __version__, recettes d'usage
│   ├── __main__.py               # point d'entrée : python -m bujo
│   ├── entry.py                  # modèle (abstraction, héritage) : Entry, Task, Event,
│   │                             #   Note, TaskState, ALLOWED_TRANSITIONS, SYMBOLS_BY_STATE
│   ├── journal.py                # journal : Journal (entrées indexées par id) + setup_logging
│   ├── exceptions.py             # exceptions : BujoError, EntryNotFoundError, EmptyNameError,
│   │                             #   InvalidDateError, InvalidStateTransitionError
│   └── cli.py                    # affichage / CLI : main(), MENU, show_choice(),
│                                 #   take_choice(), clear_screen()
├── tests/                        # tests unitaires pytest
│   ├── test_entry.py             # cycle de vie des tâches, cas d'erreur du modèle
│   └── test_journal.py           # ajout, suppression, recherche, entrées du jour
├── docs/                         # documentation Sphinx (autodoc des modules)
│   ├── conf.py                   # configuration Sphinx (autodoc, napoleon, langue fr)
│   ├── index.rst                 # page d'accueil : autodoc de tous les modules
│   ├── _static/                  # ressources statiques (répertoire réservé)
│   ├── _templates/               # templates de thèmes (répertoire réservé)
│   └── _build/                   # HTML généré (ignoré par Git)
├── .gitlab-ci.yml                # pipeline CI : flake8, pydocstyle, pytest
├── setup.cfg                     # configuration de flake8, pydocstyle et pytest
├── Dockerfile                    # image Docker de l'application
├── requirements.txt              # dépendances (tests, lint, couverture, docs)
└── .gitignore                    # caches, logs, documentation générée, docx hors dépôt
```

Les modules attendus par le cahier des charges sont ainsi répartis : modèle
(`entry.py`), journal (`journal.py`), affichage (`cli.py`), exceptions
(`exceptions.py`). La persistance n'est pas encore implémentée : le journal
vit en mémoire (voir la to-do).

## Installation et utilisation

Le projet s'utilise avec Docker (l'image `python:3.12-slim` fournit Python
et les dépendances de `requirements.txt`) :

```bash
docker build -t bujo .
docker run --rm -it bujo
```

Le menu permet d'ajouter une tâche, un événement ou une note, de marquer une
tâche comme terminée, de supprimer une entrée et d'afficher les tâches en
cours. Les identifiants (uuid) peuvent être saisis partiellement (préfixe).

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

### En bibliothèque

```python
from datetime import time

from bujo import Event, Journal, Note

journal = Journal("Mon journal")
task = journal.add_task("Ranger le bureau", "Trier les papiers")
journal.add_entry(Event("Réunion", at=time(10, 30)))
journal.add_entry(Note("Idée de projet"))
journal.complete_task(task.id)
print(*journal.open_tasks(), sep="\n")
```

## Documentation

Générer la documentation HTML avec Sphinx (autodoc de tous les modules) :

```bash
docker run --rm -v "$PWD":/app bujo \
  sphinx-build -b html docs docs/_build/html
```

Puis ouvrir `docs/_build/html/index.html`.

## Tests

```bash
docker run --rm bujo python -m pytest -v
```

32 tests unitaires couvrent le modèle des entrées (`tests/test_entry.py`) et
le journal (`tests/test_journal.py`) : cycle de vie des tâches, transitions
interdites, cas d'erreur, recherche par nom.

## Journalisation (logging)

Chaque exécution alimente deux fichiers de log créés dans le répertoire
courant (ignorés par Git via `.gitignore`) :

- `bujo_debug.log` : toutes les actions (DEBUG et plus)
- `bujo_error.log` : uniquement les erreurs (ERROR et CRITICAL)

## CI/CD

Le pipeline GitLab CI (`.gitlab-ci.yml`, exécuté à chaque push) vérifie :

1. le respect de PEP 8 (`flake8`) ;
2. la présence des docstrings (`pydocstyle`) ;
3. l'exécution de tous les tests unitaires (`pytest`).

La configuration des outils (flake8, pydocstyle, pytest) est centralisée dans
`setup.cfg`.

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
- ✅ Environnement reproductible (Docker + requirements.txt)

## Perspective d'amélioration

Toutes les fonctionnalités du niveau 1 et la plupart des exigences
techniques sont livrées (voir le statut ci-dessus). Il reste :

### Fonctionnalités
1. **Persistance** : module de sauvegarde / chargement du journal —
   aujourd'hui les entrées vivent en mémoire et sont perdues à la fin
   du programme
2. Compléter le CLI avec les transitions encore réservées à la
   bibliothèque : migrer, planifier et abandonner une tâche
3. Mesurer la **couverture de tests** (`coverage`, déjà présent dans
   `requirements.txt`) et l'intégrer au pipeline CI

### Exigences techniques
1. Workflow Git avec **branches et Merge Requests** (les commits
   explicites sur la branche principale sont déjà en place)

### Livrable :
Dépôt GitLab du projet (code source, documentation Sphinx, fichiers de
logs, tests unitaires, pipeline CI).
