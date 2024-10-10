# Use a lightweight base image
FROM linuxserver/wireguard

# Set environment variables
ENV PUID=1000
ENV PGID=1000
ENV WG_PORT=51820
ENV WG_SERVERURL=your_public_ip_or_domain
ENV WG_MTU=1420

# Expose the WireGuard port
EXPOSE 51820/udp

# Start WireGuard
CMD ["run"]
