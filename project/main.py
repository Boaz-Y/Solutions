import tkinter as tk
from gui import CodonAnalyzerGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = CodonAnalyzerGUI(root)
    root.mainloop()