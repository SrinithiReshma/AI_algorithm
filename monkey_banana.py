import pygame
import time
import random  # Import random for discontinuous movement

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monkey-Banana Problem 🍌🐵")

# Load images
background_img = pygame.image.load("background.jpg")  # Load background
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Resize to fit screen

monkey_img = pygame.image.load("monkey.png")
monkey_img = pygame.transform.scale(monkey_img, (100, 100))  # Increased size

box_img = pygame.image.load("box.png")
box_img = pygame.transform.scale(box_img, (120, 100))  # Increased size

banana_img = pygame.image.load("banana.png")
banana_img = pygame.transform.scale(banana_img, (80, 80))  # Increased size

# Object positions
monkey_x, monkey_y = 100, 500  # Monkey starts on the ground
box_x, box_y = 300, 500  # Box is placed before the banana
banana_x, banana_y = 500, 150  # Banana hanging from ceiling (adjusted for new size)
box_height = 100  # Updated box height

# Game state
on_box = False
grabbed = False
pushing_box = True

# Main loop
running = True
while running:
    screen.blit(background_img, (0, 0))  # Draw background

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pushing_box:
        # Move monkey towards the box with random pauses and step sizes
        if monkey_x < box_x:
            monkey_x += random.choice([2, 4, 6, 0])  # Random step size (including 0 for pauses)
            if random.random() < 0.1:  # 10% chance to pause
                time.sleep(0.2)
        elif monkey_x > box_x:
            monkey_x -= random.choice([2, 4, 6, 0])
            if random.random() < 0.1:
                time.sleep(0.2)
        else:
            # Push the box towards the banana with irregular movements
            if box_x < banana_x:
                step = random.choice([2, 3, 5])  # Random push step
                box_x += step
                monkey_x += step  # Monkey moves with the box
                if random.random() < 0.15:  # 15% chance to pause briefly
                    time.sleep(0.3)
            else:
                pushing_box = False  # Stop pushing once under banana
                time.sleep(0.5)  # Pause for realism

    else:
        # Monkey climbs onto the box with random steps
        if monkey_y > (box_y - 100):
            monkey_y -= random.choice([2, 4, 6])  # Random climbing speed
            if random.random() < 0.2:  # 20% chance to pause
                time.sleep(0.2)
        else:
            # Move up to banana height with slight variation
            if monkey_y > (banana_y + 20):
                monkey_y -= random.choice([2, 4, 5])
            else:
                grabbed = True  # Monkey grabs the banana
                running = False

    # Draw images
    screen.blit(box_img, (box_x, box_y))  # Draw box
    screen.blit(banana_img, (banana_x, banana_y))  # Draw banana
    screen.blit(monkey_img, (monkey_x, monkey_y))  # Draw monkey

    pygame.display.update()  # Refresh screen
    pygame.time.delay(50)  # Control speed

pygame.quit()

if grabbed:
    print("🎉 Monkey grabbed the banana! 🍌🐵")
else:
    print("Game exited.")
