#!/bin/sh
set -e

# Start virtual X server
Xvfb :0 -screen 0 1280x800x24 &
sleep 2
export DISPLAY=:0

# Launch XFCE with session bus
su - user -c "DISPLAY=:0 dbus-launch xfce4-session" &

# Start VNC server (no password, shared)
x11vnc -display :0 -nopw -forever -shared -quiet &

# Start noVNC web server
cd /opt/noVNC
./utils/novnc_proxy --vnc localhost:5900 --listen 6080

# Launch terminal automatically after desktop starts
su - user -c "DISPLAY=:0 xterm" &

