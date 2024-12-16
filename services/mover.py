import matplotlib.pyplot as plt
import json
import numpy as np

def calculate_net_rent(monthly_rent, lease_term, free_months, flat_rate_discount):
    """
    Calculates the net effective monthly rent after applying free months and flat-rate discounts.
    """
    total_rent = monthly_rent * lease_term
    total_rent -= free_months * monthly_rent
    total_rent -= flat_rate_discount
    return round(total_rent / lease_term, 2)

def calculate_commute_loss(salary, commute_time, work_days_per_year=260):
    """
    Calculates the income lost due to time spent commuting based on salary and commute time.
    """
    hourly_wage = salary / (40 * 52)
    total_commute_hours = (commute_time * 2 / 60) * work_days_per_year
    return round(total_commute_hours * hourly_wage / 12, 2)  # Monthly commute loss

def calculate_gas_cost(miles_driven, mpg, gas_price, work_days_per_year=260):
    """
    Calculates the monthly gas cost for commuting.
    """
    total_miles_per_year = miles_driven * 2 * work_days_per_year
    gallons_used_per_year = total_miles_per_year / mpg
    gas_cost_per_year = gallons_used_per_year * gas_price
    return round(gas_cost_per_year / 12, 2)  # Monthly gas cost

def main():
    # Constants
    gas_price = 3.70
    mpg = 15
    salary = 100_000
    utilities = 100

    # Scenarios
    scenarios = [
        {"monthly_rent": 772, "lease_term": 12, "free_months": 0, "flat_rate_discount": 0, "commute_time": 15, "miles_driven": 6, "fees": 40},
        {"monthly_rent": 1055, "lease_term": 12, "free_months": 2, "flat_rate_discount": 0, "commute_time": 60, "miles_driven": 26, "fees": 50},
        {"monthly_rent": 960, "lease_term": 12, "free_months": 1, "flat_rate_discount": 0, "commute_time": 45, "miles_driven": 20, "fees": 60},
        {"monthly_rent": 1321, "lease_term": 16, "free_months": 1.5, "flat_rate_discount": 0, "commute_time": 5, "miles_driven": 0, "fees": 130},
        {"monthly_rent": 1090, "lease_term": 12, "free_months": 1.5, "flat_rate_discount": 0, "commute_time": 30, "miles_driven": 17, "fees": 80},
    ]

    # Calculate costs for each scenario
    results = []
    for idx, scenario in enumerate(scenarios):
        net_rent = calculate_net_rent(scenario["monthly_rent"], scenario["lease_term"], scenario["free_months"], scenario["flat_rate_discount"])
        commute_loss = calculate_commute_loss(salary, scenario["commute_time"])
        gas_cost = calculate_gas_cost(scenario["miles_driven"], mpg, gas_price)

        total_monthly_cost = net_rent + gas_cost + scenario["fees"] + utilities
        total_monthly_cost_with_commute = total_monthly_cost + commute_loss

        results.append({
            "scenario": f"Scenario {idx + 1}",
            "net_rent": net_rent,
            "commute_loss": commute_loss,
            "gas_cost": gas_cost,
            "total_monthly_cost": total_monthly_cost,
            "total_monthly_cost_with_commute": total_monthly_cost_with_commute,
        })

    # Save results to JSON
    with open("rent_cost_analysis.json", "w") as f:
        json.dump(results, f, indent=4)

    # Visualization
    scenario_labels = [result["scenario"] for result in results]
    net_rent_values = [result["net_rent"] for result in results]
    commute_loss_values = [result["commute_loss"] for result in results]
    gas_cost_values = [result["gas_cost"] for result in results]
    total_monthly_costs = [result["total_monthly_cost_with_commute"] for result in results]

    x = range(len(results))
    bar_width = 0.25

    plt.figure(figsize=(12, 8))
    plt.bar(x, net_rent_values, width=bar_width, label="Net Rent", color="green", alpha=0.7)
    plt.bar([i + bar_width for i in x], commute_loss_values, width=bar_width, label="Commute Loss", color="orange", alpha=0.7)
    plt.bar([i + 2 * bar_width for i in x], gas_cost_values, width=bar_width, label="Gas Cost", color="blue", alpha=0.7)
    plt.bar([i + 3 * bar_width for i in x], total_monthly_costs, width=bar_width, label="Total Cost", color="black", alpha=0.7)

    plt.xticks([i + bar_width * 1.5 for i in x], scenario_labels, rotation=45)
    plt.xlabel("Scenarios")
    plt.ylabel("Monthly Costs ($)")
    plt.title("Monthly Costs Breakdown by Scenario")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
