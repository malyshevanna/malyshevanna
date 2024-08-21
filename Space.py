import random
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk
root = tk.Tk()
root.title("Space Exploration")
root.geometry("1920x1080")  


bg_image = Image.open("background.png")
bg_image = bg_image.resize((1920, 1080), Image.ANTIALIAS) 
bg_photo = ImageTk.PhotoImage(bg_image)


canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")


symbols = {
    "Planet": Image.open("Planet.png").resize((128, 128), Image.ANTIALIAS),
    "Asteroid": Image.open("Asteroid.png").resize((128, 128), Image.ANTIALIAS),
    "Spaceship": Image.open("Spaceship.png").resize((128, 128), Image.ANTIALIAS),
    "Alien Artifact": Image.open("Artifact.png").resize((128, 128), Image.ANTIALIAS)
}
symbol_photos = {key: ImageTk.PhotoImage(value) for key, value in symbols.items()}

def on_symbol_click(symbol):
    print(f"You clicked on the {symbol}!")

symbol_positions = {
    "Planet": (500, 300),
    "Asteroid": (800, 300),
    "Spaceship": (1100, 300),
    "Alien Artifact": (1400, 300)
}

for symbol, pos in symbol_positions.items():
    canvas.create_image(pos[0], pos[1], image=symbol_photos[symbol], anchor="center")
    canvas.tag_bind(canvas.create_image(pos[0], pos[1], image=symbol_photos[symbol], anchor="center"), 
                    "<Button-1>", lambda event, s=symbol: on_symbol_click(s))

root.mainloop()

MAX_LINES = 3
MAX_CONTRIBUTION = 100
MIN_CONTRIBUTION = 1

ROWS = 3
COLS = 3



symbol_count = {
    "Planets": 5,
    "Asteroids": 8,
    "Spaceships": 4,
    "Alien artifacts": 3
}

symbol_value = {
    "Planets": 2,
    "Asteroids": -2,
    "Spaceships": 6,
    "Alien artifacts": 10
}

def check_winnings(columns, lines, contribution, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column [line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values [symbol] * contribution
            winning_lines.append(line + 1)

    return winnings, winning_lines




def get_grid_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range (cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)

    return columns


def get_contribution ():
    while True: 
        amount = input("How many credits worth of fuel would you like to spend in each sector?")
        if amount.isdigit():
            amount = int(amount)
            if MIN_CONTRIBUTION <= amount <= MAX_CONTRIBUTION:
                break
            else:
                print (f"Amount must be between ${MIN_CONTRIBUTION} ${MAX_CONTRIBUTION}")
        else: 
            print ("Please enter a number")
    return amount

def get_number_of_lines():
    while True: 
        lines = input(f"Choose how many space sectors you'd like to explore (up to {MAX_LINES})")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print ("Enter a valid number of lines.")
        else: 
            print ("Please enter a number")
    return lines



    

def explore_space(balance):
    lines = get_number_of_lines()
    while True: 
        contribution = get_contribution()
        total_contribution = contribution * lines

        if total_contribution > balance:
                print (f"You don't have enough credits, your current balance is {balance} credits.")
        else: 
            break
    
    
    print (f"You're spending {contribution} worth of fuel to the exploration of {lines} sectors. Total amount spent: {total_contribution} credits.")

    grid = get_grid_spin(ROWS, COLS, symbol_count)
    print(grid)
    winnings, winning_lines = check_winnings(grid, lines, contribution, symbol_value)
    print(f"You earned ${winnings}.")
    print(f"You succeeded on", *winning_lines, "sectors")
    return winnings - total_contribution

def deposit():
    def on_submit():
        amount = int(entry.get())
        if amount > 0:
            root.destroy()
            global deposited_amount
            deposited_amount = amount

        else:
            messagebox.showerror("Error", "Amount must be greater than 0")


    root = tk.Tk()
    root.title("Deposit")
    tk.Label(root, text="You're about to start space exploration! But first, how many credits would you like to spend on it?").pack()
    entry = tk.Entry(root)
    entry.pack()
    tk.Button(root, text ="Submit", command=on_submit).pack()
    root.mainloop()
    return deposited_amount




def main():
    level = 1
    balance = deposit()
    while True:
        symbol_count = get_level_symbols(level)
        print(f"Current balance is ${balance}, Level: {level}")
        answer = input("Press enter to explore space. (q to quit):").strip().lower()
        if answer == "q":
            break
        balance += explore_space(balance)
        if balance > 300:
            level +=1
    print (f"You left with ${balance}")


def get_level_symbols(level):
    level_symbols = {
        1: {"Planet": 5, "Asteroid": 6,  "Spaceship": 4, "Alien Artifact": 2},
        2: {"Planet": 4, "Asteroid": 8, "Spaceship": 3, "Alien Artifact": 2},
        3: {"Planet": 3, "Asteroid": 10, "Spaceship": 2, "Alien Artifact": 2},
    }
    return level_symbols.get(level,{"Planet": 5, "Asteroid": 6, "Spaceship": 4, "Alien Artifact": 2})

if __name__ == "__main__":
    main ()


