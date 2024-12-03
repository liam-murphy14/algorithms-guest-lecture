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
import sys
import cProfile
import random as r
import click

GREEN = "#B3C7A5"
RED = "#AE4D5B"
WHITE = "#FEF9EB"
GREY = "#C0C0C0"
CHESS_SIZE = 650
MARGIN = 25

DEFAULT_N = 8
DEFAULT_START_X = 4
DEFAULT_START_Y = 2
DEFAULT_END_X = 2
DEFAULT_END_Y = 6
DEFAULT_BISHOP_X = 2
DEFAULT_BISHOP_Y = 3


class KnightMoves:
    def __init__(
        self,
        start_x: int = DEFAULT_START_X,
        start_y: int = DEFAULT_START_Y,
        end_x: int = DEFAULT_END_X,
        end_y: int = DEFAULT_END_Y,
        bishop_x: int = DEFAULT_BISHOP_X,
        bishop_y: int = DEFAULT_BISHOP_Y,
        n: int = DEFAULT_N,
        sleep_time: float = 0.1,
        debug: bool = False,
        profile: bool = False,
    ):
        if debug:
            self.run_cli_debug(
                start_x,
                start_y,
                end_x,
                end_y,
                bishop_x,
                bishop_y,
                n,
                profile=profile,
            )
        else:
            self.window = tk.Tk()
            self.window.title("Knight Moves")
            self.n = tk.IntVar(value=n)
            self.start_x = tk.IntVar(value=start_x)
            self.start_y = tk.IntVar(value=start_y)
            self.end_x = tk.IntVar(value=end_x)
            self.end_y = tk.IntVar(value=end_y)
            self.bishop_x = tk.IntVar(value=bishop_x)
            self.bishop_y = tk.IntVar(value=bishop_y)
            self.sleep_time = tk.DoubleVar(value=sleep_time)
            self.tick_size = tk.IntVar(value=1)
            self.running = False

    def run_gui(self):
        """
        Run the GUI.
        """
        self._get_bishop_positions(
            self.bishop_x.get(), self.bishop_y.get(), self.n.get()
        )
        self._init_window()
        self.window.mainloop()

    def run_cli_debug(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        bishop_x: int,
        bishop_y: int,
        n: int,
        profile: bool = False,
    ):
        """
        Run the CLI with debug.
        """
        self._get_bishop_positions(bishop_x, bishop_y, n)
        self.running = True
        print(
            f"Shortest path length BFS: {self.bfs(start_x, start_y, end_x, end_y, n, bishop_x, bishop_y, debug=not profile)}"
        )
        print(
            f"Shortest path length DBFS: {self.dbfs(start_x, start_y, end_x, end_y, n, bishop_x, bishop_y, debug=not profile)}"
        )


    def bfs(
        self,
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
        tick_size = 1
        try:
            tick_size = self.tick_size.get()
        except AttributeError:
            pass
        row = [2, 2, -2, -2, 1, 1, -1, -1]
        col = [1, -1, 1, -1, 2, -2, 2, -2]
        visited = set()
        # tuples of the form (x, y, distance, is_bishop_alive)
        queue = deque()
        queue.append((start_x, start_y, 0, True))
        num_visited = 0
        while queue:
            if not self.running:
                return -1

            x, y, distance, is_bishop_alive = queue.popleft()

            # check if we found the end
            if (x, y) == (end_x, end_y):
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
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
            if counter is not None and num_visited % tick_size == 0:
                counter.set(f"Visited: {num_visited} nodes")
            if chess_frame is not None:
                chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                if num_visited % tick_size == 0:
                    chess_frame.update()
                    time.sleep(sleep_time)

            for dx, dy in zip(row, col):
                new_x, new_y = x + dx, y + dy
                if is_bishop_alive and (new_x, new_y) in self.bishop_positions:
                    continue
                if self._is_valid_position(new_x, new_y, n):
                    if (new_x, new_y) == (bishop_x, bishop_y):
                        queue.append((new_x, new_y, distance + 1, False))
                    else:
                        queue.append((new_x, new_y, distance + 1, is_bishop_alive))

        if debug:
            print(f"Not found after {num_visited} nodes")
        return -1

    def dbfs(
        self,
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
    ):
        """
        Run double ended BFS to find shortest path from start to end.
        """
        tick_size = 1
        try:
            tick_size = self.tick_size.get()
        except AttributeError:
            pass
        row = [2, 2, -2, -2, 1, 1, -1, -1]
        col = [1, -1, 1, -1, 2, -2, 2, -2]
        visited_start = dict()
        visited_end = dict()
        queue_start = deque()
        queue_end = deque()
        queue_start.append((start_x, start_y, 0, True))
        queue_end.append((end_x, end_y, 0, True))
        num_visited = 0
        while queue_start and queue_end:
            if not self.running:
                return -1

            x, y, distance, is_bishop_alive = queue_start.popleft()

            if (x, y) == (end_x, end_y):
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
                if debug:
                    print(f"Found after {num_visited} nodes")
                return distance

            if (x, y, True) in visited_end:
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
                if debug:
                    print(f"Found after {num_visited} nodes")
                return distance + visited_end[(x, y, True)]

            if (x, y, False) in visited_end:
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
                if debug:
                    print(f"Found after {num_visited} nodes")
                return distance + visited_end[(x, y, False)]

            if (x, y, is_bishop_alive) in visited_start:
                if debug:
                    print(f"Already visited {(x, y, is_bishop_alive)}")
                continue

            visited_start[(x, y, is_bishop_alive)] = distance
            num_visited += 1

            if debug:
                print(f"Visiting {(x, y, is_bishop_alive)}")
            if counter is not None:
                counter.set(f"Visited: {num_visited} nodes")
            if chess_frame is not None:
                chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                if num_visited % tick_size == 0:
                    chess_frame.update()
                    time.sleep(sleep_time)

            for dx, dy in zip(row, col):
                new_x, new_y = x + dx, y + dy
                if is_bishop_alive and (new_x, new_y) in self.bishop_positions:
                    continue
                if self._is_valid_position(new_x, new_y, n):
                    if (new_x, new_y) == (bishop_x, bishop_y):
                        queue_start.append((new_x, new_y, distance + 1, False))
                    else:
                        queue_start.append(
                            (new_x, new_y, distance + 1, is_bishop_alive)
                        )

            if not self.running:
                return -1

            x, y, distance, is_bishop_alive = queue_end.popleft()

            if (x, y) == (start_x, start_y):
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
                if debug:
                    print(f"Found after {num_visited} nodes")
                return distance

            if (x, y, True) in visited_start:
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
                if debug:
                    print(f"Found after {num_visited} nodes")
                return distance + visited_start[(x, y, True)]

            if (x, y, False) in visited_start:
                if chess_frame is not None:
                    chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                    # TODO: move knight here and show path ? potentially
                    chess_frame.update()
                if counter is not None:
                    counter.set(f"Visited: {num_visited} nodes")
                if debug:
                    print(f"Found after {num_visited} nodes")
                return distance + visited_start[(x, y, False)]

            if (x, y, is_bishop_alive) in visited_end:
                if debug:
                    print(f"Already visited {(x, y, is_bishop_alive)}")
                continue

            visited_end[(x, y, is_bishop_alive)] = distance
            num_visited += 1

            if debug:
                print(f"Visiting {(x, y, is_bishop_alive)}")
            if counter is not None:
                counter.set(f"Visited: {num_visited} nodes")
            if chess_frame is not None:
                chess_frame.itemconfig(self.chess_squares[x][y], fill=GREY)
                if num_visited % tick_size == 0:
                    chess_frame.update()
                    time.sleep(sleep_time)

            for dx, dy in zip(row, col):
                new_x, new_y = x + dx, y + dy
                if is_bishop_alive and (new_x, new_y) in self.bishop_positions:
                    continue
                if self._is_valid_position(new_x, new_y, n):
                    if (new_x, new_y) == (bishop_x, bishop_y):
                        queue_end.append((new_x, new_y, distance + 1, False))
                    else:
                        queue_end.append((new_x, new_y, distance + 1, is_bishop_alive))
        return -1


    def _is_valid_position(self, x: int, y: int, n: int) -> bool:
        """
        Check if position is valid.
        """
        return 0 <= x < n and 0 <= y < n

    def _get_bishop_positions(self, bishop_x: int, bishop_y: int, n: int) -> set[tuple[int, int]]:
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
                if self._is_valid_position(new_x, new_y, n):
                    bishop_positions.add((new_x, new_y))
        self.bishop_positions = bishop_positions
        return bishop_positions

    # TKINTER ANIMATIONS

    def _reset_chess_board(self) -> None:
        """
        Reset chess board to original state.
        """
        try:
            len(self.chess_squares)
        except AttributeError:
            self.chess_squares = []

        n = self.n.get()

        self._get_bishop_positions(self.bishop_x.get(), self.bishop_y.get(), n)

        for i in range(n):
            chess_row = None
            new_row = False
            if i < len(self.chess_squares):
                chess_row = self.chess_squares[i]
            else:
                new_row = True
                chess_row = []

            for j in range(n):
                square_id = chess_row[j] if j < len(chess_row) else None
                color = (
                    RED
                    if (i, j) in self.bishop_positions
                    else WHITE if (i + j) % 2 == 0 else GREEN
                )
                x1, y1, x2, y2 = (
                    j * CHESS_SIZE / n,
                    i * CHESS_SIZE / n,
                    (j + 1) * CHESS_SIZE / n,
                    (i + 1) * CHESS_SIZE / n,
                )
                if square_id is not None:
                    self.chess_frame.coords(square_id, x1, y1, x2, y2)
                    self.chess_frame.itemconfig(square_id, fill=color)
                    self.chess_frame.tag_raise(square_id)
                else:
                    square_id = self.chess_frame.create_rectangle(
                        x1,
                        y1,
                        x2,
                        y2,
                        fill=color,
                    )
                    chess_row.append(square_id)
            if new_row:
                self.chess_squares.append(chess_row)
        # images
        SQUARE_WIDTH = CHESS_SIZE / n

        unscaled_knight_img = tk.PhotoImage(file="images/knight.png")
        scale_factor = int(unscaled_knight_img.width() / SQUARE_WIDTH) + 1
        self.knight_img = unscaled_knight_img.subsample(scale_factor, scale_factor)

        unscaled_bishop_img = tk.PhotoImage(file="images/bishop.png")
        scale_factor = int(unscaled_bishop_img.width() / SQUARE_WIDTH) + 1
        self.bishop_img = unscaled_bishop_img.subsample(scale_factor, scale_factor)

        unscaled_king_img = tk.PhotoImage(file="images/king.png")
        scale_factor = int(unscaled_king_img.width() / SQUARE_WIDTH) + 1
        self.king_img = unscaled_king_img.subsample(scale_factor, scale_factor)

        try:
            self.chess_frame.itemconfig(self.knight_image_id, image=self.knight_img)
            self.chess_frame.itemconfig(self.king_image_id, image=self.king_img)
            self.chess_frame.itemconfig(self.bishop_img_id, image=self.bishop_img)
            self.chess_frame.coords(
                self.knight_image_id,
                self.start_y.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                self.start_x.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
            )
            self.chess_frame.coords(
                self.king_image_id,
                self.end_y.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                self.end_x.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
            )
            self.chess_frame.coords(
                self.bishop_img_id,
                self.bishop_y.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                self.bishop_x.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
            )
            self.chess_frame.tag_raise(self.knight_image_id)
            self.chess_frame.tag_raise(self.king_image_id)
            self.chess_frame.tag_raise(self.bishop_img_id)
        except AttributeError:
            self.knight_image_id = self.chess_frame.create_image(
                self.start_y.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                self.start_x.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                image=self.knight_img,
            )
            self.king_image_id = self.chess_frame.create_image(
                self.end_y.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                self.end_x.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                image=self.king_img,
            )
            self.bishop_img_id = self.chess_frame.create_image(
                self.bishop_y.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                self.bishop_x.get() * CHESS_SIZE / n + CHESS_SIZE / (2 * n),
                image=self.bishop_img,
            )
        self.chess_frame.update()

    def _reset_knight_position(self):
        """
        Reset knight position to original state.
        """
        IMAGE_WIDTH = self.knight_img.width()
        self.chess_frame.moveto(
            self.knight_image_id,
            (
                self.start_y.get() * CHESS_SIZE / self.n.get()
                + CHESS_SIZE / (2 * self.n.get())
            )
            - IMAGE_WIDTH / 2,
            (
                self.start_x.get() * CHESS_SIZE / self.n.get()
                + CHESS_SIZE / (2 * self.n.get())
            )
            - IMAGE_WIDTH / 2,
        )
        self.chess_frame.update()

    def _reset_bishop_position(self):
        """
        Reset bishop position to original state.
        """
        IMAGE_WIDTH = self.bishop_img.width()
        self.chess_frame.moveto(
            self.bishop_img_id,
            (
                self.bishop_y.get() * CHESS_SIZE / self.n.get()
                + CHESS_SIZE / (2 * self.n.get())
            )
            - IMAGE_WIDTH / 2,
            (
                self.bishop_x.get() * CHESS_SIZE / self.n.get()
                + CHESS_SIZE / (2 * self.n.get())
            )
            - IMAGE_WIDTH / 2,
        )
        self._reset_chess_board()
        self.chess_frame.update()

    def _reset_king_position(self):
        """
        Reset king position to original state.
        """
        IMAGE_WIDTH = self.king_img.width()
        self.chess_frame.moveto(
            self.king_image_id,
            (
                self.end_y.get() * CHESS_SIZE / self.n.get()
                + CHESS_SIZE / (2 * self.n.get())
            )
            - IMAGE_WIDTH / 2,
            (
                self.end_x.get() * CHESS_SIZE / self.n.get()
                + CHESS_SIZE / (2 * self.n.get())
            )
            - IMAGE_WIDTH / 2,
        )
        self.chess_frame.update()

    def _start(self):
        """
        Start the animation loop
        """
        self.run_buttons_frame.pack_forget()
        self.cancel_buttons_frame.pack(pady=20)
        self.running = True

    def _stop(self):
        """
        Stop the animation loop
        """
        self.running = False
        self.cancel_buttons_frame.pack_forget()
        self.run_buttons_frame.pack(pady=20)
        self._reset_chess_board()
        self.counter_text.set("Visited: 0 nodes")
        self.result_text.set("")

    def _start_bfs(self):
        """
        Start the BFS animation loop
        """
        self._start()
        shortest_path_length = self.bfs(
            self.start_x.get(),
            self.start_y.get(),
            self.end_x.get(),
            self.end_y.get(),
            self.n.get(),
            self.bishop_x.get(),
            self.bishop_y.get(),
            self.chess_frame,
            self.sleep_time.get(),
            self.counter_text,
        )
        if shortest_path_length == -1 and self.running:
            self.result_text.set("No valid path exists!")
        elif shortest_path_length == -1 and not self.running:
            self.result_text.set("")
        else:
            self.result_text.set(f"Shortest path length: {shortest_path_length}")

    def _start_dbfs(self):
        """
        Start the double ended BFS animation loop
        """
        self._start()
        shortest_path_length = self.dbfs(
            self.start_x.get(),
            self.start_y.get(),
            self.end_x.get(),
            self.end_y.get(),
            self.n.get(),
            self.bishop_x.get(),
            self.bishop_y.get(),
            self.chess_frame,
            self.sleep_time.get(),
            self.counter_text,
        )
        if shortest_path_length == -1 and self.running:
            self.result_text.set("No valid path exists!")
        elif shortest_path_length == -1 and not self.running:
            self.result_text.set("")
        else:
            self.result_text.set(f"Shortest path length: {shortest_path_length}")

    def _handle_n_change(self):
        """
        Handle n changing.
        """
        self.window.after_idle(self._reset_chess_board)

    def _init_window(self):
        """
        Initialize the window and render the chess board.
        """
        self.content = ttk.Frame(self.window)  # TODO: make responsive/ no hardcoding
        self.content.pack()
        self.n.trace_add("write", lambda *_: self._handle_n_change())
        self.start_x.trace_add("write", lambda *_: self._reset_knight_position())
        self.start_y.trace_add("write", lambda *_: self._reset_knight_position())
        self.end_x.trace_add("write", lambda *_: self._reset_king_position())
        self.end_y.trace_add("write", lambda *_: self._reset_king_position())
        self.bishop_x.trace_add("write", lambda *_: self._reset_bishop_position())
        self.bishop_y.trace_add("write", lambda *_: self._reset_bishop_position())
        self.chess_frame = tk.Canvas(self.content, width=CHESS_SIZE, height=CHESS_SIZE)
        self.chess_frame.grid(row=0, column=0, padx=MARGIN, pady=MARGIN)
        self._reset_chess_board()

        # render buttons and counter
        self.control_frame = ttk.Frame(self.content)
        self.control_frame.grid(row=0, column=1, padx=(0, MARGIN), pady=MARGIN)

        self.counter_text = tk.StringVar(self.control_frame, value="Visited: 0 nodes")
        self.counter = ttk.Label(
            self.control_frame, textvariable=self.counter_text, font=("Arial", 44)
        )
        self.counter.pack()

        self.result_text = tk.StringVar(self.control_frame, value="")
        self.result = ttk.Label(
            self.control_frame, textvariable=self.result_text, font=("Arial", 18)
        )
        self.result.pack(pady=(10, 0))

        self.run_controls_frame = ttk.Frame(self.control_frame)
        self.n_label = ttk.Label(self.run_controls_frame, text="Chess board size:")
        self.n_entry = ttk.Entry(self.run_controls_frame, textvariable=self.n, width=8)
        self.n_label.grid(row=0, column=0, padx=10)
        self.n_entry.grid(row=0, column=1, padx=10, columnspan=2)
        self.tick_speed_label = ttk.Label(
            self.run_controls_frame, text="Tick duration:"
        )
        self.tick_speed_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.sleep_time, width=8
        )
        self.tick_speed_label.grid(row=1, column=0, padx=10)
        self.tick_speed_entry.grid(row=1, column=1, padx=10, columnspan=2)
        self.tick_size_label = ttk.Label(self.run_controls_frame, text="Tick size:")
        self.tick_size_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.tick_size, width=8
        )
        self.tick_size_label.grid(row=2, column=0, padx=10)
        self.tick_size_entry.grid(row=2, column=1, padx=10, columnspan=2)
        self.start_pos_label = ttk.Label(
            self.run_controls_frame, text="Start position:"
        )
        self.start_x_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.start_x, width=3
        )
        self.start_y_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.start_y, width=3
        )
        self.start_pos_label.grid(row=3, column=0, padx=10)
        self.start_x_entry.grid(row=3, column=1, padx=(10, 0))
        self.start_y_entry.grid(row=3, column=2, padx=(0, 10))
        self.end_pos_label = ttk.Label(self.run_controls_frame, text="End position:")
        self.end_x_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.end_x, width=3
        )
        self.end_y_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.end_y, width=3
        )
        self.end_pos_label.grid(row=4, column=0, padx=10)
        self.end_x_entry.grid(row=4, column=1, padx=(10, 0))
        self.end_y_entry.grid(row=4, column=2, padx=(0, 10))
        self.bishop_pos_label = ttk.Label(
            self.run_controls_frame, text="Bishop position:"
        )
        self.bishop_x_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.bishop_x, width=3
        )
        self.bishop_y_entry = ttk.Entry(
            self.run_controls_frame, textvariable=self.bishop_y, width=3
        )
        self.bishop_pos_label.grid(row=5, column=0, padx=10)
        self.bishop_x_entry.grid(row=5, column=1, padx=(10, 0))
        self.bishop_y_entry.grid(row=5, column=2, padx=(0, 10))
        self.run_controls_frame.pack(pady=20)

        self.run_buttons_frame = ttk.Frame(self.control_frame)
        self.bfs_button = tk.Button(
            self.run_buttons_frame,
            text="Run BFS",
            command=lambda: self._start_bfs(),
        )
        self.bfs_button.grid(row=0, column=0, padx=10)
        self.dbfs_button = tk.Button(
            self.run_buttons_frame,
            text="Run Double BFS",
            command=self._start_dbfs,
        )
        self.dbfs_button.grid(row=0, column=1, padx=10)
        self.run_buttons_frame.pack(pady=20)

        self.cancel_buttons_frame = ttk.Frame(self.control_frame)
        self.cancel_button = tk.Button(
            self.cancel_buttons_frame,
            text="Reset",
            command=self._stop,
        )
        self.cancel_button.pack()


def _int_or_default(value: str, default: int) -> int:
    """
    Convert string to int or return default.
    """
    try:
        return int(value)
    except ValueError:
        return default


def _simple_bfs(start_x: int, start_y: int, end_x: int, end_y: int, n: int, bishop_alive: bool, bishop_positions: set[tuple[int, int]]) -> int:
    """
    Simple BFS to find shortest path from start to end while respecting bishop
    """
    row = [2, 2, -2, -2, 1, 1, -1, -1]
    col = [1, -1, 1, -1, 2, -2, 2, -2]
    visited = set()
    # tuples of the form (x, y, distance)
    queue = deque()
    queue.append((start_x, start_y, 0))
    num_visited = 0
    while queue:

        x, y, distance = queue.popleft()

        # check if we found the end
        if (x, y) == (end_x, end_y):
            return distance

        # check if we can skip this node
        if (x, y) in visited:
            continue

        visited.add((x, y))
        num_visited += 1

        for dx, dy in zip(row, col):
            new_x, new_y = x + dx, y + dy
            if bishop_alive and (new_x, new_y) in bishop_positions:
                continue
            if new_x >= 0 and new_x < n and new_y >= 0 and new_y < n:
                queue.append((new_x, new_y, distance + 1))
    return -1

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
            if new_x >= 0 and new_x < n and new_y >= 0 and new_y < n:
                bishop_positions.add((new_x, new_y))
    return bishop_positions

def _test_answer(start_x: int, start_y: int, end_x: int, end_y: int, n: int, bishop_x: int, bishop_y: int) -> int:
    """
    Certainly correct (but unoptimized) solution for testing.
    """
    bishop_positions = _get_bishop_positions(bishop_x, bishop_y, n)
    to_bishop = _simple_bfs(start_x, start_y, bishop_x, bishop_y, n, True, bishop_positions)
    to_goal = _simple_bfs(start_x, start_y, end_x, end_y, n, True, bishop_positions)
    if to_bishop == -1:
        return to_goal
    bishop_to_goal = _simple_bfs(bishop_x, bishop_y, end_x, end_y, n, False, bishop_positions)
    if to_goal == -1:
        if bishop_to_goal == -1:
            return -1
        return to_bishop + bishop_to_goal
    if bishop_to_goal == -1:
        return to_goal
    return min(to_bishop + bishop_to_goal, to_goal)




def _get_test_case():
    """
    get a single test case
    """
    n = r.randint(2, 100)
    start_x = r.randint(0, n - 1)
    start_y = r.randint(0, n - 1)
    end_x = r.randint(0, n - 1)
    end_y = r.randint(0, n - 1)
    bishop_x = r.randint(0, n - 1)
    bishop_y = r.randint(0, n - 1)
    return start_x, start_y, end_x, end_y, bishop_x, bishop_y, n



def validate_algorithm(num_test_cases: int = 1000):
    """
    use the test_answer function to validate the algorithm
    """
    failed_bfs_cases = list()
    failed_dbfs_cases = list()
    for _ in range(num_test_cases):
        start_x, start_y, end_x, end_y, bishop_x, bishop_y, n = _get_test_case()
        knight_moves = KnightMoves(start_x, start_y, end_x, end_y, bishop_x, bishop_y, n, 0, True, True)
        knight_moves._get_bishop_positions(bishop_x, bishop_y, n)
        knight_moves.running = True

        correct = _test_answer(start_x, start_y, end_x, end_y, n, bishop_x, bishop_y)
        bfs = knight_moves.bfs(start_x, start_y, end_x, end_y, n, bishop_x, bishop_y)
        dbfs = knight_moves.dbfs(start_x, start_y, end_x, end_y, n, bishop_x, bishop_y)
        if correct != bfs:
            # print(f"Test failed for BFS: {start_x, start_y, end_x, end_y, bishop_x, bishop_y, n}")
            # print(f"Correct: {correct}, BFS: {bfs}")
            failed_bfs_cases.append((start_x, start_y, end_x, end_y, bishop_x, bishop_y, n))
        if correct != dbfs:
            # print(f"Test failed for DBFS: {start_x, start_y, end_x, end_y, bishop_x, bishop_y, n}")
            # print(f"Correct: {correct}, DBFS: {dbfs}")
            failed_dbfs_cases.append((start_x, start_y, end_x, end_y, bishop_x, bishop_y, n))
    print(f"Failed BFS cases: {failed_bfs_cases}")
    print(f"Failed DBFS cases: {failed_dbfs_cases}")

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        KnightMoves().run_gui()

@cli.command(help="Run the algorithm CLI in debug mode.")
@click.option('--start_x', default=DEFAULT_START_X, help='Start x position.', prompt=True)
@click.option('--start_y', default=DEFAULT_START_Y, help='Start y position.', prompt=True)
@click.option('--end_x', default=DEFAULT_END_X, help='End x position.', prompt=True)
@click.option('--end_y', default=DEFAULT_END_Y, help='End y position.', prompt=True)
@click.option('--bishop_x', default=DEFAULT_BISHOP_X, help='Bishop x position.', prompt=True)
@click.option('--bishop_y', default=DEFAULT_BISHOP_Y, help='Bishop y position.', prompt=True)
@click.option('--n', default=DEFAULT_N, help='Chess board size.', prompt=True)
def debug(start_x, start_y, end_x, end_y, bishop_x, bishop_y, n):
    KnightMoves(start_x, start_y, end_x, end_y, bishop_x, bishop_y, n, sleep_time=0, debug=True)

@cli.command(help="Validate the algorithm against the simple approach.")
@click.option('--num_test_cases', default=1000, help='Number of test cases.')
def validate(num_test_cases):
    validate_algorithm(num_test_cases)

@cli.command(help="Run the program with profiling.")
@click.option('--profile_type', type=click.Choice(['cli', 'gui']), required=True, help='Profile type.')
@click.option('--start_x', default=DEFAULT_START_X, help='Start x position.', prompt=True)
@click.option('--start_y', default=DEFAULT_START_Y, help='Start y position.', prompt=True)
@click.option('--end_x', default=DEFAULT_END_X, help='End x position.', prompt=True)
@click.option('--end_y', default=DEFAULT_END_Y, help='End y position.', prompt=True)
@click.option('--bishop_x', default=DEFAULT_BISHOP_X, help='Bishop x position.', prompt=True)
@click.option('--bishop_y', default=DEFAULT_BISHOP_Y, help='Bishop y position.', prompt=True)
@click.option('--n', default=DEFAULT_N, help='Chess board size.', prompt=True)
def profile(profile_type, start_x, start_y, end_x, end_y, bishop_x, bishop_y, n):
    if profile_type == 'cli':
        cProfile.run(
            "KnightMoves("
            + f"{start_x}, "
            + f"{start_y}, "
            + f"{end_x}, "
            + f"{end_y}, "
            + f"{bishop_x}, "
            + f"{bishop_y}, "
            + f"{n}, "
            + "debug=True, profile=True"
            + ")",
        )
    elif profile_type == 'gui':
        cProfile.run(
            "KnightMoves("
            + f"{start_x}, "
            + f"{start_y}, "
            + f"{end_x}, "
            + f"{end_y}, "
            + f"{bishop_x}, "
            + f"{bishop_y}, "
            + f"{n}, "
            + "sleep_time=0, "
            + ").run_gui()",
        )


@cli.command(help="Run the program GUI.")
def gui():
    KnightMoves().run_gui()

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
