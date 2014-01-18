#!/bin/bash
# Quick script to add documentation to gh pages

pushd .

# Change to the script directory
cd "$( dirname "${BASH_SOURCE[0]}" )"

# Add al fils to git, commit and push
# Useful commits are not needed since
# this is a documentation branch
git add *
git commit -a -m "Documentation update"
git push origin gh-pages

popd