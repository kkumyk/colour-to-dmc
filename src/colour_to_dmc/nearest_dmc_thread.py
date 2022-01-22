import csv
from scipy import spatial as sp

DMC_CSV = "dmc.csv"

dmc_threads = []
with open(DMC_CSV, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for index, row in enumerate(reader):
        dmc_threads.append(
            {
                "index": index,
                "floss": "#" + row["floss#"],
                "description": row["description"],
                "red": int(row["red"]),
                "green": int(row["green"]),
                "blue": int(row["blue"]),
                "hex": "#" + row["hex"],
                "dmc_row": row["row"],
                "prim_sec_ter": row["prim-sec-ter"]
            }
        )

rgb_colours = []
for colour in dmc_threads:
    rgb_colours.append((colour["red"], colour["green"], colour["blue"]))


def rgb_to_dmc(r, g, b):
    """
    Look up the nearest neighbors with k-d tree.
    R, G, B values are used to identify the closest DMC thread from the "dmc.csv" file.
    """

    tree = sp.KDTree(rgb_colours)
    # don't need the Euclidean distance only the index
    _, dmc_thread = tree.query((r, g, b))
    return dmc_threads[dmc_thread]


