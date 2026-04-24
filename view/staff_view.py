from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QTabWidget, QLineEdit,
                              QComboBox, QCompleter, QSpinBox, QScrollArea, QMessageBox, QFrame,
                              QDialog, QGridLayout, QSizePolicy, QFileDialog)
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
        print_btn.setStyleSheet(BTN)
        print_btn.setFixedHeight(36)
        print_btn.clicked.connect(self._print_pdf)

        done_btn = QPushButton("Done")
        done_btn.setStyleSheet(BTN)
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
        self.setMinimumSize(900, 600)
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

        # Header
        header = QFrame()
        header.setStyleSheet(f"background-color: {CARD}; border-bottom: 1px solid {BORDER};")
        header.setFixedHeight(55)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(20, 0, 20, 0)

        title_lbl = QLabel("Horizon Cinemas")
        title_lbl.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT};")

        assigned_cinema = self._assigned_cinema_name()
        user_lbl = QLabel(f"  {self.user.full_name}  |  Booking Staff  |  {assigned_cinema}")
        user_lbl.setStyleSheet(f"color: {MUTED}; font-size: 12px;")

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet(BTN_DANGER)
        logout_btn.setFixedWidth(80)
        logout_btn.clicked.connect(self._logout)

        h_layout.addWidget(title_lbl)
        h_layout.addStretch()
        h_layout.addWidget(user_lbl)
        h_layout.addWidget(logout_btn)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{ border: none; background: {DARK}; }}
            QTabBar::tab {{
                background: {CARD}; color: {MUTED};
                padding: 10px 20px; font-size: 13px;
            }}
            QTabBar::tab:selected {{ color: {ACCENT};
                border-bottom: 2px solid {ACCENT}; }}
        """)

        self.tabs.addTab(self._build_listings_tab(), "Film Listings")
        self.tabs.addTab(self._build_booking_tab(), "Book Tickets")
        self.tabs.addTab(self._build_cancel_tab(), "Cancel Booking")

        main_layout.addWidget(header)
        main_layout.addWidget(self.tabs)

    def _build_listings_tab(self):
        widget = QWidget()
        widget.setStyleSheet(f"background-color: {DARK};")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        refresh_btn = QPushButton("Refresh Listings")
        refresh_btn.setStyleSheet(BTN)
        refresh_btn.setFixedWidth(150)
        refresh_btn.clicked.connect(self._load_listings)
        layout.addWidget(refresh_btn, alignment=Qt.AlignmentFlag.AlignLeft)

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

        listings = self.film_ctrl.get_listings_for_cinema(self.user.assigned_cinema_id)
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
            book_btn.setStyleSheet(BTN)
            book_btn.setFixedHeight(28)
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

    def _build_booking_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        def lbl(text):
            l = QLabel(text)
            l.setStyleSheet(f"color: {MUTED}; font-size: 11px;")
            return l

        self.b_listing_id = QComboBox()
        self.b_listing_id.setStyleSheet(INPUT_STYLE)
        self.b_listing_id.currentIndexChanged.connect(self._on_listing_changed)
        self._load_booking_listing_options()

        self.listing_info_lbl = QLabel("Select a listing ID to see film details")
        self.listing_info_lbl.setStyleSheet(f"""
            background-color: {INPUT}; color: {MUTED};
            border: 1px solid {BORDER}; border-radius: 4px;
            padding: 6px 8px; font-size: 11px;
        """)
        self.listing_info_lbl.setWordWrap(True)
        self.listing_info_lbl.setMinimumHeight(28)

        select_btn = QPushButton("Select Seats")
        select_btn.setStyleSheet(BTN)
        select_btn.clicked.connect(self._open_seat_map)

        self.b_seats_info = QLabel("No seats selected")
        self.b_seats_info.setStyleSheet(f"""
            background-color: {INPUT}; color: {MUTED};
            border: 1px solid {BORDER}; border-radius: 4px;
            padding: 6px 8px; font-size: 11px;
        """)
        self.b_seats_info.setWordWrap(True)

        self.price_lbl = QLabel("")
        self.price_lbl.setStyleSheet(f"color: {SUCCESS}; font-size: 12px;")

        self.b_name = QLineEdit()
        self.b_name.setPlaceholderText("Customer name")
        self.b_name.setStyleSheet(INPUT_STYLE)

        self.b_phone = QLineEdit()
        self.b_phone.setPlaceholderText("Phone number")
        self.b_phone.setStyleSheet(INPUT_STYLE)

        self.b_email = QLineEdit()
        self.b_email.setPlaceholderText("Email address")
        self.b_email.setStyleSheet(INPUT_STYLE)

        book_btn = QPushButton("Confirm Booking")
        book_btn.setStyleSheet(BTN)
        book_btn.clicked.connect(self._confirm_booking)

        layout.addWidget(lbl("Listing ID"))
        layout.addWidget(self.b_listing_id)
        layout.addWidget(self.listing_info_lbl)
        layout.addWidget(select_btn)
        layout.addWidget(self.b_seats_info)
        layout.addWidget(self.price_lbl)
        for w, l in [
            (self.b_name,  "Customer Name"),
            (self.b_phone, "Customer Phone"),
            (self.b_email, "Customer Email"),
        ]:
            layout.addWidget(lbl(l))
            layout.addWidget(w)
        layout.addStretch()
        layout.addWidget(book_btn)
        return widget

    def _book_from_listing(self, listing_id):
        index = self.b_listing_id.findData(listing_id)
        if index >= 0:
            self.b_listing_id.setCurrentIndex(index)
        self.tabs.setCurrentIndex(1)

    def _load_booking_listing_options(self):
        listings = self.film_ctrl.get_all_listings()
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        
        self.b_listing_id.blockSignals(True)
        self.b_listing_id.clear()
        
        for listing in listings:
            film_title = films.get(listing.film_id, "Unknown")
            display_text = f"{film_title} - {listing.show_date} {listing.show_time}"
            self.b_listing_id.addItem(display_text, listing.listing_id)
        
        # Set up searchable completer
        self.b_listing_id.setEditable(True)
        self.b_listing_id.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.b_listing_id.setCurrentText("")
        self.b_listing_id.lineEdit().setPlaceholderText("Search listing")
        completer = self.b_listing_id.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        
        self.b_listing_id.blockSignals(False)

    def _on_listing_changed(self, index):
        if index < 0:
            return
        listing_id = self.b_listing_id.currentData()
        if listing_id is None:
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
            self.price_lbl.setText(f"Total Price: \u00a3{total}")
            self.price_lbl.setStyleSheet(f"color: {SUCCESS}; font-size: 13px;")

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

        booking_ref = self.booking_ctrl.create_booking_with_seats(
            self.user.user_id, listing_id, customer_id,
            self._selected_seat_ids, cinema_id,
            listing.show_time_category)

        if booking_ref:
            seat_nums = self._selected_seat_nums
            screen_number = self.booking_ctrl.get_screen_number_for_listing(listing_id)
            booking_date = self.booking_ctrl.get_booking_date_for_reference(booking_ref)
            self._selected_seat_ids = []
            self._selected_seat_nums = []
            self.b_seats_info.setText("No seats selected")
            self.price_lbl.setText("")
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

    def _build_cancel_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        ref_lbl = QLabel("Booking Reference")
        ref_lbl.setStyleSheet(f"color: {MUTED}; font-size: 12px;")

        self.cancel_ref = QLineEdit()
        self.cancel_ref.setPlaceholderText("e.g. BK-A3F92B1C")
        self.cancel_ref.setStyleSheet(INPUT_STYLE)

        cancel_btn = QPushButton("Cancel Booking")
        cancel_btn.setStyleSheet(BTN_DANGER)
        cancel_btn.clicked.connect(self._cancel_booking)

        self.cancel_result = QLabel("")
        self.cancel_result.setStyleSheet(f"color: {MUTED}; font-size: 13px;")

        layout.addWidget(ref_lbl)
        layout.addWidget(self.cancel_ref)
        layout.addWidget(cancel_btn)
        layout.addWidget(self.cancel_result)
        layout.addStretch()
        return widget

    def _cancel_booking(self):
        ref = self.cancel_ref.text().strip()
        if not ref:
            QMessageBox.warning(self, "Input Error", "Please enter a booking reference.")
            return
        refund = self.cancel_ctrl.cancel_booking(ref)
        if refund is not None:
            self.cancel_result.setText(
                f"Booking {ref} cancelled.\nRefund amount: £{refund:.2f}")
            self.cancel_result.setStyleSheet(f"color: {SUCCESS}; font-size: 13px;")
        else:
            self.cancel_result.setText(
                "Cancellation failed. Check the reference or the show may be today/past.")
            self.cancel_result.setStyleSheet(f"color: {DANGER}; font-size: 13px;")

    def _logout(self):
        from view.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()
