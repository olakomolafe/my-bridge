import pygame
import sys
import math
import random

# Init
pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RIALO. Breaks the Bridge")
clock = pygame.time.Clock()

# Optional Sound
try:
    collapse_sound = pygame.mixer.Sound("collapse.wav")
except:
    collapse_sound = None

# Colors
SKY = (180, 220, 255)
BRIDGE_COLOR = (100, 60, 40)
ARCH_COLOR = (80, 40, 30)
PILLAR_COLOR = (70, 70, 70)
DUST_COLOR = (150, 150, 150)
TEXT_COLOR = (0, 0, 0)

# Dust particle
class Dust:
    def __init__(self, x, y):
        self.x = x + random.randint(-10, 10)
        self.y = y
        self.radius = random.randint(2, 5)
        self.life = 30
        self.dy = random.uniform(-2, -0.5)
        self.dx = random.uniform(-1.5, 1.5)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.life -= 1
        self.dy += 0.1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, DUST_COLOR, (int(self.x), int(self.y)), self.radius)

# Segment class
class Segment:
    def __init__(self, x, y):
        self.origin_x = x
        self.rect = pygame.Rect(x, y, 60, 20)
        self.falling = False
        self.velocity = 0
        self.shake_offset = 0
        self.shaking = False
        self.shake_timer = 0
        self.hit_ground = False

    def start_shaking(self):
        self.shaking = True
        self.shake_timer = 30

    def update(self, particles):
        if self.shaking:
            self.shake_timer -= 1
            self.shake_offset = random.randint(-4, 4)
            if self.shake_timer <= 0:
                self.shaking = False
                self.falling = True
                if collapse_sound:
                    collapse_sound.play()

        elif self.falling:
            self.velocity += 0.5
            self.rect.y += self.velocity
            if self.rect.y >= 330 and not self.hit_ground:
                self.hit_ground = True
                for _ in range(10):
                    particles.append(Dust(self.rect.centerx, self.rect.bottom))

        else:
            self.rect.x = self.origin_x + self.shake_offset

    def draw(self, surface):
        pygame.draw.rect(surface, BRIDGE_COLOR, self.rect, border_radius=3)
        if not self.falling:
            pygame.draw.line(surface, PILLAR_COLOR, (self.rect.centerx, self.rect.bottom), (self.rect.centerx, self.rect.bottom + 60), 4)

# Draw arches
def draw_arches(surface, segments):
    for seg in segments:
        if not seg.falling:
            cx = seg.rect.centerx
            cy = seg.rect.bottom + 20
            radius = 30
            pygame.draw.arc(surface, ARCH_COLOR, (cx - radius, cy - radius, 2 * radius, radius * 2), math.pi, 2 * math.pi, 3)

# Create bridge
bridge_segments = []
particles = []
start_x = 100
y = 200
for i in range(10):
    seg = Segment(start_x + i * 65, y)
    bridge_segments.append(seg)

# RIALO animation
font = pygame.font.SysFont("Arial Black", 48)
rialo_x = -200
rialo_y = 150
rialo_active = False
impact_x = bridge_segments[3].rect.centerx - 30
speed = 12
bridge_hit = False

# Game loop
running = True
breaking = False

while running:
    screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Press space to trigger RIALO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not breaking:
                rialo_active = True
                breaking = True

    # Move RIALO text
    if rialo_active:
        rialo_x += speed
        if rialo_x >= impact_x and not bridge_hit:
            # Start breaking the bridge
            for i in range(3, 7):
                bridge_segments[i].start_shaking()
            bridge_hit = True

    # Update segments
    for seg in bridge_segments:
        seg.update(particles)

    for dust in particles[:]:
        dust.update()
        if dust.life <= 0:
            particles.remove(dust)

    # Draw
    draw_arches(screen, bridge_segments)
    for seg in bridge_segments:
        seg.draw(screen)
    for dust in particles:
        dust.draw(screen)

    # Draw RIALO text
    if rialo_active:
        rialo_text = font.render("RIALO.", True, TEXT_COLOR)
        screen.blit(rialo_text, (rialo_x, rialo_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
