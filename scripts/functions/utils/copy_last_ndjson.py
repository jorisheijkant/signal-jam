import shutil
from pathlib import Path
import time


def copy_last_ndjson(output_folder, name_folder_friendly):
    download_folder = Path.home() / "Downloads"
    time.sleep(2)  # Give download time to start

    max_wait = 60
    downloaded_file = None

    for _ in range(max_wait):
        ndjson_files = list(download_folder.glob("*.ndjson"))
        if ndjson_files:
            downloaded_file = max(ndjson_files, key=lambda f: f.stat().st_mtime)
            initial_size = downloaded_file.stat().st_size
            time.sleep(0.5)
            if downloaded_file.exists() and downloaded_file.stat().st_size == initial_size:
                break
        time.sleep(1)

    if downloaded_file and downloaded_file.exists():
        target_filename = f"{name_folder_friendly}_{int(time.time())}.ndjson"
        target_path = Path(output_folder) / target_filename
        shutil.move(str(downloaded_file), str(target_path))
        print(f"Downloaded file moved to {target_path}")
        return target_path
    else:
        print("Warning: Could not find downloaded file in Downloads folder")
        return None
