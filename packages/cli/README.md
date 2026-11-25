# CLI

The CLI can be divided into three vaguely-MVC layers:

- The UI elements (plant/actuator sprites, stat readout, controls)
- The simulation driver (currently using simple dummy behaviors)
- The CLI state (plant model, interaction state)

The UI is composed of several custom Effects rendered together as part of a Scene(defined in `ui_components.py`). These components are injected with an instance of the CLIState (`cli_state.py`), with which they access data and trigger actions. The CLIState contains a timer (using a simple threaded countdown) that periodically triggers the state to update based on its simulation model.

## Dependencies

### InfluxDB

The CLI pushes simulation data to an InfluxDB bucket, and will display a warning if it fails to push a snapshot. Ensure that you have InfluxDB set up and running, and that your `.env` file is configured correctly.

### InfluxDB Setup

1. Create a `secrets` directory in the project root. Within this directory, create the following files:

```
secrets/
| influxdb2-admin-password
| influxdb2-admin-token
| influxdb2-admin-username
```

2. Run `docker compose up -d` in the project root to start InfluxDB in a Docker container. This will also start the API, which is currently unused.

3. Open a web browser and navigate to `http://localhost:8086/`. Use the credentials you defined in the `secrets` directory to log in.

4. Click the Organization icon in the sidebar (colored square with a single letter in it). Click "Create Organization" and assign it a name and starting bucket name (the example `.env` defines these both as `greenhouse`).

5. In your new Organization, hover over the Load Data icon in the sidebar (horizontal line with vertical arrow above it) and click "API Tokens". Generate a custom API token with read and write permissions in the bucket you just created. Copy and paste this API token into the `.env` file under `INFLUXDB_TOKEN`

## Usage

After building the UV project, the CLI can be run using the following command: 

```shell
uv run --package cli cli <shelf> <pot>
```

with the `shelf` and `pot` arguments used to identify the specific pot which the CLI instance will represent.
