

import copy
import json
import urllib.parse
import urllib.request

version = '0.4'

def select(url,core):
  return _SimpleSolr(url,core,'solr','select')

def geturl(url):
  return urllib.request.urlopen(url).read().decode('utf-8')

class _SimpleSolr(object):

  def __init__(self,url,core,handler_path='solr',handler_name='select'):
    self.url = url.rstrip('/')
    self.core = core.rstrip('/')
    self.handler_path = handler_path.rstrip('/')
    self.handler_name = handler_name
    self.data = {}
    self.block_start = None
    self.cached_block = iter([])
    self.cached_resp = {}

    def store_one(key,item):
      self.data[key] = [item]

    def store_all(key,item):
      if key not in self.data:
        self.data[key] = list()
      self.data[key].append(item)
    
    # @todo clean up, methods for dismax,edismax,et all
    # @todo make plugable 
    self.methods = {
        'fq': lambda x: store_all('fq',x),
        'fl': lambda x: store_all('fl',x),
        'q': lambda x: store_one('q',x),
        'df': lambda x: store_one('df',x),
        'rows': lambda x: store_one('rows',x),
        'start': lambda x: store_one('start',x),
        'sort': lambda x: store_one('sort',x),
        }

  def __copy__(self):
    new_self = _SimpleSolr(self.url,self.core,self.handler_path,self.handler_name)
    new_self.data = dict(self.data)
    return new_self

  def _store(self,name):
    new_self = copy.copy(self)
    def _ret(*args,**kwargs):
      new_self.methods[name](*args,**kwargs)
      return new_self
    return _ret

  def __getattr__(self,name):
    if name in self.methods:
      return self._store(name)
    raise AttributeError("'%s' has no attribute '%s'" % (self.__class__,name) )

  def __str__(self):
    path = [ '/'.join([self.url,self.handler_path,self.core,self.handler_name]), ]
    params = []
    for k,v in self.data.items():
      kv_lst = zip([k]*len(v),v)
      params.extend(l for l in kv_lst)
    params.append(('wt','json'))
    if params:
      path.extend(['?',urllib.parse.urlencode(params)])
    return ''.join(path)

  def __len__(self):
    q_str = str(self.rows(0))
    resp = json.loads(geturl(q_str))
    try:
      l = resp['response']['numFound']
    except KeyError:
      l = None
    return l

  def __iter__(self):
    self.block_start = 0
    return self

  def __next__(self):
    try:
      r = next(self.cached_block)
    except StopIteration:
      if self._get_block():
        r = next(self.cached_block)
      else:
        raise
    return r

  def _get_block(self):
    if not self.block_start:
      start = self.data.get('start',[0])[0]
    else:
      start = self.block_start
    q_str = str(self.start(start))
    resp = json.loads(geturl(q_str))
    #if resp['responseHeader']['status'] != 0
    #   raise SolrError
    self.block_start = start + len(resp['response']['docs'])
    self.cached_block = iter(resp['response']['docs'])
    self.cached_resp = resp
    return resp['response']['numFound']

#q = select('http://localhost:8983','core0')

if __name__ == "__main__":
  local_solr = select('http://localhost:8983','core0')
  all_rows = local_solr.q('*:*')
  print(all_rows)
  for row in all_rows:
    print(row)
