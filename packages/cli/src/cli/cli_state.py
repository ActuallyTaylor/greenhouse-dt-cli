from collections.abc import Callable
from threading import Lock, Thread
from time import sleep
from datetime import datetime, timedelta

from cli.db_interface import InfluxDBInterface, PlantSnapshot


class RepeatTimerTask:
    def __init__(self, reset_value: int, fn: Callable):
        self.lock = Lock()
        self.step_timer = reset_value
        self.reset_value = reset_value
        self.fn = fn
        self.thread = None
        self.running = False
        self.alive = True

    def run(self):
        if self.running or self.thread is not None:
            self.resume()
        self.thread = Thread(target=self._cycle)
        self.thread.start()
        self.running = True

    def resume(self):
        with self.lock:
            self.running = True

    def pause(self):
        with self.lock:
            self.running = False

    def get_timer(self) -> int:
        with self.lock:
            return self.step_timer

    def kill(self):
        with self.lock:
            self.alive = False

    def _cycle(self):
        while True:
            with self.lock:
                if not self.alive:
                    break
                if self.running:
                    self.step_timer -= 1
                    if self.step_timer == 0:
                        self.step_timer = self.reset_value
                        self.fn.__call__()

            sleep(1)
    
class DummyStressModel:
    """
    Replace this with the real model
    """
    def predict(self, temperature, humidity, nitrogen, moisture, light, ph_level):
        moisture_stress = (12*(moisture - 0.5)) ** 2
        nitrogen_stress = (nitrogen - 7) ** 2
        ph_stress = (10*(ph_level - 6.5)) ** 2
        light_stress = 0 if light > 20 else 20 - light

        return (0.4 * moisture_stress + 0.3 * nitrogen_stress + 0.2 * ph_stress + 0.1 * light_stress)

class DummyDepletionModel:
    """
    Replace this with the real model
    """
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

        self.pump_until = datetime.now()

        self.timescale = 3600 # 1 second simulates 1 hour
        self.run = False

        self.db_interface = InfluxDBInterface()

        self.sim_timer = RepeatTimerTask(12, self.step)
        self.last_timer_count = 0

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
        if self.run:
            self.sim_timer.run()
        else:
            self.sim_timer.pause()

    def get_timer(self):
        return self.sim_timer.get_timer()

    def water(self):
        self.moisture += 0.2
        self.pump_until = datetime.now() + timedelta(seconds=3)

    def fertilize(self):
        self.nitrogen += 0.5

    def stop_sim(self): 
        self.sim_timer.kill()
