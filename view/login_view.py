from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controller.auth_controller import AuthController
from models.user import BookingStaff, Admin, Manager


DARK = "#202124"
CARD = "#292a2d"
PANEL = "#242528"
INPUT = "#1c1d20"
TEXT = "#e8eaed"
MUTED = "#9aa0a6"
ACCENT = "#8ab4f8"
BORDER = "#5f6368"
DANGER = "#f28b82"


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.setWindowTitle("Horizon Cinemas - Login")
        self.setFixedSize(1040, 640)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("loginRoot")
        self.setCentralWidget(central)
        central.setStyleSheet(f"""
            QWidget#loginRoot {{ background-color: {DARK}; }}
            QLabel {{ background: transparent; }}
        """)

        root = QVBoxLayout(central)
        root.setContentsMargins(32, 32, 32, 32)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        shell = QFrame()
        shell.setObjectName("loginShell")
        shell.setFixedSize(960, 560)
        shell.setStyleSheet(f"""
            QFrame#loginShell {{
                background-color: {CARD};
                border: 1px solid {BORDER};
                border-radius: 10px;
            }}
        """)
        shell_layout = QHBoxLayout(shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)
        shell_layout.addWidget(self._build_brand_panel())
        shell_layout.addWidget(self._build_form_panel())

        root.addWidget(shell)

    def _build_brand_panel(self):
        panel = QWidget()
        panel.setObjectName("brandPanel")
        panel.setFixedWidth(460)
        panel.setStyleSheet(f"""
            QWidget#brandPanel {{
                background-color: {PANEL};
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
            }}
        """)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(34, 34, 34, 34)
        layout.setSpacing(16)

        brand_row = QHBoxLayout()
        brand_row.setContentsMargins(0, 0, 0, 0)
        brand_row.setSpacing(12)

        mark = QLabel("HC")
        mark.setFixedSize(58, 42)
        mark.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mark.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        mark.setStyleSheet(f"""
            color: {DARK};
            background-color: {ACCENT};
            border-radius: 10px;
        """)

        brand_text = QVBoxLayout()
        brand_text.setSpacing(2)
        horizon = QLabel("HORIZON")
        horizon.setStyleSheet(f"color: {TEXT}; font-size: 12px; font-weight: 800; letter-spacing: 1.4px;")
        cinemas = QLabel("CINEMAS")
        cinemas.setStyleSheet(f"color: {MUTED}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        brand_text.addWidget(horizon)
        brand_text.addWidget(cinemas)

        brand_row.addWidget(mark)
        brand_row.addLayout(brand_text)
        brand_row.addStretch()

        headline = QLabel("The backstage\npass to cinema\noperations.")
        headline.setFont(QFont("Arial", 27, QFont.Weight.Bold))
        headline.setStyleSheet(f"color: {TEXT};")
        headline.setWordWrap(True)

        subhead = QLabel(
            "Booking operations, listings, staff workflows, and reports in one secured desktop portal."
        )
        subhead.setWordWrap(True)
        subhead.setStyleSheet(f"color: {MUTED}; font-size: 14px; line-height: 1.4;")

        access_note = QLabel("Manager  |  Admin  |  Staff")
        access_note.setStyleSheet(
            f"color: {ACCENT}; font-size: 11px; font-weight: 800; letter-spacing: 1px;"
        )

        access_copy = QLabel("Your role decides which workspace opens after sign in.")
        access_copy.setWordWrap(True)
        access_copy.setStyleSheet(f"color: {MUTED}; font-size: 12px;")

        layout.addLayout(brand_row)
        layout.addStretch()
        layout.addWidget(headline)
        layout.addSpacing(10)
        layout.addWidget(subhead)
        layout.addStretch()
        layout.addWidget(access_note)
        layout.addWidget(access_copy)
        return panel

    def _build_form_panel(self):
        panel = QWidget()
        panel.setObjectName("formPanel")
        panel.setFixedWidth(500)
        panel.setStyleSheet(f"""
            QWidget#formPanel {{
                background-color: {CARD};
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
            }}
        """)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(64, 54, 64, 42)
        layout.setSpacing(0)

        form = QFrame()
        form.setObjectName("form")
        form.setStyleSheet("QFrame#form { background: transparent; border: none; }")
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(12)

        eyebrow = QLabel("WELCOME BACK")
        eyebrow.setStyleSheet(f"color: {ACCENT}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        title = QLabel("Sign in to continue")
        title.setFont(QFont("Arial", 25, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")
        subtitle = QLabel("Use your assigned account to open the correct workspace.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 13px;")

        input_style = f"""
            QLineEdit {{
                background-color: {INPUT};
                color: {TEXT};
                border: 1px solid #3a3b3f;
                border-radius: 7px;
                padding: 10px 12px;
                font-size: 13px;
                min-height: 22px;
            }}
            QLineEdit:hover {{ border-color: #50525a; }}
            QLineEdit:focus {{
                border: 1px solid {ACCENT};
                background-color: #1f2024;
            }}
        """
        label_style = f"color: {MUTED}; font-size: 10px; font-weight: 700; letter-spacing: 0.5px;"

        username_label = QLabel("USERNAME")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet(input_style)
        self.username_input.returnPressed.connect(self.password_input_focus)

        password_label = QLabel("PASSWORD")
        password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(input_style)
        self.password_input.returnPressed.connect(self._handle_login)

        self.error_label = QLabel("")
        self.error_label.setWordWrap(True)
        self.error_label.setStyleSheet(f"color: {DANGER}; font-size: 12px;")
        self.error_label.hide()

        login_btn = QPushButton("Sign in")
        login_btn.setMinimumHeight(44)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT};
                color: {DARK};
                font-size: 13px;
                font-weight: 800;
                border-radius: 7px;
                border: none;
                padding: 10px 16px;
            }}
            QPushButton:hover {{ background-color: #aecbfa; }}
            QPushButton:pressed {{ background-color: #7aa7f7; }}
        """)
        login_btn.clicked.connect(self._handle_login)

        form_layout.addWidget(eyebrow)
        form_layout.addWidget(title)
        form_layout.addWidget(subtitle)
        form_layout.addSpacing(22)
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        form_layout.addSpacing(8)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(self.error_label)
        form_layout.addSpacing(12)
        form_layout.addWidget(login_btn)

        footer = QLabel("Horizon Cinemas internal system")
        footer.setAlignment(Qt.AlignmentFlag.AlignLeft)
        footer.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        layout.addWidget(form)
        layout.addStretch()
        layout.addWidget(footer)
        return panel

    def password_input_focus(self):
        self.password_input.setFocus()

    def _show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()

    def _handle_login(self):
        self.error_label.hide()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            self._show_error("Please enter both username and password.")
            return

        user = self.auth_controller.login(username, password)

        if not user:
            self._show_error("Invalid username or password.")
            return

        self._open_dashboard(user)

    def _open_dashboard(self, user):
        if isinstance(user, Manager):
            from view.manager_view import ManagerView
            self.dashboard = ManagerView(user)
        elif isinstance(user, Admin):
            from view.admin_view import AdminView
            self.dashboard = AdminView(user)
        elif isinstance(user, BookingStaff):
            from view.staff_view import StaffView
            self.dashboard = StaffView(user)
        self.dashboard.show()
        self.close()
