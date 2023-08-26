<img src="https://thumb.tildacdn.com/tild3934-3732-4633-b864-646466363531/-/format/webp/FAIRware_Logo.jpg" alt="incentive logo" height="75"/>
<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fciser.cornell.edu%2Fwp-content%2Fuploads%2F2020%2F01%2FdataciteNoBorder.png&f=1&nofb=1" alt="incentive logo" height="75"/>

[![CI](https://github.com/metadatacenter/datacite-controlled-vocabulary/workflows/Sheet2RDF/badge.svg)](https://github.com/metadatacenter/datacite-controlled-vocabulary/actions?query=workflow%3ASheet2RDF)

# [DataCite Controlled Vocabulary](http://purl.org/datacite/v4.4/)

Controlled vocabularies allow an accurate and controlled approach in describing physical and digital assets (e.g., data). One of such controlled vocabulary is **DataCite Controlled Vocabulary**. This controlled vocabulary is produced based on description of [Datacite Schema V4.4](https://schema.datacite.org/meta/kernel-4.4/). The work of creating this controlled vocabulary is part of [FAIRware project](https://researchonresearch.org/projects#!/tab/273951116-3) which if funded by [RoRi](https://researchonresearch.org/).

`sheet2rdf` and `OntoStack`, are used to build and serve **DataCite Controlled Vocabulary**, while [PURL](https://archive.org/services/purl/), is used to persist identifiers for the vocabulary:

http://purl.org/datacite/v4.4/

# Tooling

## [![DOI](https://zenodo.org/badge/327900313.svg)](https://zenodo.org/badge/latestdoi/327900313) sheet2rdf

This repository hosts automatic workflow, executed by means of Github actions, and underlying shell and python scripts which:

- Fetches Google Sheet from Google Drive and stores is as `xlsx` and `csv` files
- Converts fetched sheet to machine-actionable and FAIR RDF vocabulary using [xls2rdf](https://github.com/sparna-git/xls2rdf)
- Tests the resulting RDF vocabulary using [qSKOS](https://github.com/cmader/qSKOS/)
- Commits conversion results and tests logs to this repository
- and deploy RDF vocabulary to OntoStack to be served to humans and machines

This workflow is an extension of [excel2rdf](https://github.com/fair-data-collective/excel2rdf-template).

### Configuring sheet2rdf

In case you want to use **sheet2rdf** in your own work you need to:

1. Follow [gsheets](https://pypi.org/project/gsheets/) Quickstart and generate client_secrets.json and storage:

- When generating credentials, use type "Desktop App" (formerly "Other").

2. Create following [Github secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets):

| Secret          | Explanation                                                                                                        | DataCite Controlled Vocabulary                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DB_USER         | user name of Jena Fuseki user account that has privilages to PUT RDF vocabulary to the database                    | **\*\*\*\***                                                                                                                                            |
| DB_PASS         | password of for the above account Jena Fuseki account                                                              | **\*\*\*\***                                                                                                                                            |
| FILE_NAME       | file name that will be used when converting Google sheet to `.ttl` (RDF), `.xlsx`, and `.csv` files                | vocabulary                                                                                                                                              |
| GRAPH           | graph in the database under which the above RDF vocabulary should be stored                                        | http://purl.org/datacite/v4.4/                                                                                                                          |
| SHEET_ID        | unique ID of the sheet that will be fetched from Google drive                                                      | [1vmsxnnCRKkKRcJoRRkoQ5499U-IZgKD6ZBtUu41zz1M](https://docs.google.com/spreadsheets/d/1vmsxnnCRKkKRcJoRRkoQ5499U-IZgKD6ZBtUu41zz1M/edit#gid=1198865354) |
| SPARQL_ENDPOINT | endpoint to which RDF vocabulary is PUT                                                                            | **\*\*\*\***                                                                                                                                            |
| STORAGE         | configuration for client (i.e., sheetrdf) that is fetching Google sheet, content of storage.json | **\*\*\*\***                                                                                                                                            |
| CLIENT          | access token to Google Drive hosting Google sheet with controlled terms definitions, content of client_secret.json                  | **\*\*\*\***                                                                                                                                            |
| SAVE_DIR          | location to save output files                  | vocabularies/sheet2rdf/   |

### Citation

In case you are using this workflow the author kindly requests you to cite this repository in your publications such as:

> Nikola Vasiljevic. (2021, January 11). sheet2rdf: First release (Version v0.1). Zenodo. http://doi.org/10.5281/zenodo.4432136

For any other citation format visit http://doi.org/10.5281/zenodo.4432136

### License

This work is licensed under [Apache 2.0 License](https://github.com/niva83/sheet2rdf/blob/main/License.md)

## OntoStack

OntoStack is a set of orchestrated micro-services configured and interfaced such that they can intake vocabularies and resolve their terms and RDF properties upon requests either by humans or machines.

Some of OntoStack micro-services are:

- [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) a graph database
- [SKOSMOS](http://www.skosmos.org/) a web-based SKOS browser acting as a front-end for the vocabularies persisted by the graph database
- [Træfik](https://doc.traefik.io/traefik/) an edge router responsible for proper serving of URL requests

Currently three instances of OntoStack are available:

- Departamental instance of [DTU Wind Energy](https://www.vindenergi.dtu.dk/english/): http://data.windenergy.dtu.dk/ontologies
- National (Danish) instance ran by [DeiC](https://deic.dk/): http://ontology.deic.dk/
- International instance ran by [FAIR Data Collective](http://fairdatacollective.org/): http://vocab.fairdatacollective.org
