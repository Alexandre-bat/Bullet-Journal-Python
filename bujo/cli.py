"""Menu en ligne de commande de la bibliothèque Bullet Journal."""

from __future__ import annotations

import logging
import os

from bujo.entry import Note, Event
from bujo.exceptions import BujoError
from bujo.journal import Journal, setup_logging

MENU = """
===== Bullet Journal =====
1. Ajouter une tâche
2. Ajouter un événement
3. Ajouter une note
4. Marquer une tâche comme terminée
5. Supprimer une entrée
6. Afficher les tâches en cours
7. Quitter
"""


def clear_screen() -> None:
    """Vide le terminal."""
    os.system("cls" if os.name == "nt" else "clear")


def show_choice() -> None:
    """Affiche le menu des actions possibles."""
    print(MENU)


def take_choice(journal: Journal) -> bool:
    """Lit le choix de l'utilisateur et exécute l'action associée.

    Retourne False pour quitter le programme, True sinon.
    """
    choice = input("Votre choix : ").strip()
    try:
        if choice == "1":
            name = input("Nom de la tâche : ")
            description = input("Description : ")
            task = journal.add_task(name, description)
            print(f"Tâche ajoutée (id {task.id[:8]}…).")
        elif choice == "2":
            name = input("Nom de l'événement : ")
            event = Event(name, input("Description : "))
            journal.add_entry(event)
            print(f"Événement ajouté (id {event.id[:8]}…).")
        elif choice == "3":
            name = input("Nom de la note : ")
            note = Note(name, input("Description : "))
            journal.add_entry(note)
            print(f"Note ajoutée (id {note.id[:8]}…).")
        elif choice == "4":
            entry_id = _ask_id(journal)
            task = journal.complete_task(entry_id)
            print(f"Tâche terminée : {task}.")
        elif choice == "5":
            entry_id = _ask_id(journal)
            entry = journal.remove_entry(entry_id)
            print(f"Entrée supprimée : {entry}.")
        elif choice == "6":
            tasks = journal.open_tasks()
            if not tasks:
                print("Aucune tâche en cours.")
            for task in tasks:
                print(f"[{task.id[:8]}] {task}")
        elif choice == "7":
            return False
        else:
            print("Choix inconnu, réessayez.")
    except BujoError as error:
        print(f"Erreur : {error}")
    return True


def _ask_id(journal: Journal) -> str:
    """Demande un identifiant (début ou entier) et le résout."""
    raw = input("Identifiant de l'entrée : ").strip()
    for entry_id in journal.ids():
        if entry_id == raw or entry_id.startswith(raw):
            return entry_id
    return raw


def main() -> None:
    """Point d'entrée : initialise les logs puis lance la boucle du menu."""
    setup_logging()
    logger = logging.getLogger("bujo")
    logger.info("Démarrage du Bullet Journal.")
    journal = Journal()
    print("Bienvenue dans votre Bullet Journal !")
    running = True
    while running:
        show_choice()
        running = take_choice(journal)
        if running:
            input("Appuyez sur Entrée pour revenir au menu…")
            clear_screen()
    logger.info("Fin du programme.")


if __name__ == "__main__":
    main()
