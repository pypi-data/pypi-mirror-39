# Streamlink Helper
Just a small script to pull followed online streams for opening in streamlink. Streamlink is a livestreamer fork, and can be found at https://github.com/streamlink/streamlink

## Installation

### With PIP
Install Python 3 if you don't have it, then run this in command prompt on Windows or the terminal in MacOS or Linux.
```bash
pip install streamlink
pip install streamlink_helper
```

### Manual
Make sure you have Python 3, Git and Streamlink installed, then run this in command prompt on Windows or the terminal in MacOS or Linux.
```bash
git clone https://github.com/cronos23/streamlink_helper
cd streamlink_helper
python setup.py install
```

## Usage

In Command Prompt or PowerShell:
```
streamlink_helper
```
On first run you will be asked for your twitch.tv username. After this, it will be fetched from the configuration file.
