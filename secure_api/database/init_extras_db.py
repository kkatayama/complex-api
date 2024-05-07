from urllib.parse import unquote
from pathlib import Path
import re

from colormap import rgb2hex
from haishoku.haishoku import Haishoku

from imgcat import imgcat
import blurhash

import PIL.Image
import numpy as np
import os

import requests
from rich import print
from plexarr import PlexPy

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from sqlmodel import Session, create_engine

from secure_api.schemas.schemas import (ArtistFull, ArtistWithAlbums, AlbumAll, ArtistAll, ArtistWithAlbumTracks, ArtistWithAlbumsTracks)
from secure_api.models.models import Artist, Album, Track, ArtistExtra, AlbumExtra, TrackExtra, Favorite
from secure_api.database.database import get_session


explicit = b"\xf0\x9f\x85\xb4".decode()
url = 'https://api.mangoboat.tv'
sqlite_url = f'sqlite:///./tracks2.db'
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def patchDB(term="", repl="", preview=False, artist=None, album=None, track=None,
            artistName=True, albumName=True, trackName=True, imageName=True,
            artistPhotoURL=True, albumCoverURL=True, trackURL=True, imageURL=True):
    tables = {}
    if artistName or artistPhotoURL:
        tables["Artist"] = []
    if albumName or albumCoverURL:
        tables["Album"] = []
    if trackName or trackURL:
        tables["Track"] = []

    if artistName:
        tables["Artist"].append("artistName")
    if artistPhotoURL:
        tables["Artist"].append("artistPhotoURL")

    if albumName:
        tables["Album"].append("albumName")
    if albumCoverURL:
        tables["Album"].append("albumCoverURL")

    if trackName:
        tables["Track"].append("trackName")
    if trackURL:
        tables["Track"].append("trackURL")

    for table, columns in tables.items():
        for column in columns:
            cmd = f"sqlite3 -batch -interactive tracks.db 'SELECT REPLACE({column}, \"{term}\", \"{repl}\") FROM {table} WHERE {column} LIKE \"%{term}%\";'"
            print()
            print(cmd)
            os.system(cmd)

            if not preview:
                cmd = f"sqlite3 -batch -interactive tracks.db 'UPDATE {table} SET {column} = REPLACE({column}, \"{term}\", \"{repl}\");'"
                print()
                print(cmd)
                os.system(cmd)

            # cmd = f"sqlite3 tracks.db 'SELECT * FROM {table} WHERE {column} LIKE \"%{term}%\";'"
            # print(cmd)
            # os.system(cmd)

    temp = ''
    if artist:
        temp += f'/{artist.artistName}'
    if album:
        temp += f'/{album.albumName}'
    if track:
        temp += f'/{track.trackName}'

    term_path = Path('secure_api/music'+temp).joinpath(term)
    repl_path = Path('secure_api/music'+temp).joinpath(repl)
    print()
    print(f'RENAME: "{term_path}" => "{repl_path}"')
    if not preview:
        if not term_path.exists():
            print('[red]ERROR PATH NOT FOUND: "{term_path}"[/]')
        term_path.rename(repl_path)
#patchDB(term="Pinkpanthress", repl="PinkPantheress")


def decodeHash(hashcode: str):
    data = blurhash.decode(hashcode, 256, 256)
    im = PIL.Image.fromarray(np.array(data).astype('uint8'))
    return im

# imgcat(decodeHash('LVC?$Ixu00V@8_M{x]t7ozxaxuNb'))
# imgcat(decodeHash('LSG+H]-p4.M{4mx]%3Rj57Ipxtof'))
# imgcat(decodeHash('LFEV+*t600of4oWB%LWB9GayRjay'))


def get_image_palette(im: PIL.Image, imageURL: str):
    imagePath = unquote(imageURL).replace('https://api.mangoboat.tv', 'secure_api')
    im.save(Path(imagePath))

    h = Haishoku.loadHaishoku(imagePath)
    palette = [rgb2hex(*c[1]) for c in h.palette]
    dominant = rgb2hex(*h.dominant)
    # return dominant, palette
    return palette


def login(path="/sign-in"):
    api = url + path
    obj = {"username": "admin", "password": "admin"}
    s = requests.Session()
    r = s.post(api, json=obj)
    d = r.json()
    s.headers.update({"Authorization": "Bearer " + d["access_token"]})
    return s


def getArtists(s, path="/artists?offset=0&limit=1000"):
    api = url + path
    for item in  s.get(api).json():
        artist = Artist(**item)
        path = '/artist/{artistID}/albums-tracks'.format(artistID=artist.artistID)
        api2 = url + path

        obj = s.get(api2).json()
        artist_exp = ArtistWithAlbumsTracks(**obj)
        yield artist_exp


def generate():
    plex = PlexPy()
    music = plex.library.section(title="Music")

    with Session(engine) as db:
        s = login()
        for artist in getArtists(s):
            plex_artist = music.get(artist.artistName)
            print(plex_artist.thumbBlurHash)

            try:
                img_thumb = decodeHash(str(plex_artist.thumbBlurHash))
                url_thumb = artist.artistPhotoURL.replace("poster.jpg", "thumb.jpg")
                thumb = get_image_palette(im=img_thumb, imageURL=url_thumb)
                thumbPalette = ','.join(get_image_palette(img_thumb, url_thumb))
            except:
                thumbPalette = ''
            try:
                img_art = decodeHash(str(plex_artist.artBlurHash))
                url_art = artist.artistPhotoURL.replace("poster.jpg", "art.jpg")
                art = get_image_palette(im=img_thumb, imageURL=url_art)
                artPalette = ','.join(get_image_palette(img_art, url_art))
            except:
                artPalette = ''

            genre = next(iter(plex_artist.genres), "")
            if genre:
                genre = genre.tag
            info = plex_artist.summary

            db_artist = ArtistExtra(artistID=artist.artistID, artistName=artist.artistName, artistPhotoURL=artist.artistPhotoURL,
                                    genre=genre, info=info, thumbPalette=thumbPalette, artPalette=artPalette)
            db.add(db_artist)
            db.commit()
            db.refresh(db_artist)
            print(db_artist)

            for album in artist.albums:
                print(' + ' + album.albumName)
                plex_album = next(filter(lambda x: x.title == album.albumName+' '+explicit, plex_artist.albums()), '')
                if not plex_album:
                    plex_album = next(filter(lambda x: x.title.strip(explicit+' ') == album.albumName.strip(explicit+' '), plex_artist.albums()), '')
                if not plex_album:
                    plex_album = plex_artist.album(album.albumName)

                try:
                    img_thumb = decodeHash(str(plex_album.thumbBlurHash))
                    url_thumb = album.albumCoverURL.replace('cover.jpg', 'album.jpg')
                    thumbPalette = ','.join(get_image_palette(img_thumb, url_thumb))
                except:
                    thumbPalette = ''

                genre = next(iter(plex_album.genres), "")
                if genre:
                    genre = genre.tag
                db_album = AlbumExtra(albumID=album.albumID, albumName=album.albumName, albumCoverURL=album.ablumCoverURL,
                                      numSongs=album.numSongs, year=album.year, genre=genre, info=info, thumbPalette=thumbPalette)
                db.add(db_album)
                db.commit()
                db.refresh(db_artist)
                print(db_album)

                # for track in album.tracks:
                #     print('    - ' + track.trackName)
                #     plex_track = next(filter(lambda x: x.title.strip(explicit+' ') == track.trackName.strip(explicit+' '), plex_album.tracks()), '')
                #     if not plex_track:
                #         plex_track = plex_album.track(track.trackName)


# if __name__ == '__main__':
#     generate()
