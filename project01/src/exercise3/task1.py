with open("input.txt") as f:
    lines = [line.strip() for line in f if line.strip()]

matrix = []
for line in lines:
    row = list(map(int, line.split()))
    matrix.append(row)

size = len(matrix)
visited = [[False] * size for _ in range(size)]
squares = 0
circles = 0

def find_shape(row, col):
    stack = [(row, col)]
    visited[row][col] = True
    cells = []

    while stack:
        r, c = stack.pop()
        cells.append((r, c))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < size and 0 <= nc < size:
                if not visited[nr][nc] and matrix[nr][nc] == 1:
                    visited[nr][nc] = True
                    stack.append((nr, nc))

    return cells

for i in range(size):
    for j in range(size):
        if matrix[i][j] == 1 and not visited[i][j]:
            cells = find_shape(i, j)

            rows = [c[0] for c in cells]
            cols = [c[1] for c in cells]

            min_row = min(rows)
            max_row = max(rows)
            min_col = min(cols)
            max_col = max(cols)

            height = max_row - min_row + 1
            width = max_col - min_col + 1

            if height == width and len(cells) == height * width:
                squares += 1
            else:
                circles += 1

print(squares, circles)
