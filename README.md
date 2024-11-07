![Logo_LEF_CI-SIS](https://user-images.githubusercontent.com/48218773/227532484-eff82649-4e42-49c6-966a-dc3ea78cf59c.png)

# GitHub Action pour la publication d'IG FHIR

GitHub Action pour les valider les exemples du CI-CIS : 
  - Rapport de validation dans l'action


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
```

### Inputs

| name               | value   | default               | description                                                                                                                                                                                                                                                                                                     |
|--------------------|---------|-----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| repo    | string  |latest  | Nom du répertoire à analyser|




