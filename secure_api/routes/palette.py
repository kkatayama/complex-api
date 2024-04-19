from haishoku.haishoku import Haishoku
from colormap import rgb2hex
from urllib.parse import unquote
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlmodel import SQLModel


templates = Jinja2Templates(directory="secure_api/templates")


class ImageData(SQLModel):
    imageURL: str


palette_router = APIRouter(tags=["Palette"])


@palette_router.get('/palette', summary="Generate a palette from an image.", response_class=HTMLResponse)
def get_image_palette(request: Request, imageURL: str):
    imagePath = unquote(imageURL).replace('https://api.mangoboat.tv', 'secure_api')

    h = Haishoku.loadHaishoku(imagePath)
    palette = [rgb2hex(*c[1]) for c in h.palette]
    dominant = rgb2hex(*h.dominant)

    context = {'request': request, 'colors': palette, 'imageURL': imageURL}

    return templates.TemplateResponse("palette.html", context)
