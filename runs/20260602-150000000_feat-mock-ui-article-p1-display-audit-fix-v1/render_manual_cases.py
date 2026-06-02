from pathlib import Path

import yaml

from qai_mock_ui.ir_model import build_doc_index
from qai_mock_ui.render import render_selected_nodes, render_text_preview


BASE = Path("data/normalized/jp_egov_336M50000100002_20260501_507M60000100117")
IR = BASE / "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml"
PROFILE = BASE / "jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml"


def main() -> None:
    regdoc_ir = yaml.safe_load(IR.read_text(encoding="utf-8"))
    regdoc_profile = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))
    index = build_doc_index(regdoc_ir)
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]

    cases = [
        ("ON p1", "prefix", True, ["art1.p1"]),
        ("ON subitem ro", "prefix", True, ["art1.p1.i10.ro"]),
        ("ON siblings exact", "exact", True, ["art1.p1.i10.ro", "art1.p1.i10.ha"]),
        ("ON parent-child exact", "exact", True, ["art1.p1", "art1.p1.i2"]),
        ("ON p1-p2-p3 prefix", "prefix", True, ["art1.p1", "art1.p2", "art1.p3"]),
    ]
    for name, mode, merge, nids in cases:
        print(f"=== {name} ===")
        print(f"mode={mode} merge={merge} nids={','.join(nids)}")
        blocks = render_selected_nodes(
            index,
            purpose,
            nids,
            header_dedup_mode=mode,
            render_options={"egov_merge_article_p1": merge},
        )
        print(render_text_preview(blocks))
        print()


if __name__ == "__main__":
    main()
