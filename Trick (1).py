import streamlit as st
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(page_title="누루룽 서바이버", page_icon="⚔️", layout="wide")

html_path = Path(__file__).with_name("game.html")
html = html_path.read_text(encoding="utf-8")

components.html(html, height=820, scrolling=False)
