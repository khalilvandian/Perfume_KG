def perfumesHaveAccord(accord_uri):
    return f"""
        MATCH (a:Accord {{uri: '{accord_uri}'}})<-[:hasAccord]-(p:Perfume)
        RETURN p.uri as uri, p.label as name
    """

def perfumesShareAccords(perfume_uri):
    query = f"""
        MATCH (specific:Perfume {{uri: '{perfume_uri}'}})-[:hasAccord]->(accord:Accord)<-[:hasAccord]-(other:Perfume)
        WHERE other <> specific
        RETURN other.label AS Perfume, other.uri AS uri, COUNT(accord) AS MutualAccords
        ORDER BY MutualAccords DESC
        LIMIT 10
    """
    return query

def getAllNotes():
    return """
        MATCH (n:Note)
        RETURN n.uri AS uri, n.label AS name
    """

def perfumesHaveNote(note_uri):
    return f"""
        MATCH (n:Note {{uri: '{note_uri}'}})<-[:hasNote]-(p:Perfume)
        RETURN p.uri AS uri, p.label AS name
    """

def perfumesShareNotes(perfume_uri):
    return f"""
        MATCH (specific:Perfume {{uri: '{perfume_uri}'}})
              -[:hasNote]->(note:Note)<-[:hasNote]-(other:Perfume)
        WHERE other <> specific
        RETURN other.label AS Perfume, other.uri AS uri, COUNT(note) AS MutualNotes
        ORDER BY MutualNotes DESC
        LIMIT 10
    """

def getAllBrands():
    return """
        MATCH (b:Brand)
        RETURN b.uri AS uri, b.label AS name
    """


def getAccordsUsedByBrand(brand_uri):
    return f"""
        MATCH (brand:Brand {{uri: '{brand_uri}'}})<-[:producedBy]-(perfume:Perfume)-[:hasAccord]->(accord:Accord)
        RETURN DISTINCT accord.uri AS accordUri, accord.label AS accordName
    """


def getNotesUsedByBrand(brand_uri):
    return f"""
        MATCH (brand:Brand {{uri: '{brand_uri}'}})<-[:producedBy]-(perfume:Perfume)-[:hasNote]->(note:Note)
        RETURN DISTINCT note.uri AS noteUri, note.label AS noteName
    """



def getMostUsedAccordForBrand(brand_uri):
    return f"""
        MATCH (brand:Brand {{uri: '{brand_uri}'}})<-[:producedBy]-(perfume:Perfume)-[:hasAccord]->(accord:Accord)
        WITH accord, COUNT(*) AS usageCount
        ORDER BY usageCount DESC
        RETURN accord.label AS accordName, accord.uri AS accordUri, usageCount
        LIMIT 10
    """

def getAccordSimilarityScore(perfume_uri):
    return f"""
        MATCH (specific:Perfume {{uri: '{perfume_uri}'}})
        OPTIONAL MATCH (specific)-[:hasAccord]->(specificAccord:Accord)
        WITH specific, COLLECT(DISTINCT specificAccord) AS specificAccords

        MATCH (other:Perfume)
        WHERE other <> specific
        OPTIONAL MATCH (other)-[:hasAccord]->(otherAccord:Accord)
        WITH specific, specificAccords, other, COLLECT(DISTINCT otherAccord) AS otherAccords

        WITH other,
            [accord IN specificAccords WHERE accord IN otherAccords] AS mutualAccords,
            [accord IN specificAccords WHERE NOT accord IN otherAccords] +
            [accord IN otherAccords WHERE NOT accord IN specificAccords] AS notMutualAccords,
            SIZE([accord IN specificAccords WHERE accord IN otherAccords]) AS MutualAccordsCount,
            SIZE([accord IN specificAccords WHERE NOT accord IN otherAccords] +
                [accord IN otherAccords WHERE NOT accord IN specificAccords]) AS NotMutualAccordsCount

        WITH other,
            MutualAccordsCount,
            NotMutualAccordsCount,
            toFloat(MutualAccordsCount) / (MutualAccordsCount + NotMutualAccordsCount + 1) AS similarity

        RETURN
            other.label AS Perfume,
            other.uri AS uri,
            similarity
        ORDER BY similarity DESC
    """

def getNoteSimilarityScore(perfume_uri):
    return f"""
        MATCH (specific:Perfume {{uri: '{perfume_uri}'}})
        OPTIONAL MATCH (specific)-[:hasNote]->(specificNote:Note)
        WITH specific, COLLECT(DISTINCT specificNote) AS specificNotes

        MATCH (other:Perfume)
        WHERE other <> specific
        OPTIONAL MATCH (other)-[:hasNote]->(otherNote:Note)
        WITH specific, specificNotes, other, COLLECT(DISTINCT otherNote) AS otherNotes

        WITH other,
            [note IN specificNotes WHERE note IN otherNotes] AS mutualNotes,
            [note IN specificNotes WHERE NOT note IN otherNotes] +
            [note IN otherNotes WHERE NOT note IN specificNotes] AS notMutualNotes,
            SIZE([note IN specificNotes WHERE note IN otherNotes]) AS MutualNotesCount,
            SIZE([note IN specificNotes WHERE NOT note IN otherNotes] +
                 [note IN otherNotes WHERE NOT note IN specificNotes]) AS NotMutualNotesCount

        WITH other,
            MutualNotesCount,
            NotMutualNotesCount,
            CASE
                WHEN (MutualNotesCount + NotMutualNotesCount + 1) = 0 THEN 0
                ELSE toFloat(MutualNotesCount) / (MutualNotesCount + NotMutualNotesCount + 1)
            END AS similarity

        RETURN
            other.label AS Perfume,
            other.uri AS uri,
            similarity
        ORDER BY similarity DESC
    """
