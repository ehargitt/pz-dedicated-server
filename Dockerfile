FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install steamcmd dependencies and steamcmd itself
RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository -y multiverse \
    && apt-get update \
    && echo "steamcmd steam/question select I AGREE" | debconf-set-selections \
    && apt-get install -y steamcmd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the server
RUN useradd -m -s /bin/bash pzuser \
    && mkdir -p /opt/pzserver /home/pzuser/Zomboid \
    && chown -R pzuser:pzuser /opt/pzserver /home/pzuser/Zomboid

COPY --chown=pzuser:pzuser entrypoint.sh /home/pzuser/entrypoint.sh
COPY --chown=pzuser:pzuser update_zomboid.txt /home/pzuser/update_zomboid.txt
RUN chmod +x /home/pzuser/entrypoint.sh

EXPOSE 16261/udp 16262/udp

VOLUME ["/opt/pzserver", "/home/pzuser/Zomboid"]

USER pzuser
WORKDIR /home/pzuser

ENTRYPOINT ["/home/pzuser/entrypoint.sh"]
