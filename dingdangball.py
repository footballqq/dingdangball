import pygame
import random
import time

# 初始化pygame
pygame.init()

# 设置窗口大小
screen_width = 500
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置标题
pygame.display.set_caption("小球游戏")

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 定义小球属性
ball_radius = 20
ball_x = screen_width // 2
ball_y = 20
ball_speed_x = 0
ball_speed_y = 0
gravity = 20
max_speed_y = 50
default_speed_y = 10
acceleration_y = 10

# 定义障碍物列表
obstacles = []

# 计时器
start_time = None
is_running = False
game_over = False

# 排名列表
rankings = []

# 生成随机颜色
def random_color():
    return (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

# 生成随机障碍物
def generate_obstacles(num_obstacles):
    obstacles.clear()
    attempts = 0
    while len(obstacles) < num_obstacles and attempts < 1000:
        shape = random.choice(['circle', 'ellipse', 'rect', 'square', 'triangle'])
        color = random_color()
        if shape == 'circle':
            radius = random.randint(10, 50)
            x = random.randint(radius, screen_width - radius)
            y = random.randint(radius, screen_height - radius)
            new_obstacle = {'type': 'circle', 'x': x, 'y': y, 'radius': radius, 'color': color}
        elif shape == 'ellipse':
            width = random.randint(30, 200)
            height = random.randint(30, 100)
            x = random.randint(0, screen_width - width)
            y = random.randint(0, screen_height - height)
            new_obstacle = {'type': 'ellipse', 'x': x, 'y': y, 'width': width, 'height': height, 'color': color}
        elif shape == 'rect' or shape == 'square':
            width = random.randint(30, 200)
            height = random.randint(30, 100) if shape == 'rect' else width
            x = random.randint(0, screen_width - width)
            y = random.randint(0, screen_height - height)
            new_obstacle = {'type': 'rect', 'x': x, 'y': y, 'width': width, 'height': height, 'color': color}
        elif shape == 'triangle':
            size = random.randint(30, 100)
            x = random.randint(size, screen_width - size)
            y = random.randint(size, screen_height - size)
            new_obstacle = {'type': 'triangle', 'x': x, 'y': y, 'size': size, 'color': color}

        # 检查新障碍物是否与现有障碍物相交
        intersects = False
        for obstacle in obstacles:
            if check_collision(new_obstacle, obstacle):
                intersects = True
                break

        if not intersects:
            obstacles.append(new_obstacle)
        attempts += 1

# 检查两个障碍物是否相交
def check_collision(obstacle1, obstacle2):
    if obstacle1['type'] == 'circle' and obstacle2['type'] == 'circle':
        distance = ((obstacle1['x'] - obstacle2['x'])**2 + (obstacle1['y'] - obstacle2['y'])**2)**0.5
        return distance < obstacle1['radius'] + obstacle2['radius']
    elif obstacle1['type'] == 'circle':
        return circle_rectangle_collision(obstacle1, obstacle2)
    elif obstacle2['type'] == 'circle':
        return circle_rectangle_collision(obstacle2, obstacle1)
    else:
        return rectangle_rectangle_collision(obstacle1, obstacle2)

# 检查圆形和矩形是否相交
def circle_rectangle_collision(circle, rect):
    if 'width' not in rect or 'height' not in rect:
        return False  # 如果不是矩形或椭圆，直接返回False
    closest_x = clamp(circle['x'], rect['x'], rect['x'] + rect['width'])
    closest_y = clamp(circle['y'], rect['y'], rect['y'] + rect['height'])
    distance = ((circle['x'] - closest_x)**2 + (circle['y'] - closest_y)**2)**0.5
    return distance < circle['radius']

# 检查两个矩形是否相交
def rectangle_rectangle_collision(rect1, rect2):
    if 'width' not in rect1 or 'height' not in rect1 or 'width' not in rect2 or 'height' not in rect2:
        return False  # 如果不是矩形或椭圆，直接返回False
    return (rect1['x'] < rect2['x'] + rect2['width'] and
            rect1['x'] + rect1['width'] > rect2['x'] and
            rect1['y'] < rect2['y'] + rect2['height'] and
            rect1['y'] + rect1['height'] > rect2['y'])

# 夹紧函数
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

# 游戏主循环
running = True
clock = pygame.time.Clock()

generate_obstacles(10)  # 生成10个障碍物

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not is_running:
                    start_time = time.time()
                    ball_x = screen_width // 2
                    ball_y = 20
                    ball_speed_x = 0
                    ball_speed_y = default_speed_y
                    is_running = True
                    game_over = False
                    generate_obstacles(10)  # 每次重新生成障碍物
                else:
                    is_running = False
            elif event.key == pygame.K_LEFT and is_running:
                if ball_speed_x > 0:
                    ball_speed_x = 0
                else:
                    ball_speed_x -= 20
            elif event.key == pygame.K_RIGHT and is_running:
                if ball_speed_x < 0:
                    ball_speed_x = 0
                else:
                    ball_speed_x += 20
            elif event.key == pygame.K_DOWN and is_running:
                ball_speed_y = max_speed_y

    if is_running:
        # 更新小球位置
        ball_x += ball_speed_x * (1 / 60)
        ball_y += ball_speed_y * (1 / 60)

        # 应用重力
        if ball_speed_y < max_speed_y:
            ball_speed_y += acceleration_y * (1 / 60)

        # 边界检测
        if ball_x < ball_radius:
            ball_x = ball_radius
            ball_speed_x = abs(ball_speed_x)
        elif ball_x > screen_width - ball_radius:
            ball_x = screen_width - ball_radius
            ball_speed_x = -abs(ball_speed_x)

        if ball_y < ball_radius:
            ball_y = ball_radius
            ball_speed_y = abs(ball_speed_y)
        elif ball_y > screen_height - ball_radius:
            ball_y = screen_height - ball_radius
            ball_speed_y = -abs(ball_speed_y)

        # 检测碰撞
        for obstacle in obstacles:
            if obstacle['type'] == 'circle':
                distance = ((ball_x - obstacle['x'])**2 + (ball_y - obstacle['y'])**2)**0.5
                if distance < ball_radius + obstacle['radius']:
                    ball_speed_y = -ball_speed_y
                    ball_speed_x = -ball_speed_x
            elif obstacle['type'] == 'ellipse' or obstacle['type'] == 'rect':
                if 'width' in obstacle and 'height' in obstacle:
                    if (ball_x > obstacle['x'] and ball_x < obstacle['x'] + obstacle['width']) and (ball_y > obstacle['y'] and ball_y < obstacle['y'] + obstacle['height']):
                        ball_speed_y = -ball_speed_y
            elif obstacle['type'] == 'triangle':
                # 简单处理，实际可能需要更复杂的碰撞检测逻辑
                if (ball_x > obstacle['x'] - obstacle['size'] and ball_x < obstacle['x'] + obstacle['size']) and (ball_y > obstacle['y'] - obstacle['size'] and ball_y < obstacle['y'] + obstacle['size']):
                    ball_speed_y = -ball_speed_y

        if ball_y >= screen_height - ball_radius:
            is_running = False
            game_over = True
            end_time = time.time()
            elapsed_time = end_time - start_time
            rankings.append(elapsed_time)
            rankings.sort()

    # 绘制背景
    screen.fill(WHITE)

    # 绘制小球
    pygame.draw.circle(screen, BLACK, (int(ball_x), int(ball_y)), ball_radius)

    # 绘制障碍物
    for obstacle in obstacles:
        if obstacle['type'] == 'circle':
            pygame.draw.circle(screen, obstacle['color'], (obstacle['x'], obstacle['y']), obstacle['radius'])
        elif obstacle['type'] == 'ellipse':
            pygame.draw.ellipse(screen, obstacle['color'], (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
        elif obstacle['type'] == 'rect':
            pygame.draw.rect(screen, obstacle['color'], (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))
        elif obstacle['type'] == 'triangle':
            point1 = (obstacle['x'], obstacle['y'] + obstacle['size'])
            point2 = (obstacle['x'] + obstacle['size'], obstacle['y'])
            point3 = (obstacle['x'] - obstacle['size'], obstacle['y'])
            pygame.draw.polygon(screen, obstacle['color'], [point1, point2, point3])

    # 显示游戏结束信息
    if game_over:
        font = pygame.font.Font(None, 36)
        text = font.render(f"Game Over! Time: {elapsed_time:.2f} seconds", True, RED)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
        pygame.draw.rect(screen, BLACK, (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
        screen.blit(text, text_rect)

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

# 退出pygame
pygame.quit()