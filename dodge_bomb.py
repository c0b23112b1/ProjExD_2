import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1600, 900

DELTA = { #移動量辞書
        pg.K_UP:(0,-5),
        pg.K_DOWN:(0,+5),
        pg.K_LEFT:(-5,0),
        pg.K_RIGHT:(5,0)}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    """
    こうかとんRect　または　爆弾Rectの画面内外判定の関数
    引数：こうかとんRect，または，爆弾Rect
    戻り値：横方向判定結果，縦方向判定結果
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: #画像の右端，左端
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate

def game_over():
    """
    ゲームオーバー画面を表示する関数
    """
    fonto = pg.font.Font(None,200)
    pg.display.update()
    txt = fonto.render("Game Over",True,(255,255,255))
        
    #pg.draw.rect()
    time.sleep(5)
    return

    



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)

    
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400 #初期配置
    #爆弾
    bd_img = pg.Surface((20,20)) #1辺の長さ
    bd_img.set_colorkey((0,0,0)) #色変え
    pg.draw.circle(bd_img,(255,0,0),(10,10),10) #引数，色，中心座標，半径
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    vx,vy = +5,+5


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        if kk_rct.colliderect(bd_rct): #こうかとんと爆弾がぶつかったら
            gm_img = pg.Surface((1800,1800))
            pg.draw.rect(gm_img,(255,0,0),(0,0,1600,900))
            gm_img.set_colorkey((0,0,0))
            game_over()


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for k,v in DELTA.items(): #こうかとんの場所変化
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        screen.blit(kk_img, kk_rct)


        #爆弾
        bd_rct.move_ip(vx,vy)
        screen.blit(bd_img,bd_rct)
        yoko,tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
