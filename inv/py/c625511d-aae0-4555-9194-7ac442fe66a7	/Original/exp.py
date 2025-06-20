import pygame
import random
import math


class Exp(pygame.sprite.Sprite):
    def __init__(self, x, y, game=None, amount=1, arming=False, angle=None, speed=None):
        super().__init__()
        self.game = game
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 255, 0), [(5, 0), (10, 5), (5, 10), (0, 5)])  # Green diamond shape
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.amount = amount
        self.speed = 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.fly_duration = 60  # Fly duration in frames (2 seconds at 60 FPS)
        self.fly_timer = 0
        self.arming_speed = 5  # Increased speed during arming
        self.arming_time = 60  # Arming time in frames (1 second at 60 FPS)
        self.armed_time = self.arming_time if arming else 0  # Set armed time based on the arming argument
        self.player = game.player if game else None
        self.initial_direction = None  # Store the initial random direction

        if arming and angle is not None and speed is not None:
            self.velocity_x = speed * math.cos(angle)
            self.velocity_y = speed * math.sin(angle)

    def update(self):

        if self.fly_timer < self.fly_duration:
            self.rect.x += self.velocity_x
            self.rect.y += self.velocity_y
            self.fly_timer += 1
        else:
            # Exp has finished flying, move towards the player
            self.move_towards_player(self.player)

    def move_towards_player(self, player):
        if player:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance <= 100:  # Only move towards the player if within 100 pixels
                if distance > 0:
                    self.rect.x += dx / distance * self.speed
                    self.rect.y += dy / distance * self.speed

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))