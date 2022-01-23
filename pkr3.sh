#!/bin/bash

if [ -z ${TMUX} ];then
    tmux new-session -d -s "pakuri_session" -n "mein"
    tmux split-window -h -t "pakuri_session:mein"
    tmux split-window -v -t "pakuri_session:mein"
    tmux send-keys -t "pakuri_session:mein.0" "pipenv shell" C-m
    sleep 2
    tmux send-keys -t "pakuri_session:mein.0" "python app.py" C-m
    sleep 1
    tmux send-keys -t "pakuri_session:mein.1" "pipenv shell" C-m
    sleep 2
    tmux send-keys -t "pakuri_session:mein.1" "python watchDog.py" C-m
    sleep 1
    tmux -2 attach-session -t "pakuri_session".2
else
    tmux attach-session -t "pakuri_session"
fi