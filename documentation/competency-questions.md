# Competency Questions and SPARQL Queries

## Question 1

**Competency Question:** What are all the covered topics?

**SPARQL Query:**

```sparql
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?topic ?topicName
WHERE {
  ?topic rdf:type currkg:Topic ;
         currkg:asString ?topicName .
}
```

## Question 2

**Competency Question:** What are all the available learning media?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?media ?title
WHERE {
    ?media a currkg:Media ;
           currkg:hasTitle ?title .
}mediaTmediaTitle
```

## Question 3

**Competency Question:** What are the different types of media resources?

**SPARQL Query:**

```sparql
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?mediaType 
WHERE {
    ?media rdf:type currkg:Media .
    ?media rdf:type ?mediaType .
}

```

## Question 4

**Competency Question:** Who are all the available authors?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?author ?authorName
WHERE {
    ?author a currkg:Author ;
            currkg:hasName ?authorName .
}
```

## Question 5

**Competency Question:** Which authors are associated with a specific media resource?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaTitle ?author ?authorName
WHERE {
    ?media rdf:type currkg:Media ;
           currkg:hasTitle ?mediaTitle ;
           currkg:hasAuthor ?author .

    ?author rdf:type currkg:Author ;
            currkg:hasName ?authorName .
}
```

## Question 6

**Competency Question:** What media resources are linked to a specific topic?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaTitle
WHERE {
    ?media a currkg:Media ;
           currkg:hasTitle ?mediaTitle ;
           currkg:coversTopic ?topic .
           
    ?topic a currkg:Topic ;
           currkg:asString ?topicTitle .

    FILTER regex(?topicTitle, "A Specific Topic", "i")
}
```

## Question 7

**Competency Question:** Which persona is associated with which learning path, and what are the learning steps within that path?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?persona ?personaName ?learningPath ?learningStep ?learningStepName ?prevStep ?prevStepName ?nextStep ?nextStepName
WHERE {
    ?persona a currkg:Persona ;
             currkg:determines ?learningPath ;
             currkg:asString ?personaName.

    ?learningPath currkg:hasLearningSteps ?learningStep .
    
    ?learningStep currkg:asString ?learningStepName.

    OPTIONAL {
        ?learningStep currkg:hasPreviousLearningStep ?prevStep .
        ?prevStep currkg:asString ?prevStepName.
    }
    OPTIONAL {
        ?learningStep currkg:hasNextLearningStep ?nextStep .
        ?nextStep currkg:asString ?nextStepName.
    }
}
```

## Question 8

**Competency Question:** Which media resources belong to a specific type?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?media ?title ?type ?typeName
WHERE {
    ?media rdf:type currkg:Media ;
           currkg:hasTitle ?title ;
           rdf:type ?type .
    ?type currkg:asString ?typeName.
    
    FILTER regex(?typeName, "A Specific Type", "i")
}
```

## Question 9

**Competency Question:** What are the top 10 most referenced media resources?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaTitle (COUNT(?referencingEntity) AS ?referenceCount)
WHERE {
    ?referencingEntity currkg:references ?media .
    ?media currkg:hasTitle ?mediaTitle.
}
GROUP BY ?media ?mediaTitle
ORDER BY DESC(?referenceCount)
LIMIT 10
```

## Question 10

**Competency Question:** Are there Personas that have overlapping Learning Paths?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?learningPath ?learningPathName (GROUP_CONCAT(DISTINCT ?persona; separator=", ") AS ?personas)
WHERE {
    ?persona rdf:type currkg:Persona ;
             currkg:determines ?learningPath .
    
    ?learningPath currkg:asString ?learningPathName .
}
GROUP BY ?learningPath ?learningPathName
HAVING (COUNT(?persona) > 1)  

```

## Question 11

**Competency Question:** What topics have the most associated media resources?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?topic ?topicName (COUNT(?media) AS ?mediaCount)
WHERE {
    ?media rdf:type currkg:Media .
    ?media currkg:coversTopic ?topic .
    ?topic currkg:asString ?topicName .
}
GROUP BY ?topic ?topicName
ORDER BY DESC(?mediaCount)
LIMIT 10
```

## Question 12

**Competency Question:** Which topics are broader than a specific topic?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?broaderTopic ?broaderTopicName
WHERE {
    ?specificTopic a currkg:Topic ;
                   currkg:asString "A Specific Topic" ;
                   currkg:broaderThan ?broaderTopic .
    
    ?broaderTopic currkg:asString ?broaderTopicName .
}
```

## Question 13

**Competency Question:** What are the media resources linked to multiple topics?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaName(COUNT(?topic) AS ?count)
WHERE {
    ?media rdf:type currkg:Media ;
           currkg:hasTitle ?mediaName .
    ?media currkg:coversTopic ?topic .
}
GROUP BY ?media ?mediaName
HAVING (COUNT(?topic) > 1)
ORDER BY DESC(?count)
```

## Question 14

**Competency Question:** Which authors have contributed to multiple media resources?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?author ?authorName (COUNT(?media) AS ?count)
WHERE {
    ?media rdf:type currkg:Media .
    ?media currkg:hasAuthor ?author .
    ?author currkg:hasName ?authorName .
}
GROUP BY ?author ?authorName
HAVING (COUNT(?media) > 1)
ORDER BY DESC(?count)
```

## Question 15

**Competency Question:** What are the most common relationships ?

**SPARQL Query:**

```sparql
SELECT ?predicate (COUNT(?predicate) AS ?count)
WHERE {
    ?s ?predicate ?o .
}
GROUP BY ?predicate
ORDER BY DESC(?count)
```

## Question 16

**Competency Question:** Which authors have co-authored the most media resources?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>

SELECT ?author1 ?author2 (COUNT(DISTINCT ?media) AS ?coAuthoredMediaCount)
WHERE {
    ?media a currkg:Media .
    ?media currkg:hasAuthor ?author1 .
    ?media currkg:hasAuthor ?author2 .
    FILTER(?author1 != ?author2)
}
GROUP BY ?author1 ?author2
ORDER BY DESC(?coAuthoredMediaCount)
LIMIT 10
```

## Question 17

**Competency Question:** Which topics have the most cross-references?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?topic ?topicName (COUNT(?ref) AS ?count)
WHERE {
  ?topic rdf:type currkg:Topic ;
         currkg:asString ?topicName .
  { ?topic currkg:broaderThan ?ref } 
  UNION 
  { ?topic currkg:narrowerThan ?ref }
}
GROUP BY ?topic ?topicName
ORDER BY DESC(?count)
LIMIT 10
```

## Question 18

**Competency Question:** What are the "prerequisite chains" in learning paths?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?learningPath ?learningStep ?learningStepName ?prevStep ?prevStepName ?nextStep ?nextStepName 
WHERE {
    ?learningPath a currkg:Learning_Path .
    ?learningPath currkg:hasLearningSteps ?learningStep .
    ?learningStep currkg:asString ?learningStepName .
    
    OPTIONAL {
        ?learningStep currkg:hasNextLearningStep ?nextStep .
        ?nextStep currkg:asString ?nextStepName .
    }

    OPTIONAL {
        ?learningStep currkg:hasPreviousLearningStep ?prevStep .
        ?prevStep currkg:asString ?prevStepName .
    }
}
```

## Question 19

**Competency Question:** What themes are addressed by each module?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

```sparql
SELECT ?module ?moduleTitle ?theme ?themeName
WHERE {
    ?module a currkg:Module ;
            currkg:hasTitle ?moduleTitle ;
            currkg:hasTheme ?theme .
    ?theme currkg:asString ?themeName .
}
GROUP BY ?themeName
ORDER BY DESC(?moduleCount)
```

## Question 20

**Competency Question:** What levels are assigned to each module?

**SPARQL Query:**

```sparql
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>

SELECT ?module ?moduleTitle ?level ?levelName
WHERE {
    ?module a currkg:Module ;
            currkg:hasTitle ?moduleTitle ;
            currkg:hasLevel ?level .
    
    ?level currkg:asString ?levelName .
}
```

## Question 21 

**Competency Question:** What are the preferred labels, alternative labels, and definitions of topics in the lower-level ontology?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?topic ?prefLabel ?altLabel ?definition
WHERE {
    ?topic a currkg:Topic .
    OPTIONAL { ?topic skos:prefLabel ?prefLabel . }
    OPTIONAL { ?topic skos:altLabel ?altLabel . }
    OPTIONAL { ?topic skos:definition ?definition . }
}
```

## Question 22

**Competency Question:**: Which media resources (such as videos) are recommended or by specific presentations?

**SPARQL Query:**

```sparql
PREFIX currkg-r: <https://kastle-lab.org/currkg/lod/resource#>
PREFIX currkg: <https://kastle-lab.org/currkg/lod/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?presentation ?presentationTitle ?media ?mediaTitle ?mediaType
WHERE {
    
    ?presentation a currkg:Presentation ;
                  currkg:hasTitle ?presentationTitle ;
                  currkg:hasRecomended ?media . 
                  
    ?media a currkg:Video ;
           currkg:hasTitle ?mediaTitle ;
           rdf:type ?mediaType .
           
    FILTER (?mediaType != currkg:Media)
}
```