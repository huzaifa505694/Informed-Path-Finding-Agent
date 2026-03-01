# --- MODULE 1: IMPORTS ---
# Imports essential libraries: pygame for GUI rendering, heapq for priority queue management, 
# and math/random/time for heuristics, obstacle generation, and movement delays.
import pygame
import math
import random
import time
import heapq

# --- MODULE 2: CONFIGURATION & THEME ---
# Sets up the application's window dimensions, grid proportions, and typography.
# Defines the "Midnight" color palette used for nodes, paths, and UI elements.
WIDTH, HEIGHT = 980, 700
GRID_WIDTH = 680
ROWS = 40

BG_DARK = (10, 10, 15)
GRID_LINE = (25, 25, 40)
NODE_EMPTY = (20, 20, 30)
NODE_WALL = (70, 80, 100)
NODE_START = (0, 255, 180)  
NODE_GOAL = (255, 45, 130)   
NODE_WEIGHT = (140, 80, 255) 
NODE_OPEN = (45, 55, 90)
NODE_CLOSED = (30, 30, 50)
NODE_PATH = (255, 210, 0)
AGENT_HEAD = (255, 255, 255) 

UI_PANEL = (15, 15, 22)
UI_ACCENT = (0, 160, 255)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PATH-FINDING AGENT")

FONT_SM = pygame.font.SysFont("Segoe UI", 12, bold=True) # Made small font bold for headings
FONT_MED = pygame.font.SysFont("Segoe UI", 14, bold=True)
FONT_LG = pygame.font.SysFont("Segoe UI", 26, bold=True)

CELL_SIZE = GRID_WIDTH // ROWS

# --- MODULE 3: NODE CLASS ---
# Represents an individual cell on the grid. Tracks its physical position, current state 
# (e.g., wall, goal, path), movement weight, and handles its own visual rendering.
class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x, self.y = col * CELL_SIZE, row * CELL_SIZE
        self.color = NODE_EMPTY
        self.weight = 1

    def get_pos(self): return (self.row, self.col)
    
    def reset(self): 
        self.color, self.weight = NODE_EMPTY, 1
        
    def make_start(self): self.color = NODE_START
    def make_goal(self): self.color = NODE_GOAL
    def make_barrier(self): self.color = NODE_WALL
    def make_weight(self): self.color, self.weight = NODE_WEIGHT, 5 
    def make_open(self): self.color = NODE_OPEN
    def make_closed(self): self.color = NODE_CLOSED
    def make_path(self): self.color = NODE_PATH
    def make_agent(self): self.color = AGENT_HEAD
    
    def draw(self, win): 
        rect = (self.x + 1, self.y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(win, self.color, rect, border_radius=3)
        if self.weight > 1:
            pygame.draw.circle(win, (255, 255, 255, 40), (self.x + CELL_SIZE//2, self.y + CELL_SIZE//2), CELL_SIZE//4)

# --- MODULE 4: HEURISTICS & SEARCH ALGORITHMS ---
# Contains the distance calculations and the separated A* and Greedy Best-First Search algorithms,
# explicitly demonstrating their different mathematical and list strategies.

def heuristic(p1, p2, h_type):
    x1, y1 = p1
    x2, y2 = p2
    if h_type == "Manhattan": return abs(x1 - x2) + abs(y1 - y2)
    return math.hypot(x1 - x2, y1 - y2)

# ==========================================
# ALGORITHM 1: A* SEARCH
# Uses Expanded List (can reopen nodes)
# Priority calculation: f(n) = g(n) + h(n)
# ==========================================
def run_astar(grid, start, end, h_type, ui, stats, draw_updates=True):
    open_set, came, count = [], {}, 0
    heapq.heappush(open_set, (0, count, start))
    
    g = {n: float("inf") for row in grid for n in row}
    g[start] = 0
    f = {n: float("inf") for row in grid for n in row}
    f[start] = heuristic(start.get_pos(), end.get_pos(), h_type)
    
    visited_nodes = 0
    while open_set:
        if draw_updates:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); quit()
        
        cur = heapq.heappop(open_set)[2]

        if cur == end:
            path = []
            while cur in came:
                cur = came[cur]
                if cur != start: cur.make_path()
                path.append(cur)
            return True, path, visited_nodes, g[end] 

        for r_off, c_off in [(1,0), (-1,0), (0,1), (0,-1)]:
            r, c = cur.row + r_off, cur.col + c_off
            if 0 <= r < ROWS and 0 <= c < ROWS:
                nb = grid[r][c]
                if nb.color != NODE_WALL:
                    temp_g = g[cur] + nb.weight
                    
                    # Expanded List strategy: Re-evaluate if a shorter g(n) path is found
                    if temp_g < g[nb]:
                        came[nb] = cur
                        g[nb] = temp_g
                        h_val = heuristic(nb.get_pos(), end.get_pos(), h_type)
                        f[nb] = temp_g + h_val  # f(n) = g(n) + h(n)
                        count += 1
                        heapq.heappush(open_set, (f[nb], count, nb))
                        if nb != end and nb != start: nb.make_open()
        
        if cur != start: 
            cur.make_closed()
            visited_nodes += 1
        
        if draw_updates:
            draw_grid(WIN, grid)
            draw_sidebar(WIN, ui, stats)
            pygame.display.update()
        
    return False, [], visited_nodes, "N/A"

# ==========================================
# ALGORITHM 2: GREEDY BEST-FIRST SEARCH (GBFS)
# Uses Strict Visited List (never reopens)
# Priority calculation: f(n) = h(n)
# ==========================================
def run_gbfs(grid, start, end, h_type, ui, stats, draw_updates=True):
    open_set, came, count = [], {}, 0
    closed_set = set() # Strict visited list
    heapq.heappush(open_set, (0, count, start))
    
    g = {n: float("inf") for row in grid for n in row}
    g[start] = 0 # Tracked ONLY for the final Path Cost metric output
    
    visited_nodes = 0
    while open_set:
        if draw_updates:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); quit()
        
        cur = heapq.heappop(open_set)[2]
        
    
        if cur in closed_set:
            continue
        closed_set.add(cur)

        if cur == end:
            path = []
            while cur in came:
                cur = came[cur]
                if cur != start: cur.make_path()
                path.append(cur)
            return True, path, visited_nodes, g[end] 

        for r_off, c_off in [(1,0), (-1,0), (0,1), (0,-1)]:
            r, c = cur.row + r_off, cur.col + c_off
            if 0 <= r < ROWS and 0 <= c < ROWS:
                nb = grid[r][c]
                if nb.color != NODE_WALL and nb not in closed_set:
                    
                    temp_g = g[cur] + nb.weight
                    if temp_g < g[nb]:
                        came[nb] = cur
                        g[nb] = temp_g
                        
                    h_val = heuristic(nb.get_pos(), end.get_pos(), h_type)
                    count += 1
                    
                    
                    heapq.heappush(open_set, (h_val, count, nb))
                    if nb != end and nb != start: nb.make_open()
        
        if cur != start: 
            cur.make_closed()
            visited_nodes += 1
        
        if draw_updates:
            draw_grid(WIN, grid)
            draw_sidebar(WIN, ui, stats)
            pygame.display.update()
        
    return False, [], visited_nodes, "N/A"

# --- MODULE 5: UI INTERFACE COMPONENTS ---
# Defines the interactive glowing buttons and handles the rendering of the grid, 
# the sidebar layout, and real-time metric updates on the screen.
class NeonButton:
    def __init__(self, x, y, w, h, text, val):
        self.rect = pygame.Rect(x, y, w, h)
        self.text, self.val = text, val
        
    def draw(self, win, active=False):
        color = UI_ACCENT if active else (45, 45, 60)
        pygame.draw.rect(win, (25, 25, 35), self.rect, border_radius=4)
        pygame.draw.rect(win, color, self.rect, 1 if not active else 2, border_radius=4)
        txt_surf = FONT_MED.render(self.text, True, (255, 255, 255) if active else (140, 140, 160))
        win.blit(txt_surf, (self.rect.centerx - txt_surf.get_width()//2, self.rect.centery - txt_surf.get_height()//2))

def draw_grid(win, grid):
    win.fill(BG_DARK)
    for row in grid:
        for node in row: node.draw(win)
    for i in range(ROWS + 1):
        pygame.draw.line(win, GRID_LINE, (0, i * CELL_SIZE), (GRID_WIDTH, i * CELL_SIZE))
        pygame.draw.line(win, GRID_LINE, (i * CELL_SIZE, 0), (i * CELL_SIZE, GRID_WIDTH))

def draw_sidebar(win, ui, stats):
    px = GRID_WIDTH
    pygame.draw.rect(win, UI_PANEL, (px, 0, WIDTH - px, HEIGHT))
    win.blit(FONT_LG.render("PATH-FINDING", True, UI_ACCENT), (px + 25, 25))
    win.blit(FONT_LG.render("AGENT", True, (255, 255, 255)), (px + 25, 55))

    for key, btn in ui.items():
        if isinstance(btn, NeonButton):
            active = False
            if key == 'btn_astar': active = ui['algo'] == 'A*'
            elif key == 'btn_gbfs': active = ui['algo'] == 'GBFS'
            elif key == 'btn_man': active = ui['heuristic'] == 'Manhattan'
            elif key == 'btn_euc': active = ui['heuristic'] == 'Euclidean'
            elif key == 'btn_static': active = ui['mode'] == 'Static'
            elif key == 'btn_dynamic': active = ui['mode'] == 'Dynamic'
            elif key == 'btn_draw_wall': active = ui['draw_mode'] == 'Wall'
            elif key == 'btn_draw_weight': active = ui['draw_mode'] == 'Weight'
            elif key == 'btn_set_start': active = ui['draw_mode'] == 'Start'
            elif key == 'btn_set_goal': active = ui['draw_mode'] == 'Goal'
            btn.draw(win, active)

    sections = [("ALGORITHM", 110), ("HEURISTIC", 185), ("SIMULATION", 260), ("PLACEMENT", 335), ("STATS", 580)]
    for text, y in sections:
    
        glow = FONT_SM.render(text, True, UI_ACCENT)
        lbl = FONT_SM.render(text, True, (220, 230, 255))
        win.blit(glow, (px + 25, y + 1))
        win.blit(lbl, (px + 25, y))
        pygame.draw.line(win, (40, 40, 50), (px + 25, y + 18), (WIDTH - 25, y + 18))

    y_st = 610
    for s in [f"Visited: {stats['visited']}", f"Path Cost: {stats['cost']}", f"Time: {stats['time']}ms"]:
        win.blit(FONT_MED.render(s, True, (200, 200, 210)), (px + 30, y_st))
        y_st += 25

# --- MODULE 6: GRID UTILITIES ---
# Helper functions for wiping old search visualizations from the grid 
# and generating randomized 30% density maze obstacles.
def clear_search_visuals(grid):
    for row in grid:
        for n in row:
            if n.color in [NODE_OPEN, NODE_CLOSED, NODE_PATH]: n.reset()

def generate_maze(grid, start, end):
    for row in grid:
        for n in row:
            if n != start and n != end:
                n.reset()
                if random.random() < 0.3: 
                    n.make_barrier()

# --- MODULE 7: MAIN EXECUTION LOOP ---
# Initializes the grid/UI, manages user input (mouse clicks), controls the agent's movement,
# and handles real-time dynamic obstacle generation and automated re-planning.
def main():
    grid = [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]
    start = grid[5][5]
    end = grid[ROWS-6][ROWS-6]
    start.make_start()
    end.make_goal()
    
    px_btn = GRID_WIDTH + 25
    ui = {
        'algo':'A*', 'heuristic':'Manhattan', 'mode':'Static', 'draw_mode':'Wall',
        'btn_astar': NeonButton(px_btn, 135, 120, 30, 'A-STAR', 'A*'),
        'btn_gbfs': NeonButton(px_btn + 130, 135, 120, 30, 'GREEDY', 'GBFS'),
        'btn_man': NeonButton(px_btn, 210, 120, 30, 'MANHATTAN', 'Manhattan'),
        'btn_euc': NeonButton(px_btn + 130, 210, 120, 30, 'EUCLIDEAN', 'Euclidean'),
        'btn_static': NeonButton(px_btn, 285, 120, 30, 'STATIC', 'Static'),
        'btn_dynamic': NeonButton(px_btn + 130, 285, 120, 30, 'DYNAMIC', 'Dynamic'),
        'btn_draw_wall': NeonButton(px_btn, 360, 120, 30, 'WALLS', 'Wall'),
        'btn_draw_weight': NeonButton(px_btn + 130, 360, 120, 30, 'WEIGHTS', 'Weight'),
        'btn_set_start': NeonButton(px_btn, 400, 120, 30, 'START POS', 'Start'),
        'btn_set_goal': NeonButton(px_btn + 130, 400, 120, 30, 'GOAL POS', 'Goal'),
        'btn_start': NeonButton(px_btn, 455, 250, 40, 'START AGENT', 'Run'),
        'btn_gen_maze': NeonButton(px_btn, 505, 250, 30, 'GENERATE MAZE', 'Maze'),
        'btn_reset': NeonButton(px_btn, 545, 250, 30, 'RESET SYSTEM', 'Reset')
    }
    
    stats = {'visited': 0, 'cost': 0, 'time': 0}
    
    agent_moving = False
    agent_path = []
    last_obs_time = time.time()
    last_move_time = time.time()
    
    run = True

    while run:
        
        if agent_moving and agent_path:
            current_time = time.time()
            
            if current_time - last_move_time > 0.1:
                next_node = agent_path.pop()
                start.reset()
                start = next_node
                start.make_agent()
                last_move_time = current_time
                
                if start == end:
                    start.make_goal()
                    agent_moving = False

            if ui['mode'] == 'Dynamic' and current_time - last_obs_time > 0.01 and agent_moving:
                r, c = random.randint(0, ROWS-1), random.randint(0, ROWS-1)
                target = grid[r][c]
                
                if target.color in [NODE_EMPTY, NODE_OPEN, NODE_CLOSED, NODE_PATH] and target != start and target != end:
                    if random.random() > 0.3: target.make_barrier()
                    else: target.make_weight()
                    
                    if target in agent_path:
                        clear_search_visuals(grid)
                        t0 = time.perf_counter()
                        
                        if ui['algo'] == "A*":
                            success, new_path, visited, cost = run_astar(grid, start, end, ui['heuristic'], ui, stats, draw_updates=False)
                        else:
                            success, new_path, visited, cost = run_gbfs(grid, start, end, ui['heuristic'], ui, stats, draw_updates=False)
                            
                        stats.update({'visited': visited, 'cost': cost, 'time': round((time.perf_counter()-t0)*1000, 2)})
                        
                        if success:
                            agent_path = new_path
                        else:
                            agent_moving = False 
                
                last_obs_time = current_time

        draw_grid(WIN, grid)
        draw_sidebar(WIN, ui, stats)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT: run = False
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = e.pos
                if mx >= GRID_WIDTH:
                    for key, btn in ui.items():
                        if isinstance(btn, NeonButton) and btn.rect.collidepoint(e.pos):
                            if key in ['btn_astar','btn_gbfs']: ui['algo']=btn.val
                            elif key in ['btn_man','btn_euc']: ui['heuristic']=btn.val
                            elif key in ['btn_static','btn_dynamic']: ui['mode']=btn.val
                            elif key in ['btn_draw_wall','btn_draw_weight','btn_set_start','btn_set_goal']: ui['draw_mode']=btn.val
                            elif key == 'btn_gen_maze':
                                agent_moving = False
                                generate_maze(grid, start, end)
                            elif key == 'btn_start':
                                agent_moving = False
                                clear_search_visuals(grid)
                                start.make_start() 
                                t0 = time.perf_counter()
                                
                                if ui['algo'] == "A*":
                                    success, path_list, visited, cost = run_astar(grid, start, end, ui['heuristic'], ui, stats)
                                else:
                                    success, path_list, visited, cost = run_gbfs(grid, start, end, ui['heuristic'], ui, stats)
                                    
                                stats.update({'visited': visited, 'cost': cost, 'time': round((time.perf_counter()-t0)*1000, 2)})
                                if success:
                                    agent_path = path_list
                                    agent_moving = True
                                    last_move_time = time.time()
                                    last_obs_time = time.time()
                            elif key == 'btn_reset':
                                agent_moving = False
                                stats = {'visited': 0, 'cost': 0, 'time': 0}
                                for row in grid:
                                    for n in row: 
                                        if n != start and n != end: n.reset()
                                start.make_start()
                else:
                    if not agent_moving: 
                        c, r = mx // CELL_SIZE, my // CELL_SIZE
                        if 0 <= r < ROWS and 0 <= c < ROWS:
                            node = grid[r][c]
                            if ui['draw_mode'] == 'Wall' and node not in [start, end]: node.make_barrier()
                            elif ui['draw_mode'] == 'Weight' and node not in [start, end]: node.make_weight()
                            elif ui['draw_mode'] == 'Start' and node != end: 
                                start.reset()
                                start = node
                                start.make_start()
                            elif ui['draw_mode'] == 'Goal' and node != start: 
                                end.reset()
                                end = node
                                end.make_goal()
            
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                 if not agent_moving:
                    mx, my = e.pos
                    if mx < GRID_WIDTH:
                        c, r = mx // CELL_SIZE, my // CELL_SIZE
                        if 0 <= r < ROWS and 0 <= c < ROWS:
                            node = grid[r][c]
                            if node != start and node != end:
                                node.reset()

    pygame.quit()

if __name__ == '__main__':
    main()