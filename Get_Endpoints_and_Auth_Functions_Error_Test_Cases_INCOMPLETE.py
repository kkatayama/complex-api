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
    
