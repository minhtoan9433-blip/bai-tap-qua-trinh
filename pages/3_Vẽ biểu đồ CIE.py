"""BÀI 3: Vẽ biểu đồ CIE.

Mở file này để xem phần tính toán và giao diện của riêng bài 3.
Hàm main() dựng giao diện; các hàm phía trên thực hiện tính toán.
core.py chỉ cung cấp quy ước chung; ui.py định dạng giao diện.
"""

# 1. Thư viện và quy ước dùng chung
import streamlit as st
from core import white
from ui import setup, plot
import colour
import colour.plotting


# 2. Các hàm tính toán / dựng biểu đồ của bài
def cie_axes():
    fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931(show=False)
    ax.set(xlim=(-.05, .85), ylim=(-.05, .9), title='CIE 1931 xy · Standard observer 2°')
    return fig, ax


# 3. Nhập dữ liệu, tính kết quả và hiển thị
def main():
    setup('03 · Biểu đồ CIE hình móng ngựa', 'Không gian sắc độ CIE 1931 xy · Đường quang phổ và đường tím')
    fig, ax = cie_axes()
    if st.checkbox('Hiển thị điểm trắng D65', value=True):
        x, y = white()
        ax.scatter(x, y, c='black', marker='+', s=100)
        ax.annotate('D65', (x, y), xytext=(8, 8), textcoords='offset points')
    plot(fig, 'cie-1931')
    st.latex(r'x=X/(X+Y+Z),\quad y=Y/(X+Y+Z),\quad z=1-x-y')
    st.info('xy biểu diễn sắc độ, không thể hiện độ sáng Y. Màu màn hình chỉ minh họa vì màn hình không tái tạo được toàn bộ miền CIE.')


if __name__ == "__main__":
    main()
