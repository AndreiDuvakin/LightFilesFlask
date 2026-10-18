from dataclasses import dataclass


@dataclass
class LoginResultModel:
    success: bool
    error: str | None = None
