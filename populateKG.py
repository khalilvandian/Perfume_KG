## Load Ontology
from rdflib import Graph
from owlready2 import get_ontology
import json
import traceback
import re
import unicodedata

def preprocess_name(name):
    # Normalize unicode characters
    name = unicodedata.normalize('NFKD', name)
    # Remove diacritics (accents)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    # Replace non-alphanumeric characters with hyphens
    name = re.sub(r'[^a-zA-Z0-9]+', '-', name)
    # Remove leading and trailing hyphens
    name = name.strip('-')
    # Convert to lowercase
    name = name.lower()
    return name

def to_camel_case(snake_str):
    # components = snake_str.replace('_', ' ').split()
    # camelCased =  components[0] + ''.join(x.capitalize() for x in components[1:])
    return preprocess_name(snake_str)

def create_Accord(accord_name):
    accord_name_cc = 'Accord_' + to_camel_case(accord_name)
    accord = onto.Accord(accord_name_cc)
    accord.label.append(accord_name)
    return accord


def loadPerfume(perfume_temp, onto):
    if 'name' in perfume_temp:
        perfume_iri_name = 'Perfume_' + to_camel_case(perfume_temp['name'])
        perfume = onto.Perfume(perfume_iri_name)
        perfume.label.append(perfume_temp['name'])

    # Brand
    if 'company' in perfume_temp:
        brand_iri_name = 'Brand_' + to_camel_case(str(perfume_temp['company']))
        search_res = onto.search(iri='*' + brand_iri_name, is_a=onto.Brand)
        brand_exists = bool(search_res)

        if not brand_exists:
            brand = onto.Brand(brand_iri_name)
            brand.label.append(perfume_temp['company'])
        else:
            brand = search_res[0]

        perfume.producedByBrand.append(brand)

    # Image
    if 'image' in perfume_temp:
        perfume.image.append(perfume_temp['image'])

    # Gender
    if 'gender' in perfume_temp:
        perfume.gender.append(perfume_temp['gender'])

    # Longevity Vote
    if 'longevity' in perfume_temp:
        longevity = perfume_temp['longevity']
        if 'eternal' in longevity:
            perfume.LongetivityIseternal.append(longevity['eternal'])
        if 'long lasting' in longevity:
            perfume.LongetivityIslongLasting.append(longevity['long lasting'])
        if 'moderate' in longevity:
            perfume.LongetivityIsmoderate.append(longevity['moderate'])
        if 'very weak' in longevity:
            perfume.LongetivityIsveryWeak.append(longevity['very weak'])
        if 'weak' in longevity:
            perfume.LongetivityIsweak.append(longevity['weak'])

    # Sillage Vote
    if 'sillage' in perfume_temp:
        sillage = perfume_temp['sillage']
        if 'enormous' in sillage:
            perfume.sillageVoteIsEnormous.append(sillage['enormous'])
        if 'intimate' in sillage:
            perfume.sillageVoteIsIntimate.append(sillage['intimate'])
        if 'moderate' in sillage:
            perfume.sillageVoteIsModerate.append(sillage['moderate'])
        if 'strong' in sillage:
            perfume.sillageVoteIsStrong.append(sillage['strong'])

    # Price Vote
    if 'price value' in perfume_temp:
        price_value = perfume_temp['price value']
        if 'good value' in price_value:
            perfume.priceIsGoodValue.append(price_value['good value'])
        if 'great value' in price_value:
            perfume.priceIsGreatValue.append(price_value['great value'])
        if 'ok' in price_value:
            perfume.priceIsOk.append(price_value['ok'])
        if 'overpriced' in price_value:
            perfume.priceIsOverpriced.append(price_value['overpriced'])
        if 'way overpriced' in price_value:
            perfume.priceIsWayOverpriced.append(price_value['way overpriced'])

    # Accords
    if 'main accords' in perfume_temp and perfume_temp['main accords'] is not None:
        for accord in perfume_temp['main accords'].keys():
            accord_name = 'Accord_' + to_camel_case(str(accord))
            search_res = onto.search(iri='*' + accord_name, is_a=onto.Accord)
            accord_exists = bool(search_res)

            if not accord_exists:
                accord = create_Accord(str(accord))
            else:
                accord = search_res[0]

            perfume.hasAccord.append(accord)

    # Description
    if 'description' in perfume_temp:
        perfume.description.append(perfume_temp['description'])

    def create_Note(note_name):
        note_name_camel = 'Note_' + to_camel_case(note_name)
        note = onto.Note(note_name_camel)
        note.label.append(note_name)
        return note

    def find_Note(note_name):
        note_name_camel = 'Note_' + to_camel_case(note_name)
        matching_notes = onto.search(iri='*' + note_name_camel, is_a=onto.Note)
        return matching_notes

    # Notes
    if 'top notes' in perfume_temp and perfume_temp['top notes'] is not None:
        for note in perfume_temp['top notes']:
            matching_notes = find_Note(note)
            note_exists = bool(matching_notes)

            if not note_exists:
                res_note = create_Note(note)
            else:
                res_note = matching_notes[0]

            perfume.hasTopNote.append(res_note)

    if 'middle notes' in perfume_temp and perfume_temp['middle notes'] is not None:
        for note in perfume_temp['middle notes']:
            matching_notes = find_Note(note)
            note_exists = bool(matching_notes)

            if not note_exists:
                res_note = create_Note(note)
            else:
                res_note = matching_notes[0]

            perfume.hasMiddleNote.append(res_note)

    if 'base notes' in perfume_temp and perfume_temp['base notes'] is not None:
        for note in perfume_temp['base notes']:
            matching_notes = find_Note(note)
            note_exists = bool(matching_notes)

            if not note_exists:
                res_note = create_Note(note)
            else:
                res_note = matching_notes[0]

            perfume.hasBaseNote.append(res_note)

    if 'notes' in perfume_temp and perfume_temp['notes'] is not None:
        for note in perfume_temp['notes']:
            matching_notes = find_Note(note)
            note_exists = bool(matching_notes)

            if not note_exists:
                res_note = create_Note(note)
            else:
                res_note = matching_notes[0]

            perfume.hasNote.append(res_note)

    return perfume


def print_individual_properties(perfume):
    # show me the individual properties of the perfume
    for prop in perfume.get_properties():
        for value in prop[perfume]:
            print(".%s == %s" % (prop.python_name, value))


if __name__ == '__main__':
    # Define the path to the OWL ontology
    ontology_path = 'Ontology\perfumeKG_Base_01.rdf'
    # Load the OWL ontology
    onto = get_ontology(ontology_path).load()

    # Load Data
    with open('Babak_Data\Perfume_Database.Fragrances.json', encoding='utf-8') as f:
        data = json.load(f)

    # for keeping the data that are not loaded
    errornous_data = []
    errors = []

    for perfume_temp in data:
        ## Populate the ontology 
        
        try:
            perfume = loadPerfume(perfume_temp=perfume_temp, onto=onto)
        except Exception as e:
            errornous_data.append(perfume_temp)
            error_dict = {
                'error': str(e),
                'traceback': traceback.format_exc(),
                'data': perfume_temp['name']
            }
            errors.append(error_dict)

            continue
        # print_individual_properties(perfume)

    # Save the ontology
    onto.save(file="ontology/PerfumeKG_Loaded_01.rdf", format="rdfxml")

    # write the errornous data to a file
    # with open('errornous_data.json', 'w') as f:
        # json.dump(errornous_data, f, indent=4)

    for error_i in errors[:2]:
        print(error_i)