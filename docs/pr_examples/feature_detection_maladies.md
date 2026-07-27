# Ajout de la fonctionnalité de détection des maladies des plantes par image

## Ce que fait cette PR

Cette Pull Request ajoute la première version du module de détection des maladies des plantes à partir d'une image. L'objectif est de permettre aux agriculteurs de prendre une photo d'une plante depuis l'application et d'obtenir une estimation de la maladie détectée ainsi qu'une recommandation de traitement adaptée.

Cette fonctionnalité introduit la communication entre le frontend React et le backend FastAPI afin d'envoyer les images, traiter les requêtes et retourner un résultat exploitable par l'utilisateur.

## Pourquoi

Les maladies des plantes sont souvent détectées trop tard, ce qui peut entraîner une diminution importante des récoltes. Cette fonctionnalité permet d'aider les agriculteurs à identifier rapidement les premiers signes d'une maladie et à prendre des mesures adaptées.

Issue associée : Closes #15

## Comment tester

1. Lancer le backend FastAPI.
2. Lancer l'application frontend.
3. Accéder à la page de diagnostic des plantes.
4. Importer une image d'une plante malade.
5. Vérifier que l'API reçoit correctement l'image et retourne une réponse.

## Points d'attention pour le reviewer

- Le modèle ML utilisé dans cette version est un prototype et pourra être amélioré dans une prochaine phase.
- La validation des formats d'image devra être renforcée avant la mise en production.
- Les messages affichés à l'utilisateur devront être disponibles en français et en bambara.