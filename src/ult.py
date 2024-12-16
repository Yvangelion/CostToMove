import matplotlib.pyplot as plt
import json

import numpy as np


def calculate_net_rent(monthly_rent, lease_term, free_months, flat_rate_discount):
    """
    Calculates the net effective monthly rent after applying free months and flat rate discounts.
    """
    total_rent = monthly_rent * lease_term
    free_months_value = free_months * monthly_rent
    total_rent -= free_months_value
    total_rent -= flat_rate_discount
    net_effective_rent = total_rent / lease_term
    return round(net_effective_rent, 2)

def calculate_commute_loss(salary, commute_time, work_days_per_year=260):
    """
    Calculates the income lost due to time spent commuting based on salary and commute time.
    """
    hourly_wage = salary / (40 * 52)
    total_commute_hours = (commute_time * 2 / 60) * work_days_per_year
    commute_loss = total_commute_hours * hourly_wage
    return round(commute_loss, 2)

def calculate_gas_cost(miles_driven, mpg, gas_price, work_days_per_year=260):
    """
    Calculates the total cost of gas for commuting.
    """
    # 60 min per month
    min_gas = 60*12
    total_miles_per_year = miles_driven * 2 * work_days_per_year
    gallons_used_per_year = total_miles_per_year / mpg
    gas_cost_per_year = (gallons_used_per_year * gas_price) + min_gas
    return round(gas_cost_per_year, 2)

def main():
    hard_gas = 3.70
    hard_mpg = 15 
    hard_salary = 100_000
    hard_utilities = 100
    
    # between 6, 25, 9
    
    # 1,31,18,9,34 , 15
    
    # 1,9, 15, 18, 31, 34
    
    # 1 prob not 
    # 9 ghetto cant lie 
    #25 better than hazel muse
    # 15 prob not
    # 18 no
    #31 prob not
    #34 prob out
    # 35 no
    
    
    # Expanded scenarios with fees and utilities
    scenarios = [
       
        
        {"monthly_rent": 1200, "lease_term": 12, "free_months": 2, "flat_rate_discount": 1500, "salary": hard_salary, 
         "commute_time": 60, "miles_driven": 26, "mpg": hard_mpg, "gas_price": hard_gas, "fees": 40, "utilities": hard_utilities},

    ]

    # Initialize lists to store calculated values
    net_rent_values = []
    total_monthly_costs = []
    total_yearly_costs = []
    commute_loss_values = []
    gas_cost_values = []
    scenario_labels = []
    total_monthly_cost_commute_aa = []
    start_rent = []
    
    # between 6, 25, 9

    # Calculate costs for each scenario
    for idx, scenario in enumerate(scenarios):
        net_rent = round(calculate_net_rent(scenario["monthly_rent"], scenario["lease_term"], scenario["free_months"], scenario["flat_rate_discount"]),2)
        commute_loss = round(calculate_commute_loss(scenario["salary"], scenario["commute_time"]) / 12, 2)  # Convert to monthly
        gas_cost = round(calculate_gas_cost(scenario["miles_driven"], scenario["mpg"], scenario["gas_price"]) / 12,2)  # Convert to monthly
        rent_start = scenario["monthly_rent"]
        
        # Add fees and utilities
        fees = scenario["fees"]
        utilities = scenario["utilities"]
        total_monthly_cost = round(net_rent + gas_cost + fees + utilities,2)
        total_monthly_cost_commute = round(net_rent + gas_cost + fees + utilities + commute_loss, 2) 
        total_yearly_cost = round(total_monthly_cost * 12,2)
        
        # Append results for later use
        start_rent.append(rent_start)
        net_rent_values.append(net_rent)
        commute_loss_values.append(commute_loss)
        gas_cost_values.append(gas_cost)
        total_monthly_costs.append(total_monthly_cost)
        total_yearly_costs.append(total_yearly_cost)
        total_monthly_cost_commute_aa.append(total_monthly_cost_commute)
        scenario_labels.append(f"Scenario {idx + 1}")
        
    # Create a list of dictionaries for easier conversion to JSON
    results = []
    for idx in range(len(scenarios)):
        results.append({
            "scenario": scenario_labels[idx],
            "start rent": start_rent[idx],
            "net_rent": net_rent_values[idx],
            "commute_loss": commute_loss_values[idx],
            "gas_cost": gas_cost_values[idx],
            "total_monthly_cost": total_monthly_costs[idx],
            "total_monthly_cost_with_commute": total_monthly_cost_commute_aa[idx],
            "total_yearly_cost": total_yearly_costs[idx]
        })
        
    results_commute = []
    for idx in range(len(scenarios)):
        results_commute.append({
            "scenario": scenario_labels[idx],
            "start rent": start_rent[idx],
            "total_yearly_cost": total_yearly_costs[idx],
            "--------": "--------",
            "total_monthly_cost": total_monthly_costs[idx],
            #"total_monthly_cost_with_commute": total_monthly_cost_commute_aa[idx],
        })

    # Sort results by total monthly cost and total monthly cost with commute loss
    sorted_by_monthly_cost = sorted(results, key=lambda x: x["total_monthly_cost"])
    sorted_by_monthly_cost_with_commute = sorted(results, key=lambda x: x["total_monthly_cost_with_commute"])
    doublecost = sorted(results_commute, key=lambda x: x["total_monthly_cost"])
    rent_first = sorted(results, key=lambda x: x["net_rent"])
    
    # Output to JSON files
    
    with open("rent_sorted.json", "w") as f:
        json.dump(results, f, indent=4)
        
        
    with open("sorted_by_monthly_cost.json", "w") as f:
        json.dump(sorted_by_monthly_cost, f, indent=4)
    
    with open("sorted_by_monthly_cost_with_commute.json", "w") as f:
        json.dump(sorted_by_monthly_cost_with_commute, f, indent=4)
    
    with open("gas_no_commute.json", "w") as f:
        json.dump(doublecost, f, indent=4)
    
    with open("sorted_rentfirst_no_gas.json", "w") as f:
        json.dump(rent_first, f, indent=4)
    
    with open("unsorted_scenarios.json", "w") as f:
        json.dump(results, f, indent=4)

    # Plot results
    # Sort indices based on total cost
    sorted_indices = np.argsort(total_monthly_cost_commute_aa)

    # Reorder data based on sorted indices
    sorted_labels = [scenarios[i] for i in sorted_indices]
    sorted_net_rent = [net_rent_values[i] for i in sorted_indices]
    sorted_commute_loss = [commute_loss_values[i] for i in sorted_indices]
    sorted_gas_cost = [gas_cost_values[i] for i in sorted_indices]
    sorted_total_cost = [total_monthly_cost_commute_aa[i] for i in sorted_indices]

    # Plotting
    x = range(len(sorted_labels))  # Scenario indices
    bar_width = 0.25

    plt.figure(figsize=(12, 8), facecolor="darkgrey")  # Change figure background
    ax = plt.gca()
    ax.set_facecolor("darkgrey")  # Change plot background


    plt.bar(x, sorted_net_rent, width=bar_width, label="Net Rent", color="green", alpha=0.7)
    plt.bar([i + bar_width for i in x], sorted_commute_loss, width=bar_width, label="Commute Loss", color="orange", alpha=0.7)
    plt.bar([i + 2 * bar_width for i in x], sorted_gas_cost, width=bar_width, label="Gas Cost", color="blue", alpha=0.7)
    plt.bar([i + 3 * bar_width for i in x], sorted_total_cost, width=bar_width, label="Total Cost", color="black", alpha=0.7)

    plt.xticks([i + bar_width for i in x], sorted_labels, rotation=45)
    plt.xlabel("Scenarios")
    plt.ylabel("Monthly Costs ($)")
    plt.title("Comparison of Net Rent, Commute Loss, Gas Cost, and Total Cost (Sorted by Total Cost)")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()