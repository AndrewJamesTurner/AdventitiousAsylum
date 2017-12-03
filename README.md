# Adventitious Asylum

Platformer with battles - in an asylum!

## Installation

This game uses **Python3**, **we highly recommend using a virtual environment with Python3 as the interpreter**. 
If you are having problems installing the game, check that you aren't trying to use Python 2.x; try replacing 
`python` and `pip` with `python3` and `pip3`.

* Install python dependencies:
    * `pip install -r requirements.txt`

## Running the game

Simply run the `game.py` module.

* `python game.py`

Playing the game:

* In the platform game:
    * Left + Right keys to move left + right
    * Space to jump
    * Hold shift + press up key to climb surfaces that are climbable
    * Down key to jump down from surfaces

* In the battle game:
    * Space bar or Return key to select an attack

## Making new levels

Run the level editor

* `python LevelEditorScene.py`

Notes on using the level editor:

* Zoom in and out using the mouse wheel
* Pan using the arrow keys
* Can't add new patterns using the level editor (or change existing patterns)
    * Add / modify patterns by manually editing `patterns.json`
* The level editor doesn't load surf data into the boxes
* To see surf data, press the `d` key to render surf data over the images
    * Green = block
    * Blue = stand on
    * Lilac = ladder
    * Red = damage
