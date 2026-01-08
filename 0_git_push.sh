#!/bin/bash

git remote -v
git remote remove origin
git remote add origin https://github.com/changbeendata/video-SALMONN-2.git
git branch -M main
git push -u origin main

git config --global user.email "changbeendata@gmail.com"