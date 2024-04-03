PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE playlisttrack (
	"playlistTrackID" INTEGER NOT NULL,
	"playlistID" INTEGER NOT NULL,
	"trackID" INTEGER NOT NULL,
	"trackName" VARCHAR NOT NULL,
	"trackNumber" INTEGER NOT NULL,
	"trackURL" VARCHAR NOT NULL,
	"recordedDate" VARCHAR NOT NULL,
	duration VARCHAR NOT NULL,
	"albumID" INTEGER NOT NULL,
	"artistID" INTEGER NOT NULL,
	PRIMARY KEY ("playlistTrackID")
);
INSERT INTO playlisttrack VALUES(1,1,1,'Hold On (feat. Becky Hill)',1,'https://api.mangoboat.tv/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3','2020-10-30','3 min 43 s',1,1);
INSERT INTO playlisttrack VALUES(2,1,2,'Mixed Emotions (feat. Montell2099)',2,'https://api.mangoboat.tv/music/Netsky/Second Nature/02 - Mixed Emotions (feat. Montell2099).mp3','2020-10-30','4 min 27 s',1,1);
INSERT INTO playlisttrack VALUES(3,1,3,'Destiny (feat. Jozzy)',3,'https://api.mangoboat.tv/music/Netsky/Second Nature/03 - Destiny (feat. Jozzy).mp3','2020-10-30','4 min 2 s',1,1);
INSERT INTO playlisttrack VALUES(4,3,1,'Hold On (feat. Becky Hill)',1,'https://api.mangoboat.tv/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3','2020-10-30','3 min 43 s',1,1);
INSERT INTO playlisttrack VALUES(5,7,1,'Hold On (feat. Becky Hill)',1,'https://api.mangoboat.tv/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3','2020-10-30','3 min 43 s',1,1);
INSERT INTO playlisttrack VALUES(6,7,2,'Mixed Emotions (feat. Montell2099)',2,'https://api.mangoboat.tv/music/Netsky/Second Nature/02 - Mixed Emotions (feat. Montell2099).mp3','2020-10-30','4 min 27 s',1,1);
INSERT INTO playlisttrack VALUES(7,7,3,'Destiny (feat. Jozzy)',3,'https://api.mangoboat.tv/music/Netsky/Second Nature/03 - Destiny (feat. Jozzy).mp3','2020-10-30','4 min 2 s',1,1);
INSERT INTO playlisttrack VALUES(8,8,123,'I''M THAT GIRL 🅴',1,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/01 - I''M THAT GIRL (Explicit).mp3','2022-07-29','3 min 28 s',9,4);
INSERT INTO playlisttrack VALUES(9,8,124,'COZY 🅴',2,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/02 - COZY (Explicit).mp3','2022-07-29','3 min 30 s',9,4);
-- -- CREATE TABLE user (
-- -- 	"userID" INTEGER NOT NULL,
-- -- 	"userRole" VARCHAR NOT NULL,
-- -- 	username VARCHAR NOT NULL,
-- -- 	password VARCHAR NOT NULL,
-- -- 	"loginStatus" BOOLEAN NOT NULL,
-- -- 	PRIMARY KEY ("userID")
-- -- );
-- INSERT INTO user VALUES(1,'Customer','teddy1','$2b$12$/tR8/axgD6HqR/Te/.SwU.acJ0NBS505H879P8LH23ouDBJdcB/BS',1);
-- INSERT INTO user VALUES(3,'Customer','test3','$2b$12$M3vZePicGwu5rsPVUn8aF.gQg4YrWjlcFZNabcS8J6AuOcF5lmw92',0);
-- INSERT INTO user VALUES(4,'Customer','jungria47','$2b$12$WT18oSQFDeqntuCDjBQp3uf370evrv3Wuv9Y0hffGnAbUe3L9Xaa2',1);
-- INSERT INTO user VALUES(5,'Customer','teddy','$2b$12$AIT41DRGuRmB.vBYJBr5.uC5ZM.lv7T0wa/PKWgeHRj8ynAY/ipmC',1);
-- INSERT INTO user VALUES(6,'Customer','kae','$2b$12$2NiqG4cTNwZD22UiZJoDPukrIV/.qmezCFZ/U13i35K7tklrqr.4i',1);
-- INSERT INTO user VALUES(7,'Customer','adriscal','$2b$12$3hZN7ivJ1aIZu5lKPd3/eO.6SWe0ELWUF8ETHxAg0QqO2Nj54bweC',1);
-- INSERT INTO user VALUES(8,'Customer','testuser2','$2b$12$E7ftO7QTEsymjmermn2zOuq9e.8CMsEkdIXfrWnPfSOgYi/O/JZqm',0);
-- -- CREATE TABLE playlist (
-- -- 	"playlistID" INTEGER NOT NULL,
-- -- 	"playlistName" VARCHAR NOT NULL,
-- -- 	"playlistLength" INTEGER NOT NULL,
-- -- 	"creationDate" VARCHAR NOT NULL,
-- -- 	"userID" INTEGER,
-- -- 	PRIMARY KEY ("playlistID"),
-- -- 	FOREIGN KEY("userID") REFERENCES user ("userID")
-- -- );
-- INSERT INTO playlist VALUES(1,'Teddy''s playlist',0,'2024-03-30',1);
-- INSERT INTO playlist VALUES(2,'Test''s playlist',0,'2024-03-30',1);
-- INSERT INTO playlist VALUES(3,'Teddy''s new playlist',0,'2024-04-01',1);
-- INSERT INTO playlist VALUES(4,'This is a playlist',0,'2024-04-01',4);
-- INSERT INTO playlist VALUES(7,'teddy''s playlist',3,'2024-04-02',5);
-- INSERT INTO playlist VALUES(8,'teddy''s playlist 2',2,'2024-04-02',5);
-- -- CREATE TABLE playhistory (
-- -- 	"playhistoryID" INTEGER NOT NULL,
-- -- 	"userID" INTEGER,
-- -- 	"playDate" VARCHAR NOT NULL,
-- -- 	"trackID" INTEGER,
-- -- 	"trackName" VARCHAR NOT NULL,
-- -- 	"trackNumber" INTEGER NOT NULL,
-- -- 	"trackURL" VARCHAR NOT NULL,
-- -- 	"recordedDate" VARCHAR NOT NULL,
-- -- 	duration VARCHAR NOT NULL,
-- -- 	"albumID" INTEGER,
-- -- 	"artistID" INTEGER,
-- -- 	PRIMARY KEY ("playhistoryID"),
-- -- 	FOREIGN KEY("userID") REFERENCES user ("userID"),
-- -- 	FOREIGN KEY("trackID") REFERENCES track ("trackID"),
-- -- 	FOREIGN KEY("albumID") REFERENCES album ("albumID"),
-- -- 	FOREIGN KEY("artistID") REFERENCES artist ("artistID")
-- -- );
-- INSERT INTO playhistory VALUES(1,1,'2024-04-01',1,'Hold On (feat. Becky Hill)',1,'https://api.mangoboat.tv/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3','2020-10-30','3 min 43 s',1,1);
-- INSERT INTO playhistory VALUES(2,1,'2024-04-01',2,'Mixed Emotions (feat. Montell2099)',2,'https://api.mangoboat.tv/music/Netsky/Second Nature/02 - Mixed Emotions (feat. Montell2099).mp3','2020-10-30','4 min 27 s',1,1);
-- INSERT INTO playhistory VALUES(3,1,'2024-04-01',29,'When Darkness Falls',11,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/11 - When Darkness Falls.mp3','2012-11-19','3 min 52 s',2,1);
-- -- CREATE INDEX "ix_artist_artistName" ON artist ("artistName");
-- -- CREATE INDEX "ix_artist_artistPhotoURL" ON artist ("artistPhotoURL");
-- -- CREATE INDEX "ix_playlisttrack_playlistID" ON playlisttrack ("playlistID");
-- -- CREATE INDEX ix_user_username ON user (username);
-- -- CREATE INDEX "ix_image_imageURL" ON image ("imageURL");
-- -- CREATE INDEX ix_album_year ON album (year);
-- -- CREATE INDEX "ix_album_numSongs" ON album ("numSongs");
-- -- CREATE INDEX "ix_album_albumName" ON album ("albumName");
-- -- CREATE INDEX "ix_album_albumCoverURL" ON album ("albumCoverURL");
-- -- CREATE INDEX "ix_playlist_playlistName" ON playlist ("playlistName");
-- -- CREATE INDEX "ix_playlist_creationDate" ON playlist ("creationDate");
-- -- CREATE INDEX "ix_track_trackURL" ON track ("trackURL");
-- -- CREATE INDEX "ix_track_recordedDate" ON track ("recordedDate");
-- -- CREATE INDEX "ix_track_trackName" ON track ("trackName");
-- -- CREATE INDEX "ix_playhistory_trackName" ON playhistory ("trackName");
-- -- CREATE INDEX "ix_playhistory_trackURL" ON playhistory ("trackURL");
-- -- CREATE INDEX "ix_playhistory_playDate" ON playhistory ("playDate");
-- -- CREATE INDEX "ix_playhistory_recordedDate" ON playhistory ("recordedDate");
COMMIT;
