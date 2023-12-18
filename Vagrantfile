Vagrant.configure("2") do |config|
  config.vm.box = "borim/code2block-test-vm"
  config.vm.provision :shell, path: "provisioning/provisioning_script.sh"
  config.vm.network :forwarded_port, guest: 80, host: 8080
end
