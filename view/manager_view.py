from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                              QLineEdit, QComboBox, QSpinBox, QCompleter,
                              QMessageBox, QFrame, QHeaderView, QDoubleSpinBox,
                              QDateEdit, QTimeEdit, QScrollArea,
                              QDialog, QStackedWidget, QButtonGroup, QGridLayout)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QColor
import datetime
import os as _os
from controller.cinema_controller import CinemaController
from controller.film_controller import FilmController
from controller.auth_controller import AuthController
from controller.report_factory import ReportFactory
from controller.booking_controller import BookingController
from controller.cancellation_controller import CancellationController
from view.staff_view import TicketDialog

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
        background-color: {ACCENT}; color: {DARK};
        font-weight: 600; font-size: 12px;
        border-radius: 7px; padding: 10px 16px; border: none;
    }}
    QPushButton:hover {{ background-color: #aecbfa; }}
    QPushButton:pressed {{ background-color: #7aa7f7; }}
"""
BTN_DANGER = f"""
    QPushButton {{
        background-color: {DANGER}; color: {DARK};
        font-weight: 600; font-size: 12px;
        border-radius: 7px; padding: 10px 16px; border: none;
    }}
    QPushButton:hover {{ background-color: #ee675c; }}
    QPushButton:pressed {{ background-color: #d05a52; }}
"""
BTN_GHOST = f"""
    QPushButton {{
        background-color: transparent; color: {TEXT};
        font-weight: 500; font-size: 12px;
        border-radius: 7px; padding: 9px 14px;
        border: 1px solid #3a3b3f;
    }}
    QPushButton:hover {{ background-color: #2a2b2f; border-color: #50525a; }}
"""
INPUT_STYLE = f"""
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QDateEdit, QTimeEdit {{
        background-color: #1c1d20;
        color: {TEXT};
        border: 1px solid #3a3b3f;
        border-radius: 6px;
        padding: 8px 11px;
        font-size: 12px;
        min-height: 18px;
    }}
    QLineEdit:hover, QComboBox:hover, QSpinBox:hover,
    QDoubleSpinBox:hover, QDateEdit:hover, QTimeEdit:hover {{
        border: 1px solid #50525a;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
    QDoubleSpinBox:focus, QDateEdit:focus, QTimeEdit:focus {{
        border: 1px solid {ACCENT}; background-color: #1f2024;
    }}
    QComboBox::drop-down, QDateEdit::drop-down, QTimeEdit::drop-down {{
        border: none; width: 22px;
    }}
    QComboBox QAbstractItemView {{
        background-color: #1c1d20; color: {TEXT};
        border: 1px solid {BORDER};
        selection-background-color: {ACCENT};
        selection-color: {DARK}; outline: none;
    }}
"""

_ARROW_PATH = _os.path.join(_os.path.dirname(__file__), "chevron_down.svg").replace("\\", "/")

SEARCH_COMBO_STYLE = INPUT_STYLE + f"""
    QComboBox {{
        padding-right: 36px;
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 34px;
        border: none;
        border-left: 1px solid #3a3b3f;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
        background-color: #25262a;
    }}
    QComboBox::drop-down:hover {{
        background-color: #2e2f33;
    }}
    QComboBox::down-arrow {{
        image: url({_ARROW_PATH});
        width: 12px;
        height: 12px;
    }}
    QComboBox QLineEdit {{
        background: transparent;
        color: {TEXT};
        border: none;
        padding: 0;
        selection-background-color: {ACCENT};
    }}
"""

TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {CARD}; color: {TEXT};
        gridline-color: transparent; border: none;
        font-size: 13px; outline: none;
    }}
    QHeaderView {{ background-color: {CARD}; }}
    QHeaderView::section {{
        background-color: {CARD}; color: {MUTED};
        font-weight: 600; font-size: 10px;
        padding: 13px 16px; border: none;
        border-bottom: 1px solid {BORDER};
        text-transform: uppercase; letter-spacing: 0.7px;
    }}
    QTableWidget::item {{
        padding: 11px 16px; border: none;
        border-bottom: 1px solid #2f3035;
    }}
    QTableWidget::item:selected {{
        background-color: rgba(138, 180, 248, 0.14); color: {TEXT};
    }}
    QTableCornerButton::section {{
        background-color: {CARD}; border: none;
        border-bottom: 1px solid {BORDER};
    }}
    QScrollBar:vertical {{ background: transparent; width: 8px; margin: 4px; }}
    QScrollBar::handle:vertical {{
        background: #3a3b3f; border-radius: 4px; min-height: 24px;
    }}
    QScrollBar::handle:vertical:hover {{ background: #50525a; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
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
    QLabel {{
        border: none;
        background-color: transparent;
    }}
"""


def _session_for_qtime(qtime):
    from models.enums import ShowTime

    hour = qtime.hour()
    if hour < 12:
        return ShowTime.MORNING
    if hour < 18:
        return ShowTime.AFTERNOON
    return ShowTime.EVENING


def _listing_is_bookable(listing):
    show_time = listing.show_time
    if hasattr(show_time, "hour"):
        start_time = datetime.time(show_time.hour, show_time.minute, getattr(show_time, "second", 0))
    else:
        total_seconds = int(show_time.total_seconds())
        start_time = (datetime.datetime.min + datetime.timedelta(seconds=total_seconds)).time()
    return datetime.datetime.combine(listing.show_date, start_time) >= datetime.datetime.now()


class ManagerView(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.cinema_ctrl = CinemaController()
        self.film_ctrl = FilmController()
        self.auth_ctrl = AuthController()
        self.booking_ctrl = BookingController()
        self.cancel_ctrl = CancellationController()
        self.setWindowTitle(f"Horizon Cinemas - Manager: {user.full_name}")
        self.setMinimumSize(1180, 760)
        self._build_ui()

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

        subtitle_lbl = QLabel("Manager portal")
        subtitle_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        user_lbl = QLabel(f"  {self.user.full_name}  |  Manager")
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

        pages_config = [
            ("Films",             "Add, edit and remove films from the catalogue",   self._build_films_tab()),
            ("Cinemas",           "Manage cinema locations",                          self._build_cinemas_tab()),
            ("Screens",           "Configure screens and seating capacity",           self._build_screens_tab()),
            ("Listings",          "Schedule and manage upcoming film listings",       self._build_listings_tab()),
            ("Listing History",   "Past film listings at all cinemas",                self._build_listing_history_tab()),
            ("Book Tickets",      "Select a listing, choose seats and confirm",       self._build_booking_tab()),
            ("Cancel Booking",    "Void a reservation and issue a refund",            self._build_cancel_tab()),
            ("User Registration", "Create and manage staff and admin accounts",       self._build_user_registration_tab()),
            ("Cities & Pricing",  "Manage city locations and ticket pricing",         self._build_pricing_tab()),
            ("Reports",           "Generate operational reports",                     self._build_reports_tab()),
        ]

        for index, (label, pg_sub, page_widget) in enumerate(pages_config):
            wrapped = self._wrap_page(label, pg_sub, page_widget)
            self.pages.addWidget(wrapped)
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
            0: [self._load_films],
            1: [self._load_cinemas],
            2: [
                lambda: self._load_cinema_options(self.s_cinema_selector),
                lambda: self._load_cinema_options(self.s_cinema_combo),
            ],
            3: [
                lambda: self._load_film_options(self.l_edit_film_id),
                lambda: self._load_screen_options(self.l_edit_screen_combo),
                self._load_listings,
            ],
            4: [self._load_listing_history],
            5: [self._load_manager_booking_listing_options],
            7: [
                lambda: self._load_cinema_options(self.reg_cinema_combo),
                self._load_registered_users,
            ],
            8: [
                lambda: self._load_city_options(self.p_city_combo),
                self._load_pricing,
            ],
        }
        for refresh in refreshers.get(index, []):
            refresh()

    def _wrap_page(self, title, subtitle, inner_widget):
        container = QWidget()
        container.setObjectName("pageShell")
        outer = QVBoxLayout(container)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        hdr = QWidget()
        hdr.setStyleSheet(f"background: {DARK};")
        hdr_layout = QVBoxLayout(hdr)
        hdr_layout.setContentsMargins(28, 20, 28, 4)
        hdr_layout.setSpacing(4)
        pg_title = QLabel(title)
        pg_title.setStyleSheet(f"color: {TEXT}; font-size: 22px; font-weight: 700;")
        pg_sub_lbl = QLabel(subtitle)
        pg_sub_lbl.setStyleSheet(f"color: {MUTED}; font-size: 13px;")
        hdr_layout.addWidget(pg_title)
        hdr_layout.addWidget(pg_sub_lbl)

        outer.addWidget(hdr)
        outer.addWidget(inner_widget, 1)
        return container

    # ── Films tab ─────────────────────────────────────────────────────────────
    def _build_films_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Left: table card
        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setStyleSheet(CARD_STYLE)
        tc_lay = QVBoxLayout(tc)
        tc_lay.setContentsMargins(1, 1, 1, 1)
        tc_lay.setSpacing(0)
        tc_hdr = QWidget()
        tc_hdr.setFixedHeight(60)
        tc_hdr.setStyleSheet(f"background: {CARD};")
        hhl = QHBoxLayout(tc_hdr)
        hhl.setContentsMargins(16, 0, 16, 0)
        hhl.setSpacing(10)
        tc_ttl = QLabel("Film Catalogue")
        tc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        self.films_badge = QLabel("0")
        self.films_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        ref_btn = QPushButton("Refresh")
        ref_btn.setStyleSheet(BTN_GHOST)
        ref_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ref_btn.setFixedHeight(32)
        ref_btn.clicked.connect(self._load_films)
        hhl.addWidget(tc_ttl)
        hhl.addStretch()
        hhl.addWidget(ref_btn)
        tc_div = QWidget()
        tc_div.setFixedHeight(1)
        tc_div.setStyleSheet(f"background: {BORDER};")
        self.films_table = QTableWidget()
        self.films_table.setStyleSheet(TABLE_STYLE)
        self.films_table.setColumnCount(5)
        self.films_table.setHorizontalHeaderLabels(["ID", "Title", "Genre", "Rating", "Duration"])
        self.films_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.films_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.films_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.films_table.verticalHeader().setVisible(False)
        self.films_table.itemSelectionChanged.connect(self._on_film_row_selected)
        tc_lay.addWidget(tc_hdr)
        tc_lay.addWidget(tc_div)
        tc_lay.addWidget(self.films_table)

        # Right: scrollable form panel
        scroll = QScrollArea()
        scroll.setFixedWidth(300)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{ background: transparent; width: 6px; border-radius: 3px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 3px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)
        ri = QWidget()
        ri.setStyleSheet("background: transparent;")
        ri_lay = QVBoxLayout(ri)
        ri_lay.setContentsMargins(0, 0, 4, 0)
        ri_lay.setSpacing(12)
        scroll.setWidget(ri)

        def fl(text):
            lb = QLabel(text.upper())
            lb.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
            return lb

        def mk_card(title):
            c = QFrame()
            c.setObjectName("formCard")
            c.setStyleSheet(CARD_STYLE)
            cl = QVBoxLayout(c)
            cl.setContentsMargins(16, 14, 16, 16)
            cl.setSpacing(9)
            t = QLabel(title)
            t.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
            s = QWidget()
            s.setFixedHeight(1)
            s.setStyleSheet(f"background: {BORDER};")
            cl.addWidget(t)
            cl.addWidget(s)
            return c, cl

        # Add Film card
        add_card, acl = mk_card("Add Film")
        self.f_title = QLineEdit()
        self.f_title.setPlaceholderText("Film title")
        self.f_title.setStyleSheet(INPUT_STYLE)
        self.f_genre = QLineEdit()
        self.f_genre.setPlaceholderText("e.g. Action, Drama")
        self.f_genre.setStyleSheet(INPUT_STYLE)
        self.f_age_rating = QComboBox()
        self.f_age_rating.addItems(["U", "PG", "12A", "12", "15", "18"])
        self.f_age_rating.setStyleSheet(INPUT_STYLE)
        self.f_imdb = QDoubleSpinBox()
        self.f_imdb.setRange(0.0, 10.0)
        self.f_imdb.setSingleStep(0.1)
        self.f_imdb.setDecimals(1)
        self.f_imdb.setStyleSheet(INPUT_STYLE)
        self.f_duration = QSpinBox()
        self.f_duration.setRange(1, 300)
        self.f_duration.setSuffix(" mins")
        self.f_duration.setStyleSheet(INPUT_STYLE)
        self.f_year = QSpinBox()
        self.f_year.setRange(1900, 2100)
        self.f_year.setValue(2025)
        self.f_year.setStyleSheet(INPUT_STYLE)
        self.f_cast = QLineEdit()
        self.f_cast.setPlaceholderText("Actor 1, Actor 2, ...")
        self.f_cast.setStyleSheet(INPUT_STYLE)
        self.f_desc = QLineEdit()
        self.f_desc.setPlaceholderText("Short description")
        self.f_desc.setStyleSheet(INPUT_STYLE)
        add_film_btn = QPushButton("Add Film")
        add_film_btn.setStyleSheet(BTN)
        add_film_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_film_btn.clicked.connect(self._add_film)
        for w, lbl_text in [
            (self.f_title, "Title"), (self.f_genre, "Genre"),
            (self.f_age_rating, "Age Rating"), (self.f_imdb, "IMDb Rating"),
            (self.f_duration, "Duration"), (self.f_year, "Release Year"),
            (self.f_cast, "Cast Members"), (self.f_desc, "Description"),
        ]:
            acl.addWidget(fl(lbl_text))
            acl.addWidget(w)
        acl.addWidget(add_film_btn)

        # Remove Film card
        rm_card, rcl = mk_card("Remove Film")
        self.f_remove_id = QSpinBox()
        self.f_remove_id.setRange(1, 9999)
        self.f_remove_id.setStyleSheet(INPUT_STYLE)
        rm_btn = QPushButton("Remove Film")
        rm_btn.setStyleSheet(BTN_DANGER)
        rm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        rm_btn.clicked.connect(self._remove_film)
        rcl.addWidget(fl("Film ID"))
        rcl.addWidget(self.f_remove_id)
        rcl.addWidget(rm_btn)

        # Update Film card
        upd_card, ucl = mk_card("Update Film")
        load_row = QHBoxLayout()
        self.f_load_id = QSpinBox()
        self.f_load_id.setRange(1, 9999)
        self.f_load_id.setStyleSheet(INPUT_STYLE)
        load_btn = QPushButton("Load")
        load_btn.setStyleSheet(BTN_GHOST)
        load_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_btn.setFixedWidth(60)
        load_btn.clicked.connect(lambda: self._load_film_for_edit())
        load_row.addWidget(self.f_load_id)
        load_row.addWidget(load_btn)
        self.u_title = QLineEdit()
        self.u_title.setPlaceholderText("Title")
        self.u_title.setStyleSheet(INPUT_STYLE)
        self.u_genre = QLineEdit()
        self.u_genre.setPlaceholderText("Genre")
        self.u_genre.setStyleSheet(INPUT_STYLE)
        self.u_age_rating = QComboBox()
        self.u_age_rating.addItems(["U", "PG", "12A", "12", "15", "18"])
        self.u_age_rating.setStyleSheet(INPUT_STYLE)
        self.u_imdb = QDoubleSpinBox()
        self.u_imdb.setRange(0.0, 10.0)
        self.u_imdb.setSingleStep(0.1)
        self.u_imdb.setDecimals(1)
        self.u_imdb.setStyleSheet(INPUT_STYLE)
        self.u_duration = QSpinBox()
        self.u_duration.setRange(1, 300)
        self.u_duration.setSuffix(" mins")
        self.u_duration.setStyleSheet(INPUT_STYLE)
        self.u_year = QSpinBox()
        self.u_year.setRange(1900, 2100)
        self.u_year.setValue(2025)
        self.u_year.setStyleSheet(INPUT_STYLE)
        self.u_cast = QLineEdit()
        self.u_cast.setPlaceholderText("Cast members")
        self.u_cast.setStyleSheet(INPUT_STYLE)
        self.u_desc = QLineEdit()
        self.u_desc.setPlaceholderText("Description")
        self.u_desc.setStyleSheet(INPUT_STYLE)
        save_btn = QPushButton("Save Changes")
        save_btn.setStyleSheet(BTN)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._update_film)
        ucl.addWidget(fl("Film ID to Edit"))
        ucl.addLayout(load_row)
        for w, lbl_text in [
            (self.u_title, "Title"), (self.u_genre, "Genre"),
            (self.u_age_rating, "Age Rating"), (self.u_imdb, "IMDb Rating"),
            (self.u_duration, "Duration"), (self.u_year, "Release Year"),
            (self.u_cast, "Cast Members"), (self.u_desc, "Description"),
        ]:
            ucl.addWidget(fl(lbl_text))
            ucl.addWidget(w)
        ucl.addWidget(save_btn)

        ri_lay.addWidget(add_card)
        ri_lay.addWidget(rm_card)
        ri_lay.addWidget(upd_card)
        ri_lay.addStretch()

        layout.addWidget(tc, 1)
        layout.addWidget(scroll)
        self._load_films()
        return widget

    def _load_films(self):
        films = self.film_ctrl.get_all_films()
        self.films_table.setRowCount(len(films))
        for i, f in enumerate(films):
            self.films_table.setItem(i, 0, QTableWidgetItem(str(f.film_id)))
            self.films_table.setItem(i, 1, QTableWidgetItem(f.title))
            self.films_table.setItem(i, 2, QTableWidgetItem(f.genre))
            self.films_table.setItem(i, 3, QTableWidgetItem(str(f.age_rating)))
            self.films_table.setItem(i, 4, QTableWidgetItem(f"{f.duration} mins"))
        if hasattr(self, "films_badge"):
            self.films_badge.setText(str(len(films)))

    def _add_film(self):
        title = self.f_title.text().strip()
        genre = self.f_genre.text().strip()
        if not title or not genre:
            QMessageBox.warning(self, "Input Error", "Title and genre are required.")
            return
        ok = self.film_ctrl.add_film(
            title, self.f_desc.text().strip(), genre,
            self.f_age_rating.currentText(),
            self.f_imdb.value(), self.f_duration.value(),
            self.f_cast.text().strip(), self.f_year.value())
        if ok:
            QMessageBox.information(self, "Success", f"'{title}' added.")
            for field in [self.f_title, self.f_genre, self.f_cast, self.f_desc]:
                field.clear()
            self.f_age_rating.setCurrentIndex(0)
            self.f_imdb.setValue(0.0)
            self.f_duration.setValue(1)
            self.f_year.setValue(2025)
            self._load_films()
            if hasattr(self, "l_edit_film_id"):
                self._load_film_options(self.l_edit_film_id)
        else:
            QMessageBox.critical(self, "Failed", "Could not add film.")

    def _remove_film(self):
        film_id = self.f_remove_id.value()
        reply = QMessageBox.question(
            self, "Confirm", f"Remove film ID {film_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            ok = self.film_ctrl.remove_film(film_id)
            if ok:
                QMessageBox.information(self, "Removed", "Film removed.")
                self._load_films()
                if hasattr(self, "l_edit_film_id"):
                    self._load_film_options(self.l_edit_film_id)
                if hasattr(self, "listings_table"):
                    self._load_listings()
                if hasattr(self, "m_listing_id"):
                    self._load_manager_booking_listing_options()
            else:
                QMessageBox.critical(
                    self,
                    "Failed",
                    getattr(self.film_ctrl, "last_error", "")
                    or "Could not remove film.",
                )

    def _on_film_row_selected(self):
        if not self.films_table.selectedItems():
            return
        row = self.films_table.currentRow()
        id_item = self.films_table.item(row, 0)
        if not id_item:
            return
        film_id = int(id_item.text())
        self.f_load_id.setValue(film_id)
        self.f_remove_id.setValue(film_id)
        self._load_film_for_edit(show_warning=False)

    def _load_film_for_edit(self, show_warning=True):
        film = self.film_ctrl.get_film_by_id(self.f_load_id.value())
        if not film:
            if show_warning:
                QMessageBox.warning(self, "Not Found", "No film found with that ID.")
            return
        self.u_title.setText(film.title)
        self.u_genre.setText(film.genre)
        idx = self.u_age_rating.findText(str(film.age_rating))
        if idx >= 0:
            self.u_age_rating.setCurrentIndex(idx)
        self.u_imdb.setValue(float(film.imdb_rating))
        self.u_duration.setValue(int(film.duration))
        self.u_year.setValue(int(film.release_year))
        self.u_cast.setText(film.cast_members or "")
        self.u_desc.setText(film.description or "")

    def _update_film(self):
        film_id = self.f_load_id.value()
        title = self.u_title.text().strip()
        genre = self.u_genre.text().strip()
        if not title or not genre:
            QMessageBox.warning(self, "Input Error", "Title and genre are required.")
            return
        ok = self.film_ctrl.update_film(
            film_id, title, self.u_desc.text().strip(), genre,
            self.u_age_rating.currentText(),
            self.u_imdb.value(), self.u_duration.value(),
            self.u_cast.text().strip(), self.u_year.value())
        if ok:
            QMessageBox.information(self, "Success", f"Film ID {film_id} updated.")
            self.f_load_id.setValue(1)
            for field in [self.u_title, self.u_genre, self.u_cast, self.u_desc]:
                field.clear()
            self.u_age_rating.setCurrentIndex(0)
            self.u_imdb.setValue(0.0)
            self.u_duration.setValue(1)
            self.u_year.setValue(2025)
            self._load_films()
        else:
            QMessageBox.critical(self, "Failed", "Update failed. Check the Film ID.")

    # ── Cinemas tab ───────────────────────────────────────────────────────────
    def _build_cinemas_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Left: table card
        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setStyleSheet(CARD_STYLE)
        tc_lay = QVBoxLayout(tc)
        tc_lay.setContentsMargins(1, 1, 1, 1)
        tc_lay.setSpacing(0)
        tc_hdr = QWidget()
        tc_hdr.setFixedHeight(60)
        tc_hdr.setStyleSheet(f"background: {CARD};")
        hhl = QHBoxLayout(tc_hdr)
        hhl.setContentsMargins(16, 0, 16, 0)
        hhl.setSpacing(10)
        tc_ttl = QLabel("Cinemas")
        tc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        self.cinemas_badge = QLabel("0")
        self.cinemas_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        ref_btn = QPushButton("Refresh")
        ref_btn.setStyleSheet(BTN_GHOST)
        ref_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ref_btn.setFixedHeight(32)
        ref_btn.clicked.connect(self._load_cinemas)
        hhl.addWidget(tc_ttl)
        hhl.addStretch()
        hhl.addWidget(ref_btn)
        tc_div = QWidget()
        tc_div.setFixedHeight(1)
        tc_div.setStyleSheet(f"background: {BORDER};")
        self.cinemas_table = QTableWidget()
        self.cinemas_table.setStyleSheet(TABLE_STYLE)
        self.cinemas_table.setColumnCount(4)
        self.cinemas_table.setHorizontalHeaderLabels(["Cinema ID", "Cinema Name", "Location", "City"])
        self.cinemas_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cinemas_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cinemas_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cinemas_table.verticalHeader().setVisible(False)
        tc_lay.addWidget(tc_hdr)
        tc_lay.addWidget(tc_div)
        tc_lay.addWidget(self.cinemas_table)

        # Right: form card
        fc = QFrame()
        fc.setObjectName("formCard")
        fc.setStyleSheet(CARD_STYLE)
        fc.setFixedWidth(280)
        fcl = QVBoxLayout(fc)
        fcl.setContentsMargins(16, 14, 16, 16)
        fcl.setSpacing(9)
        fc_ttl = QLabel("Add Cinema")
        fc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        fc_sep = QWidget()
        fc_sep.setFixedHeight(1)
        fc_sep.setStyleSheet(f"background: {BORDER};")
        fcl.addWidget(fc_ttl)
        fcl.addWidget(fc_sep)

        def fl(text):
            lb = QLabel(text.upper())
            lb.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
            return lb

        self.c_name = QLineEdit()
        self.c_name.setPlaceholderText("Cinema name")
        self.c_name.setStyleSheet(INPUT_STYLE)
        self.c_location = QLineEdit()
        self.c_location.setPlaceholderText("e.g. City Centre")
        self.c_location.setStyleSheet(INPUT_STYLE)
        self.c_city_combo = QComboBox()
        self.c_city_combo.setStyleSheet(INPUT_STYLE)
        add_cinema_btn = QPushButton("Add Cinema")
        add_cinema_btn.setStyleSheet(BTN)
        add_cinema_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_cinema_btn.clicked.connect(self._add_cinema)
        for w, lbl_text in [
            (self.c_name, "Name"), (self.c_location, "Location"), (self.c_city_combo, "City"),
        ]:
            fcl.addWidget(fl(lbl_text))
            fcl.addWidget(w)
        fcl.addWidget(add_cinema_btn)
        fcl.addStretch()

        layout.addWidget(tc, 1)
        layout.addWidget(fc)
        self._load_city_options(self.c_city_combo)
        self._load_cinemas()
        return widget

    def _load_city_options(self, combo, selected_city_id=None):
        combo.blockSignals(True)
        combo.clear()

        cities = self.cinema_ctrl.get_all_cities()
        for city in cities:
            combo.addItem(city.name, city.city_id)

        combo.setEditable(True)
        combo.setStyleSheet(SEARCH_COMBO_STYLE)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setCurrentText("")
        combo.lineEdit().setPlaceholderText("Search city")
        completer = combo.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        if not cities:
            combo.addItem("No cities available", None)
            combo.setEnabled(False)
        else:
            combo.setEnabled(True)
            if selected_city_id is not None:
                index = combo.findData(selected_city_id)
                if index >= 0:
                    combo.setCurrentIndex(index)

        combo.blockSignals(False)

    def _selected_city_id(self, combo):
        city_id = combo.currentData()
        return int(city_id) if city_id is not None else None

    def _load_cinemas(self):
        cinemas = self.cinema_ctrl.get_all_cinemas()
        city_map = {city.city_id: city.name for city in self.cinema_ctrl.get_all_cities()}
        self.cinemas_table.setRowCount(len(cinemas))
        for i, c in enumerate(cinemas):
            self.cinemas_table.setItem(i, 0, QTableWidgetItem(str(c.cinema_id)))
            self.cinemas_table.setItem(i, 1, QTableWidgetItem(c.name))
            self.cinemas_table.setItem(i, 2, QTableWidgetItem(c.location))
            self.cinemas_table.setItem(i, 3, QTableWidgetItem(city_map.get(c.city_id, "Unknown")))
        if hasattr(self, "cinemas_badge"):
            self.cinemas_badge.setText(str(len(cinemas)))

    def _add_cinema(self):
        name = self.c_name.text().strip()
        location = self.c_location.text().strip()
        if not name or not location:
            QMessageBox.warning(self, "Input Error", "Name and location are required.")
            return
        city_id = self._selected_city_id(self.c_city_combo)
        if city_id is None:
            QMessageBox.warning(self, "Input Error", "Please select a city.")
            return
        ok = self.cinema_ctrl.add_cinema(name, location, city_id)
        if ok:
            QMessageBox.information(self, "Success", f"'{name}' added.")
            self.c_name.clear()
            self.c_location.clear()
            self.c_city_combo.setCurrentIndex(-1)
            self._load_cinemas()
            for combo_name in ("s_cinema_selector", "s_cinema_combo"):
                if hasattr(self, combo_name):
                    self._load_cinema_options(getattr(self, combo_name))
        else:
            QMessageBox.critical(self, "Failed", "Could not add cinema. Check the selected city.")

    # ── Screens tab ───────────────────────────────────────────────────────────
    def _build_screens_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Left: selector strip + table card
        left = QWidget()
        left.setStyleSheet("background: transparent;")
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        left_lay.setSpacing(10)

        sel_strip = QWidget()
        sel_strip.setStyleSheet("background: transparent;")
        ssl = QHBoxLayout(sel_strip)
        ssl.setContentsMargins(0, 0, 0, 0)
        ssl.setSpacing(10)
        sel_lbl = QLabel("CINEMA")
        sel_lbl.setStyleSheet(
            f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
        self.s_cinema_selector = QComboBox()
        self.s_cinema_selector.setFixedWidth(280)
        self.s_cinema_selector.setStyleSheet(INPUT_STYLE)
        load_screens_btn = QPushButton("Load Screens")
        load_screens_btn.setStyleSheet(BTN)
        load_screens_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        load_screens_btn.clicked.connect(self._load_screens)
        ssl.addWidget(sel_lbl)
        ssl.addWidget(self.s_cinema_selector)
        ssl.addWidget(load_screens_btn)
        ssl.addStretch()

        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setStyleSheet(CARD_STYLE)
        tc_lay = QVBoxLayout(tc)
        tc_lay.setContentsMargins(1, 1, 1, 1)
        tc_lay.setSpacing(0)
        tc_hdr = QWidget()
        tc_hdr.setFixedHeight(52)
        tc_hdr.setStyleSheet(f"background: {CARD};")
        hhl = QHBoxLayout(tc_hdr)
        hhl.setContentsMargins(16, 0, 16, 0)
        hhl.setSpacing(10)
        tc_ttl = QLabel("Screens")
        tc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        self.screens_badge = QLabel("0")
        self.screens_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        hhl.addWidget(tc_ttl)
        hhl.addStretch()
        tc_div = QWidget()
        tc_div.setFixedHeight(1)
        tc_div.setStyleSheet(f"background: {BORDER};")
        self.screens_table = QTableWidget()
        self.screens_table.setStyleSheet(TABLE_STYLE)
        self.screens_table.setColumnCount(4)
        self.screens_table.setHorizontalHeaderLabels(["Screen ID", "Cinema", "Screen No.", "Capacity"])
        self.screens_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.screens_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.screens_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.screens_table.verticalHeader().setVisible(False)
        self.screens_table.itemSelectionChanged.connect(self._on_screen_row_selected)
        tc_lay.addWidget(tc_hdr)
        tc_lay.addWidget(tc_div)
        tc_lay.addWidget(self.screens_table)

        left_lay.addWidget(sel_strip)
        left_lay.addWidget(tc, 1)

        # Right: Configure Screen form card
        fc = QFrame()
        fc.setObjectName("formCard")
        fc.setStyleSheet(CARD_STYLE)
        fc.setFixedWidth(280)
        fcl = QVBoxLayout(fc)
        fcl.setContentsMargins(16, 14, 16, 16)
        fcl.setSpacing(9)
        fc_ttl = QLabel("Configure Screen")
        fc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        fc_sep = QWidget()
        fc_sep.setFixedHeight(1)
        fc_sep.setStyleSheet(f"background: {BORDER};")
        fcl.addWidget(fc_ttl)
        fcl.addWidget(fc_sep)

        def fl(text):
            lb = QLabel(text.upper())
            lb.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
            return lb

        self.s_cfg_note = QLabel(
            "Seats are created automatically for each new screen:\n"
            "30% Lower Hall · 10 VIP · rest Upper Gallery")
        self.s_cfg_note.setStyleSheet(f"color: {MUTED}; font-size: 11px;")
        self.s_cfg_note.setWordWrap(True)
        self.s_cinema_combo = QComboBox()
        self.s_cinema_combo.setStyleSheet(INPUT_STYLE)
        self.s_mode = QComboBox()
        self.s_mode.addItems(["Add New Screens", "Configure Existing Screen"])
        self.s_mode.setStyleSheet(INPUT_STYLE)
        self.s_mode.currentTextChanged.connect(self._on_screen_mode_changed)
        self.s_screen_number = QSpinBox()
        self.s_screen_number.setRange(1, 200)
        self.s_screen_number.setValue(1)
        self.s_screen_number.setStyleSheet(INPUT_STYLE)
        self.s_screen_count = QSpinBox()
        self.s_screen_count.setRange(1, 50)
        self.s_screen_count.setValue(1)
        self.s_screen_count.setStyleSheet(INPUT_STYLE)
        self.s_capacity = QSpinBox()
        self.s_capacity.setRange(20, 500)
        self.s_capacity.setValue(100)
        self.s_capacity.setStyleSheet(INPUT_STYLE)
        self.configure_btn = QPushButton("Configure Screen")
        self.configure_btn.setStyleSheet(BTN)
        self.configure_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.configure_btn.clicked.connect(self._configure_screen)
        self.s_mode_lbl = fl("Action")
        self.s_screen_number_lbl = fl("Screen Number")
        self.s_screen_count_lbl = fl("Number of Screens")
        self.s_capacity_lbl = fl("Capacity per Screen")

        fcl.addWidget(self.s_cfg_note)
        fcl.addWidget(fl("Cinema"))
        fcl.addWidget(self.s_cinema_combo)
        fcl.addWidget(self.s_mode_lbl)
        fcl.addWidget(self.s_mode)
        fcl.addWidget(self.s_screen_number_lbl)
        fcl.addWidget(self.s_screen_number)
        fcl.addWidget(self.s_screen_count_lbl)
        fcl.addWidget(self.s_screen_count)
        fcl.addWidget(self.s_capacity_lbl)
        fcl.addWidget(self.s_capacity)
        fcl.addWidget(self.configure_btn)
        fcl.addStretch()

        self._load_cinema_options(self.s_cinema_selector)
        self._load_cinema_options(self.s_cinema_combo)
        self._on_screen_mode_changed(self.s_mode.currentText())

        layout.addWidget(left, 1)
        layout.addWidget(fc)
        return widget

    def _load_screens(self):
        cinema_id = self._selected_cinema_id(self.s_cinema_selector)
        if cinema_id is None:
            QMessageBox.warning(self, "No Cinema", "Please select a cinema.")
            return
        screens = self.cinema_ctrl.get_screens_for_cinema(cinema_id)
        cinema_map = {c.cinema_id: c.name for c in self.cinema_ctrl.get_all_cinemas()}
        self.screens_table.setRowCount(len(screens))
        for i, s in enumerate(screens):
            self.screens_table.setItem(i, 0, QTableWidgetItem(str(s.screen_id)))
            self.screens_table.setItem(i, 1, QTableWidgetItem(cinema_map.get(s.cinema_id, "Unknown")))
            self.screens_table.setItem(i, 2, QTableWidgetItem(str(s.screen_number)))
            self.screens_table.setItem(i, 3, QTableWidgetItem(str(s.capacity)))
        if hasattr(self, "screens_badge"):
            self.screens_badge.setText(str(len(screens)))
        if not screens:
            QMessageBox.information(self, "No Screens", "No screens found for the selected cinema.")

    def _on_screen_row_selected(self):
        if not self.screens_table.selectedItems():
            return
        row = self.screens_table.currentRow()
        screen_number_item = self.screens_table.item(row, 2)
        capacity_item = self.screens_table.item(row, 3)
        cinema_id = self._selected_cinema_id(self.s_cinema_selector)
        if not screen_number_item or not capacity_item or cinema_id is None:
            return

        self.s_mode.setCurrentText("Configure Existing Screen")
        selector_index = self.s_cinema_selector.findData(cinema_id)
        form_index = self.s_cinema_combo.findData(cinema_id)
        if selector_index >= 0:
            self.s_cinema_selector.setCurrentIndex(selector_index)
        if form_index >= 0:
            self.s_cinema_combo.setCurrentIndex(form_index)
        self.s_screen_number.setValue(int(screen_number_item.text()))
        self.s_capacity.setValue(int(capacity_item.text()))

    def _on_screen_mode_changed(self, mode):
        adding_screens = mode == "Add New Screens"
        self.s_screen_number_lbl.setVisible(not adding_screens)
        self.s_screen_number.setVisible(not adding_screens)
        self.s_screen_count_lbl.setVisible(adding_screens)
        self.s_screen_count.setVisible(adding_screens)
        self.configure_btn.setText("Add Screens" if adding_screens else "Update Screen")
        if adding_screens:
            self.s_cfg_note.setText(
                "Seats are created automatically for each new screen:\n"
                "30% Lower Hall · 10 VIP · rest Upper Gallery"
            )
        else:
            self.s_cfg_note.setText(
                "Update the capacity for an existing screen number in this cinema."
            )

    def _configure_screen(self):
        cinema_id = self._selected_cinema_id(self.s_cinema_combo)
        if cinema_id is None:
            QMessageBox.warning(self, "No Cinema", "Please select a cinema.")
            return
        capacity = self.s_capacity.value()
        mode = self.s_mode.currentText()

        if mode == "Add New Screens":
            screen_count = self.s_screen_count.value()
            created = self.cinema_ctrl.configure_screens(cinema_id, screen_count, capacity)
            if created:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Created {len(created)} screen{'s' if len(created) != 1 else ''} for cinema ID {cinema_id}."
                )
                index = self.s_cinema_selector.findData(cinema_id)
                if index >= 0:
                    self.s_cinema_selector.setCurrentIndex(index)
                self._load_screens()
                if hasattr(self, "l_edit_screen_combo"):
                    self._load_screen_options(self.l_edit_screen_combo)
                self.s_screen_count.setValue(1)
                self.s_capacity.setValue(100)
            else:
                QMessageBox.critical(
                    self,
                    "Failed",
                    "Could not create screens. Check the selected cinema and try again."
                )
            return

        screen_number = self.s_screen_number.value()
        updated = self.cinema_ctrl.configure_existing_screen(
            cinema_id, screen_number, capacity)
        if updated:
            QMessageBox.information(
                self,
                "Success",
                f"Screen {screen_number} updated for cinema ID {cinema_id}."
            )
            index = self.s_cinema_selector.findData(cinema_id)
            if index >= 0:
                self.s_cinema_selector.setCurrentIndex(index)
            self._load_screens()
            if hasattr(self, "l_edit_screen_combo"):
                self._load_screen_options(self.l_edit_screen_combo)
            self.s_screen_number.setValue(1)
            self.s_capacity.setValue(100)
        else:
            QMessageBox.critical(
                self,
                "Failed",
                "Could not update that screen. Check the selected cinema and screen number."
            )

    # ── Cities & Pricing tab ──────────────────────────────────────────────────
    def _build_pricing_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Left: table card
        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setStyleSheet(CARD_STYLE)
        tc_lay = QVBoxLayout(tc)
        tc_lay.setContentsMargins(1, 1, 1, 1)
        tc_lay.setSpacing(0)
        tc_hdr = QWidget()
        tc_hdr.setFixedHeight(60)
        tc_hdr.setStyleSheet(f"background: {CARD};")
        hhl = QHBoxLayout(tc_hdr)
        hhl.setContentsMargins(16, 0, 16, 0)
        hhl.setSpacing(10)
        tc_ttl = QLabel("Cities & Pricing")
        tc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        self.pricing_badge = QLabel("0")
        self.pricing_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        ref_btn = QPushButton("Refresh")
        ref_btn.setStyleSheet(BTN_GHOST)
        ref_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ref_btn.setFixedHeight(32)
        ref_btn.clicked.connect(self._load_pricing)
        hhl.addWidget(tc_ttl)
        hhl.addStretch()
        hhl.addWidget(ref_btn)
        tc_div = QWidget()
        tc_div.setFixedHeight(1)
        tc_div.setStyleSheet(f"background: {BORDER};")
        self.pricing_table = QTableWidget()
        self.pricing_table.setStyleSheet(TABLE_STYLE)
        self.pricing_table.setColumnCount(7)
        self.pricing_table.setHorizontalHeaderLabels([
            "City ID", "City", "Morning", "Afternoon", "Evening", "Upper Mult.", "VIP Mult."])
        self.pricing_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.pricing_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.pricing_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.pricing_table.verticalHeader().setVisible(False)
        self.pricing_table.itemSelectionChanged.connect(self._on_pricing_city_selected)
        tc_lay.addWidget(tc_hdr)
        tc_lay.addWidget(tc_div)
        tc_lay.addWidget(self.pricing_table)

        # Right: scrollable form panel
        scroll = QScrollArea()
        scroll.setFixedWidth(280)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{ background: transparent; width: 6px; border-radius: 3px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 3px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)
        ri = QWidget()
        ri.setStyleSheet("background: transparent;")
        ri_lay = QVBoxLayout(ri)
        ri_lay.setContentsMargins(0, 0, 4, 0)
        ri_lay.setSpacing(12)
        scroll.setWidget(ri)

        def fl(text):
            lb = QLabel(text.upper())
            lb.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
            return lb

        def mk_card(title):
            c = QFrame()
            c.setObjectName("formCard")
            c.setStyleSheet(CARD_STYLE)
            cl = QVBoxLayout(c)
            cl.setContentsMargins(16, 14, 16, 16)
            cl.setSpacing(9)
            t = QLabel(title)
            t.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
            s = QWidget()
            s.setFixedHeight(1)
            s.setStyleSheet(f"background: {BORDER};")
            cl.addWidget(t)
            cl.addWidget(s)
            return c, cl

        # Add City card
        city_card, ccl = mk_card("Add City")
        self.p_city_name = QLineEdit()
        self.p_city_name.setPlaceholderText("New city name")
        self.p_city_name.setStyleSheet(INPUT_STYLE)
        add_city_btn = QPushButton("Add City")
        add_city_btn.setStyleSheet(BTN)
        add_city_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_city_btn.clicked.connect(self._add_city)
        ccl.addWidget(fl("City Name"))
        ccl.addWidget(self.p_city_name)
        ccl.addWidget(add_city_btn)

        # Set Pricing card
        price_card, pcl = mk_card("Set Pricing")
        self.p_city_combo = QComboBox()
        self.p_city_combo.setStyleSheet(INPUT_STYLE)
        self.p_morning = QDoubleSpinBox()
        self.p_afternoon = QDoubleSpinBox()
        self.p_evening = QDoubleSpinBox()
        self.p_upper = QDoubleSpinBox()
        self.p_vip = QDoubleSpinBox()
        for price in [self.p_morning, self.p_afternoon, self.p_evening]:
            price.setRange(0, 9999)
            price.setDecimals(2)
            price.setPrefix("£")
            price.setStyleSheet(INPUT_STYLE)
        for mult in [self.p_upper, self.p_vip]:
            mult.setRange(1, 10)
            mult.setDecimals(2)
            mult.setSingleStep(0.05)
            mult.setValue(1.20)
            mult.setStyleSheet(INPUT_STYLE)
        save_btn = QPushButton("Save Pricing")
        save_btn.setStyleSheet(BTN)
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._save_pricing)
        for w, lbl_text in [
            (self.p_city_combo, "City"),
            (self.p_morning, "Morning Price"),
            (self.p_afternoon, "Afternoon Price"),
            (self.p_evening, "Evening Price"),
            (self.p_upper, "Upper Gallery Mult."),
            (self.p_vip, "VIP Mult."),
        ]:
            pcl.addWidget(fl(lbl_text))
            pcl.addWidget(w)
        pcl.addWidget(save_btn)

        ri_lay.addWidget(city_card)
        ri_lay.addWidget(price_card)
        ri_lay.addStretch()

        layout.addWidget(tc, 1)
        layout.addWidget(scroll)
        self._load_city_options(self.p_city_combo)
        self._load_pricing()
        return widget

    def _load_pricing(self):
        rows = self.cinema_ctrl.get_all_cities_with_pricing()
        self.pricing_table.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                if col_index in [2, 3, 4] and value is not None:
                    display = f"£{float(value):.2f}"
                elif col_index in [5, 6] and value is not None:
                    display = f"{float(value):.2f}"
                else:
                    display = "" if value is None else str(value)
                self.pricing_table.setItem(row_index, col_index, QTableWidgetItem(display))
        if hasattr(self, "pricing_badge"):
            self.pricing_badge.setText(str(len(rows)))

    def _on_pricing_city_selected(self):
        if not self.pricing_table.selectedItems():
            return
        row = self.pricing_table.currentRow()
        city_id = int(self.pricing_table.item(row, 0).text())
        city_index = self.p_city_combo.findData(city_id)
        if city_index >= 0:
            self.p_city_combo.setCurrentIndex(city_index)

        def table_float(col, default):
            item = self.pricing_table.item(row, col)
            if not item or not item.text():
                return default
            return float(item.text().replace("£", ""))

        self.p_morning.setValue(table_float(2, 0))
        self.p_afternoon.setValue(table_float(3, 0))
        self.p_evening.setValue(table_float(4, 0))
        self.p_upper.setValue(table_float(5, 1.20))
        self.p_vip.setValue(table_float(6, 1.20))

    def _add_city(self):
        city_name = self.p_city_name.text().strip()
        if not city_name:
            QMessageBox.warning(self, "Input Error", "City name is required.")
            return
        city_id = self.cinema_ctrl.add_city(city_name)
        if city_id:
            QMessageBox.information(self, "Success", f"City '{city_name}' added.")
            self.p_city_name.clear()
            self._load_city_options(self.p_city_combo, city_id)
            if hasattr(self, "c_city_combo"):
                self._load_city_options(self.c_city_combo, city_id)
            self._load_pricing()
        else:
            QMessageBox.critical(self, "Failed", "Could not add city.")

    def _save_pricing(self):
        city_id = self._selected_city_id(self.p_city_combo)
        if city_id is None:
            QMessageBox.warning(self, "Input Error", "Please select a city.")
            return
        ok = self.cinema_ctrl.set_city_pricing(
            city_id,
            self.p_morning.value(),
            self.p_afternoon.value(),
            self.p_evening.value(),
            self.p_upper.value(),
            self.p_vip.value(),
        )
        if ok:
            QMessageBox.information(self, "Success", "Pricing saved.")
            self.p_city_combo.setCurrentIndex(-1)
            self.p_morning.setValue(0.0)
            self.p_afternoon.setValue(0.0)
            self.p_evening.setValue(0.0)
            self.p_upper.setValue(1.20)
            self.p_vip.setValue(1.20)
            self._load_pricing()
        else:
            QMessageBox.critical(self, "Failed", "Could not save pricing. Check the selected city.")

    # ── Reports tab ───────────────────────────────────────────────────────────
    def _build_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Controls card
        ctrl_card = QFrame()
        ctrl_card.setObjectName("ctrlCard")
        ctrl_card.setStyleSheet(CARD_STYLE)
        ctrl_lay = QHBoxLayout(ctrl_card)
        ctrl_lay.setContentsMargins(20, 16, 20, 16)
        ctrl_lay.setSpacing(14)

        def fl(text):
            lb = QLabel(text)
            lb.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; "
                "letter-spacing: 0.5px; background: transparent;"
            )
            return lb

        report_lbl = fl("REPORT TYPE")
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Bookings Per Listing",
            "Monthly Revenue Per Cinema",
            "Top Revenue Generating Film",
            "Staff Performance",
        ])
        self.report_combo.setStyleSheet(INPUT_STYLE)
        self.report_combo.setMinimumHeight(38)

        sort_metric_lbl = fl("SORT BY")
        self.report_sort_metric = QComboBox()
        self.report_sort_metric.addItems(["Bookings", "Revenue"])
        self.report_sort_metric.setStyleSheet(INPUT_STYLE)
        self.report_sort_metric.setMinimumHeight(38)
        self.report_sort_metric.currentIndexChanged.connect(self._generate_report)

        sort_direction_lbl = fl("ORDER")
        self.report_sort_direction = QComboBox()
        self.report_sort_direction.addItems(["High to Low", "Low to High"])
        self.report_sort_direction.setStyleSheet(INPUT_STYLE)
        self.report_sort_direction.setMinimumHeight(38)
        self.report_sort_direction.currentIndexChanged.connect(self._generate_report)

        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet(BTN)
        generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        generate_btn.setMinimumHeight(40)
        generate_btn.setFixedWidth(170)
        generate_btn.clicked.connect(self._generate_report)

        selector_col = QVBoxLayout()
        selector_col.setSpacing(6)
        selector_col.addWidget(report_lbl)
        selector_col.addWidget(self.report_combo)
        sort_metric_col = QVBoxLayout()
        sort_metric_col.setSpacing(6)
        sort_metric_col.addWidget(sort_metric_lbl)
        sort_metric_col.addWidget(self.report_sort_metric)
        sort_direction_col = QVBoxLayout()
        sort_direction_col.setSpacing(6)
        sort_direction_col.addWidget(sort_direction_lbl)
        sort_direction_col.addWidget(self.report_sort_direction)

        ctrl_lay.addLayout(selector_col, 1)
        ctrl_lay.addLayout(sort_metric_col, 1)
        ctrl_lay.addLayout(sort_direction_col, 1)
        ctrl_lay.addWidget(generate_btn, 0, Qt.AlignmentFlag.AlignBottom)

        # Results table card
        res_card = QFrame()
        res_card.setObjectName("tableCard")
        res_card.setStyleSheet(CARD_STYLE)
        res_lay = QVBoxLayout(res_card)
        res_lay.setContentsMargins(1, 1, 1, 1)
        res_lay.setSpacing(0)
        res_hdr = QWidget()
        res_hdr.setFixedHeight(52)
        res_hdr.setStyleSheet(f"background: {CARD};")
        rhl = QHBoxLayout(res_hdr)
        rhl.setContentsMargins(16, 0, 16, 0)
        rhl.setSpacing(10)
        self.report_title_lbl = QLabel("Report Results")
        self.report_title_lbl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        rhl.addWidget(self.report_title_lbl)
        rhl.addStretch()
        res_div = QWidget()
        res_div.setFixedHeight(1)
        res_div.setStyleSheet(f"background: {BORDER};")
        self.report_table = QTableWidget()
        self.report_table.setStyleSheet(TABLE_STYLE)
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.report_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.report_table.horizontalHeader().setHighlightSections(False)
        self.report_table.verticalHeader().setVisible(False)
        self.report_table.verticalHeader().setDefaultSectionSize(44)
        self.report_table.setShowGrid(False)
        self.report_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        res_lay.addWidget(res_hdr)
        res_lay.addWidget(res_div)
        res_lay.addWidget(self.report_table)

        layout.addWidget(ctrl_card)
        layout.addWidget(res_card, 1)
        return widget

    def _generate_report(self):
        if not hasattr(self, "report_table"):
            return
        key_map = {
            "Bookings Per Listing": "bookings_per_listing",
            "Monthly Revenue Per Cinema": "monthly_revenue",
            "Top Revenue Generating Film": "top_revenue_film",
            "Staff Performance": "staff_performance",
        }
        key = key_map[self.report_combo.currentText()]
        try:
            report = ReportFactory.create_report(key)
            headers, data = report.get_data()
            data = self._sort_report_data(headers, data)

            self.report_table.clear()
            self.report_table.setColumnCount(len(headers))
            self.report_table.setRowCount(len(data))
            self.report_table.setHorizontalHeaderLabels([header.upper() for header in headers])
            self.report_title_lbl.setText(self.report_combo.currentText())

            right_align = {"Bookings", "Revenue", "Year", "Month"}
            for row_idx, row_data in enumerate(data):
                for col_idx, header in enumerate(headers):
                    raw = row_data[col_idx]
                    if header == "Revenue":
                        try:
                            display = f"£{float(raw):.2f}"
                        except (ValueError, TypeError):
                            display = "£0.00"
                    else:
                        display = raw if raw != "None" else "-"
                    item = QTableWidgetItem(display)
                    if header in right_align:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    if header == "Revenue":
                        item.setForeground(QColor(ACCENT))
                        item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                    self.report_table.setItem(row_idx, col_idx, item)

        except Exception as e:
            print("Report generation failed.")
            QMessageBox.critical(self, "Error", "Report generation failed. Please try again.")

    def _sort_report_data(self, headers, data):
        metric = self.report_sort_metric.currentText()
        if metric not in headers:
            return data

        metric_index = headers.index(metric)
        reverse = self.report_sort_direction.currentText() == "High to Low"

        def numeric_value(row):
            raw = row[metric_index]
            try:
                return float(str(raw).replace("Â£", "").replace(",", "").strip())
            except (TypeError, ValueError):
                return 0.0

        return sorted(data, key=numeric_value, reverse=reverse)

    # ── User Registration tab ────────────────────────────────────────────────
    def _build_user_registration_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Left: table card
        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setStyleSheet(CARD_STYLE)
        tc_lay = QVBoxLayout(tc)
        tc_lay.setContentsMargins(1, 1, 1, 1)
        tc_lay.setSpacing(0)
        tc_hdr = QWidget()
        tc_hdr.setFixedHeight(60)
        tc_hdr.setStyleSheet(f"background: {CARD};")
        hhl = QHBoxLayout(tc_hdr)
        hhl.setContentsMargins(16, 0, 16, 0)
        hhl.setSpacing(10)
        tc_ttl = QLabel("Registered Users")
        tc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        self.users_badge = QLabel("0")
        self.users_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        ref_btn = QPushButton("Refresh")
        ref_btn.setStyleSheet(BTN_GHOST)
        ref_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        ref_btn.setFixedHeight(32)
        ref_btn.clicked.connect(self._load_registered_users)
        hhl.addWidget(tc_ttl)
        hhl.addStretch()
        hhl.addWidget(ref_btn)
        tc_div = QWidget()
        tc_div.setFixedHeight(1)
        tc_div.setStyleSheet(f"background: {BORDER};")
        self.users_table = QTableWidget()
        self.users_table.setStyleSheet(TABLE_STYLE)
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(
            ["User ID", "Username", "Full Name", "Email", "Role", "Assigned Cinema"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(0, 72)
        self.users_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.users_table.setColumnWidth(4, 120)
        self.users_table.horizontalHeader().setHighlightSections(False)
        self.users_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.users_table.setShowGrid(False)
        self.users_table.verticalHeader().setVisible(False)
        self.users_table.verticalHeader().setDefaultSectionSize(44)
        self.users_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        tc_lay.addWidget(tc_hdr)
        tc_lay.addWidget(tc_div)
        tc_lay.addWidget(self.users_table)

        # Right: scrollable form card
        scroll = QScrollArea()
        scroll.setFixedWidth(300)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{ background: transparent; width: 8px; margin: 0; }}
            QScrollBar::handle:vertical {{ background: #3a3b3f; border-radius: 4px; min-height: 24px; }}
            QScrollBar::handle:vertical:hover {{ background: #50525a; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        """)
        ri = QWidget()
        ri.setStyleSheet("background: transparent;")
        ri.setMinimumWidth(1)
        ri_lay = QVBoxLayout(ri)
        ri_lay.setContentsMargins(0, 0, 0, 0)
        ri_lay.setSpacing(14)
        scroll.setWidget(ri)

        fc = QFrame()
        fc.setObjectName("actionCard")
        fc.setStyleSheet(
            f"QFrame#actionCard {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
        )
        fcl = QVBoxLayout(fc)
        fcl.setContentsMargins(20, 18, 20, 20)
        fcl.setSpacing(9)
        fc_ttl = QLabel("Register User")
        fc_ttl.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
        fc_sep = QWidget()
        fc_sep.setFixedHeight(1)
        fc_sep.setStyleSheet(f"background: {BORDER};")
        note = QLabel("Managers can create booking staff and admin accounts.")
        note.setWordWrap(True)
        note.setStyleSheet(f"color: {MUTED}; font-size: 11px;")
        fcl.addWidget(fc_ttl)
        fcl.addWidget(fc_sep)
        fcl.addWidget(note)

        def fl(text):
            lb = QLabel(text.upper())
            lb.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
            return lb

        self.reg_role = QComboBox()
        self.reg_role.addItems(["BOOKING_STAFF", "ADMIN"])
        self.reg_role.setStyleSheet(INPUT_STYLE)
        self.reg_role.currentTextChanged.connect(self._on_registration_role_changed)
        self.reg_username = QLineEdit()
        self.reg_username.setPlaceholderText("Username")
        self.reg_username.setStyleSheet(INPUT_STYLE)
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Password")
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_password.setStyleSheet(INPUT_STYLE)
        self.reg_confirm_password = QLineEdit()
        self.reg_confirm_password.setPlaceholderText("Confirm password")
        self.reg_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.reg_confirm_password.setStyleSheet(INPUT_STYLE)
        self.reg_full_name = QLineEdit()
        self.reg_full_name.setPlaceholderText("Full name")
        self.reg_full_name.setStyleSheet(INPUT_STYLE)
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Email address")
        self.reg_email.setStyleSheet(INPUT_STYLE)
        self.reg_cinema_combo = QComboBox()
        self.reg_cinema_combo.setStyleSheet(INPUT_STYLE)
        self._load_cinema_options(self.reg_cinema_combo)
        register_btn = QPushButton("Register User")
        register_btn.setStyleSheet(BTN)
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.clicked.connect(self._register_user)

        for field, lbl_text in [
            (self.reg_role, "Role"),
            (self.reg_username, "Username"),
            (self.reg_password, "Password"),
            (self.reg_confirm_password, "Confirm Password"),
            (self.reg_full_name, "Full Name"),
            (self.reg_email, "Email"),
        ]:
            fcl.addWidget(fl(lbl_text))
            fcl.addWidget(field)
        self.reg_cinema_label = fl("Assigned Cinema")
        fcl.addWidget(self.reg_cinema_label)
        fcl.addWidget(self.reg_cinema_combo)
        fcl.addWidget(register_btn)

        ri_lay.addWidget(fc)
        ri_lay.addStretch()

        layout.addWidget(tc, 1)
        layout.addWidget(scroll)
        self._on_registration_role_changed(self.reg_role.currentText())
        self._load_registered_users()
        return widget

    def _on_registration_role_changed(self, role):
        needs_cinema = role == "BOOKING_STAFF"
        self.reg_cinema_label.setVisible(needs_cinema)
        self.reg_cinema_combo.setVisible(needs_cinema)

    def _load_registered_users(self):
        staff_rows = self.auth_ctrl.get_booking_staff()
        admin_rows = self.auth_ctrl.get_users_by_roles(["ADMIN"])
        cinema_map = {c.cinema_id: c.name for c in self.cinema_ctrl.get_all_cinemas()}
        rows = [
            (user_id, username, full_name, email, "BOOKING_STAFF", cinema_id)
            for user_id, username, full_name, email, cinema_id in staff_rows
        ] + [
            (user_id, username, full_name, email, "ADMIN", cinema_id)
            for user_id, username, full_name, email, role, cinema_id in admin_rows
        ]
        self.users_table.setRowCount(len(rows))
        for row_index, (user_id, username, full_name, email, role, cinema_id) in enumerate(rows):
            self.users_table.setItem(row_index, 0, QTableWidgetItem(str(user_id)))
            self.users_table.setItem(row_index, 1, QTableWidgetItem(username))
            self.users_table.setItem(row_index, 2, QTableWidgetItem(full_name or ""))
            self.users_table.setItem(row_index, 3, QTableWidgetItem(email or ""))
            self.users_table.setItem(row_index, 4, QTableWidgetItem(role))
            assigned = cinema_map.get(cinema_id, "Not assigned") if cinema_id else "Not assigned"
            self.users_table.setItem(row_index, 5, QTableWidgetItem(assigned))
        if hasattr(self, "users_badge"):
            self.users_badge.setText(str(len(rows)))

    def _register_user(self):
        role = self.reg_role.currentText()
        username = self.reg_username.text().strip()
        password = self.reg_password.text()
        confirm_password = self.reg_confirm_password.text()
        full_name = self.reg_full_name.text().strip()
        email = self.reg_email.text().strip()
        cinema_id = self._selected_cinema_id(self.reg_cinema_combo) if role == "BOOKING_STAFF" else None

        if not username or not password or not full_name or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all user details.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return
        if role == "BOOKING_STAFF" and cinema_id is None:
            QMessageBox.warning(self, "Input Error", "Please select an assigned cinema.")
            return

        ok, result = self.auth_ctrl.register_user(
            username, password, full_name, email, role, cinema_id)
        if ok:
            QMessageBox.information(
                self,
                "User Registered",
                f"{role} user '{full_name}' registered with user ID {result}."
            )
            for field in [
                self.reg_username,
                self.reg_password,
                self.reg_confirm_password,
                self.reg_full_name,
                self.reg_email,
            ]:
                field.clear()
            self.reg_cinema_combo.setCurrentIndex(-1)
            self._load_registered_users()
        else:
            QMessageBox.critical(self, "Registration Failed", str(result))

    # ── Listings tab ──────────────────────────────────────────────────────────
    def _load_screen_options(self, combo, selected_screen_id=None):
        combo.blockSignals(True)
        combo.clear()

        screen_count = 0
        for cinema in self.cinema_ctrl.get_all_cinemas():
            screens = self.cinema_ctrl.get_screens_for_cinema(cinema.cinema_id)
            for screen in screens:
                label = (
                    f"{cinema.name} | Screen {screen.screen_number} "
                    f"(ID {screen.screen_id}, Capacity {screen.capacity})"
                )
                combo.addItem(label, screen.screen_id)
                screen_count += 1

        combo.setEditable(True)
        combo.setStyleSheet(SEARCH_COMBO_STYLE)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setCurrentText("")
        combo.lineEdit().setPlaceholderText("Search cinema or screen")
        completer = combo.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        if screen_count == 0:
            combo.addItem("No screens available", None)
            combo.setEnabled(False)
        else:
            combo.setEnabled(True)
            if selected_screen_id is not None:
                index = combo.findData(selected_screen_id)
                if index >= 0:
                    combo.setCurrentIndex(index)

        combo.blockSignals(False)

    def _selected_screen_id(self, combo):
        screen_id = combo.currentData()
        return int(screen_id) if screen_id is not None else None

    def _load_film_options(self, combo, selected_film_id=None):
        combo.blockSignals(True)
        combo.clear()

        films = self.film_ctrl.get_all_films()
        for film in films:
            combo.addItem(f"{film.title} (ID {film.film_id})", film.film_id)

        combo.setEditable(True)
        combo.setStyleSheet(SEARCH_COMBO_STYLE)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setCurrentText("")
        combo.lineEdit().setPlaceholderText("Search film title")
        completer = combo.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        if not films:
            combo.addItem("No films available", None)
            combo.setEnabled(False)
        else:
            combo.setEnabled(True)
            if selected_film_id is not None:
                index = combo.findData(selected_film_id)
                if index >= 0:
                    combo.setCurrentIndex(index)

        combo.blockSignals(False)

    def _selected_film_id(self, combo):
        film_id = combo.currentData()
        return int(film_id) if film_id is not None else None

    def _load_cinema_options(self, combo, selected_cinema_id=None):
        combo.blockSignals(True)
        combo.clear()

        cinemas = self.cinema_ctrl.get_all_cinemas()
        for cinema in cinemas:
            combo.addItem(
                f"{cinema.name} - {cinema.location} (ID {cinema.cinema_id})",
                cinema.cinema_id,
            )

        combo.setEditable(True)
        combo.setStyleSheet(SEARCH_COMBO_STYLE)
        combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        combo.setCurrentText("")
        combo.lineEdit().setPlaceholderText("Search cinema")
        completer = combo.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        if not cinemas:
            combo.addItem("No cinemas available", None)
            combo.setEnabled(False)
        else:
            combo.setEnabled(True)
            if selected_cinema_id is not None:
                index = combo.findData(selected_cinema_id)
                if index >= 0:
                    combo.setCurrentIndex(index)

        combo.blockSignals(False)

    def _selected_cinema_id(self, combo):
        cinema_id = combo.currentData()
        return int(cinema_id) if cinema_id is not None else None

    def _on_listing_selected(self):
        if not self.listings_table.selectedItems():
            return
        row = self.listings_table.currentRow()
        listing_id = int(self.listings_table.item(row, 0).text())
        listing = self._listings_map.get(listing_id)
        if not listing:
            return
        self.l_edit_id.setValue(listing_id)
        self._load_film_options(self.l_edit_film_id, listing.film_id)
        self._load_screen_options(self.l_edit_screen_combo, listing.screen_id)
        show_date = listing.show_date
        self.l_edit_date.setDate(QDate(show_date.year, show_date.month, show_date.day))
        show_time = listing.show_time
        if hasattr(show_time, 'hour'):
            self.l_edit_time.setTime(QTime(show_time.hour, show_time.minute))
        else:
            total_seconds = int(show_time.total_seconds())
            self.l_edit_time.setTime(QTime(total_seconds // 3600, (total_seconds % 3600) // 60))
        self.l_edit_hint.setText(f"Editing listing ID {listing_id}")

    def _update_listing(self):
        if not self.listings_table.selectedItems():
            QMessageBox.warning(self, "No Selection", "Select a listing row in the table first.")
            return
        screen_id = self._selected_screen_id(self.l_edit_screen_combo)
        if screen_id is None:
            QMessageBox.warning(self, "No Screen", "No screen is available for this listing.")
            return
        film_id = self._selected_film_id(self.l_edit_film_id)
        if film_id is None:
            QMessageBox.warning(self, "No Film", "Please select a film.")
            return
        listing_id = self.l_edit_id.value()
        ok = self.film_ctrl.update_listing(
            listing_id,
            film_id,
            screen_id,
            self.l_edit_date.date().toPyDate(),
            self.l_edit_time.time().toString("HH:mm:ss"),
            _session_for_qtime(self.l_edit_time.time()))
        if ok:
            QMessageBox.information(self, "Success", f"Listing ID {listing_id} updated.")
            self.l_edit_id.setValue(0)
            self.l_edit_film_id.setCurrentIndex(-1)
            self.l_edit_screen_combo.setCurrentIndex(-1)
            self.l_edit_date.setDate(QDate.currentDate())
            self.l_edit_time.setTime(QTime(18, 0))
            self.l_edit_hint.setText("Select a row to edit")
            self.listings_table.clearSelection()
            self._load_listings()
        else:
            QMessageBox.critical(
                self,
                "Failed",
                getattr(self.film_ctrl, "last_error", "")
                or "Update failed. Check Film ID and the selected screen.",
            )

    def _build_listings_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(20)

        # --- Left: table card ---
        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setMinimumWidth(0)
        tc.setStyleSheet(CARD_STYLE)
        tc_layout = QVBoxLayout(tc)
        tc_layout.setContentsMargins(1, 1, 1, 1)
        tc_layout.setSpacing(0)

        hdr = QWidget()
        hdr.setFixedHeight(60)
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(16, 0, 16, 0)
        title_lbl = QLabel("Upcoming Listings")
        title_lbl.setStyleSheet(f"color: {TEXT}; font-size: 15px; font-weight: 600;")
        self.listings_badge = QLabel("0")
        self.listings_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        hdr_layout.addWidget(title_lbl)
        hdr_layout.addStretch()

        div = QWidget()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background-color: {BORDER};")

        self.listings_table = QTableWidget()
        self.listings_table.setStyleSheet(TABLE_STYLE)
        self.listings_table.setColumnCount(8)
        self.listings_table.setHorizontalHeaderLabels(
            ["ID", "Film", "Screen", "Cinema", "City", "Date", "Time", ""])
        self.listings_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.listings_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.listings_table.setColumnWidth(0, 52)
        self.listings_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.listings_table.setColumnWidth(3, 240)
        self.listings_table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.listings_table.setColumnWidth(7, 120)
        self.listings_table.horizontalHeader().setHighlightSections(False)
        self.listings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.listings_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.listings_table.setShowGrid(False)
        self.listings_table.verticalHeader().setDefaultSectionSize(52)
        self.listings_table.verticalHeader().setVisible(False)
        self.listings_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.listings_table.itemSelectionChanged.connect(self._on_listing_selected)

        tc_layout.addWidget(hdr)
        tc_layout.addWidget(div)
        tc_layout.addWidget(self.listings_table)

        # --- Right: scroll area with Edit Listing form card ---
        scroll = QScrollArea()
        scroll.setFixedWidth(300)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(
            f"QScrollArea {{ border: none; background: transparent; }}"
            f"QScrollBar:vertical {{ background: transparent; width: 8px; margin: 0; }}"
            f"QScrollBar::handle:vertical {{ background: #3a3b3f; border-radius: 4px; min-height: 24px; }}"
            f"QScrollBar::handle:vertical:hover {{ background: #50525a; }}"
            f"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}"
        )
        inner = QWidget()
        inner.setStyleSheet("background: transparent;")
        inner.setMinimumWidth(1)
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(14)
        scroll.setWidget(inner)

        def mk_card(title, subtitle):
            card = QFrame()
            card.setObjectName("actionCard")
            card.setStyleSheet(
                f"QFrame#actionCard {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
            )
            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 18, 20, 20)
            cl.setSpacing(0)
            t = QLabel(title)
            t.setStyleSheet(f"color: {TEXT}; font-size: 13px; font-weight: 600;")
            sub = QLabel(subtitle)
            sub.setWordWrap(True)
            sub.setMinimumWidth(1)
            sub.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent;")
            sep = QWidget()
            sep.setFixedHeight(1)
            sep.setStyleSheet(f"background-color: {BORDER};")
            cl.addWidget(t)
            cl.addSpacing(4)
            cl.addWidget(sub)
            cl.addSpacing(14)
            cl.addWidget(sep)
            cl.addSpacing(14)
            return card, cl

        def fl(text):
            lbl = QLabel(text.upper())
            lbl.setStyleSheet(f"color: {MUTED}; font-size: 10px; font-weight: 600; letter-spacing: 0.5px;")
            return lbl

        add_card, add_cl = mk_card("Add Listing", "Use the guided flow to create listings with conflict checks.")
        add_listing_btn = QPushButton("Add Listing")
        add_listing_btn.setStyleSheet(BTN)
        add_listing_btn.setMinimumHeight(40)
        add_listing_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_listing_btn.clicked.connect(self._add_listing)
        add_cl.addWidget(add_listing_btn)

        edit_card, ecl = mk_card("Edit Listing", "Click a row in the table to populate these fields.")

        self.l_edit_hint = QLabel("Select a row to edit")
        self.l_edit_hint.setStyleSheet(f"color: {MUTED}; font-size: 11px; font-style: italic;")
        ecl.addWidget(self.l_edit_hint)
        ecl.addSpacing(10)

        self.l_edit_id = QSpinBox()
        self.l_edit_id.setRange(0, 9999)
        self.l_edit_id.setReadOnly(True)
        self.l_edit_id.setStyleSheet(INPUT_STYLE + f"QSpinBox {{ color: {MUTED}; }}")

        self.l_edit_film_id = QComboBox()
        self.l_edit_film_id.setStyleSheet(INPUT_STYLE)

        self.l_edit_screen_combo = QComboBox()
        self.l_edit_screen_combo.setStyleSheet(INPUT_STYLE)

        self.l_edit_date = QDateEdit()
        self.l_edit_date.setCalendarPopup(True)
        self.l_edit_date.setDate(QDate.currentDate())
        self.l_edit_date.setMinimumDate(QDate.currentDate())
        self.l_edit_date.setStyleSheet(INPUT_STYLE)

        self.l_edit_time = QTimeEdit()
        self.l_edit_time.setTime(QTime(18, 0))
        self.l_edit_time.setDisplayFormat("HH:mm")
        self.l_edit_time.setStyleSheet(INPUT_STYLE)

        for widget_item, label_text in [
            (self.l_edit_id, "Listing ID (read-only)"),
            (self.l_edit_film_id, "Film"),
            (self.l_edit_screen_combo, "Screen"),
            (self.l_edit_date, "Show Date"),
            (self.l_edit_time, "Show Time"),
        ]:
            ecl.addWidget(fl(label_text))
            ecl.addSpacing(6)
            ecl.addWidget(widget_item)
            ecl.addSpacing(10)

        update_listing_btn = QPushButton("Update Listing")
        update_listing_btn.setStyleSheet(BTN)
        update_listing_btn.setMinimumHeight(40)
        update_listing_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        update_listing_btn.clicked.connect(self._update_listing)
        ecl.addSpacing(4)
        ecl.addWidget(update_listing_btn)

        inner_layout.addWidget(add_card)
        inner_layout.addWidget(edit_card)
        inner_layout.addStretch()

        self._load_film_options(self.l_edit_film_id)
        self._load_screen_options(self.l_edit_screen_combo)

        layout.addWidget(tc, 1)
        layout.addWidget(scroll, 0)
        self._load_listings()
        return widget

    def _load_listings(self):
        listings = [
            listing for listing in self.film_ctrl.get_all_listings()
            if _listing_is_bookable(listing)
        ]
        if hasattr(self, "listings_badge"):
            self.listings_badge.setText(str(len(listings)))
        self._populate_listings_table(self.listings_table, listings, include_actions=True)

    def _populate_listings_table(self, table, listings, include_actions=False):
        if include_actions:
            self._listings_map = {listing.listing_id: listing for listing in listings}
        films = {film.film_id: film.title for film in self.film_ctrl.get_all_films()}
        table.setRowCount(len(listings))
        for row_index, listing in enumerate(listings):
            table.setItem(row_index, 0, QTableWidgetItem(str(listing.listing_id)))
            table.setItem(row_index, 1, QTableWidgetItem(films.get(listing.film_id, "Unknown")))
            table.setItem(row_index, 2, QTableWidgetItem(str(listing.screen_id)))

            try:
                cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing.listing_id)
                cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id) if cinema_id else ("?", "?")
            except Exception:
                cinema_name, city_name = ("?", "?")

            table.setItem(row_index, 3, QTableWidgetItem(cinema_name))
            table.setItem(row_index, 4, QTableWidgetItem(city_name))
            table.setItem(row_index, 5, QTableWidgetItem(str(listing.show_date)))
            table.setItem(row_index, 6, QTableWidgetItem(str(listing.show_time)))
            if not include_actions:
                continue

            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {DANGER}; color: #202124;
                    font-weight: bold; border-radius: 4px;
                    padding: 2px 8px; border: none; font-size: 11px;
                }}
                QPushButton:hover {{ background-color: #ee675c; }}
            """)
            delete_btn.setFixedSize(72, 28)
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.clicked.connect(lambda checked, lid=listing.listing_id: self._remove_listing(lid))

            btn_container = QWidget()
            btn_container.setStyleSheet("background: transparent;")
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.addWidget(delete_btn, 0, Qt.AlignmentFlag.AlignCenter)
            table.setCellWidget(row_index, 7, btn_container)

    def _build_listing_history_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(0)

        tc = QFrame()
        tc.setObjectName("tableCard")
        tc.setStyleSheet(CARD_STYLE)
        tc_layout = QVBoxLayout(tc)
        tc_layout.setContentsMargins(1, 1, 1, 1)
        tc_layout.setSpacing(0)

        hdr = QWidget()
        hdr.setFixedHeight(60)
        hdr_layout = QHBoxLayout(hdr)
        hdr_layout.setContentsMargins(16, 0, 16, 0)
        title_lbl = QLabel("Listing History")
        title_lbl.setStyleSheet(f"color: {TEXT}; font-size: 15px; font-weight: 600;")
        self.history_badge = QLabel("0")
        self.history_badge.setStyleSheet(
            f"color: {DARK}; background: {ACCENT}; border-radius: 10px; padding: 2px 8px; font-size: 11px;")
        ref_btn = QPushButton("Refresh")
        ref_btn.setStyleSheet(BTN_GHOST)
        ref_btn.setFixedHeight(32)
        ref_btn.clicked.connect(self._load_listing_history)
        hdr_layout.addWidget(title_lbl)
        hdr_layout.addStretch()
        hdr_layout.addWidget(ref_btn)

        div = QWidget()
        div.setFixedHeight(1)
        div.setStyleSheet(f"background-color: {BORDER};")

        self.listing_history_table = QTableWidget()
        self.listing_history_table.setStyleSheet(TABLE_STYLE)
        self.listing_history_table.setColumnCount(7)
        self.listing_history_table.setHorizontalHeaderLabels(
            ["Listing ID", "Film", "Screen", "Cinema", "City", "Date", "Time"])
        self.listing_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.listing_history_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.listing_history_table.setColumnWidth(3, 260)
        self.listing_history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.listing_history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.listing_history_table.verticalHeader().setVisible(False)

        tc_layout.addWidget(hdr)
        tc_layout.addWidget(div)
        tc_layout.addWidget(self.listing_history_table)

        layout.addWidget(tc)
        self._load_listing_history()
        return widget

    def _load_listing_history(self):
        today = QDate.currentDate().toPyDate()
        listings = [
            listing for listing in self.film_ctrl.get_all_listings()
            if listing.show_date < today
        ]
        if hasattr(self, "history_badge"):
            self.history_badge.setText(str(len(listings)))
        self._populate_listings_table(self.listing_history_table, listings, include_actions=False)

    def _add_listing(self):
        self._open_add_listing_wizard()

    def _open_add_listing_wizard(self):
        films = {f.film_id: f for f in self.film_ctrl.get_all_films()}
        if not films:
            QMessageBox.warning(self, "No Films", "Please add at least one film before creating a listing.")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Add Listing Wizard")
        dialog.setMinimumSize(520, 360)
        dialog.setStyleSheet(f"background-color: {DARK}; color: {TEXT};")

        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(12)

        title = QLabel("Create New Listing")
        title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")

        subtitle = QLabel("Follow each step to avoid invalid or conflicting showtimes.")
        subtitle.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        pages = QStackedWidget()

        step1 = QWidget()
        s1 = QVBoxLayout(step1)
        s1.setSpacing(8)
        s1.addWidget(QLabel("Step 1 of 3 - Select Film and Cinema"))

        film_combo = QComboBox()
        film_combo.setStyleSheet(INPUT_STYLE)
        self._load_film_options(film_combo)

        cinema_combo = QComboBox()
        cinema_combo.setStyleSheet(INPUT_STYLE)
        self._load_cinema_options(cinema_combo)

        s1.addWidget(QLabel("Film"))
        s1.addWidget(film_combo)
        s1.addWidget(QLabel("Cinema"))
        s1.addWidget(cinema_combo)
        s1.addStretch()

        step2 = QWidget()
        s2 = QVBoxLayout(step2)
        s2.setSpacing(8)
        s2.addWidget(QLabel("Step 2 of 3 - Select Screen"))

        s2_note = QLabel("Only screens from the selected cinema are shown.")
        s2_note.setStyleSheet(f"color: {MUTED}; font-size: 11px;")
        s2_note.setWordWrap(True)

        screen_cards_scroll = QScrollArea()
        screen_cards_scroll.setWidgetResizable(True)
        screen_cards_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        screen_cards_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        screen_cards_scroll.setMinimumHeight(132)
        screen_cards_scroll.setMaximumHeight(150)
        screen_cards_scroll.setFrameShape(QFrame.Shape.NoFrame)
        screen_cards_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: transparent; }}
            QScrollBar:vertical {{ background: {CARD}; width: 8px; border-radius: 4px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 4px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

        cards_container = QWidget()
        screen_cards_layout = QGridLayout(cards_container)
        screen_cards_layout.setContentsMargins(6, 6, 6, 6)
        screen_cards_layout.setSpacing(6)
        screen_cards_scroll.setWidget(cards_container)

        selected_screen = {"id": None}
        screen_button_group = QButtonGroup(dialog)
        screen_button_group.setExclusive(True)

        card_style = f"""
            QPushButton {{
                background-color: {INPUT};
                color: {TEXT};
                border: 1px solid {BORDER};
                border-radius: 6px;
                text-align: left;
                padding: 6px;
                font-size: 11px;
            }}
            QPushButton:hover {{ border: 1px solid {ACCENT}; }}
            QPushButton:checked {{
                background-color: #3c4043;
                border: 1px solid {ACCENT};
                color: {ACCENT};
                font-weight: bold;
            }}
        """

        def render_screen_cards(selected_cinema_id):
            selected_screen["id"] = None
            while screen_cards_layout.count():
                item = screen_cards_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
            for btn in screen_button_group.buttons():
                screen_button_group.removeButton(btn)
            screens = self.cinema_ctrl.get_screens_for_cinema(selected_cinema_id)
            if not screens:
                empty_lbl = QLabel("No screens found for this cinema.")
                empty_lbl.setStyleSheet(f"color: {MUTED}; font-size: 12px; padding: 8px;")
                screen_cards_layout.addWidget(empty_lbl, 0, 0)
                return
            for idx, screen in enumerate(screens):
                card = QPushButton(
                    f"Screen {screen.screen_number}  |  ID {screen.screen_id}\n"
                    f"Capacity: {screen.capacity}"
                )
                card.setCheckable(True)
                card.setMinimumHeight(52)
                card.setStyleSheet(card_style)
                screen_button_group.addButton(card, screen.screen_id)
                row, col = divmod(idx, 3)
                screen_cards_layout.addWidget(card, row, col)

        screen_button_group.idClicked.connect(
            lambda screen_id: selected_screen.__setitem__("id", int(screen_id))
        )

        s2.addWidget(s2_note)
        s2.addWidget(screen_cards_scroll)
        s2.addStretch()

        step3 = QWidget()
        s3 = QVBoxLayout(step3)
        s3.setSpacing(8)
        s3.addWidget(QLabel("Step 3 of 3 - Set Time and Create"))

        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setMinimumDate(QDate.currentDate())
        date_edit.setStyleSheet(INPUT_STYLE)

        time_edit = QTimeEdit()
        time_edit.setTime(QTime(18, 0))
        time_edit.setDisplayFormat("HH:mm")
        time_edit.setStyleSheet(INPUT_STYLE)

        s3.addWidget(QLabel("Show Date"))
        s3.addWidget(date_edit)
        s3.addWidget(QLabel("Show Time"))
        s3.addWidget(time_edit)
        s3.addStretch()

        pages.addWidget(step1)
        pages.addWidget(step2)
        pages.addWidget(step3)

        button_row = QHBoxLayout()
        back_btn = QPushButton("Back")
        back_btn.setStyleSheet(BTN)
        next_btn = QPushButton("Next")
        next_btn.setStyleSheet(BTN)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(BTN_DANGER)

        button_row.addWidget(back_btn)
        button_row.addStretch()
        button_row.addWidget(cancel_btn)
        button_row.addWidget(next_btn)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(pages)
        main_layout.addLayout(button_row)

        def update_nav_buttons():
            idx = pages.currentIndex()
            back_btn.setEnabled(idx > 0)
            next_btn.setText("Create Listing" if idx == 2 else "Next")

        def go_next():
            idx = pages.currentIndex()
            if idx == 0:
                selected_cinema_id = self._selected_cinema_id(cinema_combo)
                selected_film_id = self._selected_film_id(film_combo)
                if selected_film_id is None:
                    QMessageBox.warning(dialog, "No Film", "Please select a film to continue.")
                    return
                if selected_cinema_id is None:
                    QMessageBox.warning(dialog, "No Cinema", "Please select a cinema to continue.")
                    return
                render_screen_cards(selected_cinema_id)
                pages.setCurrentIndex(1)
            elif idx == 1:
                selected_screen_id = selected_screen["id"]
                if selected_screen_id is None:
                    QMessageBox.warning(dialog, "No Screen", "Please select a screen to continue.")
                    return
                pages.setCurrentIndex(2)
            else:
                selected_film_id = self._selected_film_id(film_combo)
                selected_screen_id = selected_screen["id"]
                if selected_film_id is None or selected_screen_id is None:
                    QMessageBox.warning(dialog, "Missing Data", "Film and screen selections are required.")
                    return
                selected_film = films.get(selected_film_id)
                show_date = date_edit.date().toPyDate()
                show_time = time_edit.time().toString("HH:mm:ss")
                if show_date < QDate.currentDate().toPyDate():
                    QMessageBox.warning(dialog, "Invalid Date", "Listing date cannot be in the past.")
                    return
                conflict = self.film_ctrl.get_listing_conflict(
                    selected_screen_id,
                    show_date,
                    show_time,
                    selected_film.duration,
                )
                if conflict:
                    QMessageBox.warning(
                        dialog,
                        "Time Slot Not Available",
                        f"This screen is occupied by '{conflict['title']}' "
                        f"from {conflict['start']} to {conflict['end']}.\n"
                        "Please change the time or go back and pick another screen.",
                    )
                    return
                ok = self.film_ctrl.add_listing(
                    selected_film_id,
                    selected_screen_id,
                    show_date,
                    show_time,
                    _session_for_qtime(time_edit.time()),
                )
                if ok:
                    QMessageBox.information(dialog, "Success", "Listing created successfully.")
                    self._load_listings()
                    if hasattr(self, "m_listing_id"):
                        self._load_manager_booking_listing_options()
                    dialog.accept()
                else:
                    QMessageBox.critical(
                        dialog,
                        "Failed",
                        getattr(self.film_ctrl, "last_error", "")
                        or "Could not create listing. Check your selections and try again.",
                    )
                    return
            update_nav_buttons()

        def go_back():
            idx = pages.currentIndex()
            if idx > 0:
                pages.setCurrentIndex(idx - 1)
                update_nav_buttons()

        back_btn.clicked.connect(go_back)
        next_btn.clicked.connect(go_next)
        cancel_btn.clicked.connect(dialog.reject)

        update_nav_buttons()
        dialog.exec()

    def _remove_listing(self, listing_id=None):
        if listing_id is None:
            listing_id = self.l_remove_id.value()
        reply = QMessageBox.question(
            self, "Confirm", f"Remove listing ID {listing_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.film_ctrl.listing_has_bookings(listing_id):
                QMessageBox.warning(
                    self,
                    "Cannot Remove Listing",
                    "This listing already has bookings, so it cannot be removed."
                )
                return
            ok = self.film_ctrl.remove_listing(listing_id)
            if ok:
                QMessageBox.information(self, "Removed", "Listing removed.")
                self._load_listings()
                if hasattr(self, "m_listing_id"):
                    self._load_manager_booking_listing_options()
            else:
                QMessageBox.critical(self, "Failed", "Could not remove listing.")


    # ── Book Tickets tab ──────────────────────────────────────────────────────
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

        self.m_listing_id = QComboBox()
        self.m_listing_id.setStyleSheet(INPUT_STYLE)
        self.m_listing_id.setMinimumHeight(38)
        self.m_listing_id.currentIndexChanged.connect(self._on_manager_listing_changed)

        self.m_listing_info = QLabel("Select a listing to see film details")
        self.m_listing_info.setStyleSheet(f"""
            background-color: {INPUT}; color: {MUTED};
            border: 1px solid {BORDER}; border-radius: 4px;
            padding: 6px 8px; font-size: 11px;
        """)
        self.m_listing_info.setWordWrap(True)
        self.m_listing_info.setMinimumHeight(28)

        self.ab_cinema_name = QLabel("")
        self.ab_cinema_name.setStyleSheet(f"color: {TEXT}; font-size: 11px; font-weight: bold; background: transparent;")
        self.ab_city_name = QLabel("")
        self.ab_city_name.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent;")

        self.ab_seats_info = QLabel("No seats selected")
        self.ab_seats_info.setStyleSheet(f"color: {MUTED}; font-size: 11px; background: transparent;")

        sel_cl.addWidget(fl("LISTING"))
        sel_cl.addWidget(self.m_listing_id)
        sel_cl.addWidget(self.m_listing_info)
        sel_cl.addWidget(self.ab_cinema_name)
        sel_cl.addWidget(self.ab_city_name)

        # ── Seat map card ─────────────────────────────────────────────────
        seat_card = QFrame()
        seat_card.setObjectName("seatCard")
        self.m_seat_card = seat_card
        seat_card.setStyleSheet(
            f"QFrame#seatCard {{ background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 4px; }}"
        )
        sc_layout = QVBoxLayout(seat_card)
        sc_layout.setContentsMargins(1, 1, 1, 1)
        sc_layout.setSpacing(0)

        seat_hdr = QWidget()
        seat_hdr.setFixedHeight(54)
        seat_hdr_h = QHBoxLayout(seat_hdr)
        seat_hdr_h.setContentsMargins(22, 0, 22, 0)
        seat_hdr_h.setSpacing(12)
        self.m_seat_map_title = QLabel("Seat Map")
        self.m_seat_map_title.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        self.m_seat_map_title.setStyleSheet(f"color: {TEXT}; background: transparent;")
        seat_hdr_h.addWidget(self.m_seat_map_title)
        seat_hdr_h.addStretch()
        seat_hdr_h.addWidget(self.ab_seats_info)

        seat_div = QWidget()
        seat_div.setFixedHeight(1)
        seat_div.setStyleSheet(f"background-color: {BORDER};")

        self.m_seat_map_scroll = QScrollArea()
        self.m_seat_map_scroll.setWidgetResizable(True)
        self.m_seat_map_scroll.setMinimumHeight(520)
        self.m_seat_map_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.m_seat_map_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.m_seat_map_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.m_seat_map_scroll.setStyleSheet(f"QScrollArea {{ background-color: {CARD}; border: none; }}")
        self.m_seat_map_body = QWidget()
        self.m_seat_map_body.setStyleSheet(f"background-color: {CARD};")
        self.m_seat_map_layout = QVBoxLayout(self.m_seat_map_body)
        self.m_seat_map_layout.setContentsMargins(16, 16, 16, 16)
        self.m_seat_map_layout.setSpacing(10)
        self.m_seat_map_scroll.setWidget(self.m_seat_map_body)

        sc_layout.addWidget(seat_hdr)
        sc_layout.addWidget(seat_div)
        sc_layout.addWidget(self.m_seat_map_scroll)

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

        self.ab_price_lbl = QLabel("")
        self.ab_price_lbl.setStyleSheet(
            f"color: {SUCCESS}; font-size: 13px; font-weight: bold; background: transparent;"
        )

        self.ab_name = QLineEdit()
        self.ab_name.setPlaceholderText("Customer name")
        self.ab_name.setStyleSheet(INPUT_STYLE)

        self.ab_phone = QLineEdit()
        self.ab_phone.setPlaceholderText("Phone number")
        self.ab_phone.setStyleSheet(INPUT_STYLE)

        self.ab_email = QLineEdit()
        self.ab_email.setPlaceholderText("Email address")
        self.ab_email.setStyleSheet(INPUT_STYLE)

        book_btn = QPushButton("Confirm Booking")
        book_btn.setStyleSheet(BTN)
        book_btn.setMinimumHeight(42)
        book_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        book_btn.clicked.connect(self._confirm_booking)

        det_cl.addWidget(det_title)
        det_cl.addSpacing(4)
        det_cl.addWidget(thin_sep())
        det_cl.addSpacing(10)
        det_cl.addWidget(self.ab_price_lbl)
        det_cl.addSpacing(10)
        for widget_item, label_text in [
            (self.ab_name,  "CUSTOMER NAME"),
            (self.ab_phone, "CUSTOMER PHONE"),
            (self.ab_email, "CUSTOMER EMAIL"),
        ]:
            det_cl.addWidget(fl(label_text))
            det_cl.addSpacing(6)
            det_cl.addWidget(widget_item)
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
        seat_col_layout = QVBoxLayout(seat_col)
        seat_col_layout.setContentsMargins(0, 0, 0, 0)
        seat_col_layout.setSpacing(0)
        seat_col_layout.addWidget(seat_card)
        content_row.addWidget(seat_col, 1)

        page_layout.addLayout(hdr_row)
        page_layout.addLayout(content_row, 1)

        self._load_manager_booking_listing_options()
        self._set_manager_seat_map_visible(False)
        outer.setWidget(widget)
        return outer

    def _set_manager_seat_map_visible(self, visible):
        self.m_seat_card.setVisible(visible)

    def _format_manager_booking_listing(self, listing, film_title):
        cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing.listing_id)
        cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id) if cinema_id else ("?", "?")
        return (
            f"{film_title} | {listing.show_date} | {listing.show_time} | "
            f"{listing.show_time_category.value} | {cinema_name}, {city_name}"
        )

    def _load_manager_booking_listing_options(self):
        listings = [
            listing for listing in self.film_ctrl.get_all_listings()
            if _listing_is_bookable(listing)
        ]
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}

        self.m_listing_id.blockSignals(True)
        self.m_listing_id.clear()

        for listing in listings:
            film_title = films.get(listing.film_id, "Unknown")
            display_text = self._format_manager_booking_listing(listing, film_title)
            self.m_listing_id.addItem(display_text, listing.listing_id)

        self.m_listing_id.setEditable(True)
        self.m_listing_id.setStyleSheet(SEARCH_COMBO_STYLE)
        self.m_listing_id.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.m_listing_id.lineEdit().setPlaceholderText("Search and select listing")
        self.m_listing_id.setCurrentIndex(-1)
        completer = self.m_listing_id.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)

        self.m_listing_id.blockSignals(False)

    def _on_manager_listing_changed(self, index):
        if index < 0:
            return
        listing_id = self.m_listing_id.currentData()
        if listing_id is None:
            self._set_manager_seat_map_visible(False)
            self._clear_manager_seat_map()
            return
        self._on_listing_changed(listing_id)

    def _clear_manager_seat_map(self, message="Select a listing to view seats."):
        def clear_child_layout(child_layout):
            while child_layout.count():
                child_item = child_layout.takeAt(0)
                child_widget = child_item.widget()
                nested_layout = child_item.layout()
                if child_widget:
                    child_widget.deleteLater()
                elif nested_layout:
                    clear_child_layout(nested_layout)

        while self.m_seat_map_layout.count():
            item = self.m_seat_map_layout.takeAt(0)
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
        self.m_seat_map_layout.addWidget(message_lbl)
        self.m_seat_map_layout.addStretch()

    def _manager_available_seat_style(self, base_color):
        return f"""
            QPushButton {{
                background-color: {base_color}; color: {MUTED};
                border-radius: 3px; border: 1px solid #4a4f52; font-size: 8px;
            }}
            QPushButton:hover {{
                background-color: #5f6368; color: {TEXT}; border-color: {ACCENT};
            }}
        """

    def _render_manager_seat_map(self, listing, film_title):
        seats = self.booking_ctrl.get_seats_for_listing(listing.listing_id)
        if not seats:
            self._clear_manager_seat_map("No seats found for this listing.")
            return

        self._clear_manager_seat_map("")
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
        self.m_seat_map_layout.addWidget(header)
        self.m_seat_map_layout.addWidget(screen)

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

        self._ab_seat_data = {seat[0]: seat for seat in seats}
        self._m_seat_buttons = {}

        for seat_type in ["LOWER_HALL", "UPPER_GALLERY", "VIP"]:
            type_seats = groups.get(seat_type, [])
            if not type_seats:
                continue
            section_lbl = QLabel(labels.get(seat_type, seat_type))
            section_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            section_lbl.setStyleSheet(f"color: {MUTED}; font-size: 10px; letter-spacing: 1px;")
            self.m_seat_map_layout.addWidget(section_lbl)

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
                        seat_btn.setStyleSheet(self._manager_available_seat_style(available_colors.get(st, INPUT)))
                        seat_btn.clicked.connect(
                            lambda _, sid=seat_id, listing_ref=listing: self._toggle_manager_embedded_seat(sid, listing_ref)
                        )
                    else:
                        seat_btn.setStyleSheet(booked_style)
                        seat_btn.setEnabled(False)
                    self._m_seat_buttons[seat_id] = (seat_btn, st)
                    row_layout.addWidget(seat_btn)
                row_layout.addStretch()
                self.m_seat_map_layout.addWidget(row_widget)

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
        self.m_seat_map_layout.addLayout(legend)
        self.m_seat_map_layout.addStretch()

    def _toggle_manager_embedded_seat(self, seat_id, listing):
        button, seat_type = self._m_seat_buttons[seat_id]
        if seat_id in self._ab_selected_seat_ids:
            self._ab_selected_seat_ids.remove(seat_id)
            button.setStyleSheet(self._manager_available_seat_style({
                "LOWER_HALL": "#3c4043",
                "UPPER_GALLERY": "#37404a",
                "VIP": "#3d2e00",
            }.get(seat_type, INPUT)))
        else:
            self._ab_selected_seat_ids.append(seat_id)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FDD835; color: #202124;
                    border-radius: 3px; border: none;
                    font-size: 8px; font-weight: bold;
                }
            """)

        self._ab_selected_seat_nums = [
            self._ab_seat_data[sid][1]
            for sid in self._ab_selected_seat_ids
        ]
        if self._ab_selected_seat_nums:
            self.ab_seats_info.setText(f"Seats: {', '.join(self._ab_selected_seat_nums)}")
            cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing.listing_id)
            total = self.booking_ctrl.calculate_price_for_seat_ids(
                cinema_id, listing.show_time_category, self._ab_selected_seat_ids)
            self.ab_price_lbl.setText(f"Total Price: £{total}")
            self.ab_price_lbl.setStyleSheet(f"color: {SUCCESS}; font-size: 13px;")
        else:
            self.ab_seats_info.setText("No seats selected")
            self.ab_price_lbl.setText("")

    def _on_listing_changed(self, listing_id):
        self._ab_selected_seat_ids = []
        self._ab_selected_seat_nums = []
        self.ab_seats_info.setText("No seats selected")
        self.ab_price_lbl.setText("")
        listings = self.film_ctrl.get_all_listings()
        listing = next((l for l in listings if l.listing_id == listing_id), None)
        if not listing:
            self.ab_cinema_name.setText("No listing found for this ID")
            self.ab_city_name.setText("")
            self._set_manager_seat_map_visible(False)
            self._clear_manager_seat_map()
            return
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        film_title = films.get(listing.film_id, "Unknown Film")
        cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing_id)
        cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id) if cinema_id else ("?", "?")
        self.ab_cinema_name.setText(f"Cinema: {cinema_name} (ID: {cinema_id})" if cinema_id else "Cinema: ?")
        self.ab_city_name.setText(f"City: {city_name}")
        self._set_manager_seat_map_visible(True)
        self._render_manager_seat_map(listing, film_title)

    def _confirm_booking(self):
        listing_id = self.m_listing_id.currentData()
        if listing_id is None:
            QMessageBox.warning(self, "Error", "Please select a listing first.")
            return
        name = self.ab_name.text().strip()
        phone = self.ab_phone.text().strip()
        email = self.ab_email.text().strip()

        if not hasattr(self, "_ab_selected_seat_ids") or not self._ab_selected_seat_ids:
            QMessageBox.warning(self, "No Seats", "Please select seats first.")
            return
        if not name or not phone or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all customer details.")
            return

        listings = self.film_ctrl.get_all_listings()
        listing = next((l for l in listings if l.listing_id == listing_id), None)
        if not listing:
            QMessageBox.critical(self, "Error", "Listing not found.")
            return

        cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing_id)
        if not cinema_id:
            QMessageBox.critical(self, "Error", "Could not determine cinema for this listing.")
            return

        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        film_title = films.get(listing.film_id, "Unknown Film")
        cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id)
        total_price = self.booking_ctrl.calculate_price_for_seat_ids(
            cinema_id, listing.show_time_category, self._ab_selected_seat_ids)

        customer_id = self.booking_ctrl.get_customer_or_create(name, phone, email)
        if customer_id is None:
            QMessageBox.warning(
                self,
                "Invalid Customer Details",
                getattr(self.booking_ctrl, "last_error", "") or "Please check the customer details.")
            return

        booking_ref = self.booking_ctrl.create_booking_with_seats(
            self.user.user_id, listing_id, customer_id,
            self._ab_selected_seat_ids, cinema_id,
            listing.show_time_category, self.user)

        if booking_ref:
            seat_nums = self._ab_selected_seat_nums
            screen_number = self.booking_ctrl.get_screen_number_for_listing(listing_id)
            booking_date = self.booking_ctrl.get_booking_date_for_reference(booking_ref)
            self._ab_selected_seat_ids = []
            self._ab_selected_seat_nums = []
            for field in [self.ab_name, self.ab_phone, self.ab_email]:
                field.clear()
            self.ab_seats_info.setText("No seats selected")
            self.ab_price_lbl.setText("")
            ticket = TicketDialog(
                self, booking_ref, film_title, cinema_name, city_name,
                listing.show_date, listing.show_time,
                listing.show_time_category.value,
                ", ".join(seat_nums),
                len(seat_nums), total_price,
                screen_number, booking_date)
            ticket.exec()
            self._on_listing_changed(listing_id)
        else:
            QMessageBox.critical(self, "Failed", "Booking failed. Please try again.")

    # ── Cancel Booking tab ────────────────────────────────────────────────────
    def _build_cancel_tab(self):
        widget = QWidget()
        root = QVBoxLayout(widget)
        root.setContentsMargins(28, 8, 28, 28)
        root.setSpacing(20)

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
        self.cancel_ref.setStyleSheet(INPUT_STYLE)

        cancel_btn = QPushButton("Cancel Booking")
        cancel_btn.setStyleSheet(BTN_DANGER)
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
                f"color: {ACCENT}; font-size: 12px; background: transparent;")
            self.cancel_ref.clear()
        else:
            self.cancel_result.setText(
                getattr(self.cancel_ctrl, "last_error", "") or "Cancellation failed. Check the reference and try again.")
            self.cancel_result.setStyleSheet(
                f"color: {DANGER}; font-size: 12px; background: transparent;")
        self.cancel_result.show()

    def _logout(self):
        from view.login_view import LoginView
        self.login = LoginView()
        self.login.show()
        self.close()
