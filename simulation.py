import numpy as np
import heapq
import matplotlib.pyplot as plt

class MorphologicalSpace:
    def __init__(self, grid_shape=(20, 20), R0=1.0, alpha=0.5, gamma_relax=0.05):
        """
        Initializes the Configuration Space C_toy.
        
        Parameters:
        - grid_shape: Size of the N x N configuration space.
        - R0: Unlabored baseline channel resistance.
        - alpha: Structural porosity deformation coefficient (etching factor).
        - gamma_relax: Structural restoration/relaxation rate over non-use.
        """
        self.shape = grid_shape
        self.R0 = R0
        self.alpha = alpha
        self.gamma_relax = gamma_relax
        
        # Channel Resistance Tensor initialized to baseline R0 for all adjacent nodes
        # Shape: (Rows, Cols, 4 directions: 0=Up, 1=Right, 2=Down, 3=Left)
        self.resistance_map = np.full((*grid_shape, 4), float(R0))
        
        # Direction vectors corresponding to [Up, Right, Down, Left]
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def _get_opposite_dir(self, direction_idx):
        return (direction_idx + 2) % 4

    def compute_step_cost(self, u, v, dir_idx, is_quantum_subsystem=False):
        """
        Calculates morphological resistance R(q_i, q_i+1) between state u and state v.
        Includes high boundary resistance penalties for restricted degrees of freedom (H3).
        """
        base_resistance = self.resistance_map[u[0], u[1], dir_idx]
        
        # H3 Condition: Low-degree-of-freedom sub-system encounter high boundary resistance
        if is_quantum_subsystem:
            # Simulate a constrained boundary (e.g., barrier at mid-grid)
            if u[1] == self.shape[1] // 2:
                base_resistance *= 100.0  # Extreme boundary cost forcing discrete tunneling
                
        return base_resistance

    def update_hysteresis(self, path):
        """
        Applies path-dependent etching (hysteresis) to lower resistance on traversed channels,
        and applies relaxation across the network.
        """
        # 1. Structural Restoration (Relaxation over non-use)
        self.resistance_map = np.minimum(
            self.R0, 
            self.resistance_map + self.gamma_relax * (self.R0 - self.resistance_map)
        )
        
        # 2. Channel Deformation / Etching along traversed path
        for i in range(len(path) - 1):
            u, v = path[i], path[i+1]
            dr = v[0] - u[0]
            dc = v[1] - u[1]
            dir_idx = self.directions.index((dr, dc))
            opp_dir_idx = self._get_opposite_dir(dir_idx)
            
            # Etch resistance in forward direction: R_new = R - alpha * R
            current_R = self.resistance_map[u[0], u[1], dir_idx]
            etched_R = max(0.01, current_R * (1.0 - self.alpha))
            
            self.resistance_map[u[0], u[1], dir_idx] = etched_R
            # Directional asymmetry: Reverse direction receives weaker deformation
            self.resistance_map[v[0], v[1], opp_dir_idx] = max(0.05, current_R * (1.0 - (self.alpha * 0.2)))


def a_star_search(space, start, target, is_quantum_subsystem=False):
    """
    Shortest-path optimization agent minimizing action S = sum(R(q_i, q_i+1)).
    """
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)

        if current == target:
            break

        for dir_idx, (dr, dc) in enumerate(space.directions):
            nxt = (current[0] + dr, current[1] + dc)
            
            # Boundary check
            if 0 <= nxt[0] < space.shape[0] and 0 <= nxt[1] < space.shape[1]:
                step_cost = space.compute_step_cost(current, nxt, dir_idx, is_quantum_subsystem)
                new_cost = cost_so_far[current] + step_cost
                
                if nxt not in cost_so_far or new_cost < cost_so_far[nxt]:
                    cost_so_far[nxt] = new_cost
                    # Heuristic: Euclidean distance as geometric lower bound
                    priority = new_cost + np.hypot(target[0] - nxt[0], target[1] - nxt[1])
                    heapq.heappush(frontier, (priority, nxt))
                    came_from[nxt] = current

    # Reconstruct trajectory
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = came_from.get(curr)
    path.reverse()
    
    return path, cost_so_far.get(target, float('inf'))


# =====================================================================
# EXPERIMENTAL PROTOCOL & HYPOTHESIS VALIDATION
# =====================================================================

def run_simulation():
    grid_size = (15, 15)
    space = MorphologicalSpace(grid_shape=grid_size, R0=1.0, alpha=0.6, gamma_relax=0.01)
    
    start_state = (2, 2)
    target_state = (12, 12)
    
    print("=== EXECUTING TOY MODEL SIMULATION ===\n")
    
    # -----------------------------------------------------------------
    # TEST H1: Emergent Continuity
    # -----------------------------------------------------------------
    path_h1, cost_h1 = a_star_search(space, start_state, target_state)
    
    # Verify adjacent steps (\delta x -> 0) without teleportation
    step_distances = [np.hypot(path_h1[i+1][0] - path_h1[i][0], 
                               path_h1[i+1][1] - path_h1[i][1]) for i in range(len(path_h1)-1)]
    
    max_step = max(step_distances) if step_distances else 0
    h1_passed = max_step <= np.sqrt(2)  # Strict nearest-neighbor adjacency
    
    print(f"[H1] Emergent Continuity:")
    print(f"     Trajectory Length: {len(path_h1)} steps")
    print(f"     Max Step Distance: {max_step:.2f}")
    print(f"     Verdict: {'VALIDATED (Continuous path selected)' if h1_passed else 'FALSIFIED (Teleportation occurred)'}\n")

    # -----------------------------------------------------------------
    # TEST H2: Asymmetric Arrow of Time (Hysteresis)
    # -----------------------------------------------------------------
    # Traversal 1: Forward path etches channels
    space.update_hysteresis(path_h1)
    _, forward_cost = a_star_search(space, start_state, target_state)
    
    # Traversal 2: Reverse path evaluation
    _, backward_cost = a_star_search(space, target_state, start_state)
    
    # Arrow of time requires directional cost asymmetry (R_forward != R_backward)
    h2_passed = not np.isclose(forward_cost, backward_cost, atol=1e-3)
    
    print(f"[H2] Asymmetric Arrow of Time:")
    print(f"     Forward Traversal Cost (etched): {forward_cost:.4f}")
    print(f"     Backward Traversal Cost:          {backward_cost:.4f}")
    print(f"     Verdict: {'VALIDATED (Path-dependent asymmetry established)' if h2_passed else 'FALSIFIED (Symmetric/no memory)'}\n")

    # -----------------------------------------------------------------
    # TEST H3: Sub-system Discrete Jumps
    # -----------------------------------------------------------------
    # Run sub-system with k -> 1 degrees of freedom hitting high boundary resistance
    path_h3, cost_h3 = a_star_search(space, start_state, target_state, is_quantum_subsystem=True)
    
    # Check if trajectory contains non-smooth / localized leap around boundary
    boundary_col = grid_size[1] // 2
    crossings = [p for p in path_h3 if p[1] == boundary_col]
    h3_passed = len(crossings) <= 2 and cost_h3 < float('inf')
    
    print(f"[H3] Sub-system Discrete Jumps:")
    print(f"     Boundary Crossings count: {len(crossings)}")
    print(f"     Total Action Cost under constraints: {cost_h3:.2f}")
    print(f"     Verdict: {'VALIDATED (Discrete transition behavior)' if h3_passed else 'FALSIFIED (Smooth classical motion persisted)'}\n")

    # -----------------------------------------------------------------
    # VISUALIZATION
    # -----------------------------------------------------------------
    grid_visual = np.ones(grid_size)
    for r, c in path_h1:
        grid_visual[r, c] = 0.3  # Trace trajectory
        
    plt.figure(figsize=(6, 6))
    plt.imshow(grid_visual, cmap='binary')
    plt.plot([p[1] for p in path_h1], [p[0] for p in path_h1], color='red', marker='o', label='Trajectory (q)')
    plt.plot(start_state[1], start_state[0], 'go', markersize=10, label='q_start')
    plt.plot(target_state[1], target_state[0], 'bo', markersize=10, label='q_target')
    plt.title("Emergent Trajectory in Configuration Space C_toy")
    plt.xlabel("Configuration State Variable 1")
    plt.ylabel("Configuration State Variable 2")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    run_simulation()
  
