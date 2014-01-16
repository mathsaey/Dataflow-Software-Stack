#!/bin/bash

# Quick script to add documentation to gh pages

git add *
git commit -a -m "Documentation update"
git push origin gh-pages