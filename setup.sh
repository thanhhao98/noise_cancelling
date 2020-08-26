#!/bin/bash
export FLASK_APP=main.py
export FLASK_ENV=development

if [ ! -d "venv" ]; then
    echo "Setup environment"
    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install pip --upgrade
    python3 -m pip install -r requirements.txt
fi
if [ -f "venv/bin/activate" ]; then
    echo "Loading Python vitualenvl from folder venv"
    source venv/bin/activate
    python3 -m pip install pip --upgrade
else
    echo "Folder venv is error, please check it!"
fi

if [ ! -d "imgtxtenh" ]; then
    echo "Clone imgtxtenh repository"
    git clone https://github.com/mauvilsa/imgtxtenh.git
    cd imgtxtenh
    echo "Build imgtxtenh"
    cmake -DCMAKE_BUILD_TYPE=Release .
    make
    cd ..
else
    if [ ! -f "imgtxtenh/imgtxtenh" ]; then
        echo "Build imgtxtenh"
        cd imgtxtenh
        cmake -DCMAKE_BUILD_TYPE=Release .
        make
        cd ..
    fi
fi

if [ ! -d "pdf" ]; then
    echo "Make folder contain pdf"
    mkdir pdf
fi

if [ ! -d "image" ]; then
    echo "Make folder contain image"
    mkdir image
fi

if [ ! -d "static" ]; then
    echo "Make folder contain static"
    mkdir static
fi
