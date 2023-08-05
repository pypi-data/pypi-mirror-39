#!/usr/bin/env python
# coding: utf-8


"""
sound.py - classes to store and play music and sound effects.
"""


## one / for float divison, double / for int division
from __future__ import division, print_function
import pygame


def get_music_player(playlist=[], fade_time=1000):
    """
    Factory method that returns a MusicPlayer instance.
    """
    return MusicPlayer(playlist, fade_time)
    
	
def get_sound_effects_player(fade_time=250):
    """
    Factory method that returns an SEPlayer instance.
    """
    return SEPlayer(fade_time)


class MusicPlayer(object):
    """
    A class to control when and how to play background music tracks. A playlist 
    of tracks and the number of times to play them is maintained and used to 
    control what's played and when.
    """
    
    ## handle to pygame's streaming music module
    player = pygame.mixer.music
    
    def __init__(self, playlist, fade_time):
        """
        Entries in the playlist consist of a tuple with the path to the track
        and how many times it should be played.
        """
        self.playlist = playlist
        self.fade_time = fade_time
        self.track_index = 0
        self.play_count = 0
        self.stopped = True
        self.fade_in = False
        self.timer = pygame.time.get_ticks()
    
    def has_next(self):
        """
        Returns True/False if there is another track in the current playlist
        that can be played.
        """
        return self.track_index < len(self.playlist) - 1
    
    def to_next(self):
        """
        Increments the current track to play.
        """
        self.track_index += 1
    
    def load(self):
        """
        Loads the current track to be played next. Does NOT start playback.
        """
        self.player.load(self.get_current_track()[0])
        
    def load_next(self):
        """
        Calls other methods to begin playback of the next track in the playlist.
        """
        if self.has_next():
            self.to_next()
            self.load()
            self.play()

    def is_busy(self):
        """
        Returns True/False if the player is currently playing a track.
        """
        if self.player.get_busy() > 0:
            return True
        else:
            return False
            
    def is_stopped(self):
        """
        Returns True/False if the player has been stopped by the stop() method.
        """
        return self.stopped 
        
    def add_track(self, track, loops=0, skip_point=None):
        """
        Adds another track to the end of the playlist. Will be repeated 
        unless the number of times to loop is given.
        
        skip_point can be used to go to the next track once this position
        has been reached during playback.
        """
        self.playlist.append((track, loops, skip_point))
        
    def play(self):
        """
        Plays the current track.
        """
        self.stopped = False
        self.player.play(self.get_current_track()[1] - 1)

    def get_playlist(self):
        """
        Returns a copy of the current playlist.
        """
        return self.playlist[:]
    
    def set_playlist(self, pl):
        """
        Set the playlist to the given list.
        """
        self.playlist = pl
        
    def pause(self):
        """
        Pauses the currently playing track.
        """
        self.player.pause()
        
    def unpause(self):
        """
        Un-pause a currently paused track.
        """
        self.player.unpause()
    
    def stop(self):
        """
        Stops playback. Play will resume from the beginning of the current
        track.
        """
        self.stopped = True
        self.player.stop()
    
    def restart_playlist(self):
        """
        Starts the playlist over from the beginning.
        """
        self.track_index = 0
        
    def rewind(self):
        """
        Starts playing the current track from the beginning.
        """
        ## this doesn't seem to work for midi tracks but does for ogg
        self.player.rewind()
        
    def _fadein(self):
        """
        Internal method, ramps the volume up by a little everytime update()
        is called if fade_in is set. Creates a fade-in effect for the 
        currently playing track.
        """
        volume = self.get_volume() + .02
        if self.get_volume() < 1.0:
            self.set_volume(volume)
        else:
            self.set_volume(1.0)
            self.fade_in = False
            
    def fadein(self):
        """
        Sets the player to fade-in whatever track is currently playing
        until the volume is at maximum.
        """
        self.fade_in = True
        
    def fadeout(self):
        """
        Sets the player to fade-out whatever track is currently playing
        until the volume is zero.
        """
        self.player.fadeout(self.get_fadetime())
                
    def get_volume(self):
        """
        Return the player's current volume.
        """
        return self.player.get_volume()
        
    def set_volume(self, vol):
        """
        Set the player's current volume.
        """
        self.player.set_volume(vol)
    
    def get_pos(self):
        """
        Returns the current track's playback time in milliseconds. This 
        represents how long the track has been playing.
        """
        return self.player.get_pos()
    
    def get_current_track(self):
        """
        Returns the current track and the number of times to play it.
        """
        assert len(self.playlist) > 0, "self.playlist is empty"
        return self.playlist[self.track_index]
    
    def get_fadetime(self):
        """
        Returns the current fade time of the player.
        """
        return self.fade_time
    
    def set_fadetime(self, msec):
        """
        Set the current fade time in milliseconds for fadein() and fadeout().
        """
        self.fade_time = msec
        
    def update(self, dt=(1/60)):
        """
        Call once per gameloop. Checks time for fadein() and will skip to next 
        track if the current one is finished.
        """
        current_time = pygame.time.get_ticks()
        ## update time with logic update interval, 1/60 by default,
        ## for _fadein()
        if current_time > self.timer + self.get_fadetime() * dt:
            self.timer = current_time
            if self.fade_in:
                self._fadein()
        ## check skip_pos for current track
        try:
            now_track = self.get_current_track()
        except AssertionError as e:
            print('MusicPlayer says: "No playlist loaded!"')
        else:
            if now_track[2] is not None:
                if self.get_pos() > now_track[2]:
                    self.load_next()
            ## check to go to next track in playlist
            if not self.is_busy() and not self.is_stopped():
                ## Not sure if this is a bug in pygame or not but play(0) plays 
                ## once, play(2) plays 3 times, and play(1) should play twice but 
                ## actually only plays once (argument for play() is how many times
                ## to repeat the track) so if the number of plays for a track is
                ## 2 then it is played again. 
                if now_track[1] == 2 and self.play_count == 0:
                    self.play_count = 1
                    self.play()
                elif self.has_next():
                    self.play_count = 0
                    self.load_next()


class SEPlayer(object):
    """
    A class to control when and how to play sound effects. A table of sounds
    is kept and the name is used to get the sound object to play it.
    """
    
    ## handle to pygame sound mixer
    mixer = pygame.mixer
    
    def __init__(self, fade_time_all=250):
        """
        Loads a SETable reference to store the sound objects in. One object
        per sound needed.
        """
        self.table = SETable()
        self.fade_time_all = fade_time_all
    
    def add_sound(self, name, path):
        """
        Add a sound to the table.
        """
        self.table.add_sound(name, path)
    
    def get_sound(self, name):
        """
        Return a sound object by name.
        """
        return self.table._get_sound(name)
	
    def get_length(self, name):
        """
        Return the length of a sound in seconds.
        """
        sound = self.table._get_sound(name)
        return sound[0].get_length()
        
    def play(self, name):
        """
        Plays a sound.
        """
        sound = self.table._get_sound(name)
        sound[0].play()

    def stop(self, name):
        """
        Stops a sound if it's playing.
        """
        sound = self.table._get_sound(name)
        sound[0].stop()

    def fadeout(self, name):
        """
        Fade-out and stop a playing sound.
        """
        sound = self.table._get_sound(name)
        sound[0].fadeout(sound[1])
            
    def stop_all(self):
        """
        Stops all sound effects that are playing.
        """
        self.mixer.stop()

    def pause_all(self):
        """
        Pause all sound effects that are playing.
        """
        self.mixer.pause()

    def unpause_all(self):
        """
        Un-pause all sound effects that are paused.
        """
        self.mixer.unpause()

    def fadeout_all(self):
        """
        Fade-out all playing sound effects.
        """
        self.mixer.fadeout(self.fade_time_all)

    def is_busy(self):
        """
        Return True/False if the mixer is playing a sound.
        """
        if self.mixer.get_busy() > 0:
            return True
        else:
            return False


class SETable(object):
    """
    Holds pygame.mixer.Sound objects for easy access by name.
    """
        
    def __init__(self):
        """
        Uses dictionary for name lookup.
        """
        self.table = {}
    
    def add_sound(self, name, path, fade_time=250):
        """
        Adds a sound to the table. The format is a tuple with the sound 
        object and the fade-out time.
        """
        sound = (pygame.mixer.Sound(path), fade_time)
        self.table[name] = sound
    
    def _get_sound(self, name):
        """
        Internal method, returns a sound corresponding to the given name.
        """
        assert name in self.table, "no sound exists by that name"
        return self.table[name]


