import json


categories = {
    "Kitchen": [
        "Plates, bowls",
        "Cups/mugs/glasses",
        "Silverware",
        "Tupperware",
        "Dish soap",
        "Pans/Pots",
        "Cookie sheets (long pans)",
        "Ladle/Spatula/tongs",
        "Pot holders",
        "Cutting Board",
        "Water Bottles",
        "Mixing bowls",
        "Measuring cups/Teaspoons/tablespoons",
        "bottle opener",
        "Drying rack",
        "towels/wash rags",
        "crockpot/instapot",
    ],
    "Bathroom": [
        "Towels/rags",
        "Body Wash/Soap/Shampoo/Conditioner/Hand Soap",
        "Toilet brush and plunger (as well as cleaner)",
        "Lotion",
        "Toothbrush/Toothpaste/toothbrush holder",
        "toilet paper",
        "shower curtain (and hooks for it!)",
    ],
    "Bedroom": [
        "Mattress",
        "Sheets and Bedding",
        "Pillows",
        "Clothing hangers",
        "Clothes (Shirts, Socks, Underwear, Pants/Skirts, dresses, etc)",
    ],
    "Laundry Room": [
        "Laundry Detergent/Softener",
        "Stain Remover",
        "Cleaners",
    ],
    "Pantry/Foodwise": [
        "Bread",
        "Milk",
        "Cheese",
        "Butter",
        "Sugar/Flour",
        "Rice",
        "Pasta",
        "Chicken/Beef",
        "Seasonings",
        "Condiments",
        "Cereals",
    ],
    "Miscellaneous": [
        "First Aid",
        "Pet Supplies",
        "Mop, Broom, Vacuum, dust pan",
        "Paper Towels",
        "Trash Bags",
        "Ziploc Bags",
        "Tools",
        "Batteries",
        "Trash Cans",
        "An Iron (and possible ironing board)",
        "Tissues",
        "Scissors",
        "Laundry Basket",
        "Lightbulbs",
        "Heater/Fan",
        "Curtains",
        "Step Stool",
        "Smoke/Carbon Dioxide Detectors",
        "Matches",
        "Flashlights",
        "Extension cords",
        "Tape",
        "Pens, pencils, erasers, sharpeners, sharpies, etc",
        "Safe Box for Documents",
    ],
}

data = {}

for category, items in categories.items():
    print(f"\n{category}:\n")
    category_data = {}
    for item in items:
        while True:
            try:
                price = float(input(f"Enter the price for {item}: $"))
                quantity = int(input(f"How many do you want for {item}? "))
                if price < 0 or quantity < 0:
                    raise ValueError("Price and quantity must be positive numbers")
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        category_data[item] = {"price": price, "quantity": quantity}
    data[category] = category_data 

# Save data to JSON file
with open("shopping_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("Data saved successfully to shopping_data.json")