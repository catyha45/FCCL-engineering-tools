import streamlit as st
import numpy as np

# 材料密度字典 (g/cm³)
MATERIAL_DENSITY = {
    '鋁 (Aluminum)': 2.70,
    '銅 (Copper)': 8.96,
    '橡膠 (Rubber)': 0.92
}

st.set_page_config(page_title='工程計算工具集', layout='wide')

# 側邊欄選單
with st.sidebar:
    st.title('工具選單')
    tool = st.radio(
        '選擇工具',
        ['捲材計算器']
    )

# 捲材計算器
if tool == '捲材計算器':
    st.title('捲材計算器')

    st.subheader('基本參數')
    inner_diameter = st.number_input('鋁管內徑 (mm)', value=164.0, step=1.0)

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

    st.subheader('膠層')
    col5, col6 = st.columns(2)
    with col5:
        adhesive_material = st.selectbox('膠層材料', list(MATERIAL_DENSITY.keys()), index=2)
    with col6:
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
        adhesive_thickness_mm = adhesive_thickness * 1e-3
        length_mm = length_m * 1000

        total_thickness = thickness_1_mm + thickness_2_mm + adhesive_thickness_mm

        r = inner_diameter / 2
        R_squared = r * r + (length_mm * total_thickness) / np.pi
        R = np.sqrt(R_squared)
        outer_diameter = 2 * R

        density_1 = MATERIAL_DENSITY[material_1]
        density_2 = MATERIAL_DENSITY[material_2]
        adhesive_density = MATERIAL_DENSITY[adhesive_material]

        volume_1 = (length_mm / 10) * (width / 10) * (thickness_1_mm / 10)
        volume_2 = (length_mm / 10) * (width / 10) * (thickness_2_mm / 10)
        adhesive_volume = (length_mm / 10) * (width / 10) * (adhesive_thickness_mm / 10)

        weight_1 = volume_1 * density_1
        weight_2 = volume_2 * density_2
        adhesive_weight = adhesive_volume * adhesive_density
        total_weight = weight_1 + weight_2 + adhesive_weight + 5000

        st.divider()
        st.subheader('計算結果')

        st.metric('單層總厚度', f'{total_thickness:.4f} mm')
        st.metric('收卷外徑', f'{outer_diameter:.2f} mm ({outer_diameter / 10:.2f} cm)')

        st.divider()

        col9, col10, col11 = st.columns(3)
        with col9:
            st.metric(f'{material_1}重量', f'{weight_1 / 1000:.3f} kg')
        with col10:
            st.metric(f'{material_2}重量', f'{weight_2 / 1000:.3f} kg')
        with col11:
            st.metric(f'{adhesive_material}重量', f'{adhesive_weight / 1000:.3f} kg')

        st.divider()
        st.metric('成品總重', f'{total_weight / 1000:.3f} kg',
                  delta=f'{(total_weight - 5000) / 1000:.3f} kg (不含鋁管)')