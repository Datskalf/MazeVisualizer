from enum import Enum
from PIL import Image, ImageDraw
from tkinter import filedialog
import sys

class TileType(Enum):
    """
    An enumerator to make tile types easier to read.
    """
    
    UNKNOWN = "0"
    WALL = "X"
    EMPTY = "-"
    START = "S"
    END = "E"

class Tile:
    """
    The tile contains the character data, as well as a static method to convert a character to TileType.
    """
    def __init__(self, type: TileType) -> None:
        self.type = type
    
    def __str__(self) -> str:
        return self.type.value
    
    @staticmethod
    def getTileType(tileChar: str) -> TileType:
        """
        Converts the character provided to a TileType
        """
        tileChar = "-" if tileChar == " " else tileChar
        if tileChar in ["X", "-", "S", "E"]:
            return TileType(tileChar)
        return TileType.UNKNOWN
        

class Maze:
    """
    The maze will read in the maze data from a file or string.
    It will then colour an n by n area of an image with the colour corresponding tile colour.
    Finally, ask the user where they want to save the image. 
    """
    mazeTiles = []
    tileSizePx = 8

    def __init__(self) -> None:
        pass
        
    def readMazeFromFile(self, filePath: str) -> None:
        """
        Read in the maze data from the file.
        """
        data = ""
        print(f"Opening file {filePath}")
        with open(filePath, "r") as file:
            data = file.read()
        
        self.readMazeFromString(data)

    def readMazeFromString(self, maze: str) -> None:
        """
        Create and populate a 2D array of tiles from the inputted string.
        """
        self.mazeTiles = []
        splStr = maze.split("\n")
        for i, row in enumerate(splStr):
            print(f"Reading line {i}")
            self.mazeTiles.append([])
            for c in row:
                self.mazeTiles[-1].append(Tile(Tile.getTileType(c)))

        self.mazeWidth = len(self.mazeTiles[0])
        self.mazeHeight = len(self.mazeTiles)


    def drawMaze(self) -> None:
        """
        For each tile, colour an n by n area of the image by the corresponding colour.
        """
        size = (self.mazeWidth * self.tileSizePx, self.mazeHeight * self.tileSizePx)
        im = Image.new("RGB", size)

        imgDraw = ImageDraw.Draw(im)
        for y, row in enumerate(self.mazeTiles):
            print(f"Writing row {y+1} out of {len(self.mazeTiles)}")
            for x, tile in enumerate(row):
                area = [(x*self.tileSizePx, y*self.tileSizePx), ((x+1)*self.tileSizePx - 1, (y+1)*self.tileSizePx - 1)]
                fill = "#f00"
                if tile.type == TileType.WALL:
                    fill = "#000"
                elif tile.type == TileType.EMPTY:
                    fill = "#fff"
                elif tile.type == TileType.START:
                    fill = "#0f0"
                elif tile.type == TileType.END:
                    fill = "#00f"

                imgDraw.rectangle(area, fill)
        
        im.show()

        self.im = im


        pass

    def saveImage(self, defaultName: str) -> None:
        """
        Prompt the user to save the image somewhere on disk.
        """
        f = filedialog.asksaveasfile(
            initialfile=defaultName,
            mode="wb",
            confirmoverwrite=True,
            filetypes=(
                ("Portable Network Graphics (*.png)", "*.png"),
                ("All Files (*.*)", "*.*")
            ),
            defaultextension=".png"
        )
        if not f:
            return
        filename = f.name
        extension = filename.split(".")[-1]
        self.im.save(filename, extension)
        f.close()


    def outputMazeToConsole(self) -> None:
        """
        Output the maze to console.
        """
        for row in self.mazeTiles:
            for tile in row:
                print(str(tile), end="")
            print("\n")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        fileName = sys.argv[1]
    else:
        print("Select the maze file from the dialog box")
        fileName = filedialog.askopenfilename(
            filetypes = (
                ("Text files (*.txt)", "*.txt"),
                ("All files (*.*)", "*.*")
            ),
            defaultextension=".txt"
        )

    maze = Maze()
    maze.readMazeFromFile(fileName)
    maze.drawMaze()

    if len(sys.argv) >= 3:
        if sys.argv[2] == "--nosave":
            exit(0)

    wishToSave = input("Do you want to save this image [y/n]: ").lower() == "y"
    if wishToSave:
        name = fileName.split("/")[-1]
        maze.saveImage(name)
