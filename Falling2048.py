from dataclasses import field
from operator import truediv
from tkinter import font
from turtle import screensize
import pygame
from pygame.locals import *
import sys
import math
from random import randint as rnd
import time

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# nums
SIZE = 70
FONT_SIZE = 40
FIELD_W = 5
FIELD_H = 6

# enums
ANI_CONBINE = 1
ANI_FALL = 2

DIR_LEFT = [-1, 0]
DIR_RIGHT = [1, 0]
DIR_DOWN = [0, 1]

# colors
C_TEXT = (255,255,255)
C_FRAME = (255,255,255)
C_BACKGROUND = (0,0,0)

# functions
def draw_text(str:str, x:int, y:int) -> None:
    """
    文字列strを描画します。(x,y)に描画します
    """
    global screen
    global font
    src = font.render(str, True, C_TEXT)
    screen.blit(src, [x, y])

def draw_block(num:int, x:int, y:int) -> None:
    """
    numと書かれたcol色のブロックを(x,y)に描画します
    """
    global screen
    global font
    r = 237*num % 256
    g = 211*num % 256
    b = 179*num % 256
    col = (r, g, b)
    pygame.draw.rect(screen, col, (x, y, SIZE, SIZE))
    (w, h) = font.size(str(2**num))
    _x = x+SIZE/2-w/2
    _y = y+SIZE/2-h/2
    draw_text(str(2**num), _x, _y)

def get_top_y(x:int) -> int:
    """
    x列目の一番上にあるブロックのy座標を返します
    """
    global field
    for y in range(FIELD_H):
        if field[y][x] > 0:
            return y
    return FIELD_H

def is_fallable(x:int, y:int) -> bool:
    """
    フィールド(x, y)の下に0ブロックがあるかどうかを返します
    """
    global field
    for _y in range(y+1, FIELD_H):
        if field[_y][x] == 0:
            return True
    return False
def start_game() -> None:
    """
    ゲームをスタートします
    """
    global field
    global is_moving
    global next_moving_num
    global horizontal_input
    global horizontal_delay
    global down_input
    global game_over
    global score

    field = [[0 for i in range(FIELD_W)] for j in range(FIELD_H)]
    is_moving = False
    next_moving_num = rnd(1, 5)
    horizontal_input = 0
    horizontal_delay = 0
    down_input = 0
    game_over = False
    score = 0

def set_animation():
    """
    今のフィールドの状態に応じて、アニメーションを設定します
    """
    global animation_place
    global animation_directions
    global is_animating
    global animation_progress
    global animation_type
    global fall_map
    # 結合
    for y in range(FIELD_H-1):
        for x in range(1, FIELD_W-1):
            if field[y][x] > 0 and field[y][x] == field[y+1][x] == field[y][x-1] == field[y][x+1]:
                animation_place = [x, y]
                animation_directions = [DIR_DOWN, DIR_LEFT, DIR_RIGHT]
                is_animating = True
                animation_progress = 0
                animation_type = ANI_CONBINE
                return
    for y in range(FIELD_H):
        for x in range(1, FIELD_W-1):
            if field[y][x] > 0 and field[y][x] == field[y][x-1] == field[y][x+1]:
                animation_place = [x, y]
                animation_directions = [DIR_LEFT, DIR_RIGHT]
                is_animating = True
                animation_progress = 0
                animation_type = ANI_CONBINE
                return
    for y in range(FIELD_H-1):
        for x in range(0, FIELD_W-1):
            if field[y][x] > 0 and field[y][x] == field[y+1][x] == field[y][x+1]:
                animation_place = [x, y]
                animation_directions = [DIR_DOWN, DIR_RIGHT]
                is_animating = True
                animation_progress = 0
                animation_type = ANI_CONBINE
                return
    for y in range(FIELD_H-1):
        for x in range(1, FIELD_W):
            if field[y][x] > 0 and field[y][x] == field[y+1][x] == field[y][x-1]:
                animation_place = [x, y]
                animation_directions = [DIR_DOWN, DIR_LEFT]
                is_animating = True
                animation_progress = 0
                animation_type = ANI_CONBINE
                return
    for y in range(FIELD_H-1):
        for x in range(FIELD_W):
            if field[y][x] > 0 and field[y][x] == field[y+1][x]:
                animation_place = [x, y]
                animation_directions = [DIR_DOWN]
                is_animating = True
                animation_progress = 0
                animation_type = ANI_CONBINE
                return
    for y in range(FIELD_H):
        for x in range(FIELD_W-1):
            if field[y][x] > 0 and field[y][x] == field[y][x+1]:
                animation_place = [x, y]
                animation_directions = [DIR_RIGHT]
                is_animating = True
                animation_progress = 0
                animation_type = ANI_CONBINE
                return
    # 落下
    fall_map = [[0 for i in range(FIELD_W)] for j in range(FIELD_H)]
    is_falling = False
    for y in range(FIELD_H):
        for x in range(FIELD_W):
            if field[y][x] > 0 and is_fallable(x, y):
                is_falling = True
                fall_map[y][x] = 1
    if is_falling:
        is_animating = True
        animation_progress = 0
        animation_type = ANI_FALL

def is_animating_place(x:int, y:int) -> bool:
    """
    フィ―ルド上の座標(x, y)がアニメーション中か否かを返します
    """
    global animation_directions
    global animation_place
    global animation_type
    global fall_map
    if animation_type == ANI_CONBINE:
        for i in animation_directions:
            if x == animation_place[0] + i[0] and y == animation_place[1] + i[1]:
                return True
    elif animation_type == ANI_FALL:
        if fall_map[y][x] == 1:
            return True 
    return False
        

    

    
    

def main():
    global screen
    global font
    global field
    global is_moving
    global next_moving_num
    global horizontal_input
    global horizontal_delay
    global down_input
    global game_over
    global animation_place
    global animation_directions
    global is_animating
    global animation_progress
    global animation_type
    global fall_map
    global score

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    myclock = pygame.time.Clock() 
    pygame.display.set_caption("Falling2048")
    running = True
    font = pygame.font.Font(None, FONT_SIZE)

    # ブロックの数値データを格納するリスト
    field = [[0 for i in range(FIELD_W)] for j in range(FIELD_H)]
    score = 0

    # ----------操作中のブロックに関する変数----------
    is_moving = False # 操作中か否か
    moving_xy = [-1, -1] # 座標
    moving_num = 0 # ブロックの数字
    fall_spd = 0.04 # 落ちるスピード
    add_delay = 10 # 次のブロックが追加されるまでの時間
    next_moving_num = rnd(1, 5) # 次にくるブロックの数字
    horizontal_input = 0 # 水平方向のキー入力
    horizontal_delay = 0 # 再度水平方向の操作が可能になるまでの時間
    down_input = 0 # 下方向のキー入力

    # ----------アニメーションに関する変数----------
    is_animating = False # アニメーションを行っているか否か
    animation_type = 0 # 現在行われているアニメーションのタイプ
    animation_progress = 0 # アニメーションの進捗([0, 1])
    animation_place = False # 現在アニメーションが行われている場所
    animation_directions = [] # アニメーションの向き
    fall_map = [] # 落ちてくるブロックの情報

    # ゲームオーバーか否か
    game_over = False

    while (running): 
        screen.fill(C_BACKGROUND)
        draw_text("SCORE", 450, 100)
        draw_text(str(score), 550-font.size(str(score))[0], 150)
        draw_text("NEXT", 450, 200)
        pygame.draw.line(screen, C_FRAME, (50,100), (50,520), 3)
        pygame.draw.line(screen, C_FRAME, (50,520), (400,520), 3)
        pygame.draw.line(screen, C_FRAME, (400,520), (400,100), 3)
        

        # キー取得
        pressed = pygame.key.get_pressed()

        # キー入力
        if horizontal_delay > 0:
            horizontal_delay -= 1
        if horizontal_delay == 0 and is_moving:
            if pressed[K_LEFT]:
                horizontal_input -= 1
                horizontal_delay = 8
            if pressed[K_RIGHT]:
                horizontal_input += 1
                horizontal_delay = 8
        if pressed[K_DOWN]:
            down_input = 1
        if game_over:
            if pressed[K_r]:
                start_game()

        # ゲームの数値処理
        if not game_over:
            if not is_animating:
                if is_moving:
                    # キーでの移動
                    if horizontal_input == 1 and moving_xy[0] < FIELD_W-1 and moving_xy[1] > -1 and field[math.ceil(moving_xy[1])][moving_xy[0]+1] == 0:
                        moving_xy[0] += 1
                    elif horizontal_input == -1 and moving_xy[0] > 0 and moving_xy[1] > -1 and field[math.ceil(moving_xy[1])][moving_xy[0]-1] == 0:
                        moving_xy[0] -= 1
                    # 非接地
                    if moving_xy[1] < FIELD_H-1 and field[math.floor(moving_xy[1])+1][moving_xy[0]] == 0:
                        moving_xy[1] += fall_spd
                        if down_input: moving_xy[1] += 0.1
                        moving_xy[1] = min(moving_xy[1], get_top_y(moving_xy[0])-1)
                    # 接地
                    else:
                        # 設置
                        if get_top_y(moving_xy[0]) > 0:
                            field[int(moving_xy[1])][moving_xy[0]] = moving_num
                        else:
                            # もし最高まで積みあがっていたらゲームオーバー
                            game_over = True
                        add_delay = 10
                        is_moving = False
                else:
                    if add_delay > 0:
                        add_delay -= 1
                    elif add_delay == 0:
                        # ブロック追加 
                        is_moving = True
                        moving_num = next_moving_num
                        next_moving_num = rnd(1, 5)
                        moving_xy = [rnd(0, FIELD_W-1), -1]
            
            # アニメーション更新
            if is_animating:
                if animation_type == ANI_CONBINE:
                    if animation_progress < 1:
                        animation_progress = min(animation_progress+0.05, 1)
                    elif animation_progress == 1:
                        for i in animation_directions:
                            field[animation_place[1]][animation_place[0]] += 1
                            field[animation_place[1]+i[1]][animation_place[0]+i[0]] = 0
                            # スコア加算
                            score += 2**(field[animation_place[1]][animation_place[0]]-1)
                        is_animating = False
                elif animation_type == ANI_FALL:
                    if animation_progress < 1:
                        animation_progress = min(animation_progress+0.05, 1)
                    elif animation_progress == 1:
                        for y in range(FIELD_H-1, -1, -1):
                            for x in range(FIELD_W):
                                if fall_map[y][x] == 1:
                                    field[y+1][x] = field[y][x]
                                    field[y][x] = 0
                        is_animating = False
            else:
                set_animation()

        
        horizontal_input = 0
        down_input = 0

        # ブロックの描画  
        for y in range(FIELD_H):
            for x in range(FIELD_W):
                if field[y][x] > 0:
                    if is_animating and is_animating_place(x, y):
                        continue
                    else:
                        draw_block(field[y][x], 50+SIZE*x, 100+SIZE*y)
        if is_moving:
            draw_block(moving_num, 50+SIZE*moving_xy[0], 100+SIZE*moving_xy[1])
        if is_animating:
            if animation_type == ANI_CONBINE:
                for i in animation_directions:
                    _x = animation_place[0] + i[0]
                    _y = animation_place[1] + i[1]
                    draw_block(field[_y][_x], 50+SIZE*(_x-i[0]*animation_progress), 100+SIZE*(_y-i[1]*animation_progress))
            elif animation_type == ANI_FALL:
                for y in range(FIELD_H):
                    for x in range(FIELD_W):
                        if fall_map[y][x] == 1:
                            draw_block(field[y][x], 50+SIZE*(x), 100+SIZE*(y+animation_progress))
        draw_block(next_moving_num, 450, 250)

        # ゲームオーバーメッセージ描画
        if game_over:
            pygame.draw.rect(screen, C_BACKGROUND, (20, 260, 430, 110))
            draw_text("GAME OVER", 150, 270)
            draw_text('PRESS "R" TO RESTART GAME', 30, 330)
        
        # print(str(is_animating)+", "+str(animation_place)+", "+str(animation_progress))
        pygame.display.update()
        pygame.display.flip()
        myclock.tick(60)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False              
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()

# pyinstaller C:\Users\yuito\Documents\Works\Code\Python\Pygame\Falling2048.py --onefile --noconsole
# python C:\Users\yuito\Documents\Works\Code\Python\Pygame\Falling2048.py