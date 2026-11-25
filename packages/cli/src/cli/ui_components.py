from datetime import datetime, timedelta

from asciimatics.effects import Sprite
from asciimatics.paths import Path
from asciimatics.renderers import ColourImageFile
from asciimatics.scene import Scene
from asciimatics.screen import KeyboardEvent, Screen, StopApplication
from asciimatics.widgets import Button, Divider, Frame, Label, Layout, PopUpDialog

from cli.cli_state import CLIState
from cli.ui_theme import UI_THEME


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

        self._theme = "custom"
        self.palette = UI_THEME

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
    def __init__(self, screen, state: CLIState):
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
        self.layout = Layout([1, 1, 1])
        self.add_layout(self.layout)
        self.pp_button = Button("Play", name="button_play_pause", on_click=self._play_pause)
        self.layout.add_widget(self.pp_button, 0)
        self.timer_label = Label("0-0", name="label_sim_timer")
        self.layout.add_widget(self.timer_label, 1)
        self.layout.add_widget(Button("Step", name="button_step", on_click=self._step), 2)
        self.layout.add_widget(Button("Water", name="button_water", on_click=self._water), 0)
        self.layout.add_widget(Button("Fertilize", name="button_fertilize", on_click=self._fertilize), 1)
        self.layout.add_widget(Button("Exit", name="button_exit", on_click=self._quit), 2)

        self.quit_popup = PopUpDialog(self._screen, "Are you sure?", ["Yes", "No"],
                    has_shadow=True, on_close=self._quit_on_yes)

        self._theme = "custom"
        self.palette = UI_THEME

        self.fix()

    def reset(self):
        return super().reset()

    def _play_pause(self):
        self.state.play_pause()

    def _step(self):
        self.state.step()

    def _water(self):
        self.state.water()

    def _fertilize(self):
        self.state.fertilize()

    def _quit(self):
        self._scene.add_effect(self.quit_popup)
        
    def _quit_on_yes(self, selected):
        if selected == 0:
            self.state.stop_sim()
            raise StopApplication("User exit")

    @property
    def stop_frame(self):
        return super().stop_frame

    def _update(self, frame_no):
        super()._update(frame_no)

        self.pp_button.text = "Pause" if self.state.run else "Play"
        self.timer_label.text = f"{self.state.get_timer()}"

class PumpSprite(Sprite):
    def __init__(self, screen, path, state: CLIState):

        self.stopped_frame = ColourImageFile(screen, 
                                    "packages/cli/src/cli/assets/pump_0.png",  
                                    round(screen.height*0.2), 
                                    uni=screen.unicode_aware,
                                    dither=screen.unicode_aware
                                    ) 
        self.anim_frames = [
            ColourImageFile(screen, 
                            f"packages/cli/src/cli/assets/pump_{i}.png",  
                            round(screen.height*0.2), 
                            uni=screen.unicode_aware,
                            dither=screen.unicode_aware
                            ) 
            for i in range(1, 4)
        ]
        self.state = state
        self.anim_frame = 0
        self.frame_interval = 0.2
        self.next_frame_time = datetime.now()
        super().__init__(
            screen=screen, 
            path=path, 
            renderer_dict={
                "default": self.stopped_frame
            }, 
            start_frame=0, 
            stop_frame=0
        )

    def update(self, frame_no):
        super().update(frame_no)
        t = datetime.now()
        if t < self.state.pump_until:
            if t > self.next_frame_time:
                self.next_frame_time = t + timedelta(seconds=self.frame_interval)
                self.anim_frame = (self.anim_frame + 1) % 3
                self._renderer_dict["default"] = self.anim_frames[self.anim_frame]
        else:
            self._renderer_dict["default"] = self.stopped_frame
        

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


class GreenhouseScene(Scene):
    def __init__(self, screen, state: CLIState):
        plant_path = Path()
        plant_root = (int(screen.width * 0.4), int(screen.height * 0.4))
        plant_path.jump_to(plant_root[0], plant_root[1])
        plant = PlantSprite(screen, plant_path, state)
        stats = SimStats(screen, state)
        pump_root = (int(screen.width * 0.875), int(screen.height * 0.65))
        pump_path = Path()
        pump_path.jump_to(pump_root[0], pump_root[1])
        pump = PumpSprite(screen, pump_path, state)
        controls = Controls(screen, state)
        effects = [stats, controls, plant, pump]
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