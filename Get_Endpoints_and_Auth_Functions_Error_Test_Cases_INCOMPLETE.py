# coding: utf-8
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


c = Console(record=True)
openapi = 'https://api.mangoboat.tv/openapi.json'
r = requests.get(url=openapi)
api = r.json()
c.print(api)
get_ipython().run_line_magic('pinfo', 'parse')
parse(openapi)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


c = Console(record=True)
openapi = 'https://api.mangoboat.tv/openapi.json'
r = requests.get(url=openapi)
api = r.json()
c.print(api)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


c = Console(record=True)
openapi = 'https://api.mangoboat.tv/openapi.json'
r = requests.get(url=openapi)
api = r.json()
c.print(api)

data = parse(openapi)
c.print(data)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


c = Console(record=True)
openapi = 'https://api.mangoboat.tv/openapi.json'
r = requests.get(url=openapi)
d = r.json()
c.print(d)


api = parse(openapi)

c.print('[cyn]Application Servers[/]')
for server in api.servers:
    c.print(f"{server.description} - {server.url}")
api.servers
api.security_schemas
api.extensions
api.external_docs
api.info
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


c = Console(record=True)
openapi = 'https://api.mangoboat.tv/openapi.json'
r = requests.get(url=openapi)
d = r.json()
c.print(d)


api = parse(openapi)

c.print(api.info)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

urls = [x.url for x in api.paths]
c.print(urls)
api.paths
c.print(api.paths[0])
p = c.paths[0]
api.paths[0].description
api.paths[0].extensions
api.paths[0].operations
c.print(api.paths[0].operations)
api.paths[0].url
api.paths[0].description
api.paths[0].operations
api.paths[0].operations[0].description
api.paths[0].operations[0].external_docs
api.paths[0].operations[0].method
api.paths[0].operations[0].method.value
api.paths[0].operations[0].parameters
api.paths[0].operations[0].request_body
api.paths[0].operations[0].request_body.content
api.paths[0].operations[0].request_body.content[0].schema
print(api.paths[0].operations[0].request_body.content[0].schema)
c.print(api.paths[0].operations[0].request_body.content[0].schema)
c.print(api.paths[0].operations[0].request_body.content[0].schema.default)
c.print(api.paths[0].operations[0].request_body.content[0].schema.enum)
c.print(api.paths[0].operations[0].request_body.content[0].schema.example)
c.print(api.paths[0].operations[0].request_body.content[0].schema.description)
c.print(api.paths[0].operations[0].request_body.content[0].schema.min_properties)
c.print(api.paths[0].operations[0].request_body.content[0].schema.nullable)
c.print(api.paths[0].operations[0].request_body.content[0].schema.properties)
c.print(api.paths[0].operations[0].request_body.content[0].schema.required)
c.print(api.paths[0].operations[0].request_body.content[0].schema.properties.)
c.print(api.paths[0].operations[0].request_body.content[0].schema.properties[0].name)
c.print(api.paths[0].operations[0].request_body.content[0].schema.properties[0].schema.min_length)
api.info
c.print(api.info)
c.print(api.info.description)
c.print(api.external_docs)
c.print(api.security)
c.print(api.schemas)
c.print(api.extensions)
c.print(api.security_schemas)
c.print(api.servers)
c.print(api.tags)
c.print(api.version)
c.print(api.paths[0])
c.print(api.paths[0])
c.print(api.paths[0].url).
c.print(api.paths[0].url)
c.print(api.paths[0].operations[1])
c.print(api.paths[0].operations[0])
c.print(api.paths[0].operations[0].tags)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

for path in api.paths:
    c.print(path.operations[0].tags)
    c.print(path.operations[0].method.name)
    break
    
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

for path in api.paths:
    c.print(path.operations[0].tags[0])
    c.print(path.operations[0].method.name)
    break
    
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

for path in api.paths:
    method = path.operations[0].method.name
    endpoint = path.url
    summary = path.operations[0].summary
    tag = path.operations[0].tags[0]
    responses = path.operations[0].responses
    c.print(path)
    c.print(method, endpoint, summary, tag, responses)
    break
    
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

for path in api.paths:
    method = path.operations[0].method.name
    endpoint = path.url
    summary = path.operations[0].summary
    tag = path.operations[0].tags[0]
    responses = path.operations[0].responses
    #c.print(path)
    c.print(method, endpoint, summary, tag, responses)
    break
method
endpoint
summary
tag
responses
responses[0].code
responses[0].content
responses[0].content[0].type
c.print(responses[0].content[0].schema)
c.print(responses[0].content[1].schema)
c.print(responses[1].content[0].schema)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

for path in api.paths:
    method = path.operations[0].method.name
    endpoint = path.url
    summary = path.operations[0].summary
    tag = path.operations[0].tags[0]
    c.print([res for res in path.operations[0].responses])
    #c.print(path)
    #c.print(method, endpoint, summary, tag, responses)
    break
resp = responses[0]
resp.code
resp.headers
resp.description
resp.is_default
resp.content
resp.content[0].__dict__
c.print(resp.content[0].__dict__)
from openapi_parser import parse
from rich.console import Console
import pandas as pd
import requests


#c = Console(record=True)
#openapi = 'https://api.mangoboat.tv/openapi.json'
#r = requests.get(url=openapi)
#d = r.json()
c.print(d)


#api = parse(openapi)
c.print('[cyn]API Info[/]')
c.print(api.info)

for path in api.paths:
    method = path.operations[0].method.name
    endpoint = path.url
    summary = path.operations[0].summary
    tag = path.operations[0].tags[0]
    c.print([res for res in path.operations[0].responses])
    #c.print(path)
    #c.print(method, endpoint, summary, tag, responses)
    break
    
