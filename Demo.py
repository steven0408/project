from tkinter import *
import player
from Gobang import *
import tkinter.messagebox as messagebox
import random

class Gobang:
    def SetWindow(self):
        self.window = Tk()   # 定義視窗
        self.window.title("五子棋 - Gobang") # 標題
        self.window.geometry('500x600')  # 視窗大小
        
        self.frame1 = Frame(self.window)
        self.canvas = Canvas(self.frame1, height=360, width=360, bg='#cd853f')
        self.canvas.pack(padx=40, pady=40)

        self.frame2 = Frame(self.window)
        self.text1 = StringVar()
        self.text1.set('下棋順序')
        self.text2 = StringVar()
        self.text2.set(" ")
        self.label1 = Label(self.frame2, textvariable=self.text1)
        self.label2 = Label(self.frame2, textvariable=self.text2, bg='#DCDCDC')
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=0, column=1)
        botton1 = Button(self.frame2, text='重新開始 (Restart)', command=lambda: self.Run())
        botton1.grid(row=1, column=0)
        botton2 = Button(self.frame2, text='退出 (Exit)', command=lambda: self.ClossWindow(text=''))
        botton2.grid(row=1, column=1)
        self.frame2.grid(row=1)
    
    def ClearCanvas(self):
        self.canvas.delete('all')
        for i in range(8):
            self.canvas.create_line((i+1) * 40, 40, (i+1) * 40, 8 * 40, fill='black')
            self.canvas.create_line(40, (i+1) * 40, 8 * 40, (i+1) * 40, fill='black') 
        self.frame1.grid(row=0)

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
        self.window.update()

    def Run(self):
        self.ClearCanvas()
        self.ResumeGame = False
        self.Board = BuildBoard(8)
        self.player1 = player.player()
        self.action = []
        self.count = 0  # 控制閥
        self.CurrentPlayer = random.choice(["Player1", "Player2"])
        self.chessman = 1   # 先手黑棋
        self.Notice(False)
        if self.CurrentPlayer == "Player2":
            self.text1.set('先手 - 黑棋')
        else :
            self.text1.set('後手 - 白棋')
            self.AiProcess()
        self.canvas.bind("<Button-1>", lambda event : self.BindProcess(event))
        mainloop()
    
    def AiProcess(self):
        self.action = self.player1.move(self.Board, self.action, self.chessman)
        if self.action in GetValid(self.Board):
            row, col = self.action
            self.Board[row, col] = self.chessman
            self.ActionToDraw(self.action, self.chessman)
            if IsContinuous(self.Board, self.action):
                self.Notice(True)
                self.ClossWindow('You Lose ~ இдஇ')
            else:
                self.CurrentPlayer = "Player2"
                self.chessman = -self.chessman
                self.Notice(False)
        else:
            print("Error")
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy())
    
    def TieProcess(self):
        if GetValid(self.Board) == []:
            self.text2.set('Tie ~  (●__●)')
            self.label2['bg'] = 'white'
            self.window.update()
            self.ClossWindow('Tie ~  (●__●)')
    
    def BindProcess(self, event):
        self.count += 1
        if self.count == 1:
            self.TieProcess()
            self.action = self.EventToAction(event)
            if self.action in GetValid(self.Board):
                row, col = self.action
                self.Board[row, col] = self.chessman
                self.ActionToDraw(self.action, self.chessman)
                if IsContinuous(self.Board, self.action):
                    self.Notice(True)
                    self.ClossWindow('You Win ~ ٩(✿∂‿∂✿)۶')
                else:
                    self.CurrentPlayer = "Player1"
                    self.chessman = -self.chessman
                    self.Notice(False)
                    self.TieProcess()
                    self.AiProcess()
                    self.count = 0
    
    def Notice(self, End):
        if End:
            if self.CurrentPlayer == 'Player1':
                self.text2.set('You Lose ~ இдஇ')
                self.label2['bg'] = 'black'
                self.label2['fg'] = 'white'
            else:   # self.CurrentPlayer == 'Player2'
                self.text2.set('You Win ~ ٩(✿∂‿∂✿)۶')
                self.label2['bg'] = 'gold'
        else :
            if self.CurrentPlayer == 'Player1':
                self.text2.set('Waiting ... ')
                self.label2['bg'] = 'red'
            else :
                self.text2.set('It is your turn ~ ')
                self.label2['bg'] = 'green'
            self.window.update()

    def ClossWindow(self, text):
        if messagebox.askokcancel("Notice", text + "\nAre you sure to close the window ?"):
            self.window.destroy()
            mainloop()
        
Game = Gobang()
Game.SetWindow()
Game.Run()
