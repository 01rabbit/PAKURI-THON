#!/bin/bash

if [ -z ${TMUX} ];then
    tmux new-session -d -s "test_session" -n "test_window"
    tmux split-window -h -t "test_session:test_window"
    tmux split-window -v -t "test_session:test_window"
    tmux send-keys -t "test_session:test_window.0" "pipenv shell" C-m
    sleep 2
    tmux send-keys -t "test_session:test_window.0" "python app.py" C-m
    sleep 1
    tmux send-keys -t "test_session:test_window.1" "pipenv shell" C-m
    sleep 2
    tmux send-keys -t "test_session:test_window.1" "python watchDog.py" C-m
    sleep 1
    tmux -2 attach-session -t "test_session".2
else
    tmux attach-session -t "test_session"
fi