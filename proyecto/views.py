from django.shortcuts import render
from django.template import loader
from django.views.generic import TemplateView
from proyecto.forms import SparqlForm, UriForm
from SPARQLWrapper import SPARQLWrapper,JSON
from elasticsearch import Elasticsearch
from numpy import *

ES_HOST = {"host": "localhost", "port": 9200}
es = Elasticsearch(hosts=[ES_HOST])
#inciar  virtuoso
#virtuoso-t -fd
class ProyectoView(TemplateView):
    template_name = 'proyecto/index.html'
    def get(self,request):
        form = SparqlForm()
        return render(request, self.template_name ,{'form': form})

    def post(self, request):
        sparql = SPARQLWrapper("http://localhost:8890/sparql")
        form = SparqlForm(request.POST)
        template_name = 'proyecto/resultados.html'
        if form.is_valid():
            query = form.cleaned_data['query']
            hospitales =run_elasticsearch_query(query)
            form = SparqlForm
            datos=[]
            for result in hospitales:
                datos.append((result["_source"]["uri"],result["_source"]["nombre"],result["_source"]["id"]))

        args = {'form':form,'query':query,'datos':datos}
        return render(request, template_name, args)

class Detalles(TemplateView):
    def get(self,request, id):
        form = UriForm()
        template_name = 'proyecto/detalles.html'
        response = id
        INDEX_NAME = 'edificios'
        resp = es.get(index=INDEX_NAME, doc_type="edificio", id=id)
        uri = resp["_source"]["uri"]
        datos = ejecutarConsulta(uri)
        lng = len(datos)

        if(id>2706):
            a = array(datos)
            x=a[5,1]
            y=a[6,1]
            n=a[9,1]

            print("lon: ",x)
            print("lat: ",y)
            print("nombre: ",n)
            lon =x
            lat =y
        else:
            if(lng>0):
                a = array(datos)
                x=a[5,1]
                n=a[2,1]
                my_list = x.split(",")
                lat =my_list[0]
                lon =my_list[1]
            else:
                lat =0
                lon =0
        return render(request, template_name ,{'form':form,'datos': datos,'lat':lat,'lon':lon,'n':n})

    def detalles(request):
        template_name = 'proyecto/uri.html'
        form =  UriForm(request.POST)
        if form.is_valid():
            uri = form.cleaned_data['uri']
            datos = ejecutarConsulta(uri)
            form = UriForm()
        args = {'datos':datos,'form':form,'uri':uri}
        return render(request, template_name, args)



def run_elasticsearch_query(query_keywords):
    es = Elasticsearch()
    # Build the search query
    query = {
        "query": {
            "match": {
                'nombre': query_keywords
            }
        }
    }
    res = es.search(index="edificios", doc_type="edificio", body=query)
    return res['hits']['hits']


def ejecutarConsulta(uri):
    sparql = SPARQLWrapper("http://localhost:8890/sparql")
    query ="""
            SELECT distinct ?s,?name
            WHERE {
                <%s> ?s ?name
            }
    """%uri
    if "dbpedia" in uri:
        sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    elif "madrid" in uri:
        uris = (uri, uri,uri, uri)
        query ="""
            SELECT distinct ?s ?name
            WHERE {{
            <%s> v:adr ?o.
            ?o ?s ?name.
            }UNION{
            <%s> v:geo ?o.
            ?o ?s ?name.
            }
            UNION{
            <%s> v:tel ?o.
            ?o ?s ?name.
            }
            UNION{
            <%s> v:org ?o.
            ?o ?s ?name.
            }
            }
        """%uris

    sparql.setReturnFormat(JSON)

    sparql.setQuery(query)
    results = sparql.query().convert()
    datos=[]
    for result in results["results"]["bindings"]:
        datos.append((result["s"]["value"],result["name"]["value"]))
    return datos
