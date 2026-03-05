# Class Alignments

The primary classes from CurrKG have direct equivalent classes in [PRO](https://www.sparontologies.net/ontologies/pro), [DataCite](https://www.sparontologies.net/ontologies/datacite[), [FaBiO](https://www.sparontologies.net/ontologies/fabio), [Mito](https://www.sparontologies.net/ontologies/mito), [dcterms](https://www.dublincore.org/specifications/dublin-core/collection-description/collection-terms/), [c4o](https://www.sparontologies.net/ontologies/c4o), [foaf](https://www.w3.org/wiki/Good_Ontologies) and [co](https://www.w3.org/TR/vocab-org/) Ontololgies; part of the [SPAR](https://www.sparontologies.net) and Organization Ontologies.

## FOAF allignment

| Curriculum KG Class | Alignment Relation | foaf |
|--------------------|-----------------|-------------|
| edu-ont:Author | subclass of | foaf:Agent |
| edu-ont:Person | equivalent class | foaf:Person|
|edu-ont:Category| sub-property of| foaf:Group |
|edu-ont:Curriculum| sub-property of | foaf:Group |
|edu-ont:Event| sub-property of | foaf:Group |
|edu-ont:Media| sub-property of | foaf:Group |
|edu-ont:Module| sub-property of | foaf:Group|
|edu-ont:Persona| sub-property of | foaf:Group |
|edu-ont:Topic| sub-property of | foaf:Group |
| edu-ont:hasTitle | sub-property of | foaf:hasName|
| edu-ont:hasName| equivalent class | foaf:hasName |

-----

## DataCite allignment

| Curriculum KG Class | Alignment Relation | datacite |
|--------------------|-----------------|-------------|
|edu-ont:Category| sub-property of| datacite:ResourceIdentifier |
|edu-ont:Curriculum| sub-property of | datacite:ResourceIdentifier |
|edu-ont:Event| sub-property of | datacite:ResourceIdentifier |
|edu-ont:Media| sub-property of | datacite:ResourceIdentifier|
|edu-ont:Module| sub-property of | datacite:ResourceIdentifier |
|edu-ont:Persona| sub-property of | datacite:ResourceIdentifier |
|edu-ont:Topic| sub-property of | datacite:ResourceIdentifier |
| edu-ont:hasType| sub-property of | datacite:hasDescriptionType |

---------

## FaBiO allignment

| Curriculum KG Class | Alignment Relation | fabio |
|--------------------|-----------------|-------------|
|edu-ont:Curriculum| sub-property of | fabio:subjectTerm |
|edu-ont:Topic| sub-property of | fabio:subjectTerm, co:listItem |

-----------

## CO allignment

| Curriculum KG Class | Alignment Relation | co |
|--------------------|-----------------|-------------|
|edu-ont:LearningStep| sub-property of | co:listItem |
|edu-ont:Level| sub-property of | co:listItem |
|edu-ont:Topic| sub-property of | co:listItem |

------------

## Mito allignment

| Curriculum KG Class | Alignment Relation | mito |
|--------------------|-----------------|-------------|
| edu-ont:refersTo| sub-property of | mito:mentions |
| edu-ont:refersTo| sub-property of | mito:mentions |
| edu-ont:coversTopic| sub-property of | mito:hasMentionedEntity |
| edu-ont:references| sub-property of | mito:mentions |

----------

## C4O allignment

| Curriculum KG Class | Alignment Relation | c4o |
|--------------------|-----------------|-------------|
| edu-ont:hasModule| sub-property of | c4o:hasContent |

---------

## OA allignment

| Curriculum KG Class | Alignment Relation | oa |
|--------------------|-----------------|-------------|
| edu-ont:hasAuthor| sub-property of | oa:annotatedBy |
| edu-ont:scopedBy| sub-property of | oa:hasTarget |

----------

## PRO allignment

| Curriculum KG Class | Alignment Relation | pro |
|--------------------|-----------------|-------------|
| edu-ont:assumesAuthorship| sub-property of | pro:withRole |
| edu-ont:assumesPersona| sub-property of | pro:withRole |









