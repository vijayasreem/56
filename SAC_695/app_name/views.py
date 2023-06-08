from django.shortcuts import render
from django.http import HttpResponse
from .models import Product
from elasticsearch import Elasticsearch
import json

# Create your views here.
def index(request):
    # Create an ElasticSearch client
    es = Elasticsearch()

    # Automatically index all products
    products = Product.objects.all()
    for product in products:
        es.index(index="products", doc_type="product", id=product.id, body=product.to_dict())

    # Execute search query against the search index
    query = request.GET.get('q')
    res = es.search(index="products", body={"query": {"query_string": {"query": query}}})
    hits = res['hits']['hits']
    results = []
    for hit in hits:
        results.append(hit['_source'])

    # Render the search results
    return render(request, "index.html", {'results': results})

def update_index(request):
    # Create an ElasticSearch client
    es = Elasticsearch()

    # Index any new or updated products
    products = Product.objects.all()
    for product in products:
        es.index(index="products", doc_type="product", id=product.id, body=product.to_dict())

    # Delete any products that have been deleted
    deleted = Product.deleted_objects.all()
    for product in deleted:
        es.delete(index="products", doc_type="product", id=product.id)

    # Return success
    return HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")