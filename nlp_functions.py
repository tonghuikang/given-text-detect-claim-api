import spacy
import textacy
import numpy as np
import json

import matplotlib.pyplot as plt

nlp = spacy.load('en_core_web_lg')

### demos available in ./function-demo.ipynb


### Function call hierarchy
# During pre-processing
'''
process_claim_list

    process_sentence

        calculate_*_phrases_and_vectors
'''

# During inference
'''
process_article

    process_sentence

        calculate_*_phrases_and_vectors


article_against_claims

    article_sentence_against_claim
    
        compare_vector_array
        
            meshgrid
            cosine
            calculate_similarity_score
'''


def calculate_verb_phrases_and_vectors(sentence):
    # https://stackoverflow.com/questions/47856247/extract-verb-phrases-using-spacy

    pattern = r'<VERB>?<ADV>*<VERB>+'
    doc = textacy.Doc(sentence, lang='en_core_web_sm')

    verb_phrase_objs = textacy.extract.pos_regex_matches(doc, pattern)
    verb_phrase_texts = [verb_phrase_obj.text for verb_phrase_obj in verb_phrase_objs]
    
    # for some reason verb_phrase_objs can only be referenced once
    verb_phrase_objs = textacy.extract.pos_regex_matches(doc, pattern)  ## 
    verb_phrase_vects = [np.array(verb_phrase_obj.vector) for verb_phrase_obj in verb_phrase_objs]
    
    return verb_phrase_texts, verb_phrase_vects


def calculate_noun_phrases_and_vectors(sentence):
    # https://stackoverflow.com/questions/47856247/extract-verb-phrases-using-spacy
    
    doc = nlp(sentence)
    
    noun_phrase_objs = doc.noun_chunks
    noun_phrase_texts = [noun_phrase_obj.text for noun_phrase_obj in noun_phrase_objs]
    # for some reason verb_phrase_objs can only be referenced once
    noun_phrase_objs = doc.noun_chunks
    noun_phrase_vects = [noun_phrase_obj.vector for noun_phrase_obj in noun_phrase_objs]
    
    return noun_phrase_texts, noun_phrase_vects


def calculate_entities_and_vectors(sentence):
    # https://stackoverflow.com/questions/47856247/extract-verb-phrases-using-spacy
    
    doc = nlp(sentence)
    
    entity_objs = doc.ents
    entity_texts = [entity_obj.text for entity_obj in entity_objs]
    # for some reason verb_phrase_objs can only be referenced once
    entity_objs = doc.ents
    entity_vects = [entity_obj.vector for entity_obj in entity_objs]
    
    return entity_texts, entity_vects


def process_sentence(sentence):
    '''
    # returns dictionary of
    claims_text : the input text of the claim
    
    verb_phrase_texts : a list containing strings of text of the verb phrases
    verb_phrase_vects : a list containing ndarrays of the phrase vectors of verb phrases
    
    noun_phrase_texts : a list containing strings of text of the noun phrase
    noun_phrase_vects : a list containing ndarrays of the phrase vectors of noun_phrases
    
    entities_texts : a list containing strings of text of the entities
    entities_vects : a list containing ndarrays of the phrase vectors of entities
    
    the nth entry each text array should correspond to the nth entry of the corresponding vector array 
    
    For each of verb, noun and entities, I decided to split them into separate functions
    This is so I can easily swap out the function instead of editing the function
    '''
    
    processed_claim = {}
    
    # not all uses spaCy as verb_phrases uses textaCy
    # so we won't tokenise the sentence with spaCy first
    
    verb_phrases, verb_phrase_vects = calculate_verb_phrases_and_vectors(sentence)
    noun_phrases, noun_phrase_vects = calculate_noun_phrases_and_vectors(sentence)
    entity, entity_vect = calculate_entities_and_vectors(sentence)
    
    processed_claim["claims_text"] = sentence
    processed_claim["verb_phrases"] = verb_phrases
    processed_claim["verb_phrase_vects"] = verb_phrase_vects
    processed_claim["noun_phrases"] = noun_phrases
    processed_claim["noun_phrase_vects"] = noun_phrase_vects
    processed_claim["entities"] = entity
    processed_claim["entities_vect"] = entity_vect
    
    return processed_claim


def process_claim_list(claims_list, debug = False):
    # want to make it different from article processing
    # each claim in the claim list is definitely a sentence
    # and also so that I can attach URL to this also
    
    processed_claims = []
    for i,claim in enumerate(claims_list):
        processed_claim = process_sentence(claim)
        processed_claims.append(processed_claim)
        if debug:
            print(i, end=" ")
        
    return processed_claims


def process_article(article_text):
    # coreference replacement with StanfordNLP could be done here
    
    doc = nlp(article_text)
    
    sentence_list = [sent.text for sent in doc.sents]
    processed_sentences = [process_sentence(sentence) for sentence in sentence_list]
    
    return processed_sentences



def meshgrid(x,y): 
    # to change to numpy's meshgrid
    return (
        [[x_ for x_ in x] for  _ in y],
        [[y_ for  _ in x] for y_ in y])

def cosine(u,v):
#     print(np.shape(u))
    return np.dot(u,v)/(np.linalg.norm(u)*np.linalg.norm(v))

def calculate_similarity_score(value_mesh):
    similarity_array = np.maximum.reduce([row for row in value_mesh[0]])
    similarity_sum = np.sum(similarity_array)
    return similarity_sum

def compare_vector_array(candidate_vector, reference_vector):
    # note that this function is not symmetrical 
    # https://stackoverflow.com/questions/15616742/ does solves it
    # still need to meshgrid
    # but all of them should be carried out in numpy
    # using my old code here
    
    pair_mesh = meshgrid(reference_vector, candidate_vector)
    value_mesh = meshgrid([0]*len(reference_vector), [0]*len(candidate_vector))

    for i,_ in enumerate(pair_mesh[0]):
        for j,_ in enumerate(pair_mesh[0][0]): 
            vector1 = pair_mesh[0][i][j]
            vector2 = pair_mesh[1][i][j]
            value_mesh[0][i][j] = cosine(vector1, vector2)
    
    similarity_score = calculate_similarity_score(value_mesh)
    
    return similarity_score/len(reference_vector)



def article_sentence_against_claim(processed_sentence, processed_claim):
#     art_sentence = processed_sentence["claims_text"]
#     art_verb_phrases = processed_sentence["verb_phrases"]
    art_verb_phrase_vects = processed_sentence["verb_phrase_vects"]
#     art_noun_phrases = processed_sentence["noun_phrases"]
    art_noun_phrase_vects = processed_sentence["noun_phrase_vects"]
#     art_entity = processed_sentence["entities"]
    art_entity_vect = processed_sentence["entities_vect"]

#     ref_sentence = processed_claim["claims_text"]
#     ref_verb_phrases = processed_claim["verb_phrases"]
    ref_verb_phrase_vects = processed_claim["verb_phrase_vects"]
#     ref_noun_phrases = processed_claim["noun_phrases"]
    ref_noun_phrase_vects = processed_claim["noun_phrase_vects"]
#     ref_entity = processed_claim["entities"]
    ref_entity_vect = processed_claim["entities_vect"]

#     print(art_verb_phrase_vects)

    # compare verb phrases
    verb_similarity_score = compare_vector_array(art_verb_phrase_vects, ref_verb_phrase_vects)
    noun_similarity_score = compare_vector_array(art_noun_phrase_vects, ref_noun_phrase_vects)
    enty_similarity_score = compare_vector_array(art_entity_vect, ref_entity_vect)
    
    return verb_similarity_score, noun_similarity_score, enty_similarity_score
    


def article_against_claims(article_text, processed_claims):

    processed_sentences = process_article(article_text)
    
    similarity_across_sentences = []
    detected = []
    
    for processed_sentence in processed_sentences:
        for processed_claim in processed_claims:
            print(processed_sentence["claims_text"])
            print(processed_claim["claims_text"])
            x,y,z = article_sentence_against_claim(processed_sentence, processed_claim)
            print(x,y,z)
            print()
            
            if x+y+z > 2.0: 
                detected.append((processed_sentence["claims_text"], processed_claim["claims_text"],x,y,z))
            
    print({"detected" : detected})
    return json.dumps({"detected" : detected})            


















