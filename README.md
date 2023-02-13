# **Conway.py**
##### *A Python simulation of Conway's Game of Life*
> **Notice:** This repository is a work-in-progress. Several features are still missing and opimizations have yet to be done. Any pre-releases published are *not* representative of the final project.

<br>

## Basics of Conway's Game of Life
Conway's Game of Life is a cell-based simulation of "life" which consists of 4 basic rules:
- Any living cell with 2 or 3 living neighbors stays alive.
- A living cell without exactly 2 or 3 neighbors dies the next generation.
- Any dead cell with exactly 3 living neighbors is revived.
##### **More information about Conway's Game of Life can be found on [Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)*

<br>

## Controls
| **Input** | **Action** |
| --------- | ---------- |
| `Left-click` | Toggle cell *(kill/create)* |
| `Right-click` | Drag to move viewport |
| `Scrollwheel` | Zoom in/out |
| `Spacebar` | Skip to next generation |
| `R` | Reset simulation |

<br>

## TODO
Features:
- [X] Accurate simulation rules.
- [X] X/Y Axis.
- [X] Movable viewport.
- [X] Add "ghost" effect option for prior generations.
- [ ] Add UI buttons below simulation canvas for pause/play.
- [ ] Add UI buttons for speed control.
- [ ] Customizable color themes.
- [X] Screen-space rendering
- [ ] "Old" screen effects + viewport warp?

Bugs:
- [X] Zoom scales viewport relative to world, not relative to viewport.
- [ ] Optimize `active_cells` set management
- [ ] Optimize rendering function for better performance
