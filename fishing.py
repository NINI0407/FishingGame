import cv2
import pygame
import random
import numpy as np

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
screen_width = 640
screen_height = 480
max_x = 600
max_y = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('釣魚遊戲')

# 載入背景圖片
background_image = pygame.image.load("background.png") 
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # 調整背景圖片大小
background_array = pygame.surfarray.array3d(background_image)

# 載入魚的圖片
fish_images = []
for i in range(1, 5): 
    img = pygame.image.load(f"fish{i}.png")
    img = pygame.transform.scale(img, (50, 50))
    fish_images.append(img)

# 載入垃圾的圖片
trash_images = []
for i in range(1, 2): 
    img = pygame.image.load(f"trash{i}.png")
    img = pygame.transform.scale(img, (50, 50))
    trash_images.append(img)

# 載入魚桿的圖片
hook = pygame.image.load("hook3.png")
hook = pygame.transform.scale(hook, (50, 90))

hook_x = screen.get_width() // 2
hook_y = 30

rod_tip_x = hook_x
rod_tip_y = 0

hook_speed = 1
hook_direction = 1 #1向右-1向左

# 初始化攝像頭
cap = cv2.VideoCapture(0)  # 使用預設攝像頭
if not cap.isOpened():
    print("無法打開攝像頭")
    exit()

# 設定魚的位置
fish_pos = []
for _ in range(10):
    fish = {
        "x": random.randint(0, max_x),
        "y": random.randint(60, max_y),
        "speed_x": random.uniform(-2, 2),
        "speed_y": random.uniform(0, 2),
        "image": random.choice(fish_images),
    }
    fish["image_flip"] = pygame.transform.flip(fish["image"], True, False)
    fish_pos.append(fish)

# 設定垃圾的位置
trash_pos = []
for _ in range(4):
    trash = {
        "x": random.randint(0, max_x),
        "y": random.randint(60, max_y),
        "speed_x": random.uniform(-2, 2),
        "speed_y": random.uniform(0, 2),
        "image": random.choice(trash_images),
    }
    trash_pos.append(trash)

score = 0
hook_returning = False
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
    # brightness_factor = 1 + (brightness - 150) / 100
    # adjusted_background_array = np.clip(background_array * brightness_factor, 0, 255).astype(np.uint8)
    # adjusted_background_image = pygame.surfarray.make_surface(adjusted_background_array)


    # 繪製背景
    screen.blit(background_image, (0, 0))

    # 創建灰階遮罩層
    gray_surface = pygame.Surface((screen_width, screen_height))
    gray_surface.fill((brightness,brightness,brightness))
    alpha = 255 - brightness #透明度
    gray_surface.set_alpha(alpha)
    

    #魚線擺動
    pygame.draw.line(screen, (0, 0, 0), (rod_tip_x, rod_tip_y), (hook_x, hook_y), 1)
    screen.blit(hook, ((hook_x - hook.get_width() // 2 - 10), hook_y))
    
    # 更新魚的位置
    for fish in fish_pos:
        fish["x"] += fish["speed_x"]
        fish["y"] += fish["speed_y"]

        # 如果魚碰到邊界，讓牠反向游
        if fish["x"] <= 0 or fish["x"] >= max_x:
            fish["speed_x"] *= -1
        if fish["y"] <= 70 or fish["y"] >= max_y:
            fish["speed_y"] *= -1

        #有小機率讓魚的方向稍微改變，增加自然感
        if random.random() < 0.01:
            fish["speed_x"] += random.uniform(-0.5, 0.5)
            fish["speed_y"] += random.uniform(-0.5, 0.5)

        #限制最大速度
        fish["speed_x"] = max(min(fish["speed_x"], 2), -2)
        fish["speed_y"] = max(min(fish["speed_y"], 2), -2)

    # 更新垃圾的位置
    for trash in trash_pos:
        trash["x"] += trash["speed_x"]
        trash["y"] += trash["speed_y"]

        # 如果垃圾碰到邊界，讓牠反向游
        if trash["x"] <= 0 or trash["x"] >= max_x:
            trash["speed_x"] *= -1
        if trash["y"] <= 70 or trash["y"] >= max_y:
            trash["speed_y"] *= -1

        #限制最大速度
        trash["speed_x"] = max(min(trash["speed_x"], 2), -2)
        trash["speed_y"] = max(min(trash["speed_y"], 2), -2)

    #防止鉤子超出畫面
    if hook_y > screen_height - 50:
        hook_y = screen_height - 50

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        hook_x -= 1
    if keys[pygame.K_RIGHT]:
        hook_x += 1
    if keys[pygame.K_DOWN]:
        hook_y += 1
    if keys[pygame.K_UP]:
        hook_y -= 1

    # 根據亮度決定魚的出現機率
    if brightness < 100:
        for fish in fish_pos: 
            if fish["speed_x"] < 0:
                screen.blit(fish["image_flip"], (fish["x"], fish["y"]))
            else:
                screen.blit(fish["image"], (fish["x"], fish["y"]))
        
        for trash in trash_pos:
            screen.blit(trash["image"], (trash["x"], trash["y"]))

    elif brightness > 100 and brightness < 150:
        for fish in fish_pos[1:7]: 
            if fish["speed_x"] < 0:
                screen.blit(fish["image_flip"], (fish["x"], fish["y"]))
            else:
                screen.blit(fish["image"], (fish["x"], fish["y"]))

        for trash in trash_pos:
            screen.blit(trash["image"], (trash["x"], trash["y"]))

    else:
        for fish in fish_pos[6:]:
            if fish["speed_x"] < 0:
                screen.blit(fish["image_flip"], (fish["x"], fish["y"]))
            else:
                screen.blit(fish["image"], (fish["x"], fish["y"]))
        for trash in trash_pos:
            screen.blit(trash["image"], (trash["x"], trash["y"]))

    #繪製灰色遮罩
    screen.blit(gray_surface, (0,0))

    # 顯示目前的亮度值
    font = pygame.font.SysFont(None, 30)
    text = font.render(f"light:{int(brightness)}", True, (0, 0, 0))
    screen.blit(text, (30, 40))

    #碰到魚
    for fish in fish_pos[:]:
        fish_rect = pygame.Rect(fish["x"], fish["y"], 50, 50)
        hook_rect = pygame.Rect(hook_x - 25, hook_y, 50, 70)
        if hook_rect.colliderect(fish_rect):
            fish["x"] = random.randint(0, max_x)
            fish["y"] = random.randint(60, max_y)
            score += 10
            hook_returning = True
    # 碰到垃圾
    for trash in trash_pos[:]:
        trash_rect = pygame.Rect(trash["x"], trash["y"], 50, 50)
        if hook_rect.colliderect(trash_rect):
            trash["x"] = random.randint(0, max_x)
            trash["y"] = random.randint(60, max_y)
            score -= 5
            hook_returning = True

    #分數
    text2 = font.render(f"score: {int(score)}", True, (0, 0, 0))
    screen.blit(text2, (15, 10))

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
