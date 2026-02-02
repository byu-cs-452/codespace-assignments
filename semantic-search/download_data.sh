#!/bin/bash
#
# download_data.sh - Download the Lex Fridman podcast embeddings dataset
#
# This script downloads the pre-computed embeddings and batch request files
# from Google Drive. The dataset is approximately 500MB.
#
# Usage:
#     chmod +x download_data.sh
#     ./download_data.sh
#

set -e

echo "📥 Downloading Lex Fridman podcast embeddings dataset..."
echo ""

# Create data directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$SCRIPT_DIR/data"
mkdir -p "$DATA_DIR"

cd "$DATA_DIR"

# Google Drive file IDs from the assignment
# Raw podcast content (batch_request files)
RAW_DATA_ID="1RXxlcUBHhE4_fQHU3qlX7Ghz5pBSvNrV"
# Embeddings
EMBEDDINGS_ID="1uCx21PhPtpnmy3ZpTc8MoR0vvokTYzrB"

echo "📦 Downloading raw podcast data..."
gdown "$RAW_DATA_ID" -O raw_data.zip

echo ""
echo "📦 Downloading embeddings..."
gdown "$EMBEDDINGS_ID" -O embeddings.zip

echo ""
echo "📂 Extracting files..."
unzip -o raw_data.zip
unzip -o embeddings.zip

echo ""
echo "🧹 Cleaning up zip files..."
rm -f raw_data.zip embeddings.zip

echo ""
echo "✅ Download complete!"
echo ""
echo "Data files are in: $DATA_DIR"
echo ""
ls -la "$DATA_DIR"
