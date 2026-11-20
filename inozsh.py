#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
import time

# Warna ANSI untuk tampilan terminal
G = "\033[92m"  # Hijau
Y = "\033[93m"  # Kuning
C = "\033[96m"  # Cyan
R = "\033[91m"  # Merah
B = "\033[1m"   # Bold
W = "\033[0m"   # Reset

HOME = os.path.expanduser("~")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")
TERMUX_DIR = os.path.join(HOME, ".termux")


def clear():
    os.system("clear")


def banner():
    clear()
    print(f"{C}{B}==========================================={W}")
    print(f"{G}{B}        INOZSH - TERMUX THEME SETUP        {W}")
    print(f"{C}{B}==========================================={W}\n")


def run_cmd(cmd, desc):
    print(f"{C}[*]{W} {desc}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"{G}[✓]{W} Selesai: {desc}\n")
        return True
    except subprocess.CalledProcessError:
        print(f"{R}[✗]{W} Gagal menjalankan: {desc}\n")
        return False


def step_packages():
    return run_cmd(
        "pkg update && pkg upgrade -y && pkg install zsh git curl -y",
        "Memperbarui paket & menginstal Zsh, Git, Curl",
    )


def step_ohmyzsh():
    omz_dir = os.path.join(HOME, ".oh-my-zsh")
    if os.path.exists(omz_dir):
        print(f"{Y}[!]{W} Oh My Zsh sudah terpasang, melewati tahap ini.\n")
        return True
    # Flag --unattended wajib agar installer tidak menghentikan skrip Python
    return run_cmd(
        'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended',
        "Menginstal Oh My Zsh",
    )


def step_p10k():
    custom_dir = os.path.join(HOME, ".oh-my-zsh", "custom", "themes", "powerlevel10k")
    if os.path.exists(custom_dir):
        print(f"{Y}[!]{W} Tema Powerlevel10k sudah ada, melewati clone.\n")
        return True
    return run_cmd(
        f"git clone --depth=1 https://github.com/romkatv/powerlevel10k.git {custom_dir}",
        "Mengunduh tema Powerlevel10k",
    )


def step_font():
    os.makedirs(TERMUX_DIR, exist_ok=True)
    local_font = os.path.join(CONFIG_DIR, "font.ttf")
    target_font = os.path.join(TERMUX_DIR, "font.ttf")

    if os.path.exists(local_font):
        shutil.copy2(local_font, target_font)
        print(f"{G}[✓]{W} Menggunakan font kustom dari folder config/font.ttf\n")
    else:
        url = "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf"
        run_cmd(f'curl -fsSL -o "{target_font}" "{url}"', "Mengunduh Nerd Font (MesloLGS NF)")

    run_cmd("termux-reload-settings", "Memuat ulang pengaturan tampilan Termux")


def step_apply_config():
    print(f"{C}[*]{W} Menerapkan file konfigurasi tema InoZsh...")
    os.makedirs(TERMUX_DIR, exist_ok=True)

    files_map = {
        "zshrc": os.path.join(HOME, ".zshrc"),
        "p10k.zsh": os.path.join(HOME, ".p10k.zsh"),
        "colors.properties": os.path.join(TERMUX_DIR, "colors.properties"),
    }

    applied = 0
    for src_name, dest_path in files_map.items():
        src_path = os.path.join(CONFIG_DIR, src_name)
        if os.path.exists(src_path):
            if os.path.exists(dest_path):
                shutil.copy2(dest_path, dest_path + ".bak")
            shutil.copy2(src_path, dest_path)
            print(f"    {G}->{W} {src_name} berhasil dipasang")
            applied += 1

    if applied == 0:
        print(f"{Y}[!]{W} Folder 'config/' kosong atau tidak ditemukan. Mengaktifkan P10k default...")
        zshrc_path = os.path.join(HOME, ".zshrc")
        if os.path.exists(zshrc_path):
            with open(zshrc_path, "r") as f:
                content = f.read()
            content = content.replace('ZSH_THEME="robbyrussell"', 'ZSH_THEME="powerlevel10k/powerlevel10k"')
            with open(zshrc_path, "w") as f:
                f.write(content)

    run_cmd("chsh -s zsh", "Menjadikan Zsh sebagai shell default")
    run_cmd("termux-reload-settings", "Menerapkan skema warna & font Termux")


def export_my_theme():
    """Mengambil konfigurasi dari Termux Anda saat ini ke folder config/ untuk dibagikan."""
    banner()
    print(f"{Y}[*] Mengemas konfigurasi Zsh & Termux Anda ke folder 'config/'...{W}\n")
    os.makedirs(CONFIG_DIR, exist_ok=True)

    sources = {
        os.path.join(HOME, ".zshrc"): "zshrc",
        os.path.join(HOME, ".p10k.zsh"): "p10k.zsh",
        os.path.join(TERMUX_DIR, "font.ttf"): "font.ttf",
        os.path.join(TERMUX_DIR, "colors.properties"): "colors.properties",
    }

    count = 0
    for src, dst_name in sources.items():
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(CONFIG_DIR, dst_name))
            print(f"{G}[✓]{W} Berhasil menyalin: {src} -> config/{dst_name}")
            count += 1
        else:
            print(f"{Y}[-]{W} Dilewati (tidak ada): {src}")

    print(f"\n{G}{B}Selesai! {count} file konfigurasi siap dibagikan bersama inozsh.py.{W}")
    input("\nTekan Enter untuk kembali ke menu...")


def full_install():
    banner()
    confirm = input(f"{Y}Lanjutkan instalasi penuh InoZsh? (y/n): {W}").strip().lower()
    if confirm != "y":
        return

    print()
    if not step_packages():
        return
    if not step_ohmyzsh():
        return
    step_p10k()
    step_font()
    step_apply_config()

    print(f"{G}{B}==========================================={W}")
    print(f"{G}{B}   INSTALASI INOZSH SELESAI SEMPURNA!      {W}")
    print(f"{G}{B}==========================================={W}")
    print(f"Ketik {C}exec zsh{W} atau restart Termux untuk melihat hasilnya.\n")
    sys.exit(0)


def main():
    while True:
        banner()
        print("Pilih menu instalasi:")
        print(f"  {G}[1]{W} Install Full Setup (Paket + OhMyZsh + P10k + Font + Tema)")
        print(f"  {G}[2]{W} Terapkan Konfigurasi Tema Saja (Dari folder config/)")
        print(f"  {C}[3]{W} Kemas Tema Saya (Backup config HP ini untuk dibagikan)")
        print(f"  {R}[0]{W} Keluar\n")

        choice = input(f"{B}Masukkan pilihan [0-3]: {W}").strip()

        if choice == "1":
            full_install()
        elif choice == "2":
            banner()
            step_font()
            step_apply_config()
            input("\nTekan Enter untuk kembali ke menu...")
        elif choice == "3":
            export_my_theme()
        elif choice == "0":
            print("Keluar dari installer.")
            break
        else:
            print(f"{R}Pilihan tidak valid!{W}")
            time.sleep(1)


if __name__ == "__main__":
    main()

