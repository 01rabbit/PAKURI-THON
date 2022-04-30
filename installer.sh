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

clear
figlet -v &> /dev/null
if [ $? -eq 0 ]; then
    printf "${RED_b}"
    figlet -w 160 -f smslant "PAKURI-THON"
    printf "${GREEN_b}"
    figlet -w 160 -f smslant "Installer"
    printf  "${NC}\n"
else
    printf "${RED_b}Figlet was not installed.${NC}\n"
    printf "${RED_b}Install figlet.${NC}\n"
    apt update && apt install figlet -y
    echo "Installed figlet. Please run this script again."
    exit 1
fi
date
printf "Step 1 : Checking for root access... "
if [ "$EUID" -ne 0 ]; then
    printf "${RED_b}Failed${NC}\n"
    printf "Please run as ${RED_b}root${NC}\n"
    exit 1
else
    printf "${GREEN_b}OK${NC}\n"
fi

printf "Step 2 : Checking for internet connection... "
if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    printf "${GREEN_b}OK${NC}\n"
else
    printf "${RED_b}Failed${NC}\n"
    printf "Please check your internet connection.\n"
    exit 1
fi
echo ""
echo "Step 3 : Creating service.ini..."
echo "Step 3-1 : Enter the IP address of your server:"
read -p "IPAddress: " IP
echo ""
cat <<EOF > service.ini
[postgresql]
user = root
password = password
host = localhost
port = 15432
database = pakuri
[webssh]
EOF
echo ""
echo "Step 3-2 : SSH login information..."
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
server = https://$IP:1337
listener = pakuri
port = 8088
[mattermost]
webhooks = http://$IP:8065/hooks/[Create webhooks token]
EOF

printf "Step 4 : Checking that Docker is installed... "
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

echo "Step 5 : Docker content is being installed..."
cd docker
printf "Step 5-1 : WebSSH... "
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

printf "Step 5-2 : Mattermost... "
docker-compose -f mattermost-docker/docker-compose.yml ps &> /dev/null
if [ $? -eq 0 ]; then
    cd mattermost-docker
    docker-compose up -d
    printf "${GREEN_b}OK${NC}\n"
else
    git clone https://github.com/mattermost/mattermost-docker.git
    cd mattermost-docker
    mkdir -pv ./volumes/app/mattermost/{data,logs,config,plugins,client-plugins}
    chown -R 2000:2000 ./volumes/app/mattermost/
    cat <<EOF > ./docker-compose.yml
version: "3"

services:

  db:
    build: db
    read_only: true
    restart: unless-stopped
    volumes:
      - ./volumes/db/var/lib/postgresql/data:/var/lib/postgresql/data
      - /etc/localtime:/etc/localtime:ro
    environment:
      - POSTGRES_USER=mmuser
      - POSTGRES_PASSWORD=mmuser_password
      - POSTGRES_DB=mattermost

  app:
    build:
      context: app
      args:
        - edition=team
    restart: unless-stopped
    volumes:
      - ./volumes/app/mattermost/config:/mattermost/config:rw
      - ./volumes/app/mattermost/data:/mattermost/data:rw
      - ./volumes/app/mattermost/logs:/mattermost/logs:rw
      - ./volumes/app/mattermost/plugins:/mattermost/plugins:rw
      - ./volumes/app/mattermost/client-plugins:/mattermost/client/plugins:rw
      - /etc/localtime:/etc/localtime:ro
    environment:
      - MM_USERNAME=mmuser
      - MM_PASSWORD=mmuser_password
      - MM_DBNAME=mattermost

      - MM_SQLSETTINGS_DATASOURCE=postgres://mmuser:mmuser_password@db:5432/mattermost?sslmode=disable&connect_timeout=10


  web:
    build: web
    ports:
      - "8065:8080"
      - "443:8443"
    read_only: true
    restart: unless-stopped
    volumes:
      - ./volumes/web/cert:/cert:ro
      - /etc/localtime:/etc/localtime:ro
    cap_drop:
      - ALL
EOF
    docker-compose up -d
    printf "${GREEN_b}Installed${NC}\n"
fi

printf "Step 5-3 : PostgreSQL... "
cd postgres
docker-compose up -d
printf "${GREEN_b}OK${NC}\n"
cd ../../

printf "Step 6 : Set up the environment..."
apt install pipenv -y
apt install libpq-dev -y
pipenv sync
printf "${GREEN_b}OK${NC}\n"

echo "Instll complete!"

echo "Complete the Mattermost setup by visiting http://$IP:8065 in your web browser.\n\
After registering an administrator, create a Bot account, Incoming Webhooks, and Outgoing Webhooks."
printf "When you are finished, type ${RED_b}sudo ./pkr3.sh${NC} to start PAKURI-THON.\n"
