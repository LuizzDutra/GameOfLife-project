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
        if type(args[i]).isinstance(str) and len(args[1]) > 0 and args[i][0] == '-':
            if args[i] == '-t':
                try:
                    TICK_TIME = float(args[i+1])
                except:
                    print("Could not recognize arguments of '-t'")
                    raise
            if args[i] == '-p':
                try:
                    CELL_SIZE = (int(args[i+1]), int(args[i+2]))
                except:
                    print("Could not recognize arguments of '-p'")
                    raise
cell_image = pg.Surface(CELL_SIZE)
cell_image.fill((255,255,255))     


#Class that processes all the inputs
class InputHandler():
    def __init__(self):
        self.mouse_press_time = 0
        self.mouse_pressed = False
        self.mouse_click = False
        self.prev_mouse_click = False
        self.mouse_drag = False
        self.MOUSE_DRAG_TIME = 0.15
        self.space_up_switch = True
        self.mouse_mov_buff = (0, 0)

    def handle_key_input(self, events: list):
        global game_state
        for event in events:
            #checks quit event for proper exit
            if event.type == pg.QUIT:
                pg.quit()

            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and self.space_up_switch:
                game_state = not game_state
                self.space_up_switch = False

            if event.type == pg.KEYUP and event.key == pg.K_SPACE:
                self.space_up_switch = True

    def handle_mouse_input(self, mouse_mov: tuple, mouse_events: tuple):
        self.mouse_mov_buff = mouse_mov
        self.mouse_drag = False
        self.mouse_click = False
        if mouse_events[0] == True:
            self.prev_mouse_click = False
            if not self.mouse_pressed:
               self.mouse_press_time = time.time()
            mouse_mov_statement = abs(mouse_mov[0]) > 3 or abs(mouse_mov[1]) > 3
            if time.time() - self.mouse_press_time > self.MOUSE_DRAG_TIME or mouse_mov_statement:
                self.mouse_drag = True
            if mouse_mov_statement:
                self.mouse_press_time = 0
            self.mouse_pressed = True
        if mouse_events[0] == False:
            self.mouse_pressed = False
            if time.time() - self.mouse_press_time <= self.MOUSE_DRAG_TIME and not self.prev_mouse_click:
                self.mouse_click = True
                self.prev_mouse_click = True


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
        for _ in range(occur):
            heat_map.remove(buffer)
    return life_coords

def game_loop(coord_list):
    global camera_pos
    global game_state
    global CELL_SIZE
    last_update = 0
    input_handler = InputHandler()

    while True:
        input_handler.handle_key_input(pg.event.get())
        input_handler.handle_mouse_input(pg.mouse.get_rel(), pg.mouse.get_pressed())

        #check if left mouse is pressed        
        if input_handler.mouse_drag:
            camera_pos[0] -= input_handler.mouse_mov_buff[0]
            camera_pos[1] -= input_handler.mouse_mov_buff[1]
            
        #game logic
        if time.time() - last_update >= TICK_TIME and game_state:
            last_update = time.time() 
            #gets the alive coords doing a tick of life
            coord_list = game_cycle(coord_list)
        elif not game_state and input_handler.mouse_click:
            new_cell_coord = [(pg.mouse.get_pos()[0] + camera_pos[0])//CELL_SIZE[0], 
                                (pg.mouse.get_pos()[1] + camera_pos[1])//CELL_SIZE[1]]
            if new_cell_coord in coord_list:
                coord_list.remove(new_cell_coord)
            else:
                coord_list.append(new_cell_coord)
    
        
        cell_draw(coord_list)

def main():
    coord_list = []
    cell_draw(coord_list)
    game_loop(coord_list)
    


if __name__ == "__main__":
    main()