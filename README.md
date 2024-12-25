# My Algs guest lecture

Finally threw all the parts of my lecture into a repo. Here is a quick overview

## Parts

There are 3 main items in this repo. First, the Nix flake, `flake.nix`, provides the necessary environment and setup to both build the LaTeX presentation and Python demo. My lecture presentation, `presentation.tex`, is what I share on screen while giving the lecture. You can build it (after installing Nix) with `nix build .#documents`, otherwise you can install the TexLive environment and build it with `pdflatex`. The really cool part is the `animations` Python package containing the demo (details on how to run it below).

## Running the demo

The demo is written in Python, using [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI, and [Click](https://click.palletsprojects.com/en/stable/) for the CLI.

### Installing dependencies

If you have installed a Python.org distribution, rather than installing Python through a package manager, you can skip this section.

#### Option 1: Using Nix

If you have Nix installed with support for flakes, then you don't need to worry about installing any dependencies. Simply `cd` into this directory and run `nix develop` to enter a shell with Python and Tkinter installed.

#### Option 2: Using Python installed through a package manager

First, be sure that you have a working Python3 installation. Once you have that, be sure to install the Tkinter module through the _system package manager_ that you used to install Python3. On macOS using Homebrew, this looks like

```shell
brew install python-tk@3.11
```

consult [this nice tutorial](https://tkdocs.com/tutorial/install.html) for more info on this.

### Usage

From the root of the repository, run the following command:

```shell
python3 animations/animations.py [OPTION]
```

Running without any options will start the GUI.

Alternatively, if you have Nix installed with support for flakes, you can `nix run` directly instead of invoking Python.

#### Options

```shell
gui [start_x] [start_y] [end_x] [end_y] [bishop_x] [bishop_y] [n]
```

Run the GUI with optional starting parameters. If no arguments are provided, the user will be prompted for them.

```shell
cli [start_x] [start_y] [end_x] [end_y] [bishop_x] [bishop_y] [n]
```

Run the CLI with starting parameters. If no arguments are provided, the user will be prompted for them.

```shell
profile [start_x] [start_y] [end_x] [end_y] [bishop_x] [bishop_y] [n]
```

Run the program with profiling. If no arguments are provided, the user will be prompted for them.


## A word to the wise

Tkinter can be extremely slow. There are particular issues with the `Canvas` object, which we use to create the chess diagram: `Tkinter.Canvas` does not reuse item ids when deleting canvas items and drawing new ones, so when you delete and redraw items over and over, the performance of the GUI tanks. This took be a long time to figure out and I have only seen it [here](https://stackoverflow.com/questions/64956625/tkinter-canvas-slow), so I will rewrite it here so that hopefully it helps someone else.

## Resources

* [LeetCode](https://leetcode.com/) is a great place to go for practice problems
* [Cracking the Coding Interview](https://www.crackingthecodinginterview.com/) is a book all about different strategies for coding interviews, and helps categorize the types of problems you might face
* [Grokking the Coding Interview](https://www.designgurus.io/course/grokking-the-coding-interview) is sort of a mix of Leetcode and Cracking the Coding Interview: it categorizes the problems by common themes, but is interactive and allows you to code up and submit your solutions to the problems as well
* [Here is a nice resource on Double-ended BFS](https://efficientcodeblog.wordpress.com/2017/12/13/bidirectional-search-two-end-bfs/)

