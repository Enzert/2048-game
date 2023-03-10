from logics import *
import pygame
import sys
from database import get_best, cur, insert_result
import json
import os

GAMERS_DB = get_best()

COLORS = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 120),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 120),
    64: (255, 235, 0),
    128: (255, 120, 120),
    256: (255, 0, 255),
    512: (255, 0, 255),
    1024: (255, 0, 255),
    2048: (255, 0, 255),
    4096: (255, 0, 255)
}

WHITE = (255, 255, 255)
GRAY = (130, 130, 130)
BLACK = (0, 0, 0)
TEXT_COLOR = (255, 127, 0)

BLOCKS = 4
SIZE_BLOCK = 110
MARGIN = 10
WIDTH = BLOCKS * SIZE_BLOCK + (BLOCKS + 1) * MARGIN
HEIGHT = WIDTH + SIZE_BLOCK
TITLE_REC = pygame.Rect(0, 0, WIDTH, 110)


def draw_top_gamers():
    font_top = pygame.font.SysFont("comicsansms", 25)
    font_gamer = pygame.font.SysFont("comicsansms", 16)
    text_head = font_top.render("Best tries: ", True, TEXT_COLOR)
    screen.blit(text_head, (250, 5))
    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f"{index + 1}. {name} - {score}"
        text_gamer = font_gamer.render(s, True, TEXT_COLOR)
        screen.blit(text_gamer, (250, 35 + 25 * index))
        print(s)


def init_const(score, mas):
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_numder(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_numder(random_num2)
    mas = insert_2_or_4(mas, x2, y2)
    score = 0
    return score, mas


def draw_interface(score, mas, delta=0):
    pygame.draw.rect(screen, WHITE, TITLE_REC)
    font = pygame.font.SysFont("comicsansms", 50)
    font_score = pygame.font.SysFont("comicsansms", 35)
    font_delta = pygame.font.SysFont("comicsansms", 25)
    text_score = font_score.render("Score: ", True, TEXT_COLOR)
    text_score_value = font_score.render(f"{score}", True, TEXT_COLOR)
    screen.blit(text_score, (20, 25))
    screen.blit(text_score_value, (155, 25))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, TEXT_COLOR)
        screen.blit(text_delta, (170, 65))
    pretty_print(mas)
    draw_top_gamers()
    for row in range(BLOCKS):
        for column in range(BLOCKS):
            value = mas[row][column]
            text = font.render(f'{value}', True, BLACK)
            w = column * SIZE_BLOCK + (column + 1) * MARGIN
            h = row * SIZE_BLOCK + (row + 1) * MARGIN + SIZE_BLOCK
            pygame.draw.rect(screen, COLORS[value], (w, h, SIZE_BLOCK, SIZE_BLOCK))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (SIZE_BLOCK - font_w) / 2
                text_y = h + (SIZE_BLOCK - font_h) / 2
                screen.blit(text, (text_x, text_y))


mas = None
score = None
USERNAME = None
path = os.getcwd()


def load_game():
    with open('data.txt') as file:
        data = json.load(file)
        mas = data['mas']
        score = data['score']
        USERNAME = data['user']
    full_path = os.path.join(path, 'data.txt')
    os.remove(full_path)
    return USERNAME, score, mas


# print(get_empty_list(mas))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


def draw_intro(USERNAME):
    img2048 = pygame.image.load("1404598408_1.png")
    font = pygame.font.SysFont("comicsansms", 50)
    text_welcome = font.render("Welcome! ", True, WHITE)
    name = 'Enter username:'
    is_find_name = False

    while not is_find_name:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == 'Enter username:':
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        USERNAME = name
                        is_find_name = True
                        break

        screen.fill(BLACK)
        text_name = font.render(name, True, WHITE)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center

        screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
        screen.blit(text_welcome, (240, 70))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(BLACK)
    return USERNAME


def draw_game_over(name, score, mas, db):
    new_start = False
    while not new_start:
        img2048 = pygame.image.load("1404598408_1.png")
        font = pygame.font.SysFont("comicsansms", 50)
        font1 = pygame.font.SysFont("comicsansms", 30)
        text_over = font.render("Game over! ", True, WHITE)
        text_hint1 = font1.render("Press 'Space' to try again", True, GRAY)
        text_hint2 = font1.render("Press 'Enter' to start new game", True, GRAY)
        text_score = font.render(f"Your score: {score} ", True, WHITE)
        best_score = db[0][1]
        if score > best_score:
            text = "New record!"
        else:
            text = f"Record: {best_score}"
        text_record = font.render(text, True, WHITE)

        make_decision = False

        while not make_decision:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # restart game with name
                        make_decision = True
                        screen.fill(BLACK)
                        insert_result(*game_loop(name, *init_const(score, mas)))
                    elif event.key == pygame.K_RETURN:
                        # restart game without name
                        new_start = True
                        make_decision = True

            screen.fill(BLACK)
            screen.blit(text_over, (220, 80))
            screen.blit(text_score, (30, 250))
            screen.blit(text_record, (30, 320))
            screen.blit(text_hint1, (60, 440))
            screen.blit(text_hint2, (30, 480))
            screen.blit(pygame.transform.scale(img2048, [200, 200]), [10, 10])
            pygame.display.update()
        insert_result(name, score)
        db = get_best()
    screen.fill(BLACK)


def save_game(USERNAME, score, mas):
    data = {
        'user': USERNAME,
        'score': score,
        'mas': mas
    }
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)


def game_loop(USERNAME, score, mas):
    draw_interface(score, mas)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or possible_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(USERNAME, score, mas)
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = move_left(mas)
                    score += delta
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                    score += delta
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                    score += delta
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                    score += delta
                if is_zero_in_mas(mas) and is_mas_move:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_numder(random_num)
                    insert_2_or_4(mas, x, y)
                    print(f'???? ?????????????????? ?????????????? ?????? ?????????????? {random_num}')
                    is_mas_move = False
                draw_interface(score, mas, delta)
                pygame.display.update()
    draw_game_over(USERNAME, score, mas, GAMERS_DB)
    return USERNAME, score


while True:
    if 'data.txt' in os.listdir(path):
        game_loop(*load_game())
    if USERNAME is None:
        game_loop(draw_intro(USERNAME), *(init_const(score, mas)))
