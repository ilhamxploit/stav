import os
import re
import sys
import time
import json
import subprocess
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from pyfiglet import Figlet


if len(sys.argv) > 2 and sys.argv[1] == "--check":
    cmd = " ".join(sys.argv[2:])
    blacklist = ["rm -rf", "rm -r", "pkill", "killall", "reboot", "shutdown", "mkfs", "dd if="]
    
    if "stav.py" not in cmd and "bashrc" not in cmd:
        for b in blacklist:
            if b in cmd:
                print(f"\n\033[94m[STAV ANTIVIRUS]\033[0m \033[91m!!! PERINTAH DIBLOKIR !!!\033[0m")
                print(f"Perintah: {cmd}")
                print("\a")
                
                try:
                    with open("stav_security.log", "a") as f:
                        f.write(f"[{datetime.now()}] DIBLOKIR: {cmd}\n")
                except: pass
                
                sys.exit(1)
    sys.exit(0)

console = Console()
STATUS_FILE = ".stav_status.json"
LOG_FILE = "stav_security.log"
STAV_SCRIPT = os.path.abspath(__file__)

def get_shell_rc():
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return os.path.expanduser("~/.zshrc")
    return os.path.expanduser("~/.bashrc")

SHELL_RC = get_shell_rc()

def get_status():
    if not os.path.exists(STATUS_FILE):
        return False
    try:
        with open(STATUS_FILE, 'r') as f:
            return json.load(f).get("active", False)
    except:
        return False

def set_status(status: bool):
    with open(STATUS_FILE, 'w') as f:
        json.dump({"active": status}, f)

def show_banner():
    os.system('clear' if os.name == 'posix' else 'cls')
    try:
        f = Figlet(font="bloody")
        ascii_art = f.renderText("STAV")
    except:
        ascii_art = "STAV\n"

    banner_content = f"[bold bright_blue]{ascii_art}[/bold bright_blue]"
    banner_content += "\n[white]Shell Trap Anti Virus[/white]"
    banner_content += "\n[blue]Developed by:[/blue] [bold white]ilhamxploit[/bold white] [blue]| By Communty Byte Hunters[/blue]"
    
    panel = Panel(
        banner_content,
        border_style="bright_blue",
        title="[bold white]BYTE HUNTERS[/bold white]",
        subtitle="[bold white]BYTE HUNTERS[/bold white]",
        padding=(1, 2),
        style="on black"
    )
    console.print(panel)
    console.print()

def install_global():
    hook_code = f"""
# STAV_GLOBAL_HOOK
# Timpa fungsi-fungsi berbahaya dengan pengecekan STAV
rm() {{
    python3 "{STAV_SCRIPT}" --check "rm $@"
    if [ $? -eq 0 ]; then command rm "$@"; fi
}}
pkill() {{
    python3 "{STAV_SCRIPT}" --check "pkill $@"
    if [ $? -eq 0 ]; then command pkill "$@"; fi
}}
killall() {{
    python3 "{STAV_SCRIPT}" --check "killall $@"
    if [ $? -eq 0 ]; then command killall "$@"; fi
}}
shutdown() {{
    python3 "{STAV_SCRIPT}" --check "shutdown $@"
    if [ $? -eq 0 ]; then command shutdown "$@"; fi
}}
# STAV_END_HOOK
"""
    try:
        content = ""
        if os.path.exists(SHELL_RC):
            with open(SHELL_RC, 'r') as f:
                content = f.read()
        
        content = re.sub(r'# STAV_GLOBAL_HOOK.*?# STAV_END_HOOK\n?', '', content, flags=re.DOTALL)
        
        with open(SHELL_RC, 'w') as f:
            f.write(content.strip() + "\n\n" + hook_code)
            
        return True
    except Exception as e:
        console.print(f"[bold white][!] Gagal memasang: {e}[/bold white]")
        return False

def uninstall_global():
    if not os.path.exists(SHELL_RC):
        return
    try:
        with open(SHELL_RC, 'r') as f:
            content = f.read()
        content = re.sub(r'# STAV_GLOBAL_HOOK.*?# STAV_END_HOOK\n?', '', content, flags=re.DOTALL)
        with open(SHELL_RC, 'w') as f:
            f.write(content.strip() + "\n")
        console.print("[bold blue][+] Berhasil dihapus.[/bold blue]")
    except Exception as e:
        console.print(f"[bold white][!] Gagal: {e}[/bold white]")

def show_menu():
    status_str = "[bold blue]AKTIF[/bold blue]" if get_status() else "[bold white]NONAKTIF[/bold white]"
    terpasang = "# STAV_GLOBAL_HOOK" in open(SHELL_RC).read() if os.path.exists(SHELL_RC) else False
    install_str = "[bold blue]TERPASANG[/bold blue]" if terpasang else "[bold white]BELUM[/bold white]"
    
    menu_text = (
        f"[bold white]Status Proteksi:[/bold white] {status_str}\n"
        f"[bold white]Terminal Global:[/bold white] {install_str}\n\n"
        "[bold white][1][/bold white] [blue]Aktifkan STAV & Pasang Auto-Protect[/blue]\n"
        "[bold white][2][/bold white] [blue]Nonaktifkan STAV[/blue]\n"
        "[bold white][3][/bold white] [blue]Hapus Proteksi [/blue]\n"
        "[bold white][4][/bold white] [blue]Lihat Log[/blue]\n"
        "[bold white][0][/bold white] [blue]Keluar[/blue]"
    )
    console.print(Panel(menu_text, title="[bold white]MENU KONTROL[/bold white]", border_style="blue"))

def lihat_log():
    if not os.path.exists(LOG_FILE):
        console.print("[bold white]Log kosong.[/bold white]")
    else:
        with open(LOG_FILE, 'r') as f:
            logs = f.readlines()
        table = Table(title="[bold white]Log Keamanan[/bold white]", border_style="bright_blue")
        table.add_column("Log", style="white")
        for line in logs[-10:]:
            table.add_row(line.strip())
        console.print(table)
    Prompt.ask("\n[bold white]Tekan Enter...[/bold white]", default="")

if __name__ == "__main__":
    while True:
        show_banner()
        show_menu()
        pilihan = Prompt.ask("\n[bold blue]»[/bold blue] [white]Pilih[/white]")
        
        if pilihan == '1':
            set_status(True)
            if install_global():
                console.print("[bold blue][+] Berhasil! Hook terpasang di .bashrc.[/bold blue]")
                console.print("[white]Menerapkan proteksi ke terminal saat ini (Auto-Inject)...[/white]")
                
                try:

                    subprocess.run(f"source {SHELL_RC}", shell=True, executable="/bin/bash")
                    os.system(f"exec bash -c 'source {SHELL_RC}; exec bash'")
                except Exception as e:
                    console.print(f"[bold white][!] Auto-inject gagal, silakan ketik 'source ~/.bashrc'[/bold white]")
            time.sleep(2)
        elif pilihan == '2':
            set_status(False)
            console.print("[bold white]STAV Nonaktif.[/bold white]")
            time.sleep(1.5)
        elif pilihan == '3':
            uninstall_global()
            Prompt.ask("Enter...")
        elif pilihan == '4':
            lihat_log()
        elif pilihan == '0':
            break
