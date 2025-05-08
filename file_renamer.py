import os
import pygame

files = os.listdir("images_old")

files.sort(key=lambda f: os.path.getmtime("images_old/"+f))

for i,f in enumerate(files):
    temp = pygame.image.load("images_old/"+f)
    pygame.image.save(temp,f"images/image_{i}.png")