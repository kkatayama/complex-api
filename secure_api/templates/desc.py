description = """
Com-Plex Backend API to manage the Users, Artists, Albums, Tracks, Playlists, PlayHistory, Favorites, and Image tables.

## Guest-User

These functions will help you get started.

**Includes:** `/create-user`, `/sign-in`, and `/sign-out`.

**You must create an account and sign-in in order to access the rest of the API**

* **Click `Authorize` to sign-in to the [Interactive Documentation](https://api.mangoboat.tv/docs)**

## My-User, My-Playlist, My-PlayHistory, and My-My-Favorites

These functions are the **logged-in user functions** and serve as the core functions for your FlutterFlow front-end.

* **`/my/user-info`**: info of the logged in user
* **`/my/playlists`**: all playlists the current user owns
* **`/my/play-history`**: the current user's play history

## User, Artist, Album, Track, Playlist, PlayHistory, Favorite, and Image

These are direct references to the Database Tabels and are modeled after the Com-Plex Class Diagrams
* The functions here populate information for all users and are to be viewed as *Administrative Functions*

## Account-Security

These functions are use to implement the OAuth2 JWT Token Security Model

* They are shown for reference and are not intended to be used in production

* They **Guest-User** functions implement a simplified version of OAuth2 JWT and is ready for use with Flutterflow!

## "/tables"

**This endpoint was added for debugging purposes**

Vist this enpoint: [https://api.mangoboat.tv/tables](https://api.mangoboat.tv/tables) to view all of the Database Tables

* These tables are actively updated but require **refreshing the browser page** to load recent changes.

## Alternative Documentation

[https://api.mangoboat.tv/redoc](https://api.mangoboat.tv/redoc)




"""
