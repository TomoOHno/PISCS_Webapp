import streamlit as st
import pandas as pd

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

# デフォルトCSVファイルのパス（デプロイ時には適切なパスに変更）
default_csv_path = "default_data.csv"
df = None

# CSVファイルのアップロード
uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])

if uploaded_file:
    file_path = uploaded_file
else:
    file_path = default_csv_path  # デフォルトCSVを利用

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
required_columns = {'分子種', '薬物名', 'CR', 'AUCratio', 'IR', 'IC'}
if df is not None and required_columns.issubset(df.columns):
    st.write("### 抽出されたデータ")
    st.dataframe(df[list(required_columns)])

    # 検索機能
    selected_drug = st.selectbox("薬物名を選択", df['薬物名'].dropna().unique())
    filtered_df = df[df['薬物名'] == selected_drug]
    st.write("### 選択された薬物の情報")
    
    if not filtered_df.empty:
        selected_data = filtered_df.iloc[0]
        st.session_state["CR"] = selected_data['CR']
        st.session_state["AUCratio"] = selected_data['AUCratio']
        st.session_state["IR"] = selected_data['IR']
        st.session_state["IC"] = selected_data['IC']
    
    st.dataframe(filtered_df)

# レイアウト調整
col1, col2 = st.columns([2, 2])

# 入力欄（デフォルト値をCSVデータから反映）
CR = col1.text_input("CR (基質寄与率)", st.session_state.get("CR", ""), key="CR")
AUCratio = col2.text_input("AUCratio", st.session_state.get("AUCratio", ""), key="AUCratio")
IR = col1.text_input("IR (阻害率)", st.session_state.get("IR", ""), key="IR")
IC = col2.text_input("IC (誘導率)", st.session_state.get("IC", ""), key="IC")

# 計算処理
if st.button("計算"):
    try:
        CR = float(st.session_state.CR) if st.session_state.CR else 0.0
        AUCratio = float(st.session_state.AUCratio) if st.session_state.AUCratio else 0.0
        IR = float(st.session_state.IR) if st.session_state.IR else 0.0
        IC = float(st.session_state.IC) if st.session_state.IC else 0.0
    except ValueError:
        st.warning("数値を正しく入力してください。")
        st.stop()
    
    results = {}
    
    if IR > 0 and IC == 0:
        if CR > 0 and IR > 0:
            results["AUCratio"] = calculate_auc_ratio(CR, IR)
        if CR > 0 and AUCratio > 0:
            results["IR"] = calculate_ir(CR, AUCratio)
        if AUCratio > 0 and IR > 0:
            results["CR"] = calculate_cr_from_ir(AUCratio, IR)
    
    if IC > 0 and IR == 0:
        if CR > 0 and IC > 0:
            results["AUCratio (誘導)"] = calculate_auc_ratio_ic(CR, IC)
        if CR > 0 and AUCratio > 0:
            results["IC"] = calculate_ic(CR, AUCratio)
        if AUCratio > 0 and IC > 0:
            results["CR"] = calculate_cr_from_ic(AUCratio, IC)
    
    if IR == 0 and IC == 0 and CR > 0 and AUCratio > 0:
        results["IR"] = calculate_ir(CR, AUCratio)
        results["IC"] = calculate_ic(CR, AUCratio)
    
    results = {k: v for k, v in results.items() if v is not None}  # 無効な値を除外
    
    if results:
        st.write("### 計算結果")
        for key, value in results.items():
            st.write(f"{key}: {value:.4f}")
    else:
        st.warning("計算に必要な値を入力するか、適切な値を設定してください。")

# クリアボタンで計算前の状態に戻す
if st.button("クリア"):
    st.session_state.clear()
    st.rerun()
