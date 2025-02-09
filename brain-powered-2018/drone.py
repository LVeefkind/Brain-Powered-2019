#! /usr/bin/env python3
# Communication with drone
# By Derk Barten and Devin Hillenius
# UvA Brain Powered 2017-2018

from pyardrone import ARDrone, at
from time import sleep, time


class Drone(object):
    def __init__(self):
        self.d = ARDrone()
        self.d.navdata_ready.wait()

    def takeoff(self):
        """Start flying the drone."""
        self.d.takeoff()

    def land(self):
        """Land the drone."""
        self.d.land()

    def move(self, direction):
        """
        Move the drone forward or backward or rotate the drone for 't' seconds.
        The 'direction' argument can be:
            - 'forward': move forward
            - 'backward': move backward
            - 'rotate_right': rotate 90 degrees to the right
            - 'rotate_left': rotate 90 degrees to the left
        """
        if direction == 'forward':
            self.forward(t=2)
        elif direction == 'backward':
            self.backward(t=1)
        elif direction == 'rotate_right':
            self.cw(t=0.4)
        elif direction == 'rotate_left':
            self.ccw(t=0.4)
        else:
            raise ValueError(
                'Given direction {} not supported!'.format(direction))
        self.d.hover()

    def forward(self, t=0.3, s=0.1):
        t_end = time() + t
        while time() < t_end:
            self.d.move(forward=s)

    def backward(self, t=0.3, s=0.1):
        t_end = time() + t
        while time() < t_end:
            self.d.move(backward=s)

    def cw(self, t=0.08, s=0.8):
        t_end = time() + t
        while time() < t_end:
            self.d.move(cw=s)

    def ccw(self, t=0.08, s=0.8):
        t_end = time() + t
        while time() < t_end:
            self.d.move(ccw=s)



if __name__ == '__main__':
    try:
            DRONE = Drone()
            
            DRONE.takeoff()
            sleep(5)
            DRONE.move('forward')
            sleep(3)
            DRONE.move('forward')
            sleep(7)
            DRONE.move('forward')
            sleep(3)
            sleep(2)
            DRONE.move('forward')
            sleep(7)
            DRONE.move('rotate_right')
            sleep(5)
            DRONE.move('forward')
            sleep(3)
            DRONE.move
            DRONE.move('forward')
            sleep(3)
            DRONE.move('forward')
            sleep(7)
            DRONE.land()
            sleep(2)
            quit()
    except Exception as e:
        print(e)
        DRONE = None
        # handle_signint(1, 1)
