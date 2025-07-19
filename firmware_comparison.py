import os
import subprocess
import tempfile
import filecmp
import hashlib
import argparse

def extract_npk(file_path, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    try:
        subprocess.run(['binwalk', '-e', '-C', extract_to, file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Extraction failed: {e}")
        exit(1)

def file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def compare_dirs(dir1, dir2):
    result = {
        "added": [],
        "removed": [],
        "changed": [],
        "unchanged": []
    }
    comp = filecmp.dircmp(dir1, dir2)

    result["added"].extend(comp.right_only)
    result["removed"].extend(comp.left_only)

    for common_file in comp.common_files:
        file1 = os.path.join(dir1, common_file)
        file2 = os.path.join(dir2, common_file)
        if file_hash(file1) != file_hash(file2):
            result["changed"].append(common_file)
        else:
            result["unchanged"].append(common_file)

    for sub_dir in comp.common_dirs:
        sub_result = compare_dirs(
            os.path.join(dir1, sub_dir),
            os.path.join(dir2, sub_dir)
        )
        for key in result:
            result[key].extend([os.path.join(sub_dir, f) for f in sub_result[key]])

    return result

def main():
    parser = argparse.ArgumentParser(description="Compare two RouterOS .npk firmware files using binwalk")
    parser.add_argument('file1', help="Path to first .npk file")
    parser.add_argument('file2', help="Path to second .npk file")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        print("[*] Extracting first file...")
        extract_npk(args.file1, tmp1)
        print("[*] Extracting second file...")
        extract_npk(args.file2, tmp2)

        # Binwalk extracts into _<filename>.extracted folders
        extracted_dirs = [d for d in os.listdir(tmp1) if d.endswith('.extracted')]
        extracted1 = os.path.join(tmp1, extracted_dirs[0]) if extracted_dirs else tmp1

        extracted_dirs = [d for d in os.listdir(tmp2) if d.endswith('.extracted')]
        extracted2 = os.path.join(tmp2, extracted_dirs[0]) if extracted_dirs else tmp2

        print("[*] Comparing extracted contents...")
        comparison = compare_dirs(extracted1, extracted2)

        print("\n--- Comparison Results ---")
        for key in comparison:
            print(f"\n{key.upper()}:")
            for item in comparison[key]:
                print(f"  {item}")

if __name__ == "__main__":
    main()
