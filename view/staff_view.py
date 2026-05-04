from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QLineEdit,
                              QComboBox, QCompleter, QScrollArea, QMessageBox, QFrame,
                              QDialog, QGridLayout, QSizePolicy, QFileDialog,
                              QStackedWidget, QButtonGroup)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextDocument
from PyQt6.QtPrintSupport import QPrinter
from collections import defaultdict
import datetime
import re
from controller.film_controller import FilmController
from controller.cinema_controller import CinemaController
from controller.booking_controller import BookingController
from controller.cancellation_controller import CancellationController
from view.seat_map_dialog import SeatMapDialog

DARK = "#202124"
CARD = "#292a2d"
INPUT = "#303134"
TEXT = "#e8eaed"
MUTED = "#9aa0a6"
ACCENT = "#8ab4f8"
BORDER = "#5f6368"
SUCCESS = "#81c995"
DANGER = "#f28b82"


def _listing_is_bookable(listing):
    show_time = listing.show_time
    if hasattr(show_time, "hour"):
        start_time = datetime.time(show_time.hour, show_time.minute, getattr(show_time, "second", 0))
    else:
        total_seconds = int(show_time.total_seconds())
        start_time = (datetime.datetime.min + datetime.timedelta(seconds=total_seconds)).time()
    return datetime.datetime.combine(listing.show_date, start_time) >= datetime.datetime.now()

BTN = f"""
    QPushButton {{
        background-color: {ACCENT}; color: #202124;
        font-weight: bold; border-radius: 4px;
        padding: 6px 16px; border: none;
    }}
    QPushButton:hover {{ background-color: #aecbfa; }}
"""
BTN_DANGER = f"""
    QPushButton {{
        background-color: {DANGER}; color: #202124;
        font-weight: bold; border-radius: 4px;
        padding: 6px 16px; border: none;
    }}
    QPushButton:hover {{ background-color: #ee675c; }}
"""
INPUT_STYLE = f"""
    QLineEdit, QComboBox, QSpinBox, QDateEdit {{
        background-color: {INPUT}; color: {TEXT};
        border: 1px solid {BORDER}; border-radius: 4px;
        padding: 6px 10px; font-size: 12px;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus {{
        border: 1px solid {ACCENT};
    }}
    QComboBox QAbstractItemView {{
        background-color: {CARD}; color: {TEXT};
        selection-background-color: {ACCENT};
    }}
"""

NAV_STYLE = f"""
    QPushButton {{
        background-color: transparent;
        color: {TEXT};
        font-size: 13px;
        text-align: left;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 10px 12px;
    }}
    QPushButton:hover {{
        background-color: {INPUT};
        border-color: {BORDER};
    }}
    QPushButton:checked {{
        background-color: {ACCENT};
        color: {DARK};
        font-weight: bold;
    }}
"""

PAGE_STYLE = f"QWidget#pageShell {{ background-color: {DARK}; }}"

CARD_STYLE = f"""
    QFrame {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 4px;
    }}
"""

UI_INPUT = f"""
    QLineEdit, QComboBox, QSpinBox, QDateEdit {{
        background-color: #1c1d20;
        color: {TEXT};
        border: 1px solid #3a3b3f;
        border-radius: 6px;
        padding: 8px 11px;
        font-size: 12px;
        min-height: 18px;
    }}
    QLineEdit:hover, QComboBox:hover, QSpinBox:hover,
    QDateEdit:hover {{ border: 1px solid #50525a; }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
    QDateEdit:focus {{
        border: 1px solid {ACCENT}; background-color: #1f2024;
    }}
    QComboBox::drop-down, QDateEdit::drop-down {{
        border: none; width: 22px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #1c1d20; color: {TEXT};
        border: 1px solid {BORDER};
        selection-background-color: {ACCENT};
        selection-color: {DARK}; outline: none;
    }}
"""

UI_BTN = f"""
    QPushButton {{
        background-color: {ACCENT}; color: {DARK};
        font-weight: 600; font-size: 12px;
        border-radius: 7px; padding: 10px 16px; border: none;
    }}
    QPushButton:hover {{ background-color: #aecbfa; }}
    QPushButton:pressed {{ background-color: #7aa7f7; }}
"""

UI_BTN_DANGER = f"""
    QPushButton {{
        background-color: {DANGER}; color: {DARK};
        font-weight: 600; font-size: 12px;
        border-radius: 7px; padding: 10px 16px; border: none;
    }}
    QPushButton:hover {{ background-color: #ee675c; }}
    QPushButton:pressed {{ background-color: #d05a52; }}
"""

UI_BTN_GHOST = f"""
    QPushButton {{
        background-color: transparent; color: {TEXT};
        font-weight: 500; font-size: 12px;
        border-radius: 7px; padding: 9px 14px;
        border: 1px solid #3a3b3f;
    }}
    QPushButton:hover {{ background-color: #2a2b2f; border-color: #50525a; }}
"""


class TicketDialog(QDialog):
    def __init__(self, parent, booking_ref, film_title, cinema_name, city_name,
                 show_date, show_time, show_time_cat, seat_numbers, quantity,
                 total_price, screen_number=None, booking_date=None):
        super().__init__(parent)
        self.setWindowTitle("Booking Confirmation")
        self.setFixedSize(380, 640)
        self.setStyleSheet(f"background-color: {DARK};")
        screen_number = screen_number if screen_number is not None else "N/A"
        booking_date = booking_date or datetime.datetime.now()
        if hasattr(booking_date, "strftime"):
            booking_date = booking_date.strftime("%Y-%m-%d %H:%M:%S")
        self.receipt_data = {
            "booking_ref": booking_ref,
            "film_title": film_title,
            "cinema_name": cinema_name,
            "city_name": city_name,
            "show_date": show_date,
            "show_time": show_time,
            "show_time_cat": show_time_cat,
            "screen_number": screen_number,
            "seat_numbers": seat_numbers,
            "quantity": quantity,
            "total_price": total_price,
            "booking_date": booking_date,
        }

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Header (accent strip) ──────────────────────────────────────────
        header = QWidget()
        header.setStyleSheet(f"background-color: {ACCENT};")
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(20, 14, 20, 14)
        h_layout.setSpacing(2)

        cinema_lbl = QLabel(cinema_name.upper())
        cinema_lbl.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        cinema_lbl.setStyleSheet("color: #202124;")
        cinema_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        city_lbl = QLabel(city_name)
        city_lbl.setStyleSheet("color: #3c4043; font-size: 11px;")
        city_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h_layout.addWidget(cinema_lbl)
        h_layout.addWidget(city_lbl)

        # ── Body ──────────────────────────────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background-color: {CARD};")
        b_layout = QVBoxLayout(body)
        b_layout.setContentsMargins(24, 18, 24, 18)
        b_layout.setSpacing(6)

        film_lbl = QLabel(film_title.upper())
        film_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        film_lbl.setStyleSheet(f"color: {TEXT};")
        film_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        film_lbl.setWordWrap(True)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"color: {BORDER};")

        def row(label, value):
            w = QWidget()
            rl = QHBoxLayout(w)
            rl.setContentsMargins(0, 2, 0, 2)
            lbl_w = QLabel(label)
            lbl_w.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
            val_w = QLabel(str(value))
            val_w.setStyleSheet(f"color: {TEXT}; font-size: 12px; font-weight: bold;")
            val_w.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            rl.addWidget(lbl_w)
            rl.addStretch()
            rl.addWidget(val_w)
            return w

        b_layout.addWidget(film_lbl)
        b_layout.addSpacing(4)
        b_layout.addWidget(sep)
        b_layout.addWidget(row("Film Date", str(show_date)))
        b_layout.addWidget(row("Showing Time", str(show_time)))
        b_layout.addWidget(row("Session", show_time_cat))
        b_layout.addWidget(row("Screen number", str(screen_number)))
        b_layout.addWidget(row("Seat Numbers", seat_numbers))
        b_layout.addWidget(row("Number of Tickets", str(quantity)))
        b_layout.addWidget(row("Booking Date", str(booking_date)))

        # ── Tear line ─────────────────────────────────────────────────────
        tear = QLabel("╌ " * 21)
        tear.setStyleSheet(f"color: {BORDER}; font-size: 9px; letter-spacing: 1px;")
        tear.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ── Price ─────────────────────────────────────────────────────────
        total_lbl = QLabel("TOTAL BOOKING COST")
        total_lbl.setStyleSheet(f"color: {MUTED}; font-size: 10px; letter-spacing: 2px;")
        total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        price_lbl = QLabel(f"£{total_price:.2f}")
        price_lbl.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        price_lbl.setStyleSheet(f"color: {SUCCESS};")
        price_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ── Booking reference ─────────────────────────────────────────────
        ref_caption = QLabel("BOOKING REFERENCE")
        ref_caption.setStyleSheet(f"color: {MUTED}; font-size: 10px; letter-spacing: 2px;")
        ref_caption.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ref_lbl = QLabel(booking_ref)
        ref_lbl.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        ref_lbl.setStyleSheet(f"color: {ACCENT}; letter-spacing: 3px;")
        ref_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        b_layout.addWidget(tear)
        b_layout.addWidget(total_lbl)
        b_layout.addWidget(price_lbl)
        b_layout.addSpacing(6)
        b_layout.addWidget(ref_caption)
        b_layout.addWidget(ref_lbl)

        # ── Footer ────────────────────────────────────────────────────────
        footer = QWidget()
        footer.setStyleSheet(f"background-color: {DARK};")
        f_layout = QVBoxLayout(footer)
        f_layout.setContentsMargins(24, 10, 24, 14)

        print_btn = QPushButton("Print PDF")
        print_btn.setStyleSheet(UI_BTN)
        print_btn.setFixedHeight(36)
        print_btn.clicked.connect(self._print_pdf)

        done_btn = QPushButton("Done")
        done_btn.setStyleSheet(UI_BTN)
        done_btn.setFixedHeight(36)
        done_btn.clicked.connect(self.accept)

        f_layout.addWidget(print_btn)
        f_layout.addWidget(done_btn)

        layout.addWidget(header)
        layout.addWidget(body)
        layout.addWidget(footer)

    def _print_pdf(self):
        data = self.receipt_data
        safe_ref = re.sub(r"[^A-Za-z0-9_-]+", "_", data["booking_ref"])
        default_name = f"receipt_{safe_ref}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Receipt PDF",
            default_name,
            "PDF Files (*.pdf)",
        )
        if not file_path:
            return
        if not file_path.lower().endswith(".pdf"):
            file_path += ".pdf"

        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setOutputFileName(file_path)

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #202124;">
            <h1 style="text-align:center;">Horizon Cinemas</h1>
            <h2 style="text-align:center;">Booking Receipt</h2>
            <hr>
            <h3>Booking Reference: {data["booking_ref"]}</h3>
            <p><b>Film Name:</b> {data["film_title"]}</p>
            <p><b>Cinema:</b> {data["cinema_name"]}, {data["city_name"]}</p>
            <p><b>Film Date:</b> {data["show_date"]}</p>
            <p><b>Showing Time:</b> {data["show_time"]}</p>
            <p><b>Session:</b> {data["show_time_cat"]}</p>
            <p><b>Screen #:</b> {data["screen_number"]}</p>
            <p><b>Number of Tickets:</b> {data["quantity"]}</p>
            <p><b>Seat Numbers:</b> {data["seat_numbers"]}</p>
            <p><b>Booking Date:</b> {data["booking_date"]}</p>
            <hr>
            <p style="font-size:18px;"><b>Total Booking Cost:</b> £{data["total_price"]:.2f}</p>
        </body>
        </html>
        """
        document = QTextDocument()
        document.setHtml(html)
        document.print(printer)
        QMessageBox.information(self, "Receipt Saved", f"Receipt PDF saved to:\n{file_path}")


class StaffView(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.film_ctrl = FilmController()
        self.cinema_ctrl = CinemaController()
        self.booking_ctrl = BookingController()
        self.cancel_ctrl = CancellationController()
        self._selected_seat_ids = []
        self._selected_seat_nums = []
        self.setWindowTitle(f"Horizon Cinemas - Staff: {user.full_name}")
        self.setMinimumSize(1100, 700)
        self._build_ui()

    def _assigned_cinema_name(self):
        cinema_id = getattr(self.user, "assigned_cinema_id", None)
        if cinema_id is None:
            return "No cinema assigned"
        for cinema in self.cinema_ctrl.get_all_cinemas():
            if cinema.cinema_id == cinema_id:
                return cinema.name
        return f"Cinema ID {cinema_id}"

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet(f"background-color: {DARK};")

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ── Header ────────────────────────────────────────────────────────
        header = QFrame()
        header.setStyleSheet(f"background-color: {CARD}; border-bottom: 1px solid {BORDER};")
        header.setFixedHeight(72)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(24, 0, 24, 0)
        h_layout.setSpacing(14)

        title_lbl = QLabel("Horizon Cinemas")
        title_lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT};")

        subtitle_lbl = QLabel("Booking Staff portal")
        subtitle_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        assigned_cinema = self._assigned_cinema_name()
        user_lbl = QLabel(f"  {self.user.full_name}  |  Booking Staff  |  {assigned_cinema}")
        user_lbl.setStyleSheet(f"color: {MUTED}; font-size: 12px;")

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(BTN_DANGER)
        logout_btn.setFixedWidth(80)
        logout_btn.clicked.connect(self._logout)

        h_layout.addWidget(title_lbl)
        h_layout.addWidget(subtitle_lbl)
        h_layout.addStretch()
        h_layout.addWidget(user_lbl)
        h_layout.addWidget(logout_btn)

        # ── Body (sidebar + content) ──────────────────────────────────────
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(16, 16, 16, 16)
        body_layout.setSpacing(16)

        # Sidebar
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            f"QFrame#sidebar {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
        )
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(8)

        nav_title = QLabel("Workspace")
        nav_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        nav_title.setStyleSheet(f"color: {TEXT}; background: transparent; border: none;")

        nav_hint = QLabel("Choose one task at a time.")
        nav_hint.setWordWrap(True)
        nav_hint.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent; border: none;")

        sidebar_layout.addWidget(nav_title)
        sidebar_layout.addWidget(nav_hint)

        self._nav_group = QButtonGroup(self)
        self._nav_group.setExclusive(True)
        self._nav_buttons = []

        self.pages = QStackedWidget()
        self.pages.setStyleSheet(PAGE_STYLE)

        nav_pages = [
            ("Film Listings", self._build_listings_tab()),
            ("Book Tickets",  self._build_booking_tab()),
            ("Cancel Booking", self._build_cancel_tab()),
        ]

        for index, (label, page_widget) in enumerate(nav_pages):
            self.pages.addWidget(page_widget)
            nav_button = QPushButton(label)
            nav_button.setCheckable(True)
            nav_button.setStyleSheet(NAV_STYLE)
            nav_button.clicked.connect(
                lambda _=False, page_index=index: self._set_page(page_index))
            self._nav_group.addButton(nav_button)
            self._nav_buttons.append(nav_button)
            sidebar_layout.addWidget(nav_button)

        sidebar_layout.addStretch()

        content_shell = QFrame()
        content_shell.setStyleSheet(f"background-color: {DARK}; border: none;")
        content_layout = QVBoxLayout(content_shell)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.pages)

        body_layout.addWidget(sidebar)
        body_layout.addWidget(content_shell, 1)

        main_layout.addWidget(header)
        main_layout.addWidget(body, 1)

        self._set_page(0)

    def _set_page(self, index):
        self.pages.setCurrentIndex(index)
        for btn_index, button in enumerate(self._nav_buttons):
            button.setChecked(btn_index == index)
        self._refresh_page_data(index)

    def _refresh_page_data(self, index):
        refreshers = {
            0: [self._load_listings],
            1: [self._load_booking_listing_options],
        }
        for refresh in refreshers.get(index, []):
            refresh()

    # ── Film Listings page ────────────────────────────────────────────────

    def _build_listings_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        widget.setStyleSheet(f"background-color: {DARK};")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(20)

        # Page header
        hdr = QVBoxLayout()
        hdr.setSpacing(4)
        title = QLabel("Film Listings")
        title.setStyleSheet(f"color: {TEXT}; font-size: 22px; font-weight: 700;")
        sub = QLabel("View scheduled films at your cinema")
        sub.setStyleSheet(f"color: {MUTED}; font-size: 13px;")
        hdr.addWidget(title)
        hdr.addWidget(sub)
        layout.addLayout(hdr)

        # Toolbar
        toolbar = QHBoxLayout()
        refresh_btn = QPushButton("Refresh Listings")
        refresh_btn.setStyleSheet(UI_BTN)
        refresh_btn.setFixedWidth(160)
        refresh_btn.clicked.connect(self._load_listings)
        toolbar.addWidget(refresh_btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: {DARK}; }}
            QScrollBar:vertical {{
                background: {DARK}; width: 8px; margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER}; border-radius: 4px; min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

        self._listings_container = QWidget()
        self._listings_container.setStyleSheet(f"background-color: {DARK};")
        self._listings_layout = QVBoxLayout(self._listings_container)
        self._listings_layout.setContentsMargins(2, 2, 10, 2)
        self._listings_layout.setSpacing(0)

        scroll.setWidget(self._listings_container)
        layout.addWidget(scroll)

        self._load_listings()
        return widget

    def _load_listings(self):
        while self._listings_layout.count():
            item = self._listings_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        listings = [
            listing for listing in self.film_ctrl.get_listings_for_cinema(self.user.assigned_cinema_id)
            if _listing_is_bookable(listing)
        ]
        films = {f.film_id: f for f in self.film_ctrl.get_all_films()}

        groups = defaultdict(list)
        for lst in listings:
            groups[(lst.film_id, lst.show_date)].append(lst)

        if not groups:
            no_lbl = QLabel("No listings available for this cinema.")
            no_lbl.setStyleSheet(f"color: {MUTED}; font-size: 13px; padding: 20px;")
            no_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self._listings_layout.addWidget(no_lbl)
            self._listings_layout.addStretch()
            return

        sorted_keys = sorted(
            groups.keys(),
            key=lambda k: (k[1], films[k[0]].title if k[0] in films else '')
        )

        prev_date = None
        for (film_id, show_date) in sorted_keys:
            film = films.get(film_id)
            if not film:
                continue

            if show_date != prev_date:
                if prev_date is not None:
                    spacer = QWidget()
                    spacer.setFixedHeight(8)
                    spacer.setStyleSheet(f"background: {DARK};")
                    self._listings_layout.addWidget(spacer)

                date_lbl = QLabel(self._format_date(show_date))
                date_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                date_lbl.setStyleSheet(f"""
                    color: {TEXT}; padding: 10px 2px 6px 2px;
                    border-bottom: 1px solid {BORDER};
                    background: transparent;
                """)
                self._listings_layout.addWidget(date_lbl)
                prev_date = show_date

            card = self._make_film_card(film, groups[(film_id, show_date)])
            self._listings_layout.addWidget(card)

            gap = QWidget()
            gap.setFixedHeight(12)
            gap.setStyleSheet(f"background: {DARK};")
            self._listings_layout.addWidget(gap)

        self._listings_layout.addStretch()

    def _format_date(self, date_val):
        if isinstance(date_val, datetime.date):
            return date_val.strftime("%A %d %b %Y")
        return str(date_val)

    def _make_film_card(self, film, listings):
        card = QFrame()
        card.setObjectName("filmCard")
        card.setStyleSheet(f"""
            QFrame#filmCard {{
                background-color: {CARD};
                border: 1px solid {BORDER};
                border-radius: 6px;
            }}
        """)
        card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        # ── Title bar ──────────────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setStyleSheet(f"""
            QWidget#titleBar {{
                background-color: {INPUT};
                border-radius: 5px 5px 0px 0px;
                border-bottom: 1px solid {BORDER};
            }}
        """)
        tb_layout = QVBoxLayout(title_bar)
        tb_layout.setContentsMargins(14, 10, 14, 10)
        tb_layout.setSpacing(3)

        title_lbl = QLabel(film.title)
        title_lbl.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT}; background: transparent;")

        meta_parts = []
        if film.imdb_rating:
            meta_parts.append(f"IMDb Rating: {film.imdb_rating}")
        if film.genre:
            meta_parts.append(film.genre)
        if film.release_year:
            meta_parts.append(str(film.release_year))
        if film.age_rating:
            meta_parts.append(film.age_rating)
        if film.duration:
            meta_parts.append(f"{film.duration} min")
        meta_lbl = QLabel(",  ".join(meta_parts))
        meta_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent;")

        tb_layout.addWidget(title_lbl)
        tb_layout.addWidget(meta_lbl)

        # ── Body: description + cast ───────────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background: transparent;")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(14, 8, 14, 8)
        body_layout.setSpacing(4)

        if film.description:
            desc_lbl = QLabel(film.description)
            desc_lbl.setStyleSheet(f"color: {TEXT}; font-size: 11px; background: transparent;")
            desc_lbl.setWordWrap(True)
            body_layout.addWidget(desc_lbl)

        if film.cast_members:
            cast_lbl = QLabel(f"Cast: {film.cast_members}")
            cast_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent;")
            cast_lbl.setWordWrap(True)
            body_layout.addWidget(cast_lbl)

        # ── Showings ───────────────────────────────────────────────────────
        showings_section = QWidget()
        showings_section.setStyleSheet(f"background: transparent;")
        sh_layout = QVBoxLayout(showings_section)
        sh_layout.setContentsMargins(14, 4, 14, 14)
        sh_layout.setSpacing(6)

        showings_lbl = QLabel("Showings:")
        showings_lbl.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        showings_lbl.setStyleSheet(f"color: {TEXT}; background: transparent;")
        sh_layout.addWidget(showings_lbl)

        sorted_listings = sorted(listings, key=lambda l: l.show_time)

        shows_frame = QFrame()
        shows_frame.setObjectName("showsFrame")
        shows_frame.setStyleSheet(f"""
            QFrame#showsFrame {{
                border: 1px solid {BORDER};
                background-color: {DARK};
                border-radius: 4px;
            }}
        """)
        shows_grid = QGridLayout(shows_frame)
        shows_grid.setContentsMargins(0, 0, 0, 0)
        shows_grid.setSpacing(0)

        for col, listing in enumerate(sorted_listings):
            available = self.booking_ctrl.get_available_seat_count(listing.listing_id)
            left_border = f"border-left: 1px solid {BORDER};" if col > 0 else ""

            h_lbl = QLabel(f"Show {col + 1}")
            h_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h_lbl.setStyleSheet(f"""
                background-color: {INPUT}; color: {TEXT};
                font-weight: bold; font-size: 11px;
                padding: 6px 8px;
                border-bottom: 1px solid {BORDER};
                {left_border}
            """)
            shows_grid.addWidget(h_lbl, 0, col)

            time_str = str(listing.show_time)[:5] if listing.show_time else ""
            i_lbl = QLabel(f"{time_str}  [{available} seats available]")
            i_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            i_lbl.setStyleSheet(f"""
                background-color: {CARD}; color: {TEXT};
                font-size: 11px; padding: 8px 8px;
                border-bottom: 1px solid {BORDER};
                {left_border}
            """)
            shows_grid.addWidget(i_lbl, 1, col)

            btn_cell = QWidget()
            btn_cell.setStyleSheet(f"background-color: {CARD}; {left_border}")
            btn_c_layout = QHBoxLayout(btn_cell)
            btn_c_layout.setContentsMargins(8, 6, 8, 6)
            book_btn = QPushButton("Book")
            book_btn.setStyleSheet(UI_BTN)
            book_btn.setFixedHeight(30)
            book_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            book_btn.clicked.connect(
                lambda _, lid=listing.listing_id: self._book_from_listing(lid))
            btn_c_layout.addWidget(book_btn)
            shows_grid.addWidget(btn_cell, 2, col)

            shows_grid.setColumnStretch(col, 1)

        sh_layout.addWidget(shows_frame)

        card_layout.addWidget(title_bar)
        card_layout.addWidget(body)
        card_layout.addWidget(showings_section)

        return card

    # ── Book Tickets page ─────────────────────────────────────────────────

    def _build_booking_tab(self):
        outer = QScrollArea()
        outer.setObjectName("pageShell")
        outer.setWidgetResizable(True)
        outer.setFrameShape(QFrame.Shape.NoFrame)
        outer.setStyleSheet(f"""
            QScrollArea#pageShell {{ background-color: {DARK}; border: none; }}
            QScrollBar:vertical {{ background: transparent; width: 8px; margin: 4px; }}
            QScrollBar::handle:vertical {{ background: #3a3b3f; border-radius: 4px; min-height: 24px; }}
            QScrollBar::handle:vertical:hover {{ background: #50525a; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)

        widget = QWidget()
        widget.setObjectName("pageShell")
        page_layout = QVBoxLayout(widget)
        page_layout.setContentsMargins(28, 24, 28, 28)
        page_layout.setSpacing(20)

        def fl(text):
            l = QLabel(text)
            l.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; "
                f"letter-spacing: 0.5px; background: transparent;"
            )
            return l

        def thin_sep():
            w = QWidget()
            w.setFixedHeight(1)
            w.setStyleSheet(f"background-color: {BORDER};")
            return w

        # Page header
        hdr_row = QHBoxLayout()
        hdr_row.setSpacing(0)
        hdr_row.setContentsMargins(0, 0, 0, 0)
        tb = QVBoxLayout()
        tb.setSpacing(4)
        tb.setContentsMargins(0, 0, 0, 0)
        pg_title = QLabel("Book Tickets")
        pg_title.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        pg_title.setStyleSheet(f"color: {TEXT};")
        pg_sub = QLabel("Select a listing, choose seats and confirm a booking.")
        pg_sub.setStyleSheet(f"color: {MUTED}; font-size: 13px;")
        tb.addWidget(pg_title)
        tb.addWidget(pg_sub)
        hdr_row.addLayout(tb)
        hdr_row.addStretch()

        # ── Listing selector card ─────────────────────────────────────────
        sel_card = QFrame()
        sel_card.setObjectName("selCard")
        sel_card.setStyleSheet(
            f"QFrame#selCard {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
        )
        sel_cl = QVBoxLayout(sel_card)
        sel_cl.setContentsMargins(20, 18, 20, 18)
        sel_cl.setSpacing(8)

        self.b_listing_id = QComboBox()
        self.b_listing_id.setStyleSheet(UI_INPUT)
        self.b_listing_id.setMinimumHeight(38)
        self.b_listing_id.currentIndexChanged.connect(self._on_listing_changed)
        self.b_listing_id.activated.connect(self._on_listing_changed)
        self._load_booking_listing_options()

        self.listing_info_lbl = QLabel("Select a listing to see film details")
        self.listing_info_lbl.setStyleSheet(f"""
            background-color: {INPUT}; color: {MUTED};
            border: 1px solid {BORDER}; border-radius: 4px;
            padding: 6px 8px; font-size: 11px;
        """)
        self.listing_info_lbl.setWordWrap(True)
        self.listing_info_lbl.setMinimumHeight(28)

        self.b_seats_info = QLabel("No seats selected")
        self.b_seats_info.setStyleSheet(
            f"color: {MUTED}; font-size: 11px; background: transparent;"
        )

        sel_cl.addWidget(fl("LISTING"))
        sel_cl.addWidget(self.b_listing_id)
        sel_cl.addWidget(self.listing_info_lbl)

        seat_card = QFrame()
        seat_card.setObjectName("seatCard")
        self.b_seat_card = seat_card
        seat_card.setStyleSheet(
            f"QFrame#seatCard {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
        )
        seat_cl = QVBoxLayout(seat_card)
        seat_cl.setContentsMargins(1, 1, 1, 1)
        seat_cl.setSpacing(0)

        seat_hdr = QWidget()
        seat_hdr.setFixedHeight(54)
        seat_hdr_h = QHBoxLayout(seat_hdr)
        seat_hdr_h.setContentsMargins(22, 0, 22, 0)
        seat_hdr_h.setSpacing(12)
        self.b_seat_map_title = QLabel("Seat Map")
        self.b_seat_map_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.b_seat_map_title.setStyleSheet(f"color: {TEXT}; background: transparent;")
        seat_hdr_h.addWidget(self.b_seat_map_title)
        seat_hdr_h.addStretch()
        seat_hdr_h.addWidget(self.b_seats_info)

        seat_div = QWidget()
        seat_div.setFixedHeight(1)
        seat_div.setStyleSheet(f"background-color: {BORDER};")

        self.b_seat_map_scroll = QScrollArea()
        self.b_seat_map_scroll.setWidgetResizable(True)
        self.b_seat_map_scroll.setMinimumHeight(520)
        self.b_seat_map_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.b_seat_map_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.b_seat_map_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.b_seat_map_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.b_seat_map_scroll.setStyleSheet(f"QScrollArea {{ background-color: {CARD}; border: none; }}")
        self.b_seat_map_body = QWidget()
        self.b_seat_map_body.setStyleSheet(f"background-color: {CARD};")
        self.b_seat_map_layout = QVBoxLayout(self.b_seat_map_body)
        self.b_seat_map_layout.setContentsMargins(16, 16, 16, 16)
        self.b_seat_map_layout.setSpacing(10)
        self.b_seat_map_scroll.setWidget(self.b_seat_map_body)

        seat_cl.addWidget(seat_hdr)
        seat_cl.addWidget(seat_div)
        seat_cl.addWidget(self.b_seat_map_scroll)

        # ── Customer details card ─────────────────────────────────────────
        det_card = QFrame()
        det_card.setObjectName("detCard")
        det_card.setStyleSheet(
            f"QFrame#detCard {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
        )
        det_cl = QVBoxLayout(det_card)
        det_cl.setContentsMargins(20, 18, 20, 20)
        det_cl.setSpacing(0)

        det_title = QLabel("Customer Details")
        det_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        det_title.setStyleSheet(f"color: {TEXT}; background: transparent;")

        self.price_lbl = QLabel("")
        self.price_lbl.setStyleSheet(
            f"color: {SUCCESS}; font-size: 13px; font-weight: bold; background: transparent;"
        )

        self.b_name = QLineEdit()
        self.b_name.setPlaceholderText("Customer name")
        self.b_name.setStyleSheet(UI_INPUT)

        self.b_phone = QLineEdit()
        self.b_phone.setPlaceholderText("Phone number")
        self.b_phone.setStyleSheet(UI_INPUT)

        self.b_email = QLineEdit()
        self.b_email.setPlaceholderText("Email address")
        self.b_email.setStyleSheet(UI_INPUT)

        book_btn = QPushButton("Confirm Booking")
        book_btn.setStyleSheet(UI_BTN)
        book_btn.setMinimumHeight(42)
        book_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        book_btn.clicked.connect(self._confirm_booking)

        det_cl.addWidget(det_title)
        det_cl.addSpacing(4)
        det_cl.addWidget(thin_sep())
        det_cl.addSpacing(10)
        det_cl.addWidget(self.price_lbl)
        det_cl.addSpacing(10)
        for w, lt in [
            (self.b_name,  "CUSTOMER NAME"),
            (self.b_phone, "CUSTOMER PHONE"),
            (self.b_email, "CUSTOMER EMAIL"),
        ]:
            det_cl.addWidget(fl(lt))
            det_cl.addSpacing(6)
            det_cl.addWidget(w)
            det_cl.addSpacing(12)
        det_cl.addSpacing(4)
        det_cl.addWidget(book_btn)

        form_col = QWidget()
        form_col.setMinimumWidth(360)
        form_col.setMaximumWidth(460)
        form_layout = QVBoxLayout(form_col)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(16)
        form_layout.addWidget(sel_card)
        form_layout.addWidget(det_card)
        form_layout.addStretch()

        content_row = QHBoxLayout()
        content_row.setContentsMargins(0, 0, 0, 0)
        content_row.setSpacing(16)
        content_row.addWidget(form_col)

        seat_col = QWidget()
        seat_layout = QVBoxLayout(seat_col)
        seat_layout.setContentsMargins(0, 0, 0, 0)
        seat_layout.setSpacing(0)
        seat_layout.addWidget(seat_card)
        content_row.addWidget(seat_col, 1)

        page_layout.addLayout(hdr_row)
        page_layout.addLayout(content_row, 1)

        self._set_staff_seat_map_visible(False)
        outer.setWidget(widget)
        return outer

    def _book_from_listing(self, listing_id):
        index = self.b_listing_id.findData(listing_id)
        if index >= 0:
            self.b_listing_id.setCurrentIndex(index)
        self._set_page(1)

    def _load_booking_listing_options(self):
        listings = [
            listing for listing in self.film_ctrl.get_listings_for_cinema(self.user.assigned_cinema_id)
            if _listing_is_bookable(listing)
        ]
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}

        self.b_listing_id.blockSignals(True)
        self.b_listing_id.clear()

        for listing in listings:
            film_title = films.get(listing.film_id, "Unknown")
            display_text = f"{film_title} - {listing.show_date} {listing.show_time}"
            self.b_listing_id.addItem(display_text, listing.listing_id)

        self.b_listing_id.setEditable(True)
        self.b_listing_id.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.b_listing_id.setCurrentIndex(-1)
        self.b_listing_id.lineEdit().setPlaceholderText("Search listing")
        completer = self.b_listing_id.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.b_listing_id.blockSignals(False)

    def _set_staff_seat_map_visible(self, visible):
        self.b_seat_card.setVisible(visible)
        self.b_seat_map_title.setVisible(visible)
        self.b_seat_map_scroll.setVisible(visible)

    def _clear_staff_seat_map(self, message="Select a listing to view seats."):
        def clear_child_layout(child_layout):
            while child_layout.count():
                child_item = child_layout.takeAt(0)
                child_widget = child_item.widget()
                nested_layout = child_item.layout()
                if child_widget:
                    child_widget.deleteLater()
                elif nested_layout:
                    clear_child_layout(nested_layout)

        while self.b_seat_map_layout.count():
            item = self.b_seat_map_layout.takeAt(0)
            widget = item.widget()
            nested = item.layout()
            if widget:
                widget.deleteLater()
            elif nested:
                clear_child_layout(nested)

        if not message:
            return

        message_lbl = QLabel(message)
        message_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message_lbl.setWordWrap(True)
        message_lbl.setStyleSheet(f"color: {MUTED}; font-size: 12px; padding: 24px;")
        self.b_seat_map_layout.addWidget(message_lbl)
        self.b_seat_map_layout.addStretch()

    def _staff_available_seat_style(self, base_color):
        return f"""
            QPushButton {{
                background-color: {base_color}; color: {MUTED};
                border-radius: 3px; border: 1px solid #4a4f52; font-size: 8px;
            }}
            QPushButton:hover {{
                background-color: #5f6368; color: {TEXT}; border-color: {ACCENT};
            }}
        """

    def _render_staff_seat_map(self, listing, film_title):
        seats = self.booking_ctrl.get_seats_for_listing(listing.listing_id)
        if not seats:
            self._clear_staff_seat_map("No seats found for this listing.")
            return

        self._clear_staff_seat_map("")

        header = QLabel(f"{film_title} | {listing.show_date} | {listing.show_time}")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"color: {TEXT}; font-size: 11px; font-weight: bold;")

        screen = QLabel("S  C  R  E  E  N")
        screen.setFixedHeight(24)
        screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        screen.setStyleSheet(f"""
            background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1,
                stop:0 #6e7478, stop:1 {INPUT});
            color: {MUTED}; font-size: 10px; letter-spacing: 5px;
            border-radius: 4px;
        """)

        self.b_seat_map_layout.addWidget(header)
        self.b_seat_map_layout.addWidget(screen)

        seats_per_row = 10
        available_colors = {
            "LOWER_HALL": "#3c4043",
            "UPPER_GALLERY": "#37404a",
            "VIP": "#3d2e00",
        }
        booked_style = """
            QPushButton {
                background-color: #1a1c1e; color: #3c4043;
                border-radius: 3px; border: 1px solid #2a2d30; font-size: 8px;
            }
        """
        labels = {
            "LOWER_HALL": "Lower Hall",
            "UPPER_GALLERY": "Upper Gallery",
            "VIP": "VIP",
        }
        groups = {"LOWER_HALL": [], "UPPER_GALLERY": [], "VIP": []}
        for seat in seats:
            groups.setdefault(seat[2], []).append(seat)

        self._b_seat_data = {seat[0]: seat for seat in seats}
        self._b_seat_buttons = {}

        for seat_type in ["LOWER_HALL", "UPPER_GALLERY", "VIP"]:
            type_seats = groups.get(seat_type, [])
            if not type_seats:
                continue

            section_lbl = QLabel(labels.get(seat_type, seat_type))
            section_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            section_lbl.setStyleSheet(f"color: {MUTED}; font-size: 10px; letter-spacing: 1px;")
            self.b_seat_map_layout.addWidget(section_lbl)

            for row_index in range((len(type_seats) + seats_per_row - 1) // seats_per_row):
                row_seats = type_seats[row_index * seats_per_row:(row_index + 1) * seats_per_row]
                row_widget = QWidget()
                row_widget.setStyleSheet("background: transparent;")
                row_layout = QHBoxLayout(row_widget)
                row_layout.setContentsMargins(0, 0, 0, 0)
                row_layout.setSpacing(3)
                row_layout.addStretch()

                row_lbl = QLabel(str(row_index + 1))
                row_lbl.setFixedWidth(20)
                row_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                row_lbl.setStyleSheet(f"color: {MUTED}; font-size: 10px;")
                row_layout.addWidget(row_lbl)

                for col_index, (seat_id, seat_num, st, status) in enumerate(row_seats):
                    if col_index == 5:
                        row_layout.addSpacing(12)

                    seat_btn = QPushButton(seat_num)
                    seat_btn.setFixedSize(46, 28)
                    if status == "AVAILABLE":
                        seat_btn.setStyleSheet(self._staff_available_seat_style(available_colors.get(st, INPUT)))
                        seat_btn.clicked.connect(
                            lambda _, sid=seat_id, listing_ref=listing: self._toggle_staff_embedded_seat(sid, listing_ref)
                        )
                    else:
                        seat_btn.setStyleSheet(booked_style)
                        seat_btn.setEnabled(False)

                    self._b_seat_buttons[seat_id] = (seat_btn, st)
                    row_layout.addWidget(seat_btn)

                row_layout.addStretch()
                self.b_seat_map_layout.addWidget(row_widget)

        legend = QHBoxLayout()
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for color, label in [
            (available_colors["LOWER_HALL"], "Available"),
            ("#FDD835", "Selected"),
            ("#1a1c1e", "Booked"),
        ]:
            box = QLabel()
            box.setFixedSize(14, 14)
            box.setStyleSheet(f"background:{color}; border-radius:3px; border:1px solid {BORDER};")
            text = QLabel(label)
            text.setStyleSheet(f"color:{MUTED}; font-size:10px;")
            legend.addWidget(box)
            legend.addWidget(text)
            legend.addSpacing(12)
        self.b_seat_map_layout.addLayout(legend)
        self.b_seat_map_layout.addStretch()

    def _toggle_staff_embedded_seat(self, seat_id, listing):
        button, seat_type = self._b_seat_buttons[seat_id]
        if seat_id in self._selected_seat_ids:
            self._selected_seat_ids.remove(seat_id)
            button.setStyleSheet(self._staff_available_seat_style({
                "LOWER_HALL": "#3c4043",
                "UPPER_GALLERY": "#37404a",
                "VIP": "#3d2e00",
            }.get(seat_type, INPUT)))
        else:
            self._selected_seat_ids.append(seat_id)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FDD835; color: #202124;
                    border-radius: 3px; border: none;
                    font-size: 8px; font-weight: bold;
                }
            """)

        self._selected_seat_nums = [
            self._b_seat_data[sid][1]
            for sid in self._selected_seat_ids
        ]
        if self._selected_seat_nums:
            self.b_seats_info.setText(f"Seats: {', '.join(self._selected_seat_nums)}")
            total = self.booking_ctrl.calculate_price_for_seat_ids(
                self.user.assigned_cinema_id, listing.show_time_category, self._selected_seat_ids)
            self.price_lbl.setText(f"Total Price: £{total:.2f}")
        else:
            self.b_seats_info.setText("No seats selected")
            self.price_lbl.setText("")

    def _on_listing_changed(self, index):
        if index < 0:
            return
        listing_id = self.b_listing_id.currentData()
        if listing_id is None:
            self._set_staff_seat_map_visible(False)
            self._clear_staff_seat_map()
            return
        self._selected_seat_ids = []
        self._selected_seat_nums = []
        self.b_seats_info.setText("No seats selected")
        self.price_lbl.setText("")
        listings = self.film_ctrl.get_listings_for_cinema(self.user.assigned_cinema_id)
        listing = next((l for l in listings if l.listing_id == listing_id), None)
        if not listing:
            self.listing_info_lbl.setText("No listing found for this ID")
            self.listing_info_lbl.setStyleSheet(f"""
                background-color: {INPUT}; color: {DANGER};
                border: 1px solid {BORDER}; border-radius: 4px;
                padding: 8px 10px; font-size: 12px;
            """)
            self._set_staff_seat_map_visible(False)
            self._clear_staff_seat_map()
            return
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        film_title = films.get(listing.film_id, "Unknown Film")
        self.listing_info_lbl.setText(
            f"▶  {film_title}   |   {listing.show_date}   |   "
            f"{listing.show_time}   |   {listing.show_time_category.value}"
        )
        self.listing_info_lbl.setStyleSheet(f"""
            background-color: {INPUT}; color: {TEXT};
            border: 1px solid {ACCENT}; border-radius: 4px;
            padding: 8px 10px; font-size: 12px; font-weight: bold;
        """)
        self._set_staff_seat_map_visible(True)
        self._render_staff_seat_map(listing, film_title)

    def _open_seat_map(self):
        listing_id = self.b_listing_id.currentData()
        if listing_id is None:
            QMessageBox.warning(self, "Error", "Please select a listing first.")
            return
        listings = self.film_ctrl.get_listings_for_cinema(self.user.assigned_cinema_id)
        listing = next((l for l in listings if l.listing_id == listing_id), None)
        if not listing:
            QMessageBox.warning(self, "Error", "Listing not found.")
            return
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        film_title = films.get(listing.film_id, "Unknown Film")
        seats = self.booking_ctrl.get_seats_for_listing(listing_id)
        if not seats:
            QMessageBox.warning(self, "No Seats", "No seats found for this listing.")
            return
        dialog = SeatMapDialog(
            self, seats, film_title,
            str(listing.show_date), listing.show_time)
        if dialog.exec():
            selected = dialog.get_selected_seat_ids()
            if not selected:
                return
            self._selected_seat_ids = selected
            self._selected_seat_nums = [
                s[1] for s in seats if s[0] in selected]
            cinema_id = self.user.assigned_cinema_id
            total = self.booking_ctrl.calculate_price_for_seat_ids(
                cinema_id, listing.show_time_category, selected)
            self.b_seats_info.setText(
                f"Seats: {', '.join(self._selected_seat_nums)}")
            self.price_lbl.setText(f"Total Price: £{total:.2f}")

    def _confirm_booking(self):
        listing_id = self.b_listing_id.currentData()
        if listing_id is None:
            QMessageBox.warning(self, "Error", "Please select a listing first.")
            return
        name = self.b_name.text().strip()
        phone = self.b_phone.text().strip()
        email = self.b_email.text().strip()

        if not self._selected_seat_ids:
            QMessageBox.warning(self, "No Seats", "Please select seats first.")
            return
        if not name or not phone or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all customer details.")
            return

        listings = self.film_ctrl.get_listings_for_cinema(self.user.assigned_cinema_id)
        listing = next((l for l in listings if l.listing_id == listing_id), None)
        if not listing:
            QMessageBox.critical(self, "Error", "Listing not found or not available at your cinema.")
            return

        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        film_title = films.get(listing.film_id, "Unknown Film")
        cinema_id = self.user.assigned_cinema_id
        cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id)
        total_price = self.booking_ctrl.calculate_price_for_seat_ids(
            cinema_id, listing.show_time_category, self._selected_seat_ids)

        customer_id = self.booking_ctrl.get_customer_or_create(name, phone, email)
        if customer_id is None:
            QMessageBox.warning(
                self,
                "Invalid Customer Details",
                getattr(self.booking_ctrl, "last_error", "") or "Please check the customer details.")
            return

        booking_ref = self.booking_ctrl.create_booking_with_seats(
            self.user.user_id, listing_id, customer_id,
            self._selected_seat_ids, cinema_id,
            listing.show_time_category, self.user)

        if booking_ref:
            seat_nums = self._selected_seat_nums
            screen_number = self.booking_ctrl.get_screen_number_for_listing(listing_id)
            booking_date = self.booking_ctrl.get_booking_date_for_reference(booking_ref)
            self._selected_seat_ids = []
            self._selected_seat_nums = []
            for field in [self.b_name, self.b_phone, self.b_email]:
                field.clear()
            self.b_seats_info.setText("No seats selected")
            self.price_lbl.setText("")
            self._render_staff_seat_map(listing, film_title)
            ticket = TicketDialog(
                self, booking_ref, film_title, cinema_name, city_name,
                listing.show_date, listing.show_time,
                listing.show_time_category.value,
                ", ".join(seat_nums),
                len(seat_nums), total_price,
                screen_number, booking_date)
            ticket.exec()
        else:
            QMessageBox.critical(self, "Failed", "Booking failed. Please try again.")

    # ── Cancel Booking page ───────────────────────────────────────────────

    def _build_cancel_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        root = QVBoxLayout(widget)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(20)

        # Page header
        hdr = QVBoxLayout()
        hdr.setSpacing(4)
        title = QLabel("Cancel Booking")
        title.setStyleSheet(f"color: {TEXT}; font-size: 22px; font-weight: 700;")
        sub = QLabel("Void a reservation and issue a refund")
        sub.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
        hdr.addWidget(title)
        hdr.addWidget(sub)
        root.addLayout(hdr)

        # Content row — centred card
        content_row = QHBoxLayout()
        content_row.setSpacing(16)

        card = QFrame()
        card.setObjectName("actionCard")
        card.setStyleSheet(f"""
            QFrame#actionCard {{
                background-color: {CARD};
                border: 1px solid {BORDER};
                border-radius: 4px;
            }}
        """)
        card.setFixedWidth(520)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(14)

        card_title = QLabel("Void Reservation")
        card_title.setStyleSheet(
            f"color: {TEXT}; font-size: 14px; font-weight: 600; background: transparent;"
        )
        card_sub = QLabel("Enter the booking reference to cancel")
        card_sub.setStyleSheet(
            f"color: {MUTED}; font-size: 11px; background: transparent;"
        )
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet(f"color: {BORDER}; background: {BORDER}; max-height: 1px;")

        ref_lbl = QLabel("Booking Reference")
        ref_lbl.setStyleSheet(
            f"color: {MUTED}; font-size: 11px; font-weight: 500; background: transparent;"
        )

        self.cancel_ref = QLineEdit()
        self.cancel_ref.setPlaceholderText("e.g. BK-A3F92B1C")
        self.cancel_ref.setStyleSheet(UI_INPUT)

        cancel_btn = QPushButton("Cancel Booking")
        cancel_btn.setStyleSheet(UI_BTN_DANGER)
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self._cancel_booking)

        self.cancel_result = QLabel("")
        self.cancel_result.setWordWrap(True)
        self.cancel_result.setStyleSheet(
            f"color: {MUTED}; font-size: 12px; background: transparent;"
        )
        self.cancel_result.hide()

        cl.addWidget(card_title)
        cl.addWidget(card_sub)
        cl.addWidget(divider)
        cl.addWidget(ref_lbl)
        cl.addWidget(self.cancel_ref)
        cl.addWidget(cancel_btn)
        cl.addWidget(self.cancel_result)
        cl.addStretch()

        content_row.addStretch()
        content_row.addWidget(card)
        content_row.addStretch()

        root.addLayout(content_row)
        root.addStretch()
        return widget

    def _cancel_booking(self):
        ref = self.cancel_ref.text().strip()
        if not ref:
            QMessageBox.warning(self, "Input Error", "Please enter a booking reference.")
            return
        refund = self.cancel_ctrl.cancel_booking(ref, self.user)
        if refund is not None:
            self.cancel_result.setText(
                f"Booking {ref} cancelled. Refund: £{refund:.2f}")
            self.cancel_result.setStyleSheet(
                f"color: {ACCENT}; font-size: 12px; background: transparent;"
            )
            self.cancel_ref.clear()
        else:
            self.cancel_result.setText(
                getattr(self.cancel_ctrl, "last_error", "") or
                "Cancellation failed. Check the reference and try again.")
            self.cancel_result.setStyleSheet(
                f"color: {DANGER}; font-size: 12px; background: transparent;"
            )
        self.cancel_result.show()

    def _logout(self):
        from view.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()
