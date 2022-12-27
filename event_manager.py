import pygame 
from singleton import Singleton

class EventManager(metaclass=Singleton):
    
    def initialize(self):
        self.__event_listeners = {}

    def register_event(self, event_type, callback):
        if event_type not in self.__event_listeners:
            self.__event_listeners[event_type] = [callback]
        else:
            self.__event_listeners[event_type].append(callback)
    
    def push(self, event):
        for listener in self.__event_listeners.get(event.type, []):
            listener(event)
        # print(self.__eventListeners)
    
    def pop_event(self, event_type, callback):
        self.__event_listeners[event_type].remove(callback)
        # print(self.__event_listeners[event_type])
