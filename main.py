import pygame as pg
import sys
import time

# 2 or 3 == Live
# < 2 == Die
# > 3 == Die



pg.init()

SCREEN = pg.display.set_mode((720,720))
SCREEN.fill((60,60,60))

camera_pos = [0, 0]


TICK_TIME = 0.1
game_state = False

CELL_SIZE = (16, 16)
args = sys.argv
if len(args) > 1:
    for i in range(len(sys.argv)):
        if type(args[i]) == str and len(args[1]) > 0 and args[i][0] == '-':
            if args[i] == '-t':
                try:
                    TICK_TIME = float(args[i+1])
                except:
                    print("Could not recognize arguments of '-t'")
            if args[i] == '-p':
                try:
                    CELL_SIZE = (int(args[i+1]), int(args[i+2]))
                except:
                    print("Could not recognize arguments of '-p'")
cell_image = pg.Surface(CELL_SIZE)
cell_image.fill((255,255,255))     

 
def abs(n):
    if n < 0:
        return n*-1
    else:
        return n

 
def cell_draw(coord_list):
    SCREEN.fill((60,60,60))
    global cell_image
    global camera_pos
    for coord in coord_list:
        SCREEN.blit(cell_image, (coord[0]*CELL_SIZE[0] - camera_pos[0], coord[1]*CELL_SIZE[1] - camera_pos[1]))
    pg.display.update()

def game_cycle(coord_list: list) -> list:
    #map that holds coords touched by cells
    heat_map = []
    
    for coord in coord_list:
        heat_map.append([coord[0]+1, coord[1]])
        heat_map.append([coord[0]-1, coord[1]])
        heat_map.append([coord[0], coord[1]+1])
        heat_map.append([coord[0], coord[1]-1])
        heat_map.append([coord[0]+1, coord[1]+1])
        heat_map.append([coord[0]-1, coord[1]-1])
        heat_map.append([coord[0]+1, coord[1]-1])
        heat_map.append([coord[0]-1, coord[1]+1])
    #heat_map calculations
    life_coords = [] #coordinates of live cells of cycle
    while len(heat_map) > 0:
        occur = heat_map.count(heat_map[0]) #number of ocurrence of a coordinate
        #filters by the living condition
        if occur == 2 and heat_map[0] in coord_list:
            life_coords.append(heat_map[0])
        if occur == 3:
            life_coords.append(heat_map[0])
        #cleans already swept coords
        buffer = heat_map[0]
        for i in range(occur):
            heat_map.remove(buffer)
    return life_coords


def game_loop(coord_list):
    global camera_pos
    global game_state
    global CELL_SIZE
    last_update = 0
    mouse_press_time = 0
    mouse_pressed = False
    mouse_click = False
    prev_mouse_click = False
    mouse_drag = False
    mouse_drag_time = 0.15
    space_up_switch = True
    while True:
        mouse_mov = pg.mouse.get_rel()
        events = pg.event.get()
        mouse_events = pg.mouse.get_pressed()
        for event in events:
            #checks quit event for proper exit
            if event.type == pg.QUIT:
                    pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if space_up_switch:
                        game_state = not game_state
                        space_up_switch = False
                    
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    space_up_switch = True
         
        mouse_drag = False
        mouse_click = False
        if mouse_events[0] == True:
            prev_mouse_click = False
            if not mouse_pressed:
                mouse_press_time = time.time()
            mouse_mov_statement = abs(mouse_mov[0]) > 3 or abs(mouse_mov[1]) > 3
            if time.time() - mouse_press_time > mouse_drag_time or mouse_mov_statement:
                mouse_drag = True
            if mouse_mov_statement:
                mouse_press_time = 0
            mouse_pressed = True
        if mouse_events[0] == False:
            mouse_pressed = False
            if time.time() - mouse_press_time <= mouse_drag_time and not prev_mouse_click:
                mouse_click = True
                prev_mouse_click = True
                
                
        
        
        #check if left mouse is pressed        
        if mouse_drag:
            camera_pos[0] -= mouse_mov[0]
            camera_pos[1] -= mouse_mov[1]
            
        #game logic
        if time.time() - last_update >= TICK_TIME and game_state:
            last_update = time.time() 
            #gets the alive coords doing a tick of life
            coord_list = game_cycle(coord_list)
        elif not game_state:
            if mouse_click:
                new_cell_coord = [(pg.mouse.get_pos()[0] + camera_pos[0])//CELL_SIZE[0], 
                                  (pg.mouse.get_pos()[1] + camera_pos[1])//CELL_SIZE[1]]
                if new_cell_coord in coord_list:
                    coord_list.remove(new_cell_coord)
                else:
                    coord_list.append(new_cell_coord)
        
        
        cell_draw(coord_list)

def main():
    #initial cell position
    #coord_list = [[10, 10], [11,10], [12,10], [13,10], [14,10], [15,10], [16,10], [17,10], [18,10],
    #              [18,9], [18, 8], [18, 7], [18, 6], [18, 5], [18, 4]]
    coord_list = []
    cell_draw(coord_list)
    game_loop(coord_list)
    





if __name__ == "__main__":
    main()