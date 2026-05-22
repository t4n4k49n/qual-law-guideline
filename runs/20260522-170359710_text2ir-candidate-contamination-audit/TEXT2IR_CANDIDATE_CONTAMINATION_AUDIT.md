# TEXT2IR CANDIDATE CONTAMINATION AUDIT

## Purpose

PDF由来の表・チェック欄・抽出記号が、DQチェックシート候補として選択可能な通常ノードへ混入していないかを横断確認した。

## Scope

- Latest representative 9 bundles under `out/20260522-130045_text2ir-final-goal-closure/<doc_id>/`
- Review UI copies under `out/*review_ui/`
- Promotion candidates under `runs/20260522-130045_text2ir-final-goal-closure/promotion_candidate/`
- Phase smoke outputs are excluded.

## Detection Rules

- `private_use_char`: U+E000-U+F8FF。例: ``。PDF抽出時のチェックボックス等の可能性。
- `dot_leader`: `........` 以上のドットリーダー。
- `checklist_columns`: 大文字の `YES` / `NO` / `N/A` / `CHECKED ITEM` / `COMMENTS`。通常英文の `no` は除外。
- `table_caption`: `Table n` 等。
- `long_fixed_width`: 長い空白で列を表現している行。他flagと併発する場合だけfinding化。
- `bullet_table_row`: bullet行にドットリーダー・チェック欄が混ざるもの。

## Summary

- Documents scanned: 19
- Findings total including copied duplicates: 72
- Unique finding keys: 36
- Severe findings (score >= 5): 18

## Document Summary

| source | doc_id | selectable nodes | findings | severe | main flags |
|---|---|---:|---:|---:|---|
| latest_run_out | `eu_gmp_vol4_chap1_20130131` | 69 | 0 | 0 | none |
| latest_run_out | `pics_pe00917_annex1_20230825` | 540 | 9 | 0 | long_fixed_width=7, table_caption=9 |
| latest_run_out | `pics_pe00917_annex11_20230825` | 23 | 0 | 0 | none |
| latest_run_out | `pics_pe00917_annex15_20230825` | 128 | 0 | 0 | none |
| latest_run_out | `pics_pe00917_annex2a_20230825` | 187 | 6 | 3 | long_fixed_width=4, private_use_char=3, table_caption=3 |
| latest_run_out | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | 1167 | 16 | 3 | long_fixed_width=12, private_use_char=3, table_caption=13 |
| latest_run_out | `pics_pe00917_part1_20230825` | 331 | 0 | 0 | none |
| latest_run_out | `pics_pe00917_part2_20230825` | 482 | 0 | 0 | none |
| latest_run_out | `who_lbm_3rd_2004_9241546506` | 791 | 5 | 3 | checklist_columns=1, dot_leader=3, form_mark=1, long_fixed_width=4, private_use_char=3, table_caption=3 |
| review_ui | `eu_gmp_vol4_chap1_20130131` | 69 | 0 | 0 | none |
| review_ui | `pics_pe00917_annex11_20230825` | 23 | 0 | 0 | none |
| review_ui | `pics_pe00917_annex15_20230825` | 128 | 0 | 0 | none |
| review_ui | `pics_pe00917_annex1_20230825` | 540 | 9 | 0 | long_fixed_width=7, table_caption=9 |
| review_ui | `pics_pe00917_annex2a_20230825` | 187 | 6 | 3 | long_fixed_width=4, private_use_char=3, table_caption=3 |
| review_ui | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | 1167 | 16 | 3 | long_fixed_width=12, private_use_char=3, table_caption=13 |
| review_ui | `pics_pe00917_part1_20230825` | 331 | 0 | 0 | none |
| review_ui | `pics_pe00917_part2_20230825` | 482 | 0 | 0 | none |
| review_ui | `who_lbm_3rd_2004_9241546506` | 791 | 5 | 3 | checklist_columns=1, dot_leader=3, form_mark=1, long_fixed_width=4, private_use_char=3, table_caption=3 |
| promotion_candidate | `eu_gmp_vol4_chap1_20130131` | 69 | 0 | 0 | none |

## Severe / Representative Findings

| source | doc_id | nid | kind | score | flags | source lines | preview |
|---|---|---|---|---:|---|---|---|
| latest_run_out | `who_lbm_3rd_2004_9241546506` | `cha8.i5` | item | 14 | private_use_char, dot_leader, checklist_columns, form_mark, table_caption, long_fixed_width | 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1769, 1770, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1785, 1786, 1787, 1796, 1798, 1803, 1808, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1862, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1920, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1967, 1978, 1979, 1980, 1982, 1987, 1992, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2044, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2085, 2086, 2087, 2088, 2091, 2102, 2103, 2104, 2106, 2111, 2116, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138, 2139, 2140, 2141, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2154, 2155, 2158, 2159 | Proper procedures for general laboratory safety, including physical, electrical and chemical safety are in place. Laboratory certification differs from laboratory commissioning activities (Chapter 7) in several important... |
| review_ui | `who_lbm_3rd_2004_9241546506` | `cha8.i5` | item | 14 | private_use_char, dot_leader, checklist_columns, form_mark, table_caption, long_fixed_width | 1742, 1743, 1744, 1745, 1746, 1747, 1748, 1749, 1750, 1751, 1752, 1753, 1754, 1755, 1756, 1757, 1758, 1759, 1760, 1769, 1770, 1771, 1772, 1773, 1774, 1775, 1776, 1777, 1778, 1779, 1780, 1785, 1786, 1787, 1796, 1798, 1803, 1808, 1810, 1811, 1812, 1813, 1814, 1815, 1816, 1817, 1818, 1819, 1820, 1821, 1822, 1823, 1824, 1825, 1826, 1827, 1828, 1829, 1830, 1831, 1832, 1833, 1834, 1835, 1836, 1837, 1838, 1839, 1840, 1841, 1842, 1843, 1844, 1845, 1846, 1847, 1848, 1849, 1850, 1862, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1920, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1967, 1978, 1979, 1980, 1982, 1987, 1992, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2044, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062, 2063, 2064, 2065, 2066, 2067, 2068, 2069, 2070, 2071, 2072, 2073, 2074, 2075, 2076, 2077, 2078, 2079, 2080, 2081, 2082, 2083, 2084, 2085, 2086, 2087, 2088, 2091, 2102, 2103, 2104, 2106, 2111, 2116, 2118, 2119, 2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127, 2128, 2129, 2130, 2131, 2132, 2133, 2134, 2135, 2136, 2137, 2138, 2139, 2140, 2141, 2142, 2143, 2144, 2145, 2146, 2147, 2148, 2149, 2150, 2151, 2152, 2153, 2154, 2155, 2158, 2159 | Proper procedures for general laboratory safety, including physical, electrical and chemical safety are in place. Laboratory certification differs from laboratory commissioning activities (Chapter 7) in several important... |
| latest_run_out | `who_lbm_3rd_2004_9241546506` | `cha8.i5.si1` | subitem | 8 | private_use_char, dot_leader, long_fixed_width | 2013, 2014 | Information on sign accurate and current ..............................................    |
| review_ui | `who_lbm_3rd_2004_9241546506` | `cha8.i5.si1` | subitem | 8 | private_use_char, dot_leader, long_fixed_width | 2013, 2014 | Information on sign accurate and current ..............................................    |
| latest_run_out | `who_lbm_3rd_2004_9241546506` | `cha8.i5.si2` | subitem | 8 | private_use_char, dot_leader, long_fixed_width | 2015 | Sign legible and not defaced .............    |
| review_ui | `who_lbm_3rd_2004_9241546506` | `cha8.i5.si2` | subitem | 8 | private_use_char, dot_leader, long_fixed_width | 2015 | Sign legible and not defaced .............    |
| latest_run_out | `pics_pe00917_annex2a_20230825` | `ann2a.sec2.ib.si1` | subitem | 6 | private_use_char, long_fixed_width | 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231 | GMP requirements  A Marketing  GMP requirements  A MAH may justify can vary from early Authorisation Holder can vary from early these steps to be a steps in making the (MAH) may justify steps in making the continuous ... |
| review_ui | `pics_pe00917_annex2a_20230825` | `ann2a.sec2.ib.si1` | subitem | 6 | private_use_char, long_fixed_width | 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231 | GMP requirements  A Marketing  GMP requirements  A MAH may justify can vary from early Authorisation Holder can vary from early these steps to be a steps in making the (MAH) may justify steps in making the continuous ... |
| latest_run_out | `pics_pe00917_annex2a_20230825` | `ann2a.sec2.ib.si2` | subitem | 6 | private_use_char, long_fixed_width | 232, 233, 234, 235, 236, 237, 243, 247, 250, 251, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269 | Refer to Section 5.23 apply as appropriate  Refer to Section 5.23 manufacture. for additional to the step of for additional information in manufacture. information in determining the determining the appropriate appropri... |
| review_ui | `pics_pe00917_annex2a_20230825` | `ann2a.sec2.ib.si2` | subitem | 6 | private_use_char, long_fixed_width | 232, 233, 234, 235, 236, 237, 243, 247, 250, 251, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269 | Refer to Section 5.23 apply as appropriate  Refer to Section 5.23 manufacture. for additional to the step of for additional information in manufacture. information in determining the determining the appropriate appropri... |
| latest_run_out | `pics_pe00917_annex2a_20230825` | `ann2a.sec2.ib.si3` | subitem | 6 | private_use_char, long_fixed_width | 272, 273, 274, 275, 276, 277, 278, 279, 280, 281 | GMP requirements can  GMP requirements applied  The application of this vary from early steps in to the manufacture of a guide does not include the making the plasmid DNA viral vector should align donation or procureme... |
| review_ui | `pics_pe00917_annex2a_20230825` | `ann2a.sec2.ib.si3` | subitem | 6 | private_use_char, long_fixed_width | 272, 273, 274, 275, 276, 277, 278, 279, 280, 281 | GMP requirements can  GMP requirements applied  The application of this vary from early steps in to the manufacture of a guide does not include the making the plasmid DNA viral vector should align donation or procureme... |
| latest_run_out | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | `ann2a.sec2.ib.si1` | subitem | 6 | private_use_char, long_fixed_width | 4568, 4569, 4570, 4571, 4572, 4573, 4574, 4575, 4576, 4577, 4578, 4579 | GMP requirements  A Marketing  GMP requirements  A MAH may justify can vary from early Authorisation Holder can vary from early these steps to be a steps in making the (MAH) may justify steps in making the continuous ... |
| review_ui | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | `ann2a.sec2.ib.si1` | subitem | 6 | private_use_char, long_fixed_width | 4568, 4569, 4570, 4571, 4572, 4573, 4574, 4575, 4576, 4577, 4578, 4579 | GMP requirements  A Marketing  GMP requirements  A MAH may justify can vary from early Authorisation Holder can vary from early these steps to be a steps in making the (MAH) may justify steps in making the continuous ... |
| latest_run_out | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | `ann2a.sec2.ib.si2` | subitem | 6 | private_use_char, long_fixed_width | 4580, 4581, 4582, 4583, 4584, 4585, 4591, 4595, 4598, 4599, 4601, 4602, 4603, 4604, 4605, 4606, 4607, 4608, 4609, 4610, 4611, 4612, 4613, 4614, 4615, 4616, 4617 | Refer to Section 5.23 apply as appropriate  Refer to Section 5.23 manufacture. for additional to the step of for additional information in manufacture. information in determining the determining the appropriate appropri... |
| review_ui | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | `ann2a.sec2.ib.si2` | subitem | 6 | private_use_char, long_fixed_width | 4580, 4581, 4582, 4583, 4584, 4585, 4591, 4595, 4598, 4599, 4601, 4602, 4603, 4604, 4605, 4606, 4607, 4608, 4609, 4610, 4611, 4612, 4613, 4614, 4615, 4616, 4617 | Refer to Section 5.23 apply as appropriate  Refer to Section 5.23 manufacture. for additional to the step of for additional information in manufacture. information in determining the determining the appropriate appropri... |
| latest_run_out | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | `ann2a.sec2.ib.si3` | subitem | 6 | private_use_char, long_fixed_width | 4620, 4621, 4622, 4623, 4624, 4625, 4626, 4627, 4628, 4629 | GMP requirements can  GMP requirements applied  The application of this vary from early steps in to the manufacture of a guide does not include the making the plasmid DNA viral vector should align donation or procureme... |
| review_ui | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | `ann2a.sec2.ib.si3` | subitem | 6 | private_use_char, long_fixed_width | 4620, 4621, 4622, 4623, 4624, 4625, 4626, 4627, 4628, 4629 | GMP requirements can  GMP requirements applied  The application of this vary from early steps in to the manufacture of a guide does not include the making the plasmid DNA viral vector should align donation or procureme... |

## Known User-Reported Case

WHO LBM 3rd の `cha8.i5`, `cha8.i5.si1`, `cha8.i5.si2` 付近で、ドットリーダーと `` が通常候補として見える問題を確認した。

入力元 `data/human-readable/who/WHO_LBM_3rd.txt` にも以下のように存在するため、文字自体はオリジナル抽出テキスト由来。ただし、それを通常 `item/subitem` 候補として表示している点は parser/profile 側の混入問題。

```text
1966:     • Information on sign accurate and
1967:        current ..............................................                                                                                  
1968:     • Sign legible and not defaced .............                                                                                               
```

## Initial Interpretation

- EU GMP Chapter 1 / PIC/S Annex 11 / PIC/S Annex 15 は、この検出では重大な候補混入が見つからない。
- WHO LBM 3rd は重大。Table 5-7 周辺のチェックリスト表が通常候補へ混入している。
- PIC/S Annex 2Aにも私用領域文字 `` を含む表状テキストが選択可能subitemへ混入している。Annexes refinedにも同じ問題が含まれる。
- PIC/S Annex 1 / Annexes refined は表本文がparagraphに吸収されている箇所があり、WHOほどではないが確認対象。
- 本問題は「入力文字の有無」ではなく、「選択可能候補として出すべきでない固定幅表/フォーム行を候補へ混ぜるか」の問題として扱うべき。

## Recommended Next Actions

1. WHO LBM profileで Table 5-7 のsurvey form範囲を `preformatted kind_raw=possible_table` に隔離する。
2. PIC/S Annex 2A の表状三列比較部分を通常subitemではなく `preformatted possible_table` へ隔離する。
3. text2ir共通側で、私用領域文字・長いドットリーダー・YES/NO/N/A列を含むbullet行を通常 `item/subitem` にしないガードを検討する。
4. `goal_check --mode promotion` に「選択可能ノード内のPDF抽出記号/チェック欄混入」をwarning/error化する追加検査を検討する。
5. WHO LBM 3rd / PIC/S Annex 2A は修正後に再生成・再監査する。
