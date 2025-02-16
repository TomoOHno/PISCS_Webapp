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

# 入力欄
CR = st.text_input("CR (基質寄与率)", "")
AUCratio = st.text_input("AUCratio", "")
IR = st.text_input("IR (阻害率)", "")
IC = st.text_input("IC (誘導率)", "")

# 計算処理
if st.button("計算"):
    try:
        CR = float(CR) if CR else None
        AUCratio = float(AUCratio) if AUCratio else None
        IR = float(IR) if IR else None
        IC = float(IC) if IC else None
    except ValueError:
        st.warning("数値を正しく入力してください。")
        st.stop()
    
    results = {}

    # IRを使う場合
    if IR is not None and IC is None:
        if CR is not None and IR is not None:
            results["AUCratio"] = calculate_auc_ratio(CR, IR)
        if CR is not None and AUCratio is not None:
            results["IR"] = calculate_ir(CR, AUCratio)
        if AUCratio is not None and IR is not None:
            results["CR"] = calculate_cr_from_ir(AUCratio, IR)

    # ICを使う場合
    if IC is not None and IR is None:
        if CR is not None and IC is not None:
            results["AUCratio (誘導)"] = calculate_auc_ratio_ic(CR, IC)
        if CR is not None and AUCratio is not None:
            results["IC"] = calculate_ic(CR, AUCratio)
        if AUCratio is not None and IC is not None:
            results["CR"] = calculate_cr_from_ic(AUCratio, IC)

    # CRとAUCratioからIRとICを求める場合
    if IR is None and IC is None and CR is not None and AUCratio is not None:
        results["IR"] = calculate_ir(CR, AUCratio)
        results["IC"] = calculate_ic(CR, AUCratio)

    # 計算結果を出力
    if results:
        st.write("### 計算結果")
        for key, value in results.items():
            if value is not None:
                st.write(f"{key}: {value:.4f}")
    else:
        st.warning("計算に必要な値を入力してください。")

# クリアボタンで計算前の状態に戻す
if st.button("クリア"):
    st.experimental_rerun()
