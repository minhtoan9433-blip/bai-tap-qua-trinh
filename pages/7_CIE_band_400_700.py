"""BÀI 7: CIE band 400 700.

Mở file này để xem phần tính toán và giao diện của riêng bài 7.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ui import setup, plot
import colour
from core import CMFS


# 2. Các hàm tính toán / dựng biểu đồ của bài
def band_data():
    wave = np.arange(400, 701)
    xyz = CMFS.copy().align(colour.SpectralShape(400, 700, 1)).values
    rgb = colour.XYZ_to_sRGB(xyz)
    # Add white until nonnegative, then normalise for an illustrative display.
    rgb -= np.minimum(rgb.min(axis=1, keepdims=True), 0)
    rgb /= np.maximum(rgb.max(axis=1, keepdims=True), 1e-12)
    return wave, xyz, np.clip(rgb, 0, 1)


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('07 · CIE band 400–700 nm', 'Dải màu quang phổ và hàm phối màu CIE 1931 · Lấy mẫu đúng 400–700 nm')
    wave, xyz, rgb = band_data()
    selected = st.slider('Khảo sát bước sóng (nm)', 400, 700, 550)
    fig, axes = plt.subplots(2, 1, figsize=(11, 5), gridspec_kw={'height_ratios': [1, 3]}, constrained_layout=True)
    axes[0].imshow(rgb[np.newaxis, :, :], aspect='auto', extent=(399.5, 700.5, 0, 1))
    axes[0].set(xlim=(400, 700), yticks=[], title='CIE spectral band · 400–700 nm')
    for i, color, label in zip(range(3), ['#d63b41', '#20824e', '#3159c7'], [r'$\bar{x}(\lambda)$', r'$\bar{y}(\lambda)$', r'$\bar{z}(\lambda)$']):
        axes[1].plot(wave, xyz[:, i], color=color, label=label)
    axes[1].set(xlim=(400, 700), xlabel='Bước sóng λ (nm)', ylabel='Giá trị hàm phối màu')
    for ax in axes:
        ax.axvline(selected, color='#15294d', linestyle='--', linewidth=1)
    axes[1].legend()
    plot(fig, 'cie-band-400-700')
    row = xyz[selected - 400]
    st.dataframe(pd.DataFrame([row], columns=['x̄', 'ȳ', 'z̄'], index=[f'{selected} nm']))
    st.download_button('Tải hàm phối màu 400–700 nm', pd.DataFrame(np.column_stack([wave, xyz]), columns=['nm', 'x_bar', 'y_bar', 'z_bar']).to_csv(index=False), 'cie-band-400-700.csv')
    st.info('Band dùng màu đơn sắc tính từ hàm phối màu 2°, sau đó chuyển sang sRGB. Các màu ngoài gamut được thêm trắng và chuẩn hóa để minh họa sắc độ; band không mô phỏng độ chói vật lý của phổ.')


if __name__ == "__main__":
    main()
