const demoUniverse = [
  { symbol: "AAPL", price: 191.2, changePct: 1.8, volume: 82400000, avgVolume: 55000000, marketCapB: 2960 },
  { symbol: "MSFT", price: 417.4, changePct: 0.9, volume: 28400000, avgVolume: 23000000, marketCapB: 3110 },
  { symbol: "NVDA", price: 894.5, changePct: 3.6, volume: 61300000, avgVolume: 35500000, marketCapB: 2205 },
  { symbol: "AMZN", price: 178.2, changePct: 2.2, volume: 40200000, avgVolume: 35500000, marketCapB: 1850 },
  { symbol: "META", price: 502.8, changePct: 1.2, volume: 22200000, avgVolume: 18600000, marketCapB: 1290 },
  { symbol: "GOOGL", price: 153.9, changePct: 0.7, volume: 28700000, avgVolume: 26200000, marketCapB: 1940 },
  { symbol: "TSLA", price: 183.1, changePct: -0.6, volume: 117000000, avgVolume: 86500000, marketCapB: 585 },
  { symbol: "AVGO", price: 1354.0, changePct: 2.8, volume: 4100000, avgVolume: 3100000, marketCapB: 624 },
  { symbol: "AMD", price: 172.7, changePct: 1.9, volume: 76800000, avgVolume: 41200000, marketCapB: 279 },
  { symbol: "NFLX", price: 613.4, changePct: 1.4, volume: 5900000, avgVolume: 4100000, marketCapB: 266 },
  { symbol: "PLTR", price: 25.5, changePct: 4.4, volume: 95600000, avgVolume: 43800000, marketCapB: 52 }
];

const resultsEl = document.getElementById("results");
const reportTextEl = document.getElementById("reportText");
const updatedAtEl = document.getElementById("updatedAt");

const controls = {
  topN: document.getElementById("topN"),
  minPrice: document.getElementById("minPrice"),
  minCap: document.getElementById("minCap"),
  minVolRatio: document.getElementById("minVolRatio")
};

document.getElementById("runButton").addEventListener("click", runScreening);
document.getElementById("regenButton").addEventListener("click", regenerateAndRun);

function regenerateAndRun() {
  for (const row of demoUniverse) {
    const drift = (Math.random() - 0.5) * 2.4;
    row.changePct = Number((row.changePct + drift).toFixed(2));
    row.volume = Math.max(1000, Math.round(row.volume * (0.82 + Math.random() * 0.4)));
    row.price = Number((row.price * (1 + drift / 100)).toFixed(2));
  }
  runScreening();
}

function scoreRow(row) {
  const volumeRatio = row.volume / row.avgVolume;
  return volumeRatio * 45 + Math.max(row.changePct, 0) * 7;
}

function runScreening() {
  const cfg = {
    topN: Number(controls.topN.value || 8),
    minPrice: Number(controls.minPrice.value || 0),
    minCap: Number(controls.minCap.value || 0),
    minVolRatio: Number(controls.minVolRatio.value || 1)
  };

  const picks = demoUniverse
    .filter((row) => row.price >= cfg.minPrice)
    .filter((row) => row.marketCapB >= cfg.minCap)
    .filter((row) => row.volume / row.avgVolume >= cfg.minVolRatio)
    .map((row) => ({ ...row, score: scoreRow(row), volumeRatio: row.volume / row.avgVolume }))
    .sort((a, b) => b.score - a.score)
    .slice(0, cfg.topN);

  renderResults(picks);
  renderReport(picks, cfg);
  updatedAtEl.textContent = new Date().toLocaleString("ja-JP");
}

function renderResults(picks) {
  if (!picks.length) {
    resultsEl.innerHTML = '<p class="meta">条件に一致する銘柄はありません。</p>';
    return;
  }

  resultsEl.innerHTML = picks
    .map(
      (row, i) => `
      <article class="result-item">
        <div>
          <div class="symbol">${i + 1}. ${row.symbol}</div>
          <div class="meta">価格 $${row.price.toFixed(2)} / 前日比 ${row.changePct > 0 ? "+" : ""}${row.changePct.toFixed(
            2
          )}% / 出来高倍率 ${row.volumeRatio.toFixed(2)}x</div>
        </div>
        <div class="score">Score ${row.score.toFixed(1)}</div>
      </article>
    `
    )
    .join("");
}

function renderReport(picks, cfg) {
  if (!picks.length) {
    reportTextEl.textContent = "本日の条件に一致する銘柄はありませんでした。";
    return;
  }

  const lines = [];
  lines.push(`[Daily Stock Picks] ${new Date().toLocaleString("ja-JP")}`);
  lines.push("");
  lines.push(
    `条件: topN=${cfg.topN}, minPrice=${cfg.minPrice}, minCap=${cfg.minCap}B, minVolRatio=${cfg.minVolRatio}`
  );
  lines.push("");

  picks.forEach((row, i) => {
    lines.push(
      `${i + 1}. ${row.symbol} | score ${row.score.toFixed(1)} | 出来高倍率 ${row.volumeRatio.toFixed(
        2
      )}x | 前日比 ${row.changePct > 0 ? "+" : ""}${row.changePct.toFixed(2)}%`
    );
  });

  lines.push("");
  lines.push("注意: 本情報は投資助言ではありません。最終判断はご自身でお願いします。");

  reportTextEl.textContent = lines.join("\n");
}

runScreening();
