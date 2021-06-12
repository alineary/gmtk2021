# Wild Wagons
#### GMTK 2021, Alina, Bennet, Eric, Robin

## Game Idea
We are creating a small shunting game where you have to add wagons onto waiting trains.
When wagons are attached to favorable wagons, bonus points will be awarded while other combinations are to be avoided.

## Gamedesign
### General
The goal is to get as many points as possible. There is no time limitation the only limitation that exists is the capacity of the incoming track. If the incoming track is overfilled you lose.
### Train creation
To create and send a train there are two types of restriction:
#### Must have
If the need- or blacklist is not fulfilled the train is not able to depart. These conditions are mainly to create a pressure of fast creating trains in order to have as few as possible wagons on the incoming track.
- Needlist: without a certain type of wagon in train or as neighbour the train is not valid
- Blacklist: with a certain type of wagon in train or as neighbour the train is not valid
#### Nice to have
For every part of the nicelist which is fulfilled you get the corresponding amount of points additionally to the 3 points per  departed wagon. For every entry of the badlist which is fulfilled you get a certain amount of minus points. You can not get less than 0 points per train.

## Setup
Clone git repo <br>
Install python 3.9.5 <br>
Install virtualenv: pip install virtualenv <br>
Create venv: virtualenv venv -p python3.9.5 || python -m virtualenv venv -p python3.9.5 <br>
Install requirements: pip install -r requirements.txt <br>

### Activation
MacOS/Linux: source mypython/bin/activate <br>
Windows: venv\Scripts\activate <br>
Now you can install packages in the venv <br>

### Deactivation
deactivate