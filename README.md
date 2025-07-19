# Firmware Comparison Tool

Python-based RouterOS firmware diff tool that extracts two `.npk` packages and recursively compares their contents, identifying added, removed, changed, and unchanged files.

---

## Summary

`firmware_comparison` automates the process of unpacking two MikroTik RouterOS firmware packages, computing SHA-256 hashes on each file, and reporting exactly what’s been added, removed, or modified between versions—making QA and security audits fast and reliable.

---

## Key Features

- **Automated extraction** of `.npk` packages via [Binwalk](https://github.com/ReFirmLabs/binwalk)  
- **SHA-256 hashing** to detect binary-level changes  
- **Recursive directory comparison** using `filecmp.dircmp`  
- **Four result categories**:  
  - **Added** files  
  - **Removed** files  
  - **Changed** files  
  - **Unchanged** files  
- **Robust** handling of nested archives (SquashFS, CramFS, etc.)  
- **Zero external Python dependencies** (only Python stdlib + Binwalk)

---

## Supported Firmware

- MikroTik RouterOS `.npk` packages for **all** CPU architectures

---

## Prerequisites

- **Python** ≥ 3.6  
- **Binwalk** installed and on your `PATH`  
  ```bash
  # Debian/Ubuntu
  sudo apt-get update && sudo apt-get install binwalk

  # Or via pip (requires libmagic/dev headers)
  pip install binwalk

## Usage

python3 firmware_comparison.py file1.npk file2.npk
