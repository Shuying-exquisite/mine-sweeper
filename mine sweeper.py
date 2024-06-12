import streamlit as st
import numpy as np

# 游戏参数
ROWS = 10
COLS = 10
MINES = 10

# 初始化游戏状态
def init_game():
    board = np.zeros((ROWS, COLS), dtype=int)
    mines_positions = set()
    while len(mines_positions) < MINES:
        pos = (np.random.randint(0, ROWS), np.random.randint(0, COLS))
        if pos not in mines_positions:
            mines_positions.add(pos)
            board[pos] = -1
    for r in range(ROWS):
        for c in range(COLS):
            if board[r, c] == -1:
                continue
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS and board[rr, cc] == -1:
                        board[r, c] += 1
    return board, np.full((ROWS, COLS), False), np.full((ROWS, COLS), False)

if 'board' not in st.session_state:
    st.session_state.board, st.session_state.revealed, st.session_state.flags = init_game()

board = st.session_state.board
revealed = st.session_state.revealed
flags = st.session_state.flags

def show_board():
    display_board = np.full((ROWS, COLS), '', dtype=object)
    for r in range(ROWS):
        for c in range(COLS):
            if flags[r, c]:
                display_board[r, c] = '🚩'
            elif not revealed[r, c]:
                display_board[r, c] = ''
            elif board[r, c] == -1:
                display_board[r, c] = '💣'
            else:
                display_board[r, c] = str(board[r, c])
    return display_board

def click_cell(r, c):
    if flags[r, c] or revealed[r, c]:
        return
    revealed[r, c] = True
    if board[r, c] == -1:
        st.error("Game Over! You hit a mine.")
    elif board[r, c] == 0:
        to_check = [(r, c)]
        while to_check:
            cr, cc = to_check.pop()
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    rr, cc = cr + dr, cc + dc
                    if 0 <= rr < ROWS and 0 <= cc < COLS and not revealed[rr, cc] and board[rr, cc] == 0:
                        revealed[rr, cc] = True
                        to_check.append((rr, cc))
                    revealed[rr, cc] = True

def flag_cell(r, c):
    if revealed[r, c]:
        return
    flags[r, c] = not flags[r, c]

# 创建显示板
display_board = show_board()

# 使用 form 确保提交的一致性
with st.form("game_form"):
    for r in range(ROWS):
        cols = st.columns(COLS)
        for c in range(COLS):
            cell_label = display_board[r, c]
            if cell_label == '':
                cell_label = " "
            with cols[c]:
                if st.form_submit_button(cell_label, key=f"{r}-{c}-reveal"):
                    click_cell(r, c)
                if st.form_submit_button('🚩', key=f"{r}-{c}-flag"):
                    flag_cell(r, c)
    st.form_submit_button("刷新")

# 检查胜利条件
if np.all((board == -1) == flags):
    st.success("Congratulations! You've flagged all the mines.")
