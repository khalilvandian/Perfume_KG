from owlready2 import get_ontology, Thing, ObjectProperty, DataProperty

# Create an empty ontology
onto = get_ontology("http://example.org/perfume_ontology.owl")

with onto:
    # Create classes (Perfume, Brand, Platform)
    class Perfume(Thing):
        pass

    class Brand(Thing):
        pass

    class Platform(Thing):
        pass

    # Create Object Properties (Relationships)
    class productOf(ObjectProperty):
        domain = [Perfume]
        range = [Brand]

    class listedOn(ObjectProperty):
        domain = [Perfume]
        range = [Platform]

    class contains(ObjectProperty):
        domain = [Perfume]
        range = [Thing]

    class hasSimilarPrices(ObjectProperty):
        domain = [Perfume]
        range = [Perfume]

    class hasSimilarScents(ObjectProperty):
        domain = [Perfume]
        range = [Perfume]

    class sameAs(ObjectProperty):
        domain = [Perfume]
        range = [Perfume]

    # Create Data Properties (Attributes of entities)
    class name(DataProperty):
        domain = [Perfume, Brand, Platform]
        range = [str]

    class price(DataProperty):
        domain = [Perfume]
        range = [float]

    class size(DataProperty):
        domain = [Perfume]
        range = [str]

    class rating(DataProperty):
        domain = [Perfume]
        range = [float]

    class scent(DataProperty):
        domain = [Perfume]
        range = [str]

    class url(DataProperty):
        domain = [Perfume]
        range = [str]

    # Handle comments as a string, with a delimiter between individual comments
    class comments(DataProperty):
        domain = [Perfume]
        range = [str]

    class has_offline_store(DataProperty):
        domain = [Platform]
        range = [str]

# Save the ontology to a file
onto.save("perfume_ontology.owl")
