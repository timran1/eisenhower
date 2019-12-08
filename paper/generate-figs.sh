#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -x

cd $SCRIPT_DIR

# Directories
FIGS_DIR="./figures"
pushd $FIGS_DIR

FIGS_OUTPUT_DIR="./output"

figs=($(find ./ -name "*.svg"))
for file in "${figs[@]}"
do
    f="$(basename -s .svg -- $file)"
    inkscape --export-use-hints --export-pdf-version="1.4"  --export-area-drawing --export-pdf="${FIGS_OUTPUT_DIR}/$f.pdf" $file #2>/dev/null
done

popd