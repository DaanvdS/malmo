cd Desktop
cd malmo
git pull

sudo chmod +x ~/Desktop/malmo/start.sh
sudo cp malmo.desktop /etc/xdg/autostart/malmo.desktop
cd Audio

if cmp --silent -- "versionGit" "versionFTP"; then
  echo "No audio update needed"
else
  curl -O http://daanvanderspek.nl/malmo/Audio/versionFTP
  curl -O http://daanvanderspek.nl/malmo/Audio/0.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/1.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/2.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/3.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/4.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/5.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/6.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/7.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/8.wav
  curl -O http://daanvanderspek.nl/malmo/Audio/9.wav
  
fi

cd ..