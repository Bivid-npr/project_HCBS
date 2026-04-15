from abc import ABC, abstractmethod
from db.connection import get_connection

class IReport(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

    @abstractmethod
    def get_report_type(self) -> str:
        pass

    @abstractmethod
    def get_data(self) -> tuple:
        """Returns (headers: list[str], rows: list[list[str]])"""
        pass

class BookingsPerListingReport(IReport):
    def get_report_type(self) -> str:
        return "Bookings Per Listing"

    def get_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM report_bookings_per_listing;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        headers = ["Film", "Date", "Show Time", "Cinema", "Bookings", "Revenue"]
        data = [[str(r[1]), str(r[2]), str(r[3]), str(r[4]), str(r[5]), str(r[6])] for r in rows]
        return headers, data

    def generate(self) -> str:
        _, data = self.get_data()
        lines = [f"{'Film':<30} {'Date':<12} {'Show':<12} {'Cinema':<25} {'Bookings':>8} {'Revenue':>10}"]
        lines.append("-" * 100)
        for r in data:
            lines.append(f"{r[0]:<30} {r[1]:<12} {r[2]:<12} {r[3]:<25} {r[4]:>8} {r[5]:>10}")
        return "\n".join(lines)

class MonthlyRevenueReport(IReport):
    def get_report_type(self) -> str:
        return "Monthly Revenue Per Cinema"

    def get_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM report_monthly_revenue;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        headers = ["Cinema", "City", "Year", "Month", "Bookings", "Revenue"]
        data = [[str(r[0]), str(r[1]), str(r[2]), str(r[3]), str(r[4]), str(r[5])] for r in rows]
        return headers, data

    def generate(self) -> str:
        _, data = self.get_data()
        lines = [f"{'Cinema':<25} {'City':<12} {'Year':>6} {'Month':>6} {'Bookings':>8} {'Revenue':>10}"]
        lines.append("-" * 75)
        for r in data:
            lines.append(f"{r[0]:<25} {r[1]:<12} {r[2]:>6} {r[3]:>6} {r[4]:>8} {r[5]:>10}")
        return "\n".join(lines)

class TopRevenueFilmReport(IReport):
    def get_report_type(self) -> str:
        return "Top Revenue Generating Film"

    def get_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM report_top_revenue_film;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        headers = ["Film", "Genre", "Bookings", "Revenue"]
        data = [[str(r[0]), str(r[1]), str(r[2]), str(r[3])] for r in rows]
        return headers, data

    def generate(self) -> str:
        _, data = self.get_data()
        lines = [f"{'Film':<30} {'Genre':<15} {'Bookings':>8} {'Revenue':>10}"]
        lines.append("-" * 65)
        for r in data:
            lines.append(f"{r[0]:<30} {r[1]:<15} {r[2]:>8} {r[3]:>10}")
        return "\n".join(lines)

class StaffPerformanceReport(IReport):
    def get_report_type(self) -> str:
        return "Staff Performance"

    def get_data(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM report_staff_performance;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        headers = ["Staff Name", "Username", "Year", "Month", "Bookings", "Revenue"]
        data = [[str(r[0]), str(r[1]), str(r[2]), str(r[3]), str(r[4]), str(r[5])] for r in rows]
        return headers, data

    def generate(self) -> str:
        _, data = self.get_data()
        lines = [f"{'Staff Name':<25} {'Username':<15} {'Year':>6} {'Month':>6} {'Bookings':>8} {'Revenue':>10}"]
        lines.append("-" * 75)
        for r in data:
            lines.append(f"{r[0]:<25} {r[1]:<15} {r[2]:>6} {r[3]:>6} {r[4]:>8} {r[5]:>10}")
        return "\n".join(lines)

class ReportFactory:
    @staticmethod
    def create_report(report_type: str) -> IReport:
        reports = {
            "bookings_per_listing": BookingsPerListingReport(),
            "monthly_revenue":      MonthlyRevenueReport(),
            "top_revenue_film":     TopRevenueFilmReport(),
            "staff_performance":    StaffPerformanceReport()
        }
        report = reports.get(report_type)
        if not report:
            raise ValueError(f"Unknown report type: {report_type}")
        return report
