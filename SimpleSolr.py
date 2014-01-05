

import urllib.parse

class SimpleSolr(object):

  def __init__(self,url,core,handler_path='solr'):
    self.url = url.rstrip('/')
    self.core = core.rstrip('/')
    self.handler_path = handler_path.rstrip('/')
    self.handler_name = 'select'
    self.data = {}

    def store_one(key,item):
      self.data[key] = [item]

    def store_all(key,item):
      if key not in self.data:
        self.data[key] = list()
      self.data[key].append(item)
    
    self.methods = {
        'fq': lambda x: store_all('fq',x),
        'rows': lambda x: store_one('rows',x),
        }
    

  def _store(self,name):
    new_self = SimpleSolr(self.url,self.core,self.handler_path)
    new_self.data = dict(self.data)
    def _ret(*args,**kwargs):
      new_self.methods[name](*args,**kwargs)
      return new_self
    return _ret


  def __getattr__(self,name):
    if name in self.methods:
      return self._store(name)
    raise AttributeError("'%s' has no attribute '%s'" % (self.__class__,name) )

  def get_query(self):
    path = [ '/'.join([self.url,self.handler_path,self.core,self.handler_name]),'?' ]
    params = []
    for k,v in self.data.items():
      kv_lst = zip([k]*len(v),v)
      params.extend(l for l in kv_lst)
    path.append(urllib.parse.urlencode(params))
    return ''.join(path)

q = SimpleSolr('http://localhost:8983','core1')

if __name__ == "__main__":
  q = SimpleSolr('http://localhost:8983','core1')
  print(q.get_query())