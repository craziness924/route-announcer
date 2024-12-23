import os
import time

import json

import pydub.playback
import yaml
import pydub
from pydub import AudioSegment

from pynput import keyboard

HOTKEYS= {
    "next_announcement": keyboard.HotKey.parse('<alt>+b'),
    "skip_next_announcement": keyboard.HotKey.parse('<alt>+m')
}

def handle_hotkeys():
    return

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
    def get_stops_for_route(self, route_key):
        route = self.routes[route_key]
        stops = []

        for announcement in route:
            try:
                if announcement['type'] != "stop":
                    continue
            except KeyError:
                print(f"Could not parse a stop in voice {self.name} for route {route_key}!")
                continue
            stops.append(announcement["name"])

        return stops
    def get_announcements_for_route(self, route_key):
        announcements = []

        route_announcements = self.routes[route_key]

        return route_announcements
    def find_index_of_stop(self, route_key, stop_name):
        route = self.routes[route_key]

        for i, s in enumerate(route):
            if s["name"] == stop_name:
                return i
                
def play_announcement(voice: Voice, route_key, announcement_index):
    announcement = voice.routes[route_key][announcement_index]
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
            
            if val <= len(options)-1:
                valid_input=True

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
        print("\n---------------------\n")

        main_menu_selection = get_selection(["Start Voice Routine", "Exit Program"],  "Please select an option below:")

        if main_menu_selection == 0:
            selected_voice_idx = get_selection(available_voices, "Please select a voice:", "name")           
            selected_voice = available_voices[selected_voice_idx]
        elif main_menu_selection == 1:
            print("Exiting!")
            exit()                

        print("Creating audio segments for selected voice!")

        print("Ready!")


        selected_route_idx = get_selection(list(selected_voice.routes.keys()), "Please select a route:")
        
        selected_route = list(selected_voice.routes.keys())[selected_route_idx]

        route_stops = selected_voice.get_stops_for_route(selected_route)
        selected_start_idx = get_selection(route_stops, "Please select a starting stop:")
        selected_start = route_stops[selected_start_idx]

        possible_destinations = list(route_stops)
        possible_destinations.remove(selected_start)

        selected_destination_idx = get_selection(possible_destinations, "Please select a destination stop:")
        selected_destination = possible_destinations[selected_destination_idx]

        current_index = selected_voice.find_index_of_stop(route_key=selected_route, stop_name=selected_start)
        max_index = len(selected_voice.routes[selected_route])-1
        
        stop_hotkey_obj= keyboard.HotKey(HOTKEYS["next_announcement"], on_activate=None)
        skip_hotkey_obj = keyboard.HotKey(HOTKEYS["skip_next_announcement"], on_activate=None)
        

    
        # From pynput example documents: https://pynput.readthedocs.io/en/latest/keyboard.html#global-hotkeys
        while True:
            time.sleep(0.3)

            try:
                with keyboard.Listener(
                    on_press=stop_hotkey_obj.press,
                    on_release=stop_hotkey_obj.release) as l:
                    
                    l.join()

                    if stop_hotkey_obj._state == stop_hotkey_obj._keys:
                        print("buh")
                        play_announcement(voice=selected_voice, route_key=selected_route, announcement_index=current_index)
                        
                        for k in HOTKEYS["next_announcement"]: 
                            stop_hotkey_obj.release(k)

                    if skip_hotkey_obj._state == skip_hotkey_obj._keys:
                        print("Skipping next!")                        
                        for k in HOTKEYS["skip_next_announcements"]: 
                            skip_hotkey_obj.release(k)

                    if current_index == max_index:
                        current_index = 0
                    else: 
                        current_index+=1
            except KeyboardInterrupt:
                print("\nExiting Voice Routine!")
                break