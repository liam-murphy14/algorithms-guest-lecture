# My Algs guest lecture

Finally threw all the parts of my lecture into a repo. Here is a quick overview

## Parts

The Outline consists of `outline.pdf` and `outline.tex` which are the LaTeX input and output of the super duper rough draft outline. Presentation, consisting of `presentation.pdf` and `presentation.tex` are similar, but more polished. The really cool part is the `animations.py` demo.

## Running the demo

The demo is written in Python, using Tkinter for the GUI, and vanilla Python for the CLI.

### Installation

First, be sure that you have a working Python3 installation. Once you have that, be sure to install the Tkinter module through your _system package manager_ if you used a package manager to install Python3 (if you installed the Python.org distribution, then you can skip this step). For me, on macOS, this looks like

```shell
brew install python-tk@3.11
```

consult [this nice tutorial](https://tkdocs.com/tutorial/install.html) for more info on this.

### Usage

```shell
python3 animations.py [OPTION]
```

Running without any options will start the GUI.

#### Options

```shell
debug [start_x] [start_y] [end_x] [end_y] [bishop_x] [bishop_y] [n]
```

Run the CLI with debug. If no arguments are provided, the user will be prompted for them.

```shell
profile [type] [start_x] [start_y] [end_x] [end_y] [bishop_x] [bishop_y] [n]
```

Run the program with profiling. If no arguments are provided, the user will be prompted for them.

```shell
help
```

Show this help message.

##### Profile Types

```shell
cli
```

Profile the cli version (this is akin to profiling the acutual algorithms, with some overhead).

```shell
gui
```

Profile the gui. This is more complex.
