import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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

# レイアウト調整
col1, col2 = st.columns([2, 2])

# セッションステートの初期化
def reset_inputs():
    st.session_state.clear()

def init_session():
    for key in ["CR", "AUCratio", "IR", "IC"]:
        if key not in st.session_state:
            st.session_state[key] = ""
init_session()

# 入力欄（デフォルト値を空欄に設定）
CR = col1.text_input("CR (基質寄与率)", st.session_state["CR"], key="CR")
AUCratio = col2.text_input("AUCratio", st.session_state["AUCratio"], key="AUCratio")
IR = col1.text_input("IR (阻害率)", st.session_state["IR"], key="IR")
IC = col2.text_input("IC (誘導率)", st.session_state["IC"], key="IC")

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
        
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({**{"CR": CR, "IR": IR, "IC": IC, "AUCratio": AUCratio}, **results})
        
        st.write("### 過去の計算結果")
        history_df = pd.DataFrame(st.session_state.history)
        st.dataframe(history_df)
    else:
        st.warning("計算に必要な値を入力するか、適切な値を設定してください。")

# Googleスプレッドシートからデータを取得
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
gc = gspread.authorize(credentials)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Bd5F6XkxNYO3b2UCm--Sr-P-QFUNqgF1RhfzaQqQ3xE/edit?usp=sharing"
sheet = gc.open_by_url(spreadsheet_url).sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)

st.write("### Googleスプレッドシートデータ")
st.dataframe(df)

# クリアボタンで計算前の状態に戻す
if st.button("クリア"):
    reset_inputs()
    init_session()
    st.rerun()
