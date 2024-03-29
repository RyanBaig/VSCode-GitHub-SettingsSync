#!/bin/bash

abs_path="$( cd "$(dirname "$0")" ; pwd -P )/main.py"


python3 $abs_path $@