# Competency Questions and SPARQL Queries

## Question 1

**Competency Question:** What are all the topics covered?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT DISTINCT ?topic ?topicName WHERE {
    ?topic rdf:type edugate:Topic ;
           edugate:asString ?topicName .
}
```

## Question 2

**Competency Question:** What are all the learning media available?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT DISTINCT ?resource ?mediaName WHERE {
    ?resource rdf:type edugate:Media ;
              edugate:hasTitle ?mediaName .
}
```

## Question 3

**Competency Question:** What are the different types of media resources?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT DISTINCT ?type WHERE {
    ?resource rdf:type ?type .
    FILTER(CONTAINS(STR(?type), "Media"))
}
```

## Question 4

**Competency Question:** Who are all the authors available?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT DISTINCT ?author ?authorName WHERE {
    ?author rdf:type edugate:Author ;
            edugate:hasName ?authorName .
}
```

## Question 5

**Competency Question:** Which authors are associated with a specific media resource?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT DISTINCT ?media ?mediaName ?author ?authorName WHERE {
    ?media rdf:type edugate:Media ;
           edugate:hasAuthor ?author ;
           edugate:hasTitle ?mediaName .

    ?author edugate:hasName ?authorName .
}
```

## Question 6

**Competency Question:** What media resources are linked to the topic "Data Science Basics"?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?media ?mediaName WHERE {
    ?media edugate:coversTopic <https://edugate.cs.wright.edu/lod/resource/Topic/Data_Science_Basics> ;
           edugate:hasTitle ?mediaName .
}
```

## Question 7

**Competency Question:** Which persona is associated with which learning path, and what are the learning steps within that path?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT DISTINCT ?persona ?personaName ?learningPath ?learningStep ?learningStepName ?nextStep ?nextStepName WHERE {
    ?persona edugate:determines ?learningPath .
    ?persona rdf:type edugate:Persona ;
             edugate:asString ?personaName .
    ?learningPath rdf:type edugate:Learning_Path ;
                  edugate:asString ?learningPathName ;
                  edugate:hasLearningSteps ?learningStep .
    ?learningStep edugate:asString ?learningStepName ;
          edugate:hasNextLearningStep ?nextStep .

    ?nextStep edugate:asString ?nextStepName .
}
```

## Question 8

**Competency Question:** Which media resources belong to the "Research Guide" category?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?media ?mediaName WHERE {
    ?media rdf:type edugate:Research_Guide ;
           edugate:hasTitle ?mediaName
}
```

## Question 9

**Competency Question:** What are the top 10 most referenced media resources?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?media ?mediaName (COUNT(?ref) AS ?referenceCount) WHERE {
    ?ref ?p ?media .
    ?media rdf:type edugate:Media ;
           edugate:hasTitle ?mediaName .
} GROUP BY ?media ?mediaName
ORDER BY DESC(?referenceCount)
LIMIT 10
```

## Question 10

**Competency Question:** What is the next learning step after "Introduction to Set Theory"?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?nextStep ?nextStepName WHERE {
    <https://edugate.cs.wright.edu/lod/resource/Learning_Path/Learning_Step/Introduction_to_Set_Theory>
        edugate:hasNextLearningStep ?nextStep ;
        edugate:asString ?nextStepName
}
```

## Question 11

**Competency Question:** What topics have the most associated media resources?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?topic ?topicName (COUNT(?media) AS ?count) WHERE {
    ?media edugate:coversTopic ?topic .
    ?topic edugate:asString ?topicName .
} GROUP BY ?topic ?topicName
ORDER BY DESC(?count)
LIMIT 10
```

## Question 12

**Competency Question:** Which topics are broader than "Complexity"?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?broaderTopic ?broaderTopicName WHERE {
    <https://edugate.cs.wright.edu/lod/resource/Topic/Complexity> edugate:broaderThan ?broaderTopic .
    ?broaderTopic edugate:asString ?broaderTopicName .
}

```

## Question 13

**Competency Question:** What are the media resources linked to multiple topics?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?media ?mediaName (COUNT(?topic) AS ?count) WHERE {
    ?media rdf:type edugate:Media ;
           edugate:coversTopic ?topic ;
           edugate:hasTitle ?mediaName .
} GROUP BY ?media ?mediaName
HAVING (COUNT(?topic) > 1)
ORDER BY DESC(?count)
```

## Question 14

**Competency Question:** Which authors have contributed to multiple media resources?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>


SELECT ?author ?authorName (COUNT(?media) AS ?count) WHERE {
    ?media rdf:type edugate:Media ;
           edugate:hasAuthor ?author .

    ?author edugate:hasName ?authorName .
} GROUP BY ?author ?authorName
HAVING (COUNT(?media) > 1)
ORDER BY DESC(?count)
```

## Question 15

**Competency Question:** What are the most common relationships ?

**SPARQL Query:**

```sparql
SELECT ?predicate (COUNT(*) AS ?count) WHERE {
    ?s ?predicate ?o .
} GROUP BY ?predicate ORDER BY DESC(?count)
```

## Question 16

**Competency Question:** Which authors have co-authored the most media resources?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?author1 ?author1Name ?author2 ?author2Name (COUNT(?media) AS ?sharedPublications) WHERE {
    ?media rdf:type edugate:Media ;  # Ensure only media resources are counted
           edugate:hasAuthor ?author1, ?author2 .

    FILTER(?author1 != ?author2)  # Exclude self-pairs

    ?author1 edugate:hasName ?author1Name .
    ?author2 edugate:hasName ?author2Name .
} GROUP BY ?author1 ?author1Name ?author2 ?author2Name
ORDER BY DESC(?sharedPublications)
LIMIT 10

```

## Question 17

**Competency Question:** Which topics have the most cross-references?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?topic ?topicName (COUNT(?relatedTopic) AS ?crossReferences) WHERE {
    ?topic edugate:broaderThan|edugate:relatedTo ?relatedTopic .
    ?topic edugate:asString ?topicName .
} GROUP BY ?topic ?topicName
ORDER BY DESC(?crossReferences)
LIMIT 10
```

## Question 18

**Competency Question:** What are the "prerequisite chains" in learning paths?

**SPARQL Query:**

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX edugate: <https://edugate.cs.wright.edu/lod/resource/>

SELECT ?prerequisiteStep ?prerequisiteStepName ?nextStep ?nextStepName WHERE {
    ?prerequisiteStep edugate:hasNextLearningStep+ ?nextStep .

    ?prerequisiteStep edugate:asString ?prerequisiteStepName .
    ?nextStep edugate:asString ?nextStepName .
}
```
