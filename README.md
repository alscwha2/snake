# Snake
Terminal based implementation of classic snake game.

## Files
* Snake - The full script for the game.
* Snake_code_snippets.py - selected code snippets containing the core functionality of the game, for Broadway round 1 interview.

<img src="https://raw.githubusercontent.com/alscwha2/images/main/manual.gif" alt="snake_gif"/>

## Game modes
### Regular Mode
Steer with wasd. Press q any time to exit. This mode is a work in progress, as output is being corrupted due to a bug involving multiple threads piping output to a terminal.
### Manual Mode
Steer with wasd. Press any button to advance one tile in the current direction. Press q at any time to quit.


## Solver
### Watch the game play itself
<img src="https://raw.githubusercontent.com/alscwha2/images/main/solver.gif" alt="snake_gif"/>

## Run
For unix-based operating systems
```
curl -o snake https://github.com/alscwha2/snake/blob/main/snake
chmod +x snake
snake -h
```
