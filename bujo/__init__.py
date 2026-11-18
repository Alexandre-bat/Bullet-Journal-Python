"""Bullet Journal — bibliothèque Python de gestion d'un journal personnel.

Ce module est la façade du package : tout ce qui sert au quotidien
s'importe directement depuis ``bujo``, sans avoir à connaître les
sous-modules ``entry``, ``journal``, ``exceptions`` et ``cli``.

Recettes d'utilisation
----------------------
1. Créer le journal : ``journal = Journal("Mon journal")``.
2. Ajouter des entrées : ``journal.add_task("Faire les courses")`` pour
   une tâche, ou ``journal.add_entry(Event("Rendez-vous"))`` et
   ``journal.add_entry(Note("Idée"))`` pour les autres types.
3. Faire avancer une tâche : ``journal.complete_task(entry_id)`` depuis
   son identifiant, ou ``task.migrate()``, ``task.plan()`` et
   ``task.discard()`` directement sur l'objet.
4. Relire le journal : ``journal.open_tasks()`` pour ce qui reste à
   faire, ``journal.entries_of_day(date.today())`` pour le log d'un
   jour, ``journal.search_by_name("courses")`` pour une recherche,
   ``journal.get_entry(entry_id)`` et ``journal.remove_entry(id)`` pour
   retrouver ou retirer une entrée, ``len(journal)`` et
   ``journal.ids()`` pour l'inventaire.
5. Afficher une entrée : ``print(entry)`` affiche le symbole du rapid
   logging suivi du nom ; ``entry.symbol`` donne seul ce symbole.
6. Logger l'exécution : ``setup_logging()`` écrit un log complet et un
   log d'erreurs dans des fichiers.
7. Jouer avec le menu : ``main()`` lance le programme interactif, ce
   que fait déjà ``python -m bujo``.
8. Gérer les erreurs : intercepter ``BujoError`` (ou une de ses
   sous-classes) autour des appels qui manipulent le journal.

Entrées et états (``bujo.entry``)
---------------------------------
- ``Entry`` : classe abstraite de base, ancêtre des trois types ; elle
  porte l'identifiant uuid, le nom validé, la description, la date de
  création et la date du log. On ne l'instancie jamais directement.
- ``Task`` : tâche à faire, avec un cycle de vie (``state``) et quatre
  transitions. C'est le type le plus utilisé du journal.
- ``Event`` : événement daté, avec une heure facultative (``at``).
- ``Note`` : information sans date ni état.
- ``TaskState`` : énumération des cinq états possibles d'une tâche
  (``TODO``, ``DONE``, ``MIGRATED``, ``PLANNED``, ``DISCARDED``).
- ``ALLOWED_TRANSITIONS`` : table des transitions autorisées, consultée
  par ``Task`` pour refuser un passage d'état illogique.
- ``SYMBOLS_BY_STATE`` : correspondance entre un état et son symbole
  rapid logging (``•``, ``×``, ``>``, ``<``, ``~``).

Organisation (``bujo.journal``)
-------------------------------
- ``Journal`` : conteneur des entrées, indexées par identifiant.
- ``setup_logging`` : configuration des deux fichiers de log.

Exceptions (``bujo.exceptions``)
--------------------------------
- ``BujoError`` : erreur mère, à attraper pour tout intercepter.
- ``EntryNotFoundError`` : identifiant inconnu du journal.
- ``EmptyNameError`` : nom d'entrée vide ou uniquement espacé.
- ``InvalidDateError`` : date, datetime ou heure de mauvais type.
- ``InvalidStateTransitionError`` : changement d'état interdit, ou
  opération réservée aux tâches demandée sur un autre type.

Menu (``bujo.cli``)
-------------------
- ``main`` : point d'entrée qui initialise les logs puis boucle.
- ``MENU`` : texte du menu affiché à l'utilisateur.
- ``show_choice`` : affiche ``MENU``.
- ``take_choice`` : lit un choix et exécute l'action demandée.
- ``clear_screen`` : vide le terminal entre deux écrans.
"""

from bujo.entry import (
    ALLOWED_TRANSITIONS,
    SYMBOLS_BY_STATE,
    Entry,
    Event,
    Note,
    Task,
    TaskState,
)
from bujo.exceptions import (
    BujoError,
    EmptyNameError,
    EntryNotFoundError,
    InvalidDateError,
    InvalidStateTransitionError,
)
from bujo.journal import Journal, setup_logging
from bujo.cli import MENU, clear_screen, main, show_choice, take_choice

__version__ = "0.1.0"

__all__ = [
    # Entrées et états
    "Entry",
    "Task",
    "Event",
    "Note",
    "TaskState",
    "ALLOWED_TRANSITIONS",
    "SYMBOLS_BY_STATE",
    # Organisation du journal
    "Journal",
    "setup_logging",
    # Exceptions
    "BujoError",
    "EntryNotFoundError",
    "EmptyNameError",
    "InvalidDateError",
    "InvalidStateTransitionError",
    # Menu en ligne de commande
    "MENU",
    "main",
    "show_choice",
    "take_choice",
    "clear_screen",
    # Métadonnées
    "__version__",
]
