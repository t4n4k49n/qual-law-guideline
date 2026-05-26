from __future__ import annotations

from typing import Any, Dict


VISUAL_REVIEW_PARSER = "niid_visual_reviewed_table_v1"

VISUAL_REVIEWED_TABLES: Dict[str, Dict[str, Any]] = {
    "付表2": {
        "columns": ["risk_group", "laboratory_bsl", "laboratory_purpose", "laboratory_practice_operation", "safety_equipment"],
        "records": [
            {
                "risk_group": "1",
                "laboratory_bsl": "基本実験室－BSL1",
                "laboratory_purpose": "教育、研究",
                "laboratory_practice_operation": "GMT",
                "safety_equipment": "特になし（開放型実験台）",
            },
            {
                "risk_group": "2",
                "laboratory_bsl": "基本実験室－BSL2",
                "laboratory_purpose": "一般診断検査、研究",
                "laboratory_practice_operation": "GMT、PPE、バイオハザード標識表示",
                "safety_equipment": "病原体の取扱いはBSCで行う",
            },
            {
                "risk_group": "3",
                "laboratory_bsl": "封じ込め実験室－BSL3",
                "laboratory_purpose": "特殊診断検査、研究",
                "laboratory_practice_operation": "上記BSL2の各項目、専用PPE、立入りの厳重制限、一方向性の気流",
                "safety_equipment": "病原体の取扱いの全操作をBSCあるいは、その他の一次封じ込め装置を用いて行う",
            },
            {
                "risk_group": "4",
                "laboratory_bsl": "高度封じ込め実験室－BSL4",
                "laboratory_purpose": "高度特殊診断検査",
                "laboratory_practice_operation": "上記BSL3の各項目、エアロックを通っての入室、退出時シャワー、専用廃棄物処理",
                "safety_equipment": "クラスIII BSCまたは、陽圧スーツとクラスII BSCに加え、両面オートクレーブ、給排気はフィルターろ過",
            },
        ],
        "notes": [
            {"mark": "BSC", "text": "生物学用安全キャビネット"},
            {"mark": "GMT", "text": "標準微生物学実験手技"},
            {"mark": "PPE", "text": "個人用曝露防止器具"},
        ],
    },
    "付表3": {
        "columns": ["criterion", "parent_criterion", "bsl1", "bsl2", "bsl3", "bsl4"],
        "records": [
            {"criterion": "実験室の独立性*1", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "汚染除去時の実験室気密性", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "内側への気流", "parent_criterion": "換気", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "制御換気系", "parent_criterion": "換気", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "排気のHEPAろ過", "parent_criterion": "換気", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "入口部二重ドア(インターロック*2)", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "エアロック*3", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "不要", "bsl4": "必要"},
            {"criterion": "エアロック＋シャワー", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "不要", "bsl4": "必要"},
            {"criterion": "前室*4", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要*5"},
            {"criterion": "排水処理*6", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "管理区域内", "parent_criterion": "オートクレーブ", "bsl1": "不要", "bsl2": "必要", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "実験室内", "parent_criterion": "オートクレーブ", "bsl1": "不要", "bsl2": "望ましい", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "両面オートクレーブ", "parent_criterion": "オートクレーブ", "bsl1": "不要", "bsl2": "不要", "bsl3": "望ましい", "bsl4": "必要"},
            {"criterion": "生物学用安全キャビネット", "parent_criterion": "", "bsl1": "不要", "bsl2": "必要*7", "bsl3": "必要", "bsl4": "必要"},
            {"criterion": "作業従事者の安全監視機能*8", "parent_criterion": "", "bsl1": "不要", "bsl2": "不要", "bsl3": "必要", "bsl4": "必要"},
        ],
        "notes": [
            {"mark": "*1", "text": "施設内の通常の人の流れからの実質的、機能的隔離。"},
            {"mark": "*2", "text": "二重ドアで構成される部屋は前室に相当する。なお、インターロックドアとは同時に２枚の扉が開放されないような機構を有するドアのことをいう。"},
            {"mark": "*3", "text": "エアロックとは気圧を保つために設ける機構のこと。通常は複数の扉を設け、インターロックドアとなっている。"},
            {"mark": "*4", "text": "実験室につながる隣室。"},
            {"mark": "*5", "text": "BSL4実験室の前室は、入口部二重ドア、エアロック、エアロック＋シャワーが相当する。"},
            {"mark": "*6", "text": "一般排水処理とは異なる消毒滅菌処理のことをいう。"},
            {"mark": "*7", "text": "エアロゾル発生のおそれがある場合は、生物学用安全キャビネットが必要。"},
            {"mark": "*8", "text": "たとえば、観察用窓、監視カメラ、インターフォン、双方向性モニター設備など。"},
        ],
    },
    "付表4": {
        "columns": ["absl", "laboratory_practice", "safety_equipment", "facility_criteria"],
        "records": [
            {
                "absl": "1",
                "laboratory_practice": "通常の動物実験の条件として、標準動物実験手技、標準微生物実験手技、立入り制限、専用服を要する。",
                "safety_equipment": "特になし。",
                "facility_criteria": "通常の動物実験施設の条件として、動物実験施設の独立性、立入り者の管理・記録、動物逸走防止対策、昆虫・野鼠等の侵入防止、室内、飼育装置など洗浄・消毒可能な仕様を要する。",
            },
            {
                "absl": "2",
                "laboratory_practice": "ABSL1の要件に加え、防護服、国際バイオハザード標識表示、糞尿・ケージ等の滅菌処理、移動用密閉容器を要する。",
                "safety_equipment": "エアロゾル発生の恐れがある場合は陰圧飼育装置及びBSC、動物実験施設内にオートクレーブ。",
                "facility_criteria": "ABSL1の要件に加え、立入り者の制限、動物安全管理区域からの動物逸走防止対策を要する。",
            },
            {
                "absl": "3",
                "laboratory_practice": "ABSL2の要件に加え、専用防護服及び履物、二重以上の気密容器による移動を要する。",
                "safety_equipment": "全操作BSC使用。飼育は動物飼育用BSC、グローブボックス、またはアイソレーションラックを使用、動物安全管理区域内にオートクレーブ。",
                "facility_criteria": "ABSL2の要件に加え、立入り者の厳重制限、出入口インターロック、前室の設置、気流の一方向性、排気のHEPAろ過、作業者の安全監視機能を要する。",
            },
            {
                "absl": "4",
                "laboratory_practice": "ABSL3の要件、及びその他はBSL4に準じる。",
                "safety_equipment": "ABSL3の要件、及びその他はBSL4に準じる。",
                "facility_criteria": "ABSL3の要件、及びその他はBSL4に準じる。",
            },
        ],
        "notes": [{"mark": "BSC", "text": "生物学用安全キャビネット"}],
    },
    "別表7": {
        "columns": ["category", "ordinance_item", "record_content", "pathogen_type_1", "pathogen_type_2", "pathogen_type_3"],
        "records": [
            {"category": "病原体等", "ordinance_item": "受入れ又は払出しに係る病原体等の種類（毒素にあっては、その種類及び量）", "record_content": "事業所ごとに受入れ元、払出し先等を記帳（実験室が複数ある場合にはそれら実験室ごとに記帳）", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "病原体等", "ordinance_item": "病原体等の受入れ又は払出しの日時", "record_content": "事業所ごとに記帳（同上）", "pathogen_type_1": "年月日・時刻", "pathogen_type_2": "年月日", "pathogen_type_3": "年月日"},
            {"category": "病原体等", "ordinance_item": "病原体等の保管の方法及び場所", "record_content": "受入れした病原体等の保管形態及び保管場所を記帳（同上）、使用ごとの保管庫の施錠状況も記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "病原体等", "ordinance_item": "使用に係る病原体等の種類", "record_content": "実験室での使用ごとに、その使用者が記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "病原体等", "ordinance_item": "病原体等の使用に係る日時", "record_content": "病原体等を使用した時刻を記帳", "pathogen_type_1": "年月日・時刻", "pathogen_type_2": "－", "pathogen_type_3": "－"},
            {"category": "病原体等", "ordinance_item": "滅菌等に係る病原体等の種類", "record_content": "実験室ごとに滅菌・無害化した病原体等を記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "病原体等", "ordinance_item": "病原体等の滅菌等の日時", "record_content": "滅菌・無害化の日時を記帳", "pathogen_type_1": "年月日・時刻", "pathogen_type_2": "年月日", "pathogen_type_3": "年月日"},
            {"category": "病原体等", "ordinance_item": "病原体等の滅菌等の方法及び場所", "record_content": "滅菌・無害化の条件等を記帳（委託等の場合にはその場所も記帳）", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "ヒト", "ordinance_item": "実験室に立入り又は退出に係る者の氏名", "record_content": "実験室ごとに記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "ヒト", "ordinance_item": "実験室への立入り又は退出の日時", "record_content": "実験室ごとに記帳", "pathogen_type_1": "年月日・時刻", "pathogen_type_2": "年月日", "pathogen_type_3": "年月日"},
            {"category": "ヒト", "ordinance_item": "実験室への立入りの目的", "record_content": "病原体等を使用の有無を含め目的を記帳", "pathogen_type_1": "有", "pathogen_type_2": "－", "pathogen_type_3": "－"},
            {"category": "ヒト", "ordinance_item": "病原体等の受入れ又は払出しする者の氏名", "record_content": "病原体等を受入れ、払出しした者の氏名を記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "ヒト", "ordinance_item": "病原体等の使用に従事する者の氏名", "record_content": "実験室で病原体等を使用した者の氏名を記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "ヒト", "ordinance_item": "病原体等の滅菌等に従事する者の氏名", "record_content": "病原体等を滅菌・無害化した者の氏名を記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "施設", "ordinance_item": "病原体等取扱施設の点検等の実施日時", "record_content": "事業所ごとに記帳", "pathogen_type_1": "年月日", "pathogen_type_2": "年月日", "pathogen_type_3": "年月日"},
            {"category": "施設", "ordinance_item": "点検を行った者の氏名", "record_content": "事業所ごとに記帳（実験室ごとに担当者が分かれる場合には、実験室ごとの者の氏名を記帳）", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "施設", "ordinance_item": "点検の内容、結果及びこれに伴う措置内容", "record_content": "措置を伴う項目については具体的に記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "有"},
            {"category": "教育", "ordinance_item": "教育訓練の実施年月日、対象者及び内容等", "record_content": "教育訓練ごとに記帳", "pathogen_type_1": "有", "pathogen_type_2": "有", "pathogen_type_3": "－"},
        ],
    },
    "別表10": {
        "columns": ["category", "ordinance_item", "specific_content", "regulation_reference"],
        "records": [
            {"category": "組織及び職務", "ordinance_item": "病原体等取扱主任者その他の病原体等の取扱い及び管理に従事する者に関する職務及び組織に関すること。", "specific_content": "病原体等安全管理委員会（仮称）の設置を含む事業所全体の組織体制、委員会の運営等。（委員会の構成・運営は別途事業所ごとに規定。）予防規程の制定・改廃等、立入り検査等への立ち会い、従事者等への教育訓練、所持者に対する意見具申など、病原体等取扱主任者の職務の規定。", "regulation_reference": "特定病原体等保持者：第3条；病原体等取扱主任者：第4条；組織体制と運営等：第7条から第14条、第23条；予防規程の制定・改廃等：第1条、第42条；その他：第40条、41条その他"},
            {"category": "管理区域", "ordinance_item": "病原体等の取扱いに従事する者であって、管理区域に立入るものの制限に関すること。", "specific_content": "管理区域、実験室等へのヒトの立入り制限。", "regulation_reference": "第15条2項"},
            {"category": "管理区域", "ordinance_item": "管理区域の設定並びに管理区域の内部において感染症の発生を予防し、及びそのまん延を防止するために講ずる措置に関すること。", "specific_content": "管理区域の設定、管理区域内の遵守事項等。", "regulation_reference": "第5条、第6条、第12条、第13条、第14条、第22条"},
            {"category": "施設の維持管理", "ordinance_item": "一種病原体等取扱施設又は二種病原体等取扱施設の維持及び管理に関すること。", "specific_content": "定期的な点検、必要な措置等。点検結果の記録（→記帳）。", "regulation_reference": "第14条（3）、（4）"},
            {"category": "病原体等の取扱い等", "ordinance_item": "病原体等の使用、保管、運搬及び滅菌譲渡に関すること。", "specific_content": "病原体等の使用、保管、滅菌等の基準の遵守事項・手続等。保管状況（施錠、鍵の管理等を含む）の確認等。事業所内の運搬の規定。", "regulation_reference": "第18条から第22条、第24条3項"},
            {"category": "病原体等の取扱い等", "ordinance_item": "病原体等の受入れ、払出し及び移動の制限に関すること。", "specific_content": "病原体等のみだりな移動の制限、受入れ・払出しの手続等。", "regulation_reference": "第20条"},
            {"category": "教育訓練", "ordinance_item": "病原体等による感染症の発生を予防し、並びにそのまん延を防止するために必要な教育及び訓練に関すること。", "specific_content": "教育訓練の対象者及びその内容等。（実施要領は別途事業所ごとに規定。）", "regulation_reference": "第27条"},
            {"category": "健康管理等", "ordinance_item": "病原体等に曝露した者又は曝露したおそれのある者に対する保健上の必要な措置に関すること。", "specific_content": "病原体等取扱者の定期的な健康診断。病原体等に曝露した場合の必要な措置等。", "regulation_reference": "第23条(2)、第28条、第33条から第39条"},
            {"category": "記帳等", "ordinance_item": "法第56条の23に規定による記帳及び保存に関すること。", "specific_content": "病原体等の管理、ヒトの立入り等に係る記帳。保存方法。", "regulation_reference": "第25条"},
            {"category": "情報管理", "ordinance_item": "病原体等の取扱いに係る情報の管理に関すること。", "specific_content": "病原体等の取扱いに係る情報へのアクセス制限等。", "regulation_reference": "第26条"},
            {"category": "事故等対応", "ordinance_item": "病原体等の盗取、所在不明その他の事故が生じたときの措置に関すること。", "specific_content": "連絡体制、警察官等への届出の手続等。", "regulation_reference": "第29条"},
            {"category": "応急措置", "ordinance_item": "災害時の応急措置に関すること。", "specific_content": "災害発生時の連絡・通報体制、汚染拡大の防止、関係者以外の立入り禁止等の応急措置等。届出の手続等。", "regulation_reference": "第30条、第31条"},
            {"category": "その他", "ordinance_item": "その他病原体等による感染症の発生の予防及びまん延の防止に関し必要な事項。", "specific_content": "その他必要な事項。", "regulation_reference": "その他"},
        ],
    },
}
