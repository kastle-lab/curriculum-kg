# curriculum-kg ![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg) ![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)


### Repository Structure
* `schema/` - Directory containing the CurrKG ontology files (e.g., schema diagrams, OWL file, competency questions).
* `scripts/` - Directory containing data, scripts used for materialization, and the resulting materialized files.
  * `data/` - Directory with source data for CurrKG.
  * `materialization/` - Directory containing the materialized instance of CurrKG (`.ttl` file) generated by the scripts.


### License

- **Code** in this repository (Python scripts used for materialization) is licensed under the [Apache License 2.0](./LICENSE).
- **Ontology** (schema files, diagrams, competency questions, sample data) is licensed under the  
  [Creative Commons Attribution-ShareAlike 4.0 International License](./LICENSE.docs).  
  This includes:
  - RDF/OWL files (`.ttl`, `.owl`)
  - Schema diagrams (`.graphml`, `.png`)
  - Initial curriculum data  
 
  By contributing, you agree to license your contributions under these same terms.