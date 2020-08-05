# Description des opérations sur Raspberry pi
## Installation du système Raspberry pi OS :
### Installation de rasp-ap:

### Installation de mosquitto :

### Installation des outils python :
-  Installation de panda

###  Configuration du system pour l'utilisation de scanners usb :
 - Créer un groupe "scanners" :
  - Avec la commande : sudo groupadd scanners
- Donner les droits d'utilisation des evenements /dev/input/event*
  - Editer /etc/udev/rules.d/99-scanners.rules
  - Ajouter KERNEL =="event*", name="input%k",MODE="660",GROUP="scanners"
  - Ajouter l'utilisateur par defaut au groupe "scanners": usermod -a -G scanners pi

## mise en route du service scanner.service
execute le script scanner.py sous forme de service.

copie de scanner.service dans /lib/systemd/system/
sudo systemctl enable scanner.service
sudo systemctl start scanner.service
## mise en route du service sequenceur.service 
