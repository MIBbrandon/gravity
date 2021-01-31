import math
import os
from pathlib import Path

import pygame
from config import *
from Objects.SolarSystem import SolarSystem
from DashboardStuff.dashboard import dashboard
from astropy.time import Time
import datetime
from sunpy.coordinates import get_body_heliographic_stonyhurst
from numpy import deg2rad, sin

pygame.init()

screenWidth, screenHeight = 1000, 700

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Gravity")
base_path = Path(os.path.dirname(__file__))
icon = pygame.image.load(os.path.join(base_path, "sprites", "gravityIcon.ico"))
pygame.display.set_icon(icon)
screen.fill((0, 0, 0))

# Creating the solar system
solarSystem = SolarSystem(screen)
solarSystem.sun.setPosition([screenWidth/2, screenHeight/2])
# print("Sun position: " + str(solarSystem.sun.getPosition()[0]) + ", " + str(solarSystem.sun.getPosition()[1]))

# Array with the initial positions of the planets
# obstime = Time('2014-05-15T07:54:00.005')
obstime = Time(datetime.datetime.now())
planet_list = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
planet_coord = [get_body_heliographic_stonyhurst(this_planet, time=obstime) for this_planet in planet_list]
i = 100 # Used for when we want to start all planets in a single line
for this_planet, this_coord in zip(planet_list, planet_coord):
    # Angle at which the planet can be found
    longitude = float(str(deg2rad(this_coord.lon)).split('rad')[0])

    # Distance from the sun
    radius = float(str(this_coord.radius).split(' AU')[0])  # Get the first 5 character positions, so 3 decimals

    # The previous radius was in AU. We want to adjust this number so that all the planets fit on the screen
    radius = math.log(radius + 1, baseController)
    # print(radius)

    # With the absolute distance (radius) and the angle (longitude) we now obtain the position of each planet
    # We obviously convert from AU to pixels (1 AU should be 200 pixels)
    XrelativePositionToSun = (radius * pixelsPerAU)
    YrelativePositionToSun = (sin(longitude) * radius * pixelsPerAU)
    relPosToSun = [XrelativePositionToSun, YrelativePositionToSun]
    # print(this_planet + " relation to sun: " + str(XrelativePositionToSun) + ", " + str(YrelativePositionToSun))

    # We now place each planet's position
    solarSystem.setPlanetPosition(this_planet, [(relPosToSun[0] + solarSystem.sun.getPosition()[0]),
                                                (relPosToSun[1] + solarSystem.sun.getPosition()[1])])

    # # ------------------Uncomment this section if you want all the planets to be in a line----------------------------
    # solarSystem.sun.setPosition([500, 350])
    # solarSystem.setPlanetPosition(this_planet, [solarSystem.sun.getPosition()[0] + i,
    #                               solarSystem.sun.getPosition()[1]])
    # i += 50
    # # ----------------------------------------------------------------------------------------------------------------

# Creating the dashboard and giving it the pointer of the Solar System
dashboard = dashboard(solarSystem)

# Now we need to give the pointer of the Solar System to the dashboard
solarSystem.obtainPointerToDashboard(dashboard)

# This keeps track of the iterations we have gone through, and tries to make it all as smooth as possible
clock = pygame.time.Clock()
FPS = 60

def drawAllObjects():
    """
    Executes the draw() method of every object
    """
    for thing in solarSystem.astralObjects:
        thing.draw()
    solarSystem.sun.draw()

    # Makes the dashboard appear only when mouse hovers above the area
    if(dashboard.isOver(pygame.mouse.get_pos())):
        dashboard.draw(screen)


def updateTimeAwareness():
    if(clock.get_fps()): #Makes sure not to return 0
        return clock.get_fps()
    return 60 #This is what I expect to be the FPS around


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            dashboard.readjustPositions([event.w, event.h])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Set running to False to end the while loop.
            if event.key == pygame.KMOD_SHIFT:
                solarSystem.shiftPressed = True
                dashboard.shiftPressed = True
            else:
                solarSystem.shiftPressed = False
                dashboard.shiftPressed = False

    # Make the screen black
    screen.fill((0, 0, 0))

    # solarSystem.printAllPlanetPositions()

    #Give the Solar System the latest information regarding time
    solarSystem.updateFPS(FPS)

    # Let the Solar System do whatever it needs to do
    solarSystem.exist()

    # Animating and activating the dashboard
    dashboard.animateAndActivate()

    # Draw each object in their new position
    drawAllObjects()

    clock.tick(60)
    FPS = updateTimeAwareness()
    pygame.display.update()