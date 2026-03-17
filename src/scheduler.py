"""
scheduler.py — Ciclo de coleta contínua a cada hora.

Uso:
  PYTHONUNBUFFERED=1 uv run src/scheduler.py &

A cada 60 minutos:
  1. collector.py --incremental  (últimas 2h)
  2. analyzer.py                 (artigos novos)
  3. scorer.py                   (recalcula tudo)
"""

import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

SRC_DIR  = Path(__file__).parent
INTERVAL = 3600  # segundos


def run(script: str, *args) -> bool:
    """Roda script Python no mesmo venv. Retorna True se exit 0."""
    cmd = [sys.executable, str(SRC_DIR / script), *args]
    env = {**os.environ, "PYTHONUNBUFFERED": "1", "PYTHONUTF8": "1"}
    result = subprocess.run(cmd, env=env)
    return result.returncode == 0


def fmt_time(dt: datetime) -> str:
    return dt.strftime("%H:%M UTC")


def main():
    print("=== NARRATIVE TRACKER — Scheduler ===")
    print(f"Intervalo: {INTERVAL // 60} minutos")
    print(f"Ctrl+C para parar.\n")

    cycle = 0
    while True:
        cycle += 1
        now = datetime.now(timezone.utc)
        next_run = now + timedelta(seconds=INTERVAL)
        print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')} UTC] ─── Ciclo #{cycle} ───")

        print("  [1/3] Coletando artigos recentes (últimas 2h)...")
        ok1 = run("collector.py", "--incremental")

        print("  [2/3] Analisando novos artigos...")
        ok2 = run("analyzer.py")

        print("  [3/3] Recalculando scores e vocabulário...")
        ok3 = run("scorer.py")

        status = "✓" if (ok1 and ok2 and ok3) else "⚠ (alguns passos falharam)"
        print(f"  {status} Ciclo #{cycle} concluído — próxima coleta às {fmt_time(next_run)}\n")

        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScheduler encerrado.")
