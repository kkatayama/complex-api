#!/usr/bin/env python3
from pathlib import Path
import re

import pandas as pd


def toExcel(df: pd.DataFrame, xlsxfile: str):
    writer = pd.ExcelWriter(xlsxfile, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

    workbook = writer.book
    workbook.formats[0].set_font_size(14)
    workbook.formats[1].set_font_size(14)
    # workbook.formats[2].set_font_size(14)
    cell_format = workbook.add_format()
    cell_format.set_font_size(16)


    worksheet = writer.sheets["Sheet1"]
    (max_row, max_col) = df.shape

    # -- Add DataFrame with Header Column as Filters
    column_settings = [{"header": column} for column in df.columns]
    worksheet.add_table(0, 0, max_row, max_col - 1, {"columns": column_settings})

    # -- Format Header Row
    worksheet.set_row(0, 20, cell_format=cell_format)

    # -- Format Column Widths Accordingly
    check = df["Endpoint"] if "Endpoint" in df else df["Function"]
    worksheet.set_column(0, 0, check.astype(str).str.len().max())
    #for i, col in enumerate(df.columns):
    #    worksheet.set_column(i, i, df[col].astype(str).str.len().max())
    worksheet.autofit()
    writer.close()

def parseRoute(route: Path):
    items = []

    regex = re.compile(r'''
        @[a-z_\.]+(?P<method>(post|get|patch|delete))[\(\"]+(?P<endpoint>[/a-zA-Z0-9\{\}_-]+) | # method or endpoint
        summary="(?P<summary>[a-zA-Z\_\-\[\]\{\}\(\)\.\:\!\'\=\+\,\!\ ]+)" | # summary
        tags=\["(?P<tag>[a-zA-Z_-]+) | # tags
        \s+(?P<condition>if .+:) | # condition
        status\.(?P<error>[A-Z0-9\_]+) | # error
        detail=(?P<detail>[a-zA-Z\_\-\"\'\[\]\{\}\(\+\:\=\)\!\,.\ ]+) # detail
    ''', re.VERBOSE)
    item = {}
    for match in regex.finditer(route.read_text()):
        m = match.groupdict()
        if m['method']:
            if ((item.get("Method")) and (not item.get("Error"))):
                items.append(dict(**item, Error="", Detail=""))
            item = {"Method": 'HTTP ' + m["method"].upper()}
        if m["endpoint"]:
            item["Endpoint"] = m["endpoint"]
        if m["summary"]:
            item["Summary"] = m["summary"]
        if m["tag"]:
            item["Tag"] = m["tag"]
        if m["condition"]:
            item["condition"] = m["condition"]
        if m["error"]:
            item["Error"] = m["error"]
        if m["detail"]:
            #print(m["detail"])
            item["Detail"] = m["detail"][:-1].strip('f"')
            #print(item["Detail"])
            items.append(dict(**item))
        #items.append(item)
    return items


def camelCase(s):
    func = s.split('(')[0]
    temp = func.split('_')
    temp_func = temp[0] + ''.join(e.title() for e in temp[1:])
    return s.replace(func, temp_func)


def parseFunction(script: Path):
    trans = {
        "plain_password: str": "String plainPassword",
        "hashed_password: str": "String hashedPassword",
        "password: str": "String password",
        "user: User": "User user",
        "expires_delta: timedelta": "Duration expiresDelta",
        "headers": 'headers: {"WWW-Authenticate": "Bearer"}',
        "token: str = Depends(reuseable_oauth)": "String token",
        "db: Session = Depends(get_session)": "Session db"
    }
    items = []
    raw = script.read_text()
    regex = re.compile(r'''
        def\s+(?P<function>[a-zA-Z0-9\_\-\(\)\:\s\=\,]+): |
        """\n*\s+(?P<summary>.+)\n*\s+""" | # summary
        status\.(?P<error>[A-Z0-9\_]+) | # error
        detail=(?P<detail>[a-zA-Z\_\-\"\'\[\]\{\}\+\:\=\!.\ ]+) | # detail
        headers=(?P<headers>(headers))
    ''', re.VERBOSE)

    item = {}
    for match in regex.finditer(script.read_text()):
        m = match.groupdict()
        if m['function']:
            function = m["function"]
            for k in trans:
                function = camelCase(function).replace(k, trans[k])
            if ((item.get("Function")) and (not item.get("Error"))):
                items.append(dict(**item, Error="", Detail=""))
            item = {"Function": function}
        if m["summary"]:
            item["Summary"] = m["summary"]
        if m["error"]:
            item["Error"] = m["error"]
        if m["detail"]:
            #print(m["detail"])
            item["Detail"] = m["detail"][:-1].strip('f")')
            #print(item["Detail"])
        if m["headers"]:
            item["Headers"] = trans[m["headers"]]
            items.append(dict(**item))
        #items.append(item)
    return items


def getRouteErrors():
    routes = []
    #for route in Path('secure_api/routes').glob('*.py'):
    #    if route.name not in ["__init__.py", "tables.py"]:
    for py in ['guest_user.py', 'my.py', 'users.py', 'artists.py', 'albums.py', 'tracks.py', 'playlists.py', 'playhistory.py', 'favorites.py', 'image.py', 'auth.py']:
        route = Path('secure_api', 'routes', py)
        print(route.name)
        items = parseRoute(route)
        routes += items
    
    df = pd.DataFrame(routes)   
    toExcel(df=df, xlsxfile='Endpoint_Error_Test_Conditions.xlsx')
    print(df)

def getFunctionErrors():
    
    functions = parseFunction(script=Path('secure_api/auth/auth_api.py'))
    
    df = pd.DataFrame(functions)
    toExcel(df=df, xlsxfile='Authentican_and_Authorization_Function_Error_Test_Conditions.xlsx')
    print(df)

getRouteErrors()
getFunctionErrors()
