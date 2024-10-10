import os
import subprocess
import sys

def run_command(command):
    """Run a shell command."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr}")
        sys.exit(1)

def setup_openvpn():
    # Update package list and install OpenVPN and Easy-RSA
    print("Installing OpenVPN and Easy-RSA...")
    run_command("sudo apt-get update")
    run_command("sudo apt-get install -y openvpn easy-rsa")

    # Create Easy-RSA directory
    easy_rsa_dir = "/etc/openvpn/easy-rsa"
    run_command(f"make-cadir {easy_rsa_dir}")

    # Copy Easy-RSA files
    os.chdir(easy_rsa_dir)
    run_command("./easyrsa init-pki")

    # Build CA
    run_command("./easyrsa build-ca nopass")

    # Generate server certificate and key
    run_command("./easyrsa gen-req server nopass")
    run_command("./easyrsa sign-req server server")

    # Generate Diffie-Hellman parameters
    run_command("./easyrsa gen-dh")

    # Create OpenVPN server configuration
    server_conf = """
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh.pem
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 8.8.8.8"
push "dhcp-option DNS 8.8.4.4"
keepalive 10 120
cipher AES-256-CBC
user nobody
group nogroup
persist-key
persist-tun
status openvpn-status.log
verb 3
    """
    
    with open("/etc/openvpn/server.conf", "w") as f:
        f.write(server_conf)

    # Enable IP forwarding
    run_command("echo 'net.ipv4.ip_forward=1' | sudo tee -a /etc/sysctl.conf")
    run_command("sudo sysctl -p")

    # Start OpenVPN
    run_command("sudo systemctl start openvpn@server")
    run_command("sudo systemctl enable openvpn@server")

    print("OpenVPN setup completed. Use the following commands to manage OpenVPN:")
    print("sudo systemctl start openvpn@server")
    print("sudo systemctl stop openvpn@server")
    print("sudo systemctl status openvpn@server")

if __name__ == "__main__":
    setup_openvpn()
