from __future__ import annotations

from datetime import datetime

import streamlit as st

from .runner import run_once


st.set_page_config(page_title="Daily Stock Gem Bot", page_icon="📈", layout="wide")


def main() -> None:
    st.title("Daily Stock Gem Bot")
    st.caption("毎日の注目銘柄スクリーニングをWebアプリで確認")

    col1, col2 = st.columns([1, 2])
    with col1:
        use_mock = st.toggle("モックデータを使う", value=False)
        run_button = st.button("スクリーニング実行", type="primary")

    if run_button:
        with st.spinner("データ取得と分析を実行中..."):
            try:
                report, picks = run_once(use_mock=use_mock)
            except Exception as exc:
                st.error(f"実行に失敗しました: {exc}")
                return

        st.success(f"更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if picks:
            rows = [
                {
                    "symbol": p.symbol,
                    "score": round(p.score, 2),
                    "price": round(p.snapshot.price, 2),
                    "change_pct": round(p.snapshot.change_pct, 2),
                    "volume": p.snapshot.volume,
                    "avg_volume": p.snapshot.avg_volume,
                    "reason": p.reason,
                }
                for p in picks
            ]
            st.subheader("候補銘柄")
            st.dataframe(rows, use_container_width=True)
        else:
            st.info("条件に一致する銘柄はありませんでした。")

        st.subheader("レポート")
        st.code(report)
    else:
        st.info("左側のボタンからスクリーニングを実行してください。")


if __name__ == "__main__":
    main()
