"""Exceptions personnalisées de la bibliothèque Bullet Journal."""

# Erreur de base de la bibliothèque Bullet Journal.


class BujoError(Exception):
    pass


# L'identifiant demandé ne correspond à aucune entrée du journal.
class EntryNotFoundError(BujoError):
    pass


# Le nom d'une entrée ne peut pas être vide.
class EmptyNameError(BujoError):
    pass


# La date fournie est invalide.
class InvalidDateError(BujoError):
    pass


# La transition d'état demandée est interdite pour une tâche.
class InvalidStateTransitionError(BujoError):
    pass


# Le signifiant demandé ne fait pas partie des signifiants connus.
class InvalidSignifierError(BujoError):
    pass


# Le journal n'a pu être sauvegardé ou chargé depuis son fichier.
class PersistenceError(BujoError):
    pass
