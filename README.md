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

## 🔬 Theoretical Mapping (White Paper ↔ Code)

| Theoretical Concept | Implementation in `simulation.py` |
| :--- | :--- |
| **Configuration Space ($\mathcal{C}_{\text{toy}}$)** | Discrete Grid Graph (`grid_shape`) |
| **Morphological Resistance $R(q)$** | Structural Tensor/Array (`resistance_map`) |
| **Action $S = \sum R(q_i, q_{i+1})$** | Accumulated Cost Function in $A^*$ Search (`a_star_search`) |
| **Arrow of Time / Memory** | Directional Channel Etching (`update_hysteresis`) |
| **Boundary / Quantum Jump** | High Resistance Penalty Boundary (`compute_step_cost`) |

---

## 🛠️ Requirements & Installation

To run the simulation, you need Python 3 and the following dependencies installed:

```bash
pip install numpy matplotlib
```bash
## 🚀 Running the Simulation

1. Clone this repository or download the main script:
```bash
git clone https://github.com/introspectionnocturnus99-dot/morphological-time-toy-model.git
cd morphological-time-toy-model
```bash
2. Run the validation script:
```bash
python simulation.py
```bash
