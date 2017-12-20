简单的飞机大战。

程序结构:
Plane War/
|-- bin/
|   |-- main.py         程序运行主体程序
|-- config/
|   |-- settings.py     程序配置(例如: 游戏背景音乐的加载等)
|-- material            程序素材放置(打飞机游戏素材放置)
    |-- ...
|-- src/                程序主体模块存放
|   |-- __init__.py |   |-- bullet.py       我方飞机发射子弹实现代码存放
|   |-- enemy.py        敌方飞机实现代码存放
|   |-- plane.py        我方飞机实现代码存放
|-- begin.py           程序启动文件
|-- README.md

启动方法:
    在Plane War目录下打开python
    然后输入 python begin.py
