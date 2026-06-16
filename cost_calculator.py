def calculate_fuel_consumption(
    route: list[int],
    distance_matrix: list[list[float]],
    weights: list[float]
) -> float:
    
    """
    Menghitung total konsumsi BBM berdasarkan perubahan
    beban paket selama perjalanan.

    """

    total_weight = sum(weights)

    remaining_weight = total_weight

    fuel_consumption = 0.0

    for i in range(len(route) - 1):

        current_node = route[i]
        next_node = route[i + 1]

        distance = distance_matrix[
            current_node
        ][
            next_node
        ]

        if total_weight == 0:
            load_ratio = 0

        else:
            load_ratio = (
                remaining_weight / total_weight
            )

        # Formula konsumsi:
        # kosong = 0.02 liter/km
        # penuh = 0.05 liter/km

        fuel_ratio = (
            0.02 +
            0.03 * load_ratio
        )

        fuel_consumption += (
            distance * fuel_ratio
        )

        # ketika sampai pelanggan,
        # paket dikurangi

        if next_node != route[0]:

            remaining_weight -= weights[next_node]
    return fuel_consumption



def calculate_tco(
    fuel_consumed: float,
    fuel_price: float,
    exec_time_ms: float,
    server_rate: float
) -> dict:
    """
    Menghitung Total Cost of Ownership.

    """

    fuel_cost = (
        fuel_consumed *
        fuel_price
    )

    server_cost = (
        exec_time_ms *
        server_rate
    )

    total_cost = (
        fuel_cost +
        server_cost
    )

    return {
        "fuel_consumption": fuel_consumed,
        "fuel_cost": fuel_cost,
        "server_cost": server_cost,
        "tco": total_cost
    }