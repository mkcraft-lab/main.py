import random
import csv
from datetime import datetime

# =========================================================
# The Mycologist – Mycelium Ops Simulation (Mushroom Edition)
# - run_log.csv: raw operational logs (audit trail)
# - daily_summary.csv: daily KPI snapshots
# - kpi_report.txt: executive summary
# =========================================================

# -----------------------------
# 0) ローカライズ（最低限）
# -----------------------------
TEXT = {
    # Actions
    "ACT1": "培地設計（コスト/収支）",
    "ACT2": "衛生巡回（汚染/治安）",
    "ACT3": "菌糸ネットワーク探索（証拠/遭遇）",
    "ACT4": "業務終了（次の日へ）",
    # Players
    "P1": "しいたけ（主人公）",
    "P2": "えのき（堅実）",
    "P3": "まいたけ（無敵の鈍感力）",
    # Labels
    "MONEY": "収支",
    "MONEY_LABEL": "¥",
    "RISK_LABEL": "胞子汚染度",
    "PRESSURE_LABEL": "圧力",
    "SECURITY_LABEL": "治安",
    "MORALE_LABEL": "士気",
    # Endings
    "END_MP": "精神力(MP)が尽きました。",
    "END_HP": "体力(HP)が尽きました。",
    "CLEAR": "森は今日も守られた。",
}

def t(k: str) -> str:
    return TEXT.get(k, k)

def money_fmt(x: int) -> str:
    return f"{x:,}"


# -----------------------------
# 1) 毒きのこ（敵候補）
# -----------------------------
POISON_MUSHROOMS = [
    {"jp": "ドクツルタケ", "alias": "死の天使", "danger": 5},
    {"jp": "ベニテングダケ", "alias": "赤い幻惑", "danger": 3},
    {"jp": "カエンタケ", "alias": "炎の指", "danger": 5},
    {"jp": "ツキヨタケ", "alias": "月夜の罠", "danger": 4},
    {"jp": "スギヒラタケ", "alias": "冷たい影", "danger": 4},
    {"jp": "シロオニタケ", "alias": "白い鬼", "danger": 4},
    {"jp": "ドクササコ", "alias": "遅効の毒", "danger": 3},
    {"jp": "シャグマアミガサタケ", "alias": "偽りの森", "danger": 4},
    {"jp": "ニガクリタケ", "alias": "苦い群れ", "danger": 2},
]

# -----------------------------
# 2) 証拠（Dossier）
# -----------------------------
DOSSIER = {
    "DOC001": {"name": "古い培地コスト表（核心）", "power": 20, "unlock_day": 2},
    "DOC002": {"name": "巡回記録の欠落（抵抗）", "power": 15, "unlock_day": 4},
    "DOC003": {"name": "汚染閾値メモ（実証）", "power": 25, "unlock_day": 6},
    "DOC004": {"name": "圧力の指示書（現物）", "power": 10, "unlock_day": 1},
    "DOC005": {"name": "改善提案の草案（成功証明）", "power": 20, "unlock_day": 8},
}


# -----------------------------
# 3) Logger（監査証跡）
# -----------------------------
class GameLogger:
    def __init__(self, filepath="run_log.csv"):
        self.filepath = filepath
        self.fieldnames = [
            "timestamp", "day", "player", "facility",
            "action", "event",
            "hp", "mp", "money",
            "spore_level", "pressure", "security", "morale",
            "evidence_count"
        ]
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.fieldnames).writeheader()

    def log(self, day, player, facility, action, event=""):
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "day": int(day),
            "player": player.name,
            "facility": facility.name,
            "action": action,
            "event": event,
            "hp": int(player.HP),
            "mp": int(player.MP),
            "money": int(player.money),
            "spore_level": int(facility.spore_level),
            "pressure": int(facility.pressure),
            "security": int(facility.security),
            "morale": int(facility.morale),
            "evidence_count": int(len(player.evidence)),
        }
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.fieldnames).writerow(row)


# -----------------------------
# 4) レポート生成（CSV + TXT）
# -----------------------------
def generate_reports(log_path="run_log.csv"):
    rows = []
    with open(log_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # int化
            for k in ["day", "hp", "mp", "money", "spore_level", "pressure", "security", "morale", "evidence_count"]:
                r[k] = int(float(r[k]))
            rows.append(r)

    if not rows:
        return

    # 日次サマリ：その日の最後のスナップショット＋回数
    by_day = {}
    for r in rows:
        d = r["day"]
        by_day.setdefault(d, {
            "day": d,
            "actions": 0,
            "events": 0,
            "money_end": 0,
            "hp_end": 0,
            "mp_end": 0,
            "spore_end": 0,
            "security_end": 0,
            "pressure_end": 0,
            "morale_end": 0,
            "evidence_end": 0
        })
        by_day[d]["actions"] += 1
        if r.get("event"):
            by_day[d]["events"] += 1

        by_day[d]["money_end"] = r["money"]
        by_day[d]["hp_end"] = r["hp"]
        by_day[d]["mp_end"] = r["mp"]
        by_day[d]["spore_end"] = r["spore_level"]
        by_day[d]["security_end"] = r["security"]
        by_day[d]["pressure_end"] = r["pressure"]
        by_day[d]["morale_end"] = r["morale"]
        by_day[d]["evidence_end"] = r["evidence_count"]

    daily = [by_day[d] for d in sorted(by_day.keys())]

    # daily_summary.csv
    with open("daily_summary.csv", "w", newline="", encoding="utf-8") as f:
        fieldnames = list(daily[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(daily)

    first = daily[0]
    last = daily[-1]

    money_delta = last["money_end"] - first["money_end"]
    spore_delta = last["spore_end"] - first["spore_end"]
    sec_delta = last["security_end"] - first["security_end"]
    pres_delta = last["pressure_end"] - first["pressure_end"]
    morale_delta = last["morale_end"] - first["morale_end"]
    ev_delta = last["evidence_end"] - first["evidence_end"]

    total_actions = sum(d["actions"] for d in daily)
    total_events = sum(d["events"] for d in daily)

    # 安定性（収支の分散）
    money_vals = [d["money_end"] for d in daily]
    avg_money = sum(money_vals) / len(money_vals)
    variance = sum((x - avg_money) ** 2 for x in money_vals) / len(money_vals)

    report = []
    report.append("Portfolio Artifact: Mycelium Ops Monitoring & KPI Reporting (Simulation)\n")
    report.append("========================================================\n\n")
    report.append("Summary\n")
    report.append(f"- Period: Day {first['day']} to Day {last['day']}\n")
    report.append(f"- Total actions logged: {total_actions}\n")
    report.append(f"- Total events logged: {total_events}\n\n")

    report.append("KPI Deltas (End - Start)\n")
    report.append(f"- Money delta: {money_delta:+,}\n")
    report.append(f"- Spore risk delta: {spore_delta:+}\n")
    report.append(f"- Security delta: {sec_delta:+}\n")
    report.append(f"- Pressure delta: {pres_delta:+}\n")
    report.append(f"- Morale delta: {morale_delta:+}\n")
    report.append(f"- Evidence delta: {ev_delta:+}\n\n")

    report.append("Stability\n")
    report.append(f"- Money variance (lower is more stable): {variance:,.2f}\n\n")

    report.append("Interpretation\n")
    report.append("- Implemented a structured logging pipeline capturing actions and risk signals.\n")
    report.append("- Produced daily KPI snapshots and an executive summary for repeatable monitoring.\n")
    report.append("- Demonstrates systems thinking, metrics design, and governance-ready audit trails.\n")

    with open("kpi_report.txt", "w", encoding="utf-8") as f:
        f.write("".join(report))


# -----------------------------
# 5) Facility（森/現場）
# -----------------------------
class Facility:
    def __init__(self, name="菌糸ネットワーク中央"):
        self.name = name
        self.spore_level = 25      # 胞子汚染度（リスク）
        self.pressure = 20         # 圧力
        self.security = 75         # 治安
        self.morale = 55           # 士気

    def display_info(self):
        print(f"\n--- 現場: {self.name} ---")
        print(f"{t('RISK_LABEL')}: {self.spore_level}% | {t('PRESSURE_LABEL')}: {self.pressure}%")
        print(f"{t('SECURITY_LABEL')}: {self.security} | {t('MORALE_LABEL')}: {self.morale}")

    def check_for_event(self):
        # 臨界：胞子汚染が高い
        if self.spore_level >= 70:
            return "SPORE_CRISIS"
        # 圧力が高すぎる
        if self.pressure >= 80:
            return "PRESSURE_SPIKE"
        return None


# -----------------------------
# 6) Player（主人公たち）
# -----------------------------
class Player:
    def __init__(self, name):
        self.name = name
        self.evidence = []
        self.poison_tolerance = 0  # 毒耐性（イベントで上下）

        if name == t("P1"):  # しいたけ
            self.HP = 95
            self.MP = 45
            self.money = -150000
            self.focus = 10
        elif name == t("P2"):  # えのき
            self.HP = 90
            self.MP = 55
            self.money = -80000
            self.focus = 12
        else:  # まいたけ
            self.HP = 110
            self.MP = 60
            self.money = 0
            self.focus = 6

    def display_status(self):
        print(f"\n--- {self.name} ---")
        print(f"HP:{self.HP}/100  MP:{self.MP}/60  {t('MONEY')}:{t('MONEY_LABEL')}{money_fmt(self.money)}")
        print(f"証拠:{len(self.evidence)}  毒耐性:{self.poison_tolerance}")

    # 6.1 培地設計（収支）
    def do_culture_planning(self, facility: Facility):
        print(f"\n🍄 {t('ACT1')}")
        self.MP = max(0, self.MP - 5)

        # 成功率：MPと集中力で少し上下
        success_chance = 55 + (self.MP // 3) + self.focus
        roll = random.randint(1, 100)

        if roll <= success_chance:
            gain = random.randint(800, 1800)
            self.money += gain
            self.MP = min(60, self.MP + 3)
            facility.morale = min(100, facility.morale + 2)
            print(f"✅ 培地設計がうまく回った。収支 +{t('MONEY_LABEL')}{money_fmt(gain)} / 士気 +2")
            # たまに「危ない培地」の選択が来る
            if random.random() < 0.35:
                self.handle_spore_dilemma(facility)
        else:
            loss = random.randint(500, 1500)
            self.money -= loss
            facility.pressure = min(100, facility.pressure + 5)
            self.MP = max(0, self.MP - 5)
            print(f"❌ 設計が崩れた。収支 -{t('MONEY_LABEL')}{money_fmt(loss)} / 圧力 +5")

    def handle_spore_dilemma(self, facility: Facility):
        print("\n⚠️【ジレンマ】安価だが胞子リスクの高い素材が提案された。")
        print("A: コスト優先（収支↑・汚染↑） / B: 安全優先（収支↓・汚染↓）")
        choice = input("選択 (A/B): ").strip().upper()

        if choice == "A":
            self.money += 2000
            facility.spore_level = min(100, facility.spore_level + 7)
            facility.pressure = max(0, facility.pressure - 1)
            print(f"→ コスト優先：収支 +{t('MONEY_LABEL')}2,000 / 汚染 +7")
        elif choice == "B":
            self.money -= 1500
            facility.spore_level = max(0, facility.spore_level - 10)
            facility.morale = min(100, facility.morale + 1)
            print(f"→ 安全優先：収支 -{t('MONEY_LABEL')}1,500 / 汚染 -10")
        else:
            print("→ 迷って保留にした（変化なし）")

    # 6.2 衛生巡回（リスク/治安）
    def do_hygiene_patrol(self, facility: Facility):
        print(f"\n🧪 {t('ACT2')}")
        self.MP = max(0, self.MP - 5)

        # 成功率：汚染が高いほど難しい、治安が低いほど難しい
        difficulty = facility.spore_level + (100 - facility.security)
        roll = random.randint(1, 140)

        if roll > difficulty:
            facility.spore_level = max(0, facility.spore_level - 12)
            facility.security = min(100, facility.security + 5)
            facility.morale = min(100, facility.morale + 2)
            print("✅ 巡回成功：汚染 -12 / 治安 +5 / 士気 +2")
        else:
            # 失敗：毒きのこ遭遇 or 事故
            print("❌ 巡回中、毒きのこの影が…")
            if random.random() < 0.7:
                self.poison_encounter(facility)
            else:
                dmg = random.randint(3, 8)
                self.HP = max(0, self.HP - dmg)
                self.MP = max(0, self.MP - 5)
                facility.pressure = min(100, facility.pressure + 4)
                print(f"→ 転倒事故：HP -{dmg} / 圧力 +4")

    def poison_encounter(self, facility: Facility):
        enemy = random.choice(POISON_MUSHROOMS)
        name = f"{enemy['jp']}（{enemy['alias']}）"
        danger = enemy["danger"]

        print(f"\n☠️ 遭遇：{name}  危険度:{danger}")
        print("行動: 1)記録して回避  2)強行突破  3)落ち着く（防御）")
        choice = input("選択 (1/2/3): ").strip()

        if choice == "1":
            # 記録して回避：リスク下げ、証拠になる場合あり
            facility.spore_level = max(0, facility.spore_level - (2 + danger))
            self.MP = min(60, self.MP + 2)
            if random.random() < 0.35:
                self.try_collect_evidence(current_day=None, force=True)
            print(f"✅ 回避成功：汚染 -{2 + danger} / MP +2")
        elif choice == "2":
            # 強行突破：収支少し増えることもあるがダメージ
            dmg = random.randint(5, 10) + danger
            self.HP = max(0, self.HP - dmg)
            self.MP = max(0, self.MP - 6)
            facility.security = max(0, facility.security - (3 + danger))
            facility.pressure = min(100, facility.pressure + 6)
            gain = random.randint(0, 1200)
            self.money += gain
            print(f"⚔️ 強行：HP -{dmg} / 治安 -{3 + danger} / 圧力 +6 / 収支 +{t('MONEY_LABEL')}{money_fmt(gain)}")
        else:
            # 防御：MP回復、でも汚染少し増える
            self.MP = min(60, self.MP + 8)
            facility.spore_level = min(100, facility.spore_level + 3)
            print("🛡️ 防御：MP +8 / 汚染 +3")

    # 6.3 探索（証拠収集/イベント）
    def do_mycelium_trip(self, facility: Facility, current_day: int):
        print(f"\n🕸️ {t('ACT3')}")
        self.MP = max(0, self.MP - 6)

        # 1) 証拠探索
        self.try_collect_evidence(current_day=current_day)

        # 2) ランダムイベント
        if random.random() < 0.35:
            event = random.choice(["PRESSURE_CALL", "MORALE_BOOST", "SPORE_LEAK"])
            if event == "PRESSURE_CALL":
                facility.pressure = min(100, facility.pressure + 7)
                self.MP = max(0, self.MP - 3)
                print("📞 圧力の連絡が来た：圧力 +7 / MP -3")
            elif event == "MORALE_BOOST":
                facility.morale = min(100, facility.morale + 6)
                print("🌿 現場の協力が得られた：士気 +6")
            else:
                facility.spore_level = min(100, facility.spore_level + 9)
                facility.security = max(0, facility.security - 3)
                print("☁️ 胞子漏れ：汚染 +9 / 治安 -3")

    def try_collect_evidence(self, current_day: int | None, force: bool = False):
        # 未回収の証拠を探す
        remaining = []
        for doc_id, info in DOSSIER.items():
            if info["name"] in self.evidence:
                continue
            if force:
                remaining.append((doc_id, info))
            else:
                if current_day is not None and current_day >= info["unlock_day"]:
                    remaining.append((doc_id, info))

        if not remaining:
            if not force:
                print("🔎 証拠は見つからなかった（また後日）")
            return

        doc_id, info = random.choice(remaining)
        # 成功率：MPと集中力
        chance = 55 + (self.MP // 3) + self.focus
        roll = random.randint(1, 100)

        if roll <= chance:
            self.evidence.append(info["name"])
            self.MP = min(60, self.MP + 4)
            print(f"📎 証拠入手：{info['name']}（Power {info['power']}） / MP +4")
        else:
            self.MP = max(0, self.MP - 4)
            print("❌ 証拠探索に失敗（MP -4）")


# -----------------------------
# 7) エンディング
# -----------------------------
def ending_mp_zero(player: Player):
    print(f"\n--- 💔 {t('END_MP')} ---")
    if player.name == t("P1"):
        print("しいたけは静かに傘を閉じ、森の外で休むことにした。")
    elif player.name == t("P2"):
        print("えのきは現場を整理し、引き継ぎメモだけ残した。")
    else:
        print("まいたけは笑っている。MPが0でも、なぜか笑っている。")

def ending_hp_zero(player: Player):
    print(f"\n--- 🚑 {t('END_HP')} ---")
    if player.name == t("P1"):
        print("しいたけは胞子にやられた…しかしログは残った。")
    elif player.name == t("P2"):
        print("えのきは堅実さで耐えたが、最後は力尽きた。")
    else:
        print("まいたけは派手に転んだ。なぜか士気は上がった。")

def final_conference(player: Player):
    power = 0
    for doc_id, info in DOSSIER.items():
        if info["name"] in player.evidence:
            power += info["power"]
    # 雑に判定（証拠が多いほど勝ち）
    defense = 70 + random.randint(0, 40)
    print("\n--- 🌳 FINAL: 森の改善会議 ---")
    print(f"提案（証拠パワー）: {power}  vs  抵抗（防御）: {defense}")

    if power >= defense:
        print("\n🎉 改善提案が通った！ログと数値が森を救った。")
        print(f"✅ {t('CLEAR')}")
    else:
        print("\n💥 まだ足りない…証拠が弱く、改善は先送りになった。")
        print("（ただしログが残った。次のあなたが続きから戦える。）")


# -----------------------------
# 8) キャラ選択
# -----------------------------
def select_character() -> Player:
    print("\n--- 🍄 誰で森を守る？ ---")
    print(f"1: {t('P1')}（バランス）")
    print(f"2: {t('P2')}（堅実）")
    print(f"3: {t('P3')}（無敵の鈍感力）")
    choice = input("番号: ").strip()

    if choice == "1":
        return Player(t("P1"))
    if choice == "2":
        return Player(t("P2"))
    return Player(t("P3"))


# -----------------------------
# 9) メイン
# -----------------------------
def start_game():
    logger = GameLogger("run_log.csv")
    facility = Facility("菌糸ネットワーク中央")
    player = select_character()
    day = 1
    max_days = 30  # ここは好みで変えてOK（30推奨）

    print("\n==============================================")
    print("  The Mycologist – Mycelium Ops Simulation 🍄")
    print("==============================================")

    logger.log(day, player, facility, action="start_game", event="")

    while player.HP > 0 and player.MP > 0 and day <= max_days:
        print(f"\n--- DAY {day} ---")
        player.display_status()
        facility.display_info()

        print("\n--- 今日の行動を選択してください ---")
        print(f"1: {t('ACT1')}")
        print(f"2: {t('ACT2')}")
        print(f"3: {t('ACT3')}")
        print(f"4: {t('ACT4')}")

        choice = input("番号を入力: ").strip()

        if choice == "1":
            player.do_culture_planning(facility)
            logger.log(day, player, facility, action="culture_planning", event="")

        elif choice == "2":
            player.do_hygiene_patrol(facility)
            logger.log(day, player, facility, action="hygiene_patrol", event="")

        elif choice == "3":
            player.do_mycelium_trip(facility, current_day=day)
            logger.log(day, player, facility, action="mycelium_trip", event="")

        elif choice == "4":
            print("\n業務終了。今日も森を守りました。")

            # まいたけだけ赤字が勝手に増える（ネタ特性）
            if player.name == t("P3"):
                deficit_increase = 5000
                player.money -= deficit_increase
                print(f"😂 [無敵の鈍感力] 赤字が自動的に {t('MONEY_LABEL')}{money_fmt(deficit_increase)} 増えました。")
                logger.log(day, player, facility, action="maitake_auto_deficit", event="")

            logger.log(day, player, facility, action="end_day", event="")
            day += 1

        else:
            print("無効な選択です。")

        # その日の終わりにイベント判定（whileの中）
        ev = facility.check_for_event()
        if ev == "SPORE_CRISIS":
            print("\n🚨【緊急】胞子汚染が臨界。森が危険です。")
            logger.log(day, player, facility, action="system_alert", event="SPORE_CRISIS")
            # 臨界時はHP/MPにダメージ
            player.HP = max(0, player.HP - 8)
            player.MP = max(0, player.MP - 8)
        elif ev == "PRESSURE_SPIKE":
            print("\n📣【緊急】圧力が過剰。判断が歪む。")
            logger.log(day, player, facility, action="system_alert", event="PRESSURE_SPIKE")
            player.MP = max(0, player.MP - 6)
            facility.morale = max(0, facility.morale - 4)

    # ===== ここから while の外 =====
    if player.MP <= 0:
        ending_mp_zero(player)
    elif player.HP <= 0:
        ending_hp_zero(player)
    else:
        final_conference(player)

    generate_reports("run_log.csv")
    print("\n出力: run_log.csv / daily_summary.csv / kpi_report.txt")


if __name__ == "__main__":
    start_game()
