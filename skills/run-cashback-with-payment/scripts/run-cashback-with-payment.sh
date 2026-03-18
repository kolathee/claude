#!/usr/bin/env zsh
set -euo pipefail

FRONTEND_DIR="$HOME/Gits/cronos-cashback/src/ClientSide"
BACKEND_DIR="$HOME/Gits/cronos-cashback/src/Agoda.Cronos.Cashback.Web"
PAYMENT_DIR="$HOME/Gits/agoda-com-spa-mobile/Agoda.Mobile.Client/src/lib/payment-sdk"

osascript <<EOF
tell application "Terminal"
  activate

  -- Tab 1: cashback frontend
  do script "cd '${FRONTEND_DIR}' && yarn watch:webview"

  -- Tab 2: cashback backend
  tell application "System Events" to keystroke "t" using command down
  delay 0.5
  tell front window
    do script "cd '${BACKEND_DIR}' && ASPNETCORE_ENVIRONMENT=Development dotnet run" in last tab
  end tell

  -- Tab 3: payment sdk service
  tell application "System Events" to keystroke "t" using command down
  delay 0.5
  tell front window
    do script "cd '${PAYMENT_DIR}' && pnpm start:payment:mobile" in last tab
  end tell
end tell
EOF