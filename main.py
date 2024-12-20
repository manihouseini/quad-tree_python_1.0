import pygame, quad_tree, random
from libraries.pygame_tools import pgame_debug
from sys import exit

pygame.init()

print("use left click to add points.")
num_of_points = int(input("please give a number of points: "))
tree_copacity = int(input("please give a copacity for the quad tree: "))
moving_points = int(
    input(
        """
please enter point mode:
1. none_moving
2. moving

>"""
    )
)
print(
    """
please enter search mode:
1. rect
2. circle
"""
)
search_mode = int(input(">"))


class App:
    def __init__(self, WIDTH, HEIGHT, FPS) -> None:
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.FPS = FPS
        self.running = True

    def setup(self):
        self.tree = quad_tree.Quad_tree(0, 0, 1000, 800, tree_copacity)
        self.points = []

        # none moving points:
        if moving_points == 1:
            for i in range(num_of_points):
                p = quad_tree.Point(random.randint(0, 1000), random.randint(0, 800), 10)
                self.points.append(p)
                self.tree.insert(p)

        # moving points:
        if moving_points == 2:
            for i in range(num_of_points):
                p = quad_tree.Moving_point(
                    random.randint(0, 1000),
                    random.randint(0, 800),
                    10,
                    self.WIN.get_size()[0],
                    self.WIN.get_size()[1],
                )
                self.points.append(p)
                self.tree.insert(p)

    def update(self):
        # moving
        if moving_points == 2:
            self.tree = quad_tree.Quad_tree(0, 0, 1000, 800, tree_copacity)
            for p in self.points:
                p.update()
                self.tree.insert(p)

        # showing the tree and the points
        self.tree.show(self.WIN)
        a = self.tree.rect_query_setup(0, 0, 1000, 800)
        for p in a:
            p.show(self.WIN, (255, 0, 0))

        # finding the points in a rect around the mouse
        if search_mode == 1:
            x, y = pygame.mouse.get_pos()
            rec = quad_tree.Rect(x - 100, y - 100, 200, 200)
            rec.show(self.WIN)
            found = self.tree.rect_query_setup(x - 100, y - 100, 200, 200)

        # finding the points in a circle around the mouse
        if search_mode == 2:
            x, y = pygame.mouse.get_pos()
            found = self.tree.circle_query_setup(x, y, 100)
            pygame.draw.circle(self.WIN, (255, 255, 0), (x, y), 100, 1)

        # showing the found points
        for p in found:
            p.show(self.WIN, (0, 255, 0))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        if pygame.mouse.get_pressed()[0]:
            if moving_points == 2:
                m = pygame.mouse.get_pos()
                p = quad_tree.Moving_point(
                    m[0], m[1], 10, self.WIN.get_size()[0], self.WIN.get_size()[1]
                )
                self.points.append(p)
                self.tree.insert(p)
            elif moving_points == 1:
                m = pygame.mouse.get_pos()
                p = quad_tree.Point(m[0], m[1], 10)
                self.points.append(p)
                self.tree.insert(p)

    def run(self):
        self.setup()
        while self.running:
            self.WIN.fill((23, 23, 23))
            self.events()

            self.update()

            self.CLOCK.tick(self.FPS)
            pgame_debug(self.CLOCK.get_fps(), 10)
            pygame.display.set_caption(str(self.CLOCK.get_fps()))
            pygame.display.flip()


app = App(1000, 800, 0)
app.run()
