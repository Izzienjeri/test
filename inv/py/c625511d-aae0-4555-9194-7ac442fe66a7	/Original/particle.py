import pygame
import random
import math


class Particle:
    def __init__(self, x, y, color, speed, angle):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.angle = angle
        self.lifetime = random.randint(60, 120)  # Particle lifetime
        self.size = random.randint(1, 3)  # Particle size

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.lifetime -= 1
        self.size -= 0.1  # Gradually decrease the particle size

    def draw(self, screen, camera_x, camera_y):
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        pygame.draw.circle(screen, self.color, (screen_x, screen_y), int(self.size))

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=50):
        super().__init__()
        self.particles = []
        self.lifetime = 60  # Explosion lifetime in frames
        self.radius = radius

        # Generate particles for the explosion
        for _ in range(100):  # Number of particles
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, radius)
            particle_x = x + distance * math.cos(angle)
            particle_y = y + distance * math.sin(angle)
            speed = random.uniform(1, 5)
            color = random.choice([(255, 0, 0), (255, 165, 0), (255, 255, 0)])  # Red, orange, yellow
            particle = Particle(particle_x, particle_y, color, speed, angle)
            self.particles.append(particle)

    def update(self):
        for particle in self.particles:
            particle.update()

        self.particles = [particle for particle in self.particles if particle.lifetime > 0]

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()  # Remove the explosion sprite when the animation is finished

    def draw(self, screen, camera_x, camera_y):
        for particle in self.particles:
            particle.draw(screen, camera_x, camera_y)
