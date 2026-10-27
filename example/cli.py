import time

from asciimatics.effects import BannerText, Effect, Print, Scroll, Sprite
from asciimatics.renderers import ColourImageFile, FigletText, ImageFile, StaticRenderer
from asciimatics.scene import Scene
from asciimatics.screen import KeyboardEvent, Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.paths import Path
import sys
import random

import logging

logging.basicConfig(filename="debug.log", level=logging.DEBUG)

class State:
    def __init__(self):
        self.water_level = 10

    def update(self):
        if random.random() < 0.05 and self.water_level > 0:
            self.water_level -= 1   

        return self.water_level

    def get_water_level(self):
        return self.water_level

    def water(self):
        self.water_level += 3


class Plant(Sprite):
    def __init__(self, screen, path, state: State):
        self.img_healthy = ColourImageFile(screen, "plant_healthy.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.img_unhealthy = ColourImageFile(screen, "plant_unhealthy.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.img_dead = ColourImageFile(screen, "plant_dead.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.state = state
        self.logger = logging.getLogger("plant")
        super().__init__(
            screen=screen, 
            path=path, 
            renderer_dict={
                "default": self.img_healthy
            }, 
            start_frame=0, 
            stop_frame=0
        )

    def update(self, frame_no):
        super().update(frame_no)

        water_level = self.state.update()
        if water_level < 1:
            self._renderer_dict["default"] = self.img_dead
        elif water_level < 6:
            self._renderer_dict["default"] = self.img_unhealthy
        elif water_level < 15:
            self._renderer_dict["default"] = self.img_healthy
        else:
            self._renderer_dict["default"] = self.img_unhealthy

        self._screen.print_at("Press \"W\" to water the plant!", 0, 0)


class WaterBar(Effect):
    def __init__(self, screen: Screen, state: State):
        super().__init__(screen)
        self.state = state

    def reset(self):
        return super().reset()

    @property
    def stop_frame(self):
        return super().stop_frame

    def _update(self, frame_no):
        super()._update(frame_no)

        water_level = self.state.get_water_level()

        left = round(self._screen.width * 0.75)
        right = round(self._screen.width * 0.8)
        bottom = round(self._screen.height * 0.9)
        top = round(self._screen.height * 0.1)

        self._screen.fill_polygon([[[left, bottom], [right, bottom], [right, top], [left, top]]], colour=0, bg=0)

        top = round(self._screen.height * (0.9 - (water_level * 0.04)))

        self._screen.fill_polygon([[[left, bottom], [right, bottom], [right, top], [left, top]]], colour=4, bg=4)
        self._screen.print_at(f"{water_level} ", left+1, top-1)
        self._screen.print_at("H2O", left+1, bottom+1)


class GreenhouseScene(Scene):
    def __init__(self, screen, state):
        self.state = state
        center = (screen.width // 2, screen.height // 2)
        path = Path()
        path.jump_to(center[0], center[1])
        path.wait(100)
        plant = Plant(screen, path, state)
        bar = WaterBar(screen, state)
        effects = [plant, bar]
        super().__init__(effects, -1)


    def process_event(self, event):
    # Allow standard event processing first
        if super().process_event(event) is None:
            return

        # If that didn't handle it, check for a key that this demo understands.
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c in (ord("x"), ord("X")):
                raise StopApplication("User exit")
            elif c == ord("w"):
                self.state.water()
            else:
                # Not a recognised key - pass on to other handlers.
                return event
        else:
            # Ignore other types of events.
            return event


        
def greenhouse(screen: Screen):
    state = State()

    scene = GreenhouseScene(screen, state)

    screen.play([scene], stop_on_resize=True)

if __name__ == "__main__":
    while True:
        try:
            Screen.wrapper(greenhouse)
            sys.exit(0)
        except ResizeScreenError:
            pass
        