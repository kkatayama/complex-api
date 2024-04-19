import mimetypes
import os

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, Header
from fastapi.responses import FileResponse, StreamingResponse
from sqlmodel import Session, select

from secure_api.models.models import User
from secure_api.database.database import get_session
from secure_api.auth.auth_api import get_currentUser
# import httpx



media_router = APIRouter()#dependencies=[Depends(get_currentUser)])


mimetypes.init()
CONTENT_CHUNK_SIZE=1024
@media_router.get("/music/{name:path}", tags=["Stream-Media"])
def stream_file(name:str, range: Optional[str] = Header(None), db: Session = Depends(get_session)): #, me: User = Depends(get_currentUser)):
    file_path = str(Path('secure_api', 'music', name))
    # print(f'\tFILE = "{file_path}"')
    if name.endswith('.jpg'):
        return FileResponse(file_path, media_type="image/jpeg")

    def chunk_generator_from_stream(stream, chunk_size, start, size):
        bytes_read = 0
        stream.seek(start)
        while bytes_read < size:
            bytes_to_read = min(chunk_size,size - bytes_read)
            yield stream.read(bytes_to_read)
            bytes_read = bytes_read + bytes_to_read
        stream.close()

    asked = range or "bytes=0-"
    stream = open(file_path, 'rb')
    total_size = os.path.getsize(file_path)
    start_byte = int(asked.split("=")[-1].split('-')[0])
    content_type, _ = mimetypes.guess_type(name)

    return StreamingResponse(
        chunk_generator_from_stream(
            stream,
            start=start_byte,
            chunk_size=CONTENT_CHUNK_SIZE,
            size=total_size
        )
        ,headers={
            "Accept-Ranges": "bytes",
            "Content-Range": f"bytes {start_byte}-{start_byte+CONTENT_CHUNK_SIZE}/{total_size}",
            "Content-Type": content_type # "video/mp4"
        },
        status_code=206)
