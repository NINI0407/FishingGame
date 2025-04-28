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

# 初始化攝像頭
cap = cv2.VideoCapture(0)  # 使用預設攝像頭
if not cap.isOpened():
    print("無法打開攝像頭")
    exit()

# 設定魚的位置
fish_x = random.randint(50, screen_width - 50)
fish_y = random.randint(50, screen_height - 50)
fish_speed_x = random.choice([-1, 1]) * random.uniform(0.5, 2)
fish_speed_y = random.choice([-1, 1]) * random.uniform(0.5, 2)


# 遊戲主循環
clock = pygame.time.Clock()
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

    # 更新魚的位置
    fish_x += fish_speed_x
    fish_y += fish_speed_y

    # 如果魚碰到邊界，讓牠反向游
    if fish_x <= 0 or fish_x >= screen_width - 50:
        fish_speed_x *= -1
    if fish_y <= 0 or fish_y >= screen_width - 50:
        fish_speed_y *= -1

    #有小機率讓魚的方向稍微改變，增加自然感
    if random.random() < 0.01:
        fish_speed_x += random.uniform(-0.5, 0.5)
        fish_speed_y += random.uniform(-0.5, 0.5)

    #限制最大速度
    fish_speed_x = max(min(fish_speed_x, 2), -2)
    fish_speed_y = max(min(fish_speed_y, 2), -2)

    # 根據亮度決定魚的出現機率
    if brightness < 150:
        screen.blit(fish1_image, (fish_x, fish_y))

    # 顯示目前的亮度值
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"亮度: {int(brightness)}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # 更新顯示
    pygame.display.update()

    # 控制FPS，讓魚游得平順（比如每秒30幀）
    clock.tick(30)

    # 處理退出事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 清理資源
cap.release()
pygame.quit()
