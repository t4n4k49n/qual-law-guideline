import sys
import types


streamlit_stub = types.ModuleType("streamlit")
streamlit_components_stub = types.ModuleType("streamlit.components")
streamlit_components_v1_stub = types.ModuleType("streamlit.components.v1")
streamlit_stub.components = streamlit_components_stub
streamlit_components_stub.v1 = streamlit_components_v1_stub
sys.modules.setdefault("streamlit", streamlit_stub)
sys.modules.setdefault("streamlit.components", streamlit_components_stub)
sys.modules.setdefault("streamlit.components.v1", streamlit_components_v1_stub)

from apps.mock_gmp_checklist_ui import _extract_source_urls, _meta_source_urls, _source_url_display


def test_extract_source_urls_from_doc_sources_deduplicates_in_order() -> None:
    meta = {
        "doc": {
            "sources": [
                {"url": " https://example.test/source-a "},
                {"url": "https://example.test/source-a"},
                {"url": "https://example.test/source-b"},
                {"url": ""},
                {"label": "missing url"},
            ]
        }
    }

    assert _extract_source_urls(meta) == [
        "https://example.test/source-a",
        "https://example.test/source-b",
    ]


def test_meta_source_urls_reads_yaml_file(tmp_path) -> None:
    meta_path = tmp_path / "sample.meta.yaml"
    meta_path.write_text(
        "\n".join(
            [
                "doc:",
                "  sources:",
                "  - url: https://example.test/law",
                "  - url: https://example.test/pdf",
            ]
        ),
        encoding="utf-8",
    )

    assert _meta_source_urls(meta_path) == [
        "https://example.test/law",
        "https://example.test/pdf",
    ]


def test_meta_source_urls_falls_back_to_url_lines_for_broken_yaml(tmp_path) -> None:
    meta_path = tmp_path / "broken.meta.yaml"
    meta_path.write_text(
        "\n".join(
            [
                "doc:",
                "  sources:",
                "  - url: https://example.test/source",
                "generation:",
                "  path: 100%broken",
            ]
        ),
        encoding="utf-8",
    )

    assert _meta_source_urls(meta_path) == ["https://example.test/source"]


def test_source_url_display_truncates_long_url() -> None:
    url = "https://example.test/" + ("a" * 90) + "/source.pdf"

    assert _source_url_display(url) == f"{url[:72]}...{url[-21:]}"
    assert len(_source_url_display(url)) < len(url)
