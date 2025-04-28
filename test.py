# import cv2
import pygame
import random
import math

# 初始化 Pygame
pygame.init()

pygame.mixer.init()

# 載入背景音樂
pygame.mixer.music.load('audio.mp3')  # 載入音樂檔案
pygame.mixer.music.set_volume(0.5)  # 設定音樂音量（0.0到1.0）
pygame.mixer.music.play(-1, 0.0)  # 循環播放背景音樂（-1表示無限循環）

# 設定遊戲視窗大小
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('釣魚遊戲')

# 載入背景圖片
background_image = pygame.image.load("background2.jpg") 
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 調整背景圖片大小
init_background_image = pygame.image.load("init_background.jpg") 
init_background_image = pygame.transform.scale(init_background_image, (screen_width, screen_height))  # 調整背景圖片大小

# 載入魚的圖片
fish1_image = pygame.image.load("fish1.png")
fish1_image = pygame.transform.scale(fish1_image, (50,50))

fish2_image = pygame.image.load("fish2.png")
fish2_image = pygame.transform.scale(fish2_image, (50,50))

# fishing_rod = pygame.image.load("fishingRod.png")
# fishing_rod = pygame.transform.scale(fishing_rod, (150, 150))

hook = pygame.image.load("hook3.png")
hook = pygame.transform.scale(hook, (50, 90))


# 設定魚的位置
fish_x = random.randint(50, screen_width - 50)
fish_y = random.randint(50, screen_height - 50)

hook_x = screen.get_width() // 2
hook_y = 30

rod_tip_x = hook_x
rod_tip_y = 0

# 設定字體
font = pygame.font.SysFont(None, 60)
font_small = pygame.font.SysFont(None, 40)

# 初始畫面顯示文字
title_text = font.render('Go Fishing', True, (255, 255, 255))  # 遊戲名稱
start_text = font_small.render('START!', True, (255, 255, 255))  # 開始遊戲提示
quit_text = font_small.render('EXIT', True, (255, 255, 255))  # 退出遊戲提示

hook_speed = 0.1
hook_direction = 1 #1向右-1向左

score = 0
# 遊戲主循環
running = True
game_start = False
while running:
    if not game_start:
        screen.blit(init_background_image, (0, 0))
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))  # 遊戲名稱
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, 200))  # 開始遊戲提示
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 250))  # 退出遊戲提示

    else:
        # 繪製背景
                screen.blit(background_image, (0, 0))

                # screen.blit(fishing_rod, (screen.get_width() - fishing_rod.get_width() , 0))

                pygame.draw.line(screen, (0, 0, 0), (rod_tip_x, rod_tip_y), (hook_x, hook_y), 1)
                screen.blit(hook, ((hook_x - hook.get_width() // 2 - 10), hook_y))

                font = pygame.font.SysFont(None, 30)
                text2 = font.render(f"score: {int(score)}", True, (0, 0, 0))
                screen.blit(text2, (15, 10))

                hook_x += hook_speed * hook_direction

                # 如果碰到左右邊界，就反方向
                if hook_x >= screen.get_width() - 200 or hook_x <= 200:
                    hook_direction *= -1

    # 更新顯示
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not game_start:  # 按下 Enter 開始遊戲
                print("遊戲開始！")
                
                game_start = True
            elif event.key == pygame.K_ESCAPE:  # 按下 Esc 退出遊戲
                running = False


# 清理資源
# cap.release()
pygame.mixer.music.stop()
pygame.quit()
