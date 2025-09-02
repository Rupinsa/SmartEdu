import os
from dotenv import load_dotenv
from helpers.text_gen import generate_text
from helpers.image_gen import generate_image
from helpers.tts import text_to_speech
import pygame

# Load environment
load_dotenv()
os.makedirs("output", exist_ok=True)
os.makedirs("assets", exist_ok=True)

# Get input
topic = input("Enter a topic to explain: ")

print("\nExplaining...\n")
text = generate_text(topic)
print("\n--- Explanation ---\n", text)

# Save text
with open("output/explanation.txt", "w") as f:
    f.write(text)

# Voice
text_to_speech(text)

# Image generation
img_path = generate_image(topic)

# Show everything
if img_path:
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("EduComic Panel")
    image = pygame.image.load(img_path)
    image = pygame.transform.scale(image, (800, 600))
    screen.blit(image, (0, 0))
    pygame.display.update()

    pygame.mixer.init()
    pygame.mixer.music.load("output/explanation.mp3")
    pygame.mixer.music.play()

    # Keep window open until voice ends or user exits
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    pygame.quit()
