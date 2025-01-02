#optimize to use renewables in times/areas of low usages and combination
#during high usage

from scipy.optimize import linprog


power_plants = ["Plant A", "Plant B", "Plant C"]
generation_costs = [50, 40, 70]
min_capacity = [10, 20, 15]
max_capacity = [100, 200, 150]
demand = 300
c = generation_costs

A_eq = [[1, 1, 1]]
b_eq = [demand]
bounds = [(min_cap, max_cap) for min_cap, max_cap in zip(min_capacity, max_capacity)]


result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")


if result.success:
    print("Optimization successful!")
    print(f"Total cost: ${result.fun:.2f}")
    for plant, power in zip(power_plants, result.x):
        print(f"{plant} generates {power:.2f} MWh")
else:
    print("Optimization failed:", result.message)
