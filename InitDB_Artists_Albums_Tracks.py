# coding: utf-8
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status

from secure_api.database.database import get_session

from sqlmodel import Session, create_engine
from secure_api import configs
from secure_api.models.models import Artist, Album, Playlist, Track, User
from secure_api.schemas.schemas import CreateArtist, CreateAlbum, CreateTrack


from pymediainfo import MediaInfo


sqlite_url = f'sqlite:///./{configs.DB_FILE}'
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


#models.SQLModel.metadata.create_all(engine)



from imgcat import imgcat
from pathlib import Path
import re




with Session(engine) as db:
    explicit = b"\xf0\x9f\x85\xb4".decode()
    
    music_path = Path.cwd().joinpath('secure_api', 'music')
    for artist_path in music_path.iterdir():
        artist_title = artist_path.name
        artist_image = artist_path.joinpath('poster.jpg')
        artist = CreateArtist(title=artist_title, image_path=str(artist_image))
        print(artist)
        imgcat(artist_image.read_bytes(), width=20, height=20)
        
        db_artist = Artist.model_validate(artist)
        db.add(db_artist)
        db.commit()
        db.refresh(db_artist)
    
        for album_path in [folder for folder in artist_path.iterdir() if folder.is_dir()]:
            album_title = album_path.name
            album_image = album_path.joinpath('cover.jpg')
            album = CreateAlbum(title=album_title, image_path=str(album_image), artist_name=artist_title)
            print(f'\t * \t {album}', end='\n\t    \t')
            imgcat(album_image.read_bytes(), width=20, height=20)

            db_album = Album.model_validate(album)
            db.add(db_album)
            db.commit()
            db.refresh(db_album)
    
            for track_path in sorted(mp3 for mp3 in album_path.glob('**/*.mp3')):
                track_title = re.sub(r'(\d{2}\s-\s)', '', track_path.name).replace('(Explicit)', explicit)
                track_path = str(track_path)
                track_date = MediaInfo.parse(track_path).general_tracks[0].recorded_date
                track = CreateTrack(title=track_title, mp3_path=str(track_path), recorded_date=track_date, artist_name=artist_title, album_name=album_title)
                print(f'\t\t * \t{track}', end='\n\t\t    \t')
                
                db_track = Track.model_validate(track)
                db.add(db_track)
                db.commit()
                db.refresh(db_track)
                
