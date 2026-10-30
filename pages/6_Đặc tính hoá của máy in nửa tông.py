"""BÀI 6: Đặc tính hoá của máy in nửa tông.

Mở file này để xem phần tính toán và giao diện của riêng bài 6.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from core import ROOT, display_rgb
from ui import setup, plot, swatch
import colour
from core import CMFS
from scipy.io import loadmat


# 2. Các hàm tính toán / dựng biểu đồ của bài
def halftone_data(source=None):
    data = loadmat(source or ROOT / 'halftone.mat')
    p = np.vstack((data['W'], data['P'])).astype(float)
    if p.shape != (121, 31) or not np.isfinite(p).all() or np.any((p < 0) | (p > 1)):
        raise ValueError('MAT phải chứa W (1×31), P (120×31), phản xạ trong 0–1.')
    return p, p[:11], p[::11]


def trc(reflections, n=20):
    root = reflections ** (1 / n)
    direction = root[-1] - root[0]
    denom = direction @ direction
    if denom < 1e-15:
        raise ValueError('Phổ mực đặc và nền giấy trùng nhau, không thể tính TRC.')
    area = ((root - root[0]) @ direction) / denom
    return area, np.polyfit(np.linspace(0, 1, 11), area, 3)


def predict_mix(p, mi, yi, n=20):
    _, py = trc(p[:11], n)
    _, pm = trc(p[::11], n)
    m = np.clip(np.polyval(pm, mi / 10), 0, 1)
    y = np.clip(np.polyval(py, yi / 10), 0, 1)
    weights = np.array([(1-m)*(1-y), m*(1-y), y*(1-m), m*y])
    primaries = p[[0, 110, 10, 120]]
    return (weights @ (primaries ** (1/n))) ** n


def spectrum_xyz(a, illuminant='D65'):
    sd = colour.SpectralDistribution(dict(a))
    return colour.sd_to_XYZ(sd, CMFS, colour.SDS_ILLUMINANTS[illuminant], method='Integration')


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('06 · Đặc tính hóa máy in nửa tông', 'Dữ liệu đo 400–700 nm · 11 mức trame · Mô hình Yule–Nielsen và Demichel')
    source = st.file_uploader('MAT tùy chọn: W (1×31), P (120×31)', type=['mat'])
    st.download_button('Tải dữ liệu MAT mẫu', (ROOT / 'halftone.mat').read_bytes(), 'halftone.mat')
    n = st.slider('Hệ số Yule–Nielsen n', 1., 30., 20., .5)
    mode = st.radio('Nội dung', ['Bảng màu trộn', 'Phổ phản xạ', 'Đường cong tái tạo tông', 'Dự báo trộn màu'], horizontal=True)
    try:
        p, yellow, magenta = halftone_data(source)
        wave = np.arange(400, 701, 10)
        levels = np.linspace(0, 1, 11)
        if mode == 'Bảng màu trộn':
            colors = np.array([display_rgb(spectrum_xyz(np.column_stack([wave, r])) / 100) for r in p]).reshape(11, 11, 3)
            fig, ax = plt.subplots(figsize=(7, 6))
            ax.imshow(colors, origin='lower', extent=(-.05, 1.05, -.05, 1.05))
            ax.set(xlabel='Tỷ lệ Yellow', ylabel='Tỷ lệ Magenta', xticks=levels, yticks=levels, title='121 mẫu màu đo · D65')
            plot(fig, 'bang-mau-nua-tong')
            st.caption('Màu ngoài gamut màn hình được cắt về sRGB để hiển thị, không thay đổi phổ đo.')
        elif mode == 'Phổ phản xạ':
            for col, samples, name, cmap in zip(st.columns(2), [yellow, magenta], ['Yellow', 'Magenta'], ['YlOrBr', 'RdPu']):
                with col:
                    fig, ax = plt.subplots(figsize=(6, 4))
                    for i, r in enumerate(samples):
                        ax.plot(wave, r, color=plt.get_cmap(cmap)(.25 + .7*i/10), label=f'{i*10}%')
                    ax.set(xlabel='Bước sóng (nm)', ylabel='Phản xạ', ylim=(0, 1), title=name)
                    ax.legend(ncol=3, fontsize=8)
                    plot(fig, 'pho-'+name)
        elif mode == 'Đường cong tái tạo tông':
            for col, samples, name in zip(st.columns(2), [yellow, magenta], ['Yellow', 'Magenta']):
                with col:
                    area, coefficients = trc(samples, n)
                    x = np.linspace(0, 1, 101)
                    fig, ax = plt.subplots(figsize=(5, 4))
                    ax.plot(levels, levels, '--', label='Lý tưởng')
                    ax.plot(levels, area, 'o', label='Ước lượng từ phổ')
                    ax.plot(x, np.polyval(coefficients, x), label='Khớp đa thức bậc 3')
                    ax.set(xlabel='Tỷ lệ trame mục tiêu', ylabel='Tỷ lệ diện tích hiệu dụng', title=name)
                    ax.legend()
                    plot(fig, 'trc-'+name)
                    st.dataframe(pd.DataFrame({'Mục tiêu': levels, 'Hiệu dụng': area, 'Gia tăng tầng thứ (%)': (area-levels)*100}))
            st.latex(r'R^{1/n}=(1-a)W^{1/n}+aS^{1/n}')
        else:
            mi = st.select_slider('Magenta (%)', options=list(range(0, 101, 10)), value=50) // 10
            yi = st.select_slider('Yellow (%)', options=list(range(0, 101, 10)), value=50) // 10
            measured = p[mi*11+yi]
            pred = predict_mix(p, mi, yi, n)
            fig, ax = plt.subplots(figsize=(9, 4))
            ax.plot(wave, measured, 'o', label='Phổ đo')
            ax.plot(wave, pred, label='Dự báo Yule–Nielsen + Demichel')
            ax.set(xlabel='Bước sóng (nm)', ylabel='Phản xạ', ylim=(0, 1))
            ax.legend()
            plot(fig, 'du-bao-tron-mau')
            st.metric('RMSE phổ phản xạ', f'{np.sqrt(np.mean((pred-measured)**2)):.6f}')
            for col, r, label in zip(st.columns(2), [measured, pred], ['Màu đo', 'Màu dự báo']):
                with col:
                    swatch(display_rgb(spectrum_xyz(np.column_stack([wave, r])) / 100), label)
            st.download_button('Tải phổ đo và dự báo', pd.DataFrame({'nm': wave, 'measured': measured, 'predicted': pred}).to_csv(index=False), 'du-bao.csv')
            st.caption('TRC bậc 3 hiệu chỉnh tỷ lệ trame. Diện tích hiệu dụng dùng dự báo được giới hạn 0–1. So sánh trên chính bộ dữ liệu đặc tính hóa, không phải tập kiểm định độc lập.')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        st.error(f'Không xử lý được dữ liệu nửa tông: {exc}')


if __name__ == "__main__":
    main()
