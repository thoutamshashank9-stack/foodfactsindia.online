import os
import shutil
from huggingface_hub import hf_hub_download

DEST = "food.parquet"

def download_via_hf_hub():
    if os.path.exists(DEST):
        print(f"'{DEST}' already exists locally ({os.path.getsize(DEST)} bytes).")
        return DEST

    print("Downloading 'food.parquet' using official huggingface_hub SDK...")
    cached_path = hf_hub_download(
        repo_id="openfoodfacts/product-database",
        filename="food.parquet",
        repo_type="dataset"
    )
    print(f"Downloaded to HuggingFace cache: {cached_path}")
    print(f"Copying to local directory '{DEST}'...")
    shutil.copy(cached_path, DEST)
    print(f"✓ '{DEST}' ready! Size: {os.path.getsize(DEST)} bytes")
    return DEST

if __name__ == '__main__':
    download_via_hf_hub()
