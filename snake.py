import tkinter as tk
import random

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="black", width=600, height=600)
canvas.pack()

snake = [[100, 100], [80, 100], [60, 100]]
direction = "Right"
grid_size = 20
score = 0
state = "start"
after_id = None

def create_food():
    while True:
        x = random.randrange(0, 600, grid_size)
        y = random.randrange(0, 600, grid_size)
        if [x, y] not in snake:
            return x, y

food_x, food_y = create_food()

def change_direction(event):
    global direction, state
    new_dir = event.keysym
    if new_dir in ("space", "Space") and state == "start":
        start_game()
        return
    if new_dir in ("r", "R"):
        restart_game()
        return
    if state != "playing":
        return
    if new_dir == "Up" and direction != "Down":
        direction = "Up"
    elif new_dir == "Down" and direction != "Up":
        direction = "Down"
    elif new_dir == "Left" and direction != "Right":
        direction = "Left"
    elif new_dir == "Right" and direction != "Left":
        direction = "Right"

root.bind("<KeyPress>", change_direction)

def draw_start_screen():
    canvas.delete("all")
    canvas.create_text(300, 250, fill="white", text="Snake Game", font=("Arial", 36))
    canvas.create_text(300, 320, fill="white", text="Press Space to start", font=("Arial", 16))

def start_game():
    global state, after_id
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    state = "playing"
    game_loop()

def restart_game():
    global snake, direction, score, food_x, food_y, state, after_id
    if after_id is not None:
        root.after_cancel(after_id)
        after_id = None
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = "Right"
    score = 0
    state = "playing"
    food_x, food_y = create_food()
    canvas.delete("all")
    game_loop()

def game_loop():
    global snake, food_x, food_y, score, state, after_id
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
            food_x, food_y = create_food()
        else:
            snake.pop()

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

    if state == "gameover":
        after_id = None
        canvas.create_text(300, 280, fill="white", text="Game Over", font=("Arial", 32))
        canvas.create_text(300, 330, fill="white", text="Press R to restart", font=("Arial", 14))
        return

    after_id = root.after(100, game_loop)

game_loop()
root.mainloop()
