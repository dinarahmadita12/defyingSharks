import pygame
import abc
import sys
import random
import pickle
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Defying Shark")

# Load sounds
main_sound = pygame.mixer.Sound('sounds/background.mp3')
coin_sound = pygame.mixer.Sound('sounds/coin.mp3')
game_over_sound = pygame.mixer.Sound('sounds/game_over.mp3')
start_sound = pygame.mixer.Sound('sounds/start.mp3')
button_sound = pygame.mixer.Sound('sounds/but.mp3')
teriak_sound = pygame.mixer.Sound('sounds/teriak.mp3')
makanhiu_sound = pygame.mixer.Sound('sounds/hiumakan.mp3')

# Load images
background_img = pygame.image.load('assets/background.png')
start_img = pygame.image.load('assets/start.png')
about_img = pygame.image.load('assets/about.png')
shop_img = pygame.image.load('assets/shop.png')
dark_theme = pygame.image.load('assets/bg1.png')
light_theme = pygame.image.load('assets/bg2.png')
#eve_theme = pygame.image.load('assets/bg3.png')
#night_theme = pygame.image.load('assets/bg4.png')
gameover_img = pygame.image.load('assets/gameover.png')
back_img = pygame.image.load('assets/back.png')  # Tambahkan baris ini
desc_img = pygame.image.load('assets/desc.png')

#HUD images
coin_icon = pygame.image.load('assets/coin1.png')
heart_icon = pygame.image.load('assets/heart.png')
restart_img = pygame.image.load('assets/restart.png')
exit_img = pygame.image.load('assets/exit.png')
pause_img = pygame.image.load('assets/pause.png')
play_img = pygame.image.load('assets/play.png')
musik_img = pygame.image.load('assets/musik.png')
unmusik_img = pygame.image.load('assets/unmusik.png')

# Animation frames
swimmer_frames = [pygame.image.load(f'assets/{i}.png') for i in range(1, 14)]
shark_frames = [pygame.image.load(f'assets/hiu{i}.png') for i in range(1, 4)]
coin_frames = [pygame.image.load(f'assets/coin{i}.png') for i in range(1, 6)]

# Scale images
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
desc_img = pygame.transform.scale(desc_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_img = pygame.transform.scale(start_img, (200, 100))
about_img = pygame.transform.scale(about_img, (200, 100))
shop_img = pygame.transform.scale(shop_img, (200, 100))
dark_theme = pygame.transform.scale(dark_theme, (SCREEN_WIDTH, SCREEN_HEIGHT))
light_theme = pygame.transform.scale(light_theme, (SCREEN_WIDTH, SCREEN_HEIGHT))
swimmer_frames = [pygame.transform.scale(img, (110, 110)) for img in swimmer_frames]
shark_frames = [pygame.transform.scale(img, (110, 115)) for img in shark_frames]
coin_frames = [pygame.transform.scale(img, (30, 30)) for img in coin_frames]
coin_icon = pygame.transform.scale(coin_icon, (30, 30))
heart_icon = pygame.transform.scale(heart_icon, (30, 30))
restart_img = pygame.transform.scale(restart_img, (200, 100))
exit_img = pygame.transform.scale(exit_img, (200, 100))
back_img = pygame.transform.scale(back_img, (70, 70))  # Tambahkan baris ini
pause_img = pygame.transform.scale(pause_img, (50,50))
play_img = pygame.transform.scale(play_img, (50,50))
button_img = pause_img
musik_img = pygame.transform.scale(musik_img, (50,50))
unmusik_img = pygame.transform.scale(unmusik_img, (50,50))
vol_img = musik_img

# MUSIK
is_muted=False
# Setup audio
swim_sound = pygame.mixer.Sound('sounds/swim.mp3')

# Fungsi untuk mute audio
def mute_audio():
    swim_sound.set_volume(0)

# Fungsi untuk unmute audio
def unmute_audio():
    swim_sound.set_volume(1)

# Fungsi untuk membuat tombol
def create_button(image_path):
    vol_img = pygame.image.load(image_path)
    # Sesuaikan ukuran gambar dengan ukuran 50x50
    vol_img = pygame.transform.scale(vol_img, (50, 50))
    return vol_img

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

#PAUSED
button_rect = button_img.get_rect(topright=(SCREEN_WIDTH, 50))
button_rect = button_img.get_rect()
button_rect.topright = (SCREEN_WIDTH - 10, 10)
is_paused = False

vol = pygame.image.load('assets/musik.png')
vol = pygame.transform.scale(vol, (50, 50))  # Mengubah ukuran gambar menjadi 50x50
vol_rect = vol.get_rect(topright=(SCREEN_WIDTH-10, 60))  # Atur posisi kanan atas sesuai kebutuhan
is_muted = False

font = pygame.font.SysFont(None, 48)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Button class
class Button:
    main_sound.play()
    def __init__(self, image, x, y, action=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = action

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        screen.blit(self.image, (self.rect.x, self.rect.y))

        if self.rect.collidepoint(mouse_pos):
            if click[0] == 1 and self.action is not None:
                self.action()
                start_sound.play()

class Music(abc.ABC):
    def __init__(self):
        self.music_playing = False

    @abc.abstractmethod
    def play_background_music(self):
        pass

    @abc.abstractmethod
    def stop_background_music(self):
        pass

    @abc.abstractmethod
    def play_coin_sound(self):
        pass

    @abc.abstractmethod
    def play_game_over_sound(self):
        pass

class MusicPlayer(Music):
    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.music_button = pygame.Rect(SCREEN_WIDTH - 70, 10, 60, 60)
        self.music_img = musik_img
        self.unmusic_img = unmusik_img
        self.vol_img = self.music_img  # Inisialisasi vol_img dengan music_img

    def play_background_music(self):
        pygame.mixer.music.load('sounds/background.mp3')
        pygame.mixer.music.play(-1)
        self.music_playing = True

    def stop_background_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False

    def play_coin_sound(self):
        coin_sound.play()

    def play_game_over_sound(self):
        game_over_sound.play()

    def toggle_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.vol_img = self.unmusic_img  # Update vol_img ketika musik di pause
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.vol_img = self.music_img  # Update vol_img ketika musik di play

    def draw(self, screen):
        screen.blit(self.vol_img, (SCREEN_WIDTH - 70, 10))  # Menggunakan vol_img untuk menggambar tombol musik

# Initialize MusicPlayer
music_player = MusicPlayer()

# Start playing the music at the beginning
music_player.play_background_music()

# Actions for buttons
def toggle_music():
    music_player.toggle_music()

def start_game():
    music_player.play_background_music()
    game_loop()

def open_shop():
    music_player.play_background_music()
    shop_loop()

def show_about():
    music_player.play_background_music()
    about_loop()

def toggle_sound():
    if music_player.music_playing:
        music_player.stop_background_music()
    else:
        music_player.play_background_music()

# Actions
current_background = None

def save_theme(theme):
    with open('selected_theme.pkl', 'wb') as file:
        pickle.dump(theme, file)

def load_theme():
    try:
        with open('selected_theme.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None

def save_total_coins(total_coins):
    with open('total_coins.pkl', 'wb') as file:
        pickle.dump(total_coins, file)

def load_total_coins():
    try:
        with open('total_coins.pkl', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return 0

def start_game():
    start_sound.play()
    game_loop()

def open_shop():
    button_sound.play()
    shop_loop()

def show_about():
    button_sound.play()
    about_loop()

def restart_game():
    button_sound.play()
    game_loop()

def exit_to_menu():
    button_sound.play
    main_menu()

# Create buttons for the main menu
start_button = Button(start_img, 300, 150, start_game)
shop_button = Button(shop_img, 300, 300, open_shop)
about_button = Button(about_img, 300, 450, show_about)

# Create buttons for the game over screen
restart_button = Button(restart_img, 300, 350, restart_game)
exit_button = Button(exit_img, 300, 450, exit_to_menu)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = swimmer_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.animation_time = 0.1
        self.current_time = 0
        self.moving = True
        self.is_muted = False

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def update(self):
         if self.moving:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                self.rect.x += 5
            if keys[pygame.K_UP]:
                self.rect.y -= 5
            if keys[pygame.K_DOWN]:
                self.rect.y += 5

        # Keep player on screen
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT

            # Update animation
            self.current_time += 1 / 60
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

    def pause_movement(self):
        self.moving = False

    def resume_movement(self):
        self.moving = True

# Enemy class (Shark)
class Shark(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = shark_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(4, 5)
        self.animation_time = 0.1
        self.current_time = 0
        self.moving = True
        self.is_muted = False

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause() 

    def update(self):
         if self.moving:
            self.rect.y += self.speed
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randint(-100, -40)
                self.speed = random.randint(2, 3)

            # Update animation
            self.current_time += 1 / 60
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
    
    def pause_movement(self):
        self.moving = False

    def resume_movement(self):
        self.moving = True

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = coin_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(2, 4)
        self.animation_time = 0.1
        self.current_time = 0
        self.movement = True 
        self.is_muted = False
        
    def toggle_mute(self):
        self.is_muted = not self.is_muted
        if self.is_muted:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def update(self):
        if self.movement:
            self.rect.y += self.speed
            if self.rect.top > SCREEN_HEIGHT:
                self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randint(-100, -40)
                self.speed = random.randint(3, 8)

            # Update animation
            self.current_time += 1 / 60
            if self.current_time >= self.animation_time:
                self.current_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]

    def pause_movement(self):
        self.movement = False

    def resume_movement(self):
        self.movement = True

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self._image = heart_icon  # Ubah heart_frames menjadi heart_icon
        self._rect = self._image.get_rect()
        self._rect.x = random.randint(0, SCREEN_WIDTH - self._rect.width)
        self._rect.y = random.randint(-100, -40)
        self._speed = 3  # Kecepatan tetap
        self._movement = True 
        self._is_muted = False

    def update(self):
        if self._movement:
            self._rect.y += self._speed
            if self._rect.top > SCREEN_HEIGHT:
                self._rect.x = random.randint(0, SCREEN_WIDTH - self._rect.width)
                self._rect.y = random.randint(-100, -40)

    # Enkapsulasi method untuk mengontrol pergerakan
    def pause_movement(self):
        self._movement = False

    def resume_movement(self):
        self._movement = True

    # Getter dan Setter untuk atribut yang mungkin perlu diakses dari luar
    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    @property
    def movement(self):
        return self._movement

    @movement.setter
    def movement(self, value):
        self._movement = value

    @property
    def is_muted(self):
        return self._is_muted

    @is_muted.setter
    def is_muted(self, value):
        self._is_muted = value

# Game over screen
def game_over_screen(coin_count):
    total_coins = load_total_coins() + coin_count
    save_total_coins(total_coins)
    
    running = True
    while running:
        screen.blit(gameover_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        font = pygame.font.Font(None, 74)
        text_surface = font.render("Game telah berakhir", True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        screen.blit(text_surface, text_rect)

        coin_surface = font.render(f"Coins collected: {coin_count}", True, WHITE)
        coin_rect = coin_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(coin_surface, coin_rect)

        restart_button.draw(screen)
        exit_button.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.rect.collidepoint(event.pos):
                    restart_button.action()
                    running = False
                if exit_button.rect.collidepoint(event.pos):
                    exit_button.action()
                    running = False

    main_menu()

# Game loop
def game_loop():
    global is_paused
    global button_img
    current_background = load_theme()
    background_y = 0
    background_speed = 2
    player = Player()
    sharks = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    hearts_group = pygame.sprite.Group()
    hearts = 4
    coin_count = 0
    level = 1  # Inisialisasi level
    level_up_timer = 0  # Timer untuk level up
    LEVEL_UP_TIME = 600  # Setiap 10 detik (60 frame/detik * 10 detik)
    is_paused = False
    button_img = pause_img 
    is_muted = False
    music_player = MusicPlayer()

    # Tambahkan koin dan hiu secara bertahap pada level 1
    if level == 1:
        # Tentukan jumlah koin yang akan muncul berdasarkan level
        num_coins = random.randint(level * 1, level * 2)  # Random antara 1-2 koin pada level 1, 2-4 koin pada level 2, dan seterusnya
        for _ in range(num_coins):
            coins.add(Coin())
        
        num_sharks = random.randint(level * 1, level * 2)  # Random antara 1-2 hiu pada level 1, 2-4 hiu pada level 2, dan seterusnya
        for _ in range(num_sharks):
            sharks.add(Shark())

    all_sprites = pygame.sprite.Group(player, *sharks, *coins, *hearts_group)
    clock = pygame.time.Clock()

    coin_spawn_timer = 0
    COIN_SPAWN_INTERVAL = 180  # Koin akan muncul setiap 3 detik (60 frame/detik * 3 detik)
    heart_spawn_timer = 0
    HEART_SPAWN_INTERVAL = 480  # Nyawa akan muncul setiap 8 detik (60 frame/detik * 8 detik)

    # Initialize unmute image and rect
    unvol_img = pygame.image.load('assets/unmusik.png')
    unvol_img = pygame.transform.scale(unvol_img, (50, 50))
    unvol_rect = unvol_img.get_rect(topright=(SCREEN_WIDTH-70, 10))

    # Mulai audio
    swim_sound.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    button_sound.play()
                    if is_paused:
                        # Resume game
                        is_paused = False
                        button_img = pause_img  # Change button to pause.png
                        # Resume movement of all sprites
                        player.resume_movement()
                        for shark in sharks:
                            shark.resume_movement()
                        for coin in coins:
                            coin.resume_movement()
                    else:
                        # Pause game
                        is_paused = True
                        button_img = play_img  # Change button to play.png
                        # Pause movement of all sprites
                        player.pause_movement()
                        for shark in sharks:
                            shark.pause_movement()
                        for coin in coins:
                            coin.pause_movement()
                elif event.type == MOUSEBUTTONDOWN:
                    if music_player.music_button.collidepoint(event.pos):
                        music_player.toggle_music()

        if not is_paused:
            all_sprites.update()

            # Spawn coin
            coin_spawn_timer += 1
            if coin_spawn_timer >= COIN_SPAWN_INTERVAL:
                coin_spawn_timer = 0
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)

            # Spawn heart
            heart_spawn_timer += 1
            if heart_spawn_timer >= HEART_SPAWN_INTERVAL:
                heart_spawn_timer = 0
                new_heart = Heart()
                hearts_group.add(new_heart)
                all_sprites.add(new_heart)

            # Check for collisions
            if pygame.sprite.spritecollide(player, sharks, False):
                teriak_sound.play()
                makanhiu_sound.play()
                hearts -= 1
                if hearts == 0:
                    game_over_screen(coin_count)
                    return
                else:
                    print("Hit! Hearts left:", hearts)
                pygame.sprite.spritecollide(player, sharks, True)

            coins_collected = pygame.sprite.spritecollide(player, coins, True)
            if coins_collected:
                coin_sound.play()
                coin_count += len(coins_collected)
                print("Coins collected:", coin_count)

            hearts_collected = pygame.sprite.spritecollide(player, hearts_group, True)
            if hearts_collected:
                button_sound.play()
                hearts += len(hearts_collected)
                print("Hearts collected:", hearts)

            # Update level timer
            level_up_timer += 1
            if level_up_timer >= LEVEL_UP_TIME:
                level_up_timer = 0
                level += 1
                print("Level up! Current level:", level)
                for _ in range(level):  # Tambahkan hiu sebanyak level saat ini
                    sharks.add(Shark())
                all_sprites.add(*sharks)

                # Update jumlah koin dan interval kemunculannya berdasarkan level baru
                num_coins = random.randint(level * 1, level * 2)
                COIN_SPAWN_INTERVAL = 60 * 3  # Reset interval menjadi 3 detik
                coin_spawn_timer = 0  # Reset timer spawn koin
                for _ in range(num_coins):
                    new_coin = Coin()
                    coins.add(new_coin)
                    all_sprites.add(new_coin)

            # Draw
            if current_background == 'dark':
                screen.blit(dark_theme, (0, background_y))
            elif current_background == 'light':
                screen.blit(light_theme, (0, background_y))

            # Gambar latar belakang kedua di atas latar belakang pertama
            if current_background == 'dark':
                screen.blit(dark_theme, (0, background_y - dark_theme.get_height()))
            elif current_background == 'light':
                screen.blit(light_theme, (0, background_y - light_theme.get_height()))

            # Update posisi latar belakang
            background_y += background_speed

            # Kembalikan posisi latar belakang ke atas layar jika mencapai batas bawah
            if background_y >= SCREEN_HEIGHT:
                background_y = 0


        all_sprites.draw(screen)

        # Draw HUD
        for i in range(hearts):
            screen.blit(heart_icon, (10 + i * 35, 10))
        screen.blit(coin_icon, (10, 50))
        font = pygame.font.Font(None, 36)
        coin_text = font.render(f": {coin_count}", True, WHITE)
        screen.blit(coin_text, (50, 50))
        
        # Display current level
        level_text = font.render(f"Level: {level}", True, WHITE)
        screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

        screen.blit(button_img, button_rect.topleft)
        if is_paused:
            draw_text("PAUSED", font, (255, 0, 0), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        if not is_muted:
            screen.blit(music_player.vol_img, vol_rect)  # Menggunakan vol_img dari music_player
        else:
            screen.blit(unvol_img, unvol_rect)

        pygame.display.flip()
        clock.tick(60)

    main_menu()


def shop_loop():
    total_coins = load_total_coins()
    current_theme = load_theme()

    def set_dark_theme():
        global current_background
        current_background = dark_theme
        save_theme('dark')

    def set_light_theme():
        global current_background
        current_background = light_theme
        save_theme('light')

    def buy_light_theme():
        nonlocal total_coins
        nonlocal current_theme

        if current_theme != 'light' and total_coins >= 100:
            total_coins -= 100
            save_total_coins(total_coins)
            save_theme('light')
            current_theme = 'light'
            current_background = light_theme

    def back_to_main_menu():
        main_menu()

    dark_button = Button(pygame.transform.scale(dark_theme, (200, 100)), 150, 250, set_dark_theme)
    light_button = Button(pygame.transform.scale(light_theme, (200, 100)), 450, 250, set_light_theme)
    buy_button = Button(pygame.Surface((100, 50)), 350, 400, buy_light_theme)
    back_button = Button(back_img, 10, 10, back_to_main_menu)

    running = True
    while running:
        if current_background:
            screen.blit(current_background, (0, 0))
        else:
            screen.blit(background_img, (0, 0))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if buy_button.rect.collidepoint(event.pos):
                    buy_light_theme()

        pygame.draw.rect(screen, (0, 255, 0), buy_button.rect)

        font = pygame.font.Font(None, 36)
        if current_theme == 'light':
            theme_status = font.render("Owned", True, ORANGE)
        else:
            theme_status = font.render("Costs 100 coins", True, ORANGE)
        screen.blit(theme_status, (330, 470))

        # Draw "Buy" text above the green button
        buy_text = font.render("Buy", True, WHITE)
        screen.blit(buy_text, (buy_button.rect.centerx - buy_text.get_width() / 2, buy_button.rect.centery - buy_text.get_height() / 2))

        total_coins_text = font.render(f"Total Coins: {total_coins}", True, WHITE)
        screen.blit(total_coins_text, (SCREEN_WIDTH - total_coins_text.get_width() - 10, 10))

        dark_button.draw(screen)
        light_button.draw(screen)

        back_button.draw(screen)

        pygame.display.flip()

    main_menu()

# About loop
def about_loop():
    current_background = load_theme()

    def back_to_main_menu():
        main_menu()

    # Create the back button
    back_button = Button(back_img, 10, 10, back_to_main_menu) 

    running = True
    while running:
        if current_background == 'dark':
            screen.blit(dark_theme, (0, 0))
        elif current_background == 'light':
            screen.blit(light_theme, (0, 0))
        else:
            screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(desc_img, (0, 0))

        back_button.draw(screen)

        pygame.display.flip()

    main_menu()

# Main menu loop
def main_menu():
    total_coins = load_total_coins()
    
    running = True
    while running:
        screen.blit(background_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        start_button.draw(screen)
        shop_button.draw(screen)
        about_button.draw(screen)

        # Display total coins in the top right corner
        font = pygame.font.Font(None, 36)
        total_coins_text = font.render(f"Total Coins: {total_coins}", True, WHITE)
        screen.blit(total_coins_text, (SCREEN_WIDTH - total_coins_text.get_width() - 10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Start the main menu
if __name__ == "__main__":
    main_menu()