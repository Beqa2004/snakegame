import pygame
from pygame.locals import *
import random

size = 58

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("assets/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = size
        self.y = size

    # ხატავს ვაშლს
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    # რანდომულ ადგილებში აჩენს ვაშლს
    def move(self):
        self.x = random.randint(0, 16) * size
        self.y = random.randint(0, 11) * size

class Snake:
    def __init__(self, parent_screen, length):
        # გველის ზომა
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("assets/block.jpg").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = "down"


    #ხატავს გველს
    def draw(self):
        self.parent_screen.fill((0, 0, 0))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    # გველის ზომას ადიდებს
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    #განსაზღვრავს მიმართულებას რომელიც გამოყენებულია Game კლასის run ფუნქციაში
    def move_left(self):
        self.direction = "left"
    def move_right(self):
        self.direction = "right"
    def move_up(self):
        self.direction = "up"
    def move_down(self):
        self.direction = "down"


    # ამოძრავებს გველს Game კლასის run ფუნქციაში მითითებული ღილაკის დაჭერისას
    def walk(self): 
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size
        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size

        self.draw()

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((1000, 700))
        self.display.fill((0, 0, 0))
        self.snake = Snake(self.display, 1)
        self.snake.draw()
        pygame.display.flip()
        self.clock = pygame.time.Clock()
        self.apple = Apple(self.display)
        self.apple.draw()
        pygame.display.flip()

    # ამოწმებს დაჯახების კორდინატებს
    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True
        return False

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.show_score()
        pygame.display.flip()

        # გველი ეჯახება ვაშლს და increase_length() ფუნქციით დიდგება ზომაში
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()

        # გველი ეჯახება თავის თავს და თამაში მთავრდება
        for i in range(3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise Exception("Game Over")


    #ფუნქცია რომელიც ანახებს მისჯის თამაში დასრულების და თავიდან დაწყბეის ან გამორთვის
    def show_game_over(self):
        self.display.fill((255, 255, 255))
        font = pygame.font.SysFont("arial", 30)
        message1 = font.render(f"Game Over! Your Score: {self.snake.length}", True, (0, 0, 0))
        self.display.blit(message1, (250, 300))
        message2 = font.render("Play Again: Enter | Exit: Escape", True, (0, 0, 0))
        self.display.blit(message2, (250, 350))
        pygame.display.flip()

    # ანახებს ქულას
    def show_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.display.blit(score, (800, 10))


    #თამაში დარესეტების ფუნქცია
    def reset(self):
        self.snake = Snake(self.display, 1)
        self.apple = Apple(self.display)




    # ღილაკების დაჭერის განსაზღვრა
    def run(self):
        pause = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                

                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            self.clock.tick(5)

if __name__ == "__main__":
    game = Game()
    game.run()