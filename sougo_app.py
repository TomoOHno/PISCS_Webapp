import streamlit as st
import pandas as pd
import os

# CSVデータの読み込み
data_path = "/mnt/data/processed_drug_interaction_data.csv"

if os.path.exists(data_path):
    interaction_data = pd.read_csv(data_path)
else:
    st.warning("データファイルが見つかりません。サンプルデータを使用します。")
    interaction_data = pd.DataFrame({
        "薬物名": ["フルボキサミン", "フルボキサミン"],
        "分子種": ["CYP1A2", "CYP3A"],
        "分類": ["阻害薬", "阻害薬"],
        "強度": ["強い", "強い"]
    })

# Streamlitアプリの作成
st.title("薬物相互作用検索ツール")

# ユーザー入力
search_drug = st.text_input("薬物名を入力:")
selected_molecule = st.selectbox("分子種を選択:", sorted(interaction_data["分子種"].dropna().unique().tolist()))
selected_classification = st.selectbox("分類を選択:", sorted(interaction_data["分類"].dropna().unique().tolist()))
selected_strength = st.selectbox("強度を選択:", sorted(interaction_data["強度"].dropna().unique().tolist()))

# フィルタリング処理
filtered_data = interaction_data.copy()
if search_drug:
    filtered_data = filtered_data[filtered_data["薬物名"].str.contains(search_drug, case=False, na=False)]
if selected_molecule:
    filtered_data = filtered_data[filtered_data["分子種"] == selected_molecule]
if selected_classification:
    filtered_data = filtered_data[filtered_data["分類"] == selected_classification]
if selected_strength:
    filtered_data = filtered_data[filtered_data["強度"] == selected_strength]

# 検索結果の表示
st.write("### 検索結果")
st.dataframe(filtered_data)

# CSVダウンロード機能
if not filtered_data.empty:
    csv = filtered_data.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="検索結果をCSVでダウンロード",
        data=csv,
        file_name="drug_interaction_results.csv",
        mime="text/csv"
    )
import streamlit as st
import pandas as pd

st.title("薬物相互作用データアップロード")

uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df.to_csv("/mnt/data/processed_drug_interaction_data.csv", index=False, encoding="utf-8")
    st.success("データが保存されました！")
