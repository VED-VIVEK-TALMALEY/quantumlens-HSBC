# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# -------------------------------------------------------------------

from dataclasses import dataclass


@dataclass
class ExecutionStep:
    agent: str
    description: str = ""