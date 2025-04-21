# Endless Runner Game

A simple, browser-based endless runner game built with Python and HTML5 Canvas.

## Game Description

Control a character that automatically moves forward while jumping over randomly generated obstacles. The game features:

- Progressive difficulty system
- Multiple obstacle types
- Color-changing character
- Score tracking
- Smooth controls

## Features

- **Dynamic Obstacles**: Different shapes and sizes of obstacles including rectangles and triangles
- **Progressive Difficulty**: Game gets harder every 1000 points with:
  - Increased speed
  - More frequent obstacles
  - Chance of multiple obstacles
  - Character color changes
- **Responsive Controls**: Jump using the spacebar
- **Score System**: Track your progress and compete for high scores

## How to Play

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the game:
```bash
python game.py
```

3. Controls:
- Press `Space` to jump
- Click `Restart Game` button to start over after game over

## Game Mechanics

- The character moves automatically from left to right
- Jump over obstacles to survive
- Each obstacle hit ends the game
- Score increases as you survive longer
- Difficulty increases every 1000 points:
  - Level 0 (0-999): Blue character, normal speed
  - Level 1 (1000-1999): Green character, increased speed
  - Level 2 (2000-2999): Red character, even faster
  - And so on...

## Technical Details

- Built with Python and Eel for browser integration
- Uses HTML5 Canvas for rendering
- Implements collision detection
- Features smooth physics-based jumping
- Progressive difficulty scaling

## Game Demo

![Game Demo](game_demo.mov)

## Requirements

- Python 3.x
- Pygame
- Eel 