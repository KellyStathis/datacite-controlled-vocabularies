<img src="https://thumb.tildacdn.com/tild3934-3732-4633-b864-646466363531/-/format/webp/FAIRware_Logo.jpg" alt="incentive logo" height="75"/>
<img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fciser.cornell.edu%2Fwp-content%2Fuploads%2F2020%2F01%2FdataciteNoBorder.png&f=1&nofb=1" alt="incentive logo" height="75"/>

[![CI](https://github.com/metadatacenter/datacite-controlled-vocabulary/workflows/Sheet2RDF/badge.svg)](https://github.com/metadatacenter/datacite-controlled-vocabulary/actions?query=workflow%3ASheet2RDF)

# DataCite Controlled Vocabularies

This repository hosts the DataCite Controlled Vocabularies that are part of the [DataCite Metadata Schema](https://datacite-metadata-schema.readthedocs.io/en/4.5/), along with workflows and scripts used to convert the DataCite Controlled Vocabularies into different formats.

There are ten controlled lists represented in this repository in the `vocabularies` directory:
- contributorType
- dateType
- descriptionType
- funderIdentifierType
- nameType
- numberType
- relatedIdentifierType
- relationType
- resourceTypeGeneral
- titleType

There are two workflows and associated scripts contained in this repository:

1. sheet2rdf: Converts a Google Sheet to CSV, XLSX, and TTL files.
2. csv2xd: Converts the CSV output from sheet2rdf to XSD files.

*The foundations of this work were completed as part of the [FAIRware project](https://researchonresearch.org/projects#!/tab/273951116-3) which is funded by [RoRi](https://researchonresearch.org/).*

# Tooling

## [![DOI](https://zenodo.org/badge/327900313.svg)](https://zenodo.org/badge/latestdoi/327900313) sheet2rdf

This repository hosts a modified version of the sheet2rdf automatic workflow, executed by means of GitHub actions, and underlying shell and python scripts which:

- Fetches Google Sheet from Google Drive
- Stores the Google Sheet as a CSV file (with modifications) and an XLSX file
- Converts fetched sheet to machine-actionable and FAIR RDF vocabulary using [xls2rdf](https://github.com/sparna-git/xls2rdf)
- Commits conversion results and tests logs to this repository
  
This workflow is an extension of [excel2rdf](https://github.com/fair-data-collective/excel2rdf-template).

### Citation

In case you are using this workflow the author kindly requests you to cite this repository in your publications such as:

> Nikola Vasiljevic. (2021, January 11). sheet2rdf: First release (Version v0.1). Zenodo. http://doi.org/10.5281/zenodo.4432136

For any other citation format visit http://doi.org/10.5281/zenodo.4432136

### License

This work is licensed under [Apache 2.0 License](https://github.com/niva83/sheet2rdf/blob/main/License.md)

## csv2xsd

This workflow and underlying scripts are used to generate the vocabulary specific XSD files necessary for inclusion in the DataCite Metadata Schema defintion.

# Configuration

The folloiwng configuration applies to both sheet2rdf and csv2xsd.

1. Follow [gsheets](https://pypi.org/project/gsheets/) Quickstart and generate client_secrets.json and storage. (When generating credentials, use type "Desktop App" instead of "Other".)

2. Create the following [GitHub secrets](https://docs.github.com/en/free-pro-team@latest/actions/reference/encrypted-secrets):

| Secret          | Explanation                                                                                                        | DataCite Controlled Vocabulary                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FILE_NAME       | file name that will be used when converting Google sheet to `.ttl` (RDF), `.xlsx`, and `.csv` files                | vocabulary                                                                                                                                              |
| SHEET_ID        | unique ID of the sheet that will be fetched from Google drive                                                      | [1Vz17roE_0_rpcZwI3qKlgxIx7p6OKDNtDM2bmsoorsU](https://docs.google.com/spreadsheets/d/1Vz17roE_0_rpcZwI3qKlgxIx7p6OKDNtDM2bmsoorsU/edit#gid=1198865354) |
| STORAGE         | configuration for client (i.e., sheetrdf) that is fetching Google sheet, content of storage.json | **\*\*\*\***                                                                                                                                                              |
| CLIENT          | access token to Google Drive hosting Google sheet with controlled terms definitions, content of client_secret.json | **\*\*\*\***                                                                                                                           |
| SAVE_DIR          | location to save output files                  | vocabularies/   |
