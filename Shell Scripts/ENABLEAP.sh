sudo systemctl enable hostapd dnsmasq
sudo cp /etc/dhcpcd.enable.conf /etc/dhcpcd.conf
sudo cp /etc/rc.enableAP.local /etc/rc.local
sudo reboot
