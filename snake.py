import tkinter as tk
import random

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="black", width=600, height=600)
canvas.pack()

grid_size = 20
TICK_MS = 70
BONUS_DURATION_MS = 5000
game_mode = "Normal"

def create_snake():
    cells = 600 // grid_size
    y_cell = random.randrange(0, cells)
    x_cell = random.randrange(2, cells)
    head_x = x_cell * grid_size
    head_y = y_cell * grid_size
    return [[head_x, head_y], [head_x - grid_size, head_y], [head_x - 2 * grid_size, head_y]]

snake = create_snake()
direction = "Right"
next_direction = "Right"
score = 0
state = "start"
after_id = None
food_eaten = 0
bonus_x = None
bonus_y = None
bonus_timer = 0

def create_food():
    while True:
        x = random.randrange(0, 600, grid_size)
        y = random.randrange(0, 600, grid_size)
        if [x, y] not in snake:
            return x, y

def create_bonus():
    while True:
        x = random.randrange(0, 600, grid_size)
        y = random.randrange(0, 600, grid_size)
        if [x, y] not in snake and (x != food_x or y != food_y):
            return x, y

food_x, food_y = create_food()

def change_direction(event):
    global direction, next_direction, state, TICK_MS, game_mode
    new_dir = event.keysym
    if state == "start":
        if new_dir in ("1", "2", "3"):
            if new_dir == "1":
                TICK_MS = 120
                game_mode = "Easy"
            elif new_dir == "2":
                TICK_MS = 80
                game_mode = "Normal"
            elif new_dir == "3":
                TICK_MS = 50
                game_mode = "Hard"
            start_game()
            return
        if new_dir in ("space", "Space"):
            TICK_MS = 80
            game_mode = "Normal"
            start_game()
            return
    if state == "gameover" and new_dir in ("q", "Q"):
        root.destroy()
        return
    if new_dir in ("r", "R"):
        restart_game()
        return
    if state != "playing":
        return
    if new_dir not in ("Up", "Down", "Left", "Right"):
        return
    if direction == "Up" and new_dir == "Down":
        return
    if direction == "Down" and new_dir == "Up":
        return
    if direction == "Left" and new_dir == "Right":
        return
    if direction == "Right" and new_dir == "Left":
        return
    next_direction = new_dir

root.bind("<KeyPress>", change_direction)

def draw_start_screen():
    canvas.delete("all")
    canvas.create_text(300, 250, fill="white", text="Snake Game", font=("Arial", 36))
    canvas.create_text(300, 310, fill="white", text="1 Easy   2 Normal   3 Hard", font=("Arial", 16))
    canvas.create_text(300, 340, fill="white", text="Press Space for Normal", font=("Arial", 14))

def start_game():
    global state, after_id
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    state = "playing"
    game_loop()

def restart_game():
    global snake, direction, next_direction, score, food_x, food_y, state, after_id, food_eaten, bonus_x, bonus_y, bonus_timer
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    snake = create_snake()
    direction = "Right"
    next_direction = "Right"
    score = 0
    state = "playing"
    food_eaten = 0
    bonus_x = None
    bonus_y = None
    bonus_timer = 0
    food_x, food_y = create_food()
    canvas.delete("all")
    game_loop()

def game_loop():
    global snake, food_x, food_y, score, state, direction, next_direction, after_id, food_eaten, bonus_x, bonus_y, bonus_timer
    if state == "start":
        draw_start_screen()
        return
    if state == "gameover":
        canvas.delete("all")
        for i, (x, y) in enumerate(snake):
            if i == 0:
                color = "lime"
            elif i == len(snake) - 1:
                color = "#004400"
            else:
                color = "green"
            canvas.create_rectangle(x, y, x + grid_size, y + grid_size, fill=color)
        canvas.create_rectangle(food_x, food_y, food_x + grid_size, food_y + grid_size, fill="red")
        canvas.create_text(10, 10, anchor="nw", fill="white", text=f"Score: {score}")
        canvas.create_text(300, 280, fill="white", text="Game Over", font=("Arial", 32))
        canvas.create_text(300, 330, fill="white", text="Press R to restart", font=("Arial", 14))
        return

    direction = next_direction
    head_x, head_y = snake[0]

    if direction == "Up":
        head_y -= grid_size
    elif direction == "Down":
        head_y += grid_size
    elif direction == "Left":
        head_x -= grid_size
    elif direction == "Right":
        head_x += grid_size

    new_head = [head_x, head_y]

    died = False
    if head_x < 0 or head_x >= 600 or head_y < 0 or head_y >= 600:
        state = "gameover"
        died = True
    elif new_head in snake:
        state = "gameover"
        died = True

    if not died:
        snake.insert(0, new_head)
        if head_x == food_x and head_y == food_y:
            score += 1
            food_eaten += 1
            food_x, food_y = create_food()
            if food_eaten >= 15 and bonus_timer == 0 and bonus_x is None:
                bonus_x, bonus_y = create_bonus()
                bonus_timer = BONUS_DURATION_MS // TICK_MS
                food_eaten = 0
        else:
            snake.pop()

        if bonus_x is not None and head_x == bonus_x and head_y == bonus_y and bonus_timer > 0:
            score += 5
            bonus_x = None
            bonus_y = None
            bonus_timer = 0

    if bonus_timer > 0:
        bonus_timer -= 1
        if bonus_timer == 0:
            bonus_x = None
            bonus_y = None

    canvas.delete("all")
    for i, (x, y) in enumerate(snake):
        if i == 0:
            color = "lime"
        elif i == len(snake) - 1:
            color = "#004400"
        else:
            color = "green"
        canvas.create_rectangle(x, y, x + grid_size, y + grid_size, fill=color)
    canvas.create_rectangle(food_x, food_y, food_x + grid_size, food_y + grid_size, fill="red")

    if bonus_x is not None and bonus_timer > 0:
        canvas.create_rectangle(bonus_x, bonus_y, bonus_x + grid_size, bonus_y + grid_size, fill="yellow")
        remaining = (bonus_timer * TICK_MS + 999) // 1000
        canvas.create_text(590, 10, anchor="ne", fill="white", text=f"Bonus: {remaining}s")

        canvas.create_text(10, 10, anchor="nw", fill="white", text=f"Score: {score}")

    if state == "gameover":
        after_id = None
        canvas.create_text(300, 280, fill="white", text="Game Over", font=("Arial", 32))
        canvas.create_text(300, 320, fill="white", text="Press R to restart", font=("Arial", 14))
        canvas.create_text(300, 350, fill="white", text="Press Q to quit", font=("Arial", 14))
        return

    after_id = root.after(TICK_MS, game_loop)

game_loop()
root.mainloop()
