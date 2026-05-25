from __future__ import annotations

from qai_text2ir.table_record_review_6_7 import build_table_record_review_inventory


def test_table_record_review_inventory_tracks_6_7_candidate_granularity() -> None:
    items = build_table_record_review_inventory()
    by_nid = {item.table_nid: item for item in items}

    assert list(by_nid) == ["cha1.p1_3.tbl1", "cha7.p7_1.tbl1", "cha11.p11_3.tbl2", "cha11.p11_3.tbl3"]
    assert by_nid["cha1.p1_3.tbl1"].records == 7
    assert by_nid["cha1.p1_3.tbl1"].candidate_granularity == "reconstructed_record"
    assert by_nid["cha1.p1_3.tbl1"].table_row_promotion == "deferred"
    assert by_nid["cha1.p1_3.tbl1"].deferred_raw_rows == [1, 2, 26]
    assert by_nid["cha7.p7_1.tbl1"].records == 4
    assert by_nid["cha11.p11_3.tbl2"].deferred_raw_rows == [1, 2, 3]
    assert by_nid["cha11.p11_3.tbl3"].review_status == "reviewed_candidate"
