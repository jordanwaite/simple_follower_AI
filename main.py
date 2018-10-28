import pygame as pg


class Game:
    # Settings
    window_width = 800
    window_height = 600
    CLOCK = pg.time.Clock()
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    x_pos = 0
    y_pos = 0
    x2_pos = 500
    y2_pos = 500
    player_speed = 2
    enemy_speed = 3
    previous_x_pos = []
    previous_y_pos = []
    player_lead_dist = 30
    aimpoint_xy = [0, 0]
    last = 0
    wait = 1000

    def __init__(self):
        self.display_surface = pg.display.set_mode((self.window_width, self.window_height))
        pg.display.set_caption("AI Practice")
        self.enemy = pg.rect.Rect((self.x_pos, self.y_pos, 10, 10))
        self.player = pg.rect.Rect((self.x2_pos, self.y2_pos, 10, 10))
        self.running = True

# Game Loop
    def run(self):
        while self.running:
            self.event()
            self.update()
            self.draw()
            self.CLOCK.tick(60)

# Quit Detection
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                        self.running = False

# Keyboard movements and aimpoint of the enemy to be at the player's aimpoint.
    def update(self):
        key = pg.key.get_pressed()

        if key[pg.K_LEFT]:
            self.x2_pos -= self.player_speed
        if key[pg.K_RIGHT]:
            self.x2_pos += self.player_speed
        if key[pg.K_UP]:
            self.y2_pos -= self.player_speed
        if key[pg.K_DOWN]:
            self.y2_pos += self.player_speed

        # X and Y aimpoint is where the player currently is plus where the player is going (bases on previous position.)
        if self.x_pos > self.aimpoint_xy[0] + self.x2_pos:
            self.x_pos -= self.enemy_speed
        else:
            self.x_pos += self.enemy_speed

        if self.y_pos > self.aimpoint_xy[1] + self.y2_pos:
            self.y_pos -= self.enemy_speed
        else:
            self.y_pos += self.enemy_speed

        # Variable that uses the player_lead function to determine where the player is going.
        self.aimpoint_xy = self.player_lead(self.x2_pos, self.y2_pos)

    def draw(self):
        # Draw the player, enemy, and player's aimpoint.
        self.display_surface.fill(self.BLACK)
        pg.draw.rect(self.display_surface, self.GREEN, (self.x2_pos, self.y2_pos, 10, 10))
        pg.draw.rect(self.display_surface, self.RED, (self.x_pos, self.y_pos, 10, 10))
        pg.draw.circle(self.display_surface, self.BLUE, (self.aimpoint_xy[0] + self.x2_pos,
                                                         self.aimpoint_xy[1] + self.y2_pos), 3)
        pg.display.flip()

    def player_lead(self, x, y):
        # Takes in the player's current (x,y) position, creates a list of the previous positions, and creates an
        # future prediction of where the player will be from the previous positions bases on <player_lead_dist value>.
        # The list will be size of <player_lead_dist>, the larger the value the further ahead the lead point will be.
        self.previous_x_pos.insert(0, x)
        self.previous_y_pos.insert(0, y)
        if len(self.previous_x_pos) > self.player_lead_dist:
            self.previous_x_pos.pop()
        if len(self.previous_y_pos) > self.player_lead_dist:
            self.previous_y_pos.pop()

        x_lead_dist = self.previous_x_pos[0] - self.previous_x_pos[-1]
        y_lead_dist = self.previous_y_pos[0] - self.previous_y_pos[-1]

        # Will print the (x,y) lead distance values every <self.wait> milliseconds.
        now = pg.time.get_ticks()
        if now - self.last > self.wait:
            self.last = now
            print(x_lead_dist, y_lead_dist)

        return x_lead_dist, y_lead_dist


if __name__ == "__main__":
    g = Game()
    g.run()
