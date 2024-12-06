from random import choice, randint

import pygame


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SPEED = 10


class GameObject:
    """Базовый класс для всех объектов в игре."""

    def __init__(self, position=(0, 0)):
        """Инициализация объекта."""
        self.position = position

    def draw(self, color):
        """Отрисовка объекта на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс для управления яблоком на игровом поле."""

    def __init__(self, position=(0, 0), body_color=(255, 0, 0)):
        """Создает яблоко в случайной позиции."""
        super().__init__(position)
        self.body_color = body_color
        super().__init__((randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                          randint(0, GRID_HEIGHT - 1) * GRID_SIZE))

    def randomize_position(self):
        """Перемещает яблоко в новую случайную позицию."""
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Класс для управления змейкой."""

    def __init__(self, position=(0, 0), body_color=(0, 255, 0)):
        """Создает змейку с начальной длиной 1 и случайным направлением."""
        super().__init__(position)
        super().__init__((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.body_color = body_color
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении.
        Если змейка пересекает саму себя,
        происходит сброс её состояния.
        """
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT)

        if new_head in self.positions[:-1]:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        """Сбрасывает состояние змейки к начальным значениям."""
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1

    def grow(self):
        """Увеличивает длину змейки на 1 сегмент."""
        self.length += 1

    def update_direction(self):
        """Обновляет направление движения змейки на основе ввода юзера."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает змейку на игровом поле."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Получает позицию головы змейки."""
        return self.position


def handle_keys(snake):
    """Обрабатывает ввод пользователя с клавиатуры."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция для запуска игры."""
    pygame.init()
    global screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Змейка')
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw(APPLE_COLOR)
        pygame.display.update()


if __name__ == '__main__':
    main()
