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
echo "Running system check..."
printf "Checking for root access... "
if [ "$EUID" -ne 0 ]; then
    printf "${RED_b}Failed${NC}\n"
    printf "Please run as ${RED_b}root${NC}\n"
    exit 1
else
    printf "${GREEN_b}OK${NC}\n"
fi

figlet -v &> /dev/null
if [ $? -eq 0 ]; then
    figlet -w 160 -f smslant "PAKURI-THON"
else
    echo -e "${RED_b}Figlet not installed.${NC}"
    echo -e "${RED_b}Please install figlet.${NC}"
    exit 1
fi
date

printf "Checking docker startup... "
if systemctl status docker.service | grep "active (running)" > /dev/null; then
    printf "${GREEN_b}OK${NC}\n"
    printf "Checking for postgres..."
    if docker-compose -f docker/postgres/docker-compose.yml ps | grep Up > /dev/null; then
        printf "${GREEN_b}OK${NC}\n"
    else
        printf "${RED_b}Failed${NC}\n"
        docker-compose -f docker/postgres/docker-compose.yml start
        echo "Start Postgres. Restat this script."
        exit 1
    fi
    printf "Checking for SSH Service..."
    if systemctl status ssh.service | grep "active (running)" > /dev/null; then
        printf "${GREEN_b}OK${NC}\n"
    else
        printf "${RED_b}Failed${NC}\n"
        systemctl start ssh.service
        echo "Start SSH Servece. Restart this script."
        exit 1
    fi
    printf "Checking for WebSSH..."
    if docker-compose -f docker/webssh/docker-compose.yml ps | grep Up > /dev/null; then
        printf "${GREEN_b}OK${NC}\n"
    else
        printf "${RED_b}Failed${NC}\n"
        docker-compose -f docker/webssh/docker-compose.yml start
        echo "Start WebSSH. Restart this script."
        exit 1
    fi
    printf "Checking for NextCloud..."
    if docker-compose -f docker/NextCloud-Docker/docker-compose.yml ps | grep Up > /dev/null; then
        printf "${GREEN_b}OK${NC}\n"
    else
        printf "${RED_b}Failed${NC}\n"
        docker-compose -f docker/NextCloud-Docker/docker-compose.yml start
        echo "Start NextCloud. Restart this script."
        exit 1
    fi
else
    printf "${RED_b}Failed${NC}\n"
    systemctl start docker.service
    echo "Start Docker. Restart this script."
    exit 1
fi

printf "Booting up PAKURI-THON...  "
if [ -z ${TMUX} ];then
    printf ">"
    sleep 1
    tmux new-session -d -s "pakuri_session" -n "main"
    printf ">"
    sleep 1
    tmux split-window -h -t "pakuri_session:main"
    printf ">"
    sleep 1
    tmux split-window -v -t "pakuri_session:main"
    printf ">"
    sleep 1
    tmux send-keys -t "pakuri_session:main.0" "pipenv shell" C-m
    for ((i=0; i<5; i++)); do
        printf ">"
        sleep 1
    done
    tmux send-keys -t "pakuri_session:main.0" "python app.py" C-m
    printf ">"
    sleep 1
    tmux send-keys -t "pakuri_session:main.1" "pipenv shell" C-m
    for ((i=0; i<5; i++)); do
        printf ">"
        sleep 1
    done
    tmux send-keys -t "pakuri_session:main.1" "python watchDog.py" C-m
    printf ">"
    sleep 1
    tmux send-keys -t "pakuri_session:main.2" "powershell-empire server --username empireadmin --password password123" C-m
    printf "> ${GREEN_b}done!${NC}\n"
    sleep 1
    tmux -2 attach-session -t "pakuri_session".2
else
    printf "Already running!"
    sleep 1
    tmux -2 attach-session -t "pakuri_session".0
fi