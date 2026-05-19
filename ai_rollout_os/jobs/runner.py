import argparse

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ai_rollout_os.core.config import get_settings
from ai_rollout_os.jobs.reminders import ReminderScheduler


def run_once() -> int:
    settings = get_settings()
    engine = create_engine(settings.database_url)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    with session_factory() as session:
        reminders = ReminderScheduler(session=session, settings=settings).run_once()
        session.commit()
        return len(reminders)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-once", action="store_true", required=True)
    parser.parse_args(argv)
    run_once()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
