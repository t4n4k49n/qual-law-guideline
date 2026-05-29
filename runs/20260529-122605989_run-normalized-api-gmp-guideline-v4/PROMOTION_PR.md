# 原薬GMPガイドライン 正式版昇格

## まとめ

承認済みの原薬GMPガイドライン正規化候補を正式版ディレクトリへ反映します。これにより `data/normalized/` から、表1のSTEPヘッダ修正まで反映済みの原薬GMPガイドラインを参照できるようになります。

## 変更内容

- `runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/promotion_candidate/` から以下4ファイルを複写。
- 複写先: `data/normalized/jp_pmda_api_gmp_guideline_20011102/`
- `runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/RUN.md` に昇格準備記録を追記。

## 昇格ファイル

- `jp_pmda_api_gmp_guideline_20011102.regdoc_ir.yaml`
- `jp_pmda_api_gmp_guideline_20011102.parser_profile.yaml`
- `jp_pmda_api_gmp_guideline_20011102.regdoc_profile.yaml`
- `jp_pmda_api_gmp_guideline_20011102.meta.yaml`

## 確認

- 親PR: `#218`
- 親PR merge commit: `4ca0420`
- `promotion_candidate/` と `data/normalized/` のSHA-256一致を確認済み。
- `data/normalized/jp_pmda_api_gmp_guideline_20011102/` のpromotion goal check: pass。
- `data/normalized/jp_pmda_api_gmp_guideline_20011102/` のIR構造チェック: pass。
- `data/normalized/` 側でも表1ヘッダが `形態ごとの生産工程の事例 STEP 1..5` であることを確認済み。
- このPRではパーサ修正や再生成を含めていません。

<!-- PR_BODY_FILE: runs/20260529-122605989_run-normalized-api-gmp-guideline-v4/PROMOTION_PR.md -->
