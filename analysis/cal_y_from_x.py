#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import json
import os

# ————————————————————————
# ここで入力ファイル名を指定してください
X_CSV_PATH = "Na.csv"       
PARAMS_JSON = "fit_params.json"   
# ————————————————————————

def main():
    # 入力ファイルチェック
    if not os.path.isfile(X_CSV_PATH):
        raise FileNotFoundError(f"X座標CSVが見つかりません: {X_CSV_PATH}")
    if not os.path.isfile(PARAMS_JSON):
        raise FileNotFoundError(f"フィットパラメータJSONが見つかりません: {PARAMS_JSON}")

    # X CSV をヘッダーなしで読み込む
    df_x = pd.read_csv(X_CSV_PATH, header=None)
    # numpy 配列に変換（shape を保つためにそのまま）
    x = df_x.values.astype(float)

    # JSON から傾き・切片を読み込む
    with open(PARAMS_JSON, 'r', encoding='utf-8') as f:
        params = json.load(f)
    slope = float(params['slope'])
    intercept = float(params['intercept'])

    # Y = slope * X + intercept を計算
    y = slope * x + intercept

    # DataFrame 化して元の形（行・列数）を保つ
    df_y = pd.DataFrame(y, index=df_x.index, columns=df_x.columns)

    # 出力ファイル名は「元のファイル名（拡張子除く）＋cal.csv」
    base = os.path.splitext(X_CSV_PATH)[0]
    output_path = f"../result/{base}cal.csv"

    # ヘッダー・インデックスなしで書き出し
    df_y.to_csv(output_path, header=False, index=False)
    print(f"計算結果を出力しました: {output_path}")

if __name__ == '__main__':
    main()
