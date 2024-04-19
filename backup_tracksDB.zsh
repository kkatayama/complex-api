#!/usr/bin/zsh

sqlite3 tracks.db '.dump "user"' > db_backups/user.sql
sqlite3 tracks.db '.dump "playlist"' > db_backups/playlist.sql
sqlite3 tracks.db '.dump "artist"' > db_backups/artist.sql
sqlite3 tracks.db '.dump "album"' > db_backups/album.sql
sqlite3 tracks.db '.dump "track"' > db_backups/track.sql
sqlite3 tracks.db '.dump "image"' > db_backups/image.sql
sqlite3 tracks.db '.dump "suggestedartist"' > db_backups/suggestedartist.sql
sqlite3 tracks.db '.dump "suggestedalbum"' > db_backups/suggestedalbum.sql
sqlite3 tracks.db '.dump "playlisttrack"' > db_backups/playlisttrack.sql
sqlite3 tracks.db '.dump "playhistory"' > db_backups/playhistory.sql
sqlite3 tracks.db '.dump "favorite"' > db_backups/favorite.sql
sqlite3 tracks.db '.dump' > db_backups/backup.sql
