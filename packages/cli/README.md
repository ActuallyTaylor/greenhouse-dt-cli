# CLI

The CLI can be divided into three vaguely-MVC layers:

- The UI elements (plant/actuator sprites, stat readout, controls)
- The simulation driver (currently using simple dummy behaviors)
- The CLI state (plant model, interaction state)

The UI is composed of several custom Effects rendered together as part of a Scene(defined in `ui_components.py`). These components are injected with an instance of the CLIState (`cli_state.py`), with which they access data and trigger actions. The CLIState contains a timer (using a simple threaded countdown) that periodically triggers the state to update based on its simulation model.

## Usage

After building the UV project, the CLI can be run using the following command: 

```shell
uv run --package cli cli <shelf> <pot>
```

with the `shelf` and `pot` arguments used to identify the specific pot which the CLI instance will represent.
