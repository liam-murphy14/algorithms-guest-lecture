"""
Provide animations for my lecture.
Outline
1. show chess board with knight and bishop for intro explanation
2. go through way to transform into bfs algo
3. show bfs algo
4. explain that there are nice optimizations that can be done with double ended bfs
5. show double ended bfs
"""
import tkinter as tk
from collections import deque

# ACTUAL ALGOS


def _is_valid_position(x, y, n):
    """
    Check if position is valid.
    """
    return 0 <= x < n and 0 <= y < n


def _get_bishop_positions(bishop_x, bishop_y, n):
    """
    Get all possible positions for the bishop.
    """
    bishop_positions = set()
    for i in range(n):
        new_positions = [
            (bishop_x + i, bishop_y + i),
            (bishop_x + i, bishop_y - i),
            (bishop_x - i, bishop_y + i),
            (bishop_x - i, bishop_y - i),
        ]
        for new_x, new_y in new_positions:
            if _is_valid_position(new_x, new_y, n):
                bishop_positions.add((new_x, new_y))
    return bishop_positions


def bfs(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    n: int,
    bishop_x: int,
    bishop_y: int,
) -> int:
    """
    Run BFS to find shortest path from start to end.
    """
    row = [2, 2, -2, -2, 1, 1, -1, -1]
    col = [1, -1, 1, -1, 2, -2, 2, -2]
    visited = set()
    bishop_positions = _get_bishop_positions(bishop_x, bishop_y, n)
    # tuples of the form (x, y, distance, is_bishop_alive)
    queue = deque()
    queue.append((start_x, start_y, 0, True))
    while queue:
        x, y, distance, is_bishop_alive = queue.popleft()
        if (x, y) == (end_x, end_y):
            return distance
        if (x, y, is_bishop_alive) in visited:
            continue
        visited.add((x, y, is_bishop_alive))
        for dx, dy in zip(row, col):
            new_x, new_y = x + dx, y + dy
            if is_bishop_alive and (new_x, new_y) in bishop_positions:
                continue
            if _is_valid_position(new_x, new_y, n):
                if (new_x, new_y) == (bishop_x, bishop_y):
                    queue.append((new_x, new_y, distance + 1, False))
                else:
                    queue.append((new_x, new_y, distance + 1, is_bishop_alive))
    return -1


def dbfs(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    n: int,
    bishop_x: int,
    bishop_y: int,
):
    """
    Run double ended BFS to find shortest path from start to end.
    """
    row = [2, 2, -2, -2, 1, 1, -1, -1]
    col = [1, -1, 1, -1, 2, -2, 2, -2]
    visited_start = dict()
    visited_end = dict()
    bishop_positions = _get_bishop_positions(bishop_x, bishop_y, n)
    queue_start = deque()
    queue_end = deque()
    queue_start.append((start_x, start_y, 0, True))
    queue_end.append((end_x, end_y, 0, True))
    while queue_start and queue_end:
        x, y, distance, is_bishop_alive = queue_start.popleft()
        if (x, y) == (end_x, end_y):
            return distance
        if (x, y, True) in visited_end:
            return distance + visited_end[(x, y, True)]
        if (x, y, False) in visited_end:
            return distance + visited_end[(x, y, False)]
        if (x, y, is_bishop_alive) in visited_start:
            continue
        visited_start[(x, y, is_bishop_alive)] = distance
        for dx, dy in zip(row, col):
            new_x, new_y = x + dx, y + dy
            if is_bishop_alive and (new_x, new_y) in bishop_positions:
                continue
            if _is_valid_position(new_x, new_y, n):
                if (new_x, new_y) == (bishop_x, bishop_y):
                    queue_start.append((new_x, new_y, distance + 1, False))
                else:
                    queue_start.append((new_x, new_y, distance + 1, is_bishop_alive))
        x, y, distance, is_bishop_alive = queue_end.popleft()
        if (x, y) == (start_x, start_y):
            return distance
        if (x, y, True) in visited_start:
            return distance + visited_start[(x, y, True)]
        if (x, y, False) in visited_start:
            return distance + visited_start[(x, y, False)]
        if (x, y, is_bishop_alive) in visited_end:
            continue
        visited_end[(x, y, is_bishop_alive)] = distance
        for dx, dy in zip(row, col):
            new_x, new_y = x + dx, y + dy
            if is_bishop_alive and (new_x, new_y) in bishop_positions:
                continue
            if _is_valid_position(new_x, new_y, n):
                if (new_x, new_y) == (bishop_x, bishop_y):
                    queue_end.append((new_x, new_y, distance + 1, False))
                else:
                    queue_end.append((new_x, new_y, distance + 1, is_bishop_alive))
    return -1


# TKINTER ANIMATIONS

GREEN = "#B3C7A5"
RED = "#AE4D5B"
WHITE = "#FEF9EB"

# TODO: add interactivity here
n = 8
start_pos = (4, 2)
end_pos = (2, 6)
bishop_pos = (2, 3)

window = tk.Tk()
window.title("Knight Moves")
window.geometry("1200x700")

CHESS_WIDTH = 650
CHESS_HEIGHT = 650

# render chess board
chess_frame = tk.Canvas(window, width=CHESS_WIDTH, height=CHESS_HEIGHT)
chess_frame.place(x=25, y=25)
chess_squares = []
for i in range(n):
    chess_row = []
    for j in range(n):
        color = WHITE if (i + j) % 2 == 0 else GREEN
        x1, y1, x2, y2 = (
            j * CHESS_WIDTH / n,
            i * CHESS_HEIGHT / n,
            (j + 1) * CHESS_WIDTH / n,
            (i + 1) * CHESS_HEIGHT / n,
        )
        square_frame = chess_frame.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
        )
        chess_row.append(square_frame)
    chess_squares.append(chess_row)

# render buttons and counter
button_frame = tk.Frame(window, width=500, height=700)
button_frame.place(x=700, y=0)
counter = tk.Label(button_frame, text="0", font=("Arial", 50))
counter.pack(expand=True, fill=tk.X)
bfs_button = tk.Button(
    button_frame,
    text="Run BFS",
    command=lambda: bfs(
        start_pos[0],
        start_pos[1],
        end_pos[0],
        end_pos[1],
        n,
        bishop_pos[0],
        bishop_pos[1],
    ),
)
bfs_button.pack(expand=True, fill=tk.X)
dbfs_button = tk.Button(
    button_frame,
    text="Run Double BFS",
    command=lambda: dbfs(
        start_pos[0],
        start_pos[1],
        end_pos[0],
        end_pos[1],
        n,
        bishop_pos[0],
        bishop_pos[1],
    ),
)
dbfs_button.pack(expand=True, fill=tk.X)

# window.mainloop()


print(
    bfs(
        start_pos[0],
        start_pos[1],
        end_pos[0],
        end_pos[1],
        n,
        bishop_pos[0],
        bishop_pos[1],
    )
)
print(
    dbfs(
        start_pos[0],
        start_pos[1],
        end_pos[0],
        end_pos[1],
        n,
        bishop_pos[0],
        bishop_pos[1],
    )
)
