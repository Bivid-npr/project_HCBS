from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QWidget,
                              QLabel, QPushButton, QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

DARK = "#202124"
CARD = "#292a2d"
INPUT = "#303134"
TEXT = "#e8eaed"
MUTED = "#9aa0a6"
ACCENT = "#8ab4f8"
BORDER = "#5f6368"

SEATS_PER_ROW = 10
AVAIL = {"LOWER_HALL": "#3c4043", "UPPER_GALLERY": "#37404a", "VIP": "#3d2e00"}
SELECTED = "#FDD835"
BOOKED = "#1a1c1e"


def _avail_style(base):
    return f"""
        QPushButton {{
            background-color: {base}; color: #9aa0a6;
            border-radius: 3px; border: 1px solid #4a4f52; font-size: 8px;
        }}
        QPushButton:hover {{
            background-color: #5f6368; color: #e8eaed; border-color: #8ab4f8;
        }}
    """

SEL_STYLE = """
    QPushButton {
        background-color: #FDD835; color: #202124;
        border-radius: 3px; border: none;
        font-size: 8px; font-weight: bold;
    }
"""
BOOKED_STYLE = """
    QPushButton {
        background-color: #1a1c1e; color: #3c4043;
        border-radius: 3px; border: 1px solid #2a2d30; font-size: 8px;
    }
"""


class SeatMapDialog(QDialog):
    def __init__(self, parent, seats, film_title, show_date, show_time):
        """seats: list of (seat_id, seat_number, seat_type, status)"""
        super().__init__(parent)
        self.setWindowTitle(f"Select Seats — {film_title}")
        self.setModal(True)
        self.setMinimumSize(740, 560)
        self.setStyleSheet(f"background-color: {DARK};")

        self._selected = []
        self._btn_map = {}
        self._seat_data = {s[0]: s for s in seats}

        self._build_ui(seats, film_title, show_date, show_time)

    def _build_ui(self, seats, film_title, show_date, show_time):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setSpacing(10)

        header = QLabel(f"{film_title}   ·   {show_date}   ·   {show_time}")
        header.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        header.setStyleSheet(f"color: {TEXT};")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        screen = QLabel("S  C  R  E  E  N")
        screen.setFixedHeight(30)
        screen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        screen.setStyleSheet(f"""
            background: qlineargradient(x1:0.5, y1:0, x2:0.5, y2:1,
                stop:0 #6e7478, stop:1 {CARD});
            color: {MUTED}; font-size: 10px; letter-spacing: 6px;
            border-radius: 4px;
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{ border: none; background: transparent; }}
            QScrollBar:vertical {{ background: {INPUT}; width: 6px; }}
            QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 3px; }}
        """)

        inner = QWidget()
        inner.setStyleSheet(f"background-color: {DARK};")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setSpacing(12)
        inner_layout.setContentsMargins(8, 8, 8, 8)
        scroll.setWidget(inner)

        groups = {"LOWER_HALL": [], "UPPER_GALLERY": [], "VIP": []}
        for s in seats:
            groups[s[2]].append(s)

        labels = {
            "LOWER_HALL": "Lower Hall",
            "UPPER_GALLERY": "Upper Gallery",
            "VIP": "VIP",
        }

        for seat_type in ["LOWER_HALL", "UPPER_GALLERY", "VIP"]:
            type_seats = groups[seat_type]
            if not type_seats:
                continue

            sec_lbl = QLabel(f"── {labels[seat_type]} ──")
            sec_lbl.setStyleSheet(
                f"color: {MUTED}; font-size: 10px; letter-spacing: 2px;")
            sec_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            inner_layout.addWidget(sec_lbl)

            base_color = AVAIL[seat_type]
            num_rows = (len(type_seats) + SEATS_PER_ROW - 1) // SEATS_PER_ROW

            for row_idx in range(num_rows):
                row_seats = type_seats[
                    row_idx * SEATS_PER_ROW:(row_idx + 1) * SEATS_PER_ROW]

                row_w = QWidget()
                row_w.setStyleSheet("background: transparent;")
                row_layout = QHBoxLayout(row_w)
                row_layout.setSpacing(3)
                row_layout.setContentsMargins(0, 0, 0, 0)

                rn_l = QLabel(str(row_idx + 1))
                rn_l.setFixedWidth(22)
                rn_l.setStyleSheet(f"color: {MUTED}; font-size: 10px;")
                rn_l.setAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                row_layout.addWidget(rn_l)

                for col_idx, (seat_id, seat_num, st, status) in enumerate(row_seats):
                    if col_idx == 5:
                        row_layout.addSpacing(18)

                    btn = QPushButton(seat_num)
                    btn.setFixedSize(52, 32)

                    if status == "AVAILABLE":
                        btn.setStyleSheet(_avail_style(base_color))
                        btn.clicked.connect(
                            lambda _, sid=seat_id: self._toggle(sid))
                    else:
                        btn.setStyleSheet(BOOKED_STYLE)
                        btn.setEnabled(False)

                    self._btn_map[seat_id] = (btn, seat_type)
                    row_layout.addWidget(btn)

                row_layout.addStretch()

                rn_r = QLabel(str(row_idx + 1))
                rn_r.setFixedWidth(22)
                rn_r.setStyleSheet(f"color: {MUTED}; font-size: 10px;")
                rn_r.setAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                row_layout.addWidget(rn_r)

                inner_layout.addWidget(row_w)

        inner_layout.addStretch()

        legend = QHBoxLayout()
        legend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for color, label in [
            (AVAIL["LOWER_HALL"], "Available"),
            (SELECTED, "Selected"),
            (BOOKED, "Booked"),
        ]:
            box = QLabel()
            box.setFixedSize(18, 18)
            box.setStyleSheet(
                f"background:{color}; border-radius:3px; border:1px solid {BORDER};")
            lbl = QLabel(label)
            lbl.setStyleSheet(f"color:{MUTED}; font-size:11px;")
            legend.addWidget(box)
            legend.addWidget(lbl)
            legend.addSpacing(20)

        self.summary_lbl = QLabel("No seats selected")
        self.summary_lbl.setStyleSheet(f"color: {ACCENT}; font-size: 12px;")
        self.summary_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_row = QHBoxLayout()

        self.confirm_btn = QPushButton("Confirm Selection (0 seats)")
        self.confirm_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {ACCENT}; color: #202124;
                font-weight: bold; border-radius: 4px;
                padding: 8px 24px; border: none; font-size: 13px;
            }}
            QPushButton:hover {{ background-color: #aecbfa; }}
        """)
        self.confirm_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent; color: {MUTED};
                border: 1px solid {BORDER}; border-radius: 4px;
                padding: 8px 20px; font-size: 13px;
            }}
            QPushButton:hover {{ color: {TEXT}; }}
        """)
        cancel_btn.clicked.connect(self.reject)

        btn_row.addStretch()
        btn_row.addWidget(self.confirm_btn)
        btn_row.addWidget(cancel_btn)

        layout.addWidget(header)
        layout.addWidget(screen)
        layout.addWidget(scroll)
        layout.addLayout(legend)
        layout.addWidget(self.summary_lbl)
        layout.addLayout(btn_row)

    def _toggle(self, seat_id):
        btn, seat_type = self._btn_map[seat_id]
        if seat_id in self._selected:
            self._selected.remove(seat_id)
            btn.setStyleSheet(_avail_style(AVAIL[seat_type]))
        else:
            self._selected.append(seat_id)
            btn.setStyleSheet(SEL_STYLE)

        n = len(self._selected)
        self.confirm_btn.setText(
            f"Confirm Selection ({n} seat{'s' if n != 1 else ''})")
        if n == 0:
            self.summary_lbl.setText("No seats selected")
        else:
            nums = [self._seat_data[sid][1] for sid in self._selected]
            self.summary_lbl.setText(f"Selected: {', '.join(nums)}")

    def get_selected_seat_ids(self):
        return list(self._selected)
