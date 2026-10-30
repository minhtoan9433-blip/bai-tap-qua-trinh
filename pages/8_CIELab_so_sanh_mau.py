"""BÀI 8: CIELab so sanh mau.

Mở file này để xem phần tính toán và giao diện của riêng bài 8.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colour
from core import white
from ui import setup, plot, metrics, swatch
import colour.plotting


# 2. Các hàm tính toán / dựng biểu đồ của bài
def lab_difference(lab1, lab2):
    a, b = np.asarray(lab1, float), np.asarray(lab2, float)
    delta = b - a
    chroma = np.hypot(b[1], b[2]) - np.hypot(a[1], a[2])
    return delta, chroma, float(colour.delta_E(a, b, method='CIE 1976')), float(colour.delta_E(a, b, method='CIE 2000'))


def cie_axes():
    fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    ax.set(xlim=(-.05, .85), ylim=(-.05, .9), title='CIE 1931 xy · Standard observer 2°')
    return fig, ax


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('08 · CIELab và sự chuyển dịch màu', 'Nhập Lab1, Lab2 · Đồ thị a*b*, CIE xy và không gian L*a*b* 3D')
    illuminant = st.selectbox('Điểm trắng chung cho hai màu Lab', ['D65', 'D50'])
    labs = []
    for col, name, defaults in zip(st.columns(2), ['Lab1', 'Lab2'], [[55., 25., 20.], [65., 5., 40.]]):
        with col:
            st.subheader(name)
            labs.append(np.array([
                st.number_input(name+' · L*', 0., 100., defaults[0]),
                st.number_input(name+' · a*', -150., 150., defaults[1]),
                st.number_input(name+' · b*', -150., 150., defaults[2]),
            ]))
            xyz = colour.Lab_to_XYZ(labs[-1], white(illuminant))
            if illuminant != 'D65':
                xyz = colour.adaptation.chromatic_adaptation_VonKries(xyz, colour.xy_to_XYZ(white(illuminant)), colour.xy_to_XYZ(white('D65')), transform='Bradford')
            rgb = colour.XYZ_to_sRGB(xyz)
            swatch(rgb, name+' · xấp xỉ trên sRGB')
            if np.any((rgb < 0) | (rgb > 1)):
                st.caption('Màu ngoài gamut sRGB; ô hiển thị đã được cắt về 0–1.')
    a, b = labs
    delta, dc, de76, de00 = lab_difference(a, b)
    metrics(['ΔL*', 'Δa*', 'Δb*'], delta)
    metrics(['ΔC*ab', 'ΔE*ab (1976)', 'ΔE00'], [dc, de76, de00])
    remarks = []
    for d, pos, neg, same in zip(delta, ['sáng hơn', 'dịch về phía đỏ (+a*)', 'dịch về phía vàng (+b*)'], ['tối hơn', 'dịch về phía xanh lá (−a*)', 'dịch về phía xanh lam (−b*)'], ['độ sáng không đổi', 'thành phần a* không đổi', 'thành phần b* không đổi']):
        remarks.append(same if abs(d) < 1e-8 else pos if d > 0 else neg)
    remarks.append('độ sắc C* tăng' if dc > 1e-8 else 'độ sắc C* giảm' if dc < -1e-8 else 'C* không đổi')
    st.success('Từ Lab1 sang Lab2: ' + '; '.join(remarks) + '.')
    st.caption('C*ab là độ sắc (chroma); dùng để diễn giải mức độ đậm màu. ΔE là khoảng cách màu, không có một ngưỡng chấp nhận chung cho mọi điều kiện quan sát.')
    L = st.slider('L* của mặt cắt nền a*b*', 0, 100, 60)
    grid = np.linspace(-128, 128, 257)
    aa, bb = np.meshgrid(grid, grid)
    background_lab = np.stack([np.full_like(aa, L), aa, bb], axis=-1)
    xyz_bg = colour.Lab_to_XYZ(background_lab, white(illuminant))
    if illuminant != 'D65':
        xyz_bg = colour.adaptation.chromatic_adaptation_VonKries(xyz_bg, colour.xy_to_XYZ(white(illuminant)), colour.xy_to_XYZ(white('D65')), transform='Bradford')
    rgb_bg = colour.XYZ_to_sRGB(xyz_bg)
    inside = np.all((rgb_bg >= 0) & (rgb_bg <= 1), axis=-1)
    background = np.where(inside[..., None], np.clip(rgb_bg, 0, 1), .94)
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.imshow(background, origin='lower', extent=(-128, 128, -128, 128), alpha=.85)
    ax.axhline(0, color='gray', lw=.7)
    ax.axvline(0, color='gray', lw=.7)
    for lab, label, marker in zip(labs, ['Lab1', 'Lab2'], ['o', 's']):
        ax.scatter(lab[1], lab[2], c='black', marker=marker, s=55)
        ax.annotate(label, (lab[1], lab[2]), xytext=(7, 8), textcoords='offset points')
    ax.annotate('', xy=b[1:], xytext=a[1:], arrowprops={'arrowstyle': '->', 'color': 'black', 'lw': 2})
    ax.set(xlabel='a* (− xanh lá / + đỏ)', ylabel='b* (− xanh lam / + vàng)', title=f'Mặt phẳng a*b* · Nền L* = {L}', xlim=(min(-128, a[1]-10, b[1]-10), max(128, a[1]+10, b[1]+10)), ylim=(min(-128, a[2]-10, b[2]-10), max(128, a[2]+10, b[2]+10)))
    plot(fig, 'cielab-ab')
    st.caption('Vùng nền xám nằm ngoài gamut sRGB tại L* đã chọn. Hai điểm thể hiện tọa độ a*b* của màu nhập; L* riêng của mỗi màu được giữ trong đồ thị 3D.')
    col1, col2 = st.columns(2)
    with col1:
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter([a[1], b[1]], [a[2], b[2]], [a[0], b[0]], c=['#275dad', '#d63b41'], s=70)
        ax.quiver(a[1], a[2], a[0], delta[1], delta[2], delta[0], color='black', arrow_length_ratio=.12)
        for lab, label in zip(labs, ['Lab1', 'Lab2']):
            ax.text(lab[1], lab[2], lab[0], label)
        ax.set(xlabel='a*', ylabel='b*', zlabel='L*', xlim=(-150, 150), ylim=(-150, 150), zlim=(0, 100), title='Không gian CIELab 3D')
        plot(fig, 'cielab-3d')
    with col2:
        fig, ax = cie_axes()
        xyz = colour.Lab_to_XYZ(np.array(labs), white(illuminant))
        valid = xyz.sum(axis=1) > 1e-12
        xy = colour.XYZ_to_xy(xyz)
        for point, ok, label in zip(xy, valid, ['Lab1', 'Lab2']):
            if ok:
                ax.scatter(*point, color='black')
                ax.annotate(label, point, xytext=(7, 7), textcoords='offset points')
        if valid.all():
            ax.annotate('', xy=xy[1], xytext=xy[0], arrowprops={'arrowstyle': '->', 'lw': 2})
        else:
            st.info('Màu đen tuyệt đối không có tọa độ xy xác định.')
        plot(fig, 'cielab-tren-cie-xy')
    st.download_button('Tải kết quả so sánh', pd.DataFrame([list(delta)+[dc, de76, de00]], columns=['delta_L', 'delta_a', 'delta_b', 'delta_C', 'delta_E76', 'delta_E00']).to_csv(index=False), 'so-sanh-Lab.csv')


if __name__ == "__main__":
    main()
