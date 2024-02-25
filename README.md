# Tortoise Tools
This is a collection of scripts/tools that I use for Tortoise.  The names of the folders describe what the files scripts inside of them should be doing.

# Prerequisites for these tools
- git
- python (recommend 3.10 or 3.11)

# Installation
1. Create and activate venv to isolate packages from global python installation
```
python -m venv venv
.\venv\Scripts\activate
```
2. Install [pytorch](https://pytorch.org/get-started/locally/) or go to the link to find the latest:
```pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118```
3. Install [whisperx](https://github.com/m-bain/whisperX) with the command below: 
```pip install git+https://github.com/m-bain/whisperx.git```
4. Install requirements:
```pip install -r requirements.txt```