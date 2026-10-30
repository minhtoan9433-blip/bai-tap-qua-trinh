import streamlit as st
from core import ROOT
from importlib import import_module
band_data = import_module('pages.7_CIE_band_400_700').band_data
import base64
from ui import setup
setup('Khoa học Màu sắc', 'Phòng thực hành màu sắc tương tác · Streamlit trên localhost')
school_logo = base64.b64encode((ROOT / 'assets/hcmute.png').read_bytes()).decode('ascii')
st.markdown(f'''
<style>
.school-brand {{display:flex;align-items:center;gap:18px;margin:12px 0 28px;color:#000;}}
.school-emblem {{flex:0 0 86px;width:86px;height:86px;overflow:hidden;}}
.school-emblem img {{display:block;width:600px;max-width:none;height:auto;}}
.school-name {{font-size:21px;font-weight:750;line-height:1.45;color:#000;}}
.school-name-en {{font-size:15px;line-height:1.5;margin-top:6px;color:#000;}}
@media (max-width:600px) {{
    .school-brand {{gap:12px;}}
    .school-name {{font-size:16px;}}
    .school-name-en {{font-size:12px;}}
}}
</style>
<div class="school-brand">
    <div class="school-emblem"><img src="data:image/png;base64,{school_logo}" alt="Logo HCMUTE"></div>
    <div>
        <div class="school-name">TRƯỜNG ĐẠI HỌC<br>CÔNG NGHỆ KỸ THUẬT TP. HỒ CHÍ MINH</div>
        <div class="school-name-en">HCM-UTE · Ho Chi Minh City University of Technology and Engineering</div>
    </div>
</div>
''', unsafe_allow_html=True)
branding, description = st.columns([1, 4])
with branding:
    st.image(str(ROOT / 'assets/logo-khoa.png'), width=140)
with description:
    st.subheader('Khoa In và Truyền thông')
    st.caption('HCMUTE · Bài tập Khoa học Màu sắc')
st.subheader('Lưu Minh Toàn · MSSV 23458018')
st.write('Khám phá cách màu sắc được đo lường, chuyển đổi và tái tạo trên màn hình, máy in. Chọn nội dung trong thanh bên để bắt đầu thực hành với dữ liệu mẫu hoặc file đo của bạn.')
_, _, rgb = band_data()
st.image(rgb[None, :, :].repeat(32, axis=0), width='stretch')
