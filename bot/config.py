import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class BotSettings:
    telegram_bot_token: str
    orders_group_id: int
    support_group_id: Optional[int]


def load_settings() -> BotSettings:
    # Load .env file if present
    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set. Provide it via environment or .env file.")

    orders_group_id_str = os.getenv("ORDERS_GROUP_ID", "").strip()
    if not orders_group_id_str:
        raise RuntimeError("ORDERS_GROUP_ID is not set. Add the numeric chat id of the target group.")

    try:
        orders_group_id = int(orders_group_id_str)
    except ValueError as exc:
        raise RuntimeError("ORDERS_GROUP_ID must be an integer (e.g., -1001234567890 for supergroups).") from exc

    support_group_id: Optional[int] = None
    if os.getenv("SUPPORT_GROUP_ID"):
        try:
            support_group_id = int(os.getenv("SUPPORT_GROUP_ID", "").strip())
        except ValueError as exc:
            raise RuntimeError("SUPPORT_GROUP_ID must be an integer chat id.") from exc

    return BotSettings(
        telegram_bot_token=token,
        orders_group_id=orders_group_id,
        support_group_id=support_group_id,
    )