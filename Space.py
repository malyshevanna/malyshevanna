import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random


MAX_ROWS = 3
COLS = 3
MIN_CONTRIBUTION = 1
MAX_CONTRIBUTION = 100
INITIAL_BALANCE = 100


symbol_count = {
    "Frozen Water Vapor": 12,
    "Planet": 5,
    "Asteroid": 8,
    "Spaceship": 4,
    "Alien Artifact": 3
}

symbol_value = {
    "Frozen Water Vapor": 1,
    "Planet": 2,
    "Asteroid": 3,
    "Spaceship": 6,
    "Alien Artifact": 10
}

def get_grid_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, count in symbols.items():
        all_symbols.extend([symbol] * count)

    grid = []
    for _ in range(rows):
        row = random.sample(all_symbols, cols)
        grid.append(row)
    
    return grid

def check_winnings(grid, contribution):
    winnings = 0
    for row in grid:
        row_value = sum(symbol_value[symbol] for symbol in row)
        winnings += row_value * contribution
    return winnings


root = tk.Tk()
root.title("Space Exploration")
root.geometry("800x600")


bg_image = Image.open("background.png")
bg_image = bg_image.resize((800, 600), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)


canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


canvas.create_rectangle(80, 80, 720, 430, fill="white", outline="white", stipple="gray50")


symbols = {
    "Frozen Water Vapor": Image.open("Ice.png").resize((70, 70), Image.LANCZOS),
    "Planet": Image.open("Planet.png").resize((70, 70), Image.LANCZOS),
    "Asteroid": Image.open("Asteroid.png").resize((70, 70), Image.LANCZOS),
    "Spaceship": Image.open("Spaceship.png").resize((70, 70), Image.LANCZOS),
    "Alien Artifact": Image.open("Artifact.png").resize((70, 70), Image.LANCZOS)
}
symbol_photos = {key: ImageTk.PhotoImage(value) for key, value in symbols.items()}


balance = INITIAL_BALANCE


balance_label = tk.Label(root, text=f"Credits: {balance}", font=("Arial", 16, "bold"), fg='#373442')
balance_label.place(x=20, y=20)

def update_balance_display():
    balance_label.config(text=f"Credits: {balance}")

def display_symbols(grid):
    canvas.delete("symbol")  
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            symbol = grid[row][col]
            x = 200 + col * 200  
            y = 150 + row * 100
            canvas.create_image(x, y, image=symbol_photos[symbol], anchor="center", tags="symbol")

def explore_space():
    global balance
    
    rows = int(row_var.get())
    contribution = int(contribution_entry.get())
    total_contribution = contribution * rows

    if total_contribution > balance:
        tk.messagebox.showerror("Insufficient Credits", f"You don't have enough credits. Your current balance is {balance} credits.")
        return

    balance -= total_contribution
    update_balance_display()

    grid = get_grid_spin(rows, COLS, symbol_count)
    display_symbols(grid)

    winnings = check_winnings(grid, contribution)
    balance += winnings
    update_balance_display()

    result_text = f"You spent {total_contribution} credits and earned {winnings} credits."
    
    tk.messagebox.showinfo("Exploration Results", result_text)

    if balance <= 0:
        tk.messagebox.showinfo("Game Over", "You've run out of credits. Game over!")
        root.quit()


control_frame = tk.Frame(root, bg='#877dab')
control_frame.place(x=200, y=470, width=400, height=80)


style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', background='#877dab', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))
style.configure('TCombobox', font=('Arial', 12))

ttk.Label(control_frame, text="Number of sectors:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
row_var = tk.StringVar(value="1")
ttk.Combobox(control_frame, textvariable=row_var, values=["1", "2", "3"], width=5, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky='w')

ttk.Label(control_frame, text="Fuel per sector:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
contribution_entry = ttk.Entry(control_frame, width=5)
contribution_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')
contribution_entry.insert(0, "10")

explore_button = ttk.Button(control_frame, text="Explore Space", command=explore_space)
explore_button.grid(row=1, column=0, columnspan=4, pady=5)

root.mainloop()
