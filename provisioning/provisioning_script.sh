sudo apt-get install -y python3-venv nginx
cd /vagrant
#python3 -m venv venv
#source /vagrant/venv/bin/activate
pip install sansio-lsp-client flask python-lsp-server "python-lsp-server[all]" gunicorn
cp /vagrant/provisioning/code2block.service /etc/systemd/system
sudo systemctl enable code2block
sudo systemctl start code2block
sudo systemctl status code2block

rm /etc/nginx/sites-available/*
rm /etc/nginx/sites-enabled/*
cp /vagrant/provisioning/code2block-nginx /etc/nginx/sites-available
ln -s /etc/nginx/sites-available/code2block-nginx /etc/nginx/sites-enabled/code2block-nginx
sudo systemctl enable nginx
sudo systemctl start nginx
sudo systemctl status nginx

sudo systemctl restart code2block
sudo systemctl restart nginx
