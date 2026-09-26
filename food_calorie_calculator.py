import tkinter as tk
from tkinter import ttk, messagebox


# ---------------- FOOD DATABASE ----------------

food_calories = {
    "Rice": 130,
    "Roti": 297,
    "Dal": 116,
    "Milk": 61,
    "Egg": 155,
    "Banana": 89,
    "Apple": 52,
    "Potato": 77,
    "Chicken": 239,
    "Paneer": 265,
    "Bread": 266,
    "Oats": 389
}


# ---------------- FUNCTIONS ----------------

total_calories = 0


def calculate_calories():

    global total_calories

    food = food_box.get()
    quantity = quantity_entry.get()

    if quantity == "":
        messagebox.showerror("Error", "Please enter quantity.")
        return

    try:
        quantity = float(quantity)

        if quantity <= 0:
            messagebox.showerror(
                "Error",
                "Quantity must be greater than 0."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Error",
            "Please enter a valid number."
        )
        return

    calories = (food_calories[food] * quantity) / 100

    total_calories = total_calories + calories

    result_label.config(
        text=f"{calories:.2f} kcal"
    )

    total_label.config(
        text=f"Total Calories: {total_calories:.2f} kcal"
    )

    history.insert(
        "",
        "end",
        values=(food, f"{quantity:.1f}", f"{calories:.2f}")
    )

    quantity_entry.delete(0, tk.END)


def clear_all():

    global total_calories

    total_calories = 0

    result_label.config(text="0 kcal")

    total_label.config(
        text="Total Calories: 0 kcal"
    )

    for item in history.get_children():
        history.delete(item)


def exit_program():

    root.destroy()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Food Calorie Calculator")

root.geometry("700x600")

root.resizable(False, False)


# ---------------- TITLE ----------------

title_label = tk.Label(
    root,
    text="🍎 Food Calorie Calculator",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=20)


subtitle_label = tk.Label(
    root,
    text="Calculate calories based on food and quantity",
    font=("Arial", 11)
)

subtitle_label.pack()


# ---------------- INPUT FRAME ----------------

input_frame = tk.Frame(root)

input_frame.pack(pady=25)


# Food label

food_label = tk.Label(
    input_frame,
    text="Select Food:",
    font=("Arial", 12)
)

food_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)


# Food dropdown

food_box = ttk.Combobox(
    input_frame,
    values=list(food_calories.keys()),
    state="readonly",
    width=20
)

food_box.current(0)

food_box.grid(
    row=0,
    column=1,
    padx=10
)


# Quantity label

quantity_label = tk.Label(
    input_frame,
    text="Quantity (grams):",
    font=("Arial", 12)
)

quantity_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)


# Quantity input

quantity_entry = tk.Entry(
    input_frame,
    width=23,
    font=("Arial", 11)
)

quantity_entry.grid(
    row=1,
    column=1,
    padx=10
)


# ---------------- CALCULATE BUTTON ----------------

calculate_button = tk.Button(
    root,
    text="Calculate & Add",
    font=("Arial", 12, "bold"),
    command=calculate_calories,
    padx=20,
    pady=8
)

calculate_button.pack(pady=10)


# ---------------- RESULT ----------------

result_label = tk.Label(
    root,
    text="0 kcal",
    font=("Arial", 20, "bold")
)

result_label.pack(pady=10)


# ---------------- HISTORY TABLE ----------------

columns = ("Food", "Quantity", "Calories")

history = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=8
)

history.heading(
    "Food",
    text="Food"
)

history.heading(
    "Quantity",
    text="Quantity (g)"
)

history.heading(
    "Calories",
    text="Calories (kcal)"
)

history.column(
    "Food",
    width=200
)

history.column(
    "Quantity",
    width=150
)

history.column(
    "Calories",
    width=150
)

history.pack(pady=15)


# ---------------- TOTAL ----------------

total_label = tk.Label(
    root,
    text="Total Calories: 0 kcal",
    font=("Arial", 16, "bold")
)

total_label.pack(pady=10)


# ---------------- BUTTONS ----------------

button_frame = tk.Frame(root)

button_frame.pack(pady=10)


clear_button = tk.Button(
    button_frame,
    text="Clear All",
    font=("Arial", 11),
    command=clear_all,
    padx=20
)

clear_button.grid(
    row=0,
    column=0,
    padx=10
)


exit_button = tk.Button(
    button_frame,
    text="Exit",
    font=("Arial", 11),
    command=exit_program,
    padx=20
)

exit_button.grid(
    row=0,
    column=1,
    padx=10
)


# ---------------- START PROGRAM ----------------

root.mainloop()