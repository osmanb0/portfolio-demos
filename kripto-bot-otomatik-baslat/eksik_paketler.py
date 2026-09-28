"""Bot klasorundeki .py dosyalarini tarar, kurulu olmayan disaridan paketleri
pip adlariyla bosluklu olarak yazdirir. kur.ps1 tarafindan cagrilir."""
import ast
import importlib.util
import os
import sys

ATLA = {"venv", ".venv", "env", "node_modules", ".git", "__pycache__", ".otomatik-baslat"}

# import adi -> pip paket adi (farkli olanlar)
PIP_ADI = {
    "binance": "python-binance",
    "dotenv": "python-dotenv",
    "telegram": "python-telegram-bot",
    "telebot": "pyTelegramBotAPI",
    "websocket": "websocket-client",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "bs4": "beautifulsoup4",
    "dateutil": "python-dateutil",
    "talib": "TA-Lib",
    "pandas_ta": "pandas-ta",
    "kucoin": "python-kucoin",
    "okx": "python-okx",
    "pybit": "pybit",
    "discord": "discord.py",
    "Crypto": "pycryptodome",
    "jwt": "PyJWT",
}


def main(kok):
    yerel, importlar = set(), set()
    for dp, dns, fns in os.walk(kok):
        dns[:] = [d for d in dns if d not in ATLA]
        yerel.update(dns)
        for f in fns:
            if not f.endswith(".py"):
                continue
            yerel.add(f[:-3])
            try:
                with open(os.path.join(dp, f), encoding="utf-8", errors="ignore") as fh:
                    agac = ast.parse(fh.read())
            except SyntaxError:
                continue
            for dugum in ast.walk(agac):
                if isinstance(dugum, ast.Import):
                    importlar.update(a.name.split(".")[0] for a in dugum.names)
                elif isinstance(dugum, ast.ImportFrom) and dugum.level == 0 and dugum.module:
                    importlar.add(dugum.module.split(".")[0])

    std = set(getattr(sys, "stdlib_module_names", ())) | set(sys.builtin_module_names)
    eksik = []
    for ad in sorted(importlar - std - yerel):
        try:
            bulundu = importlib.util.find_spec(ad) is not None
        except (ImportError, ValueError):
            bulundu = False
        if not bulundu:
            eksik.append(PIP_ADI.get(ad, ad))
    print(" ".join(eksik))


if __name__ == "__main__":
    main(sys.argv[1])
