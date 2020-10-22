[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# FlappyBird training Environment

### Description
This repository uses a custom built OpenAI gym environment for a FlappyBird game rendered using pygames to implement Behaviour Cloning.

### Repository structure
```
├── flappyGym
│   ├── envs
│   │   ├── assets
│   │   │   ├── audio
│   │   │   └── sprites
│   │   ├── complete.py
│   │   ├── constants.py
│   │   ├── data
│   │   │   └── 0_718DBFFEC2D40E1D.npy
│   │   ├── flappy.ico
│   │   ├── Flappy.py
│   │   ├── __init__.py
│   │   ├── recorder.py
│   │   ├── test.py
│   │   └── utility.py
│   ├── __init__.py
|
├── flappyGym.egg-info
│   ├── dependency_links.txt
│   ├── PKG-INFO
│   ├── requires.txt
│   ├── SOURCES.txt
│   └── top_level.txt
├── README.md
└── setup.py
```
To install the dependencies and the environment run `pip install -e .`

To start recording run `python recorder.py`
Use spacebar to start the game and UP_KEY to play the game
Once you've finished recording press `Esc` to save the data to the folder specified. 
Run the model `python complete.py ./data/`. It should learn from data and work instantly. 

### Disclaimer
This work is highly based on the following repositories:

    [sourabhv/FlapPyBird] (https://github.com/sourabhv/FlapPyBird)
    [Shivanshmundra/reinforcement_learning_beginner] (https://github.com/Shivanshmundra/reinforcement_learning_beginner)    


