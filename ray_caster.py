import pygame

from math import cos, sin, pi

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

textures = {
    '0' : pygame.image.load('wall.jpg'),
    '1' : pygame.image.load('checkpoint.jpg'),
    '2' : pygame.image.load('dark.jpg'),
}

class RayCaster(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        self.map = []
        self.block_size = 50
        self.wall_height = 50

        self.step_size = 5

        self.player = {
            "x" : 75,
            "y" : 55,
            "angle" : 90,
            "fov" : 60
        }

    def load_map(self, filename):
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(list(line))

    def draw_rect(self, x, y, texture):
        texture = pygame.transform.scale(texture, (self.block_size, self.block_size))
        rect = texture.get_rect()
        rect = rect.move((x, y))
        self.screen.blit(texture, rect)

    def draw_player_icon(self, color = BLACK):
        rect = (self.player['x'] - 2, self.player['y'] - 2, 5, 5)
        self.screen.fill(color, rect)

    def cast_ray(self, a):
        rads = a * pi / 180
        dist = 0
        while True:
            x = int(self.player['x'] + dist * cos(rads))
            y = int(self.player['y'] + dist * sin(rads))

            i = int(x / self.block_size)
            j = int(y / self.block_size)

            if self.map[j][i] != ' ':
                hit_x = x - i * self.block_size
                hit_y = y - j * self.block_size

                if 1 < hit_x < self.block_size - 1:
                    max_hit = hit_x
                else:
                    max_hit = hit_y

                tx = max_hit / self.block_size

                return dist, self.map[j][i], tx

            self.screen.set_at((x,y), WHITE)

            dist += 1

    def render(self):

        half_width = int(self.width / 2)
        half_height = int(self.height / 2)

        for x in range(0, half_width, self.block_size):
            for y in range(0, self.height, self.block_size):
                
                i = int(x / self.block_size)
                j = int(y / self.block_size)

                if self.map[j][i] != ' ':
                    self.draw_rect(x, y, textures[self.map[j][i]])

        self.draw_player_icon()

        for i in range(half_width):
            angle = self.player['angle'] - self.player['fov'] / 2 + self.player['fov'] * i / half_width
            dist, wall_type, tx = self.cast_ray(angle)

            x = half_width + i 

            h = self.height / (dist * cos((angle - self.player['angle']) * pi / 180 )) * self.wall_height

            start = int(half_height - h / 2)
            end = int(half_height + h / 2)

            image = textures[wall_type]
            tx = int(tx * image.get_width())

            for y in range(start, end):
                ty = (y - start) / (end - start)
                ty = int(ty * image.get_height())
                tex_color = image.get_at((tx, ty))
                self.screen.set_at((x, y), tex_color)
                self.screen.set_at((x, y), tex_color)

        for i in range(self.height):
            self.screen.set_at((half_width, i), BLACK)
            self.screen.set_at((half_width + 1, i), BLACK)
            self.screen.set_at((half_width - 1, i), BLACK)


pygame.init()
screen = pygame.display.set_mode((1000, 500))
screen.set_alpha(None)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

def update_FPS():
    fps = str(int(clock.get_fps()))
    fps = font.render(fps, 1, pygame.Color("white"))
    return fps

r = RayCaster(screen)
r.load_map('map.txt')

isRunning = True

move_forwards = False
move_backwards = False
move_left = False
move_right = False
turn_right = False
turn_left = False

while isRunning:

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        new_x = r.player['x']
        new_y = r.player['y']

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            elif ev.key == pygame.K_w:
                move_forwards = True
            elif ev.key == pygame.K_s:
                move_backwards = True
            elif ev.key == pygame.K_a:
                move_left = True
            elif ev.key == pygame.K_d:
                move_right = True
            elif ev.key == pygame.K_LEFT:
                turn_left = True
            elif ev.key == pygame.K_RIGHT:
                turn_right = True
        
        elif ev.type == pygame.KEYUP:
            if ev.key == pygame.K_w:
                move_forwards = False
            elif ev.key == pygame.K_s:
                move_backwards = False
            elif ev.key == pygame.K_a:
                move_left = False
            elif ev.key == pygame.K_d:
                move_right = False
            elif ev.key == pygame.K_LEFT:
                turn_left = False
            elif ev.key == pygame.K_RIGHT:
                turn_right = False

    if move_forwards:
        new_x += cos(r.player['angle'] * pi / 180) * r.step_size
        new_y += sin(r.player['angle'] * pi / 180) * r.step_size
    if move_backwards:
        new_x -= cos(r.player['angle'] * pi / 180) * r.step_size
        new_y -= sin(r.player['angle'] * pi / 180) * r.step_size
    if move_left:
        new_x -= cos((r.player['angle'] + 90) * pi / 180) * r.step_size
        new_y -= sin((r.player['angle'] + 90) * pi / 180) * r.step_size
    if move_right:
        new_x += cos((r.player['angle'] + 90) * pi / 180) * r.step_size
        new_y += sin((r.player['angle'] + 90) * pi / 180) * r.step_size
    if turn_left:
        r.player['angle'] -= 6
    if turn_right:
        r.player['angle'] += 6

    i = int(new_x / r.block_size)
    j = int(new_y / r.block_size)

    if r.map[j][i] == ' ':
        r.player['x'] = new_x
        r.player['y'] = new_y

    screen.fill(pygame.Color("gray"))
    screen.fill(pygame.Color("saddlebrown"), (int(r.width / 2), 0, int(r.width / 2),int(r.height / 2)))
    screen.fill(pygame.Color("dimgray"), (int(r.width / 2), int(r.height / 2), int(r.width / 2),int(r.height / 2)))
    r.render()

    # FPS
    screen.fill(pygame.Color("black"), (0, 0, 30, 30))
    screen.blit(update_FPS(), (0,0))
    clock.tick(30)  
    
    pygame.display.update()


pygame.quit()
