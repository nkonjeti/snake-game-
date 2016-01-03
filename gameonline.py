import pygame
import os
import random

 
# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)


# Set the width and height of each snake segment.
segment_width = 15
segment_height = 15


# Margin between each segment.
segment_margin = 3


# Set initial speed.
x_change = segment_width + segment_margin
y_change = 0
screen = pygame.display.set_mode((800, 600))
score = 0
strike = 0
fail = 0

class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """
    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super(Segment, self).__init__()
 
        # Set height, width
        self.image = pygame.Surface((segment_width, segment_height))
        self.image.fill(WHITE)


        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Food(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super(Food, self).__init__()
        self.image = pygame.image.load(os.path.join('/Users/muralikonjeti/Downloads', 'applesprite.png'))
        apple_width = 20
        apple_height = 20
        self.image = pygame.transform.scale(self.image, (apple_width, apple_height))

       
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        
# This automatically sets the rect to be the same size as your image.
# Call this function so the Pygame library can initialize itself
pygame.init()

def boostrap_snake():
    num_snake_segments = 15
    new_all_sprites_list = pygame.sprite.Group()
    new_snake_segments = []
    for i in range(num_snake_segments):
        x = 250 - (segment_width + segment_margin) * i
        y = 30
        segment = Segment(x, y)
        new_snake_segments.append(segment)
        new_all_sprites_list.add(segment)
    return new_all_sprites_list, new_snake_segments

allspriteslist, snake_segments = boostrap_snake()

snakefoodlist = pygame.sprite.Group()
food = Food(300,30)
snakefoodlist.add(food)


clock = pygame.time.Clock()
done = False
 

while not done:
    collision = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

    # Check if head of snake collides with any other segment in snake list.
    for snake_segment in snake_segments[:]:
        if pygame.sprite.collide_rect(snake_segments[3], snake_segment):
            score = 0 

            
   
    # Collision code.
    food_hit_list = pygame.sprite.spritecollide(food, allspriteslist, False)
    # If food_hit_list exists there was a collision. so we add new Food,
    
    if food_hit_list:
        score += 10
        snakefoodlist.remove(food)
        collision = True

        # Figure out where new segment will be
        x = snake_segments[0].rect.x + 18
        y = snake_segments[0].rect.y
        segment = Segment(x, y)

        # Insert new segment into the list
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)


        # Create new food segment at different place on grid.
        food = Food(random.randint(0, 800), random.randint(0, 600))
        snakefoodlist.add(food)


    display_caption = 'Snake Game                   Score = %s' % score 
    # Set the title of the window
    pygame.display.set_caption(display_caption)


    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    old_segment = snake_segments.pop()
    allspriteslist.remove(old_segment)
 
    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change
    segment = Segment(x, y)
 
    # Insert new segment into the list
    snake_segments.insert(0, segment)
    allspriteslist.add(segment)

    
    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)
 
    allspriteslist.draw(screen)
    snakefoodlist.draw(screen)
 
    # Flip screen
    pygame.display.flip()
 
    # Pause
    clock.tick(100)

pygame.quit()