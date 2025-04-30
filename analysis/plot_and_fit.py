#!/usr/bin/env python3
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# ————————————————
# ここで CSV ファイルを指定
CSV_PATH = "../data/Hg.csv"  # ← 実際のパス・ファイル名に書き換えてください
# ————————————————


def main():
    # ファイル存在チェック
    if not os.path.isfile(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH, header=None).dropna(how='all', axis=0).dropna(how='all', axis=1)
    if df.shape[1] < 2:
        raise ValueError(f"CSV must have at least 2 columns: found {df.shape[1]}")


    y = df.iloc[:, 0].astype(float).values
    x = df.iloc[:, 1].astype(float).values

    margin = 20
    x_data_min, x_data_max = x.min(), x.max()
    x_plot_min = x_data_min - margin
    x_plot_max = x_data_max + margin

    fig, ax = plt.subplots()

    # 散布図プロット
    ax.scatter(x, y, label='Data')

    # 最小二乗法による直線フィット＋共分散行列取得
    (slope, intercept), cov = np.polyfit(x, y, 1, cov=True)
    slope_err = np.sqrt(cov[0, 0])
    intercept_err = np.sqrt(cov[1, 1])

    # 直線をグラフの端まで伸ばす
    x_line = np.linspace(x_plot_min, x_plot_max, 100)
    y_line = slope * x_line + intercept
    ax.plot(x_line, y_line,
            label=f'y = {slope:.4f}±{slope_err:.4f} x + {intercept:.4f}±{intercept_err:.4f}')

    # X 軸範囲設定
    ax.set_xlim(x_plot_min, x_plot_max)

    # 軸ラベル（英語）
    ax.set_xlabel('Position $x$ [mm]')
    ax.set_ylabel('Wavelength $\\lambda$ [nm]')

    # 目盛り設定：4辺とも内向きに
    ax.tick_params(axis='both', which='both',
                   top=True, bottom=True, left=True, right=True,
                   direction='in')
    ax.tick_params(labeltop=False, labelright=False,
                   labelbottom=True, labelleft=True)

    ax.legend()
    fig.tight_layout()
    fig.savefig('../result/fit_plot.png', dpi=300)
    plt.show()

    # フィットパラメータ JSON 出力
    params = {
        'slope': float(slope),
        'slope_err': float(slope_err),
        'intercept': float(intercept),
        'intercept_err': float(intercept_err)
    }
    with open('fit_params.json', 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, indent=4)

    print("Fit results:")
    print(f"  Slope     = {slope:.6f} ± {slope_err:.6f}")
    print(f"  Intercept = {intercept:.6f} ± {intercept_err:.6f}")
    print("→ fit_params.json saved.")


if __name__ == '__main__':
    main()
