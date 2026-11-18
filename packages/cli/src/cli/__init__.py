import sys
from asciimatics.effects import Effect, Sprite
from asciimatics.renderers import ColourImageFile
from asciimatics.scene import Scene
from asciimatics.screen import KeyboardEvent, Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.paths import Path
import greenhouse_lib

class PotState:
    def __init__(self, 
                    stress_model, 
                    depletion_model, 
                    stress: float, 
                    temperature: float, 
                    humidity: float, 
                    nitrogen: float, 
                    moisture: float, 
                    light: float, 
                    ph_level: float
                    ):
        self.stress_model = stress_model
        self.depletion_model = depletion_model

        self.stress = stress
        self.temperature = temperature
        self.humidity = humidity
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.light = light
        self.ph_level = ph_level

    def step(self):
        self.stress = self.stress_model.predict(
            self.temperature, 
            self.humidity, 
            self.nitrogen, 
            self.moisture, 
            self.light, 
            self.ph_level
        )
        
        resources = self.depletion_model.update(
            self.temperature, 
            self.humidity, 
            self.nitrogen, 
            self.moisture, 
            self.light, 
            self.ph_level
        )
        self.nitrogen = resources["nitrogen"]
        self.moisture = resources["moisture"]


    def get_health(self) -> float:
        return self.stress

class PlantSprite(Sprite):
    def __init__(self, screen, path, state: PotState):
        self.img_healthy = ColourImageFile(screen, "plant_healthy.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.img_unhealthy = ColourImageFile(screen, "plant_unhealthy.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.img_dead = ColourImageFile(screen, "plant_dead.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.state = state
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

        health = self.state.get_health()

        if health < 1:
            self._renderer_dict["default"] = self.img_dead
        elif health < 6:
            self._renderer_dict["default"] = self.img_unhealthy
        elif health < 15:
            self._renderer_dict["default"] = self.img_healthy
        else:
            self._renderer_dict["default"] = self.img_unhealthy


class PlantStats(Effect):
    def __init__(self, screen, state):
        super().__init__(screen)
        self.state = state
        
        def reset(self):
            return super().reset()
    
        @property
        def stop_frame(self):
            return super().stop_frame
    
        def _update(self, frame_no):
            super()._update(frame_no)

            # Need to look into asciimatics table rendering
        

class Controls(Effect):
    def __init__(self, screen, state):
        super().__init__(screen)
        self.state = state
        
        def reset(self):
            return super().reset()
    
        @property
        def stop_frame(self):
            return super().stop_frame
    
        def _update(self, frame_no):
            super()._update(frame_no)

            # Buttons for Step and Play/Pause (runs simulation at fixed rate, ex. 10 seconds?)
            # 



class GreenhouseScene(Scene):
    def __init__(self, screen, state):
        self.state = state
        center = (screen.width // 2, screen.height // 2)
        path = Path()
        path.jump_to(center[0], center[1])
        path.wait(100)
        plant = PlantSprite(screen, path, state)
        effects = [plant, ]
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
    state = PotState()

    scene = GreenhouseScene(screen, state)

    screen.play([scene], stop_on_resize=True)


def main() -> None:
    while True:
        try:
            Screen.wrapper(greenhouse)
            sys.exit(0)
        except ResizeScreenError:
            pass
