################################################################################
"""
Grand Entrance Audio Player
(c) Stanley Solutions - 2023
"""
################################################################################

from typing import Callable
from threading import Thread

import vlc



class PlayerDeck():
    """
    Deck of Playable Audio Files.
    """

    def __init__(self, callback: Callable):
        """Initialize and Load the List of Files."""
        self.active = True
        self._files = []
        self._callback = callback
        self._active_track_index = 0
        self._active_player: vlc.MediaPlayer = None
        self._next_player: vlc.MediaPlayer = None
        self._prev_player: vlc.MediaPlayer = None

    def _advance_when_complete(self):
        """Automatic Track Advancing Mechanism."""
        while self.active:
            if self._active_player is None:
                continue
            if self._active_player.get_position() > 0.99:
                self.next()
                self._callback()

    @property
    def active_index(self) -> int:
        return self._active_track_index

    def load_playlist(self, files: list[str] = None):
        """Load the List of Tracks for the Playlist."""
        if files is None:
            return
        self._files = files
        if self._files:
            # Load the First File
            self._active_player = vlc.MediaPlayer(
                self._files[self._active_track_index]
            )
            # Previous is First File, Too!
            self._prev_player = vlc.MediaPlayer(
                self._files[self._active_track_index]
            )
            if len(self._files) > 1:
                # Next Track
                self._next_player = vlc.MediaPlayer(
                    self._files[self._active_track_index + 1]
                )
            Thread(target=self._advance_when_complete).start()

    def play(self) -> int:
        """Play the Active Track."""
        if self._active_player is not None:
            return self._active_player.play()

    def pause(self) -> int:
        """Pause the Active Track."""
        if self._active_player is not None:
            return self._active_player.pause()

    def play_stop(self):
        """Play or Stop the Active Track."""
        if self._active_player is not None:
            if self._active_player.is_playing():
                return self._active_player.stop()
            else:
                return self._active_player.play()

    def stop(self) -> int:
        """Stop the Active Track."""
        if self._active_player is not None:
            return self._active_player.stop()

    def next(self):
        """Load the Next Audio File."""
        if self._active_player is None:
            return
        # Validate Active Track Index
        if self._active_track_index < len(self._files):
            # Bump Index
            self._active_track_index += 1
            # Move Pointer Track Heads
            self._prev_player = self._active_player
            self._active_player = self._next_player
            if self._active_track_index + 1 < len(self._files):
                # Load Next File
                self._next_player = vlc.MediaPlayer(
                    self._files[self._active_track_index + 1]
                )

    def previous(self):
        """Load the Next Audio File."""
        if self._active_player is None:
            return
        # Validate Active Track Index
        if self._active_track_index > 0:
            # Bump Index
            self._active_track_index -= 1
            # Move Pointer Track Heads
            self._next_player = self._active_player
            self._active_player = self._prev_player
            if self._active_track_index > 0:
                # Load Previous File
                self._prev_player = vlc.MediaPlayer(
                    self._files[self._active_track_index - 1]
                )
