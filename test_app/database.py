from flask import g
import sqlite3
from neo4j import GraphDatabase
from rdflib_neo4j import Neo4jStoreConfig, Neo4jStore, HANDLE_VOCAB_URI_STRATEGY
from rdflib import Graph

def connect_db():
    sql = sqlite3.connect('B:/Projects/Perfume_KG/test_app/food_log.db')
    sql.row_factory = sqlite3.Row
    return sql

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_neo4j():
    URI = "neo4j+s://53601604.databases.neo4j.io"
    AUTH = ("neo4j", "P2Ui4U8o4mpSotvcLNAVXock_1IpcJh5rFANct7uKSc")

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        return driver
