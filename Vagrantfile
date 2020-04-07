# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.ssh.insert_key = false
  #config.ssh.private_key_path = 'D:\mininet\.vagrant.d\insecure_private_key'
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.define "sender" do |r2_config|
    r2_config.vm.box = "comnets/mininet"
    r2_config.vm.network "private_network", ip: "192.168.1.102", :netmask => "255.255.255.0"
    r2_config.vm.hostname = "sender"
    r2_config.hostmanager.aliases = "sender"
    r2_config.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "sender"]
      v.customize ["modifyvm", :id, "--memory", 1024.to_s]
      v.customize ["modifyvm", :id, "--cpus", 1.to_s]
    end
  end

  config.vm.define "receiver" do |r3_config|
    r3_config.vm.box = "comnets/mininet"
    r3_config.vm.network "private_network", ip: "192.168.1.103", :netmask => "255.255.255.0"
    r3_config.vm.hostname = "receiver"
    r3_config.hostmanager.aliases = "receiver"
    r3_config.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "receiver"]
      v.customize ["modifyvm", :id, "--memory", 1024.to_s]
      v.customize ["modifyvm", :id, "--cpus", 1.to_s]
    end
  end

  config.vm.define 'tactics' do |tactics_config|
    tactics_config.vm.box = "comnets/mininet"
    tactics_config.vm.network "private_network", ip: "192.168.1.99", :netmask => "255.255.255.0"
    tactics_config.vm.hostname = "tactics"
    tactics_config.hostmanager.aliases = "tactics"
    tactics_config.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "tactics"]
      v.customize ["modifyvm", :id, "--memory", 1024.to_s]
      v.customize ["modifyvm", :id, "--cpus", 1.to_s]
    end

    #tactics_config.vm.provision :ansible_local do |ansible|
    #  ansible.playbook       = "virtual_setup.yml"
    #  ansible.verbose        = true
    #  ansible.install        = true
    #  ansible.become         = true
    #  ansible.limit          = "all" # or only "nodes" group, etc.
    #  ansible.provisioning_path = "/vagrant/NodePreparation"
    #  ansible.inventory_path = "/vagrant/NodePreparation/hosts"
    #end
  end

  vagrant_synced_folder_default_type = ""

end
