from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QTableWidget, QTableWidgetItem,
                              QLineEdit, QComboBox, QSpinBox, QCompleter, QDialog,
                              QMessageBox, QFrame, QHeaderView, QDateEdit,
                              QDoubleSpinBox, QTimeEdit, QScrollArea,
                              QStackedWidget, QButtonGroup, QGridLayout,
                              QSizePolicy)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont, QColor
from controller.cinema_controller import CinemaController
from controller.film_controller import FilmController
from controller.report_factory import ReportFactory
from controller.auth_controller import AuthController
from controller.booking_controller import BookingController
from controller.cancellation_controller import CancellationController
from view.staff_view import TicketDialog
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
    QLineEdit, QComboBox, QSpinBox, QDateEdit, QTimeEdit, QDoubleSpinBox {{
        background-color: {INPUT}; color: {TEXT};
        border: 1px solid {BORDER}; border-radius: 4px;
        padding: 6px 10px; font-size: 12px;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus,
    QDateEdit:focus, QTimeEdit:focus, QDoubleSpinBox:focus {{
        border: 1px solid {ACCENT};
    }}
    QComboBox QAbstractItemView {{
        background-color: {CARD}; color: {TEXT};
        selection-background-color: {ACCENT};
    }}
"""
TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {CARD}; color: {TEXT};
        gridline-color: {BORDER}; border: none; font-size: 12px;
    }}
    QHeaderView::section {{
        background-color: {INPUT}; color: {ACCENT};
        font-weight: bold; padding: 6px; border: none;
    }}
    QTableWidget::item:selected {{ background-color: #3c4043; }}
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

PAGE_STYLE = f"""
    QWidget#pageShell {{
        background-color: {DARK};
    }}
"""

CARD_STYLE = f"""
    QFrame {{
        background-color: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
    }}
"""


class AdminView(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.cinema_ctrl = CinemaController()
        self.film_ctrl = FilmController()
        self.auth_ctrl = AuthController()
        self.booking_ctrl = BookingController()
        self.cancel_ctrl = CancellationController()
        self.setWindowTitle(f"Horizon Cinemas - Administration | {user.full_name}")
        self.setMinimumSize(1180, 760)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet(f"background-color: {DARK};")

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header = QFrame()
        header.setStyleSheet(f"background-color: {CARD}; border-bottom: 1px solid {BORDER};")
        header.setFixedHeight(72)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(24, 0, 24, 0)
        h_layout.setSpacing(14)

        title_lbl = QLabel("Horizon Cinemas")
        title_lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_lbl.setStyleSheet(f"color: {TEXT};")

        subtitle_lbl = QLabel("Administration portal")
        subtitle_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        user_lbl = QLabel(f"  {self.user.full_name}  |  Admin")
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

        main_layout.addWidget(header)
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(16, 16, 16, 16)
        body_layout.setSpacing(16)

        sidebar = QFrame()
        sidebar.setFixedWidth(238)
        sidebar.setStyleSheet(f"background-color: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(16, 16, 16, 16)
        sidebar_layout.setSpacing(8)

        nav_title = QLabel("Workspace")
        nav_title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        nav_title.setStyleSheet(f"color: {TEXT};")

        nav_hint = QLabel("Choose one task at a time.")
        nav_hint.setWordWrap(True)
        nav_hint.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        sidebar_layout.addWidget(nav_title)
        sidebar_layout.addWidget(nav_hint)

        self._nav_group = QButtonGroup(self)
        self._nav_group.setExclusive(True)
        self._nav_buttons = []

        self.pages = QStackedWidget()
        self.pages.setStyleSheet(PAGE_STYLE)

        pages = [
            ("Films", self._build_films_tab()),
            ("Listings", self._build_listings_tab()),
            ("Listing History", self._build_listing_history_tab()),
            ("Book Tickets", self._build_booking_tab()),
            ("Staff Registration", self._build_staff_registration_tab()),
            ("Cancel Booking", self._build_cancel_tab()),
            ("Reports", self._build_reports_tab()),
        ]

        for index, (label, page_widget) in enumerate(pages):
            self.pages.addWidget(page_widget)
            nav_button = QPushButton(label)
            nav_button.setCheckable(True)
            nav_button.setStyleSheet(NAV_STYLE)
            nav_button.clicked.connect(lambda checked=False, page_index=index: self._set_page(page_index))
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
        main_layout.addWidget(body, 1)

        self._set_page(0)

    def _set_page(self, index):
        self.pages.setCurrentIndex(index)
        for btn_index, button in enumerate(self._nav_buttons):
            button.setChecked(btn_index == index)

    def _build_overview_page(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        hero = QFrame()
        hero.setStyleSheet(CARD_STYLE)
        hero_layout = QVBoxLayout(hero)
        hero_layout.setContentsMargins(20, 20, 20, 20)
        hero_layout.setSpacing(8)

        title = QLabel("Administration dashboard")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")

        description = QLabel(
            "Use this portal to manage film content, schedule listings, process bookings, "
            "handle cancellations, and generate reports without switching between unrelated screens."
        )
        description.setWordWrap(True)
        description.setStyleSheet(f"color: {MUTED}; font-size: 12px; line-height: 1.4;")

        hero_layout.addWidget(title)
        hero_layout.addWidget(description)

        metrics = QGridLayout()
        metrics.setHorizontalSpacing(12)
        metrics.setVerticalSpacing(12)

        films_total = len(self.film_ctrl.get_all_films())
        listings_total = len(self.film_ctrl.get_all_listings())
        today_text = QDate.currentDate().toString("dddd, d MMMM yyyy")

        metrics.addWidget(self._make_metric_card("Films in catalogue", str(films_total), "Manage titles and metadata"), 0, 0)
        metrics.addWidget(self._make_metric_card("Scheduled listings", str(listings_total), "Set up screenings and showtimes"), 0, 1)
        metrics.addWidget(self._make_metric_card("Today", today_text, "Operational overview"), 1, 0)
        metrics.addWidget(self._make_metric_card("Workflow", "Content to booking", "A clear sequence for daily tasks"), 1, 1)

        quick_actions = QFrame()
        quick_actions.setStyleSheet(CARD_STYLE)
        quick_layout = QVBoxLayout(quick_actions)
        quick_layout.setContentsMargins(20, 20, 20, 20)
        quick_layout.setSpacing(10)

        quick_title = QLabel("Quick actions")
        quick_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        quick_title.setStyleSheet(f"color: {TEXT};")

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        actions = [
            ("Manage Films", 1),
            ("Manage Listings", 2),
            ("Book Tickets", 3),
            ("Register Staff", 4),
            ("Cancel Booking", 5),
            ("View Reports", 6),
        ]

        for label, page_index in actions:
            btn = QPushButton(label)
            btn.setStyleSheet(BTN)
            btn.clicked.connect(lambda checked=False, page=page_index: self._set_page(page))
            action_row.addWidget(btn)

        quick_layout.addWidget(quick_title)
        quick_layout.addLayout(action_row)

        layout.addWidget(hero)
        layout.addLayout(metrics)
        layout.addWidget(quick_actions)
        layout.addStretch()
        return widget

    def _make_metric_card(self, title, value, note):
        card = QFrame()
        card.setStyleSheet(CARD_STYLE)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(6)

        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px; text-transform: uppercase; letter-spacing: 1px;")

        value_lbl = QLabel(value)
        value_lbl.setWordWrap(True)
        value_lbl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        value_lbl.setStyleSheet(f"color: {TEXT};")

        note_lbl = QLabel(note)
        note_lbl.setWordWrap(True)
        note_lbl.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        card_layout.addWidget(title_lbl)
        card_layout.addWidget(value_lbl)
        card_layout.addWidget(note_lbl)
        return card

    # ── Films tab ─────────────────────────────────────────────────────────────
    def _build_films_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(BTN)
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self._load_films)

        self.films_table = QTableWidget()
        self.films_table.setStyleSheet(TABLE_STYLE)
        self.films_table.setColumnCount(5)
        self.films_table.setHorizontalHeaderLabels(
            ["ID", "Title", "Genre", "Rating", "Duration"])
        self.films_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.films_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.films_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        left_layout.addWidget(refresh_btn)
        left_layout.addWidget(self.films_table)

        # Scrollable right panel
        scroll = QScrollArea()
        scroll.setFixedWidth(296)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{
                background: {INPUT}; width: 6px; border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {BORDER}; border-radius: 3px;
            }}
        """)

        right_inner = QWidget()
        right_inner.setStyleSheet(f"background-color: {CARD}; border-radius: 8px;")
        right_layout = QVBoxLayout(right_inner)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(8)
        scroll.setWidget(right_inner)

        def lbl(text):
            l = QLabel(text)
            l.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
            return l

        def section(title):
            s = QLabel(title)
            s.setFont(QFont("Arial", 11, QFont.Weight.Bold))
            s.setStyleSheet(f"color: {TEXT};")
            return s

        def sep():
            f = QFrame()
            f.setFrameShape(QFrame.Shape.HLine)
            f.setStyleSheet(f"color: {BORDER};")
            return f

        # ── Add Film ──────────────────────────────────────────────────────
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
        add_film_btn.clicked.connect(self._add_film)

        right_layout.addWidget(section("Add New Film"))
        for w, l in [
            (self.f_title,      "Title"),
            (self.f_genre,      "Genre"),
            (self.f_age_rating, "Age Rating"),
            (self.f_imdb,       "IMDb Rating"),
            (self.f_duration,   "Duration"),
            (self.f_year,       "Release Year"),
            (self.f_cast,       "Cast Members"),
            (self.f_desc,       "Description"),
        ]:
            right_layout.addWidget(lbl(l))
            right_layout.addWidget(w)
        right_layout.addWidget(add_film_btn)

        # ── Remove Film ───────────────────────────────────────────────────
        right_layout.addWidget(sep())
        right_layout.addWidget(section("Remove Film"))

        self.f_remove_id = QSpinBox()
        self.f_remove_id.setRange(1, 9999)
        self.f_remove_id.setStyleSheet(INPUT_STYLE)

        remove_film_btn = QPushButton("Remove Film")
        remove_film_btn.setStyleSheet(BTN_DANGER)
        remove_film_btn.clicked.connect(self._remove_film)

        right_layout.addWidget(lbl("Film ID"))
        right_layout.addWidget(self.f_remove_id)
        right_layout.addWidget(remove_film_btn)

        # ── Update Film ───────────────────────────────────────────────────
        right_layout.addWidget(sep())
        right_layout.addWidget(section("Update Film"))

        load_row = QHBoxLayout()
        self.f_load_id = QSpinBox()
        self.f_load_id.setRange(1, 9999)
        self.f_load_id.setStyleSheet(INPUT_STYLE)
        load_btn = QPushButton("Load")
        load_btn.setStyleSheet(BTN)
        load_btn.setFixedWidth(60)
        load_btn.clicked.connect(self._load_film_for_edit)
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
        save_btn.clicked.connect(self._update_film)

        right_layout.addWidget(lbl("Film ID to edit"))
        right_layout.addLayout(load_row)
        for w, l in [
            (self.u_title,      "Title"),
            (self.u_genre,      "Genre"),
            (self.u_age_rating, "Age Rating"),
            (self.u_imdb,       "IMDb Rating"),
            (self.u_duration,   "Duration"),
            (self.u_year,       "Release Year"),
            (self.u_cast,       "Cast Members"),
            (self.u_desc,       "Description"),
        ]:
            right_layout.addWidget(lbl(l))
            right_layout.addWidget(w)
        right_layout.addWidget(save_btn)
        right_layout.addStretch()

        layout.addWidget(left)
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
            self._load_films()
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
            else:
                QMessageBox.critical(self, "Failed", "Could not remove film.")

    def _load_film_for_edit(self):
        film = self.film_ctrl.get_film_by_id(self.f_load_id.value())
        if not film:
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
            self._load_films()
        else:
            QMessageBox.critical(self, "Failed", "Update failed. Check the Film ID.")

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

    def _load_screen_options(self, combo, selected_screen_id=None, cinema_id=None):
        combo.blockSignals(True)
        combo.clear()

        screen_count = 0
        cinemas = self.cinema_ctrl.get_all_cinemas()
        if cinema_id is not None:
            cinemas = [c for c in cinemas if c.cinema_id == cinema_id]

        for cinema in cinemas:
            screens = self.cinema_ctrl.get_screens_for_cinema(cinema.cinema_id)
            for screen in screens:
                combo.addItem(
                    f"{cinema.name} | Screen {screen.screen_number} "
                    f"(ID {screen.screen_id}, Capacity {screen.capacity})",
                    screen.screen_id,
                )
                screen_count += 1

        combo.setEditable(True)
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

    # ── Listings tab ──────────────────────────────────────────────────────────
    def _build_listings_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(BTN)
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self._load_listings)

        self.listings_table = QTableWidget()
        self.listings_table.setStyleSheet(TABLE_STYLE)
        self.listings_table.setColumnCount(9)
        self.listings_table.setHorizontalHeaderLabels(
            ["Listing ID", "Film", "Screen", "Cinema", "City", "Date", "Time", "Session", "Actions"])
        self.listings_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.listings_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.listings_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.listings_table.itemSelectionChanged.connect(self._on_listing_selected)

        left_layout.addWidget(refresh_btn)
        left_layout.addWidget(self.listings_table)

        right_scroll = QScrollArea()
        right_scroll.setFixedWidth(296)
        right_scroll.setWidgetResizable(True)
        right_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right_scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background-color: {CARD}; border-radius: 8px; }}
            QScrollBar:vertical {{ background: {CARD}; width: 8px; border-radius: 4px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 4px; }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
        """)

        right = QWidget()
        right.setStyleSheet(f"background-color: {CARD};")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(8)
        right_scroll.setWidget(right)

        def lbl(text):
            label = QLabel(text)
            label.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
            return label

        add_lbl = QLabel("Add New Listing")
        add_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        add_lbl.setStyleSheet(f"color: {TEXT};")

        add_hint = QLabel("Use the guided flow to create listings with conflict checks.")
        add_hint.setWordWrap(True)
        add_hint.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        add_listing_btn = QPushButton("Add Listing")
        add_listing_btn.setStyleSheet(BTN)
        add_listing_btn.clicked.connect(self._add_listing)

        sep1 = QFrame()
        sep1.setFrameShape(QFrame.Shape.HLine)
        sep1.setStyleSheet(f"color: {BORDER};")

        # Remove Listing section moved to table Actions column
        # (Hidden for backwards compatibility - buttons now in table)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"color: {BORDER};")

        edit_lbl = QLabel("Edit Listing")
        edit_lbl.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        edit_lbl.setStyleSheet(f"color: {TEXT};")

        self.l_edit_hint = QLabel("Select a row to edit")
        self.l_edit_hint.setStyleSheet(f"color: {MUTED}; font-size: 11px; font-style: italic;")

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
        self.l_edit_date.setStyleSheet(INPUT_STYLE)

        self.l_edit_time = QTimeEdit()
        self.l_edit_time.setTime(QTime(18, 0))
        self.l_edit_time.setDisplayFormat("HH:mm")
        self.l_edit_time.setStyleSheet(INPUT_STYLE)

        self.l_edit_session = QComboBox()
        self.l_edit_session.addItems(["MORNING", "AFTERNOON", "EVENING"])
        self.l_edit_session.setStyleSheet(INPUT_STYLE)

        update_listing_btn = QPushButton("Update Listing")
        update_listing_btn.setStyleSheet(BTN)
        update_listing_btn.clicked.connect(self._update_listing)

        right_layout.addWidget(add_lbl)
        right_layout.addWidget(add_hint)
        right_layout.addWidget(add_listing_btn)
        right_layout.addWidget(sep1)
        right_layout.addWidget(sep2)
        right_layout.addWidget(edit_lbl)
        right_layout.addWidget(self.l_edit_hint)
        for widget_to_add, label_text in [
            (self.l_edit_id, "Listing ID (read-only)"),
            (self.l_edit_film_id, "Film ID"),
            (self.l_edit_screen_combo, "Screen"),
            (self.l_edit_date, "Show Date"),
            (self.l_edit_time, "Show Time"),
            (self.l_edit_session, "Session"),
        ]:
            right_layout.addWidget(lbl(label_text))
            right_layout.addWidget(widget_to_add)
        right_layout.addWidget(update_listing_btn)
        right_layout.addStretch()

        self._load_film_options(self.l_edit_film_id)
        self._load_screen_options(self.l_edit_screen_combo)

        layout.addWidget(left)
        layout.addWidget(right_scroll)
        self._load_listings()
        return widget

    def _load_listings(self):
        today = QDate.currentDate().toPyDate()
        listings = [
            listing for listing in self.film_ctrl.get_all_listings()
            if listing.show_date >= today
        ]
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
            table.setItem(row_index, 7, QTableWidgetItem(listing.show_time_category.value))

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
            delete_btn.setMaximumHeight(20)
            delete_btn.setMaximumWidth(60)
            delete_btn.clicked.connect(lambda checked, lid=listing.listing_id: self._remove_listing(lid))
            
            # Center the button in the cell
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_layout.addStretch()
            btn_layout.addWidget(delete_btn)
            btn_layout.addStretch()
            table.setCellWidget(row_index, 8, btn_container)

    def _build_listing_history_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(BTN)
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self._load_listing_history)

        self.listing_history_table = QTableWidget()
        self.listing_history_table.setStyleSheet(TABLE_STYLE)
        self.listing_history_table.setColumnCount(8)
        self.listing_history_table.setHorizontalHeaderLabels(
            ["Listing ID", "Film", "Screen", "Cinema", "City", "Date", "Time", "Session"])
        self.listing_history_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.listing_history_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.listing_history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        layout.addWidget(refresh_btn)
        layout.addWidget(self.listing_history_table)
        self._load_listing_history()
        return widget

    def _load_listing_history(self):
        today = QDate.currentDate().toPyDate()
        listings = [
            listing for listing in self.film_ctrl.get_all_listings()
            if listing.show_date < today
        ]
        self._populate_listings_table(self.listing_history_table, listings, include_actions=False)

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
        self.l_edit_session.setCurrentText(listing.show_time_category.value)
        self.l_edit_hint.setText(f"Editing listing ID {listing_id}")

    def _update_listing(self):
        from models.enums import ShowTime
        if not self.listings_table.selectedItems():
            QMessageBox.warning(self, "No Selection", "Select a listing row in the table first.")
            return
        screen_id = self._selected_screen_id(self.l_edit_screen_combo)
        if screen_id is None:
            QMessageBox.warning(self, "No Screen", "No screen is available for this listing.")
            return
        listing_id = self.l_edit_id.value()
        film_id = self._selected_film_id(self.l_edit_film_id)
        if film_id is None:
            QMessageBox.warning(self, "No Film", "Please select a film.")
            return
        ok = self.film_ctrl.update_listing(
            listing_id,
            film_id,
            screen_id,
            self.l_edit_date.date().toPyDate(),
            self.l_edit_time.time().toString("HH:mm:ss"),
            ShowTime(self.l_edit_session.currentText()))
        if ok:
            QMessageBox.information(self, "Success", f"Listing ID {listing_id} updated.")
            self._load_listings()
        else:
            QMessageBox.critical(self, "Failed", "Update failed. Check Film ID and the selected screen.")

    def _add_listing(self):
        self._open_add_listing_wizard()

    def _open_add_listing_wizard(self):
        from models.enums import ShowTime

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

        # Step 1: film + cinema
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

        # Step 2: screen in selected cinema
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

        # Step 3: schedule + validation
        step3 = QWidget()
        s3 = QVBoxLayout(step3)
        s3.setSpacing(8)
        s3.addWidget(QLabel("Step 3 of 3 - Set Time and Create"))

        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        date_edit.setStyleSheet(INPUT_STYLE)

        time_edit = QTimeEdit()
        time_edit.setTime(QTime(18, 0))
        time_edit.setDisplayFormat("HH:mm")
        time_edit.setStyleSheet(INPUT_STYLE)

        session_combo = QComboBox()
        session_combo.addItems(["MORNING", "AFTERNOON", "EVENING"])
        session_combo.setStyleSheet(INPUT_STYLE)

        s3.addWidget(QLabel("Show Date"))
        s3.addWidget(date_edit)
        s3.addWidget(QLabel("Show Time"))
        s3.addWidget(time_edit)
        s3.addWidget(QLabel("Session"))
        s3.addWidget(session_combo)
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
                    ShowTime(session_combo.currentText()),
                )
                if ok:
                    QMessageBox.information(dialog, "Success", "Listing created successfully.")
                    self._load_listings()
                    dialog.accept()
                else:
                    QMessageBox.critical(
                        dialog,
                        "Failed",
                        "Could not create listing. Check your selections and try again.",
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
        # Accept listing_id from table button, or fall back to spinbox (for backwards compatibility)
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
            else:
                QMessageBox.critical(self, "Failed", "Could not remove listing.")

    # ── Staff Registration tab ────────────────────────────────────────────────
    def _build_staff_registration_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(BTN)
        refresh_btn.setFixedWidth(100)
        refresh_btn.clicked.connect(self._load_booking_staff)

        self.staff_table = QTableWidget()
        self.staff_table.setStyleSheet(TABLE_STYLE)
        self.staff_table.setColumnCount(5)
        self.staff_table.setHorizontalHeaderLabels(
            ["User ID", "Username", "Full Name", "Email", "Assigned Cinema"])
        self.staff_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.staff_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.staff_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        left_layout.addWidget(refresh_btn)
        left_layout.addWidget(self.staff_table)

        right = QFrame()
        right.setFixedWidth(320)
        right.setStyleSheet(f"background-color: {CARD}; border-radius: 8px;")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(8)

        def lbl(text):
            label = QLabel(text)
            label.setStyleSheet(f"color: {MUTED}; font-size: 12px;")
            return label

        title = QLabel("Register Booking Staff")
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {TEXT};")

        note = QLabel("New users created here are automatically assigned the BOOKING_STAFF role.")
        note.setWordWrap(True)
        note.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        self.staff_username = QLineEdit()
        self.staff_username.setPlaceholderText("Username")
        self.staff_username.setStyleSheet(INPUT_STYLE)

        self.staff_password = QLineEdit()
        self.staff_password.setPlaceholderText("Password")
        self.staff_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.staff_password.setStyleSheet(INPUT_STYLE)

        self.staff_confirm_password = QLineEdit()
        self.staff_confirm_password.setPlaceholderText("Confirm password")
        self.staff_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.staff_confirm_password.setStyleSheet(INPUT_STYLE)

        self.staff_full_name = QLineEdit()
        self.staff_full_name.setPlaceholderText("Full name")
        self.staff_full_name.setStyleSheet(INPUT_STYLE)

        self.staff_email = QLineEdit()
        self.staff_email.setPlaceholderText("Email address")
        self.staff_email.setStyleSheet(INPUT_STYLE)

        self.staff_cinema_combo = QComboBox()
        self.staff_cinema_combo.setStyleSheet(INPUT_STYLE)
        self._load_cinema_options(self.staff_cinema_combo)

        register_btn = QPushButton("Register Staff")
        register_btn.setStyleSheet(BTN)
        register_btn.clicked.connect(self._register_booking_staff)

        right_layout.addWidget(title)
        right_layout.addWidget(note)
        for field, label in [
            (self.staff_username, "Username"),
            (self.staff_password, "Password"),
            (self.staff_confirm_password, "Confirm Password"),
            (self.staff_full_name, "Full Name"),
            (self.staff_email, "Email"),
            (self.staff_cinema_combo, "Assigned Cinema"),
        ]:
            right_layout.addWidget(lbl(label))
            right_layout.addWidget(field)
        right_layout.addWidget(register_btn)
        right_layout.addStretch()

        layout.addWidget(left)
        layout.addWidget(right)
        self._load_booking_staff()
        return widget

    def _load_booking_staff(self):
        staff_rows = self.auth_ctrl.get_booking_staff()
        cinema_map = {c.cinema_id: c.name for c in self.cinema_ctrl.get_all_cinemas()}
        self.staff_table.setRowCount(len(staff_rows))
        for row_index, (user_id, username, full_name, email, cinema_id) in enumerate(staff_rows):
            self.staff_table.setItem(row_index, 0, QTableWidgetItem(str(user_id)))
            self.staff_table.setItem(row_index, 1, QTableWidgetItem(username))
            self.staff_table.setItem(row_index, 2, QTableWidgetItem(full_name or ""))
            self.staff_table.setItem(row_index, 3, QTableWidgetItem(email or ""))
            self.staff_table.setItem(
                row_index, 4,
                QTableWidgetItem(cinema_map.get(cinema_id, "Not assigned")))

    def _register_booking_staff(self):
        username = self.staff_username.text().strip()
        password = self.staff_password.text()
        confirm_password = self.staff_confirm_password.text()
        full_name = self.staff_full_name.text().strip()
        email = self.staff_email.text().strip()
        cinema_id = self._selected_cinema_id(self.staff_cinema_combo)

        if not username or not password or not full_name or not email:
            QMessageBox.warning(self, "Input Error", "Please fill in all staff details.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Input Error", "Passwords do not match.")
            return
        if cinema_id is None:
            QMessageBox.warning(self, "Input Error", "Please select an assigned cinema.")
            return

        ok, result = self.auth_ctrl.register_booking_staff(
            username, password, full_name, email, cinema_id)
        if ok:
            QMessageBox.information(
                self,
                "Staff Registered",
                f"Booking staff '{full_name}' registered with user ID {result}."
            )
            for field in [
                self.staff_username,
                self.staff_password,
                self.staff_confirm_password,
                self.staff_full_name,
                self.staff_email,
            ]:
                field.clear()
            self.staff_cinema_combo.setCurrentIndex(-1)
            self._load_booking_staff()
        else:
            QMessageBox.critical(self, "Registration Failed", str(result))

    # ── Reports tab ───────────────────────────────────────────────────────────
    def _build_reports_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(14)

        # Controls row
        top_row = QHBoxLayout()
        self.report_combo = QComboBox()
        self.report_combo.addItems([
            "Bookings Per Listing",
            "Monthly Revenue Per Cinema",
            "Top Revenue Generating Film",
            "Staff Performance",
        ])
        self.report_combo.setStyleSheet(INPUT_STYLE)
        generate_btn = QPushButton("Generate Report")
        generate_btn.setStyleSheet(BTN)
        generate_btn.setFixedWidth(160)
        generate_btn.clicked.connect(self._generate_report)
        top_row.addWidget(self.report_combo)
        top_row.addWidget(generate_btn)

        # Report table
        self.report_table = QTableWidget()
        self.report_table.setStyleSheet(TABLE_STYLE + f"""
            QTableWidget::item {{ padding: 8px 14px; }}
            QTableWidget::item:alternate {{ background-color: #252628; }}
            QHeaderView::section {{ padding: 10px 14px; font-size: 12px; }}
        """)
        self.report_table.setAlternatingRowColors(True)
        self.report_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.report_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.report_table.verticalHeader().setVisible(False)
        self.report_table.setShowGrid(False)

        layout.addLayout(top_row)
        layout.addWidget(self.report_table)
        return widget

    def _generate_report(self):
        key_map = {
            "Bookings Per Listing":        "bookings_per_listing",
            "Monthly Revenue Per Cinema":  "monthly_revenue",
            "Top Revenue Generating Film": "top_revenue_film",
            "Staff Performance":           "staff_performance",
        }
        key = key_map[self.report_combo.currentText()]
        try:
            report = ReportFactory.create_report(key)
            headers, data = report.get_data()

            self.report_table.clear()
            self.report_table.setColumnCount(len(headers))
            self.report_table.setRowCount(len(data))
            self.report_table.setHorizontalHeaderLabels(headers)

            RIGHT_ALIGN = {"Bookings", "Revenue", "Year", "Month"}
            for row_idx, row_data in enumerate(data):
                for col_idx, header in enumerate(headers):
                    raw = row_data[col_idx]
                    if header == "Revenue":
                        try:
                            display = f"£{float(raw):.2f}"
                        except (ValueError, TypeError):
                            display = "£0.00"
                    else:
                        display = raw if raw != "None" else "—"
                    item = QTableWidgetItem(display)
                    if header in RIGHT_ALIGN:
                        item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                    if header == "Revenue":
                        item.setForeground(QColor(SUCCESS))
                        item.setFont(QFont("Arial", 11, QFont.Weight.Bold))
                    self.report_table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # ── Book Tickets tab ──────────────────────────────────────────────────────
    def _build_booking_tab(self):
        outer = QScrollArea()
        outer.setObjectName("pageShell")
        outer.setWidgetResizable(True)
        outer.setFrameShape(QFrame.Shape.NoFrame)
        outer.setStyleSheet(f"QScrollArea#pageShell {{ background-color: {DARK}; border: none; }}")

        widget = QWidget()
        widget.setObjectName("pageShell")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        def lbl(text):
            l = QLabel(text)
            l.setStyleSheet(f"color: {MUTED}; font-size: 11px;")
            return l

        self.ab_listing_id = QComboBox()
        self.ab_listing_id.setStyleSheet(INPUT_STYLE)
        self.ab_listing_id.setMinimumHeight(36)
        self.ab_listing_id.currentIndexChanged.connect(self._on_admin_listing_changed)
        self._load_booking_listing_options()
        self.ab_listing_info = QLabel()

        self.ab_seats_info = QLabel("No seats selected")
        self.ab_seats_info.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        self.ab_seat_map_title = QLabel("Seats")
        self.ab_seat_map_title.setStyleSheet(f"color: {TEXT}; font-size: 11px; font-weight: bold;")
        self.ab_seat_map_scroll = QScrollArea()
        self.ab_seat_map_scroll.setWidgetResizable(True)
        self.ab_seat_map_scroll.setFixedHeight(560)
        self.ab_seat_map_scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.ab_seat_map_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.ab_seat_map_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ab_seat_map_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ab_seat_map_scroll.setStyleSheet(f"""
            QScrollArea {{ border: 1px solid {BORDER}; border-radius: 4px; background-color: {CARD}; }}
            QScrollBar:vertical {{ background: {INPUT}; width: 6px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 3px; }}
        """)
        self.ab_seat_map_body = QWidget()
        self.ab_seat_map_body.setStyleSheet(f"background-color: {CARD};")
        self.ab_seat_map_layout = QVBoxLayout(self.ab_seat_map_body)
        self.ab_seat_map_layout.setContentsMargins(10, 10, 10, 10)
        self.ab_seat_map_layout.setSpacing(10)
        self.ab_seat_map_scroll.setWidget(self.ab_seat_map_body)

        # Cinema / City info for admin bookings
        self.ab_cinema_name = QLabel("")
        self.ab_cinema_name.setStyleSheet(f"color: {TEXT}; font-size: 11px; font-weight: bold;")
        self.ab_city_name = QLabel("")
        self.ab_city_name.setStyleSheet(f"color: {MUTED}; font-size: 11px;")

        self.ab_price_lbl = QLabel("")
        self.ab_price_lbl.setStyleSheet(f"color: {SUCCESS}; font-size: 12px;")

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
        book_btn.clicked.connect(self._admin_confirm_booking)

        layout.addWidget(lbl("Select Listing"))
        layout.addWidget(self.ab_listing_id)
        layout.addWidget(self.ab_seat_map_title)
        layout.addWidget(self.ab_seat_map_scroll)
        layout.addWidget(self.ab_seats_info)
        layout.addWidget(self.ab_cinema_name)
        layout.addWidget(self.ab_city_name)
        layout.addWidget(self.ab_price_lbl)
        for w, l in [
            (self.ab_name,  "Customer Name"),
            (self.ab_phone, "Customer Phone"),
            (self.ab_email, "Customer Email"),
        ]:
            layout.addWidget(lbl(l))
            layout.addWidget(w)
        layout.addStretch()
        layout.addWidget(book_btn)
        self._set_admin_seat_map_visible(False)
        outer.setWidget(widget)
        return outer

    def _set_admin_seat_map_visible(self, visible):
        self.ab_seat_map_title.setVisible(visible)
        self.ab_seat_map_scroll.setVisible(visible)

    def _format_admin_booking_listing(self, listing, film_title):
        cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing.listing_id)
        cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id) if cinema_id else ("?", "?")
        return (
            f"{film_title} | {listing.show_date} | {listing.show_time} | "
            f"{listing.show_time_category.value} | {cinema_name}, {city_name}"
        )

    def _load_booking_listing_options(self):
        listings = self.film_ctrl.get_all_listings()
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        
        self.ab_listing_id.blockSignals(True)
        self.ab_listing_id.clear()
        
        for listing in listings:
            film_title = films.get(listing.film_id, "Unknown")
            display_text = self._format_admin_booking_listing(listing, film_title)
            self.ab_listing_id.addItem(display_text, listing.listing_id)
        
        # Set up searchable completer
        self.ab_listing_id.setEditable(True)
        self.ab_listing_id.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
        self.ab_listing_id.lineEdit().setPlaceholderText("Search and select listing")
        self.ab_listing_id.setCurrentIndex(-1)
        completer = self.ab_listing_id.completer()
        if completer:
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        
        self.ab_listing_id.blockSignals(False)

    def _clear_admin_seat_map(self, message="Select a listing to view seats."):
        def clear_child_layout(child_layout):
            while child_layout.count():
                child_item = child_layout.takeAt(0)
                child_widget = child_item.widget()
                nested_layout = child_item.layout()
                if child_widget:
                    child_widget.deleteLater()
                elif nested_layout:
                    clear_child_layout(nested_layout)

        while self.ab_seat_map_layout.count():
            item = self.ab_seat_map_layout.takeAt(0)
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
        self.ab_seat_map_layout.addWidget(message_lbl)
        self.ab_seat_map_layout.addStretch()

    def _admin_available_seat_style(self, base_color):
        return f"""
            QPushButton {{
                background-color: {base_color}; color: {MUTED};
                border-radius: 3px; border: 1px solid #4a4f52; font-size: 8px;
            }}
            QPushButton:hover {{
                background-color: #5f6368; color: {TEXT}; border-color: {ACCENT};
            }}
        """

    def _render_admin_seat_map(self, listing, film_title):
        seats = self.booking_ctrl.get_seats_for_listing(listing.listing_id)
        if not seats:
            self._clear_admin_seat_map("No seats found for this listing.")
            return

        self._clear_admin_seat_map("")

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

        self.ab_seat_map_layout.addWidget(header)
        self.ab_seat_map_layout.addWidget(screen)

        seats_per_row = 10
        available_colors = {
            "LOWER_HALL": "#3c4043",
            "UPPER_GALLERY": "#37404a",
            "VIP": "#3d2e00",
        }
        selected_style = """
            QPushButton {
                background-color: #FDD835; color: #202124;
                border-radius: 3px; border: none;
                font-size: 8px; font-weight: bold;
            }
        """
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
        self._ab_seat_buttons = {}

        for seat_type in ["LOWER_HALL", "UPPER_GALLERY", "VIP"]:
            type_seats = groups.get(seat_type, [])
            if not type_seats:
                continue

            section_lbl = QLabel(labels.get(seat_type, seat_type))
            section_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            section_lbl.setStyleSheet(f"color: {MUTED}; font-size: 10px; letter-spacing: 1px;")
            self.ab_seat_map_layout.addWidget(section_lbl)

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
                        seat_btn.setStyleSheet(self._admin_available_seat_style(available_colors.get(st, INPUT)))
                        seat_btn.clicked.connect(
                            lambda _, sid=seat_id, listing_ref=listing: self._toggle_admin_embedded_seat(sid, listing_ref)
                        )
                    else:
                        seat_btn.setStyleSheet(booked_style)
                        seat_btn.setEnabled(False)

                    self._ab_seat_buttons[seat_id] = (seat_btn, st)
                    row_layout.addWidget(seat_btn)

                row_layout.addStretch()
                self.ab_seat_map_layout.addWidget(row_widget)

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
        self.ab_seat_map_layout.addLayout(legend)
        self.ab_seat_map_layout.addStretch()

    def _toggle_admin_embedded_seat(self, seat_id, listing):
        button, seat_type = self._ab_seat_buttons[seat_id]
        if seat_id in self._ab_selected_seat_ids:
            self._ab_selected_seat_ids.remove(seat_id)
            button.setStyleSheet(self._admin_available_seat_style({
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

    def _on_admin_listing_changed(self, index):
        if index < 0:
            return
        listing_id = self.ab_listing_id.currentData()
        if listing_id is None:
            self._set_admin_seat_map_visible(False)
            self._clear_admin_seat_map()
            return
        self._ab_selected_seat_ids = []
        self._ab_selected_seat_nums = []
        self.ab_seats_info.setText("No seats selected")
        self.ab_price_lbl.setText("")
        listings = self.film_ctrl.get_all_listings()
        listing = next((l for l in listings if l.listing_id == listing_id), None)
        if listing_id == 0:
            return
        if not listing:
            self.ab_cinema_name.setText("No listing found for this ID")
            self.ab_city_name.setText("")
            self._set_admin_seat_map_visible(False)
            self._clear_admin_seat_map()
            return
        films = {f.film_id: f.title for f in self.film_ctrl.get_all_films()}
        film_title = films.get(listing.film_id, "Unknown Film")
        cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing_id)
        cinema_name, city_name = self.booking_ctrl.get_cinema_info(cinema_id) if cinema_id else ("?", "?")
        self.ab_listing_info.setText(
            f"▶  {film_title}   |   {listing.show_date}   |   "
            f"{listing.show_time}   |   {listing.show_time_category.value}"
            f"\n    {cinema_name}, {city_name}"
        )
        self.ab_listing_info.setStyleSheet(f"""
            background-color: {INPUT}; color: {TEXT};
            border: 1px solid {ACCENT}; border-radius: 4px;
            padding: 8px 10px; font-size: 12px; font-weight: bold;
        """)
        # populate separate cinema/city labels for clarity
        self.ab_cinema_name.setText(f"Cinema: {cinema_name} (ID: {cinema_id})" if cinema_id else "Cinema: ?")
        self.ab_city_name.setText(f"City: {city_name}")
        self._set_admin_seat_map_visible(True)
        self._render_admin_seat_map(listing, film_title)

    def _admin_open_seat_map(self):
        listing_id = self.ab_listing_id.currentData()
        if listing_id is None:
            QMessageBox.warning(self, "Error", "Please select a listing first.")
            return
        listings = self.film_ctrl.get_all_listings()
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
            self._ab_selected_seat_ids = selected
            self._ab_selected_seat_nums = [s[1] for s in seats if s[0] in selected]
            cinema_id = self.booking_ctrl.get_cinema_id_for_listing(listing_id)
            total = self.booking_ctrl.calculate_price_for_seat_ids(
                cinema_id, listing.show_time_category, selected)
            self.ab_seats_info.setText(f"Seats: {', '.join(self._ab_selected_seat_nums)}")
            self.ab_price_lbl.setText(f"Total Price: £{total}")
            self.ab_price_lbl.setStyleSheet(f"color: {SUCCESS}; font-size: 13px;")

    def _admin_confirm_booking(self):
        listing_id = self.ab_listing_id.currentData()
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

        booking_ref = self.booking_ctrl.create_booking_with_seats(
            self.user.user_id, listing_id, customer_id,
            self._ab_selected_seat_ids, cinema_id,
            listing.show_time_category)

        if booking_ref:
            seat_nums = self._ab_selected_seat_nums
            screen_number = self.booking_ctrl.get_screen_number_for_listing(listing_id)
            booking_date = self.booking_ctrl.get_booking_date_for_reference(booking_ref)
            self._ab_selected_seat_ids = []
            self._ab_selected_seat_nums = []
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
            self._on_admin_listing_changed(self.ab_listing_id.currentIndex())
        else:
            QMessageBox.critical(self, "Failed", "Booking failed. Please try again.")

    # ── Cancel Booking tab ────────────────────────────────────────────────────
    def _build_cancel_tab(self):
        widget = QWidget()
        widget.setObjectName("pageShell")
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
