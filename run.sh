#!/usr/bin/env bash
#TODO: does not work with multiple files

nix-shell ./cli/default.nix --run "make -C cli run $(pwd)/$@" \
| nix-shell ./graph/default.nix --run "make -C graph run"

STATIC_FILEs=./ui/dist/
