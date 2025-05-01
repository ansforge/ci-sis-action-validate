![Logo_LEF_CI-SIS](https://user-images.githubusercontent.com/48218773/227532484-eff82649-4e42-49c6-966a-dc3ea78cf59c.png)

# GitHub Action pour la validation des fichiers du CI-SIS

GitHub Action pour les valider les exemples du CI-CIS : 
  - Rapport de validation dans l'action

La cle API de gazelle est accéssible via ce lien : 
- https://interop.esante.gouv.fr/evs/administration/apiKeyManagement.seam
## Usage

### Exemple Workflow file

Un exemple pour valider les exemples d'un REPO

```yaml
name: Workflow Validate
on:
  workflow_call:
  push:
  workflow_dispatch:
jobs:
  run-sushi-tests_gitHubPages:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:    
          path: source
      - uses: ansforge/ci-sis-action-validate@main
        with:      
          repo: "./source"
          apiKey:
            description: "Cle API Gazelle"
            required: true    
```

### Inputs

| name               | value   | default               | description                                                                                                                                                                                                                                                                                                     |
|--------------------|---------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| repo    | string  |  | Nom du répertoire à analyser|
| apiKey  | string  |  |Cle API de Gazelle|




