from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_net_rent(monthly_rent, lease_term, free_months, flat_rate_discount):
    discounted_rent = (monthly_rent * lease_term - flat_rate_discount) / (lease_term + free_months)
    return discounted_rent

def calculate_commute_loss(salary, commute_time):
    hourly_rate = salary / (52 * 40)  # Assume 40 hours/week, 52 weeks
    commute_loss = (commute_time * hourly_rate) * 20  # Assume 20 workdays/month
    return commute_loss

def calculate_gas_cost(miles_driven, mpg, gas_price):
    gas_cost = (miles_driven / mpg) * gas_price * 20  # Assume 20 workdays/month
    return gas_cost

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        try:
            gas_price = float(request.form.get("gas_price", 0) or 0)
            mpg = float(request.form.get("mpg", 0) or 1)  # Avoid division by zero
            salary = float(request.form.get("salary", 0) or 0)
            utilities = float(request.form.get("utilities", 0) or 0)

            scenarios = []
            num_apartments = int(request.form.get("num_apartments", 0) or 0)

            for i in range(1, num_apartments + 1):
                scenarios.append({
                    "monthly_rent": float(request.form.get(f"monthly_rent_{i}", 0) or 0),
                    "lease_term": int(request.form.get(f"lease_term_{i}", 0) or 0),
                    "free_months": int(request.form.get(f"free_months_{i}", 0) or 0),
                    "flat_rate_discount": float(request.form.get(f"flat_rate_discount_{i}", 0) or 0),
                    "commute_time": int(request.form.get(f"commute_time_{i}", 0) or 0),
                    "miles_driven": float(request.form.get(f"miles_driven_{i}", 0) or 0),
                    "fees": float(request.form.get(f"fees_{i}", 0) or 0),
                })

            results = []
            for scenario in scenarios:
                net_rent = calculate_net_rent(
                    scenario["monthly_rent"], scenario["lease_term"], scenario["free_months"], scenario["flat_rate_discount"]
                )
                commute_loss = calculate_commute_loss(salary, scenario["commute_time"])
                gas_cost = calculate_gas_cost(scenario["miles_driven"], mpg, gas_price)
                total_monthly_cost = net_rent + utilities + scenario["fees"]
                total_monthly_cost_with_commute = total_monthly_cost + commute_loss + gas_cost
                total_yearly_cost = total_monthly_cost_with_commute * 12

                results.append({
                    "scenario": scenario,
                    "net_rent": net_rent,
                    "commute_loss": commute_loss,
                    "gas_cost": gas_cost,
                    "total_monthly_cost": total_monthly_cost,
                    "total_monthly_cost_with_commute": total_monthly_cost_with_commute,
                    "total_yearly_cost": total_yearly_cost,
                })

            rankings = {
                "by_monthly": sorted(results, key=lambda x: x["total_monthly_cost"]),
                "by_monthly_commute": sorted(results, key=lambda x: x["total_monthly_cost_with_commute"]),
                "by_yearly": sorted(results, key=lambda x: x["total_yearly_cost"]),
            }

            return render_template("results.html", results=results, rankings=rankings)

        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
