from __future__ import annotations

from qai_xml2ir.nid_migration import build_existing_nids, migrate_nids


def test_migrate_nids_success_cases() -> None:
    existing_nids = {
        "art2.p1.i1",
        "art2.p1.i2.ro",
        "annex9.art1.p1.ro",
        "mp.p1",
    }
    old = ["art2.i1", "art2.i2.ro", "annex9.art1.ro", "mp.p1"]

    result = migrate_nids(old, existing_nids, dedup=True)
    assert result.resolved_nids == ["art2.p1.i1", "art2.p1.i2.ro", "annex9.art1.p1.ro", "mp.p1"]
    assert result.changed_count == 3
    assert result.unresolved_count == 0
    assert result.invalid_after_migration == []


def test_migrate_nids_unresolved_left() -> None:
    existing_nids = {"art2.p1.i1"}
    old = ["art2.i1", "art999.i1"]

    result = migrate_nids(old, existing_nids, dedup=True)
    assert "art999.i1" in result.unresolved
    assert result.unresolved_count == 1
    assert result.resolved_nids == ["art2.p1.i1"]


def test_migrate_nids_no_double_insertion() -> None:
    existing_nids = {"art2.p1.i1"}
    old = ["art2.p1.i1"]

    result = migrate_nids(old, existing_nids, dedup=True)
    assert result.unchanged_count == 1
    assert result.changed_count == 0
    assert result.resolved_nids == ["art2.p1.i1"]
    assert all("p1.p1" not in (row.new or "") for row in result.mappings)


def test_build_existing_nids_from_min_ir_dict() -> None:
    ir_data = {
        "content": {
            "nid": "root",
            "kind": "document",
            "children": [
                {
                    "nid": "art2",
                    "kind": "article",
                    "children": [
                        {
                            "nid": "art2.p1",
                            "kind": "paragraph",
                            "children": [{"nid": "art2.p1.i1", "kind": "item", "children": []}],
                        }
                    ],
                }
            ],
        }
    }
    existing, kind_by_nid = build_existing_nids(ir_data)
    assert "art2" in existing
    assert "art2.p1" in existing
    assert "art2.p1.i1" in existing
    assert kind_by_nid["art2.p1.i1"] == "item"
