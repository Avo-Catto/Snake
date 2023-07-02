import pygame, sys, random, time
from pygame.locals import *

class main:
    def __init__(self):
        self.window_size = (800, 800)
        self.run = True
        self.snake = [[(255, 255, 255), (400, 400), "N"], [(255, 255, 255), (400, 440), "N"]] # color, position, dirction
        self.speed = self.tilesize = 40
        self.fps = 1
        self.direction = "N"
        self.points = 0
        self.point_add = 10
        self.temp_points = self.points
        self.tile_coords = [(400, 440)]
        self.available_coords = [i for i in range(0, 760, self.tilesize)]
        self.berry_coords = (random.choice(self.available_coords), random.choice(self.available_coords))
        self.mountains = []
        self.pressed = False

        pygame.init()
        self.window_setup()
        self.game_loop()

    
    def window_setup(self):
        self.window = pygame.display.set_mode((self.window_size))
        pygame.display.set_caption("Snake - by AVCDO")
    

    def draw(self):
        # clear screen
        self.window.fill((0, 0, 0))

        # draw berry
        pygame.draw.rect(self.window, color=(255,0,0), rect=pygame.Rect(self.berry_coords[0], self.berry_coords[1], self.tilesize, self.tilesize))

        # draw snake tiles
        for tile in self.snake:
            pygame.draw.rect(self.window, color=tile[0], rect=pygame.Rect(tile[1][0], tile[1][1], self.tilesize, self.tilesize))
        
        # draw mountains
        for mountain in self.mountains:
            pygame.draw.rect(self.window, color=(120,120,120), rect=pygame.Rect(mountain[0], mountain[1], self.tilesize, self.tilesize))
        
        # points
        self.window.blit(pygame.font.Font("./PixeloidSans-nR3g1.ttf", 20).render(f"Pts: {self.points}", False, (255,255,0)), (10, 10))
    

    def update(self):
        self.pressed = False
        
        # direction
        if self.direction == "N":
            direction_coords = [0, -40]
        elif self.direction == "S":
            direction_coords = [0, +40]
        elif self.direction == "W":
            direction_coords = [-40, 0]
        elif self.direction == "O":
            direction_coords = [+40, 0]
        else:
            pass

        # check for collisions
        if self.berry_coords == self.snake[0][1]:

            self.berry_coords = (random.choice(self.available_coords), random.choice(self.available_coords))
            while self.berry_coords in self.tile_coords or self.berry_coords in self.mountains:
                self.berry_coords = (random.choice(self.available_coords), random.choice(self.available_coords))

            self.points += self.point_add
            self.snake.insert(-1, [(255, 255, 255), (self.snake[-1][1][0], self.snake[-1][1][1]), self.snake[-1][2]])

        if self.snake[0][1][0] < 0 or self.snake[0][1][0] > self.window_size[0] - self.tilesize or self.snake[0][1][1] < 0 or self.snake[0][1][1] > self.window_size[1] - self.tilesize or self.snake[0][1] in self.tile_coords or self.snake[0][1] in self.mountains:
            self.reset()
        
        # update snake
        self.snake.insert(0, [self.snake[-1][0], (self.snake[0][1][0] + direction_coords[0], self.snake[0][1][1] + direction_coords[1]), self.direction])
        self.snake.pop(-1)
        
        # update colliding data
        self.tile_coords.clear()
        for tile in self.snake:
            self.tile_coords.append(tile[1])
        self.tile_coords.pop(0)


    def reset(self):
        self.snake = [[(255, 255, 255), (400, 400), "N"], [(255, 255, 255), (400, 440), "N"]]
        self.direction = "N"
        self.points = 0
        self.temp_points = 0
        self.tile_coords = [(400, 440)]
        self.fps = 1
        self.berry_coords = (random.choice(self.available_coords), random.choice(self.available_coords))
        self.mountains = []
        self.pressed = False
        time.sleep(3)
    

    def difficult(self):
        if self.points - self.temp_points == 50:
            self.temp_points = self.points
            self.fps += 1
            mountain_coords = (random.choice(self.available_coords), random.choice(self.available_coords))
            while mountain_coords in self.tile_coords or mountain_coords in self.berry_coords:
                mountain_coords = (random.choice(self.available_coords), random.choice(self.available_coords))
            self.mountains.append(mountain_coords)


    def game_loop(self):
        clock = pygame.time.Clock()

        while self.run:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and self.direction != "S" and not self.pressed:
                        self.direction = "N"
                        self.pressed = True
                    if event.key == pygame.K_s and self.direction != "N" and not self.pressed:
                        self.direction = "S"
                        self.pressed = True
                    if event.key == pygame.K_a and self.direction != "O" and not self.pressed:
                        self.direction = "W"
                        self.pressed = True
                    if event.key == pygame.K_d and self.direction != "W" and not self.pressed:
                        self.direction = "O"
                        self.pressed = True
            
            self.update()
            self.difficult()
            self.draw()
            pygame.display.flip()
            
            clock.tick(self.fps)
            

main()
