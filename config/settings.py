__author__ = "Zoulf"

import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pygame.init() # 游戏初始化
pygame.mixer.init() # 混合音初始化

# 游戏背景音乐
pygame.mixer.music.load(os.path.join(BASE_DIR, "material/sound/game_music.wav"))
pygame.mixer.music.set_volume(0.2)

# 子弹发射声音
bullet_sound = pygame.mixer.Sound("material/sound/bullet.wav")
bullet_sound.set_volume(0.2)

# 我方飞机阵亡声音
me_die_sound = pygame.mixer.Sound("material/sound/game_over.wav")
me_die_sound.set_volume(0.2)

# 敌方飞机挂了的音乐
enemy1_die_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, "material/sound/enemy1_down.wav"))
enemy1_die_sound.set_volume(0.2)
