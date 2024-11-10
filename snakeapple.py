import pygame as pg
import random

# Constants
GRID_SIZE = 16  # Grid size (number of cells per row/column)
CELL_SIZE = 20  # Size of each cell in pixels
SCREEN_WIDTH = 350  # Width of the game screen
SCREEN_HEIGHT = 350  # Height of the game screen
FPS = 10  # Frames per second (game speed)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Directions for the snake
UP = -GRID_SIZE
DOWN = GRID_SIZE
LEFT = -1
RIGHT = 1


class Snake:
    def __init__(self):
        self.body = [GRID_SIZE * 2 + 1, GRID_SIZE * 2, GRID_SIZE * 2 - 1]  # Initial snake body (head at the end)
        self.direction = RIGHT  # Start moving to the right
        self.alive = True

    def move(self):
        head = self.body[0]
        new_head = head + self.direction
        self.body = [new_head] + self.body[:-1]  # Move head and update body

    def grow(self):
        head = self.body[0]
        self.body = [head + self.direction] + self.body  # Add a new segment at the head

    def change_direction(self, new_direction):
        # Prevent reversing direction
        if (self.direction == LEFT and new_direction != RIGHT) or (self.direction == RIGHT and new_direction != LEFT) or \
           (self.direction == UP and new_direction != DOWN) or (self.direction == DOWN and new_direction != UP):
            self.direction = new_direction

    def check_collision(self):
        head = self.body[0]
        if head in self.body[1:]:  # Collision with itself
            self.alive = False

    def get_head_position(self):
        return self.body[0]

    def get_body_positions(self):
        return self.body

    def draw(self, screen):
        for idx, segment in enumerate(self.body):
            color = RED if idx == 0 else GREEN  # Head is red, body is green
            x = (segment % GRID_SIZE) * CELL_SIZE
            y = (segment // GRID_SIZE) * CELL_SIZE
            pg.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))


class Apple:
    def __init__(self, snake_body):
        self.position = self.random_position(snake_body)

    def random_position(self, snake_body):
        # Generate a random position for the apple, ensuring it doesn't overlap with the snake
        position = random.randint(0, GRID_SIZE * GRID_SIZE - 1)
        while position in snake_body:
            position = random.randint(0, GRID_SIZE * GRID_SIZE - 1)
        return position

    def draw(self, screen):
        x = (self.position % GRID_SIZE) * CELL_SIZE
        y = (self.position // GRID_SIZE) * CELL_SIZE
        pg.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))


def main():
    pg.init()

    # Set up the screen
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption('Snake Game')

    # Initialize the snake and apple
    snake = Snake()
    apple = Apple(snake.get_body_positions())

    clock = pg.time.Clock()

    while snake.alive:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                snake.alive = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    snake.change_direction(UP)
                elif event.key == pg.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pg.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pg.K_RIGHT:
                    snake.change_direction(RIGHT)

        # Move the snake
        snake.move()

        # Check for collision
        snake.check_collision()

        # Check if snake eats the apple
        if snake.get_head_position() == apple.position:
            snake.grow()  # Snake grows
            apple = Apple(snake.get_body_positions())  # Generate a new apple

        # Fill the screen with black
        screen.fill(BLACK)

        # Draw the snake and the apple
        snake.draw(screen)
        apple.draw(screen)

        # Update the display
        pg.display.flip()

        # Control the game speed
        clock.tick(FPS)

    pg.quit()


if __name__ == "__main__":
    main()
