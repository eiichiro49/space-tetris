#!/usr/bin/env python3
"""
NEON TETRIS - 背景画像ジェネレータ (OpenAI Images API)
========================================================
このスクリプトを実行すると、OpenAI の画像生成APIでネオン・サイバーパンク調の
背景画像を作り、images/background.png として保存します。
ゲーム(index.html)は images/background.png があれば自動で読み込みます。

■ 使い方
  1. APIキーを環境変数にセット（キーはこのスクリプトには書きません）
       macOS / Linux:   export OPENAI_API_KEY="sk-..."
       Windows (PS)  :   $env:OPENAI_API_KEY="sk-..."
  2. ライブラリを入れる:   pip install openai
  3. このフォルダで実行  :   python generate_images.py

  ※ キーはあなたの端末の環境変数からのみ読み込まれ、ファイルには保存されません。
"""

import os
import sys
import base64

PROMPT = (
    "A vertical deep-space background for a Tetris arcade game. "
    "Starry cosmic night sky, distant glowing nebula in cyan, magenta and violet, "
    "scattered bright stars and faint galaxies, a small distant planet, "
    "subtle aurora-like glow, dreamy sci-fi atmosphere, smooth gradients, "
    "no text, no characters, no UI, dark uncluttered center area "
    "so the falling game blocks stay clearly readable."
)

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
OUT_PATH = os.path.join(OUT_DIR, "background.png")
SIZE = "1024x1536"  # 縦長 (盤面は縦長なので)


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "✗ 環境変数 OPENAI_API_KEY が見つかりません。\n"
            '  例: export OPENAI_API_KEY="sk-..."  を実行してから再度お試しください。'
        )

    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("✗ openai ライブラリが必要です。  pip install openai  を実行してください。")

    client = OpenAI()  # APIキーは環境変数から自動取得
    os.makedirs(OUT_DIR, exist_ok=True)

    print("⏳ 背景画像を生成中... (数十秒かかることがあります)")
    try:
        result = client.images.generate(
            model="gpt-image-1",
            prompt=PROMPT,
            size=SIZE,
            n=1,
        )
    except Exception as e:
        sys.exit(f"✗ 画像生成に失敗しました: {e}")

    b64 = result.data[0].b64_json
    if not b64:
        # 一部応答は URL を返す場合がある
        url = getattr(result.data[0], "url", None)
        if url:
            import urllib.request
            urllib.request.urlretrieve(url, OUT_PATH)
            print(f"✓ 保存しました: {OUT_PATH}")
            return
        sys.exit("✗ 画像データを取得できませんでした。")

    with open(OUT_PATH, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"✓ 保存しました: {OUT_PATH}")
    print("  index.html を開くと背景に反映されます。")


if __name__ == "__main__":
    main()
