from flask import Flask, render_template, request

app = Flask(__name__)

# Define source lists
protein_sources = {
    "veg": ["Paneer", "Tofu", "Soya Chunks", "Moong Dal", "Lentils"],
    "nonveg": ["Chicken Breast", "Eggs", "Fish", "Turkey", "Shrimp"]
}
fat_sources = {
    "veg": ["Avocado", "Peanuts", "Olive Oil", "Chia Seeds"],
    "nonveg": ["Egg Yolks", "Fatty Fish", "Butter", "Ghee"]
}
carb_sources = {
    "veg": ["Brown Rice", "Oats", "Quinoa", "Sweet Potato", "Banana"],
    "nonveg": ["Brown Rice", "Oats", "Sweet Potato", "Whole Wheat Bread"]
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        weight = float(request.form["weight"])
        goal = request.form["goal"]
        diet = request.form["diet"]

        # Maintenance Calories
        maintenance = weight * 2.2 * 15

        # Adjust for goal
        if goal == "cutting":
            target = maintenance * 0.9
        else:
            target = maintenance * 1.1

        # Macros
        protein_g = weight * 2
        protein_cal = protein_g * 4

        fat_g = weight * 0.8
        fat_cal = fat_g * 9

        carb_cal = target - (protein_cal + fat_cal)
        carb_g = carb_cal / 4

        # Fiber
        fiber_g = weight * 0.4

        return render_template("index.html", result={
            "maintenance": round(maintenance),
            "target": round(target),
            "protein_g": round(protein_g),
            "protein_cal": round(protein_cal),
            "fat_g": round(fat_g),
            "fat_cal": round(fat_cal),
            "carb_g": round(carb_g),
            "carb_cal": round(carb_cal),
            "fiber_g": round(fiber_g),
            "sources": {
                "protein": protein_sources[diet],
                "fat": fat_sources[diet],
                "carbs": carb_sources[diet]
            }
        })

    return render_template("index.html")

# New routes for food source pages
@app.route("/protein")
def protein():
    return render_template("protein.html")

@app.route("/fat")
def fat():
    return render_template("fat.html")

@app.route("/carbs")
def carbs():
    return render_template("carbs.html")

if __name__ == "__main__":
    app.run(debug=True)
