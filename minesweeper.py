import itertools
import random

# REFERENCE: Python itertools:
# https://medium.com/@jasonrigden/a-guide-to-python-itertools-82e5a306cdf8
# https://realpython.com/python-itertools/
# https://pymotw.com/2/itertools/
# https://towardsdatascience.com/wicked-fast-python-with-itertools-55c77443f84c
# https://stackoverflow.com/questions/22473053/itertools-equivalent-of-nested-loop-for-x-in-xs-for-y-in-ys
# https://docs.python.org/3/library/itertools.html#itertools.product


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells if self.count == len(self.cells) else set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1
        self.moves_made.add(cell)

        # Step 2
        self.mark_safe(cell)

        # Step 3
        new_sentence = Sentence(self.neighbours(cell), count)

        for mine in self.mines:
            new_sentence.mark_mine(mine)
        for safe in self.safes:
            new_sentence.mark_safe(safe)

        # Add to KB
        self.knowledge.append(new_sentence)

        # Step 4
        mines = set()
        safes = set()

        for sentence in self.knowledge:
            for cell in sentence.known_mines():
                mines.add(cell)
            for cell in sentence.known_safes():
                safes.add(cell)

        for cell in mines:
            self.mark_mine(cell)
        for cell in safes:
            self.mark_safe(cell)

        # Step 5
        additional_sentences = []

        for sentence in self.knowledge:
            if new_sentence == sentence:
                break
            elif new_sentence.cells <= sentence.cells:
                cells = sentence.cells - new_sentence.cells
                count = sentence.count - new_sentence.count
                additional_sentences.append(Sentence(cells, count))
            new_sentence = sentence

        self.knowledge.extend(additional_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Get safe moves that have not occured
        safe_moves = self.safes.difference(self.moves_made)

        # If the set is not empty then return the first safe move
        if safe_moves:
            return safe_moves.pop()

        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Set with all possible random moves
        # for i in range(self.height)
        # for j in range(self.width)
        # cell = (i, j)
        # moves.add(cell)
        moves_remaining = set(
            itertools.product(range(0, self.height), range(0, self.width))
        )

        # Moves already selected and are mines
        moves_remaining = moves_remaining - self.mines - self.moves_made

        # Return random move
        return random.choice(tuple(moves_remaining)) \
            if moves_remaining else None

    def neighbours(self, cell):
        """
        Returns a set of all the neighbours of a given cell.
        """
        neighbours_cells = set()

        # Loop over surrounding cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Skip iteration,
                # Ignore the given cell itself, only focus on neighbours.
                if (i, j) == cell:
                    continue

                # Add cells to neghbours
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbours_cells.add((i, j))

        return neighbours_cells
