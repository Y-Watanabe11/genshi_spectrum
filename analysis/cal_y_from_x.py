#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import json
import os

# ————————————————————————
# ここで入力ファイルと結果出力先を指定
X_CSV_PATH = "../data/Na.csv"       # X 座標のみを含むヘッダーなし CSV
PARAMS_JSON = "fit_params.json"   # フィットパラメータ JSON (slope, intercept, slope_err, intercept_err を含む)
OUTPUT_DIR = "../result"          # 出力ディレクトリ
# ————————————————————————

def main():
    # 入力ファイルチェック
    if not os.path.isfile(X_CSV_PATH):
        raise FileNotFoundError(f"X coordinate CSV not found: {X_CSV_PATH}")
    if not os.path.isfile(PARAMS_JSON):
        raise FileNotFoundError(f"Fit parameters JSON not found: {PARAMS_JSON}")

    # X CSV をヘッダーなしで読み込み、空行/列を削除
    df_x = (pd.read_csv(X_CSV_PATH, header=None)
              .dropna(how='all', axis=0)
              .dropna(how='all', axis=1))

    # 数値変換
    try:
        x = df_x.values.astype(float)
    except ValueError:
        raise ValueError("X CSV に数値以外が含まれています")

    # フィットパラメータ読み込み
    with open(PARAMS_JSON, 'r', encoding='utf-8') as f:
        params = json.load(f)
    slope = float(params.get('slope', 0.0))
    intercept = float(params.get('intercept', 0.0))
    slope_err = float(params.get('slope_err', 0.0))
    intercept_err = float(params.get('intercept_err', 0.0))

    # Y = slope * X + intercept および誤差の計算
    y = slope * x + intercept
    # 誤差伝播: σ_y = sqrt((x*σ_slope)^2 + σ_intercept^2)
    y_err = np.sqrt((x * slope_err)**2 + intercept_err**2)

    # 元の形状を保持して DataFrame 化
    df_y = pd.DataFrame(y, index=df_x.index, columns=df_x.columns)
    df_err = pd.DataFrame(y_err, index=df_x.index, columns=df_x.columns)

    # 結果を一つの DataFrame にまとめる
    # 各 X 列に対して、Y と Y_err を交互に並べる
    combined = pd.concat([df_y, df_err], axis=1)

    # 出力ディレクトリ作成
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 出力ファイル名生成：元のファイル名 + cal.csv
    base_name = os.path.splitext(os.path.basename(X_CSV_PATH))[0]
    output_path = os.path.join(OUTPUT_DIR, f"{base_name}cal.csv")

    # ヘッダー・インデックスなしで書き出し
    combined.to_csv(output_path, header=False, index=False)

    print(f"Calculated Y values and errors saved to: {output_path}")

if __name__ == '__main__':
    main()
