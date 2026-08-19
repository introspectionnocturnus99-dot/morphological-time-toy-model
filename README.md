# morphological-time-toy-model
Python toy model simulation for emergent time via morphological resistance minimization.
# Morphological Resistance & Emergent Time (Toy Model)

This repository contains the Python computational simulation (**Toy Model**) designed to test the hypothesis of emergent time and causality from the minimization of **Morphological Resistance $R(q)$** within a static Configuration Space $\mathcal{C}_{\text{toy}}$.

The model demonstrates how continuity, the arrow of time, and discrete transitions can naturally emerge without programming an explicit temporal variable ($t$).

---

## 🎯 Evaluated Hypotheses

The code evaluates three primary validation/falsification metrics:

| Hypothesis | Expected Phenomenon | Falsification Criterion |
| :--- | :--- | :--- |
| **H1: Emergent Continuity** | The agent selects a continuous sequence of nearest-neighbor states ($\delta x \to 0$). | Selection of chaotic leaps or "teleportation" despite continuous paths existing. |
| **H2: Arrow of Time** | Channel hysteresis reduces $R(q)$ along traversed paths, establishing a preferred direction. | Symmetric trajectories ($R_{\text{forward}} = R_{\text{backward}}$) with zero path memory. |
| **H3: Discrete Jumps** | Sub-systems with ultra-low degrees of freedom ($k \to 1$) undergo discrete leaps due to high boundary resistance (analogous to quantum tunneling). | Smooth classical motion persists regardless of boundary constraints. |

---

## 🛠️ Requirements & Installation

To run the simulation, you need Python 3 and the following dependencies installed:

```bash
pip install numpy
matplotlib```

## 🚀 Running the Simulation

1. Clone this repository or download the main script:
```bash
git clone [https://github.com/introspectionnocturnus99-dot/morphological-time-toy-model.git]
2. Run the validation script:
```bash
python simulation.py
