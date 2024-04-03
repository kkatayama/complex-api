PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE artist (
	"artistID" INTEGER NOT NULL, 
	"artistName" VARCHAR NOT NULL, 
	"artistPhotoURL" VARCHAR NOT NULL, 
	PRIMARY KEY ("artistID")
);
INSERT INTO artist VALUES(1,'Netsky','https://api.mangoboat.tv/music/Netsky/poster.jpg');
INSERT INTO artist VALUES(2,'Alison Wonderland','https://api.mangoboat.tv/music/Alison Wonderland/poster.jpg');
INSERT INTO artist VALUES(3,'Paramore','https://api.mangoboat.tv/music/Paramore/poster.jpg');
INSERT INTO artist VALUES(4,'Beyoncé','https://api.mangoboat.tv/music/Beyoncé/poster.jpg');
INSERT INTO artist VALUES(5,'Ariana Grande','https://api.mangoboat.tv/music/Ariana Grande/poster.jpg');
INSERT INTO artist VALUES(6,'Big Wild','https://api.mangoboat.tv/music/Big Wild/poster.jpg');
INSERT INTO artist VALUES(7,'Anderson .Paak','https://api.mangoboat.tv/music/Anderson .Paak/poster.jpg');
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
CREATE TABLE user (
	"userID" INTEGER NOT NULL, 
	"userRole" VARCHAR NOT NULL, 
	username VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	"loginStatus" BOOLEAN NOT NULL, 
	PRIMARY KEY ("userID")
);
INSERT INTO user VALUES(1,'Customer','teddy1','$2b$12$/tR8/axgD6HqR/Te/.SwU.acJ0NBS505H879P8LH23ouDBJdcB/BS',1);
INSERT INTO user VALUES(3,'Customer','test3','$2b$12$M3vZePicGwu5rsPVUn8aF.gQg4YrWjlcFZNabcS8J6AuOcF5lmw92',0);
INSERT INTO user VALUES(4,'Customer','jungria47','$2b$12$WT18oSQFDeqntuCDjBQp3uf370evrv3Wuv9Y0hffGnAbUe3L9Xaa2',1);
INSERT INTO user VALUES(5,'Customer','teddy','$2b$12$AIT41DRGuRmB.vBYJBr5.uC5ZM.lv7T0wa/PKWgeHRj8ynAY/ipmC',1);
INSERT INTO user VALUES(6,'Customer','kae','$2b$12$2NiqG4cTNwZD22UiZJoDPukrIV/.qmezCFZ/U13i35K7tklrqr.4i',1);
INSERT INTO user VALUES(7,'Customer','adriscal','$2b$12$3hZN7ivJ1aIZu5lKPd3/eO.6SWe0ELWUF8ETHxAg0QqO2Nj54bweC',1);
INSERT INTO user VALUES(8,'Customer','testuser2','$2b$12$E7ftO7QTEsymjmermn2zOuq9e.8CMsEkdIXfrWnPfSOgYi/O/JZqm',0);
CREATE TABLE image (
	"imageID" INTEGER NOT NULL, 
	resolution VARCHAR NOT NULL, 
	"imageURL" VARCHAR NOT NULL, 
	"imageType" VARCHAR NOT NULL, 
	PRIMARY KEY ("imageID")
);
INSERT INTO image VALUES(1,'1000x1000','https://api.mangoboat.tv/music/Netsky/poster.jpg','Artist Photo');
INSERT INTO image VALUES(2,'1400x1400','https://api.mangoboat.tv/music/Netsky/Second Nature/cover.jpg','Album Cover');
INSERT INTO image VALUES(3,'1400x1400','https://api.mangoboat.tv/music/Netsky/2 Deluxe/cover.jpg','Album Cover');
INSERT INTO image VALUES(4,'1200x1200','https://api.mangoboat.tv/music/Alison Wonderland/poster.jpg','Artist Photo');
INSERT INTO image VALUES(5,'1400x1400','https://api.mangoboat.tv/music/Alison Wonderland/Run/cover.jpg','Album Cover');
INSERT INTO image VALUES(6,'1200x1200','https://api.mangoboat.tv/music/Paramore/poster.jpg','Artist Photo');
INSERT INTO image VALUES(7,'1200x1200','https://api.mangoboat.tv/music/Paramore/Brand New Eyes/cover.jpg','Album Cover');
INSERT INTO image VALUES(8,'1400x1400','https://api.mangoboat.tv/music/Paramore/Paramore/cover.jpg','Album Cover');
INSERT INTO image VALUES(9,'1200x1200','https://api.mangoboat.tv/music/Paramore/This Is Why/cover.jpg','Album Cover');
INSERT INTO image VALUES(10,'1400x1400','https://api.mangoboat.tv/music/Paramore/After Laughter/cover.jpg','Album Cover');
INSERT INTO image VALUES(11,'1200x1200','https://api.mangoboat.tv/music/Paramore/Riot!/cover.jpg','Album Cover');
INSERT INTO image VALUES(12,'1000x1000','https://api.mangoboat.tv/music/Beyoncé/poster.jpg','Artist Photo');
INSERT INTO image VALUES(13,'1400x1400','https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/cover.jpg','Album Cover');
INSERT INTO image VALUES(14,'1200x1200','https://api.mangoboat.tv/music/Beyoncé/DELRESTO (ECHOES)/cover.jpg','Album Cover');
INSERT INTO image VALUES(15,'1080x1080','https://api.mangoboat.tv/music/Ariana Grande/poster.jpg','Artist Photo');
INSERT INTO image VALUES(16,'1400x1400','https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/cover.jpg','Album Cover');
INSERT INTO image VALUES(17,'1080x1080','https://api.mangoboat.tv/music/Big Wild/poster.jpg','Artist Photo');
INSERT INTO image VALUES(18,'1400x1400','https://api.mangoboat.tv/music/Big Wild/Superdream/cover.jpg','Album Cover');
INSERT INTO image VALUES(19,'300x300','https://api.mangoboat.tv/music/Big Wild/Invincible EP/cover.jpg','Album Cover');
INSERT INTO image VALUES(20,'1000x1000','https://api.mangoboat.tv/music/Anderson .Paak/poster.jpg','Artist Photo');
INSERT INTO image VALUES(21,'1400x1400','https://api.mangoboat.tv/music/Anderson .Paak/Malibu/cover.jpg','Album Cover');
CREATE TABLE album (
	"albumID" INTEGER NOT NULL, 
	"albumName" VARCHAR NOT NULL, 
	"numSongs" INTEGER NOT NULL, 
	year INTEGER NOT NULL, 
	"albumCoverURL" VARCHAR NOT NULL, 
	"artistID" INTEGER, 
	PRIMARY KEY ("albumID"), 
	FOREIGN KEY("artistID") REFERENCES artist ("artistID")
);
INSERT INTO album VALUES(1,'Second Nature',18,2020,'https://api.mangoboat.tv/music/Netsky/Second Nature/cover.jpg',1);
INSERT INTO album VALUES(2,'2 Deluxe',30,2012,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/cover.jpg',1);
INSERT INTO album VALUES(3,'Run',12,2015,'https://api.mangoboat.tv/music/Alison Wonderland/Run/cover.jpg',2);
INSERT INTO album VALUES(4,'Brand New Eyes',11,2009,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/cover.jpg',3);
INSERT INTO album VALUES(5,'Paramore',17,2013,'https://api.mangoboat.tv/music/Paramore/Paramore/cover.jpg',3);
INSERT INTO album VALUES(6,'This Is Why',10,2023,'https://api.mangoboat.tv/music/Paramore/This Is Why/cover.jpg',3);
INSERT INTO album VALUES(7,'After Laughter',12,2017,'https://api.mangoboat.tv/music/Paramore/After Laughter/cover.jpg',3);
INSERT INTO album VALUES(8,'Riot!',12,2007,'https://api.mangoboat.tv/music/Paramore/Riot!/cover.jpg',3);
INSERT INTO album VALUES(9,'RENAISSANCE',16,2022,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/cover.jpg',4);
INSERT INTO album VALUES(10,'DELRESTO (ECHOES)',1,2023,'https://api.mangoboat.tv/music/Beyoncé/DELRESTO (ECHOES)/cover.jpg',4);
INSERT INTO album VALUES(11,'Dangerous Woman',17,2021,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/cover.jpg',5);
INSERT INTO album VALUES(12,'Superdream',12,2019,'https://api.mangoboat.tv/music/Big Wild/Superdream/cover.jpg',6);
INSERT INTO album VALUES(13,'Invincible - EP',5,2017,'https://api.mangoboat.tv/music/Big Wild/Invincible EP/cover.jpg',6);
INSERT INTO album VALUES(14,'Malibu',16,2016,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/cover.jpg',7);
CREATE TABLE playlist (
	"playlistID" INTEGER NOT NULL, 
	"playlistName" VARCHAR NOT NULL, 
	"playlistLength" INTEGER NOT NULL, 
	"creationDate" VARCHAR NOT NULL, 
	"userID" INTEGER, 
	PRIMARY KEY ("playlistID"), 
	FOREIGN KEY("userID") REFERENCES user ("userID")
);
INSERT INTO playlist VALUES(1,'Teddy''s playlist',0,'2024-03-30',1);
INSERT INTO playlist VALUES(2,'Test''s playlist',0,'2024-03-30',1);
INSERT INTO playlist VALUES(3,'Teddy''s new playlist',0,'2024-04-01',1);
INSERT INTO playlist VALUES(4,'This is a playlist',0,'2024-04-01',4);
INSERT INTO playlist VALUES(7,'teddy''s playlist',3,'2024-04-02',5);
INSERT INTO playlist VALUES(8,'teddy''s playlist 2',2,'2024-04-02',5);
CREATE TABLE track (
	"trackID" INTEGER NOT NULL, 
	"trackName" VARCHAR NOT NULL, 
	"trackNumber" INTEGER NOT NULL, 
	"trackURL" VARCHAR NOT NULL, 
	genre VARCHAR NOT NULL, 
	"recordedDate" VARCHAR NOT NULL, 
	duration VARCHAR NOT NULL, 
	"albumID" INTEGER, 
	"artistID" INTEGER, 
	PRIMARY KEY ("trackID"), 
	FOREIGN KEY("albumID") REFERENCES album ("albumID"), 
	FOREIGN KEY("artistID") REFERENCES artist ("artistID")
);
INSERT INTO track VALUES(1,'Hold On (feat. Becky Hill)',1,'https://api.mangoboat.tv/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3','Dance','2020-10-30','3 min 43 s',1,1);
INSERT INTO track VALUES(2,'Mixed Emotions (feat. Montell2099)',2,'https://api.mangoboat.tv/music/Netsky/Second Nature/02 - Mixed Emotions (feat. Montell2099).mp3','Dance','2020-10-30','4 min 27 s',1,1);
INSERT INTO track VALUES(3,'Destiny (feat. Jozzy)',3,'https://api.mangoboat.tv/music/Netsky/Second Nature/03 - Destiny (feat. Jozzy).mp3','Dance','2020-10-30','4 min 2 s',1,1);
INSERT INTO track VALUES(4,'I Choose You',4,'https://api.mangoboat.tv/music/Netsky/Second Nature/04 - I Choose You.mp3','Dance','2020-10-30','2 min 58 s',1,1);
INSERT INTO track VALUES(5,'Broken Bottles',5,'https://api.mangoboat.tv/music/Netsky/Second Nature/05 - Broken Bottles.mp3','Dance','2020-10-30','3 min 37 s',1,1);
INSERT INTO track VALUES(6,'Blend (feat. Afronaut Zu)',6,'https://api.mangoboat.tv/music/Netsky/Second Nature/06 - Blend (feat. Afronaut Zu).mp3','Dance','2020-10-30','3 min 25 s',1,1);
INSERT INTO track VALUES(7,'Let Me Hold You',7,'https://api.mangoboat.tv/music/Netsky/Second Nature/07 - Let Me Hold You.mp3','Dance','2020-10-30','3 min 22 s',1,1);
INSERT INTO track VALUES(8,'Look At Me Go (feat. Darren Styles)',8,'https://api.mangoboat.tv/music/Netsky/Second Nature/08 - Look At Me Go (feat. Darren Styles).mp3','Dance','2020-10-30','3 min 46 s',1,1);
INSERT INTO track VALUES(9,'Don''t Care What People Say',9,'https://api.mangoboat.tv/music/Netsky/Second Nature/09 - Don''t Care What People Say.mp3','Dance','2020-10-30','3 min 25 s',1,1);
INSERT INTO track VALUES(10,'Complicated',10,'https://api.mangoboat.tv/music/Netsky/Second Nature/10 - Complicated.mp3','Dance','2020-10-30','3 min 46 s',1,1);
INSERT INTO track VALUES(11,'Free',11,'https://api.mangoboat.tv/music/Netsky/Second Nature/11 - Free.mp3','Dance','2020-10-30','3 min 21 s',1,1);
INSERT INTO track VALUES(12,'I See The Future In Your Eyes',12,'https://api.mangoboat.tv/music/Netsky/Second Nature/12 - I See The Future In Your Eyes.mp3','Dance','2020-10-30','4 min 15 s',1,1);
INSERT INTO track VALUES(13,'Waiting All Day To Get To You',13,'https://api.mangoboat.tv/music/Netsky/Second Nature/13 - Waiting All Day To Get To You.mp3','Dance','2020-10-30','2 min 55 s',1,1);
INSERT INTO track VALUES(14,'Power',14,'https://api.mangoboat.tv/music/Netsky/Second Nature/14 - Power.mp3','Dance','2020-10-30','3 min 46 s',1,1);
INSERT INTO track VALUES(15,'Float',15,'https://api.mangoboat.tv/music/Netsky/Second Nature/15 - Float.mp3','Dance','2020-10-30','3 min 20 s',1,1);
INSERT INTO track VALUES(16,'Dreaming Of You (feat. Elias)',16,'https://api.mangoboat.tv/music/Netsky/Second Nature/16 - Dreaming Of You (feat. Elias).mp3','Dance','2020-10-30','3 min 7 s',1,1);
INSERT INTO track VALUES(17,'Everybody Loves The Sunshine (feat. Daddy Waku & Chantal Kashala)',17,'https://api.mangoboat.tv/music/Netsky/Second Nature/17 - Everybody Loves The Sunshine (feat. Daddy Waku & Chantal Kashala).mp3','Dance','2020-10-30','3 min 20 s',1,1);
INSERT INTO track VALUES(18,'Basic Instinct',18,'https://api.mangoboat.tv/music/Netsky/Second Nature/18 - Basic Instinct.mp3','Dance','2020-10-30','3 min 57 s',1,1);
INSERT INTO track VALUES(19,'Love Has Gone',1,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/01 - Love Has Gone.mp3','Dance','2012-11-19','4 min 11 s',2,1);
INSERT INTO track VALUES(20,'The Whistle Song',2,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/02 - The Whistle Song.mp3','Dance','2012-11-19','4 min 39 s',2,1);
INSERT INTO track VALUES(21,'Wanna Die For You',3,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/03 - Wanna Die For You.mp3','Dance','2012-11-19','4 min 17 s',2,1);
INSERT INTO track VALUES(22,'Come Alive',4,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/04 - Come Alive.mp3','Dance','2012-11-19','4 min 10 s',2,1);
INSERT INTO track VALUES(23,'Give & Take',5,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/05 - Give & Take.mp3','Dance','2012-11-19','4 min 12 s',2,1);
INSERT INTO track VALUES(24,'Get Away From Here',6,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/06 - Get Away From Here.mp3','Dance','2012-11-19','4 min 13 s',2,1);
INSERT INTO track VALUES(25,'911',7,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/07 - 911.mp3','Dance','2012-11-19','3 min 23 s',2,1);
INSERT INTO track VALUES(26,'Squad Up',8,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/08 - Squad Up.mp3','Dance','2012-11-19','3 min 44 s',2,1);
INSERT INTO track VALUES(27,'Jetlag Funk',9,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/09 - Jetlag Funk.mp3','Dance','2012-11-19','5 min 18 s',2,1);
INSERT INTO track VALUES(28,'Puppy',10,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/10 - Puppy.mp3','Dance','2012-11-19','4 min 20 s',2,1);
INSERT INTO track VALUES(29,'When Darkness Falls',11,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/11 - When Darkness Falls.mp3','Dance','2012-11-19','3 min 52 s',2,1);
INSERT INTO track VALUES(30,'Detonate',12,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/12 - Detonate.mp3','Dance','2012-11-19','3 min 50 s',2,1);
INSERT INTO track VALUES(31,'No Beginning',13,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/13 - No Beginning.mp3','Dance','2012-11-19','5 min 19 s',2,1);
INSERT INTO track VALUES(32,'Dubplate Special',14,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/14 - Dubplate Special.mp3','Dance','2012-11-19','48 s 587 ms',2,1);
INSERT INTO track VALUES(33,'Drawing Straws',15,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/15 - Drawing Straws.mp3','Dance','2012-11-19','4 min 15 s',2,1);
INSERT INTO track VALUES(34,'We Can Only Live Today (Puppy)',16,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/16 - We Can Only Live Today (Puppy).mp3','Dance','2012-11-19','3 min 24 s',2,1);
INSERT INTO track VALUES(35,'500 Days Of Summer',17,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/17 - 500 Days Of Summer.mp3','Dance','2012-11-19','4 min 7 s',2,1);
INSERT INTO track VALUES(36,'Wanna Die For You (Metrik & Netsky Rework)',18,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/18 - Wanna Die For You (Metrik & Netsky Rework).mp3','Dance','2012-11-19','4 min 39 s',2,1);
INSERT INTO track VALUES(37,'Strobot (Netsky Remix)',19,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/19 - Strobot (Netsky Remix).mp3','Dance','2012-11-19','4 min 14 s',2,1);
INSERT INTO track VALUES(38,'No Strings Attached',20,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/20 - No Strings Attached.mp3','Dance','2012-11-19','5 min 14 s',2,1);
INSERT INTO track VALUES(39,'Get Away From Here (Instrumental)',21,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/21 - Get Away From Here (Instrumental).mp3','Dance','2012-11-19','4 min 15 s',2,1);
INSERT INTO track VALUES(40,'Cous Cous',22,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/22 - Cous Cous.mp3','Dance','2012-11-19','4 min 31 s',2,1);
INSERT INTO track VALUES(41,'Squad Up (Instrumental)',23,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/23 - Squad Up (Instrumental).mp3','Dance','2012-11-19','3 min 44 s',2,1);
INSERT INTO track VALUES(42,'Love Has Gone (Netsky''s Love Must Go On Refix)',24,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/24 - Love Has Gone (Netsky''s Love Must Go On Refix).mp3','Dance','2012-11-19','3 min 41 s',2,1);
INSERT INTO track VALUES(43,'Come Alive (Rockwell Remix)',25,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/25 - Come Alive (Rockwell Remix).mp3','Dance','2012-11-19','5 min 38 s',2,1);
INSERT INTO track VALUES(44,'No Beginning (Downbeat Mix)',26,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/26 - No Beginning (Downbeat Mix).mp3','Dance','2012-11-19','3 min 30 s',2,1);
INSERT INTO track VALUES(45,'Love Has Gone (Other Echoes Remix)',27,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/27 - Love Has Gone (Other Echoes Remix).mp3','Dance','2012-11-19','4 min 30 s',2,1);
INSERT INTO track VALUES(46,'Wanna Die For You (Live at Pukkelpop 2012)',28,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/28 - Wanna Die For You (Live at Pukkelpop 2012).mp3','Dance','2012-11-19','4 min 10 s',2,1);
INSERT INTO track VALUES(47,'Come Alive (Live At Pukkelpop 2012)',29,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/29 - Come Alive (Live At Pukkelpop 2012).mp3','Dance','2012-11-19','4 min 51 s',2,1);
INSERT INTO track VALUES(48,'Give & Take (Live At l''Ancienne Belgique)',30,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/30 - Give & Take (Live At l''Ancienne Belgique).mp3','Dance','2012-11-19','3 min 44 s',2,1);
INSERT INTO track VALUES(49,'Run',1,'https://api.mangoboat.tv/music/Alison Wonderland/Run/01 - Run.mp3','Electro','2015-03-20','3 min 38 s',3,2);
INSERT INTO track VALUES(50,'U Don’t Know (feat. Wayne Coyne)',2,'https://api.mangoboat.tv/music/Alison Wonderland/Run/02 - U Don’t Know (feat. Wayne Coyne).mp3','Electro','2015-03-20','4 min 3 s',3,2);
INSERT INTO track VALUES(51,'Take It To Reality (feat. Safia)',3,'https://api.mangoboat.tv/music/Alison Wonderland/Run/03 - Take It To Reality (feat. Safia).mp3','Electro','2015-03-20','3 min 52 s',3,2);
INSERT INTO track VALUES(52,'Naked (Alison Wonderland X Slumberjack)',4,'https://api.mangoboat.tv/music/Alison Wonderland/Run/04 - Naked (Alison Wonderland X Slumberjack).mp3','Electro','2015-03-20','3 min 17 s',3,2);
INSERT INTO track VALUES(53,'Carry On (feat. Johnny Nelson & GANZ)',5,'https://api.mangoboat.tv/music/Alison Wonderland/Run/05 - Carry On (feat. Johnny Nelson & GANZ).mp3','Electro','2015-03-20','4 min 1 s',3,2);
INSERT INTO track VALUES(54,'I Want U',6,'https://api.mangoboat.tv/music/Alison Wonderland/Run/06 - I Want U.mp3','Electro','2015-03-20','3 min 30 s',3,2);
INSERT INTO track VALUES(55,'Games',7,'https://api.mangoboat.tv/music/Alison Wonderland/Run/07 - Games.mp3','Electro','2015-03-20','3 min 35 s',3,2);
INSERT INTO track VALUES(56,'One More Hit',8,'https://api.mangoboat.tv/music/Alison Wonderland/Run/08 - One More Hit.mp3','Electro','2015-03-20','3 min 24 s',3,2);
INSERT INTO track VALUES(57,'Ignore',9,'https://api.mangoboat.tv/music/Alison Wonderland/Run/09 - Ignore.mp3','Electro','2015-03-20','3 min 54 s',3,2);
INSERT INTO track VALUES(58,'Back It Up (Alison Wonderland X AWE) 🅴',10,'https://api.mangoboat.tv/music/Alison Wonderland/Run/10 - Back It Up (Alison Wonderland X AWE) (Explicit).mp3','Electro','2015-03-20','2 min 13 s',3,2);
INSERT INTO track VALUES(59,'Cold 🅴',11,'https://api.mangoboat.tv/music/Alison Wonderland/Run/11 - Cold (Explicit).mp3','Electro','2015-03-20','3 min 32 s',3,2);
INSERT INTO track VALUES(60,'Already Gone (feat. Brave & Lido) 🅴',12,'https://api.mangoboat.tv/music/Alison Wonderland/Run/12 - Already Gone (feat. Brave & Lido) (Explicit).mp3','Electro','2015-03-20','4 min 1 s',3,2);
INSERT INTO track VALUES(61,'Careful',1,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/01 - Careful.mp3','Alternative','2009-09-28','3 min 50 s',4,3);
INSERT INTO track VALUES(62,'Ignorance',2,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/02 - Ignorance.mp3','Alternative','2009-09-28','3 min 38 s',4,3);
INSERT INTO track VALUES(63,'Playing God',3,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/03 - Playing God.mp3','Alternative','2009-09-28','3 min 2 s',4,3);
INSERT INTO track VALUES(64,'Brick by Boring Brick',4,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/04 - Brick by Boring Brick.mp3','Alternative','2009-09-28','4 min 13 s',4,3);
INSERT INTO track VALUES(65,'Turn It Off',5,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/05 - Turn It Off.mp3','Alternative','2009-09-28','4 min 19 s',4,3);
INSERT INTO track VALUES(66,'The Only Exception',6,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/06 - The Only Exception.mp3','Alternative','2009-09-28','4 min 27 s',4,3);
INSERT INTO track VALUES(67,'Feeling Sorry',7,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/07 - Feeling Sorry.mp3','Alternative','2009-09-28','3 min 5 s',4,3);
INSERT INTO track VALUES(68,'Looking Up',8,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/08 - Looking Up.mp3','Alternative','2009-09-28','3 min 29 s',4,3);
INSERT INTO track VALUES(69,'Where the Lines Overlap',9,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/09 - Where the Lines Overlap.mp3','Alternative','2009-09-28','3 min 18 s',4,3);
INSERT INTO track VALUES(70,'Misguided Ghosts',10,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/10 - Misguided Ghosts.mp3','Alternative','2009-09-28','3 min 1 s',4,3);
INSERT INTO track VALUES(71,'All I Wanted',11,'https://api.mangoboat.tv/music/Paramore/Brand New Eyes/11 - All I Wanted.mp3','Alternative','2009-09-28','3 min 45 s',4,3);
INSERT INTO track VALUES(72,'Fast in My Car',1,'https://api.mangoboat.tv/music/Paramore/Paramore/01 - Fast in My Car.mp3','Alternative','2013-05-04','3 min 42 s',5,3);
INSERT INTO track VALUES(73,'Now',2,'https://api.mangoboat.tv/music/Paramore/Paramore/02 - Now.mp3','Alternative','2013-05-04','4 min 10 s',5,3);
INSERT INTO track VALUES(74,'Grow Up',3,'https://api.mangoboat.tv/music/Paramore/Paramore/03 - Grow Up.mp3','Alternative','2013-05-04','3 min 50 s',5,3);
INSERT INTO track VALUES(75,'Daydreaming',4,'https://api.mangoboat.tv/music/Paramore/Paramore/04 - Daydreaming.mp3','Alternative','2013-05-04','4 min 31 s',5,3);
INSERT INTO track VALUES(76,'Interlude: Moving On',5,'https://api.mangoboat.tv/music/Paramore/Paramore/05 - Interlude_ Moving On.mp3','Alternative','2013-05-04','1 min 30 s',5,3);
INSERT INTO track VALUES(77,'Ain''t It Fun',6,'https://api.mangoboat.tv/music/Paramore/Paramore/06 - Ain''t It Fun.mp3','Alternative','2013-05-04','4 min 56 s',5,3);
INSERT INTO track VALUES(78,'Part II',7,'https://api.mangoboat.tv/music/Paramore/Paramore/07 - Part II.mp3','Alternative','2013-05-04','4 min 41 s',5,3);
INSERT INTO track VALUES(79,'Last Hope',8,'https://api.mangoboat.tv/music/Paramore/Paramore/08 - Last Hope.mp3','Alternative','2013-05-04','5 min 10 s',5,3);
INSERT INTO track VALUES(80,'Still into You',9,'https://api.mangoboat.tv/music/Paramore/Paramore/09 - Still into You.mp3','Alternative','2013-05-04','3 min 36 s',5,3);
INSERT INTO track VALUES(81,'Anklebiters',10,'https://api.mangoboat.tv/music/Paramore/Paramore/10 - Anklebiters.mp3','Alternative','2013-05-04','2 min 17 s',5,3);
INSERT INTO track VALUES(82,'Interlude: Holiday',11,'https://api.mangoboat.tv/music/Paramore/Paramore/11 - Interlude_ Holiday.mp3','Alternative','2013-05-04','1 min 9 s',5,3);
INSERT INTO track VALUES(83,'Proof',12,'https://api.mangoboat.tv/music/Paramore/Paramore/12 - Proof.mp3','Alternative','2013-05-04','3 min 15 s',5,3);
INSERT INTO track VALUES(84,'Hate to See Your Heart Break',13,'https://api.mangoboat.tv/music/Paramore/Paramore/13 - Hate to See Your Heart Break.mp3','Alternative','2013-05-04','5 min 9 s',5,3);
INSERT INTO track VALUES(85,'(One of Those) Crazy Girls',14,'https://api.mangoboat.tv/music/Paramore/Paramore/14 - (One of Those) Crazy Girls.mp3','Alternative','2013-05-04','3 min 32 s',5,3);
INSERT INTO track VALUES(86,'Interlude: I''m Not Angry Anymore',15,'https://api.mangoboat.tv/music/Paramore/Paramore/15 - Interlude_ I''m Not Angry Anymore.mp3','Alternative','2013-05-04','52 s 636 ms',5,3);
INSERT INTO track VALUES(87,'Be Alone',16,'https://api.mangoboat.tv/music/Paramore/Paramore/16 - Be Alone.mp3','Alternative','2013-05-04','3 min 40 s',5,3);
INSERT INTO track VALUES(88,'Future',17,'https://api.mangoboat.tv/music/Paramore/Paramore/17 - Future.mp3','Alternative','2013-05-04','7 min 50 s',5,3);
INSERT INTO track VALUES(89,'This Is Why',1,'https://api.mangoboat.tv/music/Paramore/This Is Why/01 - This Is Why.mp3','Alternative','2023-02-10','3 min 26 s',6,3);
INSERT INTO track VALUES(90,'The News',2,'https://api.mangoboat.tv/music/Paramore/This Is Why/02 - The News.mp3','Alternative','2023-02-10','3 min 7 s',6,3);
INSERT INTO track VALUES(91,'Running Out Of Time',3,'https://api.mangoboat.tv/music/Paramore/This Is Why/03 - Running Out Of Time.mp3','Alternative','2023-02-10','3 min 12 s',6,3);
INSERT INTO track VALUES(92,'C’est Comme Ça',4,'https://api.mangoboat.tv/music/Paramore/This Is Why/04 - C’est Comme Ça.mp3','Alternative','2023-02-10','2 min 29 s',6,3);
INSERT INTO track VALUES(93,'Big Man, Little Dignity',5,'https://api.mangoboat.tv/music/Paramore/This Is Why/05 - Big Man, Little Dignity.mp3','Alternative','2023-02-10','4 min 20 s',6,3);
INSERT INTO track VALUES(94,'You First',6,'https://api.mangoboat.tv/music/Paramore/This Is Why/06 - You First.mp3','Alternative','2023-02-10','4 min 5 s',6,3);
INSERT INTO track VALUES(95,'Figure 8',7,'https://api.mangoboat.tv/music/Paramore/This Is Why/07 - Figure 8.mp3','Alternative','2023-02-10','3 min 25 s',6,3);
INSERT INTO track VALUES(96,'Liar',8,'https://api.mangoboat.tv/music/Paramore/This Is Why/08 - Liar.mp3','Alternative','2023-02-10','4 min 21 s',6,3);
INSERT INTO track VALUES(97,'Crave',9,'https://api.mangoboat.tv/music/Paramore/This Is Why/09 - Crave.mp3','Alternative','2023-02-10','3 min 55 s',6,3);
INSERT INTO track VALUES(98,'Thick Skull',10,'https://api.mangoboat.tv/music/Paramore/This Is Why/10 - Thick Skull.mp3','Alternative','2023-02-10','3 min 53 s',6,3);
INSERT INTO track VALUES(99,'Hard Times',1,'https://api.mangoboat.tv/music/Paramore/After Laughter/01 - Hard Times.mp3','Alternative','2017-12-05','3 min 2 s',7,3);
INSERT INTO track VALUES(100,'Rose-Colored Boy',2,'https://api.mangoboat.tv/music/Paramore/After Laughter/02 - Rose-Colored Boy.mp3','Alternative','2017-12-05','3 min 32 s',7,3);
INSERT INTO track VALUES(101,'Told You So',3,'https://api.mangoboat.tv/music/Paramore/After Laughter/03 - Told You So.mp3','Alternative','2017-12-05','3 min 8 s',7,3);
INSERT INTO track VALUES(102,'Forgiveness',4,'https://api.mangoboat.tv/music/Paramore/After Laughter/04 - Forgiveness.mp3','Alternative','2017-12-05','3 min 39 s',7,3);
INSERT INTO track VALUES(103,'Fake Happy',5,'https://api.mangoboat.tv/music/Paramore/After Laughter/05 - Fake Happy.mp3','Alternative','2017-12-05','3 min 55 s',7,3);
INSERT INTO track VALUES(104,'26',6,'https://api.mangoboat.tv/music/Paramore/After Laughter/06 - 26.mp3','Alternative','2017-12-05','3 min 41 s',7,3);
INSERT INTO track VALUES(105,'Pool',7,'https://api.mangoboat.tv/music/Paramore/After Laughter/07 - Pool.mp3','Alternative','2017-12-05','3 min 52 s',7,3);
INSERT INTO track VALUES(106,'Grudges',8,'https://api.mangoboat.tv/music/Paramore/After Laughter/08 - Grudges.mp3','Alternative','2017-12-05','3 min 7 s',7,3);
INSERT INTO track VALUES(107,'Caught in the Middle',9,'https://api.mangoboat.tv/music/Paramore/After Laughter/09 - Caught in the Middle.mp3','Alternative','2017-12-05','3 min 34 s',7,3);
INSERT INTO track VALUES(108,'Idle Worship',10,'https://api.mangoboat.tv/music/Paramore/After Laughter/10 - Idle Worship.mp3','Alternative','2017-12-05','3 min 18 s',7,3);
INSERT INTO track VALUES(109,'No Friend',11,'https://api.mangoboat.tv/music/Paramore/After Laughter/11 - No Friend.mp3','Alternative','2017-12-05','3 min 23 s',7,3);
INSERT INTO track VALUES(110,'Tell Me How',12,'https://api.mangoboat.tv/music/Paramore/After Laughter/12 - Tell Me How.mp3','Alternative','2017-12-05','4 min 20 s',7,3);
INSERT INTO track VALUES(111,'For a Pessimist, I''m Pretty Optimistic',1,'https://api.mangoboat.tv/music/Paramore/Riot!/01 - For a Pessimist, I''m Pretty Optimistic.mp3','Alternative','2007-11-06','3 min 48 s',8,3);
INSERT INTO track VALUES(112,'That''s What You Get',2,'https://api.mangoboat.tv/music/Paramore/Riot!/02 - That''s What You Get.mp3','Alternative','2007-11-06','3 min 40 s',8,3);
INSERT INTO track VALUES(113,'Hallelujah',3,'https://api.mangoboat.tv/music/Paramore/Riot!/03 - Hallelujah.mp3','Alternative','2007-11-06','3 min 23 s',8,3);
INSERT INTO track VALUES(114,'Misery Business',4,'https://api.mangoboat.tv/music/Paramore/Riot!/04 - Misery Business.mp3','Alternative','2007-11-06','3 min 31 s',8,3);
INSERT INTO track VALUES(115,'When It Rains',5,'https://api.mangoboat.tv/music/Paramore/Riot!/05 - When It Rains.mp3','Alternative','2007-11-06','3 min 35 s',8,3);
INSERT INTO track VALUES(116,'Let the Flames Begin',6,'https://api.mangoboat.tv/music/Paramore/Riot!/06 - Let the Flames Begin.mp3','Alternative','2007-11-06','3 min 18 s',8,3);
INSERT INTO track VALUES(117,'Miracle',7,'https://api.mangoboat.tv/music/Paramore/Riot!/07 - Miracle.mp3','Alternative','2007-11-06','3 min 29 s',8,3);
INSERT INTO track VALUES(118,'crushcrushcrush',8,'https://api.mangoboat.tv/music/Paramore/Riot!/08 - crushcrushcrush.mp3','Alternative','2007-11-06','3 min 9 s',8,3);
INSERT INTO track VALUES(119,'We Are Broken',9,'https://api.mangoboat.tv/music/Paramore/Riot!/09 - We Are Broken.mp3','Alternative','2007-11-06','3 min 38 s',8,3);
INSERT INTO track VALUES(120,'Fences',10,'https://api.mangoboat.tv/music/Paramore/Riot!/10 - Fences.mp3','Alternative','2007-11-06','3 min 19 s',8,3);
INSERT INTO track VALUES(121,'Born for This',11,'https://api.mangoboat.tv/music/Paramore/Riot!/11 - Born for This.mp3','Alternative','2007-11-06','3 min 58 s',8,3);
INSERT INTO track VALUES(122,'Misery Business (Acoustic Version)',12,'https://api.mangoboat.tv/music/Paramore/Riot!/12 - Misery Business (Acoustic Version).mp3','Alternative','2007-11-06','3 min 14 s',8,3);
INSERT INTO track VALUES(123,'I''M THAT GIRL 🅴',1,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/01 - I''M THAT GIRL (Explicit).mp3','Pop','2022-07-29','3 min 28 s',9,4);
INSERT INTO track VALUES(124,'COZY 🅴',2,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/02 - COZY (Explicit).mp3','Pop','2022-07-29','3 min 30 s',9,4);
INSERT INTO track VALUES(125,'ALIEN SUPERSTAR 🅴',3,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/03 - ALIEN SUPERSTAR (Explicit).mp3','Pop','2022-07-29','3 min 35 s',9,4);
INSERT INTO track VALUES(126,'CUFF IT 🅴',4,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/04 - CUFF IT (Explicit).mp3','Pop','2022-07-29','3 min 45 s',9,4);
INSERT INTO track VALUES(127,'ENERGY',5,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/05 - ENERGY.mp3','Pop','2022-07-29','1 min 56 s',9,4);
INSERT INTO track VALUES(128,'BREAK MY SOUL',6,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/06 - BREAK MY SOUL.mp3','Pop','2022-07-29','4 min 38 s',9,4);
INSERT INTO track VALUES(129,'CHURCH GIRL 🅴',7,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/07 - CHURCH GIRL (Explicit).mp3','Pop','2022-07-29','3 min 44 s',9,4);
INSERT INTO track VALUES(130,'PLASTIC OFF THE SOFA',8,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/08 - PLASTIC OFF THE SOFA.mp3','Pop','2022-07-29','4 min 14 s',9,4);
INSERT INTO track VALUES(131,'VIRGO''S GROOVE 🅴',9,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/09 - VIRGO''S GROOVE (Explicit).mp3','Pop','2022-07-29','6 min 8 s',9,4);
INSERT INTO track VALUES(132,'MOVE',10,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/10 - MOVE.mp3','Pop','2022-07-29','3 min 23 s',9,4);
INSERT INTO track VALUES(133,'HEATED 🅴',11,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/11 - HEATED (Explicit).mp3','Pop','2022-07-29','4 min 20 s',9,4);
INSERT INTO track VALUES(134,'THIQUE 🅴',12,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/12 - THIQUE (Explicit).mp3','Pop','2022-07-29','4 min 4 s',9,4);
INSERT INTO track VALUES(135,'ALL UP IN YOUR MIND 🅴',13,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/13 - ALL UP IN YOUR MIND (Explicit).mp3','Pop','2022-07-29','2 min 49 s',9,4);
INSERT INTO track VALUES(136,'AMERICA HAS A PROBLEM 🅴',14,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/14 - AMERICA HAS A PROBLEM (Explicit).mp3','Pop','2022-07-29','3 min 18 s',9,4);
INSERT INTO track VALUES(137,'PURE/HONEY 🅴',15,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/15 - PURE_HONEY (Explicit).mp3','Pop','2022-07-29','4 min 48 s',9,4);
INSERT INTO track VALUES(138,'SUMMER RENAISSANCE 🅴',16,'https://api.mangoboat.tv/music/Beyoncé/RENAISSANCE/16 - SUMMER RENAISSANCE (Explicit).mp3','Pop','2022-07-29','4 min 34 s',9,4);
INSERT INTO track VALUES(139,'DELRESTO (ECHOES)',1,'https://api.mangoboat.tv/music/Beyoncé/DELRESTO (ECHOES)/01 - DELRESTO (ECHOES).mp3','Rap/Hip Hop','2023-07-26','4 min 34 s',10,4);
INSERT INTO track VALUES(140,'Moonlight',1,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/01 - Moonlight.mp3','Pop','2021-05-20','3 min 22 s',11,5);
INSERT INTO track VALUES(141,'Dangerous Woman',2,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/02 - Dangerous Woman.mp3','Pop','2021-05-20','3 min 55 s',11,5);
INSERT INTO track VALUES(142,'Be Alright',3,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/03 - Be Alright.mp3','Pop','2021-05-20','2 min 59 s',11,5);
INSERT INTO track VALUES(143,'Into You',4,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/04 - Into You.mp3','Pop','2021-05-20','4 min 4 s',11,5);
INSERT INTO track VALUES(144,'Side To Side (feat. Nicki Minaj) 🅴',5,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/05 - Side To Side (feat. Nicki Minaj) (Explicit).mp3','Pop','2021-05-20','3 min 46 s',11,5);
INSERT INTO track VALUES(145,'Let Me Love You (feat. Lil Wayne)',6,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/06 - Let Me Love You (feat. Lil Wayne).mp3','Pop','2021-05-20','3 min 43 s',11,5);
INSERT INTO track VALUES(146,'Greedy',7,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/07 - Greedy.mp3','Pop','2021-05-20','3 min 34 s',11,5);
INSERT INTO track VALUES(147,'Leave Me Lonely (feat. Macy Gray)',8,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/08 - Leave Me Lonely (feat. Macy Gray).mp3','Pop','2021-05-20','3 min 49 s',11,5);
INSERT INTO track VALUES(148,'Everyday (feat. Future) 🅴',9,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/09 - Everyday (feat. Future) (Explicit).mp3','Pop','2021-05-20','3 min 14 s',11,5);
INSERT INTO track VALUES(149,'Sometimes',10,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/10 - Sometimes.mp3','Pop','2021-05-20','3 min 46 s',11,5);
INSERT INTO track VALUES(150,'I Don''t Care 🅴',11,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/11 - I Don''t Care (Explicit).mp3','Pop','2021-05-20','2 min 58 s',11,5);
INSERT INTO track VALUES(151,'Bad Decisions 🅴',12,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/12 - Bad Decisions (Explicit).mp3','Pop','2021-05-20','3 min 46 s',11,5);
INSERT INTO track VALUES(152,'Touch It',13,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/13 - Touch It.mp3','Pop','2021-05-20','4 min 20 s',11,5);
INSERT INTO track VALUES(153,'Knew Better / Forever Boy',14,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/14 - Knew Better _ Forever Boy.mp3','Pop','2021-05-20','4 min 59 s',11,5);
INSERT INTO track VALUES(154,'Thinking Bout You 🅴',15,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/15 - Thinking Bout You (Explicit).mp3','Pop','2021-05-20','3 min 20 s',11,5);
INSERT INTO track VALUES(155,'Step On Up',16,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/16 - Step On Up.mp3','Pop','2021-05-20','3 min 0 s',11,5);
INSERT INTO track VALUES(156,'Jason''s Song (Gave It Away) 🅴',17,'https://api.mangoboat.tv/music/Ariana Grande/Dangerous Woman/17 - Jason''s Song (Gave It Away) (Explicit).mp3','Pop','2021-05-20','4 min 24 s',11,5);
INSERT INTO track VALUES(157,'City of Sound',1,'https://api.mangoboat.tv/music/Big Wild/Superdream/01 - City of Sound.mp3','Electro','2019-02-01','3 min 52 s',12,6);
INSERT INTO track VALUES(158,'Joypunks',2,'https://api.mangoboat.tv/music/Big Wild/Superdream/02 - Joypunks.mp3','Electro','2019-02-01','3 min 15 s',12,6);
INSERT INTO track VALUES(159,'6''s to 9''s (feat. Rationale)',3,'https://api.mangoboat.tv/music/Big Wild/Superdream/03 - 6''s to 9''s (feat. Rationale).mp3','Electro','2019-02-01','3 min 26 s',12,6);
INSERT INTO track VALUES(160,'No Words',4,'https://api.mangoboat.tv/music/Big Wild/Superdream/04 - No Words.mp3','Electro','2019-02-01','3 min 35 s',12,6);
INSERT INTO track VALUES(161,'Alley-Oop (feat. iDA HAWK)',5,'https://api.mangoboat.tv/music/Big Wild/Superdream/05 - Alley-Oop (feat. iDA HAWK).mp3','Electro','2019-02-01','3 min 21 s',12,6);
INSERT INTO track VALUES(162,'Pale Blue Dot',6,'https://api.mangoboat.tv/music/Big Wild/Superdream/06 - Pale Blue Dot.mp3','Electro','2019-02-01','2 min 56 s',12,6);
INSERT INTO track VALUES(163,'Maker',7,'https://api.mangoboat.tv/music/Big Wild/Superdream/07 - Maker.mp3','Electro','2019-02-01','4 min 11 s',12,6);
INSERT INTO track VALUES(164,'Mopsy''s Interlude',8,'https://api.mangoboat.tv/music/Big Wild/Superdream/08 - Mopsy''s Interlude.mp3','Electro','2019-02-01','2 min 12 s',12,6);
INSERT INTO track VALUES(165,'Purple Sand (My Home)',9,'https://api.mangoboat.tv/music/Big Wild/Superdream/09 - Purple Sand (My Home).mp3','Electro','2019-02-01','3 min 38 s',12,6);
INSERT INTO track VALUES(166,'She Makes Magic',10,'https://api.mangoboat.tv/music/Big Wild/Superdream/10 - She Makes Magic.mp3','Electro','2019-02-01','4 min 23 s',12,6);
INSERT INTO track VALUES(167,'Heaven',11,'https://api.mangoboat.tv/music/Big Wild/Superdream/11 - Heaven.mp3','Electro','2019-02-01','3 min 37 s',12,6);
INSERT INTO track VALUES(168,'Awaken',12,'https://api.mangoboat.tv/music/Big Wild/Superdream/12 - Awaken.mp3','Electro','2019-02-01','3 min 2 s',12,6);
INSERT INTO track VALUES(169,'When I Get There',1,'https://api.mangoboat.tv/music/Big Wild/Invincible EP/01 When I Get There.mp3','Electronic','2017-03-30','3 min 40 s',13,6);
INSERT INTO track VALUES(170,'Empty Room [Feat. Yuna]',2,'https://api.mangoboat.tv/music/Big Wild/Invincible EP/02 Empty Room [Feat. Yuna].mp3','Electronic','2017-03-30','3 min 28 s',13,6);
INSERT INTO track VALUES(171,'I Just Wanna',3,'https://api.mangoboat.tv/music/Big Wild/Invincible EP/03 I Just Wanna.mp3','Electronic','2017-03-30','3 min 3 s',13,6);
INSERT INTO track VALUES(172,'Invincible [Feat. iDA HAWK]',4,'https://api.mangoboat.tv/music/Big Wild/Invincible EP/04 Invincible [Feat. iDA HAWK].mp3','Electronic','2017-03-30','3 min 38 s',13,6);
INSERT INTO track VALUES(173,'Crickets',5,'https://api.mangoboat.tv/music/Big Wild/Invincible EP/05 Crickets.mp3','Electronic','2017-03-30','2 min 42 s',13,6);
INSERT INTO track VALUES(174,'The Bird 🅴',1,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/01 - The Bird (Explicit).mp3','R&B','2016-01-15','3 min 37 s',14,7);
INSERT INTO track VALUES(175,'Heart Don''t Stand a Chance 🅴',2,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/02 - Heart Don''t Stand a Chance (Explicit).mp3','R&B','2016-01-15','5 min 12 s',14,7);
INSERT INTO track VALUES(176,'The Waters (feat. BJ The Chicago Kid) 🅴',3,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/03 - The Waters (feat. BJ The Chicago Kid) (Explicit).mp3','R&B','2016-01-15','2 min 54 s',14,7);
INSERT INTO track VALUES(177,'The Season | Carry Me 🅴',4,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/04 - The Season _ Carry Me (Explicit).mp3','R&B','2016-01-15','5 min 28 s',14,7);
INSERT INTO track VALUES(178,'Put Me Thru 🅴',5,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/05 - Put Me Thru (Explicit).mp3','R&B','2016-01-15','2 min 40 s',14,7);
INSERT INTO track VALUES(179,'Am I Wrong (feat. Schoolboy Q)',6,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/06 - Am I Wrong (feat. Schoolboy Q).mp3','R&B','2016-01-15','4 min 13 s',14,7);
INSERT INTO track VALUES(180,'Without You (feat. Rapsody) 🅴',7,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/07 - Without You (feat. Rapsody) (Explicit).mp3','R&B','2016-01-15','3 min 19 s',14,7);
INSERT INTO track VALUES(181,'Parking Lot 🅴',8,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/08 - Parking Lot (Explicit).mp3','R&B','2016-01-15','3 min 54 s',14,7);
INSERT INTO track VALUES(182,'Lite Weight (feat. The Free Nationals United Fellowship Choir) 🅴',9,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/09 - Lite Weight (feat. The Free Nationals United Fellowship Choir) (Explicit).mp3','R&B','2016-01-15','3 min 26 s',14,7);
INSERT INTO track VALUES(183,'Room in Here (feat. The Game & Sonyae Elise) 🅴',10,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/10 - Room in Here (feat. The Game & Sonyae Elise) (Explicit).mp3','R&B','2016-01-15','3 min 59 s',14,7);
INSERT INTO track VALUES(184,'Water Fall (Interluuube) 🅴',11,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/11 - Water Fall (Interluuube) (Explicit).mp3','R&B','2016-01-15','1 min 58 s',14,7);
INSERT INTO track VALUES(185,'Your Prime 🅴',12,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/12 - Your Prime (Explicit).mp3','R&B','2016-01-15','3 min 57 s',14,7);
INSERT INTO track VALUES(186,'Come Down 🅴',13,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/13 - Come Down (Explicit).mp3','R&B','2016-01-15','2 min 49 s',14,7);
INSERT INTO track VALUES(187,'Silicon Valley 🅴',14,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/14 - Silicon Valley (Explicit).mp3','R&B','2016-01-15','4 min 4 s',14,7);
INSERT INTO track VALUES(188,'Celebrate 🅴',15,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/15 - Celebrate (Explicit).mp3','R&B','2016-01-15','3 min 46 s',14,7);
INSERT INTO track VALUES(189,'The Dreamer (feat. Talib Kweli & Timan Family Choir) 🅴',16,'https://api.mangoboat.tv/music/Anderson .Paak/Malibu/16 - The Dreamer (feat. Talib Kweli & Timan Family Choir) (Explicit).mp3','R&B','2016-01-15','5 min 40 s',14,7);
CREATE TABLE playhistory (
	"playhistoryID" INTEGER NOT NULL, 
	"userID" INTEGER, 
	"playDate" VARCHAR NOT NULL, 
	"trackID" INTEGER, 
	"trackName" VARCHAR NOT NULL, 
	"trackNumber" INTEGER NOT NULL, 
	"trackURL" VARCHAR NOT NULL, 
	"recordedDate" VARCHAR NOT NULL, 
	duration VARCHAR NOT NULL, 
	"albumID" INTEGER, 
	"artistID" INTEGER, 
	PRIMARY KEY ("playhistoryID"), 
	FOREIGN KEY("userID") REFERENCES user ("userID"), 
	FOREIGN KEY("trackID") REFERENCES track ("trackID"), 
	FOREIGN KEY("albumID") REFERENCES album ("albumID"), 
	FOREIGN KEY("artistID") REFERENCES artist ("artistID")
);
INSERT INTO playhistory VALUES(1,1,'2024-04-01',1,'Hold On (feat. Becky Hill)',1,'https://api.mangoboat.tv/music/Netsky/Second Nature/01 - Hold On (feat. Becky Hill).mp3','2020-10-30','3 min 43 s',1,1);
INSERT INTO playhistory VALUES(2,1,'2024-04-01',2,'Mixed Emotions (feat. Montell2099)',2,'https://api.mangoboat.tv/music/Netsky/Second Nature/02 - Mixed Emotions (feat. Montell2099).mp3','2020-10-30','4 min 27 s',1,1);
INSERT INTO playhistory VALUES(3,1,'2024-04-01',29,'When Darkness Falls',11,'https://api.mangoboat.tv/music/Netsky/2 Deluxe/11 - When Darkness Falls.mp3','2012-11-19','3 min 52 s',2,1);
CREATE INDEX "ix_artist_artistName" ON artist ("artistName");
CREATE INDEX "ix_artist_artistPhotoURL" ON artist ("artistPhotoURL");
CREATE INDEX "ix_playlisttrack_playlistID" ON playlisttrack ("playlistID");
CREATE INDEX ix_user_username ON user (username);
CREATE INDEX "ix_image_imageURL" ON image ("imageURL");
CREATE INDEX ix_album_year ON album (year);
CREATE INDEX "ix_album_numSongs" ON album ("numSongs");
CREATE INDEX "ix_album_albumName" ON album ("albumName");
CREATE INDEX "ix_album_albumCoverURL" ON album ("albumCoverURL");
CREATE INDEX "ix_playlist_playlistName" ON playlist ("playlistName");
CREATE INDEX "ix_playlist_creationDate" ON playlist ("creationDate");
CREATE INDEX "ix_track_trackURL" ON track ("trackURL");
CREATE INDEX "ix_track_recordedDate" ON track ("recordedDate");
CREATE INDEX "ix_track_trackName" ON track ("trackName");
CREATE INDEX "ix_playhistory_trackName" ON playhistory ("trackName");
CREATE INDEX "ix_playhistory_trackURL" ON playhistory ("trackURL");
CREATE INDEX "ix_playhistory_playDate" ON playhistory ("playDate");
CREATE INDEX "ix_playhistory_recordedDate" ON playhistory ("recordedDate");
COMMIT;
