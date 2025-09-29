#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$ROOT/tmp"
DATA_DIR="$ROOT/data/chest-xray"

mkdir -p "$TMP_DIR" "$DATA_DIR"

# Kaggle CLI 설치 확인
if ! command -v kaggle >/dev/null 2>&1; then
  echo "[ERROR] Kaggle CLI not found. Please activate venv and install with 'pip install kaggle'"
  exit 1
fi

echo "[1/3] Downloading from Kaggle..."
ZIP_FILE="$TMP_DIR/chest-xray-pneumonia.zip"
kaggle datasets download -d paultimothymooney/chest-xray-pneumonia -p "$TMP_DIR" -f chest-xray-pneumonia.zip

echo "[2/3] Unzipping..."
unzip -q -o "$ZIP_FILE" -d "$DATA_DIR"
rm -f "$ZIP_FILE"

# MacOS 숨김파일(.DS_Store 등) 제거
find "$DATA_DIR" -type f -name ".*" -delete

echo "[3/3] Done. Data at: $DATA_DIR"
echo "   Structure (top 2 levels):"
find "$DATA_DIR" -maxdepth 2 -type d -print
