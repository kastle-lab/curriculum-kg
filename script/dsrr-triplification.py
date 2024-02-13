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
##  Directory and File Parameters of Triplification run
data_path = "./data"
output_path = "./materialization"

filename = os.path.join(data_path, "dsrr-resources-271123.csv")
output_name = "dsrr-triples.ttl"

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
isA = pfs["rdf"]["type"] #isA prefix/relationship
asString = pfs["edu-ont"]["asString"] #type pattern

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


SpeakerRoleFormats = ['Podcast','Video'] #  Adjust array if new role provides SpeakerRole
speakerrole_uri = pfs["edu-ont"]["SpeakerRole"]
contributorrole_uri = pfs["edu-ont"]["ContributorRole"]
# Helper Dictionaries to make Unique Entries
author_dict = dict()
topic_dict = dict()
audience_dict = dict()
language_dict = dict()


def triplify(s,p,o):
    '''
        Adds a (subject, predicate, object) triple to graph.

        s,p, and o should be rdflib terms
    '''    
    graph.add((s,p,o))

def init_triplify():
    '''

    '''
    #  Media Mint + Typing
    for i, row in df.iterrows():
        types = row['Format'].split(",") # Format specifies Media Subclass
        media = row['Title'].strip()   
        try:
            authors = row['Author'].split(",")
        except AttributeError:
            authors = []
        description = row['Description']
        #  Media base information
        media_uri = pfs["edu-r"][f"Media{i}"]
        triplify(media_uri,isA,pfs["edu-ont"]["Media"])
        triplify(media_uri,asString,Literal(f"{media}", datatype=XSD.string))
        triplify(media_uri,pfs["edu-ont"]["hasDescription"],Literal(f"{description}", datatype=XSD.string))
        
        # Media with ContributorRole
        triplify(media_uri,pfs["edu-ont"]["providesParticipantRole"], contributorrole_uri)
        for author in authors:
            author=author.strip()
            index = 0
            if(author in author_dict): # Re-Use already created Authors
                index = author_dict[author]
            else:
                index = len(author_dict)+1
                author_dict[author] = len(author_dict)+1

            # Author as ContributorRole    
            author_uri = pfs["edu-ont"][f"Author{index}"]
            triplify(author_uri, isA, pfs["edu-ont"]["Author"] )
            triplify(author_uri,asString,Literal(author,datatype=XSD.string))
            triplify(author_uri, pfs["edu-ont"]["assumesRole"], contributorrole_uri)


        # Media with Typing
        for type in types:
            type = type.replace(" ", "").strip()
            type_uri = pfs["edu-ont"][f"{type}"]
            graph.add( (media_uri, isA, type_uri) )   
            if(type in SpeakerRoleFormats):
                # Media providesParticipantRole SpeakerRole
                triplify(media_uri,pfs["edu-ont"]["providesParticipantRole"], speakerrole_uri)
                # Author assumesRole SpeakerRole
                author_triples(authors, author_uri, speakerrole_uri)

    
        # Media with Topic    
        try:                    
            topics = row['Subject'].split(",")
            dictionary_triples(topics, "Topic", topic_dict, media_uri, "coversTopic")
        except:
            topics = []
        #  Audience
        audiences = row['Audience Category'].split(",")
        dictionary_triples(audiences, "Audience", audience_dict, media_uri, "recommendedAudience")

        #  Language
        languages = row['Language'].split(",")
        dictionary_triples(languages, "Language", language_dict, media_uri, "supportsLanguage")

    graph.add( (contributorrole_uri, isA, pfs["edu-ont"]["ParticipantRole"]) )
    graph.add( (speakerrole_uri, isA, pfs["edu-ont"]["ParticipantRole"]) )

def dictionary_check(key, dictionary):
    '''
        Checks if dictionary already has key-value pairing.

        Returns already used index-value from dictionary or 
        creates a new one
    '''
    index = 0
    if key in dictionary:
        return dictionary[key]
    else:
        index = len(dictionary)+1
        dictionary[key] = index
        return index

def author_triples(authors, predicate, role_uri):
    '''

    '''
    for author in authors:
        author=author.strip()
        index = dictionary_check(author, author_dict)
        # Author as SpeakerRole
        author_uri = pfs["edu-ont"][f"Author{index}"]
        triplify(author_uri, isA, pfs["edu-ont"]["Author"] )
        triplify(author_uri,asString,Literal(author,datatype=XSD.string))
        triplify(author_uri, pfs["edu-ont"]["assumesRole"], role_uri)

def dictionary_triples(elements, type, dictionary, subject_uri, predicate):
    '''

    '''
    for el in elements:
        el=el.strip()
        index = dictionary_check(el, dictionary)

        el_uri = pfs["edu-ont"][f"{type}{index}"]
        triplify(el_uri,isA,pfs["edu-ont"][f"{type}"])
        triplify(el_uri,asString,Literal(f"{el}",datatype=XSD.string))
        triplify(subject_uri, pfs["edu-ont"][f"{predicate}"], el_uri)
    
def main():
    init_triplify()
    output_file = os.path.join(output_path, f"{output_name}")
    graph.serialize(format="turtle", encoding="utf-8", destination=output_file)

graph = init_kg()
main()