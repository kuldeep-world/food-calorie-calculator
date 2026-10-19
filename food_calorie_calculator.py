import tkinter as tk
from tkinter import ttk, messagebox

# Indian food calorie estimates per common serving.
# Values are approximate and vary by recipe, portion size, and cooking oil.
FOODS = {
    "Roti (1 medium)": 110,
    "Paratha (1 medium)": 220,
    "Plain rice (1 cup cooked)": 205,
    "Dal (1 bowl)": 150,
    "Rajma (1 bowl)": 210,
    "Chole (1 bowl)": 240,
    "Poha (1 bowl)": 250,
    "Upma (1 bowl)": 230,
    "Idli (1 piece)": 60,
    "Dosa (1 medium)": 170,
    "Sambar (1 bowl)": 100,
    "Paneer sabzi (1 bowl)": 280,
    "Mixed vegetable sabzi (1 bowl)": 140,
    "Curd (1 bowl)": 100,
    "Milk (1 glass, 250 ml)": 150,
    "Chai with milk and sugar (1 cup)": 90,
    "Coffee with milk and sugar (1 cup)": 100,
    "Boiled egg (1)": 75,
    "Omelette (2 eggs)": 220,
    "Chicken curry (1 bowl)": 280,
    "Fish curry (1 bowl)": 230,
    "Khichdi (1 bowl)": 250,
    "Besan chilla (1 medium)": 160,
    "Sprouts chaat (1 bowl)": 150,
    "Banana (1 medium)": 105,
    "Apple (1 medium)": 95,
    "Orange (1 medium)": 60,
    "Peanuts (30 g)": 170,
    "Almonds (10)": 70,
    "Samosa (1 medium)": 260,
    "Gulab jamun (1)": 150,
    "Biscuit (2 medium)": 100,
}

ACTIVITY_FACTORS = {
    "Sedentary (little exercise)": 1.2,
    "Lightly active (1-3 days/week)": 1.375,
    "Moderately active (3-5 days/week)": 1.55,
    "Very active (6-7 days/week)": 1.725,
    "Extra active (physical job/intense training)": 1.9,
}


class CalorieCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Indian Diet & Calorie Calculator")
        self.root.geometry("1000x720")
        self.root.minsize(850, 620)
        self.root.configure(bg="#f4f7f5")

        self.food_log = []
        self.daily_target = None

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TLabel", background="#f4f7f5", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"),
                        foreground="#176b4d", background="#f4f7f5")
        style.configure("TLabelframe", background="#f4f7f5")
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"),
                        foreground="#176b4d", background="#f4f7f5")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)

        header = ttk.Label(root, text="Indian Diet & Calorie Calculator",
                           style="Header.TLabel")
        header.pack(pady=(14, 2))
        ttk.Label(root, text="Track Indian meals • Estimate BMI • Plan daily calories").pack(
            pady=(0, 12))

        main = ttk.Frame(root, padding=(14, 0, 14, 12))
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(1, weight=1)

        profile = ttk.LabelFrame(main, text="1. Your body profile", padding=12)
        profile.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 10))
        profile.columnconfigure(1, weight=1)

        self.age_var = tk.StringVar(value="19")
        self.sex_var = tk.StringVar(value="Male")
        self.height_var = tk.StringVar(value="170")
        self.weight_var = tk.StringVar(value="65")
        self.activity_var = tk.StringVar(value="Lightly active (1-3 days/week)")
        self.goal_var = tk.StringVar(value="Maintain weight")

        self.add_field(profile, "Age (years)", self.age_var, 0)
        ttk.Label(profile, text="Sex for calorie equation").grid(
            row=1, column=0, sticky="w", pady=4)
        ttk.Combobox(profile, textvariable=self.sex_var, values=["Male", "Female"],
                     state="readonly", width=27).grid(row=1, column=1, sticky="ew", pady=4)
        self.add_field(profile, "Height (cm)", self.height_var, 2)
        self.add_field(profile, "Weight (kg)", self.weight_var, 3)

        ttk.Label(profile, text="Activity level").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Combobox(profile, textvariable=self.activity_var,
                     values=list(ACTIVITY_FACTORS.keys()), state="readonly",
                     width=27).grid(row=4, column=1, sticky="ew", pady=4)
        ttk.Label(profile, text="Goal").grid(row=5, column=0, sticky="w", pady=4)
        ttk.Combobox(profile, textvariable=self.goal_var,
                     values=["Lose weight", "Maintain weight", "Gain weight"],
                     state="readonly", width=27).grid(row=5, column=1, sticky="ew", pady=4)
        ttk.Button(profile, text="Calculate BMI & calorie target",
                   command=self.calculate_profile).grid(
                       row=6, column=0, columnspan=2, sticky="ew", pady=(10, 0))

        results = ttk.LabelFrame(main, text="2. Your results", padding=12)
        results.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 10))
        self.bmi_result = tk.StringVar(value="BMI: enter your details")
        self.bmi_category = tk.StringVar(value="")
        self.maintenance_result = tk.StringVar(value="Maintenance calories: —")
        self.target_result = tk.StringVar(value="Daily goal: calculate first")
        self.remaining_result = tk.StringVar(value="Calories logged: 0 kcal")
        for var in (self.bmi_result, self.bmi_category, self.maintenance_result,
                    self.target_result, self.remaining_result):
            ttk.Label(results, textvariable=var, wraplength=400).pack(anchor="w", pady=6)
        ttk.Label(results, text="These are estimates, not medical advice.",
                  wraplength=400).pack(anchor="w", pady=(8, 0))

        food_frame = ttk.LabelFrame(main, text="3. Add food to today's log", padding=12)
        food_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        food_frame.columnconfigure(0, weight=1)
        food_frame.rowconfigure(2, weight=1)

        controls = ttk.Frame(food_frame)
        controls.grid(row=0, column=0, sticky="ew")
        controls.columnconfigure(0, weight=1)
        self.food_var = tk.StringVar(value=next(iter(FOODS)))
        ttk.Label(controls, text="Food").grid(row=0, column=0, sticky="w")
        ttk.Label(controls, text="Servings").grid(row=0, column=1, sticky="w", padx=(10, 0))
        ttk.Combobox(controls, textvariable=self.food_var, values=list(FOODS.keys()),
                     state="readonly", width=42).grid(row=1, column=0, sticky="ew", pady=4)
        self.servings_var = tk.StringVar(value="1")
        ttk.Spinbox(controls, from_=0.25, to=20, increment=0.25,
                    textvariable=self.servings_var, width=10).grid(
                        row=1, column=1, sticky="w", padx=(10, 0), pady=4)
        ttk.Button(controls, text="Add food", command=self.add_food).grid(
            row=1, column=2, padx=(10, 0), pady=4)

        columns = ("food", "servings", "calories")
        self.tree = ttk.Treeview(food_frame, columns=columns, show="headings", height=8)
        self.tree.heading("food", text="Food")
        self.tree.heading("servings", text="Servings")
        self.tree.heading("calories", text="Calories (kcal)")
        self.tree.column("food", width=500, anchor="w")
        self.tree.column("servings", width=120, anchor="center")
        self.tree.column("calories", width=150, anchor="center")
        self.tree.grid(row=2, column=0, sticky="nsew", pady=(10, 6))
        scrollbar = ttk.Scrollbar(food_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=1, sticky="ns", pady=(10, 6))
        self.tree.configure(yscrollcommand=scrollbar.set)

        bottom = ttk.Frame(food_frame)
        bottom.grid(row=3, column=0, sticky="ew")
        self.total_var = tk.StringVar(value="Total consumed: 0 kcal")
        ttk.Label(bottom, textvariable=self.total_var,
                  font=("Segoe UI", 11, "bold")).pack(side="left")
        ttk.Button(bottom, text="Remove selected", command=self.remove_food).pack(
            side="right", padx=(6, 0))
        ttk.Button(bottom, text="Clear today's log", command=self.clear_log).pack(side="right")

        ttk.Label(root, text="Food calories are approximate. Actual values depend on recipe, portion, and oil.",
                  foreground="#555555").pack(pady=(0, 10))

    @staticmethod
    def add_field(parent, label, variable, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=4)
        ttk.Entry(parent, textvariable=variable, width=30).grid(
            row=row, column=1, sticky="ew", pady=4)

    def calculate_profile(self):
        try:
            age = int(self.age_var.get())
            height = float(self.height_var.get())
            weight = float(self.weight_var.get())
            if not (18 <= age <= 100):
                messagebox.showerror("Check age", "This version is designed for adults aged 18-100.")
                return
            if height <= 0 or weight <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid details", "Enter a valid age, height, and weight.")
            return

        bmi = weight / ((height / 100) ** 2)
        if bmi < 18.5:
            category = "Below the standard adult BMI range"
        elif bmi < 25:
            category = "Within the standard adult BMI range"
        elif bmi < 30:
            category = "Above the standard adult BMI range"
        else:
            category = "High BMI range"

        # Mifflin-St Jeor equation estimates resting energy expenditure.
        if self.sex_var.get() == "Male":
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161

        maintenance = bmr * ACTIVITY_FACTORS[self.activity_var.get()]
        goal = self.goal_var.get()
        if goal == "Lose weight":
            target = maintenance - 300
        elif goal == "Gain weight":
            target = maintenance + 300
        else:
            target = maintenance

        self.daily_target = round(target)
        self.bmi_result.set(f"BMI: {bmi:.1f}")
        self.bmi_category.set(f"Screening category: {category}")
        self.maintenance_result.set(f"Estimated maintenance: {round(maintenance):,} kcal/day")
        self.target_result.set(f"Suggested starting target ({goal.lower()}): {self.daily_target:,} kcal/day")
        self.update_totals()

    def add_food(self):
        food = self.food_var.get()
        try:
            servings = float(self.servings_var.get())
            if servings <= 0 or servings > 20:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid serving", "Enter servings greater than 0 and no more than 20.")
            return

        calories = round(FOODS[food] * servings)
        item_id = self.tree.insert("", "end", values=(food, f"{servings:g}", calories))
        self.food_log.append((item_id, calories))
        self.update_totals()

    def remove_food(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select a food", "Select a food row to remove.")
            return
        for item_id in selected:
            self.tree.delete(item_id)
            self.food_log = [item for item in self.food_log if item[0] != item_id]
        self.update_totals()

    def clear_log(self):
        if not self.food_log:
            return
        if messagebox.askyesno("Clear log", "Remove all foods from today's log?"):
            for item_id, _ in self.food_log:
                self.tree.delete(item_id)
            self.food_log.clear()
            self.update_totals()

    def update_totals(self):
        total = sum(calories for _, calories in self.food_log)
        self.total_var.set(f"Total consumed: {total:,} kcal")
        if self.daily_target is None:
            self.remaining_result.set(f"Calories logged: {total:,} kcal (calculate your target above)")
        else:
            difference = self.daily_target - total
            if difference >= 0:
                self.remaining_result.set(f"Remaining to daily target: {difference:,} kcal")
            else:
                self.remaining_result.set(f"Above daily target by: {abs(difference):,} kcal")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieCalculatorApp(root)
    root.mainloop()
