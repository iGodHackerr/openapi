FROM kylemanna/openvpn

ENV OVPN_DATA="/etc/openvpn"

# Copy the environment setup script
COPY ovpn_env.sh /etc/openvpn/ovpn_env.sh

# Initialize the OpenVPN configuration
RUN ovpn_genconfig -u udp://44.226.145.213
RUN ovpn_initpki nopass
