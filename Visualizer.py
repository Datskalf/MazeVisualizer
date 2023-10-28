from enum import Enum
from PIL import Image, ImageDraw
from tkinter import filedialog

class TileType(Enum):
    UNKNOWN = "0"
    WALL = "X"
    EMPTY = "-"
    START = "S"
    END = "E"

class Tile:
    def __init__(self, type: TileType) -> None:
        self.type = type
    
    def __str__(self) -> str:
        return self.type.value
    

    @staticmethod
    def getTileType(tileChar: str) -> TileType:
        if tileChar in ["X", "-", "S", "E"]:
            return TileType(tileChar)
        return TileType.UNKNOWN
        

class Maze:
    mazeTiles = []
    tileSizePx = 20

    def __init__(self) -> None:
        pass
        
    def readMazeFromFile(self, filePath: str) -> None:
        data = ""
        with open(filePath, "r") as file:
            data = file.read()
        
        self.readMazeFromString(data)

    def readMazeFromString(self, maze: str) -> None:
        self.mazeTiles = []
        splStr = maze.split("\n")
        for row in splStr:
            self.mazeTiles.append([])
            for c in row:
                self.mazeTiles[-1].append(Tile(Tile.getTileType(c)))

        self.mazeWidth = len(self.mazeTiles[0])
        self.mazeHeight = len(self.mazeTiles)


    def drawMaze(self) -> None:
        size = (self.mazeWidth * self.tileSizePx, self.mazeHeight * self.tileSizePx)
        im = Image.new("RGB", size)

        imgDraw = ImageDraw.Draw(im)
        for y, row in enumerate(self.mazeTiles):
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
        for row in self.mazeTiles:
            for tile in row:
                print(str(tile), end="")
            print("\n")

if __name__ == "__main__":
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

    wishToSave = input("Do you want to save this image [y/n]: ").lower() == "y"
    if wishToSave:
        name = fileName.split("/")[-1]
        maze.saveImage(name)
