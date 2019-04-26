# Ansible Playbook for this project

> https://docs.docker.com/engine/security/https/

> [Provisioning a Digital Ocean Droplet for remote Docker access](https://github.com/douglasmiranda/lab/blob/master/terraform/digital-ocean-droplet-remote-docker-example.tf)

> [My Notes on Ansible for Configuration Management](https://gist.github.com/douglasmiranda/f21a4481d372ae54fcf4a6ff32249949)

For configuration management, I'm using [Ansible](https://www.ansible.com/).

This tool can ssh into your newly created server instance, install and configure the packages you desire. Of course, it can do much more and this is just a simplification.

- [Ansible Use Cases](https://www.ansible.com/use-cases)
- [Learn Ansible](https://www.ansible.com/resources/get-started)
- [Ansible Documentation](https://docs.ansible.com)

And yes, Ansible can provision infrastructure as well.

## What this Ansible Playbook does?

- Change root password
- Create a non-root user
- Disallow ssh login with root 
- Disallow ssh login with password (allow only ssh keys)
- Install unattended-upgrades (gotta have those automatic updates xD)
- Install and configure Docker + secure remote connection

If you prefer to use `ufw` as a firewall:

> https://github.com/douglasmiranda/lab/blob/master/ansible/ufw-basics.yml

> https://github.com/douglasmiranda/lab/blob/master/ansible/docker/ufw-rules-for-docker.yml

## Basics

Note: We're securing our secrets with Ansible Vault, I'm just using encrypted strings, you can do the way you want.

So the secrets are in group_vars/all.yml

https://docs.ansible.com/ansible/latest/cli/ansible-vault.html

---

First, you need to provide your information:

- site.yml
- hosts.yml
- group_vars/all.yml

Initial setup with root password (we'll execute tasks with initial-setup tag; basic deploy user creation)

First command will only create our deploy user and making sure we can log in with our ssh-key as the new user.

```bash
ansible-playbook site.yml -i hosts.yml --ask-vault-pass -e ansible_user=root --tags=initial-setup
```

Now, log in as the deploy user and configure our host. We're going to run tasks labeled as `initial-setup` because we only do those things with root in the previous step.

```bash
ansible-playbook site.yml -i hosts.yml --skip-tags=initial-setup --ask-vault-pass
```

Or use our Makefile:

```bash
make ansible-initial-setup-as-root

# And

make ansible-setup-as-deploy-user
```
