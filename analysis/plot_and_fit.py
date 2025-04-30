#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# ————————————————
# ここで CSV ファイルを指定
CSV_PATH = "Hg.csv"  #
# ————————————————

def main():
    # ファイル存在チェック
    if not os.path.isfile(CSV_PATH):
        raise FileNotFoundError(f"CSV ファイルが見つかりません: {CSV_PATH}")

    # CSV をヘッダーなしで読み込む
    df = pd.read_csv(CSV_PATH, header=None)

    # 一行目を y、二行目を x として抽出
    y = df.iloc[0].values.astype(float)
    x = df.iloc[1].values.astype(float)

    # 散布図のプロット
    plt.figure()
    plt.scatter(x, y, label='Data')
    plt.xlabel('X (row 2)')
    plt.ylabel('Y (row 1)')

    # 最小二乗法による直線フィット
    slope, intercept = np.polyfit(x, y, 1)
    y_fit = slope * x + intercept

    # フィット直線のプロット
    plt.plot(x, y_fit, label=f'Fit: y = {slope:.4f} x + {intercept:.4f}')
    plt.legend()
    plt.tight_layout()
    plt.savefig('fit_plot.png')  # PNG で保存
    plt.show()

    # 傾きと切片を JSON で保存
    params = {
        'slope': float(slope),
        'intercept': float(intercept)
    }
    with open('fit_params.json', 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, indent=4)
    print(f"Saved fit parameters to fit_params.json: {params}")

if __name__ == '__main__':
    main()
