# ROOT CAUSE AND POLICY

## Conclusion

今回の問題は、WHO LBM 3rd の Table 5-7 固有の問題ではない。

本質は、PDF由来テキストに含まれる表・フォーム・チェック欄・固定幅レイアウト崩れを、text2ir が通常の selectable `item` / `subitem` と十分に区別できていないことである。

したがって、文書個別の profile 修正を主対応にしてはいけない。WHO LBM 3rd と PIC/S Annex 2A は、共通対策の代表症例・回帰対象として扱う。

## Root Cause

### Input Layer

PDF抽出テキストには、以下のような通常本文ではない断片が残る。

- 私用領域文字
- ドットリーダー
- チェック欄
- `YES` / `NO` / `N/A` / `COMMENTS` 等の帳票列
- 固定幅空白による列表現
- 表キャプションと表行の混在

これらは入力に存在し得る。入力にあること自体を異常とは見なさない。

### Parser Layer

text2ir は、箇条書き・インデント・連続行を手掛かりに階層を作る。そのため、PDF抽出後に箇条書き風に見える表行やフォーム行が、通常の `item` / `subitem` として取り込まれる。

問題は、入力文字の存在ではなく、それを selectable candidate として出してしまうことである。

### Gate Layer

既存の strict / qualitycheck は、主にIR構造・出力ファイル・schema整合性を確認する。selectable candidate が人間に提示してよい本文品質を満たすか、特にPDF抽出由来の帳票汚染が混入していないかは十分に止められていない。

## Policy

対応方針は次の順序に固定する。

1. text2ir共通側で候補汚染を検出する。
2. 汚染が強い行・ブロックを通常 `item` / `subitem` にしない。
3. promotion gate で selectable candidate 内の汚染を止める。
4. WHO LBM 3rd / PIC/S Annex 2A を回帰fixtureとして使う。
5. profile修正は、共通対策で説明できない文書固有の境界問題に限定する。

## Anti-Pattern

以下は避ける。

- WHO LBM 3rd の Table 5-7 だけを profile で塞いで完了扱いにする。
- PIC/S Annex 2A の該当箇所だけを個別除外して完了扱いにする。
- strict 成功を selectable candidate 品質の合格と見なす。
- 入力に私用領域文字があることだけを原因として、parser/profile/gate側の責任を見ない。

## Required Common Checks

少なくとも以下は共通検出対象にする。

- U+E000-U+F8FF の私用領域文字
- 長いドットリーダー
- 大文字の `YES` / `NO` / `N/A` / `COMMENTS`
- 固定幅列を示す長い空白
- 表キャプションと表行の混在
- bullet行に帳票・チェック欄・表列が混ざるパターン

## Acceptance Direction

正式昇格候補では、selectable candidate 内に上記汚染が残っている場合、少なくとも high severity warning とし、原則として promotion fail に寄せる。

修正後は、同じ監査を再実行し、WHO LBM 3rd と PIC/S Annex 2A の severe finding が消えていることを確認する。
