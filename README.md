# Lunar Lander with PID Controller

A Python implementation of the classic Lunar Lander game featuring an autonomous PID controller that demonstrates optimal trajectory planning and landing control algorithms.

## Features

- **Autonomous Landing**: PID controller automatically pilots the lunar lander to optimal landing spots
- **Physics Simulation**: Realistic gravity, thrust, and collision physics
- **Procedural Terrain**: Randomly generated lunar surface with bonus multiplier zones
- **Visual Feedback**: Real-time display of altitude, speed, fuel, and score
- **Sound Effects**: Thrust and crash audio feedback

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd lunar-lander
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the game:
```bash
python lunarLander.py
```

### Controls
- **P**: Start game
- **Q**: Quit to main menu
- **Arrow Keys**: Manual control (if enabled)

### Gameplay
- Watch as the PID controller automatically navigates the lander to the highest-value landing zone
- Scoring is based on landing accuracy, fuel efficiency, and multiplier zones
- The game features multiple lives with fuel penalties for crashes

## Technical Details

The game demonstrates several advanced control systems concepts:

- **Optimal Trajectory Planning**: Uses boundary value problem solving for initial approach
- **PID Control**: Proportional-Integral-Derivative controller for precise landing
- **State Feedback**: Real-time monitoring of position, velocity, and orientation
- **Multi-phase Control**: Switches from trajectory following to altitude control

## Dependencies

- PyGame Zero (game engine)
- NumPy (numerical computations)
- SciPy (optimal control algorithms)
- Matplotlib (visualization support)

## License

This project builds upon aayala4's original Lunar Lander implementation.
