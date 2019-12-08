#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd $SCRIPT_DIR

# Directories
OVERLEAF_REPO_DIR="../../5da6386eba84b9000140b096"
PLOTS_OUTPUT_DIR="./output"
FIGS_OUTPUT_DIR="./figures"

# Filess
plots=( "cs-2-stages.pdf" "cs-2-cats.pdf" "cs-2-cats-bars.pdf" \
        "cs-3-stages.pdf" "cs-3-cats.pdf" "cs-3-cats-bars.pdf" \ 
        "us-stack-bar.pdf")

figs=("prog-accelerator.pdf" \
        "system-stack-a.pdf" \
        "system-stack-b.pdf" \
        "util-framework.pdf" \
        "util-stages.pdf" \
        "util-vs-effort.pdf" \
        "util-overview.pdf" \
        "lenet.pdf" \
        "stride.pdf" \
        "accel.pdf")

# Use following command to save git username and password
# git config credential.helper store
# git pull

set -x
pushd $OVERLEAF_REPO_DIR
    git pull
popd

for file in "${plots[@]}"
do
    cp "${PLOTS_OUTPUT_DIR}/${file}" "${OVERLEAF_REPO_DIR}/plots/"
done

for file in "${figs[@]}"
do
    cp "${FIGS_OUTPUT_DIR}/${file}" "${OVERLEAF_REPO_DIR}/figs/"
done

cp "${PLOTS_OUTPUT_DIR}/util-table.tex" "${OVERLEAF_REPO_DIR}/sections/"

pushd $OVERLEAF_REPO_DIR
    for file in "${plots[@]}"
    do
        git add "plots/${file}"
    done

    for file in "${figs[@]}"
    do
        git add "figs/${file}"
    done

    git add "sections/util-table.tex"

    git commit -m "send-to-overleaf.sh $(date "+%Y.%m.%d-%H.%M.%S")"
    git push
popd

echo -en "\007"
