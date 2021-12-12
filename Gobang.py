import numpy as np
import random

# 建立棋盤
def BuildBoard(BoardSize):
    return np.zeros((BoardSize, BoardSize))
    
# 列印棋盤
def PrintBoard(Board):
    for i in Board:
        print(np.where(i == 1, "●", np.where(i == -1, "○", " ")))
    print("\n")

# 獲取可以下棋位置
# 回傳 list，eq. [[2,3],[3,4]]
def GetValid(Board):
    return [[i,j] for i in range(len(Board)) for j in range(len(Board)) if Board[i,j] == 0]

# 依據 action 判斷連續
def IsContinuous(Board, action):
    row, col = action

    # 橫列
    s = np.where(Board[row] == Board[row,col])[0]
    if len(s) >= 5:
        if s[0] + 4 == s[4] or s[len(s)-1] - 4 == s[len(s)-5]:
            return True

    # 直行
    s = np.where(Board[:, col] == Board[row,col])[0]
    if len(s) >= 5:
        if s[0] + 4 == s[4] or s[len(s)-1] - 4 == s[len(s)-5]:
            return True

    # 正斜
    t = [Board[i,j] for i in range(len(Board)) for j in range(len(Board)) if i + j == row + col]
    s = np.where(t == Board[row, col])[0]
    if len(s) >= 5:
        if s[0] + 4 == s[4] or s[len(s)-1] - 4 == s[len(s)-5]:
            return True

    # 反斜
    t = [Board[i,j] for i in range(len(Board)) for j in range(len(Board)) if i - j == row - col]
    s = np.where(t == Board[row, col])[0]
    if len(s) >= 5:
        if s[0] + 4 == s[4] or s[len(s)-1] - 4 == s[len(s)-5]:
            return True
    
    return False

# 選出 Player1 落子
def Player1(Board,laststep):
    return random.choice(GetValid(Board))

# 選出 Player2 落子
def Player2(Board,laststep):
    return random.choice(GetValid(Board))