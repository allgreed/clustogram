#!/usr/bin/env bash

#TODO: does not work with multiple files
DATA_ENTRYPOINT=${1:-'multi.example.yaml'}

nix-shell ./ui/default.nix --run "make -C ui build"
nix-shell ./cli/default.nix --run "python cli/main.py $DATA_ENTRYPOINT" | UI_STATIC_CONTENT=$(pwd)/ui/dist/ nix-shell ./graph/default.nix --run "python graph/src/main.py"
