#!/usr/bin/env python
from __future__ import print_function

import logging
from dateutil.parser import parse as parse_date

from elasticsearch import Elasticsearch

def print_hits(results, facet_masks={}):
    for facet, mask in facet_masks.items():
        print('-' * 80)
        for d in results['facets'][facet]['terms']:
            print(mask % d)
    print('=' * 80)
    print()

# get trace logger and set level
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.INFO)
tracer.addHandler(logging.FileHandler('/tmp/es_trace.log'))
# instantiate es client, connects to localhost:9200 by default
es = Elasticsearch()

print('Stats for eventid 12345')
result = es.search(
    index='ommtest',
    doc_type='events',
    body={
  'query':{
    'filtered':{
      'filter':{'term':{'eventid':'12345'}}
    }
  },
  'facets':{
    'names_list':{
      'terms':{
        'field':'name'
      }
    }
  }
}
)
print_hits(result, {'names_list': '%(term)15s: %(count)3d'})

