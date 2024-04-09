# coding: utf-8
from pathlib import Path
import re

import pandas as pd


def toExcel(df: pd.DataFrame, xlsxfile: str):
    writer = pd.ExcelWriter(xlsxfile, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1", startrow=1, header=False, index=False)

    workbook = writer.book
    workbook.formats[0].set_font_size(14)
    workbook.formats[1].set_font_size(14)
    #workbook.formats[2].set_font_size(14)
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
    worksheet.set_column(0, 0, df["Endpoint"].astype(str).str.len().max())
    #for i, col in enumerate(df.columns):
    #    worksheet.set_column(i, i, df[col].astype(str).str.len().max())
    worksheet.autofit()
    writer.close()

def parseRoute(route: Path):
    items = []
    raw = route.read_text()

    regex = re.compile(r'''
        @[a-z_\.]+(?P<method>(post|get|patch|delete))[\(\"]+(?P<endpoint>[/a-zA-Z0-9\{\}_-]+) | # method or endpoint
        summary="(?P<summary>[a-zA-Z\_\-\[\]\{\}\(\)\.\:\!\'\=\+\,\!\ ]+)" | # summary
        tags=\["(?P<tag>[a-zA-Z_-]+) | # tags
        status\.(?P<error>[A-Z0-9\_]+) | # error
        detail=(?P<detail>[a-zA-Z\_\-\"\'\[\]\{\}\(\+\:\=\)\!\,.\ ]+) # detail
    ''', re.VERBOSE)
    item = {}
    for match in regex.finditer(route.read_text()):
        m = match.groupdict()
        if m['method']:
            if ((item.get("Method")) and (not item.get("Error"))):
                items.append(dict(**item, Error="", Detail=""))
            item = {"Method": m["method"]}
        if m["endpoint"]:
            item["Endpoint"] = m["endpoint"]
        if m["summary"]:
            item["Summary"] = m["summary"]
        if m["tag"]:
            item["Tag"] = m["tag"]
        if m["error"]:
            item["Error"] = m["error"]
        if m["detail"]:
            item["Detail"] = m["detail"]
            items.append(dict(**item))
        #items.append(item)
    return items


    #for line in route.read_text().splitlines():
    #print(re.findall('@[a-z_\.\"\(]+(?P<endpoint>[/a-zA-Z0-9\{\}_-]+)', route.read_text()))
    #print(re.search(r'tags=\["(?P<tag>[a-zA-Z_-]+)', raw).groupdict())
    #print(set(m.groupdict()["tag"] for m in re.finditer(r'tags=\["(?P<tag>[a-zA-Z_-]+)', route.read_text())))
routes = []
for route in Path('secure_api/routes').glob('*.py'):
    if route.name not in ["__init__.py", "tables.py"]:
        print(route.name)
        items = parseRoute(route)
        routes += items


df = pd.DataFrame(routes)
print(df)

toExcel(df=df, xlsxfile='Endpoint_Error_Test_Conditions.xlsx')
