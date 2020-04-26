#! /bin/bash

cd website
dir=`pwd`
echo "Building $dir..."
yarn build
cd ..
echo "Starting Server..."
python3 server.py
