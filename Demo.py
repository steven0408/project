from tkinter import *
import player
from Gobang import *
import tkinter.messagebox as messagebox
import random

class Gobang:
    def SetWindow(self):
        self.window = Tk()   # 定義視窗
        self.window.title("五子棋 - Gobang") # 標題
        self.window.geometry('1500x800')  # 視窗大小
        
        self.frame1 = Frame(self.window)
        self.canvas = Canvas(self.frame1, height=700, width=700, bg='#cd853f')
        self.canvas.pack(padx=40, pady=40)

        self.frame2 = Frame(self.window)
        self.text1 = StringVar()
        self.text1.set('下棋順序')
        self.text2 = StringVar()
        self.text2.set(" ")
        self.label1 = Label(self.frame2, textvariable=self.text1)
        self.label2 = Label(self.frame2, textvariable=self.text2, bg='#DCDCDC')
        self.label1.grid(row=0, column=0, ipadx=20, ipady=20)
        self.label2.grid(row=0, column=1)
        botton1 = Button(self.frame2, text='重新開始 (Restart)', command=lambda: self.Run())
        botton1.grid(row=1, column=0)
        botton2 = Button(self.frame2, text='退出 (Exit)', command=lambda: self.ClossWindow(text=''))
        botton2.grid(row=1, column=1)
        botton3 = Button(self.frame2, text='悔棋 (Regret)', command=lambda: self.RegretProcess())
        botton3.grid(row=1, column=2)
        botton4 = Button(self.frame2, text='提示(Tips)', command=lambda: self.TipProcess())
        botton4.grid(row=2, column=0)
        self.frame2.place(x=1000, y=400)
    
    def ClearCanvas(self):
        self.canvas.delete('all')
        for i in range(19):
            self.canvas.create_line((i+1) * 35, 35, (i+1) * 35, 19 * 35, fill='black')
            self.canvas.create_line(35, (i+1) * 35, 19 * 35, (i+1) * 35, fill='black') 
        self.frame1.grid(column=0)

    def EventToAction(self, event):
        x = min(int((event.x - 17)/35), 18)
        y = min(int((event.y - 17)/35), 18)
        return [x, y]

    def ActionToDraw(self, action, chessman):
        x0, y0 = action
        if chessman == 1:
            self.black_chess = self.canvas.create_oval(x0 * 35 + 18, y0 * 35 + 18, (x0+1) * 35 + 17,  (y0+1) * 35 + 17, fill='black', outline='black')  # 圓形
        else :
            self.white_chess = self.canvas.create_oval(x0 * 35 + 18, y0 * 35 + 18, (x0+1) * 35 + 17,  (y0+1) * 35 + 17, fill='white', outline='white')
        self.window.update()

    def Run(self):
        self.ClearCanvas()
        self.button4 = False
        self.droplist = []
        self.ResumeGame = False
        self.Board = BuildBoard(19)
        self.player1 = player.player()
        self.action = []
        self.suggest = 0
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
        if len(self.droplist) == 0:
            self.action = self.player1.move(self.Board, self.action, self.chessman)
        else:
            self.action, _ = self.player1.move(self.Board, self.action, self.chessman)
        
        if self.action in GetValid(self.Board):
            row, col = self.action
            self.droplist.append(self.action)
            self.Board[row, col] = self.chessman
            self.ActionToDraw(self.action, self.chessman)
            if IsContinuous(self.Board, self.action):
                self.Notice(True)
                self.ClossWindow('You Lose ~ (QAQ)')
            else:
                self.CurrentPlayer = "Player2"
                self.chessman = -self.chessman
                self.Notice(False)
        else:
            print("Error")
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy())
    
    def RegretProcess(self):
        if len(self.droplist) >= 2:
            row, col = self.droplist.pop()
            self.Board[row, col] = 0
            row, col = self.droplist.pop()
            self.Board[row, col] = 0
            self.action = self.droplist[len(self.droplist) - 1]
            self.canvas.delete(self.black_chess)
            self.canvas.delete(self.white_chess)
            self.window.update()
    
    def TipProcess(self):
        if self.CurrentPlayer == 'Player2' :
            if not self.button4 :
                _, self.suggest = self.player1.move(self.Board, self.action, -self.chessman)
                self.tip_dict = {}
                self.button4 = True
                for i in range(len(self.suggest[0])):
                    self.tip_dict[i] = self.canvas.create_text((self.suggest[0][i][0] + 1) * 35, (self.suggest[0][i][1] + 1) * 35, text=round(self.suggest[1][i], 2))
                self.window.update()
            elif self.button4 and self.suggest != 0:
                self.button4 = False
                for i in range(len(self.suggest[0])):
                    self.canvas.delete(self.tip_dict[i])
                self.window.update()

    def TieProcess(self):
        if GetValid(self.Board) == []:
            self.text2.set('Tie ~  (0__0)')
            self.label2['bg'] = 'white'
            self.window.update()
            self.ClossWindow('Tie ~  (0__0)')
    
    def BindProcess(self, event):
        self.count += 1
        if self.count == 1:
            self.TieProcess()
            self.action = self.EventToAction(event)
            if self.action in GetValid(self.Board):
                row, col = self.action
                self.droplist.append(self.action)
                self.Board[row, col] = self.chessman
                self.ActionToDraw(self.action, self.chessman)
                if IsContinuous(self.Board, self.action):
                    self.Notice(True)
                    self.ClossWindow('You Win ~ !(o w o)!')
                else:
                    if self.button4:
                        self.TipProcess()
                    self.CurrentPlayer = "Player1"
                    self.chessman = -self.chessman
                    self.Notice(False)
                    self.TieProcess()
                    self.AiProcess()
                    self.count = 0
    
    def Notice(self, End):
        if End:
            if self.CurrentPlayer == 'Player1':
                self.text2.set('You Lose ~ (QAQ)')
                self.label2['bg'] = 'black'
                self.label2['fg'] = 'white'
            else:   # self.CurrentPlayer == 'Player2'
                self.text2.set('You Win ~ !(o w o)!')
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
        
Game = Gobang()
Game.SetWindow()
Game.Run()
