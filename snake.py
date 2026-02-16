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

def create_food():
    x = random.randrange(0, 600, grid_size)
    y = random.randrange(0, 600, grid_size)
    return x, y

food_x, food_y = create_food()

def change_direction(event):
    global direction
    new_dir = event.keysym
    if new_dir == "Up" and direction != "Down":
        direction = "Up"
    elif new_dir == "Down" and direction != "Up":
        direction = "Down"
    elif new_dir == "Left" and direction != "Right":
        direction = "Left"
    elif new_dir == "Right" and direction != "Left":
        direction = "Right"

root.bind("<KeyPress>", change_direction)

def game_loop():
    global snake, food_x, food_y, score
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
    snake.insert(0, new_head)

    if head_x == food_x and head_y == food_y:
        score += 1
        food_x, food_y = create_food()
    else:
        snake.pop()

    canvas.delete("all")
    for x, y in snake:
        canvas.create_rectangle(x, y, x + grid_size, y + grid_size, fill="green")
    canvas.create_rectangle(food_x, food_y, food_x + grid_size, food_y + grid_size, fill="red")
    canvas.create_text(10, 10, anchor="nw", fill="white", text=f"Score: {score}")

    root.after(100, game_loop)

game_loop()
root.mainloop()
