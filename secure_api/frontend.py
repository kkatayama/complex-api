from fastapi import FastAPI

from nicegui import app, ui


def init(fastapi_app: FastAPI) -> None:
    @ui.page('/')
    def show():
        ui.label('Hello, FastAPI!')

        columns = [
            {'name': 'name', 'label': 'Name', 'field': 'name', 'required': True, 'align': 'left'},
            {'name': 'age', 'label': 'Age', 'field': 'age', 'sortable': True},
        ]
        rows = [
            {'name': 'Elsa', 'age': 18},
            {'name': 'Oaken', 'age': 46},
            {'name': 'Hans', 'age': 20},
            {'name': 'Sven'},
            {'name': 'Olaf', 'age': 4},
            {'name': 'Anna', 'age': 17},
        ]
        ui.table(columns=columns, rows=rows, pagination=3)
        ui.table(columns=columns, rows=rows, pagination={'rowsPerPage': 4, 'sortBy': 'age', 'page': 2})


    ui.run_with(
        fastapi_app,
        mount_path='/gui',  # NOTE this can be omitted if you want the paths passed to @ui.page to be at the root
        storage_secret='secret',  # NOTE setting a secret is optional but allows for persistent storage per user
    )
