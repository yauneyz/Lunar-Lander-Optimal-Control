import math
import numpy as np

PI = 3.1415926
HEIGHT = 800

# Ship class

class Ship():
    
    def __init__(self,x0,y0,xv0,yv0,T,theta,m,dT):
        self.x = x0
        self.y = y0
        self.xv = xv0
        self.yv = yv0
        self.T = T
        self.theta = theta
        self.dT = dT
        self.m = m
        self.gas = 10000
        
        self.T_c = 0
        self.theta_c = 0
        self.g = 9.8
        
        self.max_T = 100000
        self.max_theta = 2*np.pi

        self.foot1XPoints = []
        self.foot1YPoints = []
        self.foot2XPoints = []
        self.foot2YPoints = []
        self.leg1XPoints = []
        self.leg1YPoints = []
        self.leg2XPoints = []
        self.leg2YPoints = []
        self.bodyXPoints = []
        self.bodyYPoints = []
        
    def step(self):
        self.x += self.xv*self.dT
        self.y += self.yv*self.dT
        self.xv += (self.T/self.m)*np.sin(self.theta)*self.dT
        self.yv -= (self.g - (self.T/self.m)*np.cos(self.theta))*self.dT
        
        self.T += self.T_c
        self.theta += self.theta_c
        self.gas -= self.T*self.dT
        
        if self.T > self.max_T:
            self.T = self.max_T
        if self.theta > self.max_theta:
            self.theta = 0
            
    def set_control(self,dThrust,dTheta):
        self.T_c = dThrust
        self.theta_c = dTheta
        
    def set_vel(self,vx,vy):
        self.xv = vx
        self.yv = vy
        
    def set_strong_control(self,Thrust,theta):
        self.T = Thrust
        self.theta = theta
        
    def get_state(self):
        return self.x,self.xv,self.y,self.yv,self.theta,self.T


    def frange(self, x, y, jump):
        while x < y:
            yield x
            x += jump

    # Set x and y positions
    def setPos(self, x, y):
        self.x = x
        self.y = y

    # Get gas
    def getGas(self):
        return self.gas

    # Set gas
    def setGas(self, g):
        if g < 0:
            self.gas = 0
        else:
            self.gas = g

    # Rotate ship. Min angle of -PI and max angle of 0
    # Change thrust power based on given modifier. Max thrust power of 8 and min of 0.

    # Draw ship
    def draw(self, screen):
        self.theta = -self.theta + np.pi
        screen.draw.line((self.x - 6.0 * math.sin(self.theta + (PI / 6.0)),
                         (HEIGHT - self.y) - 6.0 * math.cos(self.theta + PI / 6.0)),
                         (self.x - 12.0 * math.sin(self.theta + (PI / 6.0)),
                          (HEIGHT - self.y) - 12.0 * math.cos(self.theta + PI / 6.0)),
                         (255, 255, 255))
        screen.draw.line((self.x - 6.0 * math.sin(self.theta - (PI / 6.0)),
                          (HEIGHT - self.y) - 6.0 * math.cos(self.theta - PI / 6.0)),
                         (self.x - 12.0 * math.sin(self.theta - (PI / 6.0)),
                          (HEIGHT - self.y) - 12.0 * math.cos(self.theta - PI / 6.0)),
                         (255, 255, 255))
        
        
        screen.draw.circle((self.x, HEIGHT - self.y), 6, (255, 255, 255))

        self.theta = -self.theta - np.pi


    # Check if ship collides with terrain from given terrain vectors
    def collision(self, xt, yt):
        foot1Touch = False
        foot2Touch = False

        for i in range(0, len(xt)):
            for j in range(0, len(self.bodyXPoints)):
                if self.bodyXPoints[j] > xt[i] - 2 and self.bodyXPoints[
                        j] < xt[i] + 2:
                    if self.bodyYPoints[j] > yt[i]:
                        return 1

        for i in range(0, len(xt)):
            for k in range(0, len(self.foot1XPoints)):
                if self.foot1XPoints[k] > xt[i] - 2 and self.foot1XPoints[
                        k] < xt[i] + 2:
                    if self.foot1YPoints[k] >= yt[i]:
                        foot1Touch = True
                if self.foot2XPoints[k] > xt[i] - 2 and self.foot2XPoints[
                        k] < xt[i] + 2:
                    if self.foot2YPoints[k] >= yt[i]:
                        foot2Touch = True
                if foot1Touch and foot2Touch:
                    return 2

        for i in range(0, len(xt)):
            for k in range(0, len(self.leg1XPoints)):
                if self.leg1XPoints[k] > xt[i] - 2 and self.leg1XPoints[
                        k] < xt[i] + 2:
                    if self.leg1YPoints[k] >= yt[i]:
                        return 1
                if self.leg2XPoints[k] > xt[i] - 2 and self.leg2XPoints[
                        k] < xt[i] + 2:
                    if self.leg2YPoints[k] >= yt[i]:
                        return 1

        return 0

    # Calculate and generate hitbox points
    def hitbox(self):
        self.bodyXPoints.clear()
        self.bodyYPoints.clear()
        self.leg1XPoints.clear()
        self.leg1YPoints.clear()
        self.leg2XPoints.clear()
        self.leg2YPoints.clear()
        self.foot1XPoints.clear()
        self.foot1YPoints.clear()
        self.foot2XPoints.clear()
        self.foot2YPoints.clear()

        for i in self.frange(0, 2.0 * PI, 0.25):
            self.bodyXPoints.append(int(round(self.x - 6.0 * math.cos(i))))
            self.bodyYPoints.append(int(round(self.y - 6.0 * math.sin(i))))

        for i in self.frange(6.0, 11.0, 1):
            self.leg1XPoints.append(
                int(round(self.x - i * math.cos(self.theta + (PI / 6.0)))))
            self.leg1YPoints.append(
                int(round(self.y - i * math.sin(self.theta + (PI / 6.0)))))
            self.leg2XPoints.append(
                int(round(self.x - i * math.cos(self.theta - (PI / 6.0)))))
            self.leg2YPoints.append(
                int(round(self.y - i * math.sin(self.theta - (PI / 6.0)))))

        for i in self.frange(11.0, 12.0, 1):
            self.foot1XPoints.append(
                int(round(self.x - i * math.cos(self.theta + (PI / 6.0)))))
            self.foot1YPoints.append(
                int(round(self.y - i * math.sin(self.theta + (PI / 6.0)))))
            self.foot2XPoints.append(
                int(round(self.x - i * math.cos(self.theta - (PI / 6.0)))))
            self.foot2YPoints.append(
                int(round(self.y - i * math.sin(self.theta - (PI / 6.0)))))
