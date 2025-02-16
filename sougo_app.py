import streamlit as st
import pandas as pd

def calculate_auc_ratio(CR, IR):
    if CR * IR >= 1 or CR < 0 or IR < 0:
        return None
    return 1 / (1 - CR * IR) if (1 - CR * IR) != 0 else None

def calculate_ir(CR, AUCratio):
    if AUCratio <= 0 or CR <= 0:
        return None
    return (AUCratio - 1) / (AUCratio * CR) if (AUCratio * CR) != 0 else None

def calculate_cr_from_ir(AUCratio, IR):
    if AUCratio <= 0 or IR <= 0:
        return None
    return (AUCratio - 1) / (AUCratio * IR) if (AUCratio * IR) != 0 else None

def calculate_auc_ratio_ic(CR, IC):
    return 1 / (1 + CR * IC) if (1 + CR * IC) != 0 else None

def calculate_ic(CR, AUCratio):
    if AUCratio <= 0 or CR <= 0:
        return None
    return (1 - AUCratio) / (AUCratio * CR) if (AUCratio * CR) != 0 else None

def calculate_cr_from_ic(AUCratio, IC):
    if AUCratio <= 0 or IC <= 0:
        return None
    return (1 - AUCratio) / (AUCratio * IC) if (AUCratio * IC) != 0 else None

st.title("薬物相互作用 計算ツール")

# レイアウト調整
col1, col2 = st.columns([2, 2])

# セッションステートの初期化
def reset_inputs():
    st.session_state.clear()

def init_session():
    for key in ["CR", "AUCratio", "IR", "IC"]:
        if key not in st.session_state:
            st.session_state[key] = 0.0
    if "history" not in st.session_state:
        st.session_state.history = []

init_session()

# 数値入力
CR = col1.number_input("CR (基質寄与率)", value=st.session_state["CR"], step=0.01, min_value=0.0, format="%.4f", key="CR")
AUCratio = col2.number_input("AUCratio", value=st.session_state["AUCratio"], step=0.01, min_value=0.0, format="%.4f", key="AUCratio")
IR = col1.number_input("IR (阻害率)", value=st.session_state["IR"], step=0.01, min_value=0.0, format="%.4f", key="IR")
IC = col2.number_input("IC (誘導率)", value=st.session_state["IC"], step=0.01, min_value=0.0, format="%.4f", key="IC")

# 計算処理
if st.button("計算"):
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
        
        # 過去の計算結果を記録
        st.session_state.history.append({**{"CR": CR, "IR": IR, "IC": IC, "AUCratio": AUCratio}, **results})
        
        # 過去の計算結果を表示
        st.write("### 過去の計算結果")
        history_df = pd.DataFrame(st.session_state.history)
        st.table(history_df)
    else:
        st.warning("計算に必要な値を入力するか、適切な値を設定してください。")

# クリアボタンでリセット
if st.button("クリア"):
    reset_inputs()
    init_session()
    st.rerun()
