"""
PieTunes is an abstraction of Apple's Scripting Bridge API for iTunes.
Copyright (C) 2018  Brian Farrell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: one.chillindude@me.com
"""

from ScriptingBridge import SBApplication
import subprocess

from pietunes.script_support import _download, _open_library


DEFAULT_LIBRARY_LOCATION = "com.apple.iTunes 'book:1:iTunes Library Location'"


class App(object):
    """The App class provides a Python API for scripting iTunes

    The client application built on this pietunes package should
    instantiate an instance of this class in order to acces the API.
    All messages sent to iTunes should use only the methods provided here.

    Attributes:
        itunes: An SBApplication instance for iTunes.app
        playlists: A dynamically updated list of all playlists known by iTunes
    """

    def __init__(self):
        """Inits App with SBAppication and a list of available playlists."""
        self.itunes = SBApplication.applicationWithBundleIdentifier_(
                      "com.apple.iTunes")
        self.playlists = self._get_playlists()

    def _get_playlists(self):
        return list(self.itunes.playlists())

    def get_playlist(self, name):
        """Return a reference to an iTunes Playlist object."""
        playlist = None
        candidate = iter(self.playlists)
        while not playlist:
            try:
                p = next(candidate)
                if p.name() == name:
                    playlist = p
                    return playlist
            except StopIteration:
                raise NotFoundError(f'\nNo playlist with the name {name}'
                                    ' could be found.\n')

    def get_sources(self):
        """Returns a list of iTunes data sources.
        """
        return self.itunes.sources()

    def get_tracks(self, playlist):
        """Returns a generator object that yields each track of the playlist.

        The yielded track is an iTunes track object.
        """
        tracks = (track for track in playlist.tracks())

        return tracks

    def get_track(self, collection, title):
        """Returns an a reference to an iTunes Track object.
        """
        track = None
        candidate = iter(collection)
        while not track:
            try:
                t = next(candidate)
                if t.name() == title:
                    track = t
                    return track
            except StopIteration:
                raise NotFoundError(f'\nNo movie with the title {title}'
                                    ' could be found.\n')

    def download_track(self, playlist, track):
        script = _download(playlist, track)
        osa = subprocess.Popen(
            ['osascript', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        osa.communicate(script)

    def open_library(self, library_location):
        # TODO: This is just a copy/paste from above - Needs Adjusting
        script = _open_library(library_location)
        osa = subprocess.Popen(
            ['osascript', '-'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        osa.communicate(script)


class NotFoundError(Exception):
    """Error thrown when the item being searched for is not found.
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
