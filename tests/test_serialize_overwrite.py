from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import qai_xml2ir.serialize as serialize


def _read_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_write_yaml_overwrite_requires_exact_yes(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / "a.yaml"
    serialize._OVERWRITE_APPROVED = None
    serialize.write_yaml(path, {"v": 1})

    prompts = {"count": 0}

    def fake_input(_prompt: str) -> str:
        prompts["count"] += 1
        return "yes"

    monkeypatch.setattr("builtins.input", fake_input)

    with pytest.raises(FileExistsError):
        serialize.write_yaml(path, {"v": 2})

    assert prompts["count"] == 1
    assert _read_yaml(path)["v"] == 1


def test_write_yaml_overwrite_yes_once_then_allows_all(tmp_path: Path, monkeypatch) -> None:
    a = tmp_path / "a.yaml"
    b = tmp_path / "b.yaml"
    serialize._OVERWRITE_APPROVED = None
    serialize.write_yaml(a, {"v": 1})
    serialize.write_yaml(b, {"v": 1})

    prompts = {"count": 0}

    def fake_input(_prompt: str) -> str:
        prompts["count"] += 1
        return "Yes"

    monkeypatch.setattr("builtins.input", fake_input)

    serialize.write_yaml(a, {"v": 2})
    serialize.write_yaml(b, {"v": 3})

    assert prompts["count"] == 1
    assert _read_yaml(a)["v"] == 2
    assert _read_yaml(b)["v"] == 3
