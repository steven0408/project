from tkinter import *
import player
from Gobang import *
import tkinter.messagebox as messagebox
import random

class Gobang:
    def __init__(self):
        self.player1 = player.player()

    def SetWindow(self):
        self.window = Tk()   # 定義視窗
        self.window.title("五子棋 - Gobang") # 標題
        self.window.geometry('500x500')  # 視窗大小
        
        frame1 = Frame(self.window)
        self.canvas = Canvas(frame1, height=360, width=360, bg='#cd853f')
        self.canvas.pack(padx=40, pady=40)
        for i in range(8):
            self.canvas.create_line((i+1) * 40, 40, (i+1) * 40, 8 * 40, fill='black')
            self.canvas.create_line(40, (i+1) * 40, 8 * 40, (i+1) * 40, fill='black')
        frame1.grid(row=0)

        frame2 = Frame(self.window)
        self.text1 = StringVar()
        self.text1.set('下棋順序')
        self.text2 = StringVar()
        self.text2.set(" ")
        self.label1 = Label(frame2, textvariable=self.text1)
        self.label2 = Label(frame2, textvariable=self.text2)
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=0, column=1)
        botton = Button(frame2, text='重新開始 (Restart)', command=self.Run)
        botton.grid(row=1, column=0)
        botton = Button(frame2, text='退出 (Exit)', command=self.ClossWindow)
        botton.grid(row=1, column=1)
        frame2.grid(row=1)
    

    def EventToAction(self, event):
        x = min(int((event.x - 20)/40), 7)
        y = min(int((event.y - 20)/40), 7)
        return [x, y]

    def ActionToDraw(self, action, chessman):
        x0, y0 = action
        if chessman == 1:
            self.canvas.create_oval(x0 * 40 + 25, y0 * 40 + 25, (x0+1) * 40 + 15,  (y0+1) * 40 + 15, fill='black', outline='black')  # 圓形
        else :
            self.canvas.create_oval(x0 * 40 + 25, y0 * 40 + 25, (x0+1) * 40 + 15,  (y0+1) * 40 + 15, fill='white', outline='white')
        
    def Run(self):
        self.SetWindow()
        self.ResumeGame = False
        self.Board = BuildBoard(8)
        self.action = []
        self.CurrentPlayer = random.choice(["Player1", "Player2"])
        self.chessman = 1   # 先手黑棋
        if self.CurrentPlayer == "Player2":
            self.text1.set('先手 - 黑棋')
        else :
            self.text1.set('後手 - 白棋')
        self.Game()

    def Game(self):
        while GetValid(self.Board) != []:
            if self.CurrentPlayer == "Player1":
                self.action = self.player1.move(self.Board, self.action, self.chessman)
                if self.action in GetValid(self.Board):
                    row, col = self.action
                    self.Board[row, col] = self.chessman
                    self.ActionToDraw(self.action, self.chessman)
                    if IsContinuous(self.Board, self.action):
                        text = 'You Lose ~ இдஇ'
                        self.text2.set(text)
                        self.ClossWindow(text)
                        mainloop()
                    else:
                        self.CurrentPlayer = "Player2"
                        self.chessman = -self.chessman
                else:
                    print("Error")
                    self.window.protocol("WM_DELETE_WINDOW", self.window.destroy())
                    break
            else:
                self.canvas.bind("<Button-1>", lambda event : self.BindProcess(event))
                mainloop()
    
    def BindProcess(self, event):
        self.action = self.EventToAction(event)
        if self.action in GetValid(self.Board):
            row, col = self.action
            self.Board[row, col] = self.chessman
            self.ActionToDraw(self.action, self.chessman)
            if IsContinuous(self.Board, self.action):
                text = 'You Win ~ ٩(✿∂‿∂✿)۶'
                self.text2.set(text)
                self.ClossWindow(text)
                mainloop()
            else:
                self.CurrentPlayer = "Player1"
                self.chessman = -self.chessman
                self.Game()

    def ClossWindow(self, text):
        if messagebox.askokcancel("Notice", text + "\nAre you sure to close the window"):
            self.window.destroy()

Game = Gobang()
Game.Run()