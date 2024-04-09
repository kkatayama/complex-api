import pandas as pd

from fastapi import FastAPI, Request, APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from secure_api.database.database import get_session, engine
from secure_api.models.models import User, Artist, Album, Track, Image, Playlist, PlaylistTrack, PlayHistory
from sqlmodel import Session, select

import re


# -- helper function to return Pandas generated HTML Table when expected in request...
def genTable(records, caption, count=0):
    table_id = f'table-{count}'
    styles = [dict(selector="caption", props=[("text-align", "center"), ("font-size", "150%"), ("color", 'black')])]
    df = pd.DataFrame(records)
    s = df.style.set_caption(caption).set_table_styles(styles)
    table = s.to_html()
    html = re.sub(r'( id="(T_[_a-z0-9]+)"| class="([_a-z0-9 ]+)" |<style.*</style>\n)', '', table, flags=re.DOTALL)
    html = re.sub(r'(https://api.mangoboat.tv/music/.+(poster|cover).jpg)', r'<img src="\1" height="100"></img>', html)
    html = re.sub(r'(https://api.mangoboat.tv/music/.+\.mp3)', r'<audio controls src="\1"></audio>', html)
    html = html.replace('<th>&nbsp;</th>', '<th>index</th>')
    html = html.replace('<table>', f'<table id="{table_id}" class="dataTable display compact hover" style="width:100%">')
    # html = html.replace('<caption>', '<caption class="mytable caption">')
    # with open(table_id+'.html', 'w') as f:
    #     f.write(html)
    thead = re.search(r'(\s+<thead>.+</thead>)', html, flags=re.DOTALL).group()
    tfoot = thead.replace('thead', 'tfoot')
    html = html.replace('</tbody>', f'</tbody>{tfoot}')
    # html = html.replace('<thead>', '<thead class="table-dark">')
    # html = html.replace('<tbody>', '<tbody class="table-group-divider">')

    return html


tables_router = APIRouter()

templates = Jinja2Templates(directory="secure_api/templates")


@tables_router.get('/tables', response_class=HTMLResponse, include_in_schema=False)
def get_tables(request: Request, db: Session = Depends(get_session)):
    tables = {}
    for i, table in enumerate(["User", "Playlist", "PlaylistTrack", "PlayHistory"]): #, "Artist","Album", "Track", "Image"]):
        db_table = db.exec(select(eval(table))).all()
        #df_table = pd.DataFrame([item.model_dump() for item in db_table])
        html_table = genTable([item.model_dump() for item in db_table], f"Table: {table}", count=i)
        tables.update({f'table_{i}': html_table})
        #print(html_table)
    context = {'request': request, "title": "Com-Plex API Database Tables", **tables}
    return templates.TemplateResponse("tables.html", context)
