# Lecture Notes

## Introduction (4 minutes)

* Introduce myself (1 min)
* Introduce the topic by talking about my experience with the class and my doubts about the practical application of abstract algorithms (1 min)
* Introduce the idea of a technical interview, and what we will be discussing in the lecture (i.e. going over a problem and how to solve it with abstract algorithms) (2 mins)

## Problem Description (3 minutes)

* Introduce the problem that we will be studying: the Knight's Path, that is similar to a problem I saw in an actual interview, which I failed (2 mins)

* Pause for questions (1 min)

## Solution (10 minutes)

* Explain how certain clues from the problem description help guide us to a graph-based solution, specifically keying in on start and end position, and the desire to find a shortest path (3 mins)

* Explain the initial solution, least optimized, which finds the path to the end, the path to the bishop, then the path from the bishop to the end position. Highlight how this simplifies the implementation, and is a good starting point (3 mins)

* Explain the small optimization that we can make, which is to find the path to the bishop and the path to the end position at the same time, and how this is a good optimization because it reduces the number of times we have to visit the same nodes (2 mins)

* Analyze the time complexity of the solution (2 mins)

## Demo (3 minutes)

* Show the demo of the solution example case (1 min)

```bash
nix run
```

* Show the demo of the solution larger case, turning tick size up to 10 or something like that (1 min)

```bash
nix run . -- gui --start-x 17 --start-y 18 --end-x 2 --end-y 1 --bishop-x 10 --bishop-y 12 --n 20
```

## Optimization (5 mins)

* Introduce the idea of a double-ended BFS, and how it can be used to optimize the solution (2 mins)

* Show demo of solution larger case with double-ended BFS (1 min)

## Conclusion (5 mins)

* Recap the problem, and how the hardest part is to translate the problem into an algorithms problem, and how this algorithms class has helped build that skill set, and that continuing that practice can make the job search much easier (1 min)

* Questions (4 mins)
