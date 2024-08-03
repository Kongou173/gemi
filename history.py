from __future__ import annotations

import base64
import json
import os


class HistoryHandler:
    def __init__(self, directory: str) -> None:
        self.directory = directory

    def __call__(self, name: str) -> History:
        return History(f'{self.directory}/{name}.json')


class History:
    def __init__(self, path: str) -> None:
        self.path = path

    def __enter__(self) -> list[dict]:
        self.cursor = self.load()
        return self.cursor

    def __exit__(self, ex_type, ex_value, trace) -> None:
        self.save(self.cursor)

    def load(self) -> list:
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save(self, history: list) -> None:
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=4, ensure_ascii=False)

    def __repr__(self) -> str:
        return f'<History {str(self.cursor)[:100]}>'


def to_jsonable(history: dict) -> dict:
    for part in history['parts']:
        if 'inline_data' in part:
            b64_data = base64.b64encode(part['inline_data']['data']).decode('utf-8')
            part['inline_data']['data'] = b64_data
    return history
