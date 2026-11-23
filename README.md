<div align="center">

# STAV (Shell Trap Anti Virus)

**Sistem Deteksi & Pemblokir Perintah Terminal Berbahaya**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Termux](https://img.shields.io/badge/Termux-Supported-blue?style=for-the-badge&logo=termux&logoColor=white)]()
[![Linux](https://img.shields.io/badge/Linux-Supported-blue?style=for-the-badge&logo=linux&logoColor=white)]()

</div>

---

## Apa itu STAV?

**STAV** adalah program keamanan berbasis CLI (Command Line Interface) yang dirancang untuk mencegah eksekusi perintah terminal yang berbahaya dan bersifat destruktif. 

STAV bekerja dengan cara menyuntikkan **"Hook"** ke dalam file `.bashrc` / `.zshrc`. Setiap kali Anda mengetik perintah berbahaya (seperti `rm -rf`, `pkill`, `reboot`, dll), STAV akan **mencegat dan memblokir** perintah tersebut sebelum dieksekusi oleh sistem.

## Fitur Utama

- **Auto-Inject Protection**: Otomatis melindungi semua terminal baru tanpa perlu konfigurasi ulang.
- **Blokir Perintah Fatal**: Mencegah penghapusan sistem (`rm -rf /`), Fork Bomb, Overwrite Disk (`dd`), dan matinya proses krusial.
- **UI Modern**: Tampilan terminal interaktif berwarna Biru-Putih dengan font kustom.
- **Log Keamanan**: Semua upaya eksekusi berbahaya dicatat ke dalam `stav_security.log`.
- **Cross-Platform**: Berjalan di Android (Termux), Linux (Ubuntu/Kali), Windows (WSL), dan MacOS.

---

## Instalasi

**1. Clone Repository:**
```bash
git clone https://github.com/IlhamCysec/stav.git
cd stav
pip install requirements.txt
python3 stav.py
