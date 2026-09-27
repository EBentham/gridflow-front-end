#!/bin/bash
# shot.sh name height band scale : headless screenshot of static/<name>.html, then slice
W=$(cygpath -m "$PWD")
"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,$2 --virtual-time-budget=9000 --screenshot="$W/shots/$1.png" "http://127.0.0.1:9713/static/$1.html?v=$RANDOM" 2>/dev/null | tail -1
uv run --system-certs --no-project --with pillow python crop.py $1 ${3:-1300} ${4:-.6}
