# Class Alignments

The primary classes from CurrKG have direct equivalent classes in [PRO](https://www.sparontologies.net/ontologies/pro), [DataCite](https://www.sparontologies.net/ontologies/datacite), [FaBiO](https://www.sparontologies.net/ontologies/fabio), [Mito](https://www.sparontologies.net/ontologies/mito), [dcterms](https://www.dublincore.org/specifications/dublin-core/collection-description/collection-terms/), [c4o](https://www.sparontologies.net/ontologies/c4o), [foaf](https://www.w3.org/wiki/Good_Ontologies) and [co](https://www.w3.org/TR/vocab-org/) Ontologies; part of the [SPAR](https://www.sparontologies.net) and Organization Ontologies.

## FOAF Alignment

| Curriculum KG Class | Alignment Relation | foaf |
|--------------------|-----------------|-------------|
| currkg:Author | subclass of | foaf:Agent |
| currkg:Person | equivalent class | foaf:Person|
|currkg:Category| sub-property of| foaf:Group |
|currkg:Curriculum| sub-property of | foaf:Group |
|currkg:Event| sub-property of | foaf:Group |
|currkg:Media| sub-property of | foaf:Group |
|currkg:Module| sub-property of | foaf:Group|
|currkg:Persona| sub-property of | foaf:Group |
|currkg:Topic| sub-property of | foaf:Group |
| currkg:hasTitle | sub-property of | foaf:hasName|
| currkg:hasName| equivalent class | foaf:hasName |

-----

## DataCite Alignment

| Curriculum KG Class | Alignment Relation | datacite |
|--------------------|-----------------|-------------|
|currkg:Category| sub-property of| datacite:ResourceIdentifier |
|currkg:Curriculum| sub-property of | datacite:ResourceIdentifier |
|currkg:Event| sub-property of | datacite:ResourceIdentifier |
|currkg:Media| sub-property of | datacite:ResourceIdentifier|
|currkg:Module| sub-property of | datacite:ResourceIdentifier |
|currkg:Persona| sub-property of | datacite:ResourceIdentifier |
|currkg:Topic| sub-property of | datacite:ResourceIdentifier |
| currkg:hasType| sub-property of | datacite:hasDescriptionType |

---------

## FaBiO Alignment

| Curriculum KG Class | Alignment Relation | fabio |
|--------------------|-----------------|-------------|
|currkg:Curriculum| sub-property of | fabio:subjectTerm |
|currkg:Topic| sub-property of | fabio:subjectTerm, co:listItem |

-----------

## CO Alignment

| Curriculum KG Class | Alignment Relation | co |
|--------------------|-----------------|-------------|
|currkg:LearningStep| sub-property of | co:listItem |
|currkg:Level| sub-property of | co:listItem |
|currkg:Topic| sub-property of | co:listItem |

------------

## Mito Alignment

| Curriculum KG Class | Alignment Relation | mito |
|--------------------|-----------------|-------------|
| currkg:refersTo| sub-property of | mito:mentions |
| currkg:refersTo| sub-property of | mito:mentions |
| currkg:coversTopic| sub-property of | mito:hasMentionedEntity |
| currkg:references| sub-property of | mito:mentions |

----------

## C4O Alignment

| Curriculum KG Class | Alignment Relation | c4o |
|--------------------|-----------------|-------------|
| currkg:hasModule| sub-property of | c4o:hasContent |

---------

## OA Alignment

| Curriculum KG Class | Alignment Relation | oa |
|--------------------|-----------------|-------------|
| currkg:hasAuthor| sub-property of | oa:annotatedBy |
| currkg:scopedBy| sub-property of | oa:hasTarget |

----------

## PRO Alignment

| Curriculum KG Class | Alignment Relation | pro |
|--------------------|-----------------|-------------|
| currkg:assumesAuthorship| sub-property of | pro:withRole |
| currkg:assumesPersona| sub-property of | pro:withRole |









