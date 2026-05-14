#!/usr/bin/env python3
# Kodların buradan aşağıda devam etmeli...
import sys
import subprocess
import os
import locale
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QStackedWidget,
                             QComboBox, QGridLayout, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class ArchiveOSWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.os_name = "ArchiveOS"
        self.showFullScreen()

        screen = QApplication.primaryScreen().size()
        self.sw = screen.width()
        self.sh = screen.height()

        self.current_theme = "dark"
        self.high_contrast = False

        try:
            sys_lang = locale.getdefaultlocale()[0]
            self.lang = "tr" if sys_lang and sys_lang.startswith("tr") else "en"
        except:
            self.lang = "en"

        self.texts = {
            "en": {
                "next": "Next", "back": "Back", "finish": "Finish",
                "welcome": f"Welcome to {self.os_name}",
                "welcome_sub": "Let's configure your system.",
                "display": "Visual Comfort", "display_sub": "Adjust visibility settings.",
                "contrast_btn": "Enable High Contrast", "contrast_on": "Contrast Active",
                "apps": "Software Center", "apps_sub": "Pick essential tools.",
                "tools": "Maintenance", "tools_sub": "Keep system clean.",
                "drivers": "Hardware", "drivers_sub": "Check for updates.",
                "driver_btn": "Driver Manager",
                "theme": "Personalization", "theme_sub": "Select desktop style.",
                "archive": "Liquid Glass", "light": "Breeze Light", "dark": "Breeze Dark",
                "goodbye": "You're Ready!", "goodbye_sub": "Setup complete.",
                "app_list": [
                    ("Firefox", "flatpak install flathub org.mozilla.firefox"),
                    ("VLC", "flatpak install flathub org.videolan.VLC"),
                    ("VS Code", "flatpak install flathub com.visualstudio.code"),
                    ("Discord", "flatpak install flathub com.discordapp.Discord"),
                    ("Wine", "sudo apt update && sudo apt install wine"),
                    ("Steam", "flatpak install flathub com.valvesoftware.Steam")
                ],
                "tool_list": [
                    ("cache", "sudo apt clean && sudo apt autoremove", "Clean"),
                    ("system", "sudo apt update && sudo apt upgrade && aos-update-manager", "Update"),
                    ("Flatpak", "flatpak update", "Update")
                ]
            },
            "tr": {
                "next": "İleri", "back": "Geri", "finish": "Bitir",
                "welcome": f"{self.os_name}'e Hoş Geldiniz",
                "welcome_sub": "Sistemi birlikte yapılandıralım.",
                "display": "Görsel Konfor", "display_sub": "Görünürlük ayarları.",
                "contrast_btn": "Yüksek Karşıtlığı Aç", "contrast_on": "Karşıtlık Aktif",
                "apps": "Yazılım Merkezi", "apps_sub": "Temel araçları seç.",
                "tools": "Sistem Bakımı", "tools_sub": "ArchiveOS'u temiz tut.",
                "drivers": "Donanım", "drivers_sub": "Sürücüleri tara.",
                "driver_btn": "Sürücü Yöneticisi",
                "theme": "Kişiselleştirme", "theme_sub": "Masaüstü stilini seç.",
                "archive": "Liquid Glass", "light": "Breeze Açık", "dark": "Breeze Koyu",
                "goodbye": "Hazırsın!", "goodbye_sub": "Kurulum bitti.",
                "app_list": [
                    ("Firefox", "flatpak install flathub org.mozilla.firefox"),
                    ("VLC", "flatpak install flathub org.videolan.VLC"),
                    ("VS Code", "flatpak install flathub com.visualstudio.code"),
                    ("Discord", "flatpak install flathub com.discordapp.Discord"),
                    ("Wine", "sudo apt update && sudo apt install wine"),
                    ("Steam", "flatpak install flathub com.valvesoftware.Steam")
                ],
                "tool_list": [
                    ("gecici dosyalar", "sudo apt clean && sudo apt autoremove", "Temizlensin mi"),
                    ("güncelle", "sudo apt update && sudo apt upgrade && aos-update-manager", "eminmisiniz"),
                    ("Flatpak", "flatpak update", "Güncelle")
                ]
            }
        }

        self.init_ui()
        self.update_theme_style()

    def get_font(self, rel_size, bold=False):
        f = QFont("Sans")
        f.setPointSizeF(self.sw * rel_size)
        if bold: f.setWeight(QFont.Weight.Bold)
        return f

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        margin = int(self.sw * 0.08)
        self.main_layout.setContentsMargins(margin, 20, margin, 20)

        header = QHBoxLayout()
        self.lang_box = QComboBox()
        self.lang_box.addItems(["English", "Türkçe"])
        self.lang_box.setCurrentIndex(1 if self.lang == "tr" else 0)
        self.lang_box.setFixedSize(100, 30)
        self.lang_box.currentIndexChanged.connect(self.manual_lang_change)
        header.addStretch(); header.addWidget(self.lang_box)
        self.main_layout.addLayout(header)

        self.pages = QStackedWidget()
        self.pages.addWidget(self.page_welcome())
        self.pages.addWidget(self.page_theme())
        self.pages.addWidget(self.page_display())
        self.pages.addWidget(self.page_apps())
        self.pages.addWidget(self.page_tools())
        self.pages.addWidget(self.page_drivers())
        self.pages.addWidget(self.page_goodbye())
        self.main_layout.addWidget(self.pages)

        self.dot_layout = QHBoxLayout()
        self.dot_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dots = []
        for i in range(7):
            dot = QLabel("•")
            dot.setStyleSheet("color: gray; font-size: 14px;")
            self.dots.append(dot)
            self.dot_layout.addWidget(dot)
        self.main_layout.addLayout(self.dot_layout)
        self.main_layout.addSpacing(10)

        nav = QHBoxLayout()
        self.btn_back = QPushButton()
        self.btn_back.setFixedSize(110, 38)
        self.btn_back.setFont(self.get_font(0.009, True))
        self.btn_back.clicked.connect(lambda: self.navigate(-1))

        self.btn_next = QPushButton()
        self.btn_next.setFixedSize(110, 38)
        self.btn_next.setFont(self.get_font(0.009, True))
        self.btn_next.clicked.connect(lambda: self.navigate(1))

        nav.addWidget(self.btn_back); nav.addStretch(); nav.addWidget(self.btn_next)
        self.main_layout.addLayout(nav)

        self.update_ui_texts()
        self.update_dots()

    def update_dots(self):
        idx = self.pages.currentIndex()
        accent = "#ffff00" if self.high_contrast else "#3daee9"
        for i, dot in enumerate(self.dots):
            if i == idx:
                dot.setStyleSheet(f"color: {accent}; font-size: 18px;")
                dot.setText("●")
            else:
                dot.setStyleSheet("color: rgba(128, 128, 128, 0.4); font-size: 14px;")
                dot.setText("•")

    def page_welcome(self):
        p = QWidget(); l = QVBoxLayout(p); l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_logo = QLabel()
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "welcome-logo.png")
        if os.path.exists(logo_path):
            pix = QPixmap(logo_path)
            s = int(self.sh * 0.15)
            self.lbl_logo.setPixmap(pix.scaled(s, s, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        self.lbl_welcome = QLabel()
        self.lbl_welcome.setFont(self.get_font(0.028, True))
        self.lbl_welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_welcome_sub = QLabel()
        self.lbl_welcome_sub.setFont(self.get_font(0.012))
        self.lbl_welcome_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        l.addStretch(); l.addWidget(self.lbl_logo, alignment=Qt.AlignmentFlag.AlignCenter)
        l.addSpacing(10); l.addWidget(self.lbl_welcome); l.addWidget(self.lbl_welcome_sub); l.addStretch()
        return p

    def page_display(self):
        p = QWidget(); l = QVBoxLayout(p)
        sec, self.lbl_disp_t, self.lbl_disp_s = self.create_title_section()
        l.addWidget(sec)

        self.btn_high_contrast = QPushButton(); self.btn_high_contrast.setFixedSize(320, 60)
        self.btn_high_contrast.setFont(self.get_font(0.011, True))
        self.btn_high_contrast.clicked.connect(self.toggle_high_contrast)
        l.addWidget(self.btn_high_contrast, alignment=Qt.AlignmentFlag.AlignCenter)

        l.addStretch()
        return p

    def page_drivers(self):
        p = QWidget(); l = QVBoxLayout(p)
        sec, self.lbl_dr_t, self.lbl_dr_s = self.create_title_section()
        l.addWidget(sec)
        self.btn_dr_mgr = QPushButton(); self.btn_dr_mgr.setFixedSize(320, 60)
        self.btn_dr_mgr.setFont(self.get_font(0.011, True))
        self.btn_dr_mgr.clicked.connect(self.open_drivers)
        l.addWidget(self.btn_dr_mgr, alignment=Qt.AlignmentFlag.AlignCenter); l.addStretch()
        return p

    def create_title_section(self):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(0, 0, 0, 15)
        t = QLabel(); t.setFont(self.get_font(0.022, True))
        s = QLabel(); s.setFont(self.get_font(0.011)); s.setWordWrap(True)
        l.addWidget(t); l.addWidget(s)
        return w, t, s

    def page_theme(self):
        p = QWidget(); l = QVBoxLayout(p)
        sec, self.lbl_theme_t, self.lbl_theme_s = self.create_title_section()
        l.addWidget(sec)
        self.btn_archive = QPushButton(); self.btn_dark = QPushButton(); self.btn_light = QPushButton()
        for b in [self.btn_archive, self.btn_dark, self.btn_light]:
            b.setFixedHeight(55); b.setFont(self.get_font(0.011, True))
            l.addWidget(b)
        self.btn_archive.clicked.connect(lambda: self.apply_kde_theme("org.archiveos.desktop", "dark"))
        self.btn_dark.clicked.connect(lambda: self.apply_kde_theme("org.kde.breezedark.desktop", "dark"))
        self.btn_light.clicked.connect(lambda: self.apply_kde_theme("org.kde.breeze.desktop", "light"))
        l.addStretch()
        return p

    def page_apps(self):
        p = QWidget(); l = QVBoxLayout(p)
        sec, self.lbl_app_t, self.lbl_app_s = self.create_title_section()
        l.addWidget(sec)
        self.app_grid = QGridLayout()
        self.app_grid.setSpacing(15)
        self.app_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addLayout(self.app_grid)
        l.addStretch()
        return p

    def page_tools(self):
        p = QWidget(); l = QVBoxLayout(p)
        sec, self.lbl_tool_t, self.lbl_tool_s = self.create_title_section()
        l.addWidget(sec)
        self.tool_grid = QGridLayout()
        self.tool_grid.setSpacing(15)
        self.tool_grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        l.addLayout(self.tool_grid)
        l.addStretch()
        return p

    def page_goodbye(self):
        p = QWidget(); l = QVBoxLayout(p); l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_gb = QLabel(); self.lbl_gb.setFont(self.get_font(0.030, True))
        self.lbl_gb_s = QLabel(); self.lbl_gb_s.setFont(self.get_font(0.014))
        l.addStretch(); l.addWidget(self.lbl_gb, alignment=Qt.AlignmentFlag.AlignCenter)
        l.addWidget(self.lbl_gb_s, alignment=Qt.AlignmentFlag.AlignCenter); l.addStretch()
        return p

    def manual_lang_change(self, index):
        self.lang = "en" if index == 0 else "tr"
        self.update_ui_texts()

    def update_ui_texts(self):
        t = self.texts[self.lang]
        self.lbl_welcome.setText(t["welcome"]); self.lbl_welcome_sub.setText(t["welcome_sub"])
        if hasattr(self, 'lbl_disp_t'):
            self.lbl_disp_t.setText(t["display"]); self.lbl_disp_s.setText(t["display_sub"])
            self.lbl_theme_t.setText(t["theme"]); self.lbl_theme_s.setText(t["theme_sub"])
            self.lbl_app_t.setText(t["apps"]); self.lbl_app_s.setText(t["apps_sub"])
            self.lbl_tool_t.setText(t["tools"]); self.lbl_tool_s.setText(t["tools_sub"])
            self.lbl_dr_t.setText(t["drivers"]); self.lbl_dr_s.setText(t["drivers_sub"])
            self.btn_dr_mgr.setText(t["driver_btn"])

        self.btn_high_contrast.setText(t["contrast_on"] if self.high_contrast else t["contrast_btn"])
        self.btn_archive.setText(t["archive"]); self.btn_light.setText(t["light"]); self.btn_dark.setText(t["dark"])
        self.btn_back.setText(t["back"]); self.lbl_gb.setText(t["goodbye"]); self.lbl_gb_s.setText(t["goodbye_sub"])
        self.btn_next.setText(t["finish"] if self.pages.currentIndex() == 6 else t["next"])
        self.btn_back.setVisible(self.pages.currentIndex() > 0)

        # Buton Genişliği Hesaplama
        btn_width = int(self.sw * 0.25)

        # App Grid Refresh
        while self.app_grid.count(): self.app_grid.takeAt(0).widget().deleteLater()
        for i, (name, cmd) in enumerate(t.get("app_list", [])):
            btn = QPushButton(name)
            btn.setFixedSize(btn_width, 60)
            btn.setFont(self.get_font(0.011, True))
            btn.clicked.connect(lambda ch, n=name, c=cmd: self.run_cmd(n, c, "Install"))
            self.app_grid.addWidget(btn, i // 2, i % 2, Qt.AlignmentFlag.AlignCenter)

        # Tool Grid Refresh
        while self.tool_grid.count(): self.tool_grid.takeAt(0).widget().deleteLater()
        for i, (name, cmd, action) in enumerate(t.get("tool_list", [])):
            btn = QPushButton(name)
            btn.setFixedSize(btn_width, 60)
            btn.setFont(self.get_font(0.011, True))
            btn.clicked.connect(lambda ch, n=name, c=cmd, a=action: self.run_cmd(n, c, a))
            self.tool_grid.addWidget(btn, i // 2, i % 2, Qt.AlignmentFlag.AlignCenter)
        self.update_theme_style()

    def run_cmd(self, name, cmd, act):
        p = f"echo '{act} {name}? (y/N)'; read -n 1 r; echo; if [[ $r =~ ^[Yy]$ ]]; then {cmd} -y; fi; read"
        subprocess.Popen(['konsole', '--hold', '-e', 'bash', '-c', p])

    def open_drivers(self):
        subprocess.Popen(['konsole', '-e', 'bash', '-c', "sudo driver-manager || sudo software-properties-gtk --open-tab=4; read"])

    def navigate(self, step):
        idx = self.pages.currentIndex() + step
        if 0 <= idx < 7:
            self.pages.setCurrentIndex(idx)
            self.update_ui_texts()
            self.update_dots()
        else:
            self.close()

    def apply_kde_theme(self, tid, mode):
        subprocess.Popen(['lookandfeeltool', '-a', tid]); self.current_theme = mode; self.update_theme_style()

    def toggle_high_contrast(self):
        self.high_contrast = not self.high_contrast
        t = 'org.kde.breeze.highcontrast' if self.high_contrast else 'org.kde.breezedark.desktop'
        subprocess.Popen(['lookandfeeltool', '-a', t])
        self.update_theme_style(); self.update_ui_texts(); self.update_dots()

    def update_theme_style(self):
        bg = "#000000" if self.high_contrast else ("#0d0d0d" if self.current_theme == "dark" else "#f5f5f5")
        txt = "#ffff00" if self.high_contrast else ("#ffffff" if self.current_theme == "dark" else "#1a1a1a")
        accent = "#ffff00" if self.high_contrast else "#3daee9"

        self.setStyleSheet(f"""
            background-color: {bg}; color: {txt};
            QPushButton {{ background: rgba(120,120,120,0.15); color: {txt}; border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; }}
            QPushButton:hover {{ background: rgba(150,150,150,0.3); border: 1px solid {accent}; }}
            QComboBox {{ background: #2a2a2a; color: white; border: 1px solid #444; border-radius: 4px; padding-left: 5px; }}
        """)
        self.btn_next.setStyleSheet(f"background: {accent}; color: black; border-radius: 6px; font-weight: bold;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ArchiveOSWizard(); win.show(); sys.exit(app.exec())
