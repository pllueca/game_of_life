import numpy as np
from typing import List, Tuple

# from a cell to an adjacent one
MOVES = [
    (0, 1),
    (0, -1),
    (1, 0),
    (1, 1),
    (1, -1),
    (-1, 0),
    (-1, 1),
    (-1, -1),
]


class GameOfLifeException(Exception):
  pass


class GameOfLife:
  """
  Logic of game of live. Represents a matrix of cells with two possible states, active and inactive.
  Each step cell change their state depending on the state of they neighbohoring cells.
  """

  def __init__(self, num_rows: int, num_cols: int, initial_active: List[Tuple[int, int]] = None):
    initial_active = initial_active or []
    self.num_cols = num_cols
    self.num_rows = num_rows
    self.mat = np.zeros((num_cols, num_rows), np.uint8)
    self.steps = 0

    for p in initial_active:
      if len(p) != 2:
        raise GameOfLifeException('Received bad initial positon: {}'.format(p))
      i, j = p
      self.mat[i, j] = 1

  def step(self) -> List[Tuple[int, int]]:
    """ Updates the cell matrix
    Rules:
      For a space that is 'populated':
        Each cell with one or no neighbors dies, as if by solitude.
        Each cell with four or more neighbors dies, as if by overpopulation.
        Each cell with two or three neighbors survives.
      For a space that is 'empty' or 'unpopulated'
        Each cell with three neighbors becomes populated.

    Returns list of positions that switched this step
    """
    changed = []
    new_mat = np.zeros_like(self.mat)
    for i in range(self.num_cols):
      for j in range(self.num_rows):
        neighbors = self.active_neighbors((i, j))
        if self.mat[i, j]:
          if len(neighbors) in [2, 3]:
            new_mat[i, j] = 1
          else:
            new_mat[i, j] = 0
            changed.append((i, j))
        else:
          if len(neighbors) == 3:
            new_mat[i, j] = 1
            changed.append((i, j))
          else:
            new_mat[i, j] = 0
    self.mat = new_mat
    self.steps += 1
    return changed

  def active_neighbors(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
    """ Return the list of positions adjacent to `position` where the cells are active """
    neighbors = []
    i, j = position
    for (mi, mj) in MOVES:
      current_position_i = i + mi
      current_position_j = j + mj
      if 0 <= current_position_i < self.num_cols and \
          0 <= current_position_j < self.num_rows and \
          self.mat[current_position_i, current_position_j] == 1:
        neighbors.append((current_position_i, current_position_j))
    return neighbors

  def activate(self, position: Tuple[int, int]) -> None:
    self.mat[position] = 1

  def deactivate(self, position: Tuple[int, int]) -> None:
    self.mat[position] = 0

  def toggle(self, position: Tuple[int, int]) -> None:
    self.mat[position] = 1 - self.mat[position]
