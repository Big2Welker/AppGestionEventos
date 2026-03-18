# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  if Vagrant.has_plugin? "vagrant-vbguest"
    config.vbguest.no_install = true
    config.vbguest.auto_update = false
    config.vbguest.no_remote = true
  end

  # =========================
  # SERVIDOR WEB (NGINX + FRONTEND)
  # =========================
  config.vm.define :web do |web|
    web.vm.box = "bento/ubuntu-22.04"
    web.vm.hostname = "web"
    web.vm.network :private_network, ip: "192.168.100.10"

    web.vm.provider "virtualbox" do |vb|
      vb.name = "vm-web"
      vb.memory = 1024
      vb.cpus = 1
    end
  end

  # =========================
  # SERVIDOR APP (FASTAPI)
  # =========================
  config.vm.define :app do |app|
    app.vm.box = "bento/ubuntu-22.04"
    app.vm.hostname = "app"
    app.vm.network :private_network, ip: "192.168.100.11"

    app.vm.provider "virtualbox" do |vb|
      vb.name = "vm-app"
      vb.memory = 1536
      vb.cpus = 1
    end
  end

end