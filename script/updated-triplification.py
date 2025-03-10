import re
import os
import pandas as pd
from rdflib import Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME

'''
Script Parameters

Please make sure to adjust the 
`output_name` to a befitting name
which does not accidentally overwrite
existing turtle files! 
'''
# Directory and File Parameters of Triplification run
data_path = "./data"
output_path = "./materialization"

data_path = os.path.join(data_path, "data-for-ns-okg.csv")
output_name = "new-schema-currkg.ttl"
output_path = os.path.join(output_path, output_name)

# Mapping of file extensions to RDF formats
EXTENSION_TO_FORMAT = {
    ".ttl": "turtle",
    ".rdf": "xml",
    ".xml": "xml",
    ".n3": "n3",
    ".nt": "nt",
    ".jsonld": "json-ld",
}


def infer_format(file_path):
    """Infer RDF format based on file extension."""
    _, ext = os.path.splitext(file_path)
    # Default to turtle if unknown
    return EXTENSION_TO_FORMAT.get(ext.lower(), "turtle")


#  Prefixes for KG
name_space = "https://edugate.cs.wright.edu/"
pfs = {
    "edu-r": Namespace(f"{name_space}lod/resource/"),
    "edu-ont": Namespace(f"{name_space}lod/ontology/"),
    "dbo": Namespace("http://dbpedia.org/ontology/"),
    "time": Namespace("http://www.w3.org/2006/time#"),
    "ssn": Namespace("http://www.w3.org/ns/ssn/"),
    "sosa": Namespace("http://www.w3.org/ns/sosa/"),
    "provo": Namespace("http://www.w3.org/ns/prov#"),
    "modl": Namespace("https://archive.org/services/purl/purl/modular_ontology_design_library/"),
    "cdt": Namespace("http://w3id.org/lindt/custom_datatypes#"),
    "ex": Namespace("https://example.com/"),
    "rdf": RDF,
    "rdfs": RDFS,
    "xsd": XSD,
    "owl": OWL,
    "time": TIME,
    "qudt": Namespace("http://qudt.org/schema/qudt/"),
}
# rdf:type shortcut
isA = pfs["rdf"]["type"]  # isA prefix/relationship
asString = pfs["edu-ont"]["asString"]  # type pattern
hasTitle = pfs["edu-ont"]["hasTitle"]
person_uri = pfs["edu-ont"]["Person"]


def sanitize_string(input_string, replace_with="X"):
    """
    Replaces special characters with a specified string and spaces with underscores.

    :param input_string: The input string to be sanitized.
    :param replace_with: The string to replace special characters with (default is empty string).
    :return: A sanitized string.
    """
    input_string = input_string.strip()  # Remove leading/trailing whitespace
    sanitized = re.sub(r'[^a-zA-Z0-9 ]', replace_with,
                       input_string)  # Replace special characters
    sanitized = sanitized.replace(" ", "_")  # Replace spaces with underscores
    return sanitized

#  Initialize KG


def init_kg(prefixes=pfs):

    kg = Graph()

    if os.path.exists(output_path):
        rdf_format = infer_format(output_path)
        print(
            f"Loading existing graph from {output_path} (format: {rdf_format})")
        kg.parse(output_path, format=rdf_format)
    else:
        print(f"Creating a new graph as {output_path} does not exist.")

    # Bind prefixes
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])

    return kg


with open(data_path, "r") as inputF:
    df = pd.read_csv(inputF)
    header = df.columns
    # print([col for col in header])


def triplify(s, p, o):
    '''
        Adds a (subject, predicate, object) triple to graph.

        s,p, and o should be rdflib terms
    '''
    try:
        global graph
        graph.add((s, p, o))
    except Exception as e:
        print(f"Error adding triple ({s}, {p}, {o}): {e}")


def get_column_value(row, column_name):
    '''
        Safely retrieves the value from a DataFrame row for a given column.
        Returns None if the column is missing or the value is NaN.
    '''
    value = row.get(column_name)
    if pd.notnull(value):
        return str(value).strip()
    else:
        return None


def dictionary_check(key, dictionary):
    '''
        Checks if dictionary already has key-value pairing.

        Returns already used index-value from dictionary or 
        creates a new one
    '''
    if key in dictionary:
        return dictionary[key]
    else:
        index = len(dictionary) + 1
        dictionary[key] = index
        return index


def dictionary_triples(elements, type, subject_uri, predicate):
    '''
        Creates triples for elements in a list using a shared dictionary.
    '''
    if not subject_uri:
        return
    for el in elements:
        el = el.strip()
        el_str = sanitize_string(el)
        el_uri = pfs["edu-r"][f"{type}/{el_str}"]
        triplify(el_uri, isA, pfs["edu-ont"][f"{type}"])
        triplify(el_uri, asString, Literal(f"{el}", datatype=XSD.string))
        triplify(subject_uri, pfs["edu-ont"][f"{predicate}"], el_uri)


def init_triplify():
    #  Media Mint + Typing
    for i, row in df.iterrows():
        module_uri = None
        media_uri = None
        curriculum_uri = None
        authors = []

        # Curriculum base information
        curriculum_title = get_column_value(row, 'Curriculum')
        if curriculum_title:
            curriculum_uri = pfs["edu-r"][f"Curriculum/{sanitize_string(curriculum_title)}"]
            triplify(curriculum_uri, isA, pfs["edu-ont"]["Curriculum"])
            triplify(curriculum_uri, hasTitle, Literal(
                curriculum_title, datatype=XSD.string))
        else:
            print(f"Row {i}: Missing or null 'Curriculum'")

        # Module Base Information
        module_title = get_column_value(row, 'Module Title')
        if module_title:
            module_uri = pfs["edu-r"][f"Module/{sanitize_string(module_title)}"]
            triplify(module_uri, isA, pfs["edu-ont"]["Module"])
            triplify(module_uri, hasTitle, Literal(
                module_title, datatype=XSD.string))

            if curriculum_uri:
                triplify(curriculum_uri, pfs["edu-ont"]
                         ["hasModule"], module_uri)
        else:
            print(f"Row {i}: Missing or null 'Module Title'")

        persona_uri = None
        # Persona Base Information
        persona_title = get_column_value(row, 'Persona')
        if persona_title:
            persona_uri = pfs["edu-r"][f"Persona/{sanitize_string(persona_title)}"]
            triplify(persona_uri, isA, pfs["edu-ont"]["Persona"])
            triplify(persona_uri, asString, Literal(
                persona_title, datatype=XSD.string))
            persona_type = get_column_value(row, 'Persona Type')

            if persona_type:
                triplify(persona_uri, pfs["edu-ont"]["hasType"],
                         Literal(persona_type, datatype=XSD.string))
            persona_role = get_column_value(row, 'Persona Role')

            if persona_role:
                triplify(persona_uri, pfs["edu-ont"]["hasRole"],
                         Literal(persona_role, datatype=XSD.string))

        else:
            print(f"Row {i}: Missing or null 'Persona'")

        # Learning Path Base Information
        learning_path = get_column_value(row, 'Learning Path')
        if learning_path:
            learning_path_uri = pfs["edu-r"][f"Learning_Path/{sanitize_string(learning_path)}"]
            triplify(learning_path_uri, isA, pfs["edu-ont"]["Learning_Path"])
            triplify(learning_path_uri, asString, Literal(
                learning_path, datatype=XSD.string))

            if persona_uri:
                triplify(persona_uri, pfs["edu-ont"]
                         ["determines"], learning_path_uri)

            if curriculum_uri:
                triplify(learning_path_uri,
                         pfs["edu-ont"]["scopedBy"], curriculum_uri)

            learning_steps = get_column_value(row, 'Learning Path')
            if learning_steps:
                steps = [s.strip() for s in learning_steps.split(',')]
                for index, step in enumerate(steps):
                    step_uri = pfs[
                        "edu-r"][f"Learning_Path/Learning_Step/{sanitize_string(step)}"]
                    triplify(step_uri, isA, pfs["edu-ont"]["Learning_Step"])
                    triplify(step_uri, asString, Literal(
                        step, datatype=XSD.string))
                    referencing_module_uri = pfs["edu-r"][f"Module/{sanitize_string(step)}"]
                    triplify(step_uri, pfs["edu-ont"]
                             ["refersTo"], referencing_module_uri)

                    if index != 0:
                        prev_step_uri = pfs[
                            "edu-r"][f"Learning_Path/Learning_Step/{sanitize_string(steps[index-1])}"]
                        triplify(step_uri, pfs["edu-ont"]
                                 ["hasPreviousLearningStep"], prev_step_uri)
                    else:
                        triplify(step_uri, isA,
                                 pfs["edu-ont"]["First_Learning_Step"])

                    if index != len(steps) - 1:
                        next_step_uri = pfs[
                            "edu-r"][f"Learning_Path/Learning_Step/{sanitize_string(steps[index+1])}"]
                        triplify(step_uri, pfs["edu-ont"]
                                 ["hasNextLearningStep"], next_step_uri)
                    else:
                        triplify(step_uri, isA,
                                 pfs["edu-ont"]["Last_Learning_Step"])

                    triplify(learning_path_uri,
                             pfs["edu-ont"]["hasLearningSteps"], step_uri)

        else:
            print(f"Row {i}: Missing or null 'Learning Path'")

        # Handle Module Category
        category_str = get_column_value(row, 'Module Category')
        if category_str and module_uri:
            module_categories = [c.strip() for c in category_str.split(',')]
            dictionary_triples(module_categories, "Category",
                               module_uri, "belongsToCategory")
        elif category_str:
            module_categories = [c.strip() for c in category_str.split(',')]
            for mc in module_categories:
                mc_uri = pfs["edu-r"][f"Category/{sanitize_string(mc)}"]
                triplify(mc_uri, isA, pfs["edu-ont"]["Category"])
                triplify(mc_uri, asString, Literal(
                    f"{mc}", datatype=XSD.string))
        else:
            print(
                f"Row {i}: Missing or null 'Module Category' or 'Module Title'")

        #  Level
        module_level_str = get_column_value(row, 'Module Level')
        if module_level_str and module_uri:
            levels = [a.strip() for a in module_level_str.split(',')]
            dictionary_triples(levels, "Level", module_uri, "hasLevel")
        else:
            print(f"Row {i}: Missing or null 'Module Level' or 'Module Title'")

        #  Media base information
        media_title = get_column_value(row, 'Media Title')
        media_link = get_column_value(row, 'Media Link')
        if media_title and media_link:
            media_uri = pfs["edu-r"][f"Media/{sanitize_string(media_title)}"]
            triplify(media_uri, isA, pfs["edu-ont"]["Media"])
            triplify(media_uri, hasTitle, Literal(
                media_title, datatype=XSD.string))
            triplify(media_uri, pfs["edu-ont"]["hasMediaSourceLink"],
                     Literal(media_link, datatype=XSD.string))

            if module_uri:
                triplify(module_uri, pfs["edu-ont"]["references"], media_uri)
        else:
            print(f"Row {i}: Missing or null 'Media Title' or 'Media Link'")

        #  Author base information
        authors_str = get_column_value(row, 'Author')
        if authors_str:
            authors = [author.strip() for author in authors_str.split(',')]
            for author in authors:
                author_uri = pfs["edu-r"][f"Author/{sanitize_string(author)}"]
                triplify(author_uri, isA, pfs["edu-ont"]["Author"])
                triplify(author_uri, pfs["edu-ont"]["hasName"], Literal(
                    author, datatype=XSD.string))

                # Media with Author
                if media_uri:
                    triplify(media_uri, pfs["edu-ont"]
                             ["hasAuthor"], author_uri)
        else:
            print(f"Row {i}: Missing or null 'Author'")

        # Event Base Information
        event_title = get_column_value(row, 'Event')
        if event_title:
            event_uri = pfs["edu-r"][f"Event/{sanitize_string(event_title)}"]
            triplify(event_uri, isA, pfs["edu-ont"]["Event"])
            triplify(event_uri, asString, Literal(
                event_title, datatype=XSD.string))

            # Event with Event Type
            event_type = get_column_value(row, 'Event Type')
            if event_type:
                triplify(event_uri, isA, Literal(
                    event_type.strip(), datatype=XSD.string))

            # Media with Event
            if media_uri:
                triplify(media_uri, pfs["edu-ont"]["providedBy"], event_uri)

            # Event with Sub Events
            sub_events_str = get_column_value(row, 'Sub Events')
            if sub_events_str:
                sub_events = [s.strip() for s in sub_events_str.split(',')]
                for sub_event in sub_events:
                    sub_event_uri = pfs["edu-r"][f"Event/{sanitize_string(sub_event)}"]
                    triplify(sub_event_uri, isA, pfs["edu-ont"]["Event"])
                    triplify(sub_event_uri, asString, Literal(
                        sub_event, datatype=XSD.string))
                    triplify(event_uri, pfs["edu-ont"]
                             ["hasSubEvent"], sub_event_uri)

        # Media with Typing
        format_str = get_column_value(row, 'Media Type')
        if format_str and media_uri:
            types = [f.strip() for f in format_str.split(',')]
            for type in types:
                type = sanitize_string(type)
                type_uri = pfs["edu-ont"][type]
                triplify(media_uri, isA, type_uri)
        else:
            print(f"Row {i}: Missing or null 'Media Type' or 'Media'")

        # Module with Topic
        mod_topic_covered_str = get_column_value(row, 'Module Topics Covered')
        if mod_topic_covered_str:
            topics = [t.strip() for t in mod_topic_covered_str.split(',')]
            if module_uri:
                dictionary_triples(topics, "Topic", module_uri, "coversTopic")
        else:
            print(f"Row {i}: Missing Module or null 'Module Topics Covered'")

        # Media with Topic
        media_topic_covered_str = get_column_value(row, 'Media Topics Covered')
        if media_topic_covered_str:
            topics = [t.strip() for t in media_topic_covered_str.split(',')]
            if media_uri:
                dictionary_triples(topics, "Topic", media_uri, "coversTopic")
        else:
            print(f"Row {i}: Missing media or null 'Media Topic Covered'")

        # Topic Relations
        topic = get_column_value(row, 'Topic')
        if topic:
            topic_uri = pfs["edu-r"][f"Topic/{sanitize_string(topic)}"]
            triplify(topic_uri, isA, pfs["edu-ont"]["Topic"])
            triplify(topic_uri, asString, Literal(topic, datatype=XSD.string))

            # Broader Topics
            broader_topics_str = get_column_value(row, 'Broader Topics')
            if broader_topics_str:
                broader_topics = [t.strip()
                                  for t in broader_topics_str.split(',')]
                for broader_topic in broader_topics:
                    broader_topic_uri = pfs["edu-r"][f"Topic/{sanitize_string(broader_topic)}"]
                    triplify(broader_topic_uri, isA, pfs["edu-ont"]["Topic"])
                    triplify(broader_topic_uri, asString, Literal(
                        broader_topic, datatype=XSD.string))
                    triplify(broader_topic_uri,
                             pfs["edu-ont"]["broaderThan"], topic_uri)

            # Narrower Topics
            narrower_topics_str = get_column_value(row, 'Narrower Topics')
            if narrower_topics_str:
                narrower_topics = [t.strip()
                                   for t in narrower_topics_str.split(',')]
                for narrower_topic in narrower_topics:
                    narrower_topic_uri = pfs["edu-r"][f"Topic/{sanitize_string(narrower_topic)}"]
                    triplify(narrower_topic_uri, isA, pfs["edu-ont"]["Topic"])
                    triplify(narrower_topic_uri, asString, Literal(
                        narrower_topic, datatype=XSD.string))
                    triplify(narrower_topic_uri,
                             pfs["edu-ont"]["narrowerThan"], topic_uri)
        else:
            print(f"Row {i}: Missing or null 'Topic Relations'")

        #  Audience
        audience_str = get_column_value(row, 'Audience')
        if audience_str and media_uri:
            audiences = [a.strip() for a in audience_str.split(',')]
            dictionary_triples(audiences, "Audience",
                               media_uri, "hasRecommendedAudience")
        else:
            print(f"Row {i}: Missing or null 'Audience' or 'Media Title'")

        #  Language
        language_str = get_column_value(row, 'Language')
        if language_str and media_uri:
            languages = [l.strip() for l in language_str.split(',')]
            if media_uri:
                dictionary_triples(languages, "Language",
                                   media_uri, "supportsLanguage")
        else:
            print(f"Row {i}: Missing or null 'Language' or 'Media'")

    # Add Person to Persona ontology graph
    graph.add((person_uri, pfs["edu-ont"]
              ["assumesRole"], pfs["edu-ont"]["Persona"]))

    print("Graph Created")


def main():
    init_triplify()

    # Serialize the graph
    graph.serialize(format="turtle", encoding="utf-8", destination=output_path)

    print("Graph Serialized")


graph = init_kg()
main()
