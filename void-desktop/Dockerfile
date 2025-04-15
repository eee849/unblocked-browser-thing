FROM voidlinux/voidlinux-musl:latest


ENV DISPLAY=:0 \
    USER=user \
    HOME=/home/user

# Step 1: Use HTTP mirror first
RUN echo "repository=http://mirror.yandex.ru/mirrors/voidlinux/current/musl" > /etc/xbps.d/00-repository-main.conf

# Step 2: Upgrade xbps itself first (required!)
RUN xbps-install -Sy xbps

# Step 3: Now install ca-certificates safely
RUN xbps-install -Sy ca-certificates && update-ca-certificates

# Optional: switch to HTTPS repo now
RUN echo "repository=https://mirror.clarkson.edu/voidlinux/current/musl" > /etc/xbps.d/00-repository-main.conf && \
    xbps-install -Sy

    RUN echo "repository=https://mirror.clarkson.edu/voidlinux/current/musl" > /etc/xbps.d/00-repository-main.conf && \
    xbps-pkgdb -m hold base-files && \
    xbps-install -Syuy --force
RUN xbps-install -y base-devel
RUN xbps-install -y xfce4 xfce4-terminal
RUN xbps-install -y firefox
RUN xbps-install -y alsa-utils xorg xterm xorg-server x11vnc
RUN xbps-install -y git curl wget sudo sox ffmpeg python3 python3-pip
RUN xbps-install -y bash
RUN xbps-install -y xorg-server-xvfb
RUN xbps-install -y tor


# Optional: install simple Python HTTP server (usually included)
RUN xbps-install -y python3


# Add user
RUN useradd -m -G audio,video,wheel -s /bin/bash $USER && \
    echo "$USER ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Copy config
COPY firefox-user.js /opt/firefox-user.js

# Get noVNC
RUN git clone https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone https://github.com/novnc/websockify /opt/noVNC/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Install websockify
# Add build dependencies needed for numpy and websockify
# Create and activate a venv to install websockify
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-deps websockify && \
    ln -s /opt/venv/bin/websockify /usr/bin/websockify

    

EXPOSE 6080
COPY start-desktop.sh /start-desktop.sh
RUN chmod +x /start-desktop.sh
CMD ["/start-desktop.sh"]
