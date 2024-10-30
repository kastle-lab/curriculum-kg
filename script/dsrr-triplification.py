import os
import pandas as pd
import rdflib
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib import OWL, RDF, RDFS, XSD, TIME
import pandas as pd

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

filename = os.path.join(data_path, "data-for-demo-OKG.csv")
output_name = "dsrr-triples-okg.ttl"

#  Prefixes for KG
name_space = "https://edugate.cs.wright.edu/"
pfs = {
    "edu-r": Namespace(f"{name_space}lod/resource"),
    "edu-ont": Namespace(f"{name_space}lod/resource"),
    "dbo": Namespace("http://dbpedia.org/ontology/"),
    "time": Namespace("http://www.w3.org/2006/time#"),
    "ssn": Namespace("http://www.w3.org/ns/ssn/"),
    "sosa": Namespace("http://www.w3.org/ns/sosa/"),
    "provo": Namespace("http://www.w3.org/ns/prov#"),
    "modl": Namespace("https://archive.org/services/purl/purl/modular_ontology_design_library"),
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

#  Initialize KG


def init_kg(prefixes=pfs):
    kg = Graph()
    for prefix in pfs:
        kg.bind(prefix, pfs[prefix])
    return kg


with open(filename, "r") as inputF:
    df = pd.read_csv(inputF)
    header = df.columns
    # print([col for col in header])


# Adjust array if new role provides SpeakerRole
SpeakerRoleFormats = ['Podcast', 'Video']
speakerrole_uri = pfs["edu-ont"]["SpeakerRole"]
contributorrole_uri = pfs["edu-ont"]["ContributorRole"]
# Helper Dictionaries to make Unique Entries
author_dict = dict()
topic_dict = dict()
audience_dict = dict()
language_dict = dict()
modules_dict = dict()
media_dict = dict()
module_category_dict = dict()
curriculum_dict = dict()


def triplify(s, p, o):
    '''
        Adds a (subject, predicate, object) triple to graph.

        s,p, and o should be rdflib terms
    '''
    try:
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


def dictionary_triples(elements, type, dictionary, subject_uri, predicate):
    '''
        Creates triples for elements in a list using a shared dictionary.
    '''
    if not subject_uri:
        return
    for el in elements:
        el = el.strip()
        index = dictionary_check(el, dictionary)
        el_uri = pfs["edu-ont"][f"{type}{index}"]
        triplify(el_uri, isA, pfs["edu-ont"][f"{type}"])
        triplify(el_uri, asString, Literal(f"{el}", datatype=XSD.string))
        triplify(subject_uri, pfs["edu-ont"][f"{predicate}"], el_uri)


def init_triplify():
    '''

    '''
    #  Media Mint + Typing
    for i, row in df.iterrows():
        module_uri = None
        media_uri = None
        curriculum_uri = None
        authors = []

        # Curriculum base information
        curriculum_title = get_column_value(row, 'Curriculum')
        if curriculum_title:
            curriculum_index = dictionary_check(
                curriculum_title, curriculum_dict)
            curriculum_uri = pfs["edu-r"][f"Curriculum{curriculum_index}"]
            triplify(curriculum_uri, isA, pfs["edu-ont"]["Curriculum"])
            triplify(curriculum_uri, asString, Literal(
                curriculum_title, datatype=XSD.string))
        else:
            print(f"Row {i}: Missing or null 'Curriculum'")

        # Module Base Information
        module_title = get_column_value(row, 'Module Title')
        if module_title:
            module_index = dictionary_check(module_title, modules_dict)
            module_uri = pfs["edu-r"][f"Module{module_index}"]
            triplify(module_uri, isA, pfs["edu-ont"]["Module"])
            triplify(module_uri, asString, Literal(
                module_title, datatype=XSD.string))

            # Module with ContributorRole
            triplify(
                module_uri, pfs["edu-ont"]["providesParticipantRole"], contributorrole_uri)
            if curriculum_uri:
                triplify(curriculum_uri, pfs["edu-ont"]
                         ["hasModule"], module_uri)
        else:
            print(f"Row {i}: Missing or null 'Module Title'")

        #  Author base information
        authors_str = get_column_value(row, 'Author')
        if authors_str:
            authors = [author.strip() for author in authors_str.split(',')]
            for author in authors:
                index = dictionary_check(author, author_dict)
                author_uri = pfs["edu-ont"][f"Author{index}"]
                triplify(author_uri, isA, pfs["edu-ont"]["Author"])
                triplify(author_uri, asString, Literal(
                    author, datatype=XSD.string))
                # Author as SpeakerRole
                triplify(author_uri, pfs["edu-ont"]
                         ["assumesRole"], speakerrole_uri)

                # Author as ContributorRole
                triplify(author_uri, pfs["edu-ont"]
                         ["assumesRole"], contributorrole_uri)
        else:
            print(f"Row {i}: Missing or null 'Author'")

        #  Media base information
        media_title = get_column_value(row, 'Media Title')
        media_link = get_column_value(row, 'Media Link')
        if media_title and media_link:
            key = f"{media_title}{dictionary_check(
                authors[0].strip(), author_dict)}" if authors else media_title
            index = dictionary_check(key, media_dict)
            media_uri = pfs["edu-r"][f"Media{index}"]
            triplify(media_uri, isA, pfs["edu-ont"]["Media"])
            triplify(media_uri, asString, Literal(
                media_title, datatype=XSD.string))
            triplify(media_uri, pfs["edu-ont"]["hasLink"],
                     Literal(media_link, datatype=XSD.string))

            # Media with ContributorRole
            triplify(media_uri, pfs["edu-ont"]
                     ["providesParticipantRole"], contributorrole_uri)

            if module_uri:
                triplify(module_uri, pfs["edu-ont"]["references"], media_uri)
        else:
            print(f"Row {i}: Missing or null 'Media Title' or 'Media Link'")

        # Handle prerequisite modules
        if module_uri:
            prereq_modules_str = get_column_value(row, 'Prerequisite Modules')
            if prereq_modules_str:
                prereq_modules = [m.strip()
                                  for m in prereq_modules_str.split(',')]
                for module in prereq_modules:
                    index = dictionary_check(module, modules_dict)
                    prereq_module_uri = pfs["edu-r"][f"Module{index}"]
                    triplify(module_uri, pfs["edu-ont"]
                             ["hasPrerequisite"], prereq_module_uri)
        else:
            pass  # Can't process prerequisites without module_uri

        # Handle Module Category
        category_str = get_column_value(row, 'Category')
        if category_str and module_uri:
            module_categories = [c.strip() for c in category_str.split(',')]
            dictionary_triples(module_categories, "Category",
                               module_category_dict, module_uri, "isInCategory")
        else:
            print(f"Row {i}: Missing or null 'Category' or 'Module Title'")

        # Media with Typing
        format_str = get_column_value(row, 'Format')
        if format_str and media_uri:
            types = [f.strip() for f in format_str.split(',')]
            for type in types:
                type = type.replace(" ", "")
                type_uri = pfs["edu-ont"][type]
                triplify(media_uri, isA, type_uri)
                if type in SpeakerRoleFormats:
                    # Module providesParticipantRole SpeakerRole
                    if module_uri:
                        triplify(
                            module_uri, pfs["edu-ont"]["providesParticipantRole"], speakerrole_uri)

                    # Media providesParticipantRole SpeakerRole
                    triplify(
                        media_uri, pfs["edu-ont"]["providesParticipantRole"], speakerrole_uri)

                    # Author assumesRole SpeakerRole
                    if authors:
                        author_triples(authors, author_uri, speakerrole_uri)
        else:
            print(f"Row {i}: Missing or null 'Format' or 'Media'")

        # Module and Media with Topic
        topic_covered_str = get_column_value(row, 'Topic Covered')
        if topic_covered_str:
            topics = [t.strip() for t in topic_covered_str.split(',')]
            if module_uri:
                dictionary_triples(topics, "Topic", topic_dict,
                                   module_uri, "coversTopic")
            if media_uri:
                dictionary_triples(topics, "Topic", topic_dict,
                                   media_uri, "coversTopic")
        else:
            print(f"Row {i}: Missing or null 'Topic Covered'")

        # Topic Relations
        topic = get_column_value(row, 'Topic')
        if topic:
            topic_index = dictionary_check(topic, topic_dict)
            topic_uri = pfs["edu-ont"][f"Topic{topic_index}"]
            triplify(topic_uri, isA, pfs["edu-ont"]["Topic"])
            triplify(topic_uri, asString, Literal(topic, datatype=XSD.string))

            # Broader Topics
            broader_topics_str = get_column_value(row, 'Broader Topics')
            if broader_topics_str:
                broader_topics = [t.strip()
                                  for t in broader_topics_str.split(',')]
                for broader_topic in broader_topics:
                    broader_topic_index = dictionary_check(
                        broader_topic, topic_dict)
                    broader_topic_uri = pfs["edu-ont"][f"Topic{
                        broader_topic_index}"]
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
                    narrower_topic_index = dictionary_check(
                        narrower_topic, topic_dict)
                    narrower_topic_uri = pfs["edu-ont"][f"Topic{
                        narrower_topic_index}"]
                    triplify(narrower_topic_uri, isA, pfs["edu-ont"]["Topic"])
                    triplify(narrower_topic_uri, asString, Literal(
                        narrower_topic, datatype=XSD.string))
                    triplify(narrower_topic_uri,
                             pfs["edu-ont"]["narrowerThan"], topic_uri)
        else:
            print(f"Row {i}: Missing or null 'Topic Relations'")

        # Media with Topic
        try:
            topics = row['Subject'].split(",")
            dictionary_triples(topics, "Topic", topic_dict,
                               media_uri, "coversTopic")
        except:
            topics = []

        # Media with Topic
        try:
            topics = row['Subject'].split(",")
            dictionary_triples(topics, "Topic", topic_dict,
                               media_uri, "coversTopic")
        except:
            topics = []
        #  Audience
        audience_str = get_column_value(row, 'Audience')
        if audience_str and module_uri:
            audiences = [a.strip() for a in audience_str.split(',')]
            dictionary_triples(audiences, "Audience",
                               audience_dict, module_uri, "recommendedAudience")
        else:
            print(f"Row {i}: Missing or null 'Audience' or 'Module Title'")

        #  Language
        language_str = get_column_value(row, 'Language')
        if language_str and media_uri:
            languages = [l.strip() for l in language_str.split(',')]
            if media_uri:
                dictionary_triples(languages, "Language",
                                   language_dict, media_uri, "supportsLanguage")
        else:
            print(f"Row {i}: Missing or null 'Language' or 'Media'")

    # Add roles to graph
    graph.add((contributorrole_uri, isA, pfs["edu-ont"]["ParticipantRole"]))
    graph.add((speakerrole_uri, isA, pfs["edu-ont"]["ParticipantRole"]))

    print("Graph Created")


def author_triples(authors, predicate, role_uri):
    '''

    '''
    for author in authors:
        author = author.strip()
        index = dictionary_check(author, author_dict)

        # Author as SpeakerRole
        author_uri = pfs["edu-ont"][f"Author{index}"]
        triplify(author_uri, isA, pfs["edu-ont"]["Author"])
        triplify(author_uri, asString, Literal(author, datatype=XSD.string))
        triplify(author_uri, pfs["edu-ont"]["assumesRole"], role_uri)


def main():
    init_triplify()

    # Serialize the graph
    output_file = os.path.join(output_path, f"{output_name}")
    graph.serialize(format="ntriples", encoding="utf-8",
                    destination=output_file)

    print("Graph Serialized")


graph = init_kg()
main()
