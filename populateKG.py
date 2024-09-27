## Load Ontology
from rdflib import Graph
from owlready2 import get_ontology
import json

def to_camel_case(snake_str):
    components = snake_str.replace('_', ' ').split()
    return components[0] + ''.join(x.capitalize() for x in components[1:])


def create_Accord(accord_name):
    accord_name = to_camel_case(accord_name)
    accord = onto.Accord(accord_name)
    return accord

# Define the path to the OWL ontology
ontology_path = 'ontology/RefactoredPerfumeOntology_02.rdf'
# Load the OWL ontology
onto = get_ontology(ontology_path).load()

# Load Data
with open('Babak_Data\Perfume_Database.Fragrances.json', encoding='utf-8') as f:
    data = json.load(f)

## Populate the ontology 
# Load the first instance of the perfume
perfume_temp = data[0]
perfume_iri_name = to_camel_case(perfume_temp['name'])
perfume = onto.Perfume(perfume_iri_name)

### Label
perfume.label.append(perfume_temp['name'])

### brand
brand_iri_name = to_camel_case(str(perfume_temp['company']))
search_res = onto.search(iri= '*'+brand_iri_name, is_a=onto.Brand)
brand_exists = bool(search_res)

if not brand_exists:
    brand = onto.Brand(brand_iri_name)
else:
    brand = search_res[0]

perfume.producedByBrand.append(brand)

### Image
perfume.image = perfume_temp['image']

### Gender
perfume.gender = perfume_temp['gender']

### Longetivity Vote
perfume.LongetivityIseternal.append(perfume_temp['longevity']['eternal'])
perfume.LongetivityIslongLasting.append(perfume_temp['longevity']['long lasting'])
perfume.LongetivityIsmoderate.append(perfume_temp['longevity']['moderate'])
perfume.LongetivityIsveryWeak.append(perfume_temp['longevity']['very weak'])
perfume.LongetivityIsweak.append(perfume_temp['longevity']['weak'])

### Sillage Vote
perfume.sillageVoteIsEnormous.append(perfume_temp['sillage']['enormous'])
perfume.sillageVoteIsIntimate.append(perfume_temp['sillage']['intimate'])
perfume.sillageVoteIsModerate.append(perfume_temp['sillage']['moderate'])
perfume.sillageVoteIsStrong.append(perfume_temp['sillage']['strong'])

### Price Vote
perfume.priceIsGoodValue.append(perfume_temp['price value']['good value'])
perfume.priceIsGreatValue.append(perfume_temp['price value']['great value'])
perfume.priceIsOk.append(perfume_temp['price value']['ok'])
perfume.priceIsOverpriced.append(perfume_temp['price value']['overpriced'])
perfume.priceIsWayOverpriced.append(perfume_temp['price value']['way overpriced'])

### Price
# perfume.price.append(perfume_temp['price'])

### Accords
for accord in perfume_temp['main accords'].keys():
    # make the name camel case
    accord_name = to_camel_case(str(accord))

    search_res = onto.search(iri= '*'+accord_name, is_a=onto.Accord)
    accord_exists = bool(search_res)
    
    if accord_exists:
        continue
    else:
        create_Accord(accord_name)

### Description
perfume.description.append(perfume_temp['description'])

### Notes
if 'top notes' in perfume_temp.keys():
    for note in perfume_temp['top notes']:
        note_name = to_camel_case(note)
        matching_notes = onto.search(iri=note_name, is_a=onto.Note)
        note_exists = bool(matching_notes)

        if not note_exists:
            note = onto.Note(note_name + 'Note')
        else:
            note = matching_notes[0]

        perfume.hasTopNote.append(note)

if 'middle notes' in perfume_temp.keys():
    for note in perfume_temp['middle notes']:
        note_name = to_camel_case(note)
        matching_notes = onto.search(iri=note_name, is_a=onto.Note)
        note_exists = bool(matching_notes)

        if not note_exists:
            note = onto.Note(note_name + 'Note')
        else:
            note = matching_notes[0]

        perfume.hasMiddleNote.append(note)

if 'base notes' in perfume_temp.keys():
    for note in perfume_temp['base notes']:
        note_name = to_camel_case(note)
        matching_notes = onto.search(iri=note_name, is_a=onto.Note)
        note_exists = bool(matching_notes)

        if not note_exists:
            note = onto.Note(note_name + 'Note')
        else:
            note = matching_notes[0]

        perfume.hasBaseNote.append(note)

if perfume_temp['notes'] in perfume_temp.keys():
    for note in perfume_temp['notes']:
        note_name = to_camel_case(note)
        matching_notes = onto.search(iri=note_name, is_a=onto.Note)
        note_exists = bool(matching_notes)

        if not note_exists:
            note = onto.Note(note_name + 'Note')
        else:
            note = matching_notes[0]

        perfume.hasNote.append(note)


# show me the individual properties of the perfume
for prop in perfume.get_properties():
    for value in prop[perfume]:
        print(".%s == %s" % (prop.python_name, value))

# Save the ontology
onto.save(file="ontology/RefactoredPerfumeOntology_test.rdf", format="rdfxml")

print(perfume)