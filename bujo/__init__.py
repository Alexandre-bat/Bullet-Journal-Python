"""Bullet Journal — bibliothèque Python de gestion d'un journal personnel.

Ce package expose l'API publique de la bibliothèque :

- les types d'entrées (Entry, Task, Event, Note) et l'état d'une
  tâche (TaskState)
- l'organisation du journal (Journal) et la configuration des logs
  (setup_logging)
- les exceptions personnalisées
- la fonction ``main`` du menu en ligne de commande
"""

from bujo.entry import Entry, Event, Note, Task, TaskState
from bujo.exceptions import (
    BujoError,
    EmptyNameError,
    EntryNotFoundError,
    InvalidDateError,
    InvalidStateTransitionError,
)
from bujo.journal import Journal, setup_logging

__version__ = "0.1.0"

__all__ = [
    "Entry",
    "Task",
    "Event",
    "Note",
    "TaskState",
    "Journal",
    "setup_logging",
    "BujoError",
    "EntryNotFoundError",
    "EmptyNameError",
    "InvalidDateError",
    "InvalidStateTransitionError",
    "__version__",
]
