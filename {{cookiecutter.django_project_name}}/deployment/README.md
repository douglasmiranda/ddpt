# Deployment

> NOTE: This text is a working in progress.

Deployment is always a complex subject to cover, it shouldn't be.. but it is. The approach we'll take here
it's not the easiest or a definitive guide on how to deploy your Django with Docker.

If you run a "simple" Django app you may be better off starting things as simple as possible and from there
you can expand as much as you like.

I won't cover the topics in-depth. If you're not familiar with some subject covered here, you should do some
research about it.

- [Deployment](#deployment)
  - [Provisioning](#provisioning)
    - [Terraform](#terraform)
      - [Digital Ocean](#digital-ocean)
  - [Configuration Management](#configuration-management)
    - [Ansible](#ansible)
  - [Docker](#docker)
    - [Docker Swarm](#docker-swarm)
    - [Secrets](#secrets)
  - [Databases](#databases)
    - [Postgres](#postgres)
    - [Redis](#redis)
  - [Object Storage (File/Media)](#object-storage-filemedia)
  - [Django](#django)
  - [CI/CD](#cicd)
    - [GitlabCI](#gitlabci)
    - [GitHub Actions](#github-actions)

## Provisioning

Provisioning can be many things in I.T. but here we're talking about provision a server/instance with the
appropriated operating system. Let's be specific, we're talking about creating a server with Debian Stretch,
so you can ssh into it and do the things you want.

I'm going to use a tool called Terraform to create our Debian instance on Digital Ocean and/or Linode.

The steps are so similar for Digital Ocean and Linode, that I could just show you how to do this in only one
of them. Maybe in the future, I'll add an example for AWS too.

> Create a [Digital Ocean](https://m.do.co/c/6c759c705865) account.

OR

> Create a [Linode](https://www.linode.com/?r=f89d7040a73d83627bd6e7490244b280015354d9) account.

**NOTE:** If you find this subject new/complicated/unnecessary for you, just go to your favorite provider
and manually create an instance with Debian Stretch and jump to [Configuration Management](#configuration-management) section.

Basically, we need an instance more or less like this:

- Debian Stretch (You can go with Ubuntu, Alpine, whatever, as long as you know your way around the distro)
- Basic resources like 1GB RAM, 1CPU...
- Open ports:
  - SSH
  - HTTP/HTTPS
  - Docker Remote (2376)
- SSH connection with ssh key (always better than user/password)

### Terraform

> Familiarize yourself with [Terraform](https://www.terraform.io).

If you know the basics of Terraform, you can just go to [provisioning/terraform](provisioning/terraform) and
do your thing.

> [Terraform Providers](https://www.terraform.io/docs/providers/index.html)

> [Some of my Terraform snippets](https://github.com/douglasmiranda/lab/tree/master/terraform)

> [My notes on Terraform](https://gist.github.com/douglasmiranda/ec2baf28d8cb7215d4033de3aad17025)

After you learn Terraform and read the documentation of Digital Ocean provider, you can adapt the file
I provided to fit your plans.

#### Digital Ocean

> [provisioning/terraform/digitalocean](provisioning/terraform/digitalocean)

> [How To Use Terraform with DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-use-terraform-with-digitalocean)

> [Digital Ocean Provider](https://www.terraform.io/docs/providers/do/index.html)

You'll need an API token and the name of your SSH key available in your Digital Ocean dashboard, so you can use the files the way I provided them.

## Configuration Management

In this project we're focusing in a more advanced deployment, so for this step you could use tools to
automate the configuration of your server too. I will provide an Ansible Playbook for you, if you don't
know [Ansible](https://www.ansible.com/) or use another tool for this OR just don't want to mess with those
things right now, here's the list of what we need:

(Basics)
- A Linux server (I'm using Debian Stretch for this project)
- SSH access
- An up-to-date Docker installation.

(Recommended)
- Change root password
- Create a non-root user
- Disallow ssh login with root 
- Disallow ssh login with password (allow only ssh keys)
- Install unattended-upgrades (gotta have those automatic updates xD)
- Install and configure Docker + secure remote connection

### Ansible

I'm assuming you're familiar with Ansible, if not, it's never too late to [learn](https://www.ansible.com/resources/get-started) how to automate things.

I'm providing an Ansible Playbook that will do the config for you, you just need to fill some blanks
(inform server IP, desired passwords..) and as long as you have access to your Debian Stretch server
with ssh keys you will know how to deal with the playbook.

> [Check out the information about the Ansible Playbook for this project.](provisioning/ansible)

## Docker

TODO

### Docker Swarm

TODO

### Secrets

TODO

## Databases

TODO

### Postgres

TODO

### Redis

TODO

## Object Storage (File/Media)

TODO

## Django

TODO

## CI/CD

TODO

### GitlabCI

TODO

### GitHub Actions

TODO
