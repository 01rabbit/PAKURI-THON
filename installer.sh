#!/bin/bash

NC='\e[0m'
BOLD='\e[1m'
BLACK_b='\e[1;30m'
RED_b='\e[1;31m'
GREEN_b='\e[1;32m'
YELLOW_b='\e[1;33m'
BLUE_b='\e[1;34m'
PURPLE_b='\e[1;35m'
LIGHTBLUE_b='\e[1;36m'

IFACE="eth0"
IP_ADDRESS=$(/sbin/ip -f inet -o addr show "$IFACE" | cut -d\  -f 7 | cut -d/ -f 1)

clear
echo "Step 1/10 Running system check..."
printf "Checking for root access... "
if [ "$EUID" -ne 0 ]; then
    printf "${RED_b}Failed${NC}\n"
    printf "Please run as ${RED_b}root${NC}\n"
    exit 1
else
    printf "${GREEN_b}OK${NC}\n"
fi

printf "Step 2/10 : Checking for internet connection... "
if ping -q -c 1 -W 1 google.com >/dev/null; then
    printf "${GREEN_b}OK${NC}\n"
else
    printf "${RED_b}Failed${NC}\n"
    printf "Please check your internet connection.\n"
    exit 1
fi

figlet -v &> /dev/null
if [ $? -eq 0 ]; then
    figlet -w 160 -f smslant "PAKURI-THON"
    echo -e "${Green_b}"
    figlet -w 160 -f smslant "Installer"
    echo -e "${NC}\n"
else
    echo -e "${RED_b}Figlet was not installed.${NC}"
    echo -e "${RED_b}Install figlet.${NC}"
    apt update && apt install figlet -y
    echo "Installed figlet. Please run this script again."
    exit 1
fi
date
echo "Step 3/10 : Creating service.ini..."
cat <<EOF > service.ini
[postgresql]
user = rot
password = password
host = localhost
port = 15432
database = pakuri
[nextcloud]
server = http://$IP_ADDRESS:8080
EOF
echo "Step 4/10 : Nextcloud login information..."
echo "Enter the name(ID) and password(at least 8 characters, uppercase and lowercase letters, symbols, and numbers) of chatbot you want to use."
read -p "Name(ID): " NAME
read -sp "Password: " PASSWORD
echo ""
cat <<EOF >> service.ini
username = $NAME
password = $PASSWORD
inforoom = Information
[webssh]
EOF
echo "Step 5/10 : SSH login information..."
echo "Enter the username and password for ssh login."
read -p "USERNAME: " USERNAME
read -sp "PASSWORD: " PASSWORD
ENCPASS=`echo -n $PASSWORD|base64`
echo ""
cat <<EOF >> service.ini
username = $USERNAME
password = $ENCPASS
[empire]
username = empireadmin
password = password123
server = https://$IP_ADDRESS:1337
listener = pakuri
port = 8088
EOF

printf "Step 6/10 : Checking that Docker is installed... "
docker --version &> /dev/null
if [ $? -eq 0 ]; then
    printf "${GREEN_b}OK${NC}\n"
else
    printf "${RED_b}Failed${NC}\n"
    printf "Install Docker.\n"
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
    echo 'deb [arch=amd64] https://download.docker.com/linux/debian buster stable' > /etc/apt/sources.list.d/docker.list
    apt update && apt install docker-ce -y
    apt install docker-compose -y
    systemctl start docker
    systemctl enable docker
fi

echo "Step 7/10 : Docker content is being installed..."
cd docker
printf "WebSSH... "
docker-compose -f webssh/docker-compose.yml ps &> /dev/null
if [ $? -eq 0 ]; then
    cd webssh
    docker-compose up -d
    printf "${GREEN_b}OK${NC}\n"
else
    git clone https://github.com/huashengdun/webssh.git webssh
    cd webssh
    docker-compose up -d
    printf "${GREEN_b}Installed${NC}\n"
fi
cd ..

printf "Step 8/10 : Nextcloud... "
cd NextCloud-Docker
docker-compose up -d
printf "${GREEN_b}OK${NC}\n"
cd ..

printf "Step 9/10 : PostgreSQL... "
cd postgres
docker-compose up -d
printf "${GREEN_b}OK${NC}\n"
cd ../../..

printf "Step 10/10 : Set up the environment..."
apt install libpq-dev pipenv -y
pipenv sync
printf "${GREEN_b}OK${NC}\n"

echo "Instll complete!"
echo "Please accsess http://$IP_ADDRESS:8080 with a web browser to complete the Nextcloud configuration."
printf "When you are finished, type ${RED_b}sudo ./pkr3.sh${NC} to start PAKURI-THON.\n"