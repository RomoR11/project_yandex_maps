import os
import sys
import pygame
import requests

params = {'ll': '28.332373,57.819140',
          'z': 6, 'l': 'map'}
change_l = {'map': 'sat', 'sat': 'hybrid', 'hybrid': 'map'}
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
screen = pygame.display.set_mode((600, 500))
input_rect, search_rect = pygame.Rect((5, 455, 505, 40)), pygame.Rect((515, 455, 80, 40))
pygame.draw.rect(screen, 'white', (5, 455, 505, 40))
pygame.draw.rect(screen, 'grey', (515, 455, 80, 40))
font = pygame.font.Font(None, 25)
string_rendered = font.render('Искать', 1, pygame.Color('black'))
intro_rect = string_rendered.get_rect()
intro_rect.x = 530
intro_rect.y = 465
screen.blit(string_rendered, intro_rect)
screen.blit(pygame.image.load(map_file), (0, 0))
active = False
search = ''


def get_step(z):
    return (1 - z / 21) * 4


def get_coord(coord, event):
    x_coord, y_coord = coord
    if event.key == pygame.K_UP:
        y_coord += step if y_coord + step <= 90 else y_coord
    elif event.key == pygame.K_DOWN:
        y_coord -= step if y_coord - step >= -90 else y_coord
    elif event.key == pygame.K_LEFT:
        x_coord = x_coord - step if x_coord - step >= -180 else 180
    elif event.key == pygame.K_RIGHT:
        x_coord = x_coord + step if x_coord + step <= 180 else -180
    return f'{x_coord},{y_coord}'


def find_search(text):
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": text,
        "format": "json"}
    resp = requests.get("http://geocode-maps.yandex.ru/1.x/", params=geocoder_params).json()
    x, y = resp["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
    return ','.join([x, y])


if __name__ == '__main__':
    running = True
    step = get_step(params['z'])
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if search_rect.collidepoint(event.pos):
                    active = False
                    params['ll'] = find_search(search)
                    params['pt'] = f'{params["ll"]},pm2rdl'
                    search = ''
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
            elif event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        search = search[:-1]
                    else:
                        search += event.unicode
                if event.key == pygame.K_PAGEUP:
                    params['z'] += 1 if params['z'] < 21 else 0
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        step = get_step(params['z'])
                elif event.key == pygame.K_PAGEDOWN:
                    params['z'] -= 1 if params['z'] > 0 else 0
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                        step = get_step(params['z'])
                elif event.key == pygame.K_UP:
                    params['ll'] = get_coord([float(i) for i in params['ll'].split(',')], event)
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_DOWN:
                    params['ll'] = get_coord([float(i) for i in params['ll'].split(',')], event)
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_LEFT:
                    params['ll'] = get_coord([float(i) for i in params['ll'].split(',')], event)
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_RIGHT:
                    params['ll'] = get_coord([float(i) for i in params['ll'].split(',')], event)
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_1:
                    params['l'] = 'map'
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_2:
                    params['l'] = 'sat'
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
                elif event.key == pygame.K_3:
                    params['l'] = 'skl'
                    response = requests.get(url=map_request, params=params)
                    if response.status_code == 200:
                        with open(map_file, "wb") as file:
                            file.write(response.content)
                        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
os.remove(map_file)