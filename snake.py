import tkinter as tk

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

canvas = tk.Canvas(root, bg="black", width=600, height=600)
canvas.pack()

direction = "Right"

def change_direction(event):
    global direction
    if event.keysym == "Up":
        direction = "Up"
    elif event.keysym == "Down":
        direction = "Down"
    elif event.keysym == "Left":
        direction = "Left"
    elif event.keysym == "Right":
        direction = "Right"
    print(f"Direction changed to: {direction}")

root.bind("<KeyPress>", change_direction)

def game_loop():
    root.after(100, game_loop)

game_loop()
root.mainloop()
