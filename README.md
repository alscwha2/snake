# Snake
Terminal based implementation of classic snake game.

## Files
* snake - The full script for the game.
* code_sample.py - selected code snippets containing the core functionality of the game, for Broadway round 1 interview.

<img src="https://raw.githubusercontent.com/alscwha2/images/main/manual.gif" alt="snake_gif"/>

## Game modes
### Regular Mode
`snake -r`  
Steer with wasd. Press q any time to exit.  
This mode is a work in progress. Output must be piped into a different terminal, as printing to the calling terminal results in corrupted output.

<img src="https://raw.githubusercontent.com/alscwha2/images/main/regular.gif" alt="snake_gif"/>

### Manual Mode
`snake [-m]`  
Steer with wasd. Press any button to advance one tile in the current direction. Press q at any time to quit.


## Solver
`snake -s`  
### Watch the game play itself
<img src="https://raw.githubusercontent.com/alscwha2/images/main/solver.gif" alt="snake_gif"/>

## Run
For unix-based operating systems
```
curl -o snake https://raw.githubusercontent.com/alscwha2/snake/main/snake
chmod +x snake
./snake -h
```
