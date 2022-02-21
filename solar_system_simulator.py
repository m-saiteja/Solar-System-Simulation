import math
import pygame
pygame.init()

WIDTH, HEIGHT = 1000, 800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

SUN_COLOR = (255, 69, 0)
MERCURY_COLOR = (105, 105, 105)
VENUS_COLOR = (102, 102, 51)
EARTH_COLOR = (0, 0, 255)
MARS_COLOR = (255, 0, 0)
JUPITER_COLOR = (204, 102, 0)
SATURN_COLOR = (255, 153, 0)
URANUS_COLOR = (0, 204, 102)
NEPTUNE_COLOR = (0, 102, 153)

FONT = pygame.font.SysFont("comicsans", 16)


class CreatePlanet:
    """
    Class to create a planet with the given paramters.
    """
    AU = 149.6e6 * 1000 # distance between sun and earth in meters.
    G = 6.67428e-11     # gravitational constant.
    SCALE = 50 / AU
    TIMESTEP = 3600*24  # number of seconds in a day.

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.name = name
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.is_sun = False
        self.distance_to_sun = 0

        self.vel_x = 0
        self.vel_y = 0

    def plot(self, window):
        """
        Function to plot the simulation
        """
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        width = 0
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(window, self.color, False, updated_points, 2)

        pygame.draw.circle(window, self.color, (x, y), self.radius, width)

        if not self.is_sun:
            distance_text = FONT.render(f"{self.name}: {round(self.distance_to_sun/1000, 2)}km", 1, self.color)
            window.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def gravity_pull(self, other):
        """
        Fcuntion to calculate the gravity full and adjust the movement
        of the planets.
        """
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.is_sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_coordinates(self, planets):
        """
        Function to update the coordinates.
        """
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.gravity_pull(planet)
            total_fx += fx
            total_fy += fy

        self.vel_x += total_fx / self.mass * self.TIMESTEP
        self.vel_y += total_fy / self.mass * self.TIMESTEP

        self.x += self.vel_x * self.TIMESTEP
        self.y += self.vel_y * self.TIMESTEP
        self.orbit.append((self.x, self.y))



def main():
    """
    Main function to call the rest of the class methods.
    """
    run = True
    clock = pygame.time.Clock()

    sun = CreatePlanet(0, 0, 13, SUN_COLOR, 1.98*10**30, "SUN")
    sun.is_sun = True

    mercury = CreatePlanet(0.387*CreatePlanet.AU, 0, 4, MERCURY_COLOR, 3.30*10**23, "MERCURY")
    mercury.vel_y = -47.4*1000

    venus = CreatePlanet(0.723*CreatePlanet.AU, 0, 5, VENUS_COLOR, 4.86*10**23, "VENUS")
    venus.vel_y = -35.02*1000

    earth = CreatePlanet(-1*CreatePlanet.AU, 0, 6, EARTH_COLOR, 5.97*10**24, "EARTH")
    earth.vel_y = 29.78*1000

    mars = CreatePlanet(-1.524*CreatePlanet.AU, 0, 5, MARS_COLOR, 6.39*10**23, "MARS")
    mars.vel_y = 24.077*1000

    jupiter = CreatePlanet(5.203*CreatePlanet.AU, 0, 10, JUPITER_COLOR, 1898*10**24, "JUPITER")
    jupiter.vel_y = 13.1*1000

    saturn = CreatePlanet(9.555*CreatePlanet.AU, 0, 8, SATURN_COLOR, 568*10**24, "STAURN")
    saturn.vel_y = 9.7*1000

    # commenting out the code for URANUS and NETPTUNE as they are not
    # being covered on the screen :(

    # uranus = CreatePlanet(19.191*CreatePlanet.AU, 0, 18, URANUS_COLOR, 86.8*10**24, "URANUS")
    # uranus.vel_y = 6.8*1000

    # neptune = CreatePlanet(30.107*CreatePlanet.AU, 0, 18, NEPTUNE_COLOR, 102*10**24, "NEPTUNE")
    # neptune.vel_y = 5.4*1000


    planets = [sun, mercury, venus, earth, mars, jupiter, saturn]  #, uranus, neptune]
    while run:
        clock.tick(60)
        WINDOW.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_coordinates(planets)
            planet.plot(WINDOW)
        pygame.display.update()
    pygame.quit()

main()
