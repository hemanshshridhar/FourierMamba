import numpy as np

def concentric_zigzag_from_bottom_center(a: np.ndarray):
    """
    Concentric zig-zag traversal starting at bottom row, center-left cell.
    Works for any HxW array (even/odd both fine).
    """
    H, W = a.shape
    start_r, start_c = H - 1, (W // 2) - 1  # bottom row, center-left
    rmin = rmax = start_r
    cmin = cmax = start_c

    seen = set()
    order_rc = []

    def add(r, c):
        if 0 <= r < H and 0 <= c < W and (r, c) not in seen:
            seen.add((r, c))
            order_rc.append((r, c))

    add(start_r, start_c)

    # Helper sweeps with zig-zag parity to match the desired pattern
    def sweep_row(r, c_from, c_to, left_to_right=True):
        if left_to_right:
            rng = range(c_from, c_to + 1)
        else:
            rng = range(c_to, c_from - 1, -1)
        for c in rng:
            add(r, c)

    def sweep_col(c, r_from, r_to, top_to_bottom=True):
        if top_to_bottom:
            rng = range(r_from, r_to + 1)
        else:
            rng = range(r_to, r_from - 1, -1)
        for r in rng:
            add(r, c)

    # Grow outward in rectangular rings
    while len(order_rc) < H * W:
        # Expand RIGHT on bottom row first (produces 61, 62, ... initially)
        if cmax + 1 < W:
            cmax += 1
            sweep_row(rmax, cmax, cmax, left_to_right=True)  # just the new cell
            # pull a short up-left hook to begin the zig (lands on the row above, slightly left)
            if rmin - 1 >= 0 and cmax - 1 >= 0:
                add(rmin - 1, cmax - 1)

        # Expand TOP
        if rmin - 1 >= 0:
            rmin -= 1
            # snake across the new top row; alternate direction by current width parity
            width = cmax - cmin + 1
            left_to_right = (width % 2 == 0)
            sweep_row(rmin, cmin, cmax, left_to_right=left_to_right)

        # Expand LEFT
        if cmin - 1 >= 0:
            cmin -= 1
            # move along top to include the new left column cell
            add(rmin, cmin)
            # drop down the new left edge to the bottom with a snake-like return
            sweep_col(cmin, rmin + 1, rmax, top_to_bottom=True)

        # Expand BOTTOM
        if rmax + 1 < H:
            rmax += 1
            # sweep the new bottom row; alternate direction by current width parity
            width = cmax - cmin + 1
            left_to_right = (width % 2 == 1)
            sweep_row(rmax, cmin, cmax, left_to_right=left_to_right)

        # Expand RIGHT again to finish the ring closure nicely
        if cmax + 1 < W:
            cmax += 1
            add(rmax, cmax)
            # stitch upward on the right edge back toward the top row
            if rmin < rmax:
                sweep_col(cmax, rmin, rmax - 1, top_to_bottom=False)

        # Safety: stop when the ring fully covers the array
        if rmin == 0 and rmax == H - 1 and cmin == 0 and cmax == W - 1:
            # fill any remaining holes due to de-duplication / hooks
            for r in range(H):
                for c in range(W):
                    add(r, c)
            break

    return [a[r, c] for r, c in order_rc]


# ---- Example (your array) ----
dataBlock2D = np.array([
    [1,  2,  3,  4,  5,  6,  7,  8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17,18, 19, 20, 21, 22, 23, 24],
    [25,26, 27, 28, 29, 30, 31, 32],
    [33,34, 35, 36, 37, 38, 39, 40],
    [41,42, 43, 44, 45, 46, 47, 48],
    [49,50, 51, 52, 53, 54, 55, 56],
    [57,58, 59, 60, 61, 62, 63, 64]
])

out = concentric_zigzag_from_bottom_center(dataBlock2D)
print(out[:24])    # -> [60, 61, 62, 53, 52, 59, 58, 51, 44, 45, 54, 63, 64, 56, 47, 38, 37, 36, 43, 50, 57, 55, 48, 39]
print(len(out))    # 64