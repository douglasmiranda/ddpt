# We sill:
# - create a simple droplet
# - allow ssh access to our user with sshkey
# - configure firewall to allow the desired connections

provider "digitalocean" {
  token = "${var.digitalocean_token}"
}

data "digitalocean_ssh_key" "me" {
  name = "${var.digitalocean_sshkey_name}"
}

resource "digitalocean_droplet" "ddpt" {
  image = "debian-9-x64"
  name = "ddpt-web-1"
  region = "nyc3"
  size = "s-1vcpu-1gb"
  monitoring = true
  private_networking = true
  tags = ["ddpt", "web"]

  ssh_keys = ["${data.digitalocean_ssh_key.me.fingerprint}"]
}

resource "digitalocean_firewall" "web" {
  name = "ssh-docker-http-https"

  droplet_ids = ["${digitalocean_droplet.ddpt.id}"]

  # Allow incoming ssh, http, https, icmp and Docker remote connection
  inbound_rule = [
    {
      protocol = "tcp"
      port_range = "22"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    # Docker remote connection
    {
      protocol = "tcp"
      port_range = "2376"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "tcp"
      port_range = "80"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "tcp"
      port_range = "443"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "icmp"
      source_addresses = ["0.0.0.0/0", "::/0"]
    },
  ]

  outbound_rule = [
    {
      protocol = "tcp"
      port_range = "1-6553"
      destination_addresses   = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "udp"
      port_range = "1-6553"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    },
    {
      protocol = "icmp"
      destination_addresses = ["0.0.0.0/0", "::/0"]
    }
  ]
}
