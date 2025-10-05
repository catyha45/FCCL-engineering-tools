import streamlit as st
import numpy as np

# 材料密度字典 (g/cm³)
MATERIAL_DENSITY = {
    '鋁 (Aluminum)': 2.70,
    '銅 (Copper)': 8.96,
    'PI (Polyimide)': 1.42,
    '無': 0.0
}

# 管材密度與重量
CORE_TYPES = {
    '鋁管': 5000,  # g
    '紙管': 500    # g
}

ADHESIVE_DENSITY = 0.92  # 橡膠密度

st.set_page_config(page_title='工程計算工具集', layout='wide')

# 側邊欄選單
with st.sidebar:
    st.title('工具選單')

    if st.button('捲材計算器', use_container_width=True):
        st.session_state.tool = '捲材計算器'
    if st.button('other1', use_container_width=True):
        st.session_state.tool = 'other1'
    if st.button('other2', use_container_width=True):
        st.session_state.tool = 'other2'

    if 'tool' not in st.session_state:
        st.session_state.tool = '捲材計算器'

    tool = st.session_state.tool

# 捲材計算器
if tool == '捲材計算器':
    st.title('捲材計算器')

    st.subheader('基本參數')
    col_core1, col_core2 = st.columns(2)
    with col_core1:
        core_type = st.selectbox('管材類型', list(CORE_TYPES.keys()))
    with col_core2:
        inner_diameter = st.number_input('管材內徑 (mm)', value=164.0, step=1.0)

    st.subheader('第一層材料')
    col1, col2 = st.columns(2)
    with col1:
        material_1 = st.selectbox('第一層材料', list(MATERIAL_DENSITY.keys()), index=1)
    with col2:
        thickness_1 = st.number_input('第一層厚度 (μm)', value=45.0, step=1.0)

    st.subheader('第二層材料')
    col3, col4 = st.columns(2)
    with col3:
        material_2 = st.selectbox('第二層材料', list(MATERIAL_DENSITY.keys()), index=1, key='mat2')
    with col4:
        thickness_2 = st.number_input('第二層厚度 (μm)', value=45.0, step=1.0)

    st.subheader('第三層材料')
    col5, col6 = st.columns(2)
    with col5:
        material_3 = st.selectbox('第三層材料', list(MATERIAL_DENSITY.keys()), index=3, key='mat3')
    with col6:
        thickness_3 = st.number_input('第三層厚度 (μm)', value=0.0, step=1.0)

    st.subheader('膠層')
    adhesive_thickness = st.number_input('膠層厚度 (μm)', value=250.0, step=1.0)

    st.subheader('尺寸')
    col7, col8 = st.columns(2)
    with col7:
        width = st.number_input('料寬 (mm)', value=560.0, step=1.0)
    with col8:
        length_m = st.number_input('長度 (m)', value=700.0, step=1.0)

    if st.button('計算', type='primary'):
        thickness_1_mm = thickness_1 * 1e-3
        thickness_2_mm = thickness_2 * 1e-3
        thickness_3_mm = thickness_3 * 1e-3
        adhesive_thickness_mm = adhesive_thickness * 1e-3
        length_mm = length_m * 1000

        total_thickness = thickness_1_mm + thickness_2_mm + thickness_3_mm + adhesive_thickness_mm

        r = inner_diameter / 2
        R_squared = r * r + (length_mm * total_thickness) / np.pi
        R = np.sqrt(R_squared)
        outer_diameter = 2 * R

        density_1 = MATERIAL_DENSITY[material_1]
        density_2 = MATERIAL_DENSITY[material_2]
        density_3 = MATERIAL_DENSITY[material_3]

        volume_1 = (length_mm / 10) * (width / 10) * (thickness_1_mm / 10)
        volume_2 = (length_mm / 10) * (width / 10) * (thickness_2_mm / 10)
        volume_3 = (length_mm / 10) * (width / 10) * (thickness_3_mm / 10)
        adhesive_volume = (length_mm / 10) * (width / 10) * (adhesive_thickness_mm / 10)

        weight_1 = volume_1 * density_1
        weight_2 = volume_2 * density_2
        weight_3 = volume_3 * density_3
        adhesive_weight = adhesive_volume * ADHESIVE_DENSITY
        core_weight = CORE_TYPES[core_type]
        total_weight = weight_1 + weight_2 + weight_3 + adhesive_weight + core_weight

        st.divider()
        st.subheader('計算結果')

        st.metric('單層總厚度', f'{total_thickness:.4f} mm')
        st.metric('收卷外徑', f'{outer_diameter:.2f} mm ({outer_diameter / 10:.2f} cm)')

        st.divider()

        col9, col10, col11, col12 = st.columns(4)
        with col9:
            st.metric(f'{material_1}重量', f'{weight_1 / 1000:.3f} kg')
        with col10:
            st.metric(f'{material_2}重量', f'{weight_2 / 1000:.3f} kg')
        with col11:
            st.metric(f'{material_3}重量', f'{weight_3 / 1000:.3f} kg')
        with col12:
            st.metric('膠層重量', f'{adhesive_weight / 1000:.3f} kg')

        st.divider()
        st.metric('成品總重', f'{total_weight / 1000:.3f} kg',
                  delta=f'{(total_weight - core_weight) / 1000:.3f} kg (不含{core_type})')

if tool == 'other1':
    st.title('other1')

if tool == 'other2':
    st.title('other2')