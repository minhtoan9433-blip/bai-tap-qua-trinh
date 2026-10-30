"""BÀI 4: Vẽ gamut màu của thiết bị RGB.

Mở file này để xem phần tính toán và giao diện của riêng bài 4.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import numpy as np
import pandas as pd
import colour
from ui import setup, plot
import colour.plotting


# 2. Các hàm tính toán / dựng biểu đồ của bài
def cie_axes():
    fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    ax.set(xlim=(-.05, .85), ylim=(-.05, .9), title='CIE 1931 xy · Standard observer 2°')
    return fig, ax


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('04 · Gamut thiết bị RGB', 'So sánh tam giác màu của thiết bị trên biểu đồ CIE 1931 xy')
    names = st.multiselect('Không gian RGB', ['sRGB', 'Adobe RGB (1998)', 'Display P3', 'ITU-R BT.2020'], default=['sRGB'])
    custom = st.checkbox('Nhập tọa độ ba màu cơ bản của thiết bị')
    fig, ax = cie_axes()
    for name in names:
        cs = colour.RGB_COLOURSPACES[name]
        points = np.vstack([cs.primaries, cs.primaries[0]])
        ax.plot(points[:, 0], points[:, 1], label=name, linewidth=2)
    if custom:
        defaults = [[.64, .33], [.30, .60], [.15, .06]]
        points = []
        for col, name, values in zip(st.columns(3), ['R', 'G', 'B'], defaults):
            with col:
                points.append([st.number_input(name+' x', 0., 1., values[0]), st.number_input(name+' y', 0., 1., values[1])])
        p = np.array(points)
        if np.any(p.sum(axis=1) > 1) or np.any(p[:, 1] == 0) or abs(np.linalg.det(np.column_stack([p, np.ones(3)]))) < 1e-8:
            st.error('Cần y > 0, x + y ≤ 1; ba điểm không được thẳng hàng.')
        else:
            p = np.vstack([p, p[0]])
            ax.plot(p[:, 0], p[:, 1], 'k--o', label='Thiết bị tùy chỉnh')
    if names or custom:
        ax.legend()
    plot(fig, 'gamut-rgb')
    for name in names:
        st.write(name)
        st.dataframe(pd.DataFrame(colour.RGB_COLOURSPACES[name].primaries, index=['R', 'G', 'B'], columns=['x', 'y']))


if __name__ == "__main__":
    main()
