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
fiber_sources = {
    "veg": ["Spinach", "Broccoli", "Chia Seeds", "Oats", "Apples"],
    "nonveg": ["Avocado", "Sweet Corn", "Pumpkin", "Green Peas", "Carrot"]
}

# Image links
image_links = {
    # Protein
    "Paneer": "https://i.pinimg.com/564x/8f/82/99/8f8299183b36f94a3952c1ff502b5fd1.jpg",
    "Tofu": "https://i.pinimg.com/564x/5b/d3/2d/5bd32de4b648ed3b88a64d3961b1f650.jpg",
    "Soya Chunks": "https://i.pinimg.com/564x/f0/38/b3/f038b3a3317e1a97ef3702a90ea9493e.jpg",
    "Moong Dal": "https://i.pinimg.com/564x/cf/3d/f5/cf3df5a40e0d3a9b1d2fd6c94ef68962.jpg",
    "Lentils": "https://i.pinimg.com/564x/44/ef/5a/44ef5a190263f3ed46a83ad9a7f11e04.jpg",
    "Chicken Breast": "https://i.pinimg.com/564x/86/49/20/864920e6aa3c70dfc383d52dc7487a38.jpg",
    "Eggs": "https://i.pinimg.com/564x/90/89/70/908970c138b157899fdf155050eaf3ec.jpg",
    "Fish": "https://i.pinimg.com/564x/3a/45/b7/3a45b72f5eb2065a3ec3ae2a14ea4c46.jpg",
    "Turkey": "https://i.pinimg.com/564x/57/1d/4a/571d4a5c1280fd7fc1858b7b2d8b96b6.jpg",
    "Shrimp": "https://i.pinimg.com/564x/5c/3e/84/5c3e84b760dcf229a95bb4f443678f56.jpg",
    # Fat
    "Avocado": "https://i.pinimg.com/564x/7b/e6/e5/7be6e56a735ecfb02083c14257e38f7f.jpg",
    "Peanuts": "https://i.pinimg.com/564x/56/ef/e7/56efe7d982c7f95bd7b3652f802345a6.jpg",
    "Olive Oil": "https://i.pinimg.com/564x/52/02/8b/52028b4160fc848b8a259208ad12a969.jpg",
    "Chia Seeds": "https://i.pinimg.com/564x/cf/f6/80/cff6805eb4c82a18f020c8f8940e4c7e.jpg",
    "Egg Yolks": "https://i.pinimg.com/564x/3c/99/5c/3c995c61bc1e0e26e96c3132aa94b13b.jpg",
    "Fatty Fish": "https://i.pinimg.com/564x/8b/92/df/8b92dffdc9b77e18e054509cf77917df.jpg",
    "Butter": "https://i.pinimg.com/564x/68/52/2d/68522d017c2151bc08a57bcf8e2c2451.jpg",
    "Ghee": "https://i.pinimg.com/564x/94/17/fc/9417fcde4bb6f67aefc9b5cbe8bd530a.jpg",
    # Carbs
    "Brown Rice": "https://i.pinimg.com/564x/7d/89/89/7d8989f3a65b02c5e58d166f184c4b56.jpg",
    "Oats": "https://i.pinimg.com/564x/39/c9/b1/39c9b187169e263b878ce671d6a87cfd.jpg",
    "Quinoa": "https://i.pinimg.com/564x/7e/10/c3/7e10c39827a0a1c678ea6f360f8692cb.jpg",
    "Sweet Potato": "https://i.pinimg.com/564x/f4/67/57/f46757d4a869bb2c3aebc1d9fef3b749.jpg",
    "Banana": "https://i.pinimg.com/564x/53/3d/32/533d32b3d5b6e98e5f181e32902a34bb.jpg",
    "Whole Wheat Bread": "https://i.pinimg.com/564x/49/b3/4f/49b34fdd222b96a7b9670613c312b944.jpg",
    # Fiber
    "Spinach": "https://i.pinimg.com/564x/82/4d/37/824d378a05ea4b77ebeb3c71116c3c52.jpg",
    "Broccoli": "https://i.pinimg.com/564x/d6/47/d9/d647d9a647b8b5a12a5f4bc54727ab6e.jpg",
    "Apples": "https://i.pinimg.com/564x/27/3b/8a/273b8a3b4c4038cdd222d6e19c6be33c.jpg",
    "Sweet Corn": "https://i.pinimg.com/564x/43/b6/20/43b62000ad2acccf31c147a3c7552e76.jpg",
    "Pumpkin": "https://i.pinimg.com/564x/4a/5e/5a/4a5e5a65486c45862e0b6d1225c0f80f.jpg",
    "Green Peas": "https://i.pinimg.com/564x/6f/2f/16/6f2f1687723c20c6c93bc20abfca08e2.jpg",
    "Carrot": "https://i.pinimg.com/564x/f1/5b/cf/f15bcf624c18161e85851de689cf86a0.jpg"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        weight = float(request.form["weight"])
        goal = request.form["goal"]
        diet = request.form["diet"]

        maintenance = weight * 2.2 * 15
        target = maintenance * 0.9 if goal == "cutting" else maintenance * 1.1

        protein_g = weight * 2
        protein_cal = protein_g * 4

        fat_g = weight * 0.8
        fat_cal = fat_g * 9

        carb_cal = target - (protein_cal + fat_cal)
        carb_g = carb_cal / 4

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
            "diet": diet
        })

    return render_template("index.html")

@app.route("/protein")
def protein():
    diet = request.args.get("diet", "veg")
    items = protein_sources[diet]
    images = {item: image_links[item] for item in items}
    return render_template("protein.html", sources=images, diet=diet)

@app.route("/fat")
def fat():
    diet = request.args.get("diet", "veg")
    items = fat_sources[diet]
    images = {item: image_links[item] for item in items}
    return render_template("fat.html", sources=images, diet=diet)

@app.route("/carbs")
def carbs():
    diet = request.args.get("diet", "veg")
    items = carb_sources[diet]
    images = {item: image_links[item] for item in items}
    return render_template("carbs.html", sources=images, diet=diet)

@app.route("/fiber")
def fiber():
    diet = request.args.get("diet", "veg")
    items = fiber_sources[diet]
    images = {item: image_links[item] for item in items}
    return render_template("fiber.html", sources=images, diet=diet)

if __name__ == "__main__":
    app.run(debug=True)
