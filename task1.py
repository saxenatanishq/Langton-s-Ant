import pygame
import random
import math
import time

blocksize = 10 #size of each block of the grid
# Since the gridspace was to be kept infinity, so here I have used a margin to determine the distance between the end of the grid and the visible space
margin = 100
# To make sure that the ant does not get spawned at the corner of the screen, I have added some padding
padding = 20
starting_probability = 0.8
decay_frames = 5

class Ant:
    def __init__(self, screen,arr):
        x_blocks = screen.get_width()//blocksize
        y_blocks = screen.get_height()//blocksize
        self.direction = math.floor(random.random()*4) + 1 # The initial direction of the ant is random
        self.x = random.randint(padding , x_blocks - 1 - padding) # Random spawn location of the ant
        self.y = random.randint(padding , y_blocks - 1 - padding) # Random spawn location of the ant
         
    def move_forward(self):
        if self.direction == 1: # up
            self.y -= 1
        elif self.direction == 2: # right
            self.x += 1
        elif self.direction == 3: # down
            self.y += 1
        else: # left
            self.x -= 1
    
    
    def move(self, index):
        def change_direction(clockwise):
            if clockwise == 1: # if the direction is to be changed in clockwise direction
                self.direction = (self.direction + 1) % 4
            else: # if the driection is to be changed in anti clockwise direction
                self.direction = (self.direction - 1) % 4
        
        if index == 1: # depending on the color of the block, this function is called to change the direction of the ant
            change_direction(-1)
        else:
            change_direction(1)
        
        self.move_forward()   

        

class App:
    def __init__(self):
        pygame.display.set_caption("Langton's Ant")
        pygame.init()
        self.screen = pygame.display.set_mode((720, 720)) #sceeen size
        self.clock = pygame.time.Clock()
        self.running = True
        x_blocks = self.screen.get_width()//blocksize  # number of blocks visible on screen
        y_blocks = self.screen.get_height()//blocksize # number of blocks visible on screen
        
        # initialising a 2D array to mark every block of the grid (not only the blocks visible on screen)
        # The three parameters of a block are [color(1==black, 0==white), probability, ant number linked to that probabiltiy (ant1 or ant2)]
        self.arr = [[[0,0,0] for _ in range(x_blocks + 2*margin)] for __ in range(y_blocks + 2*margin)]  
        self.ant1 = Ant(self.screen, self.arr)
        self.ant2 = Ant(self.screen, self.arr)
        self.font = pygame.font.SysFont(None, 30)

    def drawgrid(self):
        for x in range(0, self.screen.get_width(), blocksize):
            for y in range(0, self.screen.get_height(), blocksize):
                rect = pygame.Rect(x, y, blocksize, blocksize)
                if self.arr[margin + x//blocksize][margin + y//blocksize][0] == 1:
                    # if the block is black
                    pygame.draw.rect(self.screen, "black", rect)
                else:
                    # if the block is a default white block
                    pygame.draw.rect(self.screen, "gray", rect,1)
                
                # to show the current position of the ant 1
                ant1_rect = pygame.Rect(self.ant1.x * blocksize, self.ant1.y * blocksize, blocksize, blocksize)
                pygame.draw.rect(self.screen, "red", ant1_rect)

                # to show the current position of the ant 2
                ant2_rect = pygame.Rect(self.ant2.x * blocksize, self.ant2.y * blocksize, blocksize, blocksize)
                pygame.draw.rect(self.screen, "blue", ant2_rect)

    # function to update the porbabilities of each block (to decay the probabilites linearly over time)
    def update_probabilities(self):
        for i in range(len(self.arr)):
            for j in range(len(self.arr[i])):
                if self.arr[i][j][1] > 0:
                    self.arr[i][j][1] -= starting_probability/decay_frames
                else:
                    self.arr[i][j][1] = 0


    def run(self):
        frame_count = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            for ant in [self.ant1, self.ant2]:
                if ant == self.ant1:
                    ant_no = 1
                else:
                    ant_no = 2
                
                # To make sure that the ants have not crossed the infinity line (Although it is very rare that anything like this will happen because the ants are very far away from the edge, which depends on the margin)
                grid_x = margin + ant.x
                grid_y = margin + ant.y
                if 0 <= grid_x < len(self.arr) and 0 <= grid_y < len(self.arr):
                    num, p, ant_num = self.arr[margin + ant.x][margin + ant.y]
                    current_x = ant.x
                    current_y = ant.y
                    if p==0:
                        # if p is 0, i.e. there is no pheremone their on that block, then the ant will move normally
                        ant.move(num)
                    else:
                        if ant_no != ant_num:
                            # If the current ant is not the same as the pheremone owner ant then the probabilites get reversed
                            p = 1-p

                        if random.random() < p:
                            # The ant skips that block and moves forward
                            ant.move_forward()
                        else:
                            # The ant follows the standard turning rule ignoring the pheremone
                            ant.move(num)
                    
                    # updating the block through which the ant passed through
                    self.arr[margin + current_x][margin + current_y] = [(num+1)%2, starting_probability, ant_no]
                else:
                    # In case (very rarely) if the ant crosses the infinity border line, then it will get resawned at the centre of the screen
                    ant.x, ant.y = self.screen.get_width()//2 , self.screen.get_height()//2
            
            
            self.screen.fill("white")
            self.drawgrid()
            self.update_probabilities()
            
            # To print the frames elapsed at the top left corner of the screen
            frame_text = self.font.render(f"Frames: {frame_count}", True, "black")
            self.screen.blit(frame_text, (10, 10))
            
            pygame.display.flip()
            self.clock.tick(10)
            frame_count += 1

        pygame.quit()

if __name__ == "__main__":
    app = App()
    app.run()