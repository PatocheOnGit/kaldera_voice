# Kaldera Voice

Chat vocal du serveur Minecraft **Kaldera** : une version modifiée de [Plasmo Voice](https://github.com/plasmoapp/plasmo-voice), par Plasmo (Apehum et l'équipe Plasmo), sous licence **GNU LGPL 3.0**. Ce dépôt public contient le code de nos modifications, comme la licence le demande. Tout le mérite du chat vocal revient à l'équipe Plasmo.

## Ce qui change par rapport à Plasmo Voice

- Branche `kaldera`, partie de Plasmo Voice 2.2.0-beta.3 (commit `198ad94`) ; seule la version NeoForge 26.3 est construite et livrée.
- Nom « Kaldera Voice », logo Kaldera, icônes recolorées aux couleurs de Kaldera (`kaldera/recolor_icons.py`, à partir des icônes d'origine).
- Palette des écrans aux couleurs de Kaldera.
- Traduction française complète (`kaldera/fr_fr.json`), livrée avec le mod.
- Aucun appel aux serveurs de Plasmo depuis le jeu des joueurs : pas de vérification de mise à jour, pas de téléchargement de traductions ni de crédits (le launcher Kaldera livre tout).
- Crédits et liens d'origine conservés dans l'onglet « À propos », avec un lien vers ce dépôt.

Les modifications de code sont appliquées par `kaldera/rebrand.py` (idempotent), pour pouvoir les refaire après une fusion de l'original.

## Construire

```bash
./gradlew :client:26.3-neoforge:build -x test
```

Le jar est dans `client/26.3-neoforge/build/libs/`. Dans le projet Kaldera : `./gradlew buildVoice`.

## Reprendre un correctif de Plasmo Voice

```bash
git remote add upstream https://github.com/plasmoapp/plasmo-voice.git
git fetch upstream
git merge upstream/main
python kaldera/rebrand.py
python kaldera/recolor_icons.py
```

## Licence

GNU LGPL 3.0 (voir `LICENSE`), comme Plasmo Voice. Les icônes recolorées dérivent de celles de Plasmo Voice et restent sous la même licence.
