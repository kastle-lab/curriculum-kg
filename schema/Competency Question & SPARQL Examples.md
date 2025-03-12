# Competency Questions and SPARQL Queries

## Question 1

**Competency Question:** What are all the covered topics?

**SPARQL Query:**

```sparql
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?topic ?topicName
WHERE {
  ?topic rdf:type edu-ont:Topic ;
         edu-ont:asString ?topicName .
}
```

## Question 2

**Competency Question:** What are all the available learning media?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?media ?title
WHERE {
    ?media a edu-ont:Media ;
           edu-ont:hasTitle ?title .
}mediaTmediaTitle
```

## Question 3

**Competency Question:** What are the different types of media resources?

**SPARQL Query:**

```sparql
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?mediaType 
WHERE {
    ?media rdf:type edu-ont:Media .
    ?media rdf:type ?mediaType .
}

```

## Question 4

**Competency Question:** Who are all the available authors?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?author ?authorName
WHERE {
    ?author a edu-ont:Author ;
            edu-ont:hasName ?authorName .
}
```

## Question 5

**Competency Question:** Which authors are associated with a specific media resource?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaTitle ?author ?authorName
WHERE {
    ?media rdf:type edu-ont:Media ;
           edu-ont:hasTitle ?mediaTitle ;
           edu-ont:hasAuthor ?author .

    ?author rdf:type edu-ont:Author ;
            edu-ont:hasName ?authorName .
}
```

## Question 6

**Competency Question:** What media resources are linked to a specific topic?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaTitle
WHERE {
    ?media a edu-ont:Media ;
           edu-ont:hasTitle ?mediaTitle ;
           edu-ont:coversTopic ?topic .
           
    ?topic a edu-ont:Topic ;
           edu-ont:asString ?topicTitle .

    FILTER regex(?topicTitle, "A Specific Topic", "i")
}
```

## Question 7

**Competency Question:** Which persona is associated with which learning path, and what are the learning steps within that path?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?persona ?personaName ?learningPath ?learningStep ?learningStepName ?prevStep ?prevStepName ?nextStep ?nextStepName
WHERE {
    ?persona a edu-ont:Persona ;
             edu-ont:determines ?learningPath ;
             edu-ont:asString ?personaName.

    ?learningPath edu-ont:hasLearningSteps ?learningStep .
    
    ?learningStep edu-ont:asString ?learningStepName.

    OPTIONAL {
        ?learningStep edu-ont:hasPreviousLearningStep ?prevStep .
        ?prevStep edu-ont:asString ?prevStepName.
    }
    OPTIONAL {
        ?learningStep edu-ont:hasNextLearningStep ?nextStep .
        ?nextStep edu-ont:asString ?nextStepName.
    }
}
```

## Question 8

**Competency Question:** Which media resources belong to a specific type?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?media ?title ?type ?typeName
WHERE {
    ?media rdf:type edu-ont:Media ;
           edu-ont:hasTitle ?title ;
           rdf:type ?type .
    ?type edu-ont:asString ?typeName.
    
    FILTER regex(?typeName, "A Specific Type", "i")
}
```

## Question 9

**Competency Question:** What are the top 10 most referenced media resources?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaTitle (COUNT(?referencingEntity) AS ?referenceCount)
WHERE {
    ?referencingEntity edu-ont:references ?media .
    ?media edu-ont:hasTitle ?mediaTitle.
}
GROUP BY ?media ?mediaTitle
ORDER BY DESC(?referenceCount)
LIMIT 10
```

## Question 10

**Competency Question:** What is the next learning step after a specific learning step?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?nextStep ?nextStepLabel
WHERE {
    ?learningStep a edu-ont:Learning_Step ;
                  edu-ont:asString "Specific Learning Step Name" ;
                  edu-ont:hasNextLearningStep ?nextStep .
    
    OPTIONAL { ?nextStep edu-ont:asString ?nextStepLabel }
}
```

## Question 11

**Competency Question:** What topics have the most associated media resources?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?topic ?topicName (COUNT(?media) AS ?mediaCount)
WHERE {
    ?media rdf:type edu-ont:Media .
    ?media edu-ont:coversTopic ?topic .
    ?topic edu-ont:asString ?topicName .
}
GROUP BY ?topic ?topicName
ORDER BY DESC(?mediaCount)
LIMIT 10
```

## Question 12

**Competency Question:** Which topics are broader than a specific topic?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?broaderTopic ?broaderTopicName
WHERE {
    ?specificTopic a edu-ont:Topic ;
                   edu-ont:asString "A Specific Topic" ;
                   edu-ont:broaderThan ?broaderTopic .
    
    ?broaderTopic edu-ont:asString ?broaderTopicName .
}
```

## Question 13

**Competency Question:** What are the media resources linked to multiple topics?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?media ?mediaName(COUNT(?topic) AS ?count)
WHERE {
    ?media rdf:type edu-ont:Media ;
           edu-ont:hasTitle ?mediaName .
    ?media edu-ont:coversTopic ?topic .
}
GROUP BY ?media ?mediaName
HAVING (COUNT(?topic) > 1)
ORDER BY DESC(?count)
```

## Question 14

**Competency Question:** Which authors have contributed to multiple media resources?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?author ?authorName (COUNT(?media) AS ?count)
WHERE {
    ?media rdf:type edu-ont:Media .
    ?media edu-ont:hasAuthor ?author .
    ?author edu-ont:hasName ?authorName .
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
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>

SELECT ?author1 ?author2 (COUNT(DISTINCT ?media) AS ?coAuthoredMediaCount)
WHERE {
    ?media a edu-ont:Media .
    ?media edu-ont:hasAuthor ?author1 .
    ?media edu-ont:hasAuthor ?author2 .
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
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?topic ?topicName (COUNT(?ref) AS ?count)
WHERE {
  ?topic rdf:type edu-ont:Topic ;
         edu-ont:asString ?topicName .
  { ?topic edu-ont:broaderThan ?ref } 
  UNION 
  { ?topic edu-ont:narrowerThan ?ref }
}
GROUP BY ?topic ?topicName
ORDER BY DESC(?count)
LIMIT 10
```

## Question 18

**Competency Question:** What are the "prerequisite chains" in learning paths?

**SPARQL Query:**

```sparql
PREFIX edu-r: <https://edugate.cs.wright.edu/lod/resource/>
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?learningPath ?learningStep ?learningStepName ?prevStep ?prevStepName ?nextStep ?nextStepName 
WHERE {
    ?learningPath a edu-ont:Learning_Path .
    ?learningPath edu-ont:hasLearningSteps ?learningStep .
    ?learningStep edu-ont:asString ?learningStepName .
    
    OPTIONAL {
        ?learningStep edu-ont:hasNextLearningStep ?nextStep .
        ?nextStep edu-ont:asString ?nextStepName .
    }

    OPTIONAL {
        ?learningStep edu-ont:hasPreviousLearningStep ?prevStep .
        ?prevStep edu-ont:asString ?prevStepName .
    }
}
```

## Question 19

**Competency Question:** What events are available, and what are their types? (Presentation, Tutorial, Workshop etc)

**SPARQL Query:**

```sparql
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT ?event ?eventTitle ?eventType
WHERE {
    ?event rdf:type edu-ont:Event .
    ?event edu-ont:asString ?eventTitle .
    
    OPTIONAL {
        ?event edu-ont:hasEventType ?eventType .
    }
}
```

## Question 20

**Competency Question:** What levels are assigned to each module?

**SPARQL Query:**

```sparql
PREFIX edu-ont: <https://edugate.cs.wright.edu/lod/ontology/>

SELECT ?module ?moduleTitle ?level ?levelName
WHERE {
    ?module a edu-ont:Module ;
            edu-ont:hasTitle ?moduleTitle ;
            edu-ont:hasLevel ?level .
    
    ?level edu-ont:asString ?levelName .
}
```
