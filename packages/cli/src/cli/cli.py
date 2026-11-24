import sys

from asciimatics.exceptions import ResizeScreenError
from asciimatics.paths import Path
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from cli.cli_state import CLIState, DummyDepletionModel, DummyStressModel
from cli.ui_components import Controls, GreenhouseScene, PlantSprite, SimStats


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

    scene = GreenhouseScene(screen, state)

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
