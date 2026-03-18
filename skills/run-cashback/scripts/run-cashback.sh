#!/usr/bin/env zsh
set -euo pipefail

FRONTEND_DIR="$HOME/Gits/cronos-cashback/src/ClientSide"
BACKEND_DIR="$HOME/Gits/cronos-cashback/src/Agoda.Cronos.Cashback.Web"

osascript <<EOF
tell application "Terminal"
  activate

  do script "cd '${FRONTEND_DIR}' && yarn watch:webview"

  tell application "System Events" to keystroke "t" using command down
  delay 0.5

  tell front window
    do script "cd '${BACKEND_DIR}' && ASPNETCORE_ENVIRONMENT=Development dotnet run" in last tab
  end tell
end tell
EOF