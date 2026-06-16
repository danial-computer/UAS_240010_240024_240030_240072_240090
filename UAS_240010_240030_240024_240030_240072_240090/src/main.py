"""
main.py — Lead Integration & CLI Runner
Simulasi TSP Logistik: Greedy vs Dynamic Programming (Held-Karp)

Penggunaan:
    python src/main.py --scenario subsidy
    python src/main.py --scenario crisis
    python src/main.py --scenario crisis --data data/custom.json
"""

import argparse
import os
import sys

# Pastikan folder src/ ada di path agar import antar modul berjalan
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_loader import load_dataset
from greedy_algorithm import greedy_tsp
from dp_algorithm import dp_tsp
from cost_calculator import calculate_fuel_consumption, calculate_tco


# ─────────────────────────────────────────────
#  Konstanta harga per skenario
# ─────────────────────────────────────────────
FUEL_PRICES = {
    "subsidy": 5_000,   # Rp 5.000 / liter
    "crisis":  20_000,  # Rp 20.000 / liter
}
SERVER_RATE = 50  # Rp 50 / ms


# ─────────────────────────────────────────────
#  Utilitas pencetakan tabel CLI
# ─────────────────────────────────────────────
def _separator(widths: list[int], char: str = "─", cross: str = "┼") -> str:
    """Buat baris pemisah tabel."""
    return "├" + cross.join(char * (w + 2) for w in widths) + "┤"


def _header_sep(widths: list[int]) -> str:
    return "╞" + "╪".join("═" * (w + 2) for w in widths) + "╡"


def _top_border(widths: list[int]) -> str:
    return "╭" + "┬".join("─" * (w + 2) for w in widths) + "╮"


def _bottom_border(widths: list[int]) -> str:
    return "╰" + "┴".join("─" * (w + 2) for w in widths) + "╯"


def _row(values: list[str], widths: list[int], bold_col: int = -1) -> str:
    cells = []
    for i, (v, w) in enumerate(zip(values, widths)):
        cells.append(f" {str(v).ljust(w)} ")
    return "│" + "│".join(cells) + "│"


def format_route(route: list[int], locations: list[dict]) -> str:
    """Mengubah list indeks menjadi nama lokasi yang mudah dibaca."""
    names = [locations[i]["name"] for i in route]
    return " → ".join(names)


def print_comparison_table(
    dataset_path: str,
    scenario: str,
    locations: list[dict],
    greedy_result: tuple,
    dp_result: tuple,
    weights: list[float],
    distance_matrix: list[list[float]],
) -> None:
    """
    Mencetak tabel perbandingan hasil Greedy vs DP ke terminal.

    Kolom: Metrik | Greedy | DP
    Baris: Dataset, Rute, Jarak Total, Bensin Habis,
           Waktu Running, Biaya Bensin, Biaya Server, TCO Akhir
    """
    fuel_price = FUEL_PRICES[scenario]

    g_route, g_dist, g_time = greedy_result
    d_route, d_dist, d_time = dp_result

    # Hitung konsumsi BBM
    g_fuel = calculate_fuel_consumption(g_route, distance_matrix, weights)
    d_fuel = calculate_fuel_consumption(d_route, distance_matrix, weights)

    # Hitung TCO
    g_tco = calculate_tco(g_fuel, fuel_price, g_time, SERVER_RATE)
    d_tco = calculate_tco(d_fuel, fuel_price, d_time, SERVER_RATE)

    # Format nilai
    g_route_str = format_route(g_route, locations)
    d_route_str = format_route(d_route, locations)

    def rp(val: float) -> str:
        return f"Rp {val:,.0f}"

    def km(val: float) -> str:
        return f"{val:.2f} km"

    def lt(val: float) -> str:
        return f"{val:.4f} L"

    def ms(val: float) -> str:
        return f"{val:.4f} ms"

    rows_data = [
        ("Dataset",        os.path.basename(dataset_path),  os.path.basename(dataset_path)),
        ("Skenario",       scenario.upper(),                 scenario.upper()),
        ("Harga BBM",      rp(fuel_price) + "/L",           rp(fuel_price) + "/L"),
        ("Rute",           g_route_str,                      d_route_str),
        ("Jarak Total",    km(g_dist),                       km(d_dist)),
        ("Bensin Habis",   lt(g_fuel),                       lt(d_fuel)),
        ("Waktu Running",  ms(g_time),                       ms(d_time)),
        ("Biaya Bensin",   rp(g_tco["fuel_cost"]),           rp(d_tco["fuel_cost"])),
        ("Biaya Server",   rp(g_tco["server_cost"]),         rp(d_tco["server_cost"])),
        ("TCO Akhir",      rp(g_tco["tco"]),                 rp(d_tco["tco"])),
    ]

    # Hitung lebar kolom secara dinamis
    col0_w = max(len(r[0]) for r in rows_data)
    col1_w = max(len(r[1]) for r in rows_data + [("", "GREEDY (Heuristik)", "")])
    col2_w = max(len(r[2]) for r in rows_data + [("", "", "DP / HELD-KARP (Optimal)")])

    col0_w = max(col0_w, len("Metrik"))
    col1_w = max(col1_w, len("GREEDY (Heuristik)"))
    col2_w = max(col2_w, len("DP / HELD-KARP (Optimal)"))

    widths = [col0_w, col1_w, col2_w]

    # Header judul
    total_width = sum(widths) + len(widths) * 3 + len(widths) - 1
    title = f" TSP LOGISTIK — PERBANDINGAN HASIL ALGORITMA "
    print()
    print("╔" + "═" * total_width + "╗")
    print("║" + title.center(total_width) + "║")
    print("╚" + "═" * total_width + "╝")
    print()

    # Tabel
    print(_top_border(widths))
    print(_row(["Metrik", "GREEDY (Heuristik)", "DP / HELD-KARP (Optimal)"], widths))
    print(_header_sep(widths))

    for i, (metric, gval, dval) in enumerate(rows_data):
        print(_row([metric, gval, dval], widths))
        if i == 2:  # pemisah setelah baris info header
            print(_separator(widths))
        elif i == len(rows_data) - 2:  # pemisah sebelum TCO
            print(_separator(widths))

    print(_bottom_border(widths))

    # Ringkasan
    saving = d_tco["tco"] - g_tco["tco"]
    print()
    if saving > 0:
        print(f"  ✅  Greedy lebih hemat TCO sebesar {rp(abs(saving))} dibanding DP.")
    elif saving < 0:
        print(f"  ✅  DP lebih hemat TCO sebesar {rp(abs(saving))} dibanding Greedy.")
    else:
        print("  ⚖️   TCO kedua algoritma identik.")
    print()


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Simulasi TSP Logistik Pengiriman Paket\n"
            "Membandingkan algoritma Greedy vs Dynamic Programming (Held-Karp)\n"
            "dalam dua skenario ekonomi: subsidi BBM dan krisis BBM."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Contoh penggunaan:\n"
            "  python src/main.py --scenario subsidy\n"
            "  python src/main.py --scenario crisis\n"
            "  python src/main.py --scenario crisis --data data/custom.json\n"
            "  python src/main.py --scenario subsidy --data data/dataset_10.json\n"
        ),
    )
    parser.add_argument(
        "--scenario",
        required=True,
        choices=["subsidy", "crisis"],
        help=(
            "Skenario harga BBM yang akan disimulasikan.\n"
            "  subsidy = Rp 5.000/liter (BBM bersubsidi)\n"
            "  crisis  = Rp 20.000/liter (krisis energi)"
        ),
    )
    parser.add_argument(
        "--data",
        default="data/dataset.json",
        metavar="PATH",
        help=(
            "Path ke file dataset JSON. "
            "(default: data/dataset.json)\n"
            "Contoh: --data data/rute_bandung.json"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # 1. Muat dataset
    print(f"\n  📂  Membaca dataset: {args.data}")
    dataset = load_dataset(args.data)

    locations       = dataset["locations"]
    distance_matrix = dataset["distance_matrix"]
    weights         = [loc["weight_kg"] for loc in locations]

    n = len(locations)
    print(f"  🗺️   Jumlah lokasi    : {n} (1 Hub + {n - 1} Pelanggan)")
    print(f"  ⚙️   Skenario         : {args.scenario.upper()}")
    print(f"  💰  Harga BBM        : Rp {FUEL_PRICES[args.scenario]:,}/liter")

    # 2. Jalankan algoritma Greedy
    print("\n  🔄  Menjalankan Greedy (Nearest Neighbor)...")
    greedy_result = greedy_tsp(distance_matrix, start_node=0)
    print(f"       Selesai dalam {greedy_result[2]:.4f} ms")

    # 3. Jalankan algoritma DP (Held-Karp)
    print("  🔄  Menjalankan DP / Held-Karp...")
    dp_result = dp_tsp(distance_matrix, start_node=0)
    print(f"       Selesai dalam {dp_result[2]:.4f} ms")

    # 4. Cetak tabel perbandingan
    print_comparison_table(
        dataset_path=args.data,
        scenario=args.scenario,
        locations=locations,
        greedy_result=greedy_result,
        dp_result=dp_result,
        weights=weights,
        distance_matrix=distance_matrix,
    )


if __name__ == "__main__":
    main()
