'''
Program Name: Space Adventure
Developpers: Veer and Justin 
Purpose: To create a 2d alien shooter (Rules explained in the game)
'''

import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

width = 500
height = 500
fps = 60

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
current_time = pygame.time.get_ticks()
mob_time = pygame.time.get_ticks()
attack_time = pygame.time.get_ticks()

#Function that draws text onto the screen
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
  font = pygame.font.Font(font_name, size)
  text_surface = font.render(text, True, white)
  text_rect = text_surface.get_rect()
  text_rect.midtop = (x,y)
  surf.blit(text_surface, text_rect)

#Similar to the draw text function, but this helps with drawing the player's lives
def draw_lives(surf, x, y, lives, img):
  for i in range(lives):
    img_rect = img.get_rect()
    space_gap = 5
    img_rect.x = x + ((img_rect.width+space_gap)*i)
    img_rect.y = y
    surf.blit(img, img_rect)

#Loading images
main_character = pygame.image.load(path.join(img_dir, "space.png")).convert()
laser = pygame.image.load(path.join(img_dir, "laserGreen11.png")).convert()
enemy = pygame.image.load(path.join(img_dir, "space-ship.png")).convert()
heart = pygame.image.load(path.join(img_dir, "heart.png")).convert()
heart = pygame.transform.scale(heart, (40, 34))
heart.set_colorkey(white)
bomb = pygame.image.load(path.join(img_dir, "bomb.png")).convert()
enemy_2 = pygame.image.load(path.join(img_dir, "alien.png")).convert()
background = pygame.image.load(path.join(img_dir, "space11.png")).convert()
background =pygame.transform.scale(background, (400, 400))
background_rect = background.get_rect()

#loading sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot.wav"))
bound_sound = pygame.mixer.Sound(path.join(snd_dir, "Pickup_Coin21.wav"))
press_sound = pygame.mixer.Sound(path.join(snd_dir, "Blip_Select10.wav"))
game_over_sound = pygame.mixer.Sound(path.join(snd_dir, "Lose_sound.wav"))
game_over_sound.set_volume(1.5)

expl_sounds = []
for snd in ["Explosion.wav", "Explosion8.wav"]:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.2)

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['llg'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (85, 85))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (65, 65))
    explosion_anim['sm'].append(img_sm)
    img_sm = pygame.transform.scale(img, (90, 90))
    explosion_anim['llg'].append(img_sm)

#Creates player; controls movement and shooting; and sets up basic characteristics about the player
class player(pygame.sprite.Sprite):
  def __init__(self): #Initializes the player and creates the main character
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(main_character,(120, 100))
    self.image.set_colorkey(black)
    self.rect = self.image.get_rect()
    self.rect.centerx = width/2
    self.rect.bottom = height - 10
    self.speed = 0
    self.lives = 3


  def update(self): #Updates main characters position based on user input
    self.speed = 0
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_LEFT]:
      self.speed = - 7
    if keystate[pygame.K_RIGHT]:
      self.speed = 7
    if self.rect.right > width:
      self.rect.right = width
    if self.rect.left < 0:
      self.rect.left = 0

    self.rect.x += self.speed

  def shoot(self): #Controls the shooting mechanics of the player
    bullet_init = bullet(self.rect.centerx, self.rect.top)
    all_sprites.add(bullet_init)
    bullets.add(bullet_init)
    shoot_sound.play()


#Sets up basic characteristics for bullets (movement, position, speed)
class bullet(pygame.sprite.Sprite):
  def __init__(self, x, y): #Spawns bullet and sets up characteristics
    pygame.sprite.Sprite.__init__(self)
    self.image = laser
    self.image.set_colorkey(black)
    #self.image = pygame.Surface((10, 20))
    #self.image.fill(yellow)
    self.rect = self.image.get_rect()
    self.rect.bottom = y
    self.rect.centerx = x
    self.speedy = -10
    self.switch = 'up'

  def update(self): #Controls bullet speed and rebound mechanics

    if self.switch == 'up':
      self.rect.y += self.speedy
    if self.switch == 'down':
      self.rect.y -= self.speedy
    if self.rect.y <= 10:
      self.switch = 'down'
      bound_sound.play()
    if self.rect.y > height:
      expl = explosion(self.rect.center, 'lg')
      all_sprites.add(expl)
      self.kill()




#Creates basic alien mob and sets up it's various characteristics
class mob(pygame.sprite.Sprite):
  def __init__(self): #Creates basic alien mob
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(enemy,(50, 38))
    self.image.set_colorkey(black)
    self.rect = self.image.get_rect()
    self.rect.x = random.randrange(-100, -40)
    self.rect.y = random.randrange(height-200)
    self.speed = random.randrange(1, 5)

  def update(self): #Controls it's behaviour
    self.rect.x += self.speed
    if self.rect.left > width + 20:
      self.rect.x = random.randrange(-100, -40)
      self.rect.y = random.randrange(height - 200)
      self.speed = random.randrange(1, 5)

#Creates alien mob that attacks player
class attack_mob(pygame.sprite.Sprite):
  def __init__(self): #Spwans in attack mob
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(bomb,(50, 38))
    self.image.set_colorkey(black)
    self.rect = self.image.get_rect()
    self.rect.x = random.randrange(width-30)
    self.rect.y = random.randrange(-100, -40)
    self.speed = random.randrange(1, 3)

  def update(self): #Controls attack mob behaviour
    self.rect.y += self.speed
    if self.rect.top > height-5:
      expl = explosion(self.rect.center, 'lg')
      all_sprites.add(expl)
    if self.rect.top > height+30:
      self.rect.x = random.randrange(width-30)
      self.rect.y = random.randrange(-100, -40)
      self.speed = random.randrange(1, 3)

#Creates a mob that bounces of of walls
class special_mob(pygame.sprite.Sprite):
  def __init__(self): #Spawns in mob
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(enemy_2,(80, 68))
    self.image.set_colorkey(black)
    self.rect = self.image.get_rect()
    self.rect.x = random.randrange(-100, -40)
    self.rect.y = random.randrange(height-200)
    self.speed = 4
    self.switch = 'right'


  def update(self): #Controls the mob's behaviour
    if self.switch == 'right':
      self.rect.x += self.speed
    if self.switch == 'left':
      self.rect.x -= self.speed
    if self.rect.x >= width-10:
      self.switch = 'left'
    if self.rect.x <= 10:
      self.switch = 'right'

class explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.rect.center = center
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
  screen.fill(black)
  screen.blit(background, background_rect)
  draw_text(screen, "Space Adventure", 64, width / 2, height / 4)
  draw_text(screen, "Arrow Keys To Move, Space to Fire", 22, width / 2, height / 2)
  draw_text(screen, "Press any key to begin and 1 for the rules", 18, width / 2, height * 3 / 4)
  pygame.display.flip()
  waiting = True
  while waiting:
      clock.tick(fps)
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
          if event.type == pygame.KEYDOWN:
              press_sound.play()
              waiting = False
              if event.key == pygame.K_1:
                  press_sound.play()
                  rules()

def end_screen(score):
  screen.fill(black)
  screen.blit(background, background_rect)
  draw_text(screen, "Game Over", 64, width / 2, height / 4)
  draw_text(screen, "Final Score: "+ str(score), 64, width / 2, height / 2)
  draw_text(screen, "Press enter to return to the start screen and 1 for the rules", 18, width / 2, height * 3 / 4)
  pygame.display.flip()
  waiting = True
  while waiting:
      clock.tick(fps)
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_RETURN:
                waiting = False
              if event.key == pygame.K_1:
                rules()
                end_screen(score)

def rules():
  screen.fill(black)
  screen.blit(background, background_rect)
  draw_text(screen, "Rules:", 64, width / 2, height / 4)
  draw_text(screen, "Press 2 to to start the game", 24, width / 2, height - 80)
  draw_text(screen, "Press Spacebar to shoot and use the arrow keys to control player movement", 16, width/2, height /4 + 80 )
  draw_text(screen, "Bullets bounce, so don't get hit by it, or you'll lose a life", 16, width/2, height /4 + 120 )
  draw_text(screen, "If you get hit by a bomb you'll also lose a life", 16, width/2, height /4 + 160 )
  draw_text(screen, "Score depends on the speed of the alien, faster ones will give you higher score", 16, width/2, height /4 + 200 )
  draw_text(screen, "The game will end when your lives reach zero", 16, width/2, height /4 + 240 )
  1
  pygame.display.flip()
  waiting = True
  while waiting:
      clock.tick(fps)
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_2:
                waiting = False


game_over = True
game_end = False
running = True
while running:
    if game_over:
      show_go_screen()
      all_sprites = pygame.sprite.Group()
      mobs = pygame.sprite.Group()
      bullets = pygame.sprite.Group()
      player_var = player()
      all_sprites.add(player_var)

      #Starts the spawning process for the basic alien mob by adding it to it's group
      for i in range(5):
        m = mob()
        all_sprites.add(m)
        mobs.add(m)
      pygame.mixer.music.play(loops=-1)
      score = 0
      temp_score = 0
      delay = 2000
      game_over = False

    if game_end:
      end_screen(score)
      game_end = False
      game_over = True

    # keep loop running at the right speed
    clock.tick(fps)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        #Checks if user wants to shoot, and calls shoot function
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            player_var.shoot()


    #spawns special mob
    if mob_time == 0 or current_time-mob_time > 4000:
      chance = random.randrange(1, 10)
      if chance > 7:
        spec_mob = special_mob()
        all_sprites.add(spec_mob)
        mobs.add(spec_mob)
        mob_time = pygame.time.get_ticks()


    if temp_score > 50:
      if delay > 1000:
        temp_score -=50
        delay -= 300
    #spawns attack mob
    if attack_time == 0 or current_time-attack_time > delay:
      att_mob = attack_mob()
      all_sprites.add(att_mob)
      mobs.add(att_mob)
      attack_time = pygame.time.get_ticks()

    # Update
    all_sprites.update()

    #check if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
      score += hit.speed
      temp_score += hit.speed
      random.choice(expl_sounds).play()
      expl = explosion(hit.rect.center, 'sm')
      all_sprites.add(expl)
      m = mob()
      all_sprites.add(m)
      mobs.add(m)

    #check if mob hit player
    hits = pygame.sprite.spritecollide(player_var, mobs, True)

    #Controls the reduction of lives in the case of collisions
    for hit in hits:
      #if hits:
      player_var.lives -=1
      expl = explosion(hit.rect.center, 'lg')
      all_sprites.add(expl)
      random.choice(expl_sounds).play()
      if player_var.lives == 0:
        expl = explosion(hit.rect.center, 'llg')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        game_over_sound.play()
        game_end = True

    #Checks for any hits between the player and it's bullets
    hits = pygame.sprite.spritecollide(player_var, bullets, True)
    if hits:
      for hit in hits:
        player_var.lives -= 1
        expl = explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
      if player_var.lives == 0:
        expl = explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        game_over_sound.play()
        game_end = True
    # Draw / render
    screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, 'Score: '+ str(score) , 30, width/2, 7)
    draw_lives(screen, width-150, 5, player_var.lives, heart)
    # *after* drawing everything, flip the display
    pygame.display.flip()
    current_time = pygame.time.get_ticks()

#Graphics


pygame.quit()
