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
import time

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
    for i in range(1, n):
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
    chess_frame: tk.Canvas | None = None,
    sleep_time: float = 0,
    counter: tk.Label | None = None,
    debug: bool = False,
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
    num_visited = 0
    while queue:
        x, y, distance, is_bishop_alive = queue.popleft()

        # check if we found the end
        if (x, y) == (end_x, end_y):
            if chess_frame is not None:
                chess_frame.itemconfig(chess_squares[x][y], fill=GREY)
                # TODO: move knight here and show path ? potentially
                chess_frame.update()
                time.sleep(sleep_time)
            if debug:
                print(f"Found after {num_visited} nodes")
            return distance

        # check if we can skip this node
        if (x, y, is_bishop_alive) in visited:
            if debug:
                print(f"Already visited {(x, y, is_bishop_alive)}")
            continue

        visited.add((x, y, is_bishop_alive))
        num_visited += 1

        if debug:
            print(f"Visiting {(x, y, is_bishop_alive)}")
        if counter is not None:
            counter.config(text=f"Visited: {num_visited} nodes")
        if chess_frame is not None:
            chess_frame.itemconfig(chess_squares[x][y], fill=GREY)
            chess_frame.update()
            time.sleep(sleep_time)

        for dx, dy in zip(row, col):
            new_x, new_y = x + dx, y + dy
            if is_bishop_alive and (new_x, new_y) in bishop_positions:
                continue
            if _is_valid_position(new_x, new_y, n):
                if (new_x, new_y) == (bishop_x, bishop_y):
                    queue.append((new_x, new_y, distance + 1, False))
                else:
                    queue.append((new_x, new_y, distance + 1, is_bishop_alive))

    if debug:
        print(f"Not found after {num_visited} nodes")
    return -1


def dbfs(
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
    n: int,
    bishop_x: int,
    bishop_y: int,
    chess_frame: tk.Canvas | None = None,
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
GREY = "#C0C0C0"

# TODO: add interactivity here
n = 16
start_pos = (4, 2)
end_pos = (2, 6)
bishop_pos = (2, 3)

window = tk.Tk()
window.title("Knight Moves")
window.geometry("1200x700")  # TODO: make responsive/ no hardcoding
CHESS_SIZE = 650  # TODO: make responsive/ no hardcoding
CHESS_MARGIN = 25  # TODO: make responsive/ no hardcoding

# render chess board
chess_frame = tk.Canvas(window, width=CHESS_SIZE, height=CHESS_SIZE)
chess_frame.place(x=CHESS_MARGIN, y=CHESS_MARGIN)
chess_squares = []  # list of lists of rectangle ids
for i in range(n):
    chess_row = []
    for j in range(n):
        color = WHITE if (i + j) % 2 == 0 else GREEN
        x1, y1, x2, y2 = (
            j * CHESS_SIZE / n,
            i * CHESS_SIZE / n,
            (j + 1) * CHESS_SIZE / n,
            (i + 1) * CHESS_SIZE / n,
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

# images
SQUARE_WIDTH = CHESS_SIZE / n

unscaled_knight_img = tk.PhotoImage(file="knight.png")
scale_factor = int(unscaled_knight_img.width() / SQUARE_WIDTH) + 1
knight_img = unscaled_knight_img.subsample(scale_factor, scale_factor)

unscaled_bishop_img = tk.PhotoImage(file="bishop.png")
scale_factor = int(unscaled_bishop_img.width() / SQUARE_WIDTH) + 1
bishop_img = unscaled_bishop_img.subsample(scale_factor, scale_factor)

unscaled_king_img = tk.PhotoImage(file="king.png")
scale_factor = int(unscaled_king_img.width() / SQUARE_WIDTH) + 1
king_img = unscaled_king_img.subsample(scale_factor, scale_factor)

chess_frame.create_image(
    start_pos[1] * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
    start_pos[0] * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
    image=knight_img,
)
chess_frame.create_image(
    end_pos[1] * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
    end_pos[0] * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
    image=king_img,
)
chess_frame.create_image(
    bishop_pos[1] * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
    bishop_pos[0] * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
    image=bishop_img,
)

bishop_positions = _get_bishop_positions(bishop_pos[0], bishop_pos[1], n)
for x, y in bishop_positions:
    chess_frame.itemconfig(chess_squares[x][y], fill=RED)
chess_frame.update()

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
        chess_frame,
        0.1,
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
        chess_frame,
    ),
)
dbfs_button.pack(expand=True, fill=tk.X)

window.mainloop()


# print(
#     bfs(
#         start_pos[0],
#         start_pos[1],
#         end_pos[0],
#         end_pos[1],
#         n,
#         bishop_pos[0],
#         bishop_pos[1],
#         None,
#         0.0,
#         None,
#         True,
#     )
# )
# print(
#     dbfs(
#         start_pos[0],
#         start_pos[1],
#         end_pos[0],
#         end_pos[1],
#         n,
#         bishop_pos[0],
#         bishop_pos[1],
#     )
# )
