# Simple audio splitter

Simple audio splitter GUI made with PySimpleGUI using hadcoded ffmpeg commands.

## Usage

Remember to install [**ffmpeg**](https://www.ffmpeg.org/) and [**python3-tk**](https://docs.python.org/3/library/tkinter.html) before running the binary:

```sh
sudo apt install ffmpeg python3-tk
```

Then download and run the the binary as usual:

```sh
wget https://github.com/b-Tomas/simple-audio-splitter/releases/download/v0.1.0/audio-splitter
./audio-splitter
```

## Run from source

Make sure system dependencies are met (see above) and then:

```sh
# Clone the repo
git clone https://github.com/b-Tomas/simple-audio-splitter
# Create a virtual environment (make sure you are using Python3)
virtualenv .venv
. .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run
python main.py
```

## Build executable

```sh
. .venv/bin/activate
pip install pyinstaller
pyinstaller audio-splitter.spec
```
