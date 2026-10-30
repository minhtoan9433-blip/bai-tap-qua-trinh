"""BÀI 5: Vẽ gamut màu của thiết bị in.

Mở file này để xem phần tính toán và giao diện của riêng bài 5.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import numpy as np
import pandas as pd
import colour
from core import ROOT
from ui import setup, plot
import colour.plotting
from core import white


# 2. Các hàm tính toán / dựng biểu đồ của bài
def printer_gamut(source, illuminant='D50'):
    df = pd.read_csv(source).set_index('ColorSpace')
    labels = ['R', 'Y', 'G', 'C', 'B', 'M']
    if not set(labels).issubset(df.columns) or not {'L', 'a', 'b'}.issubset(df.index):
        raise ValueError('Cần cột ColorSpace,C,M,Y,R,G,B và các dòng L,a,b như file mẫu.')
    lab = df.loc[['L', 'a', 'b'], labels].to_numpy(float).T
    if not np.isfinite(lab).all() or np.any((lab[:, 0] < 0) | (lab[:, 0] > 100)):
        raise ValueError('Lab phải hữu hạn và L* trong 0–100.')
    xyz = colour.Lab_to_XYZ(lab, white(illuminant))
    if np.any(xyz.sum(axis=1) <= 1e-12):
        raise ValueError('Không xác định được xy cho mẫu màu đen tuyệt đối.')
    return labels, lab, colour.XYZ_to_xy(xyz)


def cie_axes():
    fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    ax.set(xlim=(-.05, .85), ylim=(-.05, .9), title='CIE 1931 xy · Standard observer 2°')
    return fig, ax


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('05 · Gamut màu máy in', 'Đọc sáu mẫu Lab C, M, Y, R, G, B và biểu diễn trên CIE xy')
    source = st.file_uploader('CSV gamut máy in', type=['csv'])
    illuminant = st.selectbox('Điểm trắng của dữ liệu Lab', ['D65', 'D50'])
    st.caption('Mẫu không ghi điểm trắng. D65 giữ quy ước project gốc; chọn D50 nếu dữ liệu đo theo D50.')
    st.download_button('Tải CSV gamut mẫu', (ROOT / 'GamutMayIn_CMY_RGB_2.csv').read_bytes(), 'GamutMayIn_CMY_RGB_2.csv')
    try:
        labels, lab, xy = printer_gamut(source if source is not None else ROOT / 'GamutMayIn_CMY_RGB_2.csv', illuminant)
        fig, ax = cie_axes()
        p = np.vstack([xy, xy[0]])
        ax.plot(p[:, 0], p[:, 1], 'ko-', label='Máy in: R–Y–G–C–B–M')
        for label, point in zip(labels, xy):
            ax.annotate(label, point, xytext=(5, 5), textcoords='offset points')
        if st.checkbox('So sánh sRGB', value=True):
            rgb = colour.RGB_COLOURSPACES['sRGB'].primaries
            rgb = np.vstack([rgb, rgb[0]])
            ax.plot(rgb[:, 0], rgb[:, 1], '--', color='#275dad', label='sRGB · D65')
        ax.legend()
        plot(fig, 'gamut-may-in')
        df = pd.DataFrame(np.column_stack([lab, xy]), index=labels, columns=['L*', 'a*', 'b*', 'x', 'y'])
        st.dataframe(df)
        st.download_button('Tải tọa độ gamut', df.to_csv(), 'gamut-xy.csv')
        st.info('Đa giác qua sáu mẫu là gamut gần đúng theo xy, không mô tả toàn bộ thể tích gamut 3D.')
    except (ValueError, KeyError, TypeError, UnicodeError) as exc:
        st.error(f'File gamut không hợp lệ: {exc}')


if __name__ == "__main__":
    main()
