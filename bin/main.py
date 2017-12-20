__author__ = "Zoulf"

import sys

from pygame.locals import *
from config.settings import *
from src.plane import Plane
from src.enemy import SmallEnemy
from src.bullet import Bullet

bg_size = 480, 700  # 初始化游戏背景大小(宽, 高)
screen = pygame.display.set_mode(bg_size) # 设置背景对话框
pygame.display.set_caption("Plane Wars") # 设置标题

backgroud = pygame.image.load(os.path.join(BASE_DIR, "material/image/background.png")) # 加载背景图片,并设置为不透明

# 血槽颜色绘制
color_black = (0, 0, 0)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_white = (255, 255, 255)

# 获取我方飞机
plane = Plane(bg_size)

def add_small_enemies(group1, group2, num):
    """
    添加小型敌机
    指定多个敌机对象添加到精灵组（sprite.group）
    参数group1、group2是两个精灵组类型的形参，用以存储多个精灵对象（敌机）。
    需要注意的一点是group既然是特定的精灵组结构体，在向其内部添加精灵对象时需要调用其对应的成员函数add()
    """
    for i in range(num):
        small_enemy = SmallEnemy(bg_size)
        group1.add(small_enemy)
        group2.add(small_enemy)

def main():
    me_destroy_index = 0
    bullets = []
    pygame.mixer.music.play(loops=-1) # loops = -1，音乐无限循环(默认循环播放一次)
    running = True
    delay = 60 # 对一些效果进行延迟，效果更好一些
    plane = Plane(bg_size)
    switch_image = False

    enemies = pygame.sprite.Group() # 生成敌方飞机组(一种精灵组用以存储所有敌机精灵)
    small_enemies = pygame.sprite.Group() # 敌方小型飞机组(不同型号敌机创建不同的精灵组来存储)

    add_small_enemies(small_enemies, enemies, 4) # 生成若干敌方小型飞机

    # 定义子弹, 各种敌机和我方敌机的毁坏图像索引
    bullet_index = 0
    e1_destroy_index = 0
    plane_destroy_index = 0

    # 定义子弹实例化个数
    bullet1 = []
    bullet_num = 6
    for i in range(bullet_num):
        bullet1.append(Bullet(plane.rect.midtop))

    while running:
        # 绘制背景图
        screen.blit(backgroud, (0, 0))

        # 飞机是喷气式的, 那么这个就涉及到一个帧数的问题
        clock = pygame.time.Clock()
        clock.tick(60)

        # 绘制我方飞机的两种不同状态，喷气时与不喷气时
        if not delay % 3:
            switch_image = not switch_image

        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)

                pygame.draw.line(screen, color_black,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)

                energy_remain = each.energy / SmallEnemy.energy
                # 如果血量大约百分之二十则为绿色，否则为红色
                if energy_remain > 0.2:
                    energy_color = color_green
                else:
                    energy_color = color_red

                pygame.draw.line(screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                 2)

                # 随机循环输出敌方小飞机
                for e in small_enemies:
                    e.move()
                    screen.blit(e.image, e.rect)
            else:
                while e1_destroy_index == 0:
                    e1_destroy_index_second = 0
                    screen.blit(each.destroy_images[e1_destroy_index_second], each.rect)
                    e1_destroy_index = (e1_destroy_index_second + 1) % 4
                    e1_destroy_index_second += 1
                enemy1_die_sound.play()
                each.reset()

        # 飞机存活状态
        if plane.active:
            if switch_image:
                screen.blit(plane.image_one, plane.rect)
            else:
                screen.blit(plane.image_two, plane.rect)

            # 飞机存活状态下才能发射子弹，且没10帧发射一颗移动的子弹
            if not (delay % 10):
                bullet_sound.play()
                bullets = bullet1
                bullets[bullet_index].reset(plane.rect.midtop)
                bullet_index = (bullet_index + 1) % bullet_num

            for b in bullets:
                # 只有激活的子弹才能击中敌机
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False,
                                                              pygame.sprite.collide_mask)
                    # 如果子弹击中敌机
                    if enemies_hit:
                        b.active = False # 子弹损毁
                        for e in enemies_hit:
                            e.active = False # 小型飞机被毁

        # 毁坏状态绘制爆炸的场面
        else:
            if not (delay % 3):
                while me_destroy_index == 0:
                    screen.blit(plane.destroy_images[plane_destroy_index], plane.rect)
                    # 四张图片切换实现动画效果
                    me_destroy_index = (plane_destroy_index + 1) % 4
                    plane_destroy_index += 1
                # 爆炸声音效果
                me_die_sound.play()
                plane.reset()

        # 调用 pygame 实现的碰撞方法 spritecollide (我方飞机如果和敌机碰撞, 更改飞机的存活属性)
        enemies_down = pygame.sprite.spritecollide(plane, enemies, False, pygame.sprite.collide_mask)
        if enemies_down:
            plane.active = False
            for enemy in enemies:
                enemy.active = False

        # 响应用户的操作
        for event in pygame.event.get():
            # 如果按下屏幕上的关闭按钮，触发quit事件，游戏退出
            if event.type == 12:
                pygame.quit()
                sys.exit()

        if delay == 0:
            delay = 60
        delay -= 1

        # 获取用户输入的所有键盘序列，如向上
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            plane.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            plane.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            plane.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            plane.move_right()

        # 再而我们将背景图像输出到屏幕上
        pygame.display.flip()