# Key Notions

* Author
    * Rationale: Representing the Authors of different articles and are tied to a string with "hasName"
    * Connected Pattern: Agent Role, Role Dependent Name (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/agentrole
        * https://archive.org/services/purl/domain/modular_ontology_design_library/role-dependent-name
    * Source Dataset(s): dssr, The KGC Open Knowledge Graph Curriculum

* Category
    * Rationale: Represents the different categories of the modules in the curriculum. 
    * Connected Pattern: Part Whole (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/PartWhole
    * Source Dataset(s): dssr

* Curriculum
    * Rationale: Represents the set of modules that is scoped by the LearningPath of each Persona and is tied to a title that indicates the source of that curriculum.
    * Connected Pattern: NameStub (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/namestub
    * Source Dataset(s): The KGC Open Knowledge Graph Curriculum

* Event
    * Rationale: Represents the Media provided as form of delivery of educational content that is presentations, tutorials, videos etc.
    * Connected Pattern: Event (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/event
    * Source Dataset(s): The KGC Open Knowledge Graph Curriculum

* LearningStep
    * Rationale: Represents the set of learning steps the individual has to take in order to follow their personal learning path.
    * Connected Pattern: Reccurent Event (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/recurrentevent
    * Source Dataset(s): dssr, The KGC Open Knowledge Graph Curriculum

* Level
    * Rationale: Represents the level of the modules that are delivered; wherether thet are foundational etc.
    * Connected Pattern: Explicit Typing (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/explicittyping
    * Source Dataset(s): open kg

* Media
    * Rationale: Represents the set of the media types that cover a specific topic of the curriculum.
    * Connected Pattern: Reporting-Event (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/reporting-event
    * Source Dataset(s): dssr, The KGC Open Knowledge Graph Curriculum

* Module
    * Rationale: Represents the different modules the curriculum is divided into.
    * Connected Pattern: PartWhole (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/PartWhole
    * Source Dataset(s): dssr, The KGC Open Knowledge Graph Curriculum

* Person
    * Rationale: Represents the individual that in intenting to learn through the curriculum and that will be assuming a persona or an author in order to get a relevant learning path depending on the context.
    * Connected Pattern: Role-Dependent-Name (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/role-dependent-name
    * Source Dataset(s): -

* Persona
    * Rationale: Represents the "category" the individual "falls in" in terms of end goal in their learning journey and relative background.
    * Connected Pattern: Role-Dependent-Name (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/role-dependent-name
    * Source Dataset(s): -

* Topic
    * Rationale: Represents the topic covered by a given module that can be narrower or browder depending on given learning step and level.
    * Connected Pattern: Reccurent Event (Modular Ontology Design Library (MODL))
        * https://archive.org/services/purl/domain/modular_ontology_design_library/recurrentevent
    * Data Source(s): dssr, The KGC Open Knowledge Graph Curriculum




