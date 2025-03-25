#!/bin/sh


export DISPLAY=:0
export USER=user
export HOME=/home/user
export MOZ_ENABLE_PULSEAUDIO=0

# Fix permissions
mkdir -p /tmp/.X11-unix
chown root:root /tmp/.X11-unix
chmod 1777 /tmp/.X11-unix

# Clean any old locks
rm -f /tmp/.X0-lock

# Start Xvfb
Xvfb :0 -screen 0 1280x800x24 &
sleep 2

# Start x11vnc
x11vnc -display :0 -forever -nopw -shared &
sleep 2

# Generate a test audio tone if you want:
sox -n -r 44100 -c 2 /tmp/test.wav synth 15 sine 440

# Option 1: Serve audio over HTTP directly
cd /tmp
python3 -m http.server 8080 &

# Option 2: Live-stream audio (optional - requires source)
# ffmpeg -re -i /tmp/test.wav -f mp3 -content_type audio/mpeg -ice_name "Void Stream" icecast://source:hackme@localhost:8000/mystream


# Start XFCE Desktop as user
su - $USER -c "
  export DISPLAY=:0
  startxfce4 &
  sleep 3

  # Create firefox profile if not found
  PROFILE_NAME=tor-profile
  if ! grep -q \"\$PROFILE_NAME\" ~/.mozilla/firefox/profiles.ini 2>/dev/null; then
    firefox -CreateProfile \"\$PROFILE_NAME\"
  fi

  PROFILE_PATH=\$(grep Path ~/.mozilla/firefox/profiles.ini | grep \"\$PROFILE_NAME\" | cut -d= -f2)
  mkdir -p ~/.mozilla/firefox/\"\$PROFILE_PATH\"
  cp /opt/firefox-user.js ~/.mozilla/firefox/\"\$PROFILE_PATH\"/user.js

  firefox --profile ~/.mozilla/firefox/\"\$PROFILE_PATH\" &
"


# 🔊 STREAM AUDIO (ALSA -> MP3 -> HTTP)
mkfifo /tmp/audiofifo

# Replace `hw:0` with correct ALSA device if needed
ffmpeg -f alsa -i hw:0 -acodec libmp3lame -ab 128k -f mp3 /tmp/audiofifo &

# Serve audio via raw HTTP stream
socat TCP-LISTEN:8080,reuseaddr,fork OPEN:/tmp/audiofifo,rdonly &

# Generate self-signed cert
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout /opt/noVNC/key.pem -out /opt/noVNC/cert.pem \
  -days 365 -subj "/CN=localhost"

# Start noVNC
cd /opt/noVNC
./utils/novnc_proxy \
  --vnc localhost:5900 \
  --listen 0.0.0.0:6080 \
  --cert /opt/noVNC/cert.pem \
  --key /opt/noVNC/key.pem \
  --web .