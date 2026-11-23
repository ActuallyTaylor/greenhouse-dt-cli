import sys
from asciimatics.effects import Effect, Sprite
from asciimatics.renderers import ColourImageFile
from asciimatics.scene import Scene
from asciimatics.screen import KeyboardEvent, Screen
from asciimatics.widgets import Divider, Frame, Label, Layout, Button, PopUpDialog
from asciimatics.exceptions import ResizeScreenError, StopApplication
from asciimatics.paths import Path
from greenhouse_lib import GrowthStrategy, PlantStressModel
from cli.db_interface import PlantSnapshot, InfluxDBInterface

class DummyStressModel:
    def predict(self, temperature, humidity, nitrogen, moisture, light, ph_level):
        moisture_stress = (12*(moisture - 0.5)) ** 2
        nitrogen_stress = ((nitrogen - 7)) ** 2
        ph_stress = (10*(ph_level - 6.5)) ** 2
        light_stress = 0 if light > 20 else 20 - light

        return (0.4 * moisture_stress + 0.3 * nitrogen_stress + 0.2 * ph_stress + 0.1 * light_stress)

class DummyDepletionModel:
    def update(self, stress, temperature, humidity, nitrogen, moisture, light, ph_level):
        return {
            "moisture": moisture - (0.025 / min(1, stress)) - (0 if humidity > moisture else (moisture - humidity) * 0.25), 
            "nitrogen": nitrogen - (0.25 / min(1, stress))
        }

class CLIState:
    def __init__(self, 
                    shelf_id: int, 
                    pot_id: int, 
                    stress_model: DummyStressModel, 
                    depletion_model: DummyDepletionModel, 
                    stress: float, 
                    temperature: float, 
                    humidity: float, 
                    nitrogen: float, 
                    moisture: float, 
                    light: float, 
                    ph_level: float
                    ):
        self.shelf_id = shelf_id
        self.pot_id = pot_id
        
        self.stress_model = stress_model
        self.depletion_model = depletion_model

        self.stress = stress
        self.temperature = temperature
        self.humidity = humidity
        self.nitrogen = nitrogen
        self.moisture = moisture
        self.light = light
        self.ph_level = ph_level

        self.timescale = 3600 # 1 second simulates 1 hour
        self.step_timer = 0
        self.run = False

        self.db_interface = InfluxDBInterface()

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
            self.stress, 
            self.temperature, 
            self.humidity, 
            self.nitrogen, 
            self.moisture, 
            self.light, 
            self.ph_level
        )
        self.nitrogen = resources["nitrogen"]
        self.moisture = resources["moisture"]

        snapshot = PlantSnapshot(self.shelf_id, 
                                 self.pot_id, 
                                 self.stress, 
                                 self.temperature, 
                                 self.humidity, 
                                 self.nitrogen, 
                                 self.moisture, 
                                 self.light, 
                                 self.ph_level)

        self.db_interface.write_snapshot(snapshot)

    def get_health(self) -> float:
        return self.stress

    def play_pause(self):
        self.run = not self.run


class PlantSprite(Sprite):
    def __init__(self, screen, path, state: CLIState):
        self.img_healthy = ColourImageFile(screen, "packages/cli/src/cli/assets/plant_healthy.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.img_unhealthy = ColourImageFile(screen, "packages/cli/src/cli/assets/plant_unhealthy.png", round(screen.height*0.75), uni=screen.unicode_aware,
                                      dither=screen.unicode_aware)
        self.img_dead = ColourImageFile(screen, "packages/cli/src/cli/assets/plant_dead.png", round(screen.height*0.75), uni=screen.unicode_aware,
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

        if health > 20:
            self._renderer_dict["default"] = self.img_dead
        elif health > 10:
            self._renderer_dict["default"] = self.img_unhealthy
        elif health :
            self._renderer_dict["default"] = self.img_healthy
       

class SimStats(Frame):
    def __init__(self, screen: Screen, state: CLIState):
        super().__init__(screen,
                         screen.height * 2 // 5, 
                         screen.width * 1 // 4,
                         x=screen.width * 3 // 4,
                         y=screen.height * 1 // 8,
                         can_scroll=False,
                         title="Simulator Stats"
                         )
        
        self.state = state

        layout = Layout([3, 2])

        self.add_layout(layout)
        layout.add_widget(Label("Temperature"), 0)
        self.temp_value = Label("71 °F", name="value_temperature")
        layout.add_widget(self.temp_value, 1)
        
        layout.add_widget(Label("Humidity"), 0)
        self.humid_value = Label("50%", name="value_humidity")
        layout.add_widget(self.humid_value, 1)
        
        layout.add_widget(Label("Light"), 0)
        self.light_value = Label("24 mol/sqm/day", name="value_light")
        layout.add_widget(self.light_value, 1)

        layout.add_widget(Divider(), 0)
        layout.add_widget(Divider(), 1)

        layout.add_widget(Label(f"Shelf {state.shelf_id}"), 0)
        layout.add_widget(Label(f"Pot {state.pot_id}"), 1)

        layout.add_widget(Divider(), 0)
        layout.add_widget(Divider(), 1)

        layout.add_widget(Label("Moisture"), 0)
        self.moist_value = Label("35%", name="value_moisture")
        layout.add_widget(self.moist_value, 1)
        
        layout.add_widget(Label("Nitrogen"), 0)
        self.nit_value = Label("7.0 mg/kg", name="value_nitrogen")
        layout.add_widget(self.nit_value, 1)
        
        layout.add_widget(Label("Soil pH"), 0)
        self.ph_value = Label("7.0 mg/kg", name="value_ph")
        layout.add_widget(self.ph_value, 1)
        
        layout.add_widget(Label("Stress"), 0)
        self.stress_value = Label("1.4", name="value_stress")
        layout.add_widget(self.stress_value, 1)

        self.fix()

    def reset(self):
        return super().reset()

    @property
    def stop_frame(self):
        return super().stop_frame

    def _update(self, frame_no):
        super()._update(frame_no)
        self.temp_value.text = f"{self.state.temperature:.1f} °F"
        self.humid_value.text = f"{100*self.state.humidity:.0f}%"
        self.light_value.text = f"{self.state.light:.1f} mol/sqm/day"
        self.moist_value.text = f"{100*self.state.moisture:.0f}%"
        self.nit_value.text = f"{self.state.nitrogen:.1f} mg/kg"
        self.ph_value.text = f"{self.state.ph_level:.1f}"
        self.stress_value.text = f"{self.state.stress:.1f}"

class Controls(Frame):
    def __init__(self, screen, state):
        super().__init__(screen, 
                         screen.height * 1 // 5, 
                         screen.width * 1 // 2, 
                         x=screen.width * 1 // 4, 
                         y=screen.height * 4 // 5, 
                         hover_focus=True, 
                         can_scroll=False, 
                         title="Pot Sim Controls"
                         )
        
        self.state = state
        self.layout = Layout([1, 1])
        self.add_layout(self.layout)
        self.pp_button = Button("Play", name="button_play_pause", on_click=self._play_pause)
        self.layout.add_widget(self.pp_button, 0)
        self.layout.add_widget(Button("Step", name="button_step", on_click=self._step), 1)
        self.layout.add_widget(Button("Water", name="button_water", on_click=self._water), 0)
        self.layout.add_widget(Button("Fertilize", name="button_fertilize", on_click=self._fertilize), 1)
        self.layout.add_widget(Button("Exit", name="button_exit", on_click=self._quit), 1)

        self.quit_popup = PopUpDialog(self._screen, "Are you sure?", ["Yes", "No"],
                    has_shadow=True, on_close=self._quit_on_yes)
        
        self.fix()

    def reset(self):
        return super().reset()

    def _play_pause(self):
        self.state.play_pause()

    def _step(self):
        self.state.step()

    def _water(self):
        self.state.moisture += 0.2

    def _fertilize(self):
        self.state.nitrogen += 0.5

    def _quit(self):
        self._scene.add_effect(self.quit_popup)
        
    def _quit_on_yes(self, selected):
        if selected == 0:
            raise StopApplication("User exit")

    @property
    def stop_frame(self):
        return super().stop_frame

    def _update(self, frame_no):
        super()._update(frame_no)

        self.pp_button.text = "Pause" if self.state.run else "Play"


class GreenhouseScene(Scene):
    def __init__(self, screen, state: CLIState):
        self.state = state
        center = (screen.width // 2, screen.height // 2)
        path = Path()
        path.jump_to(center[0], center[1])
        path.wait(100)
        plant = PlantSprite(screen, path, state)
        status = SimStats(screen, state)
        controls = Controls(screen, state)
        effects = [plant, status, controls]
        super().__init__(effects, -1)


    def process_event(self, event):
        if super().process_event(event) is None:
            return

        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c in (ord("x"), ord("X")):
                raise StopApplication("User exit")
            else:
                return event
        else:
            return event


        
def greenhouse(screen: Screen):
    state = CLIState(
        shelf_id=int(sys.argv[1]), 
        pot_id=int(sys.argv[2]),
        stress_model=DummyStressModel(), 
        depletion_model=DummyDepletionModel(), 
        stress=0, 
        temperature=71, 
        humidity=0.4, 
        nitrogen=6.5, 
        moisture=0.53, 
        light=19, 
        ph_level=6.6
    )

    # scene = GreenhouseScene(screen, state)
    path = Path()
    plant_root = (int(screen.width*0.4), int(screen.height * 0.4))
    path.jump_to(plant_root[0], plant_root[1])
    plant = PlantSprite(screen, path, state)
    stats = SimStats(screen, state)
    controls = Controls(screen, state)
    effects = [stats, controls, plant]
    # effects = [stats, controls]
    scene = Scene(effects)

    screen.play([scene], stop_on_resize=True, allow_int=True)

def main() -> None:
    while True:
        try:
            Screen.wrapper(greenhouse)
            sys.exit(0)
        except ResizeScreenError:
            pass

if __name__ == "__main__":
    main()
