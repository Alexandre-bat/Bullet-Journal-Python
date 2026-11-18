"""Organisation du journal : stockage et cycle de vie des entrées."""

from __future__ import annotations

import logging
from datetime import date

from bujo.entry import Entry, Task, TaskState
from bujo.exceptions import EntryNotFoundError, InvalidStateTransitionError

logger = logging.getLogger("bujo")


def setup_logging(
    debug_file: str = "bujo_debug.log",
    error_file: str = "bujo_error.log",
) -> None:
    """Configure les fichiers de log : debug complet et erreurs seules."""
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    debug_handler = logging.FileHandler(debug_file, encoding="utf-8")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    error_handler = logging.FileHandler(error_file, encoding="utf-8")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(debug_handler)
    logger.addHandler(error_handler)


class Journal:
    """Journal personnel contenant des entrées indexées par identifiant."""

    # Initialise un journal vide portant le nom donné.
    def __init__(self, name: str = "Mon journal") -> None:
        self.name: str = name
        self._entries: dict[str, Entry] = {}

    # Nombre d'entrées dans le journal.
    def __len__(self) -> int:
        return len(self._entries)

    # Retourne les identifiants de toutes les entrées.
    def ids(self) -> list[str]:
        return list(self._entries)

    # Ajoute une entrée et retourne son identifiant unique.
    def add_entry(self, entry: Entry) -> str:
        if not isinstance(entry, Entry):
            raise TypeError("Seules des entrées du journal peuvent être "
                            "ajoutées.")
        self._entries[entry.id] = entry
        logger.debug("Entrée %s (%s) ajoutée au journal « %s ».",
                     entry.id, entry.name, self.name)
        return entry.id

    # Crée une tâche, l'ajoute au journal et la retourne.
    def add_task(
        self,
        name: str,
        description: str = "",
        log_date: date | None = None,
        signifier: str | None = None,
    ) -> Task:
        task = Task(name, description, log_date, signifier)
        self.add_entry(task)
        return task

    # Retourne l'entrée correspondant à l'identifiant donné.
    def get_entry(self, entry_id: str) -> Entry:
        try:
            return self._entries[entry_id]
        except KeyError:
            logger.error("Entrée introuvable : %s.", entry_id)
            raise EntryNotFoundError(
                f"Aucune entrée avec l'identifiant {entry_id}."
            ) from None

    # Supprime et retourne l'entrée correspondant à l'identifiant.
    def remove_entry(self, entry_id: str) -> Entry:
        entry = self.get_entry(entry_id)
        del self._entries[entry_id]
        logger.debug("Entrée %s supprimée.", entry_id)
        return entry

    # Retourne l'entrée demandée après avoir vérifié sa nature.
    def _task(self, entry_id: str) -> Task:
        entry = self.get_entry(entry_id)
        if not isinstance(entry, Task):
            raise InvalidStateTransitionError(
                "Seule une tâche peut changer d'état."
            )
        return entry

    # Marque une tâche comme terminée (symbole ×).
    def complete_task(self, entry_id: str) -> Task:
        task = self._task(entry_id)
        task.complete()
        logger.debug("Tâche %s terminée.", entry_id)
        return task

    # Marque une tâche comme migrée (symbole >).
    def migrate_task(self, entry_id: str) -> Task:
        task = self._task(entry_id)
        task.migrate()
        logger.debug("Tâche %s migrée.", entry_id)
        return task

    # Marque une tâche comme planifiée (symbole <).
    def plan_task(self, entry_id: str) -> Task:
        task = self._task(entry_id)
        task.plan()
        logger.debug("Tâche %s planifiée.", entry_id)
        return task

    # Marque une tâche comme abandonnée (symbole ~).
    def discard_task(self, entry_id: str) -> Task:
        task = self._task(entry_id)
        task.discard()
        logger.debug("Tâche %s abandonnée.", entry_id)
        return task

    # Retourne les tâches restant à faire, dans l'ordre d'ajout.
    def open_tasks(self) -> list[Task]:
        return [
            entry
            for entry in self._entries.values()
            if isinstance(entry, Task) and entry.state is TaskState.TODO
        ]

    # Retourne les entrées du log de la journée donnée.
    def entries_of_day(self, day: date) -> list[Entry]:
        if not isinstance(day, date):
            raise TypeError("day doit être un datetime.date.")
        return [
            entry for entry in self._entries.values()
            if entry.log_date == day
        ]

    # Rechercher les entrées dont le nom contient le mot-clé.
    #     Recherche secondaire (insensible à la casse) qui retourne
    #     toutes les entrées correspondantes.
    def search_by_name(self, keyword: str) -> list[Entry]:
        needle = keyword.casefold()
        return [
            entry for entry in self._entries.values()
            if needle in entry.name.casefold()
        ]
