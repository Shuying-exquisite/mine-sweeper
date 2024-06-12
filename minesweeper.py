import streamlit as st
import streamlit.components.v1 as components

# 读取HTML文件内容
with open("minesweeper.html", "r", encoding="utf-8") as f:
    html_content = f.read()

# 创建Streamlit组件并嵌入HTML内容
components.html(html_content, height=800)

# 其他Streamlit组件（如果需要）
st.title("嵌入式扫雷游戏")
st.write("使用Streamlit嵌入HTML和JavaScript游戏")
