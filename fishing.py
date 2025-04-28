import cv2
import pygame
import random

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('釣魚遊戲')

# 載入背景圖片
background_image = pygame.image.load("background.png") 
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 調整背景圖片大小

# 載入魚的圖片
fish1_image = pygame.image.load("fish1.png")
fish1_image = pygame.transform.scale(fish1_image, (50,50))

fish2_image = pygame.image.load("fish2.png")
fish2_image = pygame.transform.scale(fish2_image, (50,50))

fishing_rod = pygame.image.load("fishingRod.png")
fishing_rod = pygame.transform.scale(fishing_rod, (50, 50))

# 初始化攝像頭
cap = cv2.VideoCapture(0)  # 使用預設攝像頭
if not cap.isOpened():
    print("無法打開攝像頭")
    exit()

# 設定魚的位置
fish_x = random.randint(50, screen_width - 50)
fish_y = random.randint(50, screen_height - 50)

score = 0
# 遊戲主循環
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        print("無法讀取攝像頭影像")
        break

    # 將影像轉為灰階來計算亮度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = gray.mean()  # 計算影像亮度的平均值

    # 繪製背景
    screen.blit(background_image, (0, 0))

    screen.blit(fishing_rod, (screen.get_width() - fishing_rod.get_width() - 10, 10))

    # 根據亮度決定魚的出現機率
    if brightness < 100:  # 當光線較暗時，顯示魚
        fish_x = random.randint(50, screen_width - 50)
        fish_y = random.randint(50, screen_height - 50)
        screen.blit(fish1_image, (fish_x, fish_y))  # 顯示魚圖片
    else:  # 當光線較強時，顯示較少的魚
        fish_x = random.randint(50, screen_width - 50)
        fish_y = random.randint(50, screen_height - 50)
        screen.blit(fish2_image, (fish_x, fish_y))  # 顯示魚圖片

    # 顯示目前的亮度值
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"亮度: {int(brightness)}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    text2 = font.render("分數: {score}", True, (0, 0, 0))
    screen.blit(text2, (15, 10))

    # 更新顯示
    pygame.display.update()

    # 處理退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 清理資源
cap.release()
pygame.quit()
