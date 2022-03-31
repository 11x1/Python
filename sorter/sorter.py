import random
import pygame
import time

# Set the window title to "Sorting"
pygame.display.set_caption("Sorting Visualiser - by khey/11x1")

def generate_random_values(amount):
    value_list = []
    for i in range(amount):
        value_list.append(random.randint(0, 500))
    return value_list

screen = pygame.display.set_mode((800, 500))
width, height = screen.get_size()

values = generate_random_values(width - 1)
sorted_copy_list = sorted(values.copy())

def visualise_sort():
    iter = 1
    for value in values:
        current_value = value

        color = (255, 0, 0)
        if iter < len(values) and current_value > values[iter]:
            pygame.draw.line(screen, color, (iter, 0), (iter, height), 2)
            temp = values[iter]
            values[iter] = current_value
            values[iter - 1] = temp
            # break # uncomment this break to only visualise the first sort
        iter += 1

def draw():
    screen.fill((0, 0, 0))
    iter = 1
    color = (255, 255, 255)
    if values == sorted_copy_list: color = (0, 255, 0)

    for value in values:
        pygame.draw.line(screen, color, (iter, height), (iter, height - value), 2)
        iter += 1
    visualise_sort()
    pygame.display.update()

while True:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
