"""
Convert the curriculum CSV export into RDF triples.

This script is intentionally verbose and heavily commented so that someone
who is new to Python, RDFLib, or this repository can still follow the flow.

High-level workflow:
1. Read a CSV file into a pandas DataFrame.
2. Create or load an RDF graph.
3. Walk row-by-row through the spreadsheet.
4. Turn each row into CurriculumKG resources and relationships.
5. Save the graph as a Turtle file.

Important:
- The default output file is `new-schema-currkg.ttl`.
- If you do not want to append to or overwrite an existing RDF file, change
  the `--output` argument when running the script.
- The script expects to be run from inside the `script/` directory unless you
  pass explicit file paths for `--input-data`, `--current-file`, and `--output`.
"""

import re
import os
import pandas as pd
from rdflib import Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
import argparse

# `df` is filled in `main()` after the CSV is loaded.
# It stays global because the original script structure expects helper
# functions like `init_triplify()` to read from a shared DataFrame.
df = None

# Default Script input/output names for a triplification run.
# These can all be overridden from the command line.
data_input_name = "data-okg.csv"
output_name = "new-schema-currkg.ttl"
data_path = os.path.join("./data", data_input_name)
current_file_path = output_path = os.path.join(
    "./materialization", output_name)

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
    """Infer the RDF serialization format from the file extension."""
    _, ext = os.path.splitext(file_path)
    # Turtle is the safest default for this repository because all
    # generated instance-data examples currently use `.ttl`.
    return EXTENSION_TO_FORMAT.get(ext.lower(), "turtle")


# Namespace and prefix setup for the knowledge graph.
# `pfs` acts as a small registry so the rest of the script can build URIs
# without hardcoding the base namespace over and over again.
name_space = "https://edugate.cs.wright.edu/"
pfs = {
    "edu-r": Namespace(f"{name_space}lod/resource/"),
    "edu-ont": Namespace(f"{name_space}lod/ontology/"),
    "dbo": Namespace("http://dbpedia.org/ontology/"),
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

# Common URI shortcuts used throughout the script.
# These make the row-mapping logic easier to read.
# rdf:type shortcut
isA = pfs["rdf"]["type"]  # isA prefix/relationship
asString = pfs["edu-ont"]["asString"]  # type pattern
hasTitle = pfs["edu-ont"]["hasTitle"]
person_uri = pfs["edu-ont"]["Person"]


def sanitize_string(input_string, replace_with="X"):
    """
    Convert free-text values into URI-safe fragments.

    Why this exists:
    - CSV values can contain spaces, punctuation, slashes, and other
      characters that are awkward in RDF resource identifiers.
    - The script uses the sanitized value as part of the URI local name.

    Example:
    "Data Science / AI" -> "Data_Science_X_AI"

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
    """
    Create the RDF graph used by the script.

    If the target file already exists, we load it first so a run can extend an
    existing graph instead of always starting from an empty one.
    """

    kg = Graph()

    if os.path.exists(current_file_path):
        rdf_format = infer_format(current_file_path)
        print(
            f"Loading existing graph from {current_file_path} (format: {rdf_format})")
        kg.parse(current_file_path, format=rdf_format)
    else:
        print(f"Creating a new graph as {output_path} does not exist.")

    # Bind prefixes
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])

    return kg


def triplify(s, p, o):
    """
    Add one RDF triple to the graph.

    The parameters should already be RDFLib terms:
    - `s`: subject
    - `p`: predicate
    - `o`: object

    This helper centralizes the `graph.add(...)` call so any future logging or
    validation can be added in one place.
    
    s,p, and o should be rdflib terms (URIRef, Literal, BNode) that are ready to be added to the graph.
    """
    try:
        global graph
        graph.add((s, p, o))
    except Exception as e:
        print(f"Error adding triple ({s}, {p}, {o}): {e}")


def get_column_value(row, column_name):
    """
    Safely read a value from a pandas Dataframe row for a given column.

    Returning `None` for missing/blank or NaN values keeps the main mapping logic
    straightforward because each block can simply check `if value:`.
    """
    value = row.get(column_name)
    if pd.notnull(value):
        return str(value).strip()
    else:
        return None


def dictionary_check(key, dictionary): 
    """
    Checks if dictionary already has key-value pairing.
    Returns already used index-value from dictionary or creates a new one, a stable integer ID for a dictionary key.
        
    This helper is currently unused, but it has been kept because it may be
    useful for future numbered-resource generation or deterministic indexing.
    """
    if key in dictionary:
        return dictionary[key]
    else:
        index = len(dictionary) + 1
        dictionary[key] = index
        return index


def dictionary_triples(elements, type, subject_uri, predicate):
    """
    Creates triples for elements in a set of typed resources from a comma-separated list using a shared dictionary.

    Example:
    - If a module has categories `AI, Ethics`
    - this helper creates the `Category.*` resources
    - and links the module to each category with the requested predicate.
    """
    if not subject_uri:
        return
    for el in elements:
        el = el.strip()
        el_str = sanitize_string(el)
        el_uri = pfs["edu-r"][f"{type}.{el_str}"]
        triplify(el_uri, isA, pfs["edu-ont"][f"{type}"])
        triplify(el_uri, asString, Literal(f"{el}", datatype=XSD.string))
        triplify(subject_uri, pfs["edu-ont"][f"{predicate}"], el_uri)


def init_triplify():
    """
    Walk through the loaded DataFrame and materialize all supported entities.

    The script processes one CSV row at a time. Each row can contribute:
    - curriculum metadata
    - module metadata
    - persona and learning-path information
    - media resources and authors
    - events and sub-events
    - topics, languages, audience, levels, and categories
    """
    #  Media Mint + Typing
    for i, row in df.iterrows():
        # Reset row-scoped URIs for each CSV record so resources do not leak
        # across iterations.
        module_uri = None
        media_uri = None
        curriculum_uri = None
        authors = []

        # Curriculum base information.
        # Every row can atleast belong to one curriculum.
        curriculum_title = get_column_value(row, 'Curriculum')
        if curriculum_title:
            curriculum_uri = pfs["edu-r"][f"Curriculum.{sanitize_string(curriculum_title)}"]
            triplify(curriculum_uri, isA, pfs["edu-ont"]["Curriculum"])
            triplify(curriculum_uri, hasTitle, Literal(
                curriculum_title, datatype=XSD.string))
        else:
            print(f"Row {i}: Missing or null 'Curriculum'")

        # Module base information.
        # Modules are one of the main anchors in the KG because media, topics,
        # and learning steps often point back to them.
        module_title = get_column_value(row, 'Module Title')
        if module_title:
            module_uri = pfs["edu-r"][f"Module.{sanitize_string(module_title)}"]
            triplify(module_uri, isA, pfs["edu-ont"]["Module"])
            triplify(module_uri, hasTitle, Literal(
                module_title, datatype=XSD.string))

            if curriculum_uri:
                triplify(curriculum_uri, pfs["edu-ont"]
                         ["hasModule"], module_uri)
        else:
            print(f"Row {i}: Missing or null 'Module Title'")

        persona_uri = None
        # Persona base information.
        # Personas let the KG describe different target learners or users.
        persona_title = get_column_value(row, 'Persona')
        if persona_title:
            persona_uri = pfs["edu-r"][f"Persona.{sanitize_string(persona_title)}"]
            triplify(persona_uri, isA, pfs["edu-ont"]["Persona"])
            triplify(persona_uri, asString, Literal(
                persona_title, datatype=XSD.string))
            persona_type = get_column_value(row, 'Persona Type')

            if persona_type:
                persona_type_uri = pfs["edu-r"][f"PersonaType.{sanitize_string(persona_type)}"]
                triplify(persona_type_uri, isA, pfs["edu-ont"]["PersonaType"])
                triplify(persona_uri, pfs["edu-ont"]
                         ["hasType"], persona_type_uri)
                triplify(persona_type_uri, asString, Literal(
                    persona_type, datatype=XSD.string))

            persona_profession = get_column_value(row, 'Persona Profession')

            if persona_profession:
                persona_profession_uri = pfs[
                    "edu-r"][f"Profession.{sanitize_string(persona_profession)}"]
                triplify(persona_profession_uri, isA,
                         pfs["edu-ont"]["Profession"])
                triplify(persona_uri, pfs["edu-ont"]
                         ["hasProfession"], persona_profession_uri)
                triplify(persona_profession_uri, asString, Literal(
                    persona_profession, datatype=XSD.string))

        else:
            print(f"Row {i}: Missing or null 'Persona'")

        # Learning path information.
        # The same CSV column is used both as the path label and as the list of
        # ordered learning steps. This means the field should contain a
        # comma-separated sequence in the desired order.
        learning_path = get_column_value(row, 'Learning Path')
        if learning_path:
            learning_path_uri = pfs["edu-r"][f"LearningPath.{sanitize_string(learning_path)}"]
            triplify(learning_path_uri, isA, pfs["edu-ont"]["LearningPath"])
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
                    # Each step gets its own URI inside the parent learning
                    # path namespace so the order can be expressed explicitly.
                    step_uri = pfs[
                        "edu-r"][f"LearningPath.{sanitize_string(learning_path)}.LearningStep.{sanitize_string(step)}"]
                    triplify(step_uri, isA, pfs["edu-ont"]["LearningStep"])
                    triplify(step_uri, asString, Literal(
                        step, datatype=XSD.string))
                    referencing_module_uri = pfs["edu-r"][f"Module.{sanitize_string(step)}"]
                    triplify(step_uri, pfs["edu-ont"]
                             ["refersTo"], referencing_module_uri)

                    if index != 0:
                        prev_step_uri = pfs[
                            "edu-r"][f"LearningPath.{sanitize_string(learning_path)}.LearningStep.{sanitize_string(steps[index-1])}"]
                        triplify(step_uri, pfs["edu-ont"]
                                 ["hasPreviousLearningStep"], prev_step_uri)
                    else:
                        triplify(step_uri, isA,
                                 pfs["edu-ont"]["FirstLearningStep"])

                    if index != len(steps) - 1:
                        next_step_uri = pfs[
                            "edu-r"][f"LearningPath.{sanitize_string(learning_path)}.LearningStep.{sanitize_string(steps[index+1])}"]
                        triplify(step_uri, pfs["edu-ont"]
                                 ["hasNextLearningStep"], next_step_uri)
                    else:
                        triplify(step_uri, isA,
                                 pfs["edu-ont"]["LastLearningStep"])

                    triplify(learning_path_uri,
                             pfs["edu-ont"]["hasLearningStep"], step_uri)

        else:
            print(f"Row {i}: Missing or null 'Learning Path'")

        # Module categories.
        # If there is no module URI for the row, we still materialize the
        # category resources, but there is nothing to link them to.
        category_str = get_column_value(row, 'Module Category')
        if category_str and module_uri:
            module_categories = [c.strip() for c in category_str.split(',')]
            dictionary_triples(module_categories, "Category",
                               module_uri, "belongsTo")
        elif category_str:
            module_categories = [c.strip() for c in category_str.split(',')]
            for mc in module_categories:
                mc_uri = pfs["edu-r"][f"Category.{sanitize_string(mc)}"]
                triplify(mc_uri, isA, pfs["edu-ont"]["Category"])
                triplify(mc_uri, asString, Literal(
                    f"{mc}", datatype=XSD.string))
        else:
            print(
                f"Row {i}: Missing or null 'Module Category' or 'Module Title'")

        # Module difficulty or level labels.
        module_level_str = get_column_value(row, 'Module Level')
        if module_level_str and module_uri:
            levels = [a.strip() for a in module_level_str.split(',')]
            dictionary_triples(levels, "Level", module_uri, "hasLevel")
        else:
            print(f"Row {i}: Missing or null 'Module Level' or 'Module Title'")

        # Media base information.
        # A media record needs both a title and a source link to be useful.
        media_title = get_column_value(row, 'Media Title')
        media_link = get_column_value(row, 'Media Link')
        if media_title and media_link:
            media_uri = pfs["edu-r"][f"Media.{sanitize_string(media_title)}"]
            triplify(media_uri, isA, pfs["edu-ont"]["Media"])
            triplify(media_uri, hasTitle, Literal(
                media_title, datatype=XSD.string))
            triplify(media_uri, pfs["edu-ont"]["hasMediaSourceLink"],
                     Literal(media_link, datatype=XSD.string))

            if module_uri:
                triplify(module_uri, pfs["edu-ont"]["references"], media_uri)
        else:
            print(f"Row {i}: Missing or null 'Media Title' or 'Media Link'")

        # Author information.
        # Multiple authors are expected to be stored as comma-separated values.
        authors_str = get_column_value(row, 'Author')
        if authors_str:
            authors = [author.strip() for author in authors_str.split(',')]
            for author in authors:
                author_uri = pfs["edu-r"][f"Author.{sanitize_string(author)}"]
                triplify(author_uri, isA, pfs["edu-ont"]["Author"])
                triplify(author_uri, pfs["edu-ont"]["hasName"], Literal(
                    author, datatype=XSD.string))

                # Media with Author
                if media_uri:
                    triplify(media_uri, pfs["edu-ont"]
                             ["hasAuthor"], author_uri)

                # Add Person to Author ontology graph
                graph.add(
                    (person_uri, pfs["edu-ont"]["assumesAuthorship"], pfs["edu-ont"]["Author"]))
        else:
            print(f"Row {i}: Missing or null 'Author'")

        # Event base information.
        # Events can provide media and can also contain sub-events.
        event_title = get_column_value(row, 'Event')
        if event_title:
            event_uri = pfs["edu-r"][f"Event.{sanitize_string(event_title)}"]
            triplify(event_uri, isA, pfs["edu-ont"]["Event"])
            # Todo: Add event title relationship
            triplify(event_uri, asString, Literal(
                event_title, datatype=XSD.string))

            # Event with Event Type
            # Todo: Add event type relationship
            event_type = get_column_value(row, 'Event Type')
            if event_type:
                triplify(event_uri, isA, Literal(
                    event_type.strip(), datatype=XSD.string))

            # Media with Event
            if media_uri:
                triplify(event_uri, pfs["edu-ont"]["provides"], media_uri)

            # Event with Sub Events
            sub_events_str = get_column_value(row, 'Sub Events')
            if sub_events_str:
                sub_events = [s.strip() for s in sub_events_str.split(',')]
                for sub_event in sub_events:
                    sub_event_uri = pfs["edu-r"][f"Event.{sanitize_string(sub_event)}"]
                    triplify(sub_event_uri, isA, pfs["edu-ont"]["Event"])
                    triplify(sub_event_uri, asString, Literal(
                        sub_event, datatype=XSD.string))
                    triplify(event_uri, pfs["edu-ont"]
                             ["hasSubEvent"], sub_event_uri)

        # Media typing.
        # The ontology treats each media type as a class and asserts that the
        # media instance is also of that class.
        format_str = get_column_value(row, 'Media Type')
        if format_str and media_uri:
            types = [f.strip() for f in format_str.split(',')]
            for type in types:
                type = sanitize_string(type)
                type_uri = pfs["edu-ont"][type]
                triplify(media_uri, isA, type_uri)
                triplify(type_uri, asString, Literal(
                    format_str, datatype=XSD.string))
        else:
            print(f"Row {i}: Missing or null 'Media Type' or 'Media'")

        # Topics covered by a module.
        mod_topic_covered_str = get_column_value(row, 'Module Topics Covered')
        if mod_topic_covered_str:
            topics = [t.strip() for t in mod_topic_covered_str.split(',')]
            if module_uri:
                dictionary_triples(topics, "Topic", module_uri, "coversTopic")
        else:
            print(f"Row {i}: Missing Module or null 'Module Topics Covered'")

        # Topics covered by a media item.
        media_topic_covered_str = get_column_value(row, 'Media Topics Covered')
        if media_topic_covered_str:
            topics = [t.strip() for t in media_topic_covered_str.split(',')]
            if media_uri:
                dictionary_triples(topics, "Topic", media_uri, "coversTopic")
        else:
            print(f"Row {i}: Missing media or null 'Media Topic Covered'")

        # Topic Relations
        # This lets the graph represent broader/narrower topic structure.
        topic = get_column_value(row, 'Topic')
        if topic:
            topic_uri = pfs["edu-r"][f"Topic.{sanitize_string(topic)}"]
            triplify(topic_uri, isA, pfs["edu-ont"]["Topic"])
            triplify(topic_uri, asString, Literal(topic, datatype=XSD.string))

            # Broader Topics
            broader_topics_str = get_column_value(row, 'Broader Topics')
            if broader_topics_str:
                broader_topics = [t.strip()
                                  for t in broader_topics_str.split(',')]
                for broader_topic in broader_topics:
                    broader_topic_uri = pfs["edu-r"][f"Topic.{sanitize_string(broader_topic)}"]
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
                    narrower_topic_uri = pfs["edu-r"][f"Topic.{sanitize_string(narrower_topic)}"]
                    triplify(narrower_topic_uri, isA, pfs["edu-ont"]["Topic"])
                    triplify(narrower_topic_uri, asString, Literal(
                        narrower_topic, datatype=XSD.string))
                    triplify(narrower_topic_uri,
                             pfs["edu-ont"]["narrowerThan"], topic_uri)
        else:
            print(f"Row {i}: Missing or null 'Topic Relations'")

        # Recommended audience for a media item.
        audience_str = get_column_value(row, 'Audience')
        if audience_str and media_uri:
            audiences = [a.strip() for a in audience_str.split(',')]
            dictionary_triples(audiences, "Audience",
                               media_uri, "hasRecommended")
        else:
            print(f"Row {i}: Missing or null 'Audience' or 'Media Title'")

        # Language labels for a media item.
        language_str = get_column_value(row, 'Language')
        if language_str and media_uri:
            languages = [l.strip() for l in language_str.split(',')]
            if media_uri:
                dictionary_triples(languages, "Language",
                                   media_uri, "hasLanguage")
        else:
            print(f"Row {i}: Missing or null 'Language' or 'Media'")

    # Add Person to Persona ontology graph
    graph.add((person_uri, pfs["edu-ont"]
              ["assumesPersona"], pfs["edu-ont"]["Persona"]))

    print("Graph Created")


def main():
    """
    Parse command-line arguments, load the CSV, and write the RDF graph.

    Example:
        python updated-triplification.py \
            --input-data ./data/data-okg.csv \
            --current-file ./materialization/new-schema-currkg.ttl \
            --output ./materialization/new-schema-currkg.ttl
    """

    global data_path
    global output_path
    global current_file_path

    parser = argparse.ArgumentParser(
        description="Materialize CurriculumKG RDF triples from a CSV file."
    )
    parser.add_argument(
        "--input-data", help="The CSV File to use for materialization", default=data_path)
    parser.add_argument(
        "--current-file", help="The current file which has the graph", default=current_file_path)
    parser.add_argument("--output", help="The output file to save the graph to",
                        default=output_path)
    args = parser.parse_args()

    data_path = args.input_data
    current_file_path = args.current_file
    output_path = args.output

    # Load the CSV once and keep it available globally for the row-mapping
    # helper. This matches the original script structure and keeps the rest of
    # the file unchanged.
    with open(data_path, "r") as inputF:
        global df
        # Read the CSV file into a DataFrame
        df = pd.read_csv(inputF)
        header = df.columns
        # print([col for col in header])

    # Make sure the destination directory exists before trying to write the
    # serialized graph to disk.
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Start triplification
    # Create triples from the loaded CSV rows.
    init_triplify()

    # Serialize the graph to a file in the specified format (default is Turtle).
    graph.serialize(format="turtle", encoding="utf-8", destination=output_path)

    print("Graph Serialized")
    print(f"Graph saved to {output_path}")
    # Print the number of triples in the graph
    print(f"Number of triples in the graph: {len(graph)}")


graph = init_kg()
if __name__ == "__main__":
    # The import guard prevents the script from running automatically if it is
    # imported from another Python file for testing or reuse.
    main()
