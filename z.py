import numpy as np

def progressive_zigzag(a: np.ndarray):
    """
    Progressive concentric zigzag like the diagram:
    start: bottom row, center-left cell
    then expand a ring each iteration and snake around its perimeter:
      bottom→right, right edge↑, top→left, left edge↓ (repeat)
    """
    H, W = a.shape
    start_c = (W // 2) - 1        # center-left
    rmax = H - 1                  # bottom row fixed
    rmin = rmax                   # top of current ring
    cmin = cmax = start_c         # left/right of current ring

    order = []
    seen = set()

    def add(r, c):
        if 0 <= r < H and 0 <= c < W and (r, c) not in seen:
            seen.add((r, c))
            order.append((r, c))

    # start on the green dot
    add(rmax, start_c)

    first_ring = True
    while len(order) < H * W:
        # --- expand RIGHT first (extra step the first time to match the short run in the figure) ---
        steps_right = 2 if first_ring and cmax + 2 < W else 1
        for _ in range(steps_right):
            if cmax + 1 < W:
                cmax += 1
                # go right on bottom to the new right edge
                for c in range(order[-1][1] + 1, cmax + 1):
                    add(rmax, c)
        first_ring = False

        # --- expand UP and LEFT by one (if possible) ---
        if rmin > 0:
            rmin -= 1
        if cmin > 0:
            cmin -= 1

        # up the right edge
        for r in range(rmax - 1, rmin - 1, -1):
            add(r, cmax)

        # left across the new top row
        for c in range(cmax - 1, cmin - 1, -1):
            add(rmin, c)

        # down the new left edge
        for r in range(rmin + 1, rmax + 1):
            add(r, cmin)

        # loop grows the ring again

    # return values in traversal order
    return [a[r, c] for r, c in order]


# --- Example with your 8×8 block ---
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

out = progressive_zigzag(dataBlock2D)
print(out[:64])   # preview
print(len(out))   # 64