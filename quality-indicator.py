# In [460]: mat2.shape
# Out[460]: (46, 52)

# def coverage(mat: np.


mat2a = mat2.copy()  # wuch3
mat2a = mat_hlm.copy()
# mat2a = mat10.copy()

row, col = mat2a.shape
min_ = 5
max_ = 50
limit = max(0.2 * min(row, col), min_)
# limit = min(limit, max_)

# find min(row, col) max numbers and calculate abs(
# r, c = divmod(mat2a.argmax(), col)

spread = 0
tot_coll = 0
for elm in range(min(row, col)):
    r, c = divmod(mat2a.argmax(), col)

    ideal_c = r * col / row

    max_ = mat2a[r, c]

    valid = False
    if abs(c - ideal_c) < limit:
        logger.info("  r: %s, c: %s, %s", r, c, max_)
        valid = True
        mat2a[r] = 0  # reset rows
        for idx in range(col):  # reset cols
            mat2a[r, idx] = 0
    else:
        # reset mat2a[r, c] only
        mat2a[r, c] = 0

    if max_ and valid:
        _ = abs(c - ideal_c)
        spread += _
        tot_coll += 1

spread /= tot_coll

logger.info("\n limit: %s, av. spread: %.2f, coverage: %.2f%%", limit, spread, tot_coll/min(row,col) * 100)

# wuch3 av. spread: 1.83, covera ge rate: 0.96
# limit: 9.200000000000001, av. spread: 1.83, coverage: 95.65%

# hlmch2 av. spread: 5.72, coverage rate: 0.71
# limit: 11.0, av. spread: 5.72, coverage: 70.91%

# loverch10 limit=84.4 av. spread: 8.81, coverage: 75.12%
# limit: 20, av. spread: 1.86, coverage: 64.22%
# limit: 30, av. spread: 2.46, coverage: 66.82%
# limit: 50, av. spread: 4.00, coverage: 69.19%
# limit: 84.4, av. spread: 8.81, coverage: 75.12%