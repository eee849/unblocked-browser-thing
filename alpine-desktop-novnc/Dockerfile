FROM alpine:latest

ENV DISPLAY=:0 \
    USER=user \
    HOME=/home/user

RUN apk update && apk add --no-cache \
    xfce4 \
    xfce4-terminal \
    x11vnc \
    xvfb \
    dbus \
    ttf-dejavu \
    mesa-dri-gallium \
    mesa-gl \
    bash \
    sudo \
    git \
    python3 \
    py3-pip \
    curl \
    upower \
    pm-utils \
    libnotify \
    xfce4-notifyd \
    xfce4-pulseaudio-plugin \
    xterm

# Add user
RUN adduser -D $USER && \
    echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    mkdir -p $HOME && \
    echo "exec startxfce4" > $HOME/.xinitrc && \
    chown -R $USER:$USER $HOME

    #use Xterm instead of XFCE4 terminal
    RUN mkdir -p /home/user/.config/xfce4/helpers \
 && echo 'TerminalEmulator=xterm' > /home/user/.config/xfce4/helpers.rc \
 && chown -R user:user /home/user/.config


# Install websockify (via pip)
RUN apk add --no-cache --virtual .build-deps \
    build-base \
    python3-dev \
    libffi-dev \
    openssl-dev \
    musl-dev && \
    pip install --break-system-packages websockify && \
    apk del .build-deps

# noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/websockify

COPY start-desktop.sh /start-desktop.sh
RUN chmod +x /start-desktop.sh

EXPOSE 6080
CMD ["/start-desktop.sh"]
