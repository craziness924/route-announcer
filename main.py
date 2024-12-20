import os

import json

import pydub.playback
import yaml
import pydub
from pydub import AudioSegment

from pynput import keyboard


class Voice:
    def __init__(self, name, path, routes):
        self.name: str = name
        self.path: str = path
        
        self.routes: dict = routes

        self.audio_segments: dict[str, AudioSegment] = {}
        
        self._initialized_audio_segments = False
    
    # creating audio segments for a simple announcement can take a while, so we do it ahead of time
    def create_audio_segments(self):
        if self._initialized_audio_segments:
            return False
        
        for f in os.scandir(self.path):
            if f.is_dir() or f.name == "voice_info.json":
                continue

            try:
                a_s = pydub.AudioSegment.from_file(f.path)

                self.audio_segments[f.path] = a_s
            except:
                print(f)
                

def play_announcement(files_to_play):
    # f = ["voices/crystal/nextstop.mp3", "voices/crystal/derailment.mp3", "voices/crystal/street.mp3", "voices/crystal/metro.mp3", "voices/crystal/bay.mp3", "voices/crystal/1.mp3"]
    # audio_segments: list[AudioSegment] = []

    # for r in files_to_play:
    #     a = AudioSegment.from_file(r)
    #     audio_segments.append(a)

    # for a_s in audio_segments:
    #     pydub.playback.play(a_s)
    #     time.sleep(0.2)

    pass

def create_hotkeys():
    pass

def load_config(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config

def load_voices(voices_path) -> list[Voice]:
    voices: list[Voice] = []
    
    for voice_path in os.scandir(voices_path):
        if voice_path.is_file():
            continue
        
        for file in os.scandir(voice_path):
            if file.name == "voice_info.json" and file.is_file():
                with open(file) as f:
                    voice_info = json.load(f)
                    
                    voice_dir = os.path.dirname(file.path)

                    v = Voice(voice_info["name"], voice_dir, routes=voice_info["routes"])
                    
                    voices.append(v)

    return voices

def handle_key_press(key):
    if key == keyboard.Key.alt:
        # play_announcement(["voices/crystal/16.mp3", "voices/crystal/to.mp3", "voices/crystal/rocky_island.mp3", "voices/crystal/centre.mp3"])
        pass

def get_selection(options, prompt=None, opt_name_key=None):
    valid_input = False

    while not valid_input:
        print(f"\n{prompt}")
        for i, o in enumerate(options):
            if opt_name_key:
                print(f"[{i+1}] {o.__dict__[opt_name_key]}")
            else:
                print(f"[{i+1}] {o}")
            
        try:
            val = int(input())-1
            
            try:
                if options.items[val]:
                    valid_input = True
            except AttributeError:
                options[val]
                valid_input = True

        except (KeyError, IndexError, ValueError):
            print("Invalid input!\n")

    return val


if __name__ == "__main__":
    config_path = "config.yaml"
    config = load_config(config_path)

    available_voices = load_voices(config["voices_path"])

    # keyboard_listener = keyboard.Listener(on_press=handle_key_press)
    # keyboard_listener.start()

    while True:
        selected_voice: Voice = None
        selecting_input = True
        print("\n---------------------\n\n")

        main_menu_selection = get_selection(["Start Voice Routine", "Exit Program"],  "Please select an option below:")
        print("\n")

        if main_menu_selection == 0:
            selected_voice_idx = get_selection(available_voices, "Please select a voice:", "name")
            # for i, v in enumerate(available_voices):
            #     print(f"[{i+1}] {v.name}")
            
            selected_voice = available_voices[selected_voice_idx]
            selecting_input = False
        elif main_menu_selection == 1:
            print("Exiting program!")
            exit()                

        print("Creating audio segments for selected voice!")
        #selected_voice.create_audio_segments()

        print("Ready!")

        selecting_input = True

        while selecting_input:
            selected_start = get_selection(selected_voice.routes.keys(), "Please select a route:")

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n Exiting Voice Routine!")