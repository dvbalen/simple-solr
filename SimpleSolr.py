

import copy
import urllib.parse

def solr_select(url,path):
  return _SimpleSolr(url,path,'solr','select','dismax')

class _SimpleSolr(object):

  # @todo request_handler doesn't do anything
  def __init__(self,url,core,handler_path='solr',handler_name='select',request_handler='dismax'):
    self.url = url.rstrip('/')
    self.core = core.rstrip('/')
    self.handler_path = handler_path.rstrip('/')
    self.handler_name = handler_name
    self.request_handler = request_handler
    self.data = {}

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
        'q': lambda x: store_all('q',x),
        'rows': lambda x: store_one('rows',x),
        'start': lambda x: store_one('start',x),
        }
    

  def __copy__(self):
    new_self = _SimpleSolr(self.url,self.core,self.handler_path,self.handler_name,self.request_handler)
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

  def get_query(self):
    path = [ '/'.join([self.url,self.handler_path,self.core,self.handler_name]), ]
    params = []
    for k,v in self.data.items():
      kv_lst = zip([k]*len(v),v)
      params.extend(l for l in kv_lst)
    if params:
      path.extend(['?',urllib.parse.urlencode(params)])
    return ''.join(path)

q = solr_select('http://localhost:8983','core1')

if __name__ == "__main__":
  q = SimpleSolr('http://localhost:8983','core1')
  print(q.get_query())
