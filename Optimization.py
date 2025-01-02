#optimize to use renewables in times/areas of low usages and combination
#during high usage

from scipy.optimize import linprog

# Input data
power_plants = ["Plant A", "Plant B", "Plant C"]
generation_costs = [50, 40, 70]  # Cost per MWh for each plant
min_capacity = [10, 20, 15]      # Minimum generation capacity (MWh)
max_capacity = [100, 200, 150]   # Maximum generation capacity (MWh)
demand = 300                     # Total electricity demand (MWh)

# Objective function: Minimize cost
c = generation_costs  # Coefficients for the cost function

# Constraints
# Total generation must meet or exceed demand
A_eq = [[1, 1, 1]]  # Coefficients for the equality constraint
b_eq = [demand]     # Total demand

# Generation must stay within min and max capacities
bounds = [(min_cap, max_cap) for min_cap, max_cap in zip(min_capacity, max_capacity)]

# Solve the optimization problem
result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

# Display results
if result.success:
    print("Optimization successful!")
    print(f"Total cost: ${result.fun:.2f}")
    for plant, power in zip(power_plants, result.x):
        print(f"{plant} generates {power:.2f} MWh")
else:
    print("Optimization failed:", result.message)
