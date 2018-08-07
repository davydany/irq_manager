# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

  config.vm.box = "bento/centos-7.5"

  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"

  config.vm.synced_folder ".", "/irq_manager"

  config.vm.provider "virtualbox" do |vb|
    # Customize the amount of memory and cpus
    vb.memory = "2048"
    vb.cpus = 4
  end
  config.vm.provision "file", source: "./vm/files/mongodb-org-3.2.repo", destination: "/tmp/mongodb-org-3.2.repo"

  config.vm.provision "shell", inline: <<-SHELL
    yum install -y epel-release
    yum install -y python34 python34-pip vim

    # install mongodb
    mv /tmp/mongodb-org-3.2.repo /etc/yum.repos.d/mongodb-org-3.2.repo
    yum repolist
    yum -y install mongodb-org
    systemctl start mongod

    # setup python
    pip3 install virtualenv
    pip3 install ipython
    python3 -m virtualenv /irq_manager/venv
    /irq_manager/venv/bin/pip install -r /irq_manager/requirements_dev.txt
    /irq_manager/venv/bin/pip install -e /irq_manager
    ln -s /irq_manager /home/vagrant/irq_manager
  SHELL
end
