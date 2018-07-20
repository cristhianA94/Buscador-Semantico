from elasticsearch import Elasticsearch
from SPARQLWrapper import SPARQLWrapper,JSON
from numpy import *
ES_HOST = {"host": "localhost", "port": 9200}
es = Elasticsearch(hosts=[ES_HOST])

def ejecutarConsulta(query):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query)
    results = sparql.query().convert()
    datos=[]
    for result in results["results"]["bindings"]:
        datos.append((result["s"]["value"],result["name"]["value"]))
    return datos

def guardarHospitales():
    INDEX_NAME = 'hospitales'
    # es.indices.create(index=INDEX_NAME)
    query ="""
        SELECT distinct *
        WHERE {
        ?s schema:name ?name.
        ?s rdf:type sbc:HealthBuilding.
        }
    """
    datos = ejecutarConsulta(query)
    # return datos
    i=0
    for dato in datos:
        i += 1
        hospital = {"uri": dato[0], "nombre": dato[1],"id":i}
        resp = es.index(index=INDEX_NAME, doc_type="hospital", body=hospital, id=i)
        # resp = es.get(index=INDEX_NAME, doc_type="hospital", id=iz)
        # document = resp["_source"]
        # print(document)
        # print('nombre:', dato[1])
        # print('id: ',i)

def guardarEdiciosSeguridad():
    INDEX_NAME = 'edificios'
    doc_type = 'edificio'
    # es.indices.create(index=INDEX_NAME)
    query ="""
SELECT distinct *
WHERE {
?s v:fn ?name.
?s rdf:type <https://datos.madrid.es/egob/kos/entidadesYorganismos/CentrosAtencionMedica/CentrosSalud>.
}
    """
    datos = ejecutarConsulta(query)
    # return datos
    i=2706+12+22+17+25+47+20
    for dato in datos:
        i += 1
        edificio = {"uri": dato[0], "nombre": dato[1],"id":i}
        resp = es.index(index=INDEX_NAME, doc_type=doc_type, body=edificio, id=i)

def obtenerResource():
    # INDEX_NAME = 'hospitales'
    datos = guardarHospitales()
    for dato in datos:
        query ="""
        SELECT ?s,?name
        WHERE {
            <%s> ?s ?name
        }
        """%dato[0]
        hospital = ejecutarConsulta(query)

        a = array(hospital)
        # print(a[:1,[0,1]])
        i=0
        x,y = a.shape
        data = {}
        print("---------------------")
        while(i<x):
            # print(a[i,1])
            data[a[i,0]]=a[i,1]
            print(data)
            i += 1

    # for data in y:
    #     # print(dato[0])
    #     hospital = {"uri": dato[0], "nombre": dato[1]}
    #     i += 1
    #     hospital = {"uri": dato[0], "nombre": dato[1]}
    #     # resp = es.index(index=INDEX_NAME, doc_type="hospital", body=hospital, id=i)

# SELECT distinct *
# WHERE {
# ?s v:fn ?name.
# ?s rdf:type <https://datos.madrid.es/egob/kos/entidadesYorganismos/ParquesBomberos>.
# }


def document_view():
    INDEX_NAME = 'hospitales'
    resp = es.get(index=INDEX_NAME, doc_type="hospital", id=3)
    document = resp["_source"]
    print(document)

guardarEdiciosSeguridad()
