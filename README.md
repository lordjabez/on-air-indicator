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

Edit `~/.config/on-air-indicator/config.toml` with your device details.
See `config.sample.toml` for the expected format.

### Getting Tuya device credentials

Tuya devices require a device ID, local key, and IP address. To obtain these:

1. Pair your devices using the [Smart Life](https://apps.apple.com/app/smart-life/id1115101477)
   or [Tuya Smart](https://apps.apple.com/app/tuya-smart/id1034649547) app
2. Create a developer account at [iot.tuya.com](https://iot.tuya.com)
3. Create a Cloud Project — choose the data center
   [region](https://github.com/jasonacox/tinytuya#setup-wizard---getting-local-keys)
   that matches your Smart Life account
4. Note your **API ID** (Access ID/Client ID) and **API Secret** (Access Secret/Client Secret)
   from the project's Authorization Key section
5. Under **Devices > Link Tuya App Account**, scan the QR code with the Smart Life app
   (Me tab > upper-right scan icon) to link your devices to the project
6. Under **Service API**, subscribe to **IoT Core** and **Authorization Token Management**
   (subscriptions expire periodically and need renewal)
7. Run the tinytuya wizard to pull device IDs and local keys:

```bash
uvx tinytuya wizard
```

This produces a `devices.json` file containing the `id` and `key` for each device.
Use `tinytuya scan` to discover local IP addresses on your network.

### Getting Kasa device IP addresses

Kasa (TP-Link) devices only need an IP address. Pair your device using the
[Kasa Smart](https://apps.apple.com/app/kasa-smart/id1034035493) app first,
then discover it on your network using the
[python-kasa](https://python-kasa.readthedocs.io/en/latest/cli.html) CLI:

```bash
uvx python-kasa discover
```

This broadcasts on UDP ports 9999 and 20002 and prints each device's IP, model,
and alias. Newer TP-Link devices (those responding on port 20002) require your
TP-Link cloud credentials:

```bash
uvx python-kasa discover --username you@example.com --password your-password
```

You can also set `KASA_USERNAME` and `KASA_PASSWORD` environment variables instead
of passing them on every command.

Alternatively, check your router's DHCP client list for the device IP.

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
