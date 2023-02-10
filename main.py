import pygame
import sys
from time import sleep

pygame.init()
screen = pygame.display.set_mode((720,720))
square_size = (16, 16)
square_image = pygame.Surface(square_size)
square_image.fill((255, 255, 255))


#■
"""
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

def create_field(x: int, y: int) -> list:
    return [[0 for i in range(x)] for i in range(y)]

def populate_field(field: list, coords: list) -> list:
    for i in coords:
        field[i[0]][i[1]] = 1
    return field

def draw_field(field: list, x_len: int, y_len: int):
    screen.fill((0,0,0))
    screen.blit(back_image, (0,0))
    for y in range(y_len):
        for x in range(x_len):
            if field[x][y] == 1:
                screen.blit(square_image, (x*square_size[0], y*square_size[1]))
    pygame.display.update()

def gameLoop(field: list):
    tick_time = 0.1
    all_dead = False
    alive_count = 0
    near_count = 0
    x_len = len(field[0])
    y_len = len(field)
    draw_field(field, x_len, y_len)
    #begins to check cells
    while not all_dead:
        sleep(tick_time)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
        coord_storage = [] #[x, y, 0 or 1]
        alive_count = 0
        for y in range(y_len):
            for x in range(x_len):
                near_count = 0
                if x < x_len-1 and field[x+1][y] == 1:
                    near_count += 1
                if x > 0 and field[x-1][y] == 1:
                    near_count += 1
                if y < y_len-1 and field[x][y+1] == 1:
                    near_count += 1
                if y > 0 and field[x][y-1] == 1:
                    near_count += 1
                    
                if x < x_len-1 and y < y_len-1 and field[x+1][y+1] == 1:
                    near_count += 1
                if x > 0 and y > 0 and field[x-1][y-1] == 1:
                    near_count += 1
                if x > 0 and y < y_len-1 and field[x-1][y+1] == 1:
                    near_count += 1
                if x < x_len-1 and y > 0 and field[x+1][y-1] == 1:
                    near_count += 1
                            
                            
                if near_count < 2:
                    coord_storage.append([x, y, 0])
                elif near_count == 2 and field[x][y] == 1:
                    coord_storage.append([x, y, 1])
                    alive_count += 1
                elif near_count == 3:
                    coord_storage.append([x, y, 1])
                    alive_count += 1
                elif near_count > 3:
                    coord_storage.append([x, y, 0])
        for i in coord_storage:
            field[i[0]][i[1]] = i[2]
        if alive_count == 0:
            all_dead = True
        draw_field(field, x_len, y_len)
        

def main():
    global back_image
    try:
        field_size = int(sys.argv[1])
    except Exception as error:
        field_size = 20
        print(error)
        
    back_image = pygame.Surface((square_size[0]*field_size, square_size[1]*field_size))
    back_image.fill((20,20,20))
    #creates a 2d field with list comprehension
    field = create_field(field_size, field_size)
    #square
    #field = populate_field(field, [[0, 0], [1,0], [0,1], [1,1]])
    #bar
    #field = populate_field(field, [[0,1], [1,1], [2,1]])
    #ship
    field = populate_field(field, [[1,1], [3,1], [2,2], [3,2], [2,3]])
    
    gameLoop(field)
    return
    

if __name__ == "__main__":
    main()