#!/usr/bin/env bash
set -euo pipefail

LABEL="com.makingofthings.OnAirIndicator"
PLIST_TEMPLATE="$(dirname "$0")/com.makingofthings.OnAirIndicator.plist"
PLIST_DEST="$HOME/Library/LaunchAgents/$LABEL.plist"

binary_path=$(command -v on-air-indicator 2>/dev/null || true)
if [[ -z "$binary_path" ]]; then
    echo "Error: on-air-indicator not found on PATH." >&2
    echo "Install it first: uv tool install ." >&2
    exit 1
fi

# Unload existing agent if present
if launchctl list "$LABEL" &>/dev/null; then
    echo "Unloading existing agent..."
    launchctl unload "$PLIST_DEST" 2>/dev/null || true
fi

# Generate plist from template
sed "s|{{BINARY_PATH}}|$binary_path|g" "$PLIST_TEMPLATE" > "$PLIST_DEST"

echo "Installed plist to $PLIST_DEST (binary: $binary_path)"

launchctl load "$PLIST_DEST"
echo "Agent loaded."
