sudo systemctl disable hostapd dnsmasq
sudo cp /etc/dhcpcd.disable.conf /etc/dhcpcd.conf
sudo cp /etc/rc.disableAP.local /etc/rc.local
sudo reboot
