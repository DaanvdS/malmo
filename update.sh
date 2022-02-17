cd Desktop
git pull
cd Audio

if cmp --silent -- "versionGit" "versionFTP"; then
  echo "No audio update needed"
else
  wget http://daanvanderspek.nl/malmo/Audio/0.wav
  wget http://daanvanderspek.nl/malmo/Audio/1.wav
  wget http://daanvanderspek.nl/malmo/Audio/2.wav
  wget http://daanvanderspek.nl/malmo/Audio/3.wav
  wget http://daanvanderspek.nl/malmo/Audio/4.wav
  wget http://daanvanderspek.nl/malmo/Audio/5.wav
  wget http://daanvanderspek.nl/malmo/Audio/6.wav
  wget http://daanvanderspek.nl/malmo/Audio/7.wav
  wget http://daanvanderspek.nl/malmo/Audio/8.wav
  wget http://daanvanderspek.nl/malmo/Audio/9.wav
  
fi

cd ..