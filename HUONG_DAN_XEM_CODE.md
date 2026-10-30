# Hướng dẫn xem mã nguồn từng bài

**Sinh viên: Lưu Minh Toàn — MSSV: 23458018**

Mở thư mục **`pages`**. Mỗi bài là một file Python riêng, có thể mở bằng VS Code hoặc nhấp chuột phải → **Open with → Notepad** như ví dụ của giảng viên. Nếu Windows ẩn đuôi file, bật **View → Show → File name extensions** để thấy đuôi `.py`.

## Các file cần chấm

| Yêu cầu trong đề | File mã nguồn | Phần cần xem |
| --- | --- | --- |
| 1. Chuyển đổi sRGB ↔ XYZ | [1_Chuyển đổi Không gian Màu.py](pages/1_Chuyển%20đổi%20Không%20gian%20Màu.py) | `main()`: chuẩn hóa RGB, chuyển đổi hai chiều bằng Colour, xử lý hiển thị màu ngoài gamut |
| 2. XYZ từ phổ đo | [2_Tính giá trị 3 thành phần.py](pages/2_Tính%20giá%20trị%203%20thành%20phần.py) | `read_spectrum()` kiểm tra CSV; `spectrum_xyz()` tích phân phổ; `main()` nhập và xuất kết quả |
| 3. Biểu đồ CIE móng ngựa | [3_Vẽ biểu đồ CIE.py](pages/3_Vẽ%20biểu%20đồ%20CIE.py) | `cie_axes()` dựng biểu đồ; `main()` đánh dấu điểm trắng D65 |
| 4. Gamut thiết bị RGB | [4_Vẽ gamut màu của thiết bị RGB.py](pages/4_Vẽ%20gamut%20màu%20của%20thiết%20bị%20RGB.py) | `cie_axes()` và `main()`: lấy primaries, khép tam giác gamut, nhập thiết bị tùy chỉnh |
| 5. Gamut máy in | [5_Vẽ gamut màu của thiết bị in.py](pages/5_Vẽ%20gamut%20màu%20của%20thiết%20bị%20in.py) | `printer_gamut()`: đọc Lab, đổi XYZ → xy; `main()` vẽ đa giác sáu mẫu |
| 6. Đặc tính hóa máy in nửa tông | [6_Đặc tính hoá của máy in nửa tông.py](pages/6_Đặc%20tính%20hoá%20của%20máy%20in%20nửa%20tông.py) | `halftone_data()` đọc MAT; `trc()` tính đường cong; `predict_mix()` dự báo; `main()` gồm bốn chế độ |
| Nâng cao: CIE band 400–700 nm | [7_CIE_band_400_700.py](pages/7_CIE_band_400_700.py) | `band_data()` lấy mẫu 400–700 nm; `main()` vẽ band và hàm phối màu |
| Nâng cao: CIELab, Lab1 → Lab2 | [8_CIELab_so_sanh_mau.py](pages/8_CIELab_so_sanh_mau.py) | `lab_difference()` tính độ lệch, ΔE76/ΔE00; `main()` nhận xét, vẽ a*b*, 3D và CIE xy |
| Nâng cao: logo trường, khoa | [home.py](home.py) | Khối nhận diện HCMUTE, logo khoa, thông tin sinh viên trên trang chủ |

## Cách đọc mỗi file

1. **Thư viện và quy ước dùng chung:** các import ở đầu file.
2. **Các hàm tính toán / dựng biểu đồ:** công thức và xử lý dữ liệu của chính bài đó. Bài 1 tính trực tiếp trong `main()`.
3. **Hàm `main()`:** nhập dữ liệu bằng Streamlit, gọi phép tính và trình bày kết quả.

Các file bài tập gọi thư viện `colour-science` cho các phép chuyển đổi tiêu chuẩn. Các bước chuẩn bị dữ liệu, công thức TRC/trộn mực, điều kiện đầu vào và cách dựng biểu đồ được viết trực tiếp trong file bài tương ứng.

## Những file hỗ trợ

- `app.py`: đăng ký trang chủ và tám trang bài tập, giữ thứ tự 1–8.
- `core.py`: chỉ còn đường dẫn project, hàm phối màu CIE dùng chung, điểm trắng và hàm hiển thị sRGB.
- `ui.py`: định dạng trang, ô màu, kết quả số và tải biểu đồ PNG.
- `assets/`: logo và tài liệu nguồn nhận diện.
- `tests/test_app.py`: kiểm tra số học và hoạt động của từng bài.
- `Color_Cyan_Sample.csv`, `GamutMayIn_CMY_RGB_2.csv`, `halftone.mat`: dữ liệu mẫu giữ từ project gốc.

## Xem ứng dụng chạy

Mở `run.bat` rồi truy cập **http://localhost:8501**. Chọn bài trong thanh bên. Đọc file `.py` bằng Notepad chỉ để xem code; muốn thực thi giao diện cần chạy bằng Streamlit và giữ các file hỗ trợ trong project.

Xem hướng dẫn cài thư viện và quy ước khoa học trong [README.md](README.md).
