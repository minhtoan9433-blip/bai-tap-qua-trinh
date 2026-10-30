import io
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def setup(title, caption):
    st.set_page_config(page_title=title + ' · Khoa học Màu sắc', page_icon='🎨', layout='wide')
    st.markdown('''<style>
    .stApp {background: #f6f8fc;}
    h1,h2,h3 {color:#15294d;}
    [data-testid="stSidebar"] {background:#eaf0f9;}
    [data-testid="stMetric"] {background:white;padding:16px;border-radius:12px;border:1px solid #dde5f1;}
    .block-container {padding-top:2rem;max-width:1250px;}
    </style>''', unsafe_allow_html=True)
    st.caption('COLOR SCIENCE LAB / LƯU MINH TOÀN · 23458018')
    st.title(title)
    st.caption(caption)

def plot(fig, name='bieu-do'):
    st.pyplot(fig)
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=160, bbox_inches='tight')
    st.download_button('Tải biểu đồ PNG', buffer.getvalue(), name + '.png', 'image/png', key=name)
    plt.close(fig)

def swatch(rgb, label='Màu hiển thị'):
    rgb = np.clip(rgb, 0, 1)
    st.image(np.tile(rgb, (70, 260, 1)), caption=label, width=260)

def metrics(labels, values):
    for col, label, value in zip(st.columns(len(labels)), labels, values):
        col.metric(label, f'{value:.4f}')
