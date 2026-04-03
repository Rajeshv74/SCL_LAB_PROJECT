import streamlit as st
import random
import math
import matplotlib.pyplot as plt

# -----------------------------
# Cost Function
# -----------------------------
def cost_function(solution, demand):
    solar, wind, battery = solution

    total_supply = solar + wind + battery
    penalty = abs(demand - total_supply)

    # Cost weights
    cost = (0.3 * solar) + (0.5 * wind) + (0.2 * battery)

    return cost + 2 * penalty
# -----------------------------
# Neighbor Function
# -----------------------------
def neighbor(solution):
    new_solution = solution[:]
    idx = random.randint(0, 2)
    change = random.uniform(-5, 5)
    new_solution[idx] = max(0, new_solution[idx] + change)
    return new_solution


# -----------------------------
# Simulated Annealing
# -----------------------------
def simulated_annealing(demand):
    T = 100
    cooling = 0.95

    current = [random.uniform(10, 50) for _ in range(3)]
    best = current[:]

    history = []

    while T > 1:
        new = neighbor(current)

        delta = cost_function(new, demand) - cost_function(current, demand)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new

        if cost_function(current, demand) < cost_function(best, demand):
            best = current

        history.append(cost_function(current, demand))
        T *= cooling

    return best, history


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🌱 Renewable Energy Grid Optimization")
st.subheader("Using Simulated Annealing")

demand = st.slider("Energy Demand (MW)", 50, 200, 100)

if st.button("Run Optimization ⚡"):

    best, history = simulated_annealing(demand)

    solar, wind, battery = best
    total = solar + wind + battery

    st.write("### 🔋 Optimized Energy Distribution")
    st.write(f"☀ Solar: {solar:.2f} MW")
    st.write(f"🌬 Wind: {wind:.2f} MW")
    st.write(f"🔋 Battery: {battery:.2f} MW")
    st.write(f"⚡ Total Supply: {total:.2f} MW")

    st.write("### 📉 Cost Convergence")

    fig, ax = plt.subplots()
    ax.plot(history)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Cost")

    st.pyplot(fig)

    st.success("Optimization Completed 🚀")