from io import BytesIO
from pathlib import Path
from urllib.parse import urljoin

import PIL.Image
from dateutil.parser import parse
from pymediainfo import MediaInfo
from rich.console import Console
from rich.traceback import install
from secure_api import configs
from secure_api.models.models import Album, Artist, Image, Track
from sqlmodel import Session, create_engine, select

install(show_locals=True, locals_hide_dunder=False)

def get_year(text):
    try:
        return parse(text).year
    except:
        pass
    try:
        return parse(text, dayfirst=True).year
    except:
        pass
    try:
        return parse(text, yearfirst=True).year
    except:
        pass
    return text


def get_date(text):
    try:
        return parse(text).date()
    except:
        pass
    try:
        return parse(text, dayfirst=True).date()
    except:
        pass
    try:
        return parse(text, yearfirst=True).date()
    except:
        pass
    return text


def getIMG(img_path):
    img = PIL.Image.open(BytesIO(img_path.read_bytes()))
    width, height = img.size
    return f'{width}x{height}'


def insert_tracks():
    images = []

    c = Console()
    api_url = 'https://api.mangoboat.tv'
    sqlite_url = f'sqlite:///./{configs.DB_FILE}'
    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

    explicit = b"\xf0\x9f\x85\xb4".decode()
    secure_api = Path.cwd().joinpath('secure_api')
    music_path = Path.cwd().joinpath('secure_api', 'music')


    for artist_path in sorted(music_path.iterdir()):
        artist_name = artist_path.name
        artist_image = (artist_path / 'poster.jpg').relative_to(secure_api)
        artist_image_url = urljoin(api_url, str(artist_image))
        if not (secure_api /artist_image).exists():
            c.print(f'[red]"{artist_image}"[/] == MISSING')
        # imgcat(secure_api.joinpath(artist_image).read_bytes(), width=20, height=20)

        artist = Artist(
            artistName = artist_name,
            artistPhotoURL = artist_image_url
        )
        db_artist = artist # Artist.model_validate(artist)

        with Session(engine) as db:
            # -- Only add Artist if it doesn't exist -- #
            if db.exec(select(Artist).where(Artist.artistPhotoURL == artist.artistPhotoURL)).first() is None:
                # c.print(f'artist: "{artist}"')
                db.add(db_artist)
                db.commit()
                db.refresh(db_artist)
                # c.print(db_artist)
                print('Artist :', {k:v for k,v in db_artist.dict().items() if "ID" in k or "Name" in k})

                # artistID = db_artist.artistID
                images.append(Image(
                    resolution=getIMG(secure_api/artist_image),
                    imageURL=artist_image_url,
                    imageType="Artist Photo",
                    artistID=db_artist.artistID,
                    albumID=0,
                    artist=db_artist,
                    album=None,
                ))
            else:
                db_artist = db.exec(select(Artist).where(Artist.artistPhotoURL == artist.artistPhotoURL)).first()



        for album_path in sorted(folder for folder in artist_path.iterdir() if folder.is_dir()):
            album_info = MediaInfo.parse(next(album_path.glob('**/*.mp3'))).general_tracks[0]
            album_title = album_info.album # album_path.name
            album_num_tracks = album_info.track_name_total
            album_year = get_year(album_info.recorded_date)
            album_image = (album_path / 'cover.jpg').relative_to(secure_api)
            album_image_url = urljoin(api_url, str(album_image))
            if not album_num_tracks:
                album_num_tracks = len(sorted(album_path.glob('**/*.mp3')))
            if not (secure_api /album_image).exists():
                c.print(f'[red]"{album_image}"[/] == MISSING')
            # imgcat(secure_api.joinpath(album_image).read_bytes(), width=20, height=20)

            album = Album(
                albumName=album_title,
                numSongs=album_num_tracks,
                year=album_year,
                albumCoverURL=album_image_url,

                artistID=db_artist.artistID,
            )
            db_album = album # Album.model_validate(album)

            with Session(engine) as db:
                # -- Only add Album if it doesn't exist -- #
                if db.exec(select(Album).where(Album.albumCoverURL == album.albumCoverURL)).first() is None:
                    # c.print(f'album: "{album}"')
                    db.add(db_album)
                    db.commit()
                    db.refresh(db_album)
                    # c.print(db_album)
                    print('Album :', {k:v for k,v in db_album.dict().items() if "ID" in k or "Name" in k})

                    # albumID = db_album.albumID
                    images.append(Image(
                        resolution=getIMG(secure_api/album_image),
                        imageURL=album_image_url,
                        imageType="Album Cover",
                        artistID=db_artist.artistID,
                        albumID=db_album.albumID,
                        # artist=db_artist,
                        # album=db_album,
                    ))
                else:
                    db_album = db.exec(select(Album).where(Album.albumCoverURL == album.albumCoverURL)).first()

            for track_path in sorted(mp3 for mp3 in album_path.glob('**/*.mp3')):
                track_info = MediaInfo.parse(track_path).general_tracks[0]
                mp3_path = urljoin(api_url, str(track_path.relative_to(secure_api)))
                # track_title = re.sub(r'(\d{2}\s-\s)', '', track_path.with_suffix("").name).replace('(Explicit)', explicit)
                track_title = f'{track_info.track_name} {explicit}' if 'Explicit' in track_path.name else track_info.track_name
                track_num = int(track_info.track_name_position)
                track_date = get_date(track_info.recorded_date)
                track_duration = track_info.other_duration[0]
                genre = str(track_info.genre)

                track = Track(
                    trackName=track_title,
                    trackNumber=track_num,
                    trackURL=mp3_path,
                    genre=genre,
                    recordedDate=str(track_date),
                    duration=track_duration,

                    artistID=db_artist.artistID,
                    albumID=db_album.albumID,
                )
                db_track = track # Track(**track) # Track.model_validate(track)

                with Session(engine) as db:
                    # -- Only add Track if it doesn't exist -- #
                    if db.exec(select(Track).where(Track.trackURL == track.trackURL)).first() is None:
                        # c.print(f'track: "{track}"')
                        db.add(db_track)
                        db.commit()
                        db.refresh(db_track)
                        # c.print(db_track)
                        print('Track :', {k:v for k,v in db_track.dict().items() if "ID" in k or "Name" in k})


    # -- Process All Images -- #
    for img in images:
        db_img = Image.model_validate(img)

        with Session(engine) as db:
            # -- Only add Image if it doesn't exist -- #
            if db.exec(select(Image).where(Image.imageURL == img.imageURL)).first() is None:
                # c.print(img)
                db.add(db_img)
                db.commit()
                db.refresh(db_img)
                # c.print(db_img)
            # c.print(f'image: "{img.imageURL}"')
                print('Image :', {k:v for k,v in db_image.dict().items() if "ID" in k or "Name" in k})

# if __name__ == '__main__':
#     insert_tracks()
