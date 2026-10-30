import os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parent / '.mpl-cache'))
import streamlit as st
pages = [st.Page('home.py', title='Trang chủ', icon='🎨', default=True)]
labels = ['Chuyển đổi sRGB ↔ XYZ', 'XYZ từ phổ đo', 'CIE hình móng ngựa', 'Gamut thiết bị RGB', 'Gamut máy in', 'Máy in nửa tông', 'CIE band 400–700 nm', 'CIELab và chuyển dịch màu']
for i, (path, title) in enumerate(zip(sorted((Path(__file__).resolve().parent / 'pages').glob('[1-8]_*.py')), labels), 1):
    pages.append(st.Page(str(path), title=f'{i:02d} · {title}', url_path=f'bai-{i}'))
st.navigation(pages).run()
