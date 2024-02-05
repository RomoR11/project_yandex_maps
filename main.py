import os
import sys
import pygame
import requests

params = {'ll': '28.332373,57.819140',
          'z': 6, 'l': 'map'}
map_request = "http://static-maps.yandex.ru/1.x"
response = requests.get(url=map_request, params=params)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)
pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
if __name__ == '__main__':
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    params['z'] += 1 if params['z'] < 21 else 0
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_PAGEDOWN:
                    params['z'] -= 1 if params['z'] > 0 else 0
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
os.remove(map_file)