import pygame
from sys import exit
from pygame import *
import os

class Main:
    
    def __init__(self) -> None:#初始化调用函数
        def quit(event):self.running=False
        self.call={QUIT:[quit,]}#在下面向call中添加事件类型：调用函数键值对，来使该函数在Update中正确调用
        
        pass

    def printfps(self):# 绘制帧率
        now = pygame.time.get_ticks()
        if now - self.start_time >= 100 :
            self.start_time = pygame.time.get_ticks()
            fps = self.clock.get_fps()  # 使用clock对象直接获取帧率
            self.fps_text = self.msyh10.render(f"FPS: {fps:.2f}", True, (0, 255, 0))
        self.screen.blit(self.fps_text, (10, 10))

    def PreUpdate(self):#更新前函数。向这里添加处理事件之前应该调用的函数。
        self.screen.fill(self.bgcolor)
        pass

    def Update(self):#更新函数。处理事件。无需更改，添加处理事件的函数请到__init__添加，非事件处理函数请到Pre和After中添加。
        for event in pygame.event.get():
            for func in self.call.get(event.type,[]):
                func(event)

    def AfterUpdate(self):#更新后函数。向这里添加处理事件之后应该调用的函数。
        self.printfps()
        pass
    
    def LateUpdate(self):#绘制后函数。一些特殊函数需要在这里调用。
        pass


    def Init(self):#初始化pygame和其他函数。
        self.displaysize = (640,480)
        self.fpslimit = -1
        pygame.init()
        #screen = pygame.display.set_mode((640, 480),pygame.RESIZABLE)
        self.screen = pygame.display.set_mode(self.displaysize)
        pygame.display.set_caption("apofai_player")
        self.clock = pygame.time.Clock()
        self.msyh24 = pygame.font.Font('msyh.ttc', 24)
        self.msyh10 = pygame.font.Font('msyh.ttc', 10)
        self.bgcolor = (0,0,0)
        #printfps
        self.start_time = pygame.time.get_ticks() - 100
        pass

    def Run(self):#pygame主循环
        self.running = True
        while self.running:
            self.PreUpdate()
            self.Update()
            self.AfterUpdate()
            pygame.display.flip()
            self.LateUpdate()
            self.clock.tick(self.fpslimit)

    def Del(self):#退出函数
        pygame.quit()
        exit()


    def main(self):#主函数
        self.Init()
        self.Run()
        self.Del()

if __name__ == "__main__":
    main = Main()
    main.main()