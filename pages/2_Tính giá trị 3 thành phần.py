"""BÀI 2: Tính giá trị 3 thành phần.

Mở file này để xem phần tính toán và giao diện của riêng bài 2.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from core import ROOT
from ui import setup, metrics, plot
import numpy as np
import colour
from core import CMFS


# 2. Các hàm tính toán / dựng biểu đồ của bài
def read_spectrum(source, percent=False):
    df = pd.read_csv(source, header=None, comment='#')
    if df.shape[1] != 2:
        raise ValueError('CSV phải có đúng 2 cột: bước sóng (nm), phản xạ.')
    numeric = df.apply(pd.to_numeric, errors='coerce')
    if numeric.iloc[0].isna().all():
        numeric = numeric.iloc[1:]
    a = numeric.to_numpy(float)
    if len(a) < 4 or not np.isfinite(a).all():
        raise ValueError('Cần ít nhất 4 dòng dữ liệu số hữu hạn.')
    a = a[np.argsort(a[:, 0])]
    if np.any(np.diff(a[:, 0]) <= 0):
        raise ValueError('Bước sóng không được trùng nhau.')
    if a[0, 0] < 360 or a[-1, 0] > 830:
        raise ValueError('Bước sóng phải nằm trong 360–830 nm.')
    if percent:
        a[:, 1] /= 100
    if np.any((a[:, 1] < 0) | (a[:, 1] > 1)):
        raise ValueError('Phản xạ phải trong 0–1; chọn đơn vị % nếu file dùng 0–100.')
    return a


def spectrum_xyz(a, illuminant='D65'):
    sd = colour.SpectralDistribution(dict(a))
    return colour.sd_to_XYZ(sd, CMFS, colour.SDS_ILLUMINANTS[illuminant], method='Integration')


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('02 · Tính XYZ từ phổ phản xạ', 'Tích phân phổ × nguồn sáng × hàm phối màu CIE 1931, quan sát viên 2°')
    source = st.file_uploader('CSV phổ đo: bước sóng (nm), phản xạ', type=['csv'])
    percent = st.checkbox('Phản xạ trong file dùng đơn vị % (0–100)')
    illuminant = st.selectbox('Nguồn sáng', ['D65', 'D50', 'A'])
    st.caption('Chưa tải file: dùng Color_Cyan_Sample.csv. Chấp nhận CSV có hoặc không có tiêu đề.')
    st.download_button('Tải CSV mẫu', (ROOT / 'Color_Cyan_Sample.csv').read_bytes(), 'Color_Cyan_Sample.csv')
    try:
        a = read_spectrum(source if source is not None else ROOT / 'Color_Cyan_Sample.csv', percent)
        xyz = spectrum_xyz(a, illuminant)
        metrics(['X', 'Y', 'Z'], xyz)
        if a[0, 0] > 360 or a[-1, 0] < 830:
            st.info(f'File phủ {a[0,0]:g}–{a[-1,0]:g} nm. Colour nội suy và mở rộng bằng giá trị biên đến 360–830 nm; XYZ là ước lượng khi thiếu phổ ở hai đầu.')
        st.latex(r'X=k\int R(\lambda)S(\lambda)\overline{x}(\lambda)d\lambda,\quad k=100/\int S(\lambda)\overline{y}(\lambda)d\lambda')
        st.caption('Y, Z tính tương tự với ȳ, z̄. Vật phản xạ hoàn hảo có Y = 100.')
        fig, ax = plt.subplots(figsize=(9, 3))
        ax.plot(a[:, 0], a[:, 1], color='#275dad')
        ax.set(xlabel='Bước sóng (nm)', ylabel='Phản xạ', ylim=(0, 1), title='Phổ phản xạ đo được')
        plot(fig, 'pho-phan-xa')
        st.dataframe(pd.DataFrame(a, columns=['Bước sóng (nm)', 'Phản xạ']))
        st.download_button('Tải kết quả XYZ', pd.DataFrame([xyz], columns=['X', 'Y', 'Z']).to_csv(index=False), 'XYZ.csv')
    except (ValueError, TypeError, KeyError, UnicodeError) as exc:
        st.error(f'Không đọc được phổ: {exc}')


if __name__ == "__main__":
    main()
