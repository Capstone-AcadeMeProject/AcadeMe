# -*- mode: ruby -*-
# vi: set ft=ruby :

# This Vagrantfile can be used with VirtualBox or Docker as a provider
# VirtualBox will be the default. To use Docker type:
#
#     vagrant up --provider=docker
#
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  # config.vm.box_version = "20200206.0.0"
  config.vm.hostname = "ubuntu"

  config.vm.network "forwarded_port", guest: 3000, host: 3000, host_ip: "127.0.0.1"
  # reference: https://www.virtualbox.org/manual/ch06.html#network_hostonly
  # config.vm.network "private_network", ip: "192.168.56.0"

  ############################################################
  # Provider for VirtualBox
  ############################################################
  config.vm.provider :virtualbox do |vb|
   vb.memory = "512"
   vb.cpus = 1
   #vb.gui = true

  #   Fixes some DNS issues on some networks
  # vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
  # vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end

  ############################################################
  # Provider for Docker
  ############################################################
  config.vm.provider :docker do |docker, override|
    override.vm.box = nil
    docker.image = "rofrano/vagrant-provider:debian"
    docker.remains_running = true
    docker.has_ssh = true
    docker.privileged = true
    docker.volumes = ["/sys/fs/cgroup:/sys/fs/cgroup:rw"]
    # Uncomment to force arm64 for testing images on Intel
    docker.create_args = ["--platform=linux/arm64"] 
    docker.create_args = ["--cgroupns=host"] 
  end

  ############################################################
  # Copy some host files to configure VM like the host
  ############################################################

  # Copy your .gitconfig file so that your git credentials are correct
  if File.exists?(File.expand_path("~/.gitconfig"))
    config.vm.provision "file", source: "~/.gitconfig", destination: "~/.gitconfig"
  end

  # Copy your ssh keys for github so that your git credentials work
  if File.exists?(File.expand_path("~/.ssh/id_rsa"))
    config.vm.provision "file", source: "~/.ssh/id_rsa", destination: "~/.ssh/id_rsa"
  end
  if File.exists?(File.expand_path("~/.ssh/id_rsa.pub"))
    config.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "~/.ssh/id_rsa.pub"
  end

  # Copy your .vimrc file so that your VI editor looks nice
  if File.exists?(File.expand_path("~/.vimrc"))
    config.vm.provision "file", source: "~/.vimrc", destination: "~/.vimrc"
  end

  ############################################################
  # Create a Python 3 environment for development work
  ############################################################
  config.vm.provision "shell", inline: <<-SHELL
    # Update and install
    apt-get update
    apt-get install -y vim git tree python3-dev python3-pip python3-venv apt-transport-https
    apt-get upgrade python3
    apt-get -y autoremove
    # Create a Python3 Virtual Environment and Activate it in .profile
    sudo -H -u vagrant sh -c 'python3 -m venv ~/venv'
    sudo -H -u vagrant sh -c 'echo ". ~/venv/bin/activate" >> ~/.profile'
    
    # Install app dependencies in virtual environment as vagrant user
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && pip install -U pip && pip install wheel'
    sudo -H -u vagrant sh -c '. ~/venv/bin/activate && cd /vagrant && pip install -r requirements.txt'    
  SHELL

  ######################################################################
  # Add Postgres database as a docker container
  ######################################################################
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install -y apache2
    rm -rf /var/www/html
    #create symbolic link for home page
    ln -s /vagrant/templates /var/www/html
    
    # Prepare postgres data share
    sudo mkdir -p /var/lib/postgresql/data
    sudo chown vagrant:vagrant /var/lib/postgresql/data
  SHELL

  # Add Redis docker container
  config.vm.provision "docker" do |d|
    d.pull_images "postgres:alpine"
    # d.ports = ["5432:5432"]
    d.run "postgres:alpine",
      # args: "--restart=always -d --name redis -h redis -p 6379:6379 -v /var/lib/redis/data:/data"
      # args: "-d --name postgres -p 5432:5432 -v /var/lib/postgres/data"
      # args: "-d --name postgres -h localhost -p 5432:5432 -v psql_data:/var/lib/postgres/data postgres"
      args: "--restart=always -d --name postgres -p 5432:5432 -v /var/lib/postgresql/data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres"
  end
end
