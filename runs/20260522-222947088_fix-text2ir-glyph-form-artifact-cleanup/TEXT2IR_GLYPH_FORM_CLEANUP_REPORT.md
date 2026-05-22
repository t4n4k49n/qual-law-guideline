# TEXT2IR GLYPH / FORM CLEANUP REPORT

## Conclusion

今回の問題は、WHO個別patchではなく、text2ir共通のPDF抽出artifact問題として対処した。

結果として、代表9文書の `.regdoc_ir.yaml` には literal Private Use Area glyph は残らず、WHO LBM 3rd の `cha8.i5.si1` / `cha8.i5.si2` のようなフォーム行は通常の本文候補ではなく、sanitize済みの `form_artifact` として明示的に隔離される。

## What changed

1. glyph sanitizer
   - PUA bulletをmarker判定前に通常bullet相当に正規化。
   - checkbox系PUAはフォーム文脈で `[ ]` へ正規化。
   - 不明なPUAは literal ではなく `<PUA-U+XXXX>` へescape。

2. artifact classifier
   - `CHECKED ITEM`, `YES NO N/A`, dot leader + PUA checkbox, safety survey系フォームを検出。
   - 通常の固定幅表や本文中の単語 `no` をフォーム扱いしないよう判定を制限。

3. parser integration
   - 本文とフォームが同一ノードへ混ざった場合、本文を親ノードに残し、フォーム部を子の `form_artifact` へ分離。
   - フォーム行単体は `preformatted` / `kind_raw: form_artifact` / `not_selectable` / `sanitized_layout_artifact` に変換。

4. promotion gate
   - literal PUA、replacement char、可読本文のsevere form artifact、contamination guard残存、artifact kind selectableを検出したらpromotion/releaseでFAIL。

## Remaining risk

- `form_artifact` への隔離は「表として安全に構造化できない場合の暫定正規化」であり、将来の表構造化改善余地は残る。
- WHO LBMは固定幅表と本文の混在が大きく、今後の正式昇格前には人手レビューで過剰隔離がないか確認する必要がある。
- PIC/S Annex 1 の既存 single newline qualitycheck warning は本件外として残る。

## Self review checklist

- [x] WHO文書IDのベタ書きで対処していない。
- [x] 該当2行だけをdropしていない。
- [x] `cha8.i5` の説明文を削除していない。
- [x] literal PUAを代表9文書から除去した。
- [x] `preformatted` / `form_artifact` を selectable に入れていない。
- [x] promotion gateで再発を検出できる。
- [x] 代表9文書を再生成して確認した。

