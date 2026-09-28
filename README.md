# Timeless

Un système d'exploitation mobile original, réactif et portable, conçu pour prolonger la vie de
smartphones anciens sans bloatware.

> **État du projet : J0 — cadrage et laboratoire reproductible.** Aucun noyau, prototype QEMU ou port
> matériel n'est encore revendiqué comme existant.

## Principes

- Réactivité perçue et stabilité mesurées avant l'ajout de fonctions.
- Cœur commun portable ; adaptations matérielles isolées par architecture et appareil.
- Système, outils de construction, spécifications et documentation publics.
- Preuves réelles avant toute affirmation de compatibilité ou de performance.
- Travail matériel réversible, documenté et soumis à validation explicite.
- Cycle obligatoire : Spec Kit → clarification → plan → tâches → analyse → implémentation → preuves.

La constitution complète du projet est dans
[`.specify/memory/constitution.md`](.specify/memory/constitution.md).

## Licence

Le code est distribué sous **GPL-3.0-or-later**. Les spécifications, la documentation et les artefacts
de conception sont distribués sous **CC-BY-SA-4.0**, sauf indication contraire pour un élément tiers.
Les firmwares matériels nécessaires restent des dépendances externes documentées ; ils ne font pas
partie du projet Timeless.

Voir [`LICENSE`](LICENSE).

## Démarrage du travail

Le premier lot sera une spécification J0 : laboratoire QEMU reproductible et preuve de démarrage d'un
noyau autonome. Aucun achat, flash d'appareil ou exposition à des données personnelles/à Internet ne
fait partie de ce dépôt de démarrage.

## Contribution

Chaque lot passe par une branche dédiée et une pull request documentée. Les commits suivent
Conventional Commits ; les PR relient les artefacts Spec Kit, les preuves de test/mesure et les mises à
jour de documentation.
