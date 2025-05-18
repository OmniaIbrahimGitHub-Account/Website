import pygame
import sys
import random
import math
import os

pygame.init()
pygame.mixer.set_num_channels(8)

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("لعبة السمكة والقرش")

SUN_COLOR = (255, 223, 0)
MOON_COLOR = (200, 200, 200)
STAR_COLOR = (255, 255, 255)
CLOUD_COLOR = (255, 255, 255, 180)
FISH_COLOR = (255, 165, 0)
FISH_SHINE_COLOR = (255, 215, 0)
FISH_STRIPE_COLOR = (255, 69, 0)
COIN_COLOR = (255, 215, 0)
SHARK_COLOR = (80, 140, 190)
SHARK_BELLY_COLOR = (210, 230, 245)
SHARK_FIN_COLOR = (60, 110, 160)
BUBBLE_COLOR = (255, 255, 255, 128)
BUBBLE_SHINE_COLOR = (255, 255, 255, 200)
SMALL_FISH_COLOR = (100, 100, 255)
BLOOD_COLOR = (200, 0, 0)
GLOW_COLOR = (255, 215, 0, 100)
SHADOW_COLOR = (0, 0, 0, 80)
SAND_COLOR = (255, 200, 100, 120)
CORAL_COLOR = (255, 100, 50, 150)
ICE_COLOR = (200, 200, 255, 150)
FOG_COLOR = (200, 200, 255, 50)
SAND_FLOOR_COLOR = (240, 200, 120)
CORAL_FLOOR_COLOR = (200, 100, 100)
ICE_FLOOR_COLOR = (180, 200, 255)

try:
    font = pygame.font.SysFont("comicsansms", 60, bold=True)
except:
    font = pygame.font.SysFont("Arial", 60, bold=True)

fish_x, fish_y = width // 4, height // 2
fish_speed = 6
fish_angle = 0
fish_scale = 1.0
score = 0
level = 1
game_over = False
win = False
shark_x, shark_y = width - 100, height // 2
shark_speed = 1.2
shark_shake = 0
shark_angle = 0
time_counter = 0
flash_timer = 0
blood_particles = []
glow_particles = []
sea_particles = []

coins = [[random.randint(0, width), random.randint(height // 2, height)] for _ in range(6)]

bubbles = [[random.randint(0, width), random.randint(height // 2, height), random.randint(2, 10), random.uniform(1, 3)] for _ in range(100)]

small_fish = [[random.randint(0, width), random.randint(height // 2, height), random.randint(-2, 2)] for _ in range(12)]

stars = [[random.randint(0, width), random.randint(0, height // 2), random.uniform(1, 3)] for _ in range(50)]

clouds = [[random.randint(0, width), random.randint(50, 150), random.randint(60, 100), random.uniform(0.5, 1.5)] for _ in range(5)]

clock = pygame.time.Clock()
FPS = 60

try:
    coin_sound = pygame.mixer.Sound(r"C:\Users\ae\OneDrive\Desktop\New folder\coin.mp3")
    coin_sound.set_volume(0.5)
    print("Loaded coin.mp3 successfully")
except Exception as e:
    coin_sound = None
    print(f"Failed to load coin.mp3: {e}")

try:
    game_over_sound = pygame.mixer.Sound(r"C:\Users\ae\OneDrive\Desktop\New folder\fail.wav")
    game_over_sound.set_volume(0.6)
    print("Loaded fail.wav successfully")
except Exception as e:
    game_over_sound = None
    print(f"Failed to load fail.wav: {e}")

try:
    win_sound = pygame.mixer.Sound(r"C:\Users\ae\OneDrive\Desktop\New folder\win.mp3")
    win_sound.set_volume(0.6)
    print("Loaded win.mp3 successfully")
except Exception as e:
    win_sound = None
    print(f"Failed to load win.mp3: {e}")

try:
    clap_sound = pygame.mixer.Sound(r"C:\Users\ae\OneDrive\Desktop\New folder\clap.wav")
    clap_sound.set_volume(0.5)
    print("Loaded clap.wav successfully")
except Exception as e:
    clap_sound = None
    print(f"Failed to load clap.wav: {e}")

def get_sea_color():
    if level == 1:
        return (0, 180, 200)  # أزرق فيروزي
    elif level == 2:
        return (0, 100, 180)  # أزرق عميق
    else:
        return (20, 50, 120)  # أزرق جليدي

def get_floor_color():
    if level == 1:
        return SAND_FLOOR_COLOR
    elif level == 2:
        return CORAL_FLOOR_COLOR
    else:
        return ICE_FLOOR_COLOR

def lerp_color(color1, color2, t):
    r = int(color1[0] + (color2[0] - color1[0]) * t)
    g = int(color1[1] + (color2[1] - color1[1]) * t)
    b = int(color1[2] + (color2[2] - color1[2]) * t)
    a = int(color1[3] + (color2[3] - color1[3]) * t) if len(color1) == 4 else 255
    return (r, g, b, a) if len(color1) == 4 else (r, g, b)

def get_sky_color():
    global time_counter
    time_counter += 0.005
    phase = (math.sin(time_counter) + 1) / 2
    day_sky = (135, 206, 235)
    night_sky = (20, 20, 50)
    return lerp_color(day_sky, night_sky, phase)

def get_sun_moon_color():
    phase = (math.sin(time_counter) + 1) / 2
    return lerp_color(SUN_COLOR, MOON_COLOR, phase)

def draw_sun_moon():
    phase = (math.sin(time_counter) + 1) / 2
    center = (width - 100, 100)
    base_color = get_sun_moon_color()
    glow_layers = 10 if phase < 0.5 else 5
    max_radius = 80 if phase < 0.5 else 60
    for i in range(glow_layers):
        radius = 50 + i * (max_radius - 50) / glow_layers
        alpha = int(100 * (1 - i / glow_layers) * (1 - phase if phase < 0.5 else phase))
        glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*base_color, alpha), (radius, radius), radius)
        screen.blit(glow_surface, (center[0] - radius, center[1] - radius))
    pygame.draw.circle(screen, base_color, center, 50)

def draw_stars():
    phase = (math.sin(time_counter) + 1) / 2
    alpha = int(255 * phase)
    for star in stars:
        radius = star[2] + math.sin(pygame.time.get_ticks() * 0.01 + star[0]) * 0.5
        star_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(star_surface, (*STAR_COLOR, alpha), (5, 5), int(radius))
        screen.blit(star_surface, (star[0] - 5, star[1] - 5))

def draw_clouds():
    phase = (math.sin(time_counter) + 1) / 2
    if phase < 0.5:
        for cloud in clouds:
            cloud[0] -= cloud[3]
            if cloud[0] < -cloud[2]*2:
                cloud[0] = width + cloud[2]*2
                cloud[1] = random.randint(50, 150)
            
            cloud_surface = pygame.Surface((cloud[2]*3, cloud[2]*2), pygame.SRCALPHA)
            pygame.draw.ellipse(cloud_surface, CLOUD_COLOR, (0, cloud[2]*0.5, cloud[2]*2, cloud[2]))
            pygame.draw.ellipse(cloud_surface, CLOUD_COLOR, (cloud[2]*0.5, 0, cloud[2], cloud[2]*0.8))
            pygame.draw.ellipse(cloud_surface, CLOUD_COLOR, (cloud[2]*1.5, 0, cloud[2], cloud[2]*0.8))
            pygame.draw.ellipse(cloud_surface, CLOUD_COLOR, (cloud[2]*0.2, cloud[2]*0.8, cloud[2]*0.8, cloud[2]*0.8))
            pygame.draw.ellipse(cloud_surface, CLOUD_COLOR, (cloud[2]*1.0, cloud[2]*0.8, cloud[2]*0.8, cloud[2]*0.8))
            highlight = pygame.Surface((cloud[2]*3, cloud[2]*2), pygame.SRCALPHA)
            pygame.draw.ellipse(highlight, (255, 255, 255, 30), (cloud[2]*0.2, cloud[2]*0.2, cloud[2]*1.6, cloud[2]*0.8))
            cloud_surface.blit(highlight, (0, 0))
            screen.blit(cloud_surface, (cloud[0] - cloud[2], cloud[1] - cloud[2]*0.5))

def draw_sea_floor():
    floor_color = get_floor_color()
    pygame.draw.rect(screen, floor_color, (0, height - 50, width, 50))
    if level == 1:
        for i in range(10):
            star_x = random.randint(0, width)
            star_y = height - random.randint(10, 40)
            pygame.draw.polygon(screen, (255, 150, 150), [
                (star_x, star_y), (star_x + 5, star_y + 15),
                (star_x + 20, star_y + 15), (star_x + 7, star_y + 22),
                (star_x + 10, star_y + 35), (star_x, star_y + 25),
                (star_x - 10, star_y + 35), (star_x - 7, star_y + 22),
                (star_x - 20, star_y + 15), (star_x - 5, star_y + 15)
            ])
    elif level == 2:
        for i in range(8):
            coral_x = random.randint(0, width)
            coral_y = height - random.randint(20, 50)
            pygame.draw.ellipse(screen, (255, 120, 120), (coral_x - 20, coral_y, 40, 20))
            pygame.draw.ellipse(screen, (255, 150, 150), (coral_x - 10, coral_y - 20, 20, 30))
    else:
        for i in range(5):
            crack_x = random.randint(0, width)
            crack_y = height - random.randint(10, 40)
            pygame.draw.line(screen, (150, 170, 200), (crack_x - 20, crack_y), (crack_x + 20, crack_y), 3)

def draw_waves():
    if level == 1:
        wave_height = 15
        wave_speed = 0.005
        for x in range(0, width, 6):
            y = height // 2 + math.sin(x * 0.02 + pygame.time.get_ticks() * wave_speed) * wave_height
            pygame.draw.line(screen, (255, 255, 255, 200), (x, y), (x, y + 5), 2)
            pygame.draw.line(screen, (0, 100, 150), (x, y + 5), (x, height), 4)
    elif level == 2:
        wave_height = 25
        wave_speed = 0.008
        for x in range(0, width, 5):
            y = height // 2 + math.sin(x * 0.03 + pygame.time.get_ticks() * wave_speed) * wave_height
            pygame.draw.line(screen, (255, 255, 255, 220), (x, y - 5), (x, y + 5), 3)
            pygame.draw.line(screen, (0, 80, 150), (x, y + 5), (x, height), 5)
            if random.random() < 0.1:
                splash_y = y - random.randint(5, 15)
                pygame.draw.circle(screen, (255, 255, 255, 180), (x, splash_y), 3)
    else:
        wave_height = 10
        wave_speed = 0.002
        for x in range(0, width, 10):
            y = height // 2 + math.sin(x * 0.015 + pygame.time.get_ticks() * wave_speed) * wave_height
            pygame.draw.line(screen, (200, 220, 255, 200), (x, y), (x, y + 10), 4)
            pygame.draw.line(screen, (50, 80, 150), (x, y + 10), (x, height), 6)
            if random.random() < 0.05:
                crack_y = y + random.randint(0, 10)
                pygame.draw.line(screen, (150, 170, 200), (x - 5, crack_y), (x + 5, crack_y), 2)

def draw_end_waves():
    wave_height = 10
    for x in range(0, width, 10):
        y = height // 2 + math.sin(x * 0.015 + pygame.time.get_ticks() * 0.002) * wave_height
        pygame.draw.line(screen, (0, 0, 255, 100), (x, y), (x, height), 3)

def draw_bubbles():
    global bubbles
    bubble_count = 100 if level == 1 else 70 if level == 2 else 30
    bubble_size = (2, 10) if level != 2 else (4, 12)
    while len(bubbles) < bubble_count:
        bubbles.append([random.randint(0, width), height, random.randint(*bubble_size), random.uniform(1, 3)])
    for bubble in bubbles[:]:
        bubble[1] -= bubble[3]
        bubble_surface = pygame.Surface((bubble[2] * 2, bubble[2] * 2), pygame.SRCALPHA)
        pygame.draw.circle(bubble_surface, BUBBLE_COLOR, (bubble[2], bubble[2]), bubble[2])
        pygame.draw.circle(bubble_surface, BUBBLE_SHINE_COLOR, (bubble[2] - bubble[2] * 0.3, bubble[2] - bubble[2] * 0.3), bubble[2] * 0.3)
        screen.blit(bubble_surface, (bubble[0] - bubble[2], bubble[1] - bubble[2]))
        if bubble[1] < height // 2:
            bubbles.remove(bubble)

def draw_sea_particles():
    global sea_particles
    if level == 1:
        particle_color = SAND_COLOR
        particle_count = 30
        particle_size = (2, 5)
    elif level == 2:
        particle_color = CORAL_COLOR
        particle_count = 15
        particle_size = (5, 10)
    else:
        particle_color = ICE_COLOR
        particle_count = 20
        particle_size = (3, 7)
    while len(sea_particles) < particle_count:
        sea_particles.append([
            random.randint(0, width),
            random.randint(height // 2, height),
            random.uniform(-1, 1),
            random.uniform(-1.5, -0.5),
            random.randint(*particle_size)
        ])
    for particle in sea_particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 0.05
        if particle[4] <= 0 or particle[1] < height // 2:
            sea_particles.remove(particle)
        else:
            particle_surface = pygame.Surface((particle[4] * 2, particle[4] * 2), pygame.SRCALPHA)
            if level == 2:
                pygame.draw.rect(particle_surface, particle_color, (0, 0, particle[4] * 2, particle[4]))
            else:
                pygame.draw.circle(particle_surface, particle_color, (particle[4], particle[4]), particle[4])
            screen.blit(particle_surface, (particle[0] - particle[4], particle[1] - particle[4]))

def draw_fog():
    if level == 3:
        fog_surface = pygame.Surface((width, height // 2), pygame.SRCALPHA)
        fog_surface.fill(FOG_COLOR)
        screen.blit(fog_surface, (0, height // 2))

def draw_small_fish():
    global small_fish
    for fish in small_fish:
        fish[0] += fish[2]
        if fish[0] < 0 or fish[0] > width:
            fish[2] = -fish[2]
        
        fish_surface = pygame.Surface((30, 15), pygame.SRCALPHA)
        pygame.draw.ellipse(fish_surface, SMALL_FISH_COLOR, (0, 0, 20, 10))
        pygame.draw.polygon(fish_surface, SMALL_FISH_COLOR, [(20, 5), (30, 0), (30, 10)])
        pygame.draw.circle(fish_surface, (0, 0, 0), (5, 3), 2)
        
        if fish[2] > 0:
            screen.blit(fish_surface, (fish[0] - 15, fish[1] - 7))
        else:
            screen.blit(pygame.transform.flip(fish_surface, True, False), (fish[0] - 15, fish[1] - 7))

def draw_shadow(x, y, width, height, scale):
    shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surface, SHADOW_COLOR, (0, 0, width, height))
    scaled_shadow = pygame.transform.scale(shadow_surface, (width * scale, height * scale))
    screen.blit(scaled_shadow, (x - width * scale // 2 + 10, y - height * scale // 2 + 10))

def draw_fish(x, y, angle, scale):
    draw_shadow(x, y, 60, 40, scale)
    base_surface = pygame.Surface((80, 50), pygame.SRCALPHA)
    
    pygame.draw.ellipse(base_surface, FISH_COLOR, (0, 0, 60, 40))
    pygame.draw.arc(base_surface, FISH_STRIPE_COLOR, (5, 5, 50, 30), 0, math.pi, 2)
    pygame.draw.arc(base_surface, FISH_STRIPE_COLOR, (10, 10, 40, 20), 0, math.pi, 2)
    
    highlight = pygame.Surface((60, 40), pygame.SRCALPHA)
    pygame.draw.ellipse(highlight, (*FISH_SHINE_COLOR, 80), (10, 5, 40, 20))
    base_surface.blit(highlight, (0, 0))
    
    fin_angle = math.sin(pygame.time.get_ticks() * 0.01) * 10
    tail_points = [(60, 20), (80, 20 - fin_angle), (90, 20), (80, 20 + fin_angle)]
    dorsal_points = [(30, 0), (40, -10 + fin_angle*0.5), (50, 0)]
    ventral_points = [(30, 40), (40, 50 + fin_angle*0.5), (50, 40)]
    pygame.draw.polygon(base_surface, FISH_COLOR, tail_points)
    pygame.draw.polygon(base_surface, FISH_COLOR, dorsal_points)
    pygame.draw.polygon(base_surface, FISH_COLOR, ventral_points)
    
    pygame.draw.circle(base_surface, (0, 0, 0), (15, 15), 5)
    pygame.draw.circle(base_surface, (255, 255, 255), (16, 14), 2)
    pygame.draw.circle(base_surface, (255, 255, 255, 100), (10, 10), 3)
    
    scaled_surface = pygame.transform.scale(base_surface, (80 * scale, 50 * scale))
    rotated_surface = pygame.transform.rotate(scaled_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(x, y))
    screen.blit(rotated_surface, rotated_rect)

def draw_shark(x, y, shake_offset, angle):
    draw_shadow(x + shake_offset, y, 140, 60, 1.0)
    body_surface = pygame.Surface((180, 100), pygame.SRCALPHA)
    
    body_rect = pygame.Rect(20, 20, 140, 60)
    pygame.draw.ellipse(body_surface, SHARK_COLOR, body_rect)
    
    belly_rect = pygame.Rect(30, 30, 120, 40)
    pygame.draw.ellipse(body_surface, SHARK_BELLY_COLOR, belly_rect)
    
    tail_points = [
        (160, 50), (180, 30), (185, 50),
        (180, 70), (160, 50)
    ]
    pygame.draw.polygon(body_surface, SHARK_FIN_COLOR, tail_points)
    
    dorsal_fin = [
        (100, 10), (110, -5), (120, 10)
    ]
    pygame.draw.polygon(body_surface, SHARK_FIN_COLOR, dorsal_fin)
    
    pectoral_fin = [
        (70, 50), (60, 70), (80, 60), (90, 55)
    ]
    pygame.draw.polygon(body_surface, SHARK_FIN_COLOR, pectoral_fin)
    
    eye_pos = (45, 40)
    pygame.draw.circle(body_surface, (0, 0, 0), eye_pos, 6)
    pygame.draw.circle(body_surface, (255, 255, 255), (eye_pos[0]+2, eye_pos[1]-2), 2)
    
    mouth_points = [
        (35, 60), (50, 65), (65, 63)
    ]
    pygame.draw.lines(body_surface, (0, 0, 0), False, mouth_points, 2)
    
    for i in range(3):
        tooth_top = [(40+i*15, 62), (45+i*15, 58), (50+i*15, 62)]
        pygame.draw.polygon(body_surface, (255, 255, 255), tooth_top)
    
    for i in range(3):
        start_pos = (30, 45 + i*8 - 8)
        end_pos = (40, 45 + i*8 - 8)
        pygame.draw.line(body_surface, (130, 170, 210), start_pos, end_pos, 2)
    
    highlight = pygame.Surface((180, 100), pygame.SRCALPHA)
    pygame.draw.ellipse(highlight, (255, 255, 255, 60), (30, 25, 120, 40))
    body_surface.blit(highlight, (0, 0))
    
    rotated_surface = pygame.transform.rotate(body_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=(x + shake_offset, y))
    screen.blit(rotated_surface, rotated_rect)

def draw_blood_particles():
    global blood_particles
    for particle in blood_particles[:]:
        particle[0] += particle[2]
        particle[1] += particle[3]
        particle[4] -= 0.1
        if particle[4] <= 0:
            blood_particles.remove(particle)
        else:
            pygame.draw.circle(screen, BLOOD_COLOR, (int(particle[0]), int(particle[1])), int(particle[4]))

def draw_glow_particles():
    global glow_particles
    for particle in glow_particles[:]:
        particle[1] -= particle[3]
        particle[4] -= 0.05
        if particle[4] <= 0:
            glow_particles.remove(particle)
        else:
            particle_surface = pygame.Surface((particle[4] * 2, particle[4] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, COIN_COLOR, (particle[4], particle[4]), particle[4])
            screen.blit(particle_surface, (particle[0] - particle[4], particle[1] - particle[4]))

def move_shark():
    global shark_x, shark_y, fish_x, fish_y, shark_angle
    dx = fish_x - shark_x
    dy = fish_y - shark_y
    distance = math.sqrt(dx**2 + dy**2)
    if distance > 20:
        shark_x += (dx / distance) * shark_speed
        shark_y += (dy / distance) * shark_speed
        shark_angle = -math.degrees(math.atan2(dy, dx)) + 180

def check_collision():
    global game_over, flash_timer, shark_shake, blood_particles
    fish_rect = pygame.Rect(fish_x - 20 * fish_scale, fish_y - 20 * fish_scale, 40 * fish_scale, 40 * fish_scale)
    shark_rect = pygame.Rect(shark_x - 70, shark_y - 30, 140, 60)
    if fish_rect.colliderect(shark_rect):
        game_over = True
        flash_timer = 60
        shark_shake = 15
        for _ in range(20):
            blood_particles.append([
                fish_x, fish_y,
                random.uniform(-3, 3),
                random.uniform(-3, 3),
                random.randint(5, 15)
            ])
        if game_over_sound:
            game_over_sound.play()
        pygame.mixer.music.fadeout(1000)

def check_win():
    global win, flash_timer, level, shark_speed, glow_particles
    score_target = 100 if level == 1 else 200
    if score >= score_target:
        win = True
        flash_timer = 60
        for _ in range(30):
            glow_particles.append([
                width // 2, height // 2,
                random.uniform(-2, 2),
                random.uniform(-3, -1),
                random.randint(5, 10)
            ])
        if win_sound:
            win_sound.play()
        if clap_sound:
            clap_sound.play()

def reset_level():
    global fish_x, fish_y, shark_x, shark_y, score, coins, shark_speed, game_over, win, flash_timer, shark_shake, blood_particles, fish_angle, shark_angle, fish_scale, glow_particles, sea_particles, bubbles
    fish_x, fish_y = width // 4, height // 2
    shark_x, shark_y = width - 100, height // 2
    fish_angle = 0
    shark_angle = 0
    fish_scale = 1.0
    score = 0
    coins = [[random.randint(0, width), random.randint(height // 2, height)] for _ in range(6)]
    shark_speed = 1.2 if level == 1 else 1.5
    game_over = False
    win = False
    flash_timer = 0
    shark_shake = 0
    blood_particles = []
    glow_particles = []
    sea_particles = []
    bubbles = [[random.randint(0, width), random.randint(height // 2, height), random.randint(2, 10), random.uniform(1, 3)] for _ in range(100 if level == 1 else 70 if level == 2 else 30)]
    pygame.mixer.music.play(-1)

def draw_win_background():
    gradient_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(100):
        alpha = int(50 * (1 - i / 100))
        pygame.draw.rect(gradient_surface, (*GLOW_COLOR[:3], alpha), (0, i * height // 100, width, height // 100))
    screen.blit(gradient_surface, (0, 0))

def main():
    global fish_x, fish_y, score, game_over, coins, shark_x, shark_y, shark_speed, flash_timer, shark_shake, level, win, fish_angle, fish_scale
    try:
        pygame.mixer.music.load(r"C:\Users\ae\OneDrive\Desktop\New folder\see.mp3")
        pygame.mixer.music.set_volume(0.8)  # Corrected to valid range (0.0 to 1.0)
        pygame.mixer.music.play(-1)
        print("Loaded see.mp3 successfully with volume 0.8")
    except Exception as e:
        print(f"Failed to load see.mp3: {e}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_over and not win:
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] and fish_x > 20:
                fish_x -= fish_speed
                dx = -1
            if keys[pygame.K_RIGHT] and fish_x < width - 20:
                fish_x += fish_speed
                dx = 1
            if keys[pygame.K_UP] and fish_y > height // 2:
                fish_y -= fish_speed
                dy = -1
            if keys[pygame.K_DOWN] and fish_y < height - 20:
                fish_y += fish_speed
                dy = 1
            if dx != 0 or dy != 0:
                fish_angle = -math.degrees(math.atan2(dy, dx)) + 180

            move_shark()
            check_collision()

            fish_rect = pygame.Rect(fish_x - 20 * fish_scale, fish_y - 20 * fish_scale, 40 * fish_scale, 40 * fish_scale)
            for coin in coins[:]:
                coin_rect = pygame.Rect(coin[0] - 10, coin[1] - 10, 20, 20)
                if fish_rect.colliderect(coin_rect):
                    coins.remove(coin)
                    score += 10
                    fish_scale = min(fish_scale + 0.05, 1.5)
                    coins.append([random.randint(0, width), random.randint(height // 2, height)])
                    if coin_sound:
                        coin_sound.play()
                    check_win()

        screen.fill(get_sky_color())
        draw_stars()
        draw_clouds()
        pygame.draw.rect(screen, get_sea_color(), (0, height // 2, width, height // 2))
        draw_sea_floor()
        draw_fog()
        draw_waves()
        draw_bubbles()
        draw_sea_particles()
        draw_small_fish()
        draw_sun_moon()

        if game_over:
            draw_blood_particles()

        if not game_over:
            draw_fish(fish_x, fish_y, fish_angle, fish_scale)

        for coin in coins:
            radius = 10 + math.sin(pygame.time.get_ticks() * 0.01 + coin[0]) * 2
            pygame.draw.circle(screen, COIN_COLOR, (coin[0], coin[1]), int(radius))

        shark_offset = math.sin(pygame.time.get_ticks() * 0.1) * shark_shake if shark_shake > 0 else 0
        draw_shark(shark_x, shark_y, shark_offset, shark_angle)
        if shark_shake > 0:
            shark_shake -= 0.5

        score_text = font.render(f"Score: {score} | Level: {level}", True, (255, 255, 255))
        score_rect = score_text.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, (0, 0, 0, 100), score_rect.inflate(10, 10))
        screen.blit(score_text, score_rect)

        if game_over:
            draw_end_waves()
            if flash_timer > 0:
                alpha = int(220 * (flash_timer / 60))
                fade_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                fade_surface.fill((*(get_sea_color()), alpha))
                screen.blit(fade_surface, (0, 0))
                flash_timer -= 1
            text_scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.005) * 0.1
            game_over_text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
            shadow_text = font.render("Game Over! Press R to Restart", True, (0, 0, 0))
            scaled_surface = pygame.transform.scale(game_over_text, (int(game_over_text.get_width() * text_scale), int(game_over_text.get_height() * text_scale)))
            scaled_shadow = pygame.transform.scale(shadow_text, (int(shadow_text.get_width() * text_scale), int(shadow_text.get_height() * text_scale)))
            game_over_rect = scaled_surface.get_rect(center=(width // 2, height // 2))
            shadow_rect = scaled_shadow.get_rect(center=(width // 2 + 5, height // 2 + 5))
            screen.blit(scaled_shadow, shadow_rect)
            screen.blit(scaled_surface, game_over_rect)
            if keys[pygame.K_r]:
                reset_level()
                level = 1

        if win:
            draw_win_background()
            draw_glow_particles()
            if flash_timer > 0:
                radius = (60 - flash_timer) * 10
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                for i in range(10):
                    alpha = int(100 * (1 - i / 10))
                    pygame.draw.circle(glow_surface, (*GLOW_COLOR[:3], alpha), (radius, radius), radius - i * (radius / 10))
                screen.blit(glow_surface, (width // 2 - radius, height // 2 - radius))
                flash_timer -= 1
                for _ in range(5):
                    if random.random() < 0.3:
                        glow_particles.append([
                            random.randint(width // 2 - 150, width // 2 + 150),
                            random.randint(height // 2 - 100, height // 2 + 100),
                            random.uniform(-1, 1),
                            random.uniform(-2, -0.5),
                            random.randint(3, 8)
                        ])
            text_scale = 1.0 + math.sin(pygame.time.get_ticks() * 0.005) * 0.1
            win_text = font.render(f"You Win! Press R to Level {level + 1}", True, (0, 255, 0))
            shadow_text = font.render(f"You Win! Press R to Level {level + 1}", True, (0, 0, 0))
            scaled_surface = pygame.transform.scale(win_text, (int(win_text.get_width() * text_scale), int(win_text.get_height() * text_scale)))
            scaled_shadow = pygame.transform.scale(shadow_text, (int(shadow_text.get_width() * text_scale), int(shadow_text.get_height() * text_scale)))
            win_rect = scaled_surface.get_rect(center=(width // 2, height // 2))
            shadow_rect = scaled_shadow.get_rect(center=(width // 2 + 5, height // 2 + 5))
            screen.blit(scaled_shadow, shadow_rect)
            screen.blit(scaled_surface, win_rect)
            if keys[pygame.K_r]:
                level += 1
                reset_level()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()