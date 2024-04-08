# Com-Plex API

* [openapi.json](https://api.mangoboat.tv/openapi.json)
* [View Tables](https://api.mangoboat.tv/tables)

* [Interactive Documentation](https://api.mangoboat.tv/docs)
* [Alternative Documentation](https://api.mangoboat.tv/redoc)

* [systemd-setup](https://ashfaque.medium.com/deploy-fastapi-app-on-debian-with-nginx-uvicorn-and-systemd-2d4b9b12d724)
* [logging-setup](https://python.plainenglish.io/effortless-exception-error-handling-in-fastapi-a-clean-and-simplified-approach-db6f6a7a497c)

## OpenAPI 

``` json

{
    '/create-user': {
        'post': {
            'tags': ['User-Guest'],
            'summary': 'Create a user account (via JSON)',
            'operationId': 'create_user',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/CreateUser'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/sign-in': {
        'post': {
            'tags': ['User-Guest'],
            'summary': 'Submit credentials and retrieve access tokens (via JSON)',
            'operationId': 'sign_in',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/LoginUser'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/TokenSchema'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/sign-out': {
        'get': {
            'tags': ['User-Guest'],
            'summary': 'Sign out the currently logged in user',
            'operationId': 'sign_out',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/UserSignOut'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/my/user-info': {
        'get': {
            'tags': ['My-User'],
            'summary': 'Get basic info of currently logged in user',
            'operationId': 'get_my_user',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/UserFull'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/my/user-details': {
        'get': {
            'tags': ['My-User'],
            'summary': 'Get detailed info of currently logged in user',
            'operationId': 'get_my_userDetails',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/UserWithPlaylistsPlayHistory'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/my/user-details-tracks': {
        'get': {
            'tags': ['My-User'],
            'summary': 'Get detailed info of currently logged in user (with tracks expanded)',
            'operationId': 'get_my_userDetails_tracks',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/UserWithPlaylistsPlayHistoryAll'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/my/username': {
        'patch': {
            'tags': ['My-User'],
            'summary': 'Modify username of currently logged in user',
            'operationId': 'edit_my_username',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/EditUser'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/password': {
        'patch': {
            'tags': ['My-User'],
            'summary': "Change a user's password",
            'operationId': 'change_my_password',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ChangePass'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/user': {
        'delete': {
            'tags': ['My-User'],
            'summary': 'Delete user account',
            'operationId': 'delete_my_user',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeleteUser'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/my/playlist': {
        'post': {
            'tags': ['My-Playlist'],
            'summary': 'Create a playlist for the logged in user',
            'operationId': 'create_my_playlist',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/CreatePlaylist'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Playlist'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/playlists': {
        'get': {
            'tags': ['My-Playlist'],
            'summary': "Get array[] of user's playlists",
            'operationId': 'get_my_playlists',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlaylistAll'}, 'type': 'array', 'title': 'Response Get My Playlists My Playlists Get'}}}
                }
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/playlists/tracks': {
        'get': {
            'tags': ['My-Playlist'],
            'summary': "Get array[] of user's playlists (with tracks expanded)",
            'operationId': 'get_my_playlists_tracks',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlaylistWithPlaylistTracks'}, 'type': 'array', 'title': 'Response Get My Playlists Tracks My Playlists Tracks Get'}}}
                }
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/playlist/{playlistID}': {
        'patch': {
            'tags': ['My-Playlist'],
            'summary': "Rename a user's playlist",
            'operationId': 'rename_my_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/RenamePlaylist'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Playlist'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'get': {
            'tags': ['My-Playlist'],
            'summary': 'Get details of a single playlist (with tracks)',
            'operationId': 'get_my_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlaylistWithUserTracks'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'delete': {
            'tags': ['My-Playlist'],
            'summary': "Delete a user's playlist",
            'operationId': 'delete_my_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeletePlaylist'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/my/playlist/{playlistID}/tracks': {
        'post': {
            'tags': ['My-Playlist'],
            'summary': 'Add a single track to a playlist',
            'operationId': 'addTrack_my_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/AddPlaylistTrack'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlaylistTrackAll'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'get': {
            'tags': ['My-Playlist'],
            'summary': 'Get details of a single playlist (with tracks expanded)',
            'operationId': 'get_my_playlist_playlistID_tracks',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlaylistWithUserTracksAll'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'delete': {
            'tags': ['My-Playlist'],
            'summary': 'Delete a single track from a playlist',
            'operationId': 'delete_my_playlist_playlistID_tracks',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeletePlaylistTrack'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeletePlaylistTrack'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/my/play-history': {
        'get': {
            'tags': ['My-PlayHistory'],
            'summary': 'Get array[] of playhistory for currently logged in user',
            'operationId': 'get_my_play_history',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlayHistoryFull'}, 'type': 'array', 'title': 'Response Get My Play History My Play History Get'}}}
                }
            },
            'security': [{'JWT': []}]
        },
        'post': {
            'tags': ['My-PlayHistory'],
            'summary': "Add a track to logged in user's play history",
            'operationId': 'addTrack_my_play_history',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlayHistoryAddMyTrack'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlayHistory'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/play-history-tracks': {
        'get': {
            'tags': ['My-PlayHistory'],
            'summary': 'Get array[] of playhistory for currently logged in user (with tracks expanded)',
            'operationId': 'get_my_play_history_tracks',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlayHistoryExtended'}, 'type': 'array', 'title': 'Response Get My Play History Tracks My Play History Tracks Get'}}}
                }
            },
            'security': [{'JWT': []}]
        }
    },
    '/my/play-history/{playhistoryID}': {
        'get': {
            'tags': ['My-PlayHistory'],
            'summary': 'Get details of a play history entry for currently logged in user',
            'operationId': 'get_my_playhistory_playhistoryID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playhistoryID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playhistoryid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlayHistoryExtended'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/users': {
        'get': {
            'tags': ['User'],
            'summary': 'Get array[] of all users',
            'operationId': 'get_users',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/User'}, 'type': 'array', 'title': 'Response Get Users Users Get'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/user/{userID}': {
        'get': {
            'tags': ['User'],
            'summary': 'Get details of a single user',
            'operationId': 'get_user_userID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'userID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Userid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/UserWithPlaylistsPlayHistory'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'patch': {
            'tags': ['User'],
            'summary': "Edit a user's username",
            'operationId': 'edit_user_userID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'userID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Userid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/EditUser'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'delete': {
            'tags': ['User'],
            'summary': 'Delete a user',
            'operationId': 'delete_user_userID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'userID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Userid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeleteUser'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/artists': {
        'get': {
            'tags': ['Artist'],
            'summary': 'Get array[] of all artists',
            'operationId': 'get_artists',
            'security': [{'JWT': []}],
            'parameters': [
                {'name': 'offset', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'default': 0, 'title': 'Offset'}},
                {'name': 'limit', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'maximum': 1000, 'default': 8, 'title': 'Limit'}}
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/ArtistFull'}, 'title': 'Response Get Artists Artists Get'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/artist/{artistID}/albums': {
        'get': {
            'tags': ['Artist'],
            'summary': 'Get info for a single artist (includes albums)',
            'operationId': 'get_artist_artistID_albums',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'artistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Artistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ArtistWithAlbums'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/artist/{artistID}/album/{albumID}/tracks': {
        'get': {
            'tags': ['Artist'],
            'summary': "Get a single artist's album (with tracks)",
            'operationId': 'get_artist_artistID_album_albumID_tracks',
            'security': [{'JWT': []}],
            'parameters': [
                {'name': 'artistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Artistid'}},
                {'name': 'albumID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Albumid'}}
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ArtistWithAlbumTracks'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/artist/{artistID}/albums-tracks': {
        'get': {
            'tags': ['Artist'],
            'summary': 'Get all albums with tracks for a single artist',
            'operationId': 'get_artist_artistID_albums_tracks',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'artistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Artistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ArtistWithAlbumsTracks'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/albums': {
        'get': {
            'tags': ['Album'],
            'summary': 'Get array[] of all albums',
            'operationId': 'get_albums',
            'security': [{'JWT': []}],
            'parameters': [
                {'name': 'offset', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'default': 0, 'title': 'Offset'}},
                {'name': 'limit', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'maximum': 1000, 'default': 8, 'title': 'Limit'}}
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/AlbumFull'}, 'title': 'Response Get Albums Albums Get'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/album/{albumID}/tracks': {
        'get': {
            'tags': ['Album'],
            'summary': 'Get info for a single album (with tracks)',
            'operationId': 'get_album_albumID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'albumID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Albumid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/AlbumWithTracks'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/tracks': {
        'get': {
            'tags': ['Track'],
            'summary': 'Get array[] of all albums',
            'operationId': 'get_tracks',
            'security': [{'JWT': []}],
            'parameters': [
                {'name': 'offset', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'default': 0, 'title': 'Offset'}},
                {'name': 'limit', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'maximum': 1000, 'default': 8, 'title': 'Limit'}}
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/TrackFull'}, 'title': 'Response Get Tracks Tracks Get'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/track/{trackID}': {
        'get': {
            'tags': ['Track'],
            'summary': 'Get details of a single track',
            'operationId': 'get_track_trackID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'trackID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Trackid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/TrackAll'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/playlist': {
        'post': {
            'tags': ['Playlist'],
            'summary': 'Create a playlist for a specified user',
            'operationId': 'create_playlist',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/CreateUserPlaylist'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Playlist'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/playlists': {
        'get': {
            'tags': ['Playlist'],
            'summary': 'Get array[] of all playlists for all users',
            'operationId': 'get_playlists',
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlaylistAll'}, 'type': 'array', 'title': 'Response Get Playlists Playlists Get'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/playlists/tracks': {
        'get': {
            'tags': ['Playlist'],
            'summary': 'Get array[] of all playlists for all users (with tracks expanded)',
            'operationId': 'get_playlists_tracks',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlaylistWithPlaylistTracks'}, 'type': 'array', 'title': 'Response Get Playlists Tracks Playlists Tracks Get'}}}
                }
            },
            'security': [{'JWT': []}]
        }
    },
    '/playlist/{playlistID}': {
        'patch': {
            'tags': ['Playlist'],
            'summary': 'Rename a playlist',
            'operationId': 'rename_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/RenamePlaylist'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Playlist'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'get': {
            'tags': ['Playlist'],
            'summary': 'Get details of a single playlist (with tracks)',
            'operationId': 'get_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlaylistWithUserTracks'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'delete': {
            'tags': ['Playlist'],
            'summary': 'Delete a single playlist',
            'operationId': 'delete_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeletePlaylist'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/playlist/{playlistID}/tracks': {
        'post': {
            'tags': ['Playlist'],
            'summary': "Add a single track to a user's playlist",
            'operationId': 'addTrack_playlist_playlistID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/AddPlaylistTrack'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlaylistTrackAll'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'get': {
            'tags': ['Playlist'],
            'summary': 'Get details of a single playlist (with tracks expanded)',
            'operationId': 'get_playlist_playlistID_tracks',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlaylistWithUserTracksAll'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        },
        'delete': {
            'tags': ['Playlist'],
            'summary': 'Delete a single track from a playlist',
            'operationId': 'delete_playlist_playlistID_tracks',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playlistID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playlistid'}}],
            'requestBody': {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeletePlaylistTrack'}}}},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/DeletePlaylistTrack'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/play-history': {
        'get': {
            'tags': ['PlayHistory'],
            'summary': "Get array[] of playhistory for all user's",
            'operationId': 'get_playhistory',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlayHistoryFull'}, 'type': 'array', 'title': 'Response Get Playhistory Play History Get'}}}
                }
            },
            'security': [{'JWT': []}]
        },
        'post': {
            'tags': ['PlayHistory'],
            'summary': "Add a track to a user's play history",
            'operationId': 'add_playhistory_trackID',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlayHistoryAddUserTrack'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlayHistory'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            },
            'security': [{'JWT': []}]
        }
    },
    '/play-history/tracks': {
        'get': {
            'tags': ['PlayHistory'],
            'summary': "Get array[] of playhistory for all user's (with tracks expanded)",
            'operationId': 'get_playhistory_tracks',
            'responses': {
                '200': {
                    'description': 'Successful Response',
                    'content': {'application/json': {'schema': {'items': {'$ref': '#/components/schemas/PlayHistoryExtended'}, 'type': 'array', 'title': 'Response Get Playhistory Tracks Play History Tracks Get'}}}
                }
            },
            'security': [{'JWT': []}]
        }
    },
    '/play-history/{playhistoryID}': {
        'get': {
            'tags': ['PlayHistory'],
            'summary': 'Get details of a single play history entry',
            'operationId': 'get_playhistory_playhistoryID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'playhistoryID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Playhistoryid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/PlayHistoryExtended'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/images': {
        'get': {
            'tags': ['Image'],
            'summary': 'Get array[] of all images',
            'operationId': 'get_images',
            'security': [{'JWT': []}],
            'parameters': [
                {'name': 'offset', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'default': 0, 'title': 'Offset'}},
                {'name': 'limit', 'in': 'query', 'required': False, 'schema': {'type': 'integer', 'maximum': 1000, 'default': 8, 'title': 'Limit'}}
            ],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/ImageFull'}, 'title': 'Response Get Images Images Get'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/image/{imageID}': {
        'get': {
            'tags': ['Image'],
            'summary': 'Get details of a single image',
            'operationId': 'get_image_imageID',
            'security': [{'JWT': []}],
            'parameters': [{'name': 'imageID', 'in': 'path', 'required': True, 'schema': {'type': 'integer', 'title': 'Imageid'}}],
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/ImageAll'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/sign-up': {
        'post': {
            'tags': ['Account-Security'],
            'summary': 'Create a user account (via FORM)',
            'operationId': 'sign_up',
            'requestBody': {'content': {'application/json': {'schema': {'$ref': '#/components/schemas/CreateUser'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/login': {
        'post': {
            'tags': ['Account-Security'],
            'summary': 'Submit credentials and retrieve access tokens (via FORM)',
            'operationId': 'login',
            'requestBody': {'content': {'application/x-www-form-urlencoded': {'schema': {'$ref': '#/components/schemas/Body_login_login_post'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/TokenSchema'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/refresh-token': {
        'post': {
            'tags': ['Account-Security'],
            'summary': 'Refresh jwt API tokens (via FORM)',
            'operationId': 'refresh_token',
            'requestBody': {'content': {'application/x-www-form-urlencoded': {'schema': {'$ref': '#/components/schemas/Body_refresh_token_refresh_token_post'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/TokenSchema'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/auth/me': {
        'get': {
            'tags': ['Account-Security'],
            'summary': 'Get details of currently logged in user',
            'operationId': 'auth_me',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/User'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/auth/me/playlists': {
        'get': {
            'tags': ['Account-Security'],
            'summary': 'Include user playlists',
            'operationId': 'auth_me_playlists',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/UserWithPlaylists'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/test-access-token': {
        'post': {
            'tags': ['Account-Security'],
            'summary': 'Test if the access token is valid',
            'operationId': 'test_access_token',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/TokenPayload'}}}}},
            'security': [{'JWT': []}]
        }
    },
    '/test-refresh-token': {
        'post': {
            'tags': ['Account-Security'],
            'summary': 'Test if the refresh token is valid',
            'operationId': 'test_refresh_token',
            'requestBody': {'content': {'application/x-www-form-urlencoded': {'schema': {'$ref': '#/components/schemas/Body_test_refresh_token_test_refresh_token_post'}}}, 'required': True},
            'responses': {
                '200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/TokenPayload'}}}},
                '422': {'description': 'Validation Error', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/HTTPValidationError'}}}}
            }
        }
    },
    '/logout': {
        'get': {
            'tags': ['Account-Security'],
            'summary': 'Revoke all tokens and log the user out',
            'operationId': 'logout',
            'responses': {'200': {'description': 'Successful Response', 'content': {'application/json': {'schema': {}}}}},
            'security': [{'JWT': []}]
        }
    }
}

```
