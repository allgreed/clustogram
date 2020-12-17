#!/usr/bin/env bash

#TODO: does not work with multiple files
DATA_ENTRYPOINT=${1:-'single.example.yaml'}

nix-shell ./cli/default.nix --run "make -C cli run $(pwd)/$DATA_ENTRYPOINT" \
| UI_STATIC_CONTENT=$(pwd)/ui/dist/ nix-shell ./graph/default.nix --run "make -C graph run"

