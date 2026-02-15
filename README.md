# On-Air Indicator

Toggles smart home devices (Tuya plugs, Kasa light strips) when your Mac's camera
activates, giving you a physical on-air indicator for video calls. Works by streaming
macOS system logs for camera state changes.

Inspired by [OnAir](https://github.com/henrik242/OnAir).

## Requirements

- macOS (uses the `log stream` command for camera event detection)
- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Installation

Install as a uv tool so the `on-air-indicator` command is available globally:

```bash
uv tool install .
```

This places the binary on your PATH (typically `~/.local/bin/on-air-indicator`).

## Configuration

Copy the sample config and fill in your device details:

```bash
mkdir -p ~/.config/on-air-indicator
cp config.sample.toml ~/.config/on-air-indicator/config.toml
```

Edit `~/.config/on-air-indicator/config.toml` with your device IDs, IPs, and keys.
See `config.sample.toml` for the expected format.

## Usage

Run directly:

```bash
on-air-indicator
```

Or run as a module:

```bash
uv run python -m on_air_indicator
```

### Running via launchd

To run automatically at login, first install with `uv tool install .` (see above),
then use the setup script. It finds the installed binary, generates the plist, and
loads the launch agent:

```bash
./setup-launchd.bash
```

Re-run the script any time the binary path changes (e.g. after reinstalling with uv).

## How It Works

The tool runs `/usr/bin/log stream` as a subprocess, filtering for
`com.apple.controlcenter` camera state change events. When a camera turns on
(an app starts using it), all configured devices are turned on. When the camera
turns off (the app list becomes empty), all devices are turned off. Each device
is toggled independently so a single device failure doesn't affect the others.

## References

- [tinytuya](https://pypi.org/project/tinytuya/)
- [python-kasa](https://github.com/python-kasa/python-kasa)
