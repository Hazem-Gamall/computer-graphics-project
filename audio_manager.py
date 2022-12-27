from singleton import Singleton
from pygame import mixer

class AudioManager(metaclass=Singleton):
    def initialize(self):
        mixer.init()
        mixer.music.set_volume(0.2)
        self.sounds = {}
    
    def register_sound(self, sound_name, sound_path):
        self.sounds[sound_name] = sound_path
    
    def play_sound(self, sound_name):
        sound_path = self.sounds.get(sound_name, None)
        if not sound_path:
            print("Sound hasn't been registered")
            return
        mixer.music.load(sound_path)
        mixer.music.play()
