import qrcode
import hashlib

def create_qrcode(message,filename):
    img =qrcode.make(message)
    img.save(filename)

cmd = "nmap -sn 127.0.0.1 -oA tmp/Ping_scan_127.0.0.1_20220623153338"
hs = hashlib.md5(cmd.encode()).hexdigest()
filename = f"static/images/qrcode/{hs}.png"
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
    figlet -w 160 -f smslant "PAKURI-THON"
else
    echo -e "${RED_b}Figlet not installed.${NC}"
    echo -e "${RED_b}Please install figlet.${NC}"
    exit 1
fi

date



printf "Booting up PAKURI-THON...  "
if [ -z ${TMUX} ];then
    printf ">"
    sleep 1
    tmux new-session -d -s "pakuri_session" -n "main"
    tmux send-keys -t "pakuri_session:main.1" "python watchDog.py" C-m
    printf ">"
    sleep 1
    #wssh
    tmux new-window -n "webssh"
    tmux send-keys -t "webssh" "wssh" C-m
    tmux select-window -t "main"
    # iniファイルの読み込み
    declare -r INI_FILE="config.ini"
    # sectionの指定
    tmux -2 attach-session -t "pakuri_session".0
else
    printf "Already running!"
    sleep 1
    tmux -2 attach-session -t "pakuri_session".0
fi