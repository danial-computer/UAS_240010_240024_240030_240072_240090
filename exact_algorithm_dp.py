import time

def exact_algorithm_dp(
        distances_matrix: list[list[float]],
        start_node: int = 0
) -> tuple[list[int], float, float]:
    start_time = time.perf_counter()
    n = len(distances_matrix)

    memo = {}
    parent = {}

    def visit(mask: int, current:int) -> float:
        if mask == (1 << n) - 1:
            return distances_matrix[current][start_node]
        
        state = (mask, current)
        if state in memo:
            return memo[state]
        
        minimum_cost = float('inf')
        next_node_selected = -1

        for next_node in range(n):
            if mask & (1 << next_node) == 0:
                new_cost = (
                    distances_matrix[current][next_node] + visit(mask | (1 << next_node), next_node)
                )
                if new_cost < minimum_cost:
                    minimum_cost = new_cost
                    next_node_selected = next_node

        memo[state] = minimum_cost
        parent[state] = next_node_selected
        return minimum_cost         
    
    total_distance = visit(1 << start_node, start_node)

    # Reconstruct the path
    route = [start_node]
    mask = 1 << start_node
    current = start_node

    while True:
        next_node = parent.get((mask, current))
        if next_node is None:
            break
        route.append(next_node)
        mask |= (1 << next_node)
        current = next_node

        if current == start_node:
            break

    end_time = time.perf_counter()

    execution_time_ms = (end_time - start_time) * 1000
    return (
        route, 
        total_distance, 
        execution_time_ms
    )
