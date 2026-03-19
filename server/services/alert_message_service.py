from db.database import engine
from sqlalchemy import text


def create_alert_cases(alert_cases: list[int]):
    """
    Insert cases with missing admission/discharge dates into the cases table,
    so that they can be included in the alert generation process.
    """
    if not alert_cases or len(alert_cases) == 0:
        return

    with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO alert_messages (timestamp, message, type, case_id) VALUES (:id)"),
                [{"id": int(case_id)} for case_id in alert_cases],)
