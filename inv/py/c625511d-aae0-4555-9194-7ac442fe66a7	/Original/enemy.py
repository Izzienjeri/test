import math

import pygame
import random
from config import ENEMY_SIZE, ENEMY_SPEED, WINDOW_SIZE
from topdown.arena import GameArea
from topdown.enemy_bullet import EnemyBullet
from topdown.exp import Exp
from topdown.explosion import Explosion

from typing import List, Tuple

import pygame
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image, player, enemy_group, game, speed=2.0):  # Change speed to float
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = float(x)  # Use float for x position
        self.y = float(y)  # Use float for y position
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.player = player
        self.enemy_group = enemy_group
        self.game = game
        self.max_health = 100
        self.health = self.max_health
        self.speed = float(speed)  # Use float for speed
        self.target_x = None
        self.target_y = None
        self.original_speed = float(speed)  # Use float for original speed
        self.ice_timer = 0
        self.burning_timer = 0
        self.burning_duration = 1000  # Duration of burning effect in milliseconds (1 second)
        self.burning_damage = 0  # Damage taken per second while burning (initialized to 0)
        self.last_burning_damage_time = 0 # Duration of burning effect in milliseconds (1 second)

    def handle_burn(self):
        collided_fire_areas = pygame.sprite.spritecollide(self, self.game.fire_areas, False)
        if collided_fire_areas:
            self.burning_timer = self.burning_duration
            self.burning_damage = collided_fire_areas[0].damage  # Set the burning damage based on the collided fire area

        # Apply burning damage if the enemy is burning
        if self.burning_timer > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_burning_damage_time >= 250:  # Damage every 0.25 seconds
                self.take_damage(self.burning_damage)
                self.last_burning_damage_time = current_time

            self.burning_timer -= self.game.delta_time * 1000  # Decrease the burning timer

    def handle_slow(self):
        collided_ice_patches = pygame.sprite.spritecollide(self, self.game.ice_patches, False)
        if collided_ice_patches:

            self.ice_timer = 500  # Reset the ice timer to 0.5 seconds
            # Get the maximum slow percentage from the collided ice patches
            max_slow_percentage = max(patch.slow_percentage for patch in collided_ice_patches)
            self.speed = self.original_speed * (1 - max_slow_percentage / 100)  # Apply the slow percentage
        else:
            self.ice_timer = max(0, self.ice_timer - self.game.delta_time * 1000)  # Decrease the ice timer

            if self.ice_timer == 0:
                self.speed = self.original_speed  # Restore the original speed when not on an ice patch

    def update(self):
        self.follow_player()
        self.move()
        self.avoid_collision()
        self.handle_burn()
        self.handle_slow()

        # Wrap the enemy position around the game area
        if self.x < 0:
            self.x = GameArea.size[0]
        elif self.x > GameArea.size[0]:
            self.x = 0

        if self.y < 0:
            self.y = GameArea.size[1]
        elif self.y > GameArea.size[1]:
            self.y = 0

        # Update the enemy's rect position
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

    def move(self):
        if self.target_x is not None and self.target_y is not None:
            # Calculate the direction towards the target position
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance > 0:
                # Normalize the direction vector
                direction_x = dx / distance
                direction_y = dy / distance

                # Update the enemy's position based on the normalized direction and speed
                self.x += direction_x * self.speed
                self.y += direction_y * self.speed

        # Update the enemy's rect position
        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

    def follow_player(self):
        player_center_x = self.player.x + self.player.rect.width // 2
        player_center_y = self.player.y + self.player.rect.height // 2

        # Calculate the distances considering wrapping around the edges
        dx = player_center_x - self.x
        dy = player_center_y - self.y

        # Check if going over the edge is shorter in the x-direction
        if abs(dx) > GameArea.size[0] / 2:
            if dx > 0:
                dx -= GameArea.size[0]
            else:
                dx += GameArea.size[0]

        # Check if going over the edge is shorter in the y-direction
        if abs(dy) > GameArea.size[1] / 2:
            if dy > 0:
                dy -= GameArea.size[1]
            else:
                dy += GameArea.size[1]

        self.target_x = self.x + dx

        self.target_y = self.y + dy




    def avoid_collision(self):
        # Check for collision with other enemies
        collided_enemies = pygame.sprite.spritecollide(self, self.enemy_group, False)
        for enemy in collided_enemies:
            if enemy != self:
                # Calculate the distance between the enemies
                dx = self.rect.centerx - enemy.rect.centerx
                dy = self.rect.centery - enemy.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)

                # Calculate the minimum distance required to avoid overlap
                min_distance = (self.rect.width + enemy.rect.width) / 2

                if distance < min_distance:
                    # Enemies are overlapping, separate them
                    overlap = min_distance - distance
                    angle = math.atan2(dy, dx)
                    self.rect.centerx += math.cos(angle) * overlap / 2
                    self.rect.centery += math.sin(angle) * overlap / 2
                    enemy.rect.centerx -= math.cos(angle) * overlap / 2
                    enemy.rect.centery -= math.sin(angle) * overlap / 2

                    # Update the enemy's position based on the rect position
                    self.x = self.rect.centerx
                    self.y = self.rect.centery

                    enemy.x = enemy.rect.centerx

                    enemy.y = enemy.rect.centery

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.die()

    def die(self):
        # Spawn 1 exp
        exp = Exp(self.rect.centerx, self.rect.centery, game=self.game)
        explosion = Explosion(self.rect.centerx, self.rect.centery, radius=20)
        self.game.explosions.add(explosion)
        self.game.exp_group.add(exp)
        self.kill()

    def draw(self, screen, camera_x, camera_y):
        self.draw_health_bar(screen, camera_x, camera_y)
        # Calculate the offset for wrapping
        offset_x = (camera_x // GameArea.size[0]) * GameArea.size[0]
        offset_y = (camera_y // GameArea.size[1]) * GameArea.size[1]

        # Draw the object at its wrapped position
        screen_x = self.rect.x - camera_x + offset_x
        screen_y = self.rect.y - camera_y + offset_y
        screen.blit(self.image, (screen_x, screen_y))

    def draw_health_bar(self, screen, camera_x, camera_y):
        bar_width = int(self.rect.width * 0.8)
        bar_height = 5
        bar_x = self.rect.centerx - bar_width // 2 - camera_x
        bar_y = self.rect.top - 10 - camera_y

        # Draw the background of the health bar
        background_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(screen, (0, 0, 0), background_rect)

        # Calculate the width of the green and red portions of the health bar
        green_width = int(bar_width * (self.health / self.max_health))
        red_width = bar_width - green_width

        # Draw the green portion of the health bar
        green_rect = pygame.Rect(bar_x, bar_y, green_width, bar_height)
        pygame.draw.rect(screen, (0, 255, 0), green_rect)

        # Draw the red portion of the health bar
        red_rect = pygame.Rect(bar_x + green_width, bar_y, red_width, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), red_rect)

        # Draw the outline of the health bar
        pygame.draw.rect(screen, (0, 0, 0), background_rect, 1)
class ShootingEnemy(Enemy):
    def __init__(self, x, y, player, enemy_group, game):
        image = pygame.Surface((100, 100))
        image.fill((0, 255, 0))  # Green color for shooting enemies
        super().__init__(x, y, image, player, enemy_group, game, speed=0.75)  # Pass speed=1 to the base class constructor
        self.max_health = 400
        self.health = self.max_health

        self.shooting_cooldown = 1000  # Cooldown duration in milliseconds
        self.last_shot_time = 0

    def update(self):
        super().update()
        self.shoot()


    def shoot(self):
        if self.game.renderer.is_inside_camera(self.rect):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shooting_cooldown:
                dx = self.player.rect.centerx - self.rect.centerx
                dy = self.player.rect.centery - self.rect.centery
                angle = math.degrees(math.atan2(dy, dx))
                bullet = EnemyBullet(self.rect.centerx, self.rect.centery, angle, 5)
                self.game.enemy_bullets.add(bullet)
                self.last_shot_time = current_time

    def die(self):
        # Spawn 4 exps that fly out in random directions for 2 seconds
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            speed = 5  # Increased speed for shooting enemy exp
            exp = Exp(self.rect.centerx, self.rect.centery, game=self.game, arming=True, angle=angle, speed=speed)
            self.game.exp_group.add(exp)
        explosion = Explosion(self.rect.centerx, self.rect.centery, radius=200)  # Medium explosion for shooting enemies
        self.game.explosions.add(explosion)
        super().die()


class SnakeSegment(Enemy):
    def __init__(self, x, y, game, prev_segment=None, is_head=False):
        image = pygame.Surface((20, 20))  # Adjust the size as needed
        image.fill((0, 255, 0))  # Green color for snake segments
        super().__init__(x, y, image, game.player, game.enemies, game, speed=2.0)  # Adjust the speed as needed

        self.prev_segment = prev_segment
        self.is_head = is_head
        self.min_distance = 15  # Adjust the minimum distance between segments
        self.velocity_smoothing = 0.8  # Adjust the velocity smoothing factor as needed
        self.following_player = False

        # Generate random initial direction with minimum x and y components
        min_direction = 0.5  # Minimum direction component (adjust as needed)
        angle = random.uniform(0, 2 * math.pi)
        self.velocity_x = math.cos(angle) * self.speed
        self.velocity_y = math.sin(angle) * self.speed

        # Ensure minimum x and y direction components
        if abs(self.velocity_x) < min_direction:
            self.velocity_x = math.copysign(min_direction, self.velocity_x)
        if abs(self.velocity_y) < min_direction:
            self.velocity_y = math.copysign(min_direction, self.velocity_y)

    def update(self):
        if self.is_head:
            if self.following_player:
                self.follow_player_movement()
            else:
                self.move_randomly()
                self.check_boundary_collision()
        else:
            if self.prev_segment is None or self.prev_segment.health <= 0:
                self.is_head = True
                self.following_player = True
                print("following")
            else:
                self.follow_prev_segment()

        self.rect.centerx = round(self.x)
        self.rect.centery = round(self.y)

        self.handle_burn()  # Call the handle_burn method explicitly
        self.handle_slow()  # Call the handle_slow method explicitly

    def move_randomly(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def check_boundary_collision(self):
        if self.x <= 0 or self.x >= self.game.game_area_surface.get_width() - self.rect.width:
            self.velocity_x = -self.velocity_x
        if self.y <= 0 or self.y >= self.game.game_area_surface.get_height() - self.rect.height:
            self.velocity_y = -self.velocity_y

    def follow_player_movement(self):
        player_x = self.player.rect.centerx
        player_y = self.player.rect.centery

        dx = player_x - self.x
        dy = player_y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        direction_x = dx / distance
        direction_y = dy / distance

        target_velocity_x = direction_x * self.speed
        target_velocity_y = direction_y * self.speed

        # Apply velocity smoothing to make the movement smoother
        self.velocity_x = self.velocity_x * self.velocity_smoothing + target_velocity_x * (
                1 - self.velocity_smoothing)
        self.velocity_y = self.velocity_y * self.velocity_smoothing + target_velocity_y * (
                1 - self.velocity_smoothing)

        self.x += self.velocity_x
        self.y += self.velocity_y

    def follow_prev_segment(self):
        prev_x = self.prev_segment.x
        prev_y = self.prev_segment.y

        dx = prev_x - self.x
        dy = prev_y - self.y

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.min_distance:
            direction_x = dx / distance
            direction_y = dy / distance

            target_velocity_x = direction_x * self.speed
            target_velocity_y = direction_y * self.speed

            self.x += target_velocity_x
            self.y += target_velocity_y

    def die(self):
        self.health = 0
        explosion = Explosion(self.rect.centerx, self.rect.centery, radius=10)
        self.kill()

        # 25% chance of dropping 1 exp
        if random.random() < 0.25:
            exp = Exp(self.x, self.y, game=self.player.game, amount=1)
            self.player.game.exp_group.add(exp)

    def draw(self, screen, camera_x, camera_y):
        super().draw(screen, camera_x, camera_y)  # Call the draw method of the parent Enemy class
        segment_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, (0, 255, 0), segment_rect)


def create_snake_segments(x, y, game, snake_length=20):
    segments = []
    prev_segment = None
    for i in range(snake_length):
        segment_x = x - i * 20  # Adjust the spacing between segments
        segment_y = y
        is_head = (i == 0)  # Set is_head to True for the first segment (head)
        segment = SnakeSegment(segment_x, segment_y, game, prev_segment, is_head)
        segments.append(segment)
        prev_segment = segment
    return segments



class LightningEnemy(Enemy):
    def __init__(self, x, y, player, enemy_group, game):
        image = pygame.Surface((100, 100))
        image.fill((255, 0, 255))  # Purple color for lightning enemies
        super().__init__(x, y, image, player, enemy_group, game, speed=0.5)
        self.max_health = 300
        self.health = self.max_health
        self.charge_duration = 3000  # Charge duration in milliseconds
        self.charge_start_time = None
        self.tracking_stop_time = None
        self.fire_direction = self.get_random_direction()
        self.lightning_start_time = None
        self.lightning_duration = 2000  # Duration of the lightning bolt in milliseconds (2 seconds)
        self.damage_interval = 250  # Interval between each damage tick in milliseconds (0.25 seconds)
        self.last_damage_time = 0

    def update(self):
        super().update()

        # Calculate the distance between the player and the lightning enemy
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance <= 1000:
            self.charge()
            self.fire()

            if self.lightning_start_time is not None:
                current_time = pygame.time.get_ticks()
                if current_time - self.lightning_start_time <= self.lightning_duration:
                    if current_time - self.last_damage_time >= self.damage_interval:
                        self.damage_player(1)
                        self.last_damage_time = current_time
                else:
                    self.lightning_start_time = None
        else:
            # Reset the charge if the player is more than 1300 pixels away

            self.reset_charge()

    def reset_charge(self):
        self.charge_start_time = None
        self.tracking_stop_time = None

    def damage_player(self, amount):
        if self.lightning_start_time is not None:
            # Calculate the distance between the player and the lightning bolt
            player_center = self.player.rect.center
            lightning_start = (self.rect.centerx, self.rect.centery)
            lightning_end = (
                lightning_start[0] + self.fire_direction[0] * 1000,
                lightning_start[1] + self.fire_direction[1] * 1000
            )

            # Check if the player is within the range of the lightning bolt
            distance = self.distance_to_line(player_center, lightning_start, lightning_end)
            if distance <= 30:  # Adjust the threshold as needed
                self.player.take_damage(amount)

    def distance_to_line(self, point, line_start, line_end):
        # Calculate the distance between a point and a line segment
        px, py = point
        x1, y1 = line_start
        x2, y2 = line_end

        # Calculate the vectors
        dx = x2 - x1
        dy = y2 - y1
        distance = abs(dy * px - dx * py + x2 * y1 - y2 * x1) / math.sqrt(dx ** 2 + dy ** 2)
        return distance

    def die(self):
        # Spawn 6 exps that fly out in different directions
        num_exp = 6
        for i in range(num_exp):
            angle = i * (360 / num_exp) * math.pi / 180  # Convert degrees to radians
            speed = 5  # Adjust the speed as needed
            exp = Exp(self.rect.centerx, self.rect.centery, game=self.game, arming=True, angle=angle, speed=speed)
            self.game.exp_group.add(exp)
        explosion = Explosion(self.rect.centerx, self.rect.centery, radius=200)  # Large explosion for lightning enemies
        self.game.explosions.add(explosion)
        super().die()

    def charge(self):
        if self.charge_start_time is None and self.lightning_start_time is None:
            # Start charging
            self.charge_start_time = pygame.time.get_ticks()
            self.tracking_stop_time = self.charge_start_time + self.charge_duration - 500  # Stop tracking 0.5 seconds before firing
            if self.fire_direction is None:
                self.fire_direction = (1, 0)  # Initial fire direction towards the right if not set

        elif self.charge_start_time is not None:
            current_time = pygame.time.get_ticks()

            if current_time < self.tracking_stop_time:
                # Calculate the desired angle towards the player
                dx = self.player.rect.centerx - self.rect.centerx
                dy = self.player.rect.centery - self.rect.centery
                desired_angle = math.atan2(dy, dx)

                # Calculate the current angle of the fire direction
                current_angle = math.atan2(self.fire_direction[1], self.fire_direction[0])

                # Calculate the angle difference
                angle_diff = desired_angle - current_angle

                # Normalize the angle difference to be within -pi and pi
                angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi

                # Calculate the rotation speed based on the charge duration
                rotation_speed = math.pi / (self.charge_duration / 6)  # Adjust the speed as needed

                # Rotate the fire direction towards the desired angle
                if angle_diff > 0:
                    current_angle += min(angle_diff, rotation_speed)
                else:
                    current_angle -= min(-angle_diff, rotation_speed)

                # Update the fire direction based on the current angle
                self.fire_direction = (math.cos(current_angle), math.sin(current_angle))

            # Check if charging is complete
            if current_time >= self.charge_start_time + self.charge_duration:
                self.charge_start_time = None

    def fire(self):
        if self.charge_start_time is None and self.lightning_start_time is None:
            # Fire the lightning bolt
            self.lightning_start_time = pygame.time.get_ticks()

    def rotate_vector(self, vector, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        cos_theta = math.cos(angle_radians)
        sin_theta = math.sin(angle_radians)
        x = vector[0] * cos_theta - vector[1] * sin_theta
        y = vector[0] * sin_theta + vector[1] * cos_theta
        return x, y

    def calculate_fire_direction(self):
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            direction_x = dx / distance
            direction_y = dy / distance
            return direction_x, direction_y
        return None

    def draw(self, screen, camera_x, camera_y):
        super().draw(screen, camera_x, camera_y)

        if self.lightning_start_time is not None:
            # Draw the lightning bolt
            current_time = pygame.time.get_ticks()
            if current_time - self.lightning_start_time <= self.lightning_duration:
                start_pos = (self.rect.centerx - camera_x, self.rect.centery - camera_y)
                end_pos = (
                    start_pos[0] + self.fire_direction[0] * 1000,
                    start_pos[1] + self.fire_direction[1] * 1000
                )

                # Check if the lightning bolt intersects with the player's rect
                player_rect = self.player.rect.move(-camera_x, -camera_y)
                if player_rect.clipline(start_pos, end_pos):
                    # Calculate the intersection point
                    intersection = player_rect.clipline(start_pos, end_pos)
                    if intersection:
                        # Update the end position to the intersection point
                        end_pos = intersection[0]

                self.draw_lightning_bolt(screen, start_pos, end_pos, (255, 255, 0))  # Yellow color



        else:
            # Draw the laser
            self.draw_laser(screen, camera_x, camera_y)

    def draw_laser(self, screen, camera_x, camera_y):
        # Draw the red laser during charging
        start_pos = (self.rect.centerx - camera_x, self.rect.centery - camera_y)
        end_pos = (
            start_pos[0] + self.fire_direction[0] * 1000,
            start_pos[1] + self.fire_direction[1] * 1000
        )

        # Check if the laser intersects with the player's rect
        player_rect = self.player.rect.move(-camera_x, -camera_y)
        if player_rect.clipline(start_pos, end_pos):
            # Calculate the intersection point
            intersection = player_rect.clipline(start_pos, end_pos)
            if intersection:
                # Update the end position to the intersection point
                end_pos = intersection[0]

        pygame.draw.line(screen, (255, 0, 0), start_pos, end_pos, 2)

    def get_random_direction(self):
        angle = random.uniform(0, 2 * math.pi)
        return (math.cos(angle), math.sin(angle))

    def draw_lightning_bolt(self, screen, start, end, color):
        num_lines = 5  # Number of lightning lines to draw
        line_points = []

        for _ in range(num_lines):
            points = self.generate_lightning_points(start, end)
            line_points.append(points)

        for points in line_points:
            pygame.draw.lines(screen, color, False, points, 1)  # Increased width of lightning bolt


    def generate_lightning_points(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        points: List[Tuple[int, int]] = [start]

        # Calculate the distance between start and end points
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = max(2, math.sqrt(dx ** 2 + dy ** 2))

        # Calculate the number of segments based on the distance
        num_segments = int(distance / 10)  # Adjust the divisor to change the number of segments

        # Generate intermediate points with random offsets
        for i in range(1, num_segments):
            x = start[0] + dx * i / num_segments
            y = start[1] + dy * i / num_segments

            # Apply random offset to x and y coordinates
            offset_x = random.randint(-10, 10)  # Adjust the range of the offset
            offset_y = random.randint(-10, 10)  # Adjust the range of the offset

            points.append((int(x + offset_x), int(y + offset_y)))

        points.append(end)
        return points

    def draw_lightning_segment(self, screen, start, end, color):
        # Calculate the distance between start and end points
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance = max(2, math.sqrt(dx ** 2 + dy ** 2))

        # Calculate the number of segments based on the distance
        num_segments = int(distance / 10)  # Adjust the divisor to change the number of segments

        # Initialize the current position to the start position
        current_pos = start

        # Draw the starting oscillating circle
        circle_radius = 5  # Adjust the radius as needed
        circle_width = 2  # Adjust the width of the circle outline
        oscillation_amplitude = 2  # Adjust the amplitude of the oscillation
        oscillation_speed = 0.1  # Adjust the speed of the oscillation
        oscillation_offset = pygame.time.get_ticks() * oscillation_speed
        circle_radius += oscillation_amplitude * math.sin(oscillation_offset)
        pygame.draw.circle(screen, color, end, circle_radius, circle_width)

        # Draw the lightning segments
        for _ in range(num_segments):
            # Calculate the next position with random offset
            next_pos = (
                current_pos[0] + dx / num_segments + random.randint(-3, 3),
                current_pos[1] + dy / num_segments + random.randint(-3, 3)
            )

            # Draw the line segment
            pygame.draw.line(screen, color, current_pos, next_pos, 1)  # Increased width of lightning bolt

            # Update the current position
            current_pos = next_pos

        # Draw the ending oscillating circle
        oscillation_offset = pygame.time.get_ticks() * oscillation_speed
        circle_radius += oscillation_amplitude * math.sin(oscillation_offset)




def spawn_enemy(game_area_rect, player, game):
    # Choose a random side of the screen to spawn the enemy
    side = random.choice(['left', 'right', 'top', 'bottom'])

    if side == 'left':
        x = game_area_rect.left + 100
        y = random.randint(game_area_rect.top + 100, game_area_rect.bottom - 100)
    elif side == 'right':
        x = game_area_rect.right - 100
        y = random.randint(game_area_rect.top + 100, game_area_rect.bottom - 100)
    elif side == 'top':
        x = random.randint(game_area_rect.left + 100, game_area_rect.right - 100)
        y = game_area_rect.top + 100
    else:  # 'bottom'
        x = random.randint(game_area_rect.left + 100, game_area_rect.right - 100)
        y = game_area_rect.bottom - 100

    # Randomly choose between regular enemies, shooting enemies, and snake enemies
    enemy_type = random.random()

    if enemy_type < 0.1:  # 10% chance of spawning a snake enemy
        snake_segments = create_snake_segments(x, y, game, snake_length=20)
        for segment in snake_segments:
            game.enemies.add(segment)
    elif enemy_type < 0.2:  # 20% chance of spawning a shooting enemy
            enemy = ShootingEnemy(x, y, player, game.enemies, game)
            game.enemies.add(enemy)
    elif enemy_type < 0.35:  # 30% chance of spawning a lightning enemy
        enemy = LightningEnemy(x, y, player, game.enemies, game)
        game.enemies.add(enemy)
    else:  # 70% chance of spawning a regular enemy
        image = pygame.Surface((ENEMY_SIZE, ENEMY_SIZE))
        image.fill((255, 0, 0))  # Red color for regular enemies
        enemy = Enemy(x, y, image, player, game.enemies, game)
        game.enemies.add(enemy)
