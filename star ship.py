import sys
import pygame
import random
import pygame.time
import os


pygame.init()

screen_width=1200
screen_height=800
bg_color=(37,7,107)
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Star ship')
clock = pygame.time.Clock()

class Ship:
    def __init__(self,screen):
        self.screen=screen
        self.screen_rect=screen.get_rect()
        image_path=os.path.join(os.path.dirname(__file__), 'images\ship1.bmp')
        self.original_image=pygame.image.load(image_path)
        scaled_width = 90
        scaled_height = 180 
        self.image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
        self.rect=self.image.get_rect()
        self.rect.midbottom=self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        self.angle=0


    def rotate(self,angle):
        self.angle=angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)   
    
    def reset_position(self):
        self.image = pygame.transform.scale(self.original_image, (90, 180))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle = 0
        pygame.time.delay(0)

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.rect.x += 10
        if self.moving_left and self.rect.left>0:
            self.rect.x -= 10
        if self.moving_up and self.rect.top>0:
            self.rect.y -= 10
        if self.moving_down and self.rect.bottom<self.screen_rect.bottom:
            self.rect.y += 10

    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Star:
    def __init__(self, screen):
        self.screen = screen
        self.rect = pygame.Rect(0, 0, 20, 20)  
        self.rect.x = random.randint(20, screen_width - self.rect.width)  
        self.rect.y = random.randint(150, screen_height - self.rect.height)  

    def blitme(self):
        pygame.draw.rect(self.screen, (255, 178, 102), self.rect)  

class Counter:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)  
        self.star_count = 0

    def star_number(self):
        self.star_count += 1
    
    def reset_counter(self):
        self.star_count = 0

    def blitme(self):
        text = self.font.render(f'Stars: {self.star_count}', True, (255, 255, 0))
        self.screen.blit(text, (10, 30))

class Message:
    def __init__(self,screen):
        self.screen=screen
        self.font=pygame.font.Font(None, 40)
        
    def blitme(self):
        text_1=self.font.render('Your time is over!', True, (255, 255, 255))
        text_2=self.font.render('The game will restart in 5 sec!', True, (255,0,0))
        self.screen.blit(text_1, (10, 60))
        self.screen.blit(text_2, (10, 90))
    

text_message=Message(screen)

counter_text=Counter(screen)

stars = [Star(screen) for star in range(30)]

ship=Ship(screen)

running=True 
game_over=False
start_time = pygame.time.get_ticks()
elapsed_time = 0

while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) // 1000
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
                ship.rotate(-90)
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
                ship.rotate(90)
            elif event.key == pygame.K_DOWN:
                ship.moving_down = True
                ship.rotate(180)
            elif event.key == pygame.K_UP:
                ship.moving_up = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
                ship.reset_position()
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False
                ship.reset_position()
            elif event.key == pygame.K_DOWN:
                ship.moving_down = False
                ship.reset_position()
            elif event.key == pygame.K_UP:
                ship.moving_up = False
                ship.reset_position()

    for star in stars:
        if ship.rect.colliderect(star.rect):  
            counter_text.star_number()
            stars.remove(star)
            new_star = Star(screen)  
            stars.append(new_star)

    ship.update()
    screen.fill(bg_color)
    for star in stars:
        star.blitme()
    ship.blitme()
    counter_text.blitme()
    font = pygame.font.SysFont('Calibri', 20, True, False)
    text = font.render(f'Time: {elapsed_time} sec', True, (255, 255, 255))
    screen.blit(text, (10, 10))

    if elapsed_time >= 60 and game_over==False:
        text_message.blitme()
        game_over=True
    
    pygame.display.flip()
    clock.tick(60)

    if game_over:
        pygame.time.delay(5000)
        game_over=False
        start_time = pygame.time.get_ticks()  
        counter_text.reset_counter()


    
   

