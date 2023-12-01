"""
Provide animations for my lecture.
TODO: refactor into class
Outline
1. show chess board with knight and bishop for intro explanation
2. go through way to transform into bfs algo
3. show bfs algo
4. explain that there are nice optimizations that can be done with double ended bfs
5. show double ended bfs
"""
import tkinter as tk
from tkinter import ttk
from collections import deque
import time

# ACTUAL ALGOS


def _is_valid_position(x: int, y: int, n: int) -> bool:
    """
    Check if position is valid.
    """
    return 0 <= x < n and 0 <= y < n


def _get_bishop_positions(bishop_x: int, bishop_y: int, n: int) -> set[tuple[int, int]]:
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
    counter: tk.StringVar | None = None,
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
        if not running:
            return -1

        x, y, distance, is_bishop_alive = queue.popleft()

        # check if we found the end
        if (x, y) == (end_x, end_y):
            if chess_frame is not None:
                chess_frame.itemconfig(chess_squares[x][y], fill=GREY)
                # TODO: move knight here and show path ? potentially
                chess_frame.update()
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
            counter.set(f"Visited: {num_visited} nodes")
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


def _reset_chess_board() -> None:
    """
    Reset chess board to original state.
    """
    global chess_squares
    chess_squares = []
    bishop_positions = _get_bishop_positions(bishop_x.get(), bishop_y.get(), n.get())
    for i in range(n.get()):
        chess_row = []
        for j in range(n.get()):
            color = (
                RED
                if (i, j) in bishop_positions
                else WHITE
                if (i + j) % 2 == 0
                else GREEN
            )
            x1, y1, x2, y2 = (
                j * CHESS_SIZE / n.get(),
                i * CHESS_SIZE / n.get(),
                (j + 1) * CHESS_SIZE / n.get(),
                (i + 1) * CHESS_SIZE / n.get(),
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
    SQUARE_WIDTH = CHESS_SIZE / n.get()

    unscaled_knight_img = tk.PhotoImage(file="knight.png")
    scale_factor = int(unscaled_knight_img.width() / SQUARE_WIDTH) + 1
    global knight_img
    knight_img = unscaled_knight_img.subsample(scale_factor, scale_factor)

    unscaled_bishop_img = tk.PhotoImage(file="bishop.png")
    scale_factor = int(unscaled_bishop_img.width() / SQUARE_WIDTH) + 1
    global bishop_img
    bishop_img = unscaled_bishop_img.subsample(scale_factor, scale_factor)

    unscaled_king_img = tk.PhotoImage(file="king.png")
    scale_factor = int(unscaled_king_img.width() / SQUARE_WIDTH) + 1
    global king_img
    king_img = unscaled_king_img.subsample(scale_factor, scale_factor)

    global knight_image_id, bishop_img_id, king_image_id
    knight_image_id = chess_frame.create_image(
        start_y.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        start_x.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        image=knight_img,
    )
    king_image_id = chess_frame.create_image(
        end_y.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        end_x.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        image=king_img,
    )
    bishop_img_id = chess_frame.create_image(
        bishop_y.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        bishop_x.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        image=bishop_img,
    )
    chess_frame.update()


def _reset_knight_position():
    """
    Reset knight position to original state.
    """
    global knight_image_id
    chess_frame.delete(knight_image_id)
    knight_image_id = chess_frame.create_image(
        start_y.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        start_x.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        image=knight_img,
    )
    chess_frame.update()


def _reset_bishop_position():
    """
    Reset bishop position to original state.
    """
    global bishop_img_id
    chess_frame.delete(bishop_img_id)
    bishop_img_id = chess_frame.create_image(
        bishop_y.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        bishop_x.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        image=bishop_img,
    )
    _reset_chess_board()
    chess_frame.update()


def _reset_king_position():
    """
    Reset king position to original state.
    """
    global king_image_id
    chess_frame.delete(king_image_id)
    king_image_id = chess_frame.create_image(
        end_y.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        end_x.get() * CHESS_SIZE / n.get() + CHESS_SIZE / (2 * n.get()),
        image=king_img,
    )
    chess_frame.update()


def _start():
    """
    Start the animation loop
    """
    run_buttons_frame.pack_forget()
    cancel_buttons_frame.pack(pady=20)
    global running
    running = True


def _stop():
    """
    Stop the animation loop
    """
    global running
    running = False
    cancel_buttons_frame.pack_forget()
    run_buttons_frame.pack(pady=20)
    _reset_chess_board()
    counter_text.set("Visited: 0 nodes")
    result_text.set("")


def _start_bfs():
    """
    Start the BFS animation loop
    """
    _start()
    shortest_path_length = bfs(
        start_x.get(),
        start_y.get(),
        end_x.get(),
        end_y.get(),
        n.get(),
        bishop_x.get(),
        bishop_y.get(),
        chess_frame,
        sleep_time.get(),
        counter_text,
    )
    if shortest_path_length == -1:
        result_text.set("No valid path exists!")
    else:
        result_text.set(f"Shortest path length: {shortest_path_length}")


GREEN = "#B3C7A5"
RED = "#AE4D5B"
WHITE = "#FEF9EB"
GREY = "#C0C0C0"


window = tk.Tk()
window.title("Knight Moves")
content = ttk.Frame(window)  # TODO: make responsive/ no hardcoding
content.pack()
CHESS_SIZE = 650  # TODO: make responsive/ no hardcoding
MARGIN = 25  # TODO: make responsive/ no hardcoding

# defaults
n = tk.IntVar(value=8)
n.trace_add("write", lambda *_: _reset_chess_board())
start_x = tk.IntVar(value=4)
start_y = tk.IntVar(value=2)
start_x.trace_add("write", lambda *_: _reset_knight_position())
start_y.trace_add("write", lambda *_: _reset_knight_position())
end_x = tk.IntVar(value=2)
end_y = tk.IntVar(value=6)
end_x.trace_add("write", lambda *_: _reset_king_position())
end_y.trace_add("write", lambda *_: _reset_king_position())
bishop_x = tk.IntVar(value=2)
bishop_y = tk.IntVar(value=3)
bishop_x.trace_add("write", lambda *_: _reset_bishop_position())
bishop_y.trace_add("write", lambda *_: _reset_bishop_position())
sleep_time = tk.DoubleVar(value=0.1)

# render chess board
chess_frame = tk.Canvas(content, width=CHESS_SIZE, height=CHESS_SIZE)
chess_frame.grid(row=0, column=0, padx=MARGIN, pady=MARGIN)


_reset_chess_board()

# render buttons and counter
control_frame = ttk.Frame(content)
control_frame.grid(row=0, column=1, padx=(0, MARGIN), pady=MARGIN)

counter_text = tk.StringVar(control_frame, value="Visited: 0 nodes")
counter = ttk.Label(control_frame, textvariable=counter_text, font=("Arial", 44))
counter.pack()

result_text = tk.StringVar(control_frame, value="")
result = ttk.Label(control_frame, textvariable=result_text, font=("Arial", 18))
result.pack(pady=(10, 0))

run_buttons_frame = ttk.Frame(control_frame)
bfs_button = ttk.Button(
    run_buttons_frame,
    text="Run BFS",
    command=lambda: _start_bfs(),
)
bfs_button.grid(row=0, column=0, padx=10)
dbfs_button = ttk.Button(
    run_buttons_frame, text="Run Double BFS", command=lambda: print("hi")
)
dbfs_button.grid(row=0, column=1, padx=10)
run_buttons_frame.pack(pady=20)

cancel_buttons_frame = ttk.Frame(control_frame)
cancel_button = ttk.Button(
    cancel_buttons_frame,
    text="Reset",
    command=_stop,
)
cancel_button.pack()

run_controls_frame = ttk.Frame(control_frame)
n_label = ttk.Label(run_controls_frame, text="Chess board size:")
n_entry = ttk.Entry(run_controls_frame, textvariable=n, width=8)
n_label.grid(row=0, column=0, padx=10)
n_entry.grid(row=0, column=1, padx=10, columnspan=2)
tick_speed_label = ttk.Label(run_controls_frame, text="Tick duration:")
tick_speed_entry = ttk.Entry(run_controls_frame, textvariable=sleep_time, width=8)
tick_speed_label.grid(row=1, column=0, padx=10)
tick_speed_entry.grid(row=1, column=1, padx=10, columnspan=2)
start_pos_label = ttk.Label(run_controls_frame, text="Start position:")
start_x_entry = ttk.Entry(run_controls_frame, textvariable=start_x, width=3)
start_y_entry = ttk.Entry(run_controls_frame, textvariable=start_y, width=3)
start_pos_label.grid(row=2, column=0, padx=10)
start_x_entry.grid(row=2, column=1, padx=(10, 0))
start_y_entry.grid(row=2, column=2, padx=(0, 10))
end_pos_label = ttk.Label(run_controls_frame, text="End position:")
end_x_entry = ttk.Entry(run_controls_frame, textvariable=end_x, width=3)
end_y_entry = ttk.Entry(run_controls_frame, textvariable=end_y, width=3)
end_pos_label.grid(row=3, column=0, padx=10)
end_x_entry.grid(row=3, column=1, padx=(10, 0))
end_y_entry.grid(row=3, column=2, padx=(0, 10))
bishop_pos_label = ttk.Label(run_controls_frame, text="Bishop position:")
bishop_x_entry = ttk.Entry(run_controls_frame, textvariable=bishop_x, width=3)
bishop_y_entry = ttk.Entry(run_controls_frame, textvariable=bishop_y, width=3)
bishop_pos_label.grid(row=4, column=0, padx=10)
bishop_x_entry.grid(row=4, column=1, padx=(10, 0))
bishop_y_entry.grid(row=4, column=2, padx=(0, 10))
run_controls_frame.pack(pady=20)


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
