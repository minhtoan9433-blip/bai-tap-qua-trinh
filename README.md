# Khoa học Màu sắc — Streamlit local

**Sinh viên:** Lưu Minh Toàn — **MSSV:** 23458018.

Hoàn thiện từ [repo gốc](https://github.com/minhtoan9433-blip/KHOA-HOC-MAU-SAC), bản tải về ở commit `a089e01`. Có thể chạy localhost hoặc triển khai trên Streamlit Community Cloud. Logo trường lấy từ website HCMUTE do người dùng cung cấp; logo Khoa In và Truyền thông lấy từ tài liệu nhận diện chính thức của khoa. Nguồn ở `assets/SOURCES.md`.

**Dành cho giảng viên:** mở thư mục `pages` để xem tám file Python theo từng bài. Phần tính toán và giao diện của mỗi bài nằm trực tiếp trong file đó. Bảng đối chiếu file và hàm cần xem nằm trong [HUONG_DAN_XEM_CODE.md](HUONG_DAN_XEM_CODE.md).

## Chạy ngay trên máy hiện tại

Mở `run.bat`, giữ cửa sổ đó trong khi dùng ứng dụng, rồi truy cập **http://localhost:8501**. Dừng bằng `Ctrl+C`.

Hoặc mở PowerShell tại thư mục bài tập:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Cài lại / chạy trên máy khác

Cài Python 3.12, mở terminal trong thư mục project rồi chạy:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Nếu dùng uv: `uv venv --python 3.12`, sau đó `uv pip install -r requirements.txt`.

Môi trường `.venv` không đưa vào file nộp; cần cài lại trên máy khác. Sau khi đã cài thư viện, các phép tính, dữ liệu mẫu và logo hoạt động offline.

## Chạy trên Streamlit Community Cloud

- Chọn repo `minhtoan9433-blip/bai-tap-qua-trinh`, nhánh `main`, file chạy `app.py` (file `Khoa học Màu sắc.py` vẫn được hỗ trợ).
- Trong **Advanced settings**, chọn **Python 3.12**. Bộ phiên bản trong `requirements.txt` dùng được với Python 3.11–3.13; `colour-science==0.4.6` không hỗ trợ Python 3.14.
- Cloud phải cài `requirements.txt` ở thư mục gốc. Lệnh `import colour` thuộc gói **`colour-science`**, không phải gói `colour`.
- Nếu gặp `ModuleNotFoundError` tại `import colour`, mở **Manage app → Logs** để kiểm tra bước cài phụ thuộc, xác nhận đúng repo/nhánh rồi **Reboot app** sau khi cập nhật. Nếu cần đổi Python, triển khai lại theo hướng dẫn của Streamlit.
- Không cài thư viện bằng `pip` bên trong mã ứng dụng. Cloud quản lý thư viện từ `requirements.txt`.

Tài liệu: [Phụ thuộc ứng dụng](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies), [đổi phiên bản Python](https://docs.streamlit.io/deploy/streamlit-community-cloud/manage-your-app/upgrade-python).

## Đối chiếu yêu cầu đề

| Nội dung | Chức năng |
| --- | --- |
| 1. sRGB ↔ XYZ | Nhập RGB 0–255 hoặc XYZ thang Y=100, xử lý gamma, xem ô màu và cảnh báo ngoài gamut |
| 2. XYZ từ phổ đo | Upload CSV, chọn D65/D50/A, phản xạ 0–1 hoặc %, tích phân với CIE 1931 2° |
| 3. CIE móng ngựa | Đường quang phổ, đường tím, tọa độ xy và điểm trắng D65 |
| 4. Gamut RGB | sRGB, Adobe RGB (1998), Display P3, BT.2020, tọa độ primaries tùy chọn |
| 5. Gamut máy in | CSV sáu mẫu Lab, chọn điểm trắng, so sánh sRGB, xuất tọa độ |
| 6. Máy in nửa tông | Bảng 121 màu, phổ 11 mức trame, TRC, dự báo Yellow–Magenta, RMSE |
| Thêm logo | Logo trường và khoa chính thức lưu local trên trang chủ |
| CIE dạng band | Dải phổ và hàm x̄, ȳ, z̄ đúng **400–700 nm**, bước 1 nm; khảo sát bước sóng |
| So sánh CIELab | Nhập Lab1/Lab2; mặt phẳng a*b*, 3D L*a*b*, CIE xy; vector chuyển dịch, ΔL*, Δa*, Δb*, ΔC*, ΔE76, ΔE00 và nhận xét |

Các biểu đồ có thể tải PNG; các trang tính toán có thể xuất dữ liệu CSV.

## Định dạng dữ liệu

- **Phổ:** CSV 2 cột `nm,reflectance`, có/không tiêu đề. Tối thiểu 4 dòng, bước sóng tăng không trùng, trong 360–830 nm. Phản xạ 0–1 hoặc chọn đơn vị %. Mặc định dùng `Color_Cyan_Sample.csv`.
- **Gamut:** giữ cấu trúc `GamutMayIn_CMY_RGB_2.csv`: tiêu đề `ColorSpace,C,M,Y,R,G,B`, ba hàng `L,a,b`.
- **Nửa tông:** MAT có `W` 1×31 và `P` 120×31, tương ứng 400:10:700 nm. Ghép `[W;P]` thành 121 phổ, Yellow thay đổi nhanh nhất, Magenta thay đổi theo từng nhóm 11 mẫu.

## Quy ước khoa học và giới hạn

- Quan sát viên CIE 1931 2°. XYZ nội bộ dùng 0–1, kết quả phổ và chuyển đổi trình bày thang Y=100. sRGB dùng D65 và có xử lý gamma.
- Phổ thiếu hai đầu miền 360–830 nm được thư viện Colour nội suy/mở rộng bằng giá trị biên. Trang tính XYZ nêu rõ giới hạn này. Kết quả từ file 400–700 nm là ước lượng ngoài miền đo.
- File gamut mẫu không ghi điểm trắng Lab. Mặc định D65 để giữ quy ước project mẫu; người dùng có thể đổi D50 theo thiết lập máy đo. Không tự khẳng định dữ liệu đo dùng nguồn sáng nào.
- Trang CIELab dùng cùng điểm trắng cho hai mẫu; khi hiển thị Lab D50 trên sRGB, thích nghi sắc độ D50→D65 bằng Bradford. CIE xy của Lab giữ điểm trắng gốc đã chọn.
- CIE band là màu quang phổ minh họa từ CMFs; thêm trắng và chuẩn hóa RGB ngoài gamut. Band không mô tả độ chói vật lý. Mặt cắt a*b* tô xám vùng ngoài sRGB. Màu nhập giữ nguyên khi tính ΔE; chỉ ô màu hiển thị được cắt gamut.
- ΔC* diễn giải độ sắc (chroma), không đồng nhất tuyệt đối với độ bão hòa. ΔE00 không áp dụng một ngưỡng đạt/không đạt chung cho mọi tình huống.
- Gamut máy in qua sáu mẫu là đa giác gần đúng trong xy, không phải thể tích gamut 3D.
- TRC dùng chiếu bình phương tối thiểu trong miền R^(1/n), khớp đa thức bậc 3; mô hình trộn dùng Demichel và Yule–Nielsen. Tỷ lệ hiệu dụng dự báo được giới hạn 0–1. RMSE so sánh trên cùng bộ dữ liệu đặc tính hóa, không phải kiểm định độc lập.

## Kiểm tra

```powershell
$env:MPLCONFIGDIR = "$PWD/.mpl-cache"
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

11 bài kiểm tra gồm: chuyển đổi trắng sRGB và hai chiều, vật phản xạ hoàn hảo Y=100, dữ liệu CSV lỗi, miền band, đầu mút TRC, cặp tham chiếu ΔE00, thực thi mọi trang bằng Streamlit AppTest và các chế độ tương tác. Có thể xuất hiện cảnh báo `missing ScriptRunContext` khi AppTest chạy; đây là cảnh báo của môi trường kiểm tra.

Mã số sinh viên được giữ từ repo gốc. Mã nguồn và khai báo thư viện được lưu trong repo GitHub.
