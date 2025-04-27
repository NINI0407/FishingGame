import pygame
import sounddevice as sd
import numpy as np
import random

# 初始化 Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("聲控釣魚遊戲 🎣")
clock = pygame.time.Clock()

# 浮標初始位置
bobber_x, bobber_y = 400, 300

# 魚初始位置
fish_x, fish_y = random.randint(100, 700), random.randint(400, 580)

# 分數
score = 0

# 音量偵測函數
def get_sound_level():
    duration = 0.1  # 每次錄製 0.1 秒
    sample_rate = 44100
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    volume_norm = np.linalg.norm(recording) * 10  # 音量放大調整
    return volume_norm

running = True
font = pygame.font.SysFont(None, 48)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 魚移動（讓魚會慢慢飄）
    fish_x += random.randint(-2, 2)
    fish_y += random.randint(-1, 1)

    # 防止魚游出界
    fish_x = max(50, min(750, fish_x))
    fish_y = max(400, min(580, fish_y))

    # 聲音偵測
    sound_level = get_sound_level()
    print(f"音量：{sound_level:.2f}")

    # 音量閾值，決定拉竿
    if sound_level > 3:  # 根據你的麥克風靈敏度可以調高低
        print("拉竿！")

        # 計算浮標跟魚的距離
        distance = ((bobber_x - fish_x) ** 2 + (bobber_y - fish_y) ** 2) ** 0.5
        if distance < 30:
            print("釣到魚了！🎯")
            score += 1
            # 魚重生
            fish_x, fish_y = random.randint(100, 700), random.randint(400, 580)
        else:
            print("沒釣到，魚跑掉了～")

    # 畫背景
    screen.fill((135, 206, 235))  # 天空藍
    pygame.draw.rect(screen, (0, 105, 148), (0, 400, 800, 200))  # 湖水

    # 畫浮標
    pygame.draw.circle(screen, (255, 0, 0), (int(bobber_x), int(bobber_y)), 10)

    # 畫魚
    pygame.draw.circle(screen, (255, 255, 0), (int(fish_x), int(fish_y)), 15)

    # 顯示分數
    score_text = font.render(f"分數: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
