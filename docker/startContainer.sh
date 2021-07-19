#!/bin/bash

echo "Starting container..."

if [[ -n $DISCORD_TOKEN_FILE ]]; then
    echo "Loading discord token secret..."
    export DISCORD_TOKEN=$(grep -v '^#' $DISCORD_TOKEN_FILE | xargs)

fi;


if [[ -n $SAUCENAO_KEY_FILE ]]; then
    echo "Loading saucenao key secret..."
    export SAUCENAO_KEY=$(grep -v '^#' $SAUCENAO_KEY_FILE | xargs)

fi;

if [[ -n $YT_KEY_FILE ]]; then
    echo "Loading youtube key secret..."
    export YT_KEY=$(grep -v '^#' $YT_KEY_FILE | xargs)

fi;

if [[ -n $SPOTIFY_ID_FILE ]]; then
    echo "Loading spotify id secret..."
    export SPOTIFY_ID=$(grep -v '^#' $SPOTIFY_ID_FILE | xargs)

fi;

if [[ -n $SPOTIFY_SECRET_FILE ]]; then
    echo "Loading spotify secret..."
    export SPOTIFY_SECRET=$(grep -v '^#' $SPOTIFY_SECRET_FILE | xargs)

fi;

./sources/main.py
