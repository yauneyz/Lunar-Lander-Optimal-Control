import pgzrun
import ship as lander
import terrain as land
# from control import op_traject as Controller
#from controller import get_control
from andrew import Controller,PID
import time
import numpy as np

WIDTH = 1400
HEIGHT = 800
DIM = (WIDTH, HEIGHT)
PI = 3.1415926

# Game class


class Game:
    # Initialize game state
    def __init__(self):
        # Variables for game state
        self.score = 0
        self.state = 1
        self.multiplier = 1
        self.playing = True

        # Used to see if there is no collision (0), a crash (1), or a potential landing (2)
        self.collided = 0

        # Variables for physics
        self.dt = 1e-1

        # Used to see what kind of landing: good landing (1), hard landing (2), or a crash (3)
        self.landingType = 0

        # Ship and terrain objects
        self.terrain = land.Terrain()
        self.xTerrain = []
        self.yTerrain = []

        # Used to schedule a life reset after the landing/crash screen
        self.resetScheduled = False
        
    # Reset game state
    def resetGame(self):
        self.resetLife()
        game.state = 2
        game.score = 0
        game.landPID = PID(0.5,0.4,1e-3,dT = self.dt) 
        game.ship.setGas(1e20)

    # Reset settings for new life
    def resetLife(self):
        game.ship = lander.Ship(100,600,0,0,0,0,1,self.dt)
        self.x,self.y,self.xv,self.yv,self.T,self.theta = game.ship.get_state()

        game.terrain.generate(WIDTH, HEIGHT, 450, 1)
        game.collided = 0
        game.multiplier = 1
        game.xTerrain = game.terrain.getXPoints()
        game.yTerrain = game.terrain.getYPoints()
        game.playing = True
        game.resetScheduled = False

        self.xf,self.yf = self.terrain.get_goal()
        # Initialize the control
        init_state = [100, 600, 0, 0, self.xf, HEIGHT - self.yf, 1, 1e-1, 15]

        self.control = Controller(*init_state)
        self.control_time = 0


    # Callback for switching from game over screen
    def gameOver(self):
        game.resetScheduled = False
        game.state = 1


game = Game()
game.resetGame()

# Main logic for drawing


def draw():
    screen.clear()

    # Main menu state
    if game.state == 1:
        screen.draw.text(
            "LUNAR LANDER",
            (WIDTH / 2 - 250, HEIGHT / 2 - 60),
            fontsize=80,
            fontname="roboto",
        )
        screen.draw.text("Press P to play", (WIDTH / 2 - 70, HEIGHT / 2 + 50),
                         fontname="roboto")
        screen.draw.text(
            "Controls:\nLeft and Right Arrows: Rotate Ship\nUp and Down Arrows: Strengthen/Weaken Thrusters\nQ: Quit game",
            (WIDTH / 2 - 270, HEIGHT / 2 + 120),
            align="center",
            fontname="roboto",
        )

    # Playing state
    elif game.state == 2:
        game.ship.draw(screen)
        game.terrain.draw(screen)
        scoreStr = "SCORE    " + str(game.score)
        gasStr = "FUEL       " + str(int(game.gas))
        altStr = "ALTITUDE                      " + \
            str(int(HEIGHT - 10 - game.y))
        xVelStr = "HORIZONTAL SPEED    " + str(int(game.xv))
        yVelStr = "VERTICAL SPEED         " + str(int(-game.yv))
        screen.draw.text(scoreStr, (40, 40), fontsize=20, fontname="roboto")
        screen.draw.text(gasStr, (40, 60), fontsize=20, fontname="roboto")
        screen.draw.text(altStr, (WIDTH - 260, 40),
                         fontsize=20,
                         fontname="roboto")
        screen.draw.text(xVelStr, (WIDTH - 260, 60),
                         fontsize=20,
                         fontname="roboto")
        screen.draw.text(yVelStr, (WIDTH - 260, 80),
                         fontsize=20,
                         fontname="roboto")

        # If the ship collided with the terrain, display the correct message
        if game.collided == 1:
            screen.draw.text(
                "YOU CRASHED\nYOU LOST 100 FUEL UNITS",
                (WIDTH / 2 - 130, HEIGHT / 2 - 30),
                align="center",
                fontname="roboto",
            )
            if not game.resetScheduled:
                game.resetScheduled = True
                clock.schedule(game.resetLife, 4.0)
        elif game.collided == 2:
            if game.landingType == 1:
                screen.draw.text(
                    "GOOD LANDING\n50 FUEL UNITS ADDED",
                    (WIDTH / 2 - 100, HEIGHT / 2 - 30),
                    align="center",
                    fontname="roboto",
                )
            elif game.landingType == 2:
                screen.draw.text("HARD LANDING",
                                 (WIDTH / 2 - 75, HEIGHT / 2 - 30),
                                 fontname="roboto")
            elif game.landingType == 3:
                screen.draw.text(
                    "YOU CRASHED\nYOU LOST 100 FUEL UNITS",
                    (WIDTH / 2 - 130, HEIGHT / 2 - 30),
                    align="center",
                    fontname="roboto",
                )
            if not game.resetScheduled:
                game.resetScheduled = True
                clock.schedule(game.resetLife, 4.0)

    # Game over state
    elif game.state == 3:
        game.ship.draw(screen)
        game.terrain.draw(screen)
        scoreStr = "SCORE    " + str(game.score)
        gasStr = "FUEL       " + str(int(game.gas))
        altStr = "ALTITUDE                      " + \
            str(int(HEIGHT - 10 - game.y))
        xVelStr = "HORIZONTAL SPEED    " + str(int(game.xv))
        yVelStr = "VERTICAL SPEED         " + str(int(-game.yVel))
        screen.draw.text(scoreStr, (40, 40), fontsize=20, fontname="roboto")
        screen.draw.text(gasStr, (40, 60), fontsize=20, fontname="roboto")
        screen.draw.text(altStr, (WIDTH - 260, 40),
                         fontsize=20,
                         fontname="roboto")
        screen.draw.text(xVelStr, (WIDTH - 260, 60),
                         fontsize=20,
                         fontname="roboto")
        screen.draw.text(yVelStr, (WIDTH - 260, 80),
                         fontsize=20,
                         fontname="roboto")

        screen.draw.text(
            "YOU RAN OUT OF FUEL\nGAME OVER",
            (WIDTH / 2 - 115, HEIGHT / 2 - 30),
            align="center",
            fontname="roboto",
        )
        if not game.resetScheduled:
            game.resetScheduled = True
            clock.schedule(game.gameOver, 5.0)


# Update game state
def update(dt):
    game.dt = dt

    # Menu state. Wait for 'p' to start game
    if game.state == 1:
        if keyboard.p:
            game.resetGame()

    # Game state. Update game variables, update ship, check collisions
    elif game.state == 2:
        if game.playing:
            # Get the fuel, velocities, positions, and angle
            game.gas = game.ship.getGas()

            game.x,game.xv,game.y,game.yv,game.T,game.theta = game.ship.get_state()

            # If ship goes off on the side of the screen, it is moved to the other side.
            if game.x > WIDTH + 10:
                game.x = -10
            elif game.x < -10:
                game.x = WIDTH + 10

            # If the ship goes too high, then it is placed back at the initial spawn point
            if game.y < -50:
                game.x = 100
                game.y = 100
                game.xv = 50
                game.yv = 0

            # Makes x velocity stay within - 100 and 100 inclusive
            if game.xv >= 100:
                game.xv = 100
            elif game.xv <= -100:
                game.xv = -100

            # Consider gravity

            # Get the controls
            state = [game.x, game.y, game.xv, game.yv]
            if game.control_time < np.abs(game.control.tf):
                theta, T = game.control.get_control(game.control_time, *state)
        
                game.control_time += dt
                game.ship.set_strong_control(T,theta)
                game.ship.step()
            else:
                T_control = game.landPID.step(game.yf - game.y)
                game.ship.set_strong_control(T_control,0)
                game.ship.step()


            # Q key; Effectively quit program
            if keyboard.q:
                game.state = 1

            # Recalculates ship's hitbox
            game.ship.hitbox()

            # Checks if the ship collided with the terrain
            game.collided = 0
            game.collided = game.ship.collision(game.xTerrain,game.yTerrain)
            game.collided = 0

            # Crashed
            if game.collided == 1:
                game.playing = False
                game.score += 5
                game.ship.setGas(game.ship.getGas() - 100)
                game.gas = game.ship.getGas()
            # Potential landing
            elif game.collided == 2:
                game.playing = False

                # Checks if the ship landed on a multiplier spot
                game.multiplier = game.terrain.multiplierCheck(
                    game.ship.getXpos())

                # If the user has a good landing
                if game.yVel < 12 and abs(game.xv) < 25:
                    game.landingType = 1
                    game.ship.setGas(game.ship.getGas() + 50)
                    game.score += game.multiplier * 50
                # If the user has a hard landing
                elif game.yVel < 25 and abs(game.xv) < 25:
                    game.landingType = 2
                    game.score += game.multiplier * 15
                # If the user was going too fast resulting in a crash
                else:
                    game.landingType = 3
                    game.score += 5
                    game.ship.setGas(game.ship.getGas() - 100)

                # Update game state gas for display
                game.gas = game.ship.getGas()

            # Out of gas
            if game.ship.getGas() <= 0:
                game.gas = game.ship.getGas()
                game.state = 3


# Run game
pgzrun.go()
