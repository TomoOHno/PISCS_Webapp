import streamlit as st
import pandas as pd
import os

def calculate_auc_ratio(CR, IR):
    if CR * IR >= 1:
        return None
    return 1 / (1 - CR * IR)

def calculate_ir(CR, AUCratio):
    if AUCratio * CR == 0:
        return None
    return (AUCratio - 1) / (AUCratio * CR)

def calculate_cr_from_ir(AUCratio, IR):
    if AUCratio * IR == 0:
        return None
    return (AUCratio - 1) / (AUCratio * IR)

def calculate_auc_ratio_ic(CR, IC):
    return 1 / (1 + CR * IC)

def calculate_ic(CR, AUCratio):
    if AUCratio * CR == 0:
        return None
    return (1 - AUCratio) / (AUCratio * CR)

def calculate_cr_from_ic(AUCratio, IC):
    if AUCratio * IC == 0:
        return None
    return (1 - AUCratio) / (AUCratio * IC)

st.title("薬物相互作用 計算ツール")

# デフォルトCSVファイルのパス
default_csv_path = "default_data.csv"
df = None

# CSVファイルのアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

if uploaded_file:
    file_path = uploaded_file
elif os.path.exists(default_csv_path):
    file_path = default_csv_path  # デフォルトCSVを利用
else:
    file_path = None
    st.warning("デフォルトのCSVファイルが存在しません。CSVをアップロードしてください。")

if file_path:
    try:
        df = pd.read_csv(file_path, encoding="utf-8", skip_blank_lines=True, on_bad_lines='skip')
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"CSVの読み込みに失敗しました: {e}")
        df = None

if df is not None and not df.empty:
    st.write("### CSVデータ")
    st.dataframe(df)
else:
    st.warning("CSVファイルが空か、正しく読み込めませんでした。データを確認してください。")

# 必要なカラムを表示
required_columns = {'分子種', '薬物名', '影響度'}
if df is not None and required_columns.issubset(df.columns):
    st.write("### 分子種・薬物名・影響度のピックアップ")
    extracted_df = df[list(required_columns)]
    st.dataframe(extracted_df)

    # 検索機能
    selected_drug = st.selectbox("薬物名を選択", df['薬物名'].dropna().unique())
    filtered_df = df[df['薬物名'] == selected_drug]
    st.write("### 選択された薬物の情報")
    
    if not filtered_df.empty:
        st.dataframe(filtered_df)

# クリアボタンで計算前の状態に戻す
if st.button("クリア"):
    st.session_state.clear()
    st.rerun()
