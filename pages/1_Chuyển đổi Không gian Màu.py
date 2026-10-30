"""BÀI 1: Chuyển đổi Không gian Màu.

Mở file này để xem phần tính toán và giao diện của riêng bài 1.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import numpy as np
import colour
from ui import setup, metrics, swatch


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('01 · Chuyển đổi sRGB ↔ XYZ', 'Gamma sRGB · Điểm trắng D65 · XYZ theo thang Y = 100')
    mode = st.radio('Chiều chuyển đổi', ['sRGB → XYZ', 'XYZ → sRGB'], horizontal=True)
    left, right = st.columns(2)
    with left:
        if mode == 'sRGB → XYZ':
            rgb = np.array([st.slider(c, 0, 255, v) for c, v in zip(['R', 'G', 'B'], [45, 120, 210])]) / 255
            xyz = colour.sRGB_to_XYZ(rgb)
        else:
            xyz = np.array([st.number_input(c, min_value=0., value=v, step=1.) for c, v in zip(['X', 'Y', 'Z'], [20., 25., 30.])]) / 100
            rgb = colour.XYZ_to_sRGB(xyz)
    with right:
        metrics(['X', 'Y', 'Z'], xyz * 100)
        metrics(['R (0–255)', 'G (0–255)', 'B (0–255)'], rgb * 255)
        if np.any((rgb < -1e-5) | (rgb > 1 + 1e-5)):
            st.warning('Màu ngoài gamut sRGB. Giữ nguyên giá trị tính toán; ô màu được cắt về 0–255 để hiển thị.')
        swatch(rgb)
    st.latex(r'[X,Y,Z]^T=M_{sRGB\to XYZ}\,[R_{linear},G_{linear},B_{linear}]^T')
    st.info('Đã giải mã gamma sRGB trước khi nhân ma trận và mã hóa gamma khi đổi ngược.')


if __name__ == "__main__":
    main()
