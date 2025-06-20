import random

import pygame
import math

from topdown.explosion import Explosion


class FireBomb(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, game, damage, radius, player_velocity_x, player_velocity_y):
        super().__init__()
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.game = game
        self.speed = 8
        self.angle = 0
        self.rotation_speed = 720  # 2 rotations per second (360 degrees * 2)
        self.width = 20
        self.height = 40
        self.original_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.damage = damage
        self.radius = radius
        self.velocity_x = self.speed * math.cos(math.radians(self.angle)) + player_velocity_x
        self.velocity_y = self.speed * math.sin(math.radians(self.angle)) + player_velocity_y

    def update(self, delta_time):

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 0:
            # Calculate the direction vector towards the crosshair
            direction_x = dx / distance
            direction_y = dy / distance

            # Update the fire bomb's position based on the direction vector
            self.x += direction_x * self.speed
            self.y += direction_y * self.speed
            self.rect.centerx = round(self.x)
            self.rect.centery = round(self.y)

        self.angle += self.rotation_speed * delta_time
        self.angle %= 360

        if distance < 5:
            self.explode()

    def explode(self):
        self.game.fire_areas.add(FireArea(self.rect.centerx, self.rect.centery, self.game, self.damage, self.radius))
        explosion = Explosion(self.rect.centerx, self.rect.centery, radius=self.radius)
        self.game.explosions.add(explosion)
        self.kill()

    def draw(self, screen, camera_x, camera_y):
        # Calculate the position of the fire bomb relative to the camera
        screen_x = self.rect.centerx - camera_x
        screen_y = self.rect.centery - camera_y

        # Rotate the image based on the current angle
        rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
        rotated_rect = rotated_image.get_rect(center=(screen_x, screen_y))

        # Draw the rotated image on the screen
        screen.blit(rotated_image, rotated_rect)


class FireArea(pygame.sprite.Sprite):
    def __init__(self, x, y, game, damage, radius):
        super().__init__()
        self.x = x
        self.y = y
        self.game = game
        self.duration = 4000
        self.radius = radius
        self.particles = []
        self.start_time = pygame.time.get_ticks()
        self.damage = damage

        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)  # Add a rect attribute

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.kill()
        else:
            self.update_particles()

    def update_particles(self):
        # Remove expired particles
        self.particles = [particle for particle in self.particles if not particle.is_expired()]

        # Generate new particles
        if len(self.particles) < 200:  # Increase the number of particles
            for _ in range(10):  # Generate multiple particles per frame
                particle = FireParticle(self.x, self.y, self.radius)
                self.particles.append(particle)

    def draw(self, screen, camera_x, camera_y):
        for particle in self.particles:
            particle.draw(screen, camera_x, camera_y)
class FireParticle:
    def __init__(self, x, y, max_radius):
        self.x = x + random.randint(-max_radius, max_radius)
        self.y = y + random.randint(-max_radius, max_radius)
        self.color = self.get_random_color()
        self.size = random.randint(3, 6)  # Increase the size range of particles
        self.speed = random.randint(2, 4)  # Increase the speed range of particles
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.randint(30, 60)  # Reduce the lifetime of particles
        self.start_time = pygame.time.get_ticks()

    def get_random_color(self):
        red = random.randint(200, 255)
        green = random.randint(0, 150)
        blue = 0
        return red, green, blue

    def is_expired(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.start_time >= self.lifetime

    def draw(self, screen, camera_x, camera_y):
        pygame.draw.circle(screen, self.color, (int(self.x - camera_x), int(self.y - camera_y)), self.size)
        self.update()

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.size -= 0.2  # Increase the rate at which particles shrink