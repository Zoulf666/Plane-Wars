__author__ = "Zoulf"

from random import randint

import pygame

class SmallEnemy(pygame.sprite.Sprite):
    """
    定义小飞机敌人
    """
    energy = 1

    def __init__(self, bg_size):
        super(SmallEnemy, self).__init__()
        self.image = pygame.image.load("material/image/enemy1.png")
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 2
        self.energy = SmallEnemy.energy
        # 定义敌机出现的位置，保证不会在程序刚开始时就出现敌机
        self.rect.left , self.rect.top = (
            randint(0, self.width - self.rect.width),
            randint(-5 * self.rect.height, -5)
        )
        self.active = True
        # 加载飞机被摧毁图片
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load("material/image/enemy1_down1.png"),
                pygame.image.load("material/image/enemy1_down2.png"),
                pygame.image.load("material/image/enemy1_down3.png"),
                pygame.image.load("material/image/enemy1_down4.png")
            ]
        )

    def move(self):
        """
        定义敌机的移动函数，因为是只是竖着走，所以只比较飞机顶部位置与总屏幕高度就行
        """
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        """
        当敌机向下移出屏幕，以及敌机死亡
        """
        self.rect.left, self.rect.top = (
            randint(0, self.width - self.rect.left),
            randint(-5 * self.rect.height, 0)
        )
        self.active = True
