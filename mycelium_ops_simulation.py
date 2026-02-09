import random
import csv
from datetime import datetime

# =========================================================
# Project: BizOps Simulation Framework
# Module: Resource & Risk Management Simulator
# Description:
#   A simulation model to optimize resource allocation under
#   uncertainty and constraints.
#   Generates audit trails (CSV) for post-mortem analysis.
# =========================================================

# -----------------------------
# 0) Configuration / Constants
# -----------------------------
TEXT = {
    # Actions (Operations)
    "ACT1": "Resource Allocation (リソース配分実行)",
    "ACT2": "Compliance Audit (コンプライアンス監査)",
    "ACT3": "Process Mining (プロセス分析・証拠保全)",
    "ACT4": "End of Day (日次締め処理)",
    
    # Simulation Models (Characters)
    "P1": "Model-A (Balanced Ops)",
    "P2": "Model-B (Efficiency Focus)",
    "P3": "Model-C (High Risk / High Return)",
    
    # KPIs / Metrics
    "MONEY": "Capital",
    "MONEY_LABEL": "¥",
    "RISK_LABEL": "Risk Level (リスク係数)",
    "PRESSURE_LABEL": "System Load (負荷)",
    "SECURITY_LABEL": "Governance (統制レベル)",
    "MORALE_LABEL": "Team Engagement (組織活力)",
    
    # System Messages
    "END_MP": "Resource Exhausted: Cognitive Load Limit Reached.",
    "END_HP": "Critical Failure: Operational Capacity Depleted.",
    "CLEAR": "Objective Achieved: Sustainable Operation Model Established.",
}

def t(k: str) -> str:
    return TEXT.get(k, k)

def money_fmt(x: int) -> str:
    return f"{x:,}"


# -----------------------------
# 1) Risk Events (Formerly Poison Mushrooms)
# -----------------------------
RISK_EVENTS = [
    {"code": "ERR_01", "name": "Unexpected Downtime", "impact": 5},
    {"code": "ERR_02", "name": "Data Breach Attempt", "impact": 3},
    {"code": "ERR_03", "name": "Supply Chain Disruption", "impact": 5},
    {"code": "ERR_04", "name": "Compliance Violation", "impact": 4},
    {"code": "ERR_05", "name": "Audit Failure", "impact": 4},
    {"code": "ERR_06", "name": "Human Error (Critical)", "impact": 4},
    {"code": "ERR_07", "name": "Budget Overrun", "impact": 3},
    {"code": "ERR_08", "name": "Stakeholder Conflict", "impact": 4},
    {"code": "ERR_09", "name": "Minor Bug", "impact": 2},
]

# -----------------------------
# 2) Evidence / Audit Logs (Formerly Dossier)
# -----------------------------
AUDIT_LOGS = {
    "LOG001": {"name": "Cost Analysis Report (Legacy)", "power": 20, "unlock_day": 2},
    "LOG002": {"name": "Missing Audit Trail", "power": 15, "unlock_day": 4},
    "LOG003": {"name": "Risk Threshold Violation Data", "power": 25, "unlock_day": 6},
    "LOG004": {"name": "Unauthorized Instruction Log", "power": 10, "unlock_day": 1},
    "LOG005": {"name": "Optimization Proposal Draft", "power": 20, "unlock_day": 8},
}


# -----------------------------
# 3) Logger (Audit Trail)
# -----------------------------
class SystemLogger:
    def __init__(self, filepath="audit_trail.csv"):
        self.filepath = filepath
        self.fieldnames = [
            "timestamp", "day", "model_id", "facility_id",
            "action_type", "event_details",
            "capacity_hp", "cognitive_mp", "capital_balance",
            "risk_metric", "system_load", "governance_score", "engagement_score",
            "evidence_count"
        ]
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.fieldnames).writeheader()

    def log(self, day, player, facility, action, event=""):
        row = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "day": int(day),
            "model_id": player.name,
            "facility_id": facility.name,
            "action_type": action,
            "event_details": event,
            "capacity_hp": int(player.HP),
            "cognitive_mp": int(player.MP),
            "capital_balance": int(player.money),
            "risk_metric": int(facility.risk_level),
            "system_load": int(facility.system_load),
            "governance_score": int(facility.governance),
            "engagement_score": int(facility.engagement),
            "evidence_count": int(len(player.evidence)),
        }
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=self.fieldnames).writerow(row)


# -----------------------------
# 4) Report Generation
# -----------------------------
def generate_reports(log_path="audit_trail.csv"):
    rows = []
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                # Convert numeric fields
                for k in ["day", "capacity_hp", "cognitive_mp", "capital_balance", 
                          "risk_metric", "system_load", "governance_score", 
                          "engagement_score", "evidence_count"]:
                    r[k] = int(float(r[k]))
                rows.append(r)
    except FileNotFoundError:
        return

    if not rows:
        return

    # Aggregate Daily Snapshots
    by_day = {}
    for r in rows:
        d = r["day"]
        by_day.setdefault(d, {
            "day": d,
            "actions": 0,
            "events": 0,
            "balance_end": 0,
            "risk_end": 0
        })
        by_day[d]["actions"] += 1
        if r.get("event_details"):
            by_day[d]["events"] += 1
        by_day[d]["balance_end"] = r["capital_balance"]
        by_day[d]["risk_end"] = r["risk_metric"]

    daily = [by_day[d] for d in sorted(by_day.keys())]

    # Generate Executive Summary
    first = daily[0]
    last = daily[-1]
    
    report = []
    report.append("BizOps Simulation: Executive Summary Report\n")
    report.append("========================================================\n")
    report.append(f"Simulation Period: Day {first['day']} - Day {last['day']}\n")
    report.append(f"Final Capital Balance: {t('MONEY_LABEL')}{money_fmt(last['balance_end'])}\n")
    report.append(f"Final Risk Metric: {last['risk_end']} (Threshold: 70)\n")
    report.append("\nConclusion:\n")
    report.append("The simulation demonstrates the trade-off between resource allocation and operational risk.\n")
    
    with open("executive_summary.txt", "w", encoding="utf-8") as f:
        f.write("".join(report))


# -----------------------------
# 5) Facility (Operational Environment)
# -----------------------------
class OpEnvironment:
    def __init__(self, name="Main_Branch_Ops"):
        self.name = name
        self.risk_level = 25       # Formerly spore_level
        self.system_load = 20      # Formerly pressure
        self.governance = 75       # Formerly security
        self.engagement = 55       # Formerly morale

    def display_info(self):
        print(f"\n--- Environment: {self.name} ---")
        print(f"{t('RISK_LABEL')}: {self.risk_level}% | {t('PRESSURE_LABEL')}: {self.system_load}%")
        print(f"{t('SECURITY_LABEL')}: {self.governance} | {t('MORALE_LABEL')}: {self.engagement}")

    def check_for_anomaly(self):
        if self.risk_level >= 70:
            return "CRITICAL_RISK_ALERT"
        if self.system_load >= 80:
            return "OVERLOAD_ALERT"
        return None


# -----------------------------
# 6) Player (Simulation Agent)
# -----------------------------
class SimAgent:
    def __init__(self, name):
        self.name = name
        self.evidence = []
        self.resilience = 0

        if name == t("P1"):  # Balanced
            self.HP = 95
            self.MP = 45
            self.money = -150000
            self.focus = 10
        elif name == t("P2"):  # Efficient
            self.HP = 90
            self.MP = 55
            self.money = -80000
            self.focus = 12
        else:  # High Risk
            self.HP = 110
            self.MP = 60
            self.money = 0
            self.focus = 6

    def display_status(self):
        print(f"\n--- Agent Status: {self.name} ---")
        print(f"Capacity(HP):{self.HP}  Cognitive(MP):{self.MP}  {t('MONEY')}:{t('MONEY_LABEL')}{money_fmt(self.money)}")
        print(f"Audit Logs:{len(self.evidence)}  Resilience:{self.resilience}")

    # 6.1 Resource Allocation
    def execute_allocation(self, env: OpEnvironment):
        print(f"\n📊 {t('ACT1')}")
        self.MP = max(0, self.MP - 5)

        success_chance = 55 + (self.MP // 3) + self.focus
        roll = random.randint(1, 100)

        if roll <= success_chance:
            gain = random.randint(800, 1800)
            self.money += gain
            self.MP = min(60, self.MP + 3)
            env.engagement = min(100, env.engagement + 2)
            print(f"✅ Allocation Optimized. Capital +{t('MONEY_LABEL')}{money_fmt(gain)} / Engagement +2")
            
            if random.random() < 0.35:
                self.handle_tradeoff(env)
        else:
            loss = random.randint(500, 1500)
            self.money -= loss
            env.system_load = min(100, env.system_load + 5)
            self.MP = max(0, self.MP - 5)
            print(f"❌ Allocation Inefficient. Capital -{t('MONEY_LABEL')}{money_fmt(loss)} / Load +5")

    def handle_tradeoff(self, env: OpEnvironment):
        print("\n⚠️ [DECISION POINT] Low-cost / High-risk Vendor Proposed.")
        print("A: Cost Priority (Risk UP) / B: Safety Priority (Cost UP)")
        choice = input("Select (A/B): ").strip().upper()

        if choice == "A":
            self.money += 2000
            env.risk_level = min(100, env.risk_level + 7)
            env.system_load = max(0, env.system_load - 1)
            print(f"→ Selected A: Capital +2000 / Risk +7")
        elif choice == "B":
            self.money -= 1500
            env.risk_level = max(0, env.risk_level - 10)
            env.engagement = min(100, env.engagement + 1)
            print(f"→ Selected B: Capital -1500 / Risk -10")
        else:
            print("→ No Decision Made.")

    # 6.2 Compliance Audit
    def execute_audit(self, env: OpEnvironment):
        print(f"\n🛡️ {t('ACT2')}")
        self.MP = max(0, self.MP - 5)

        difficulty = env.risk_level + (100 - env.governance)
        roll = random.randint(1, 140)

        if roll > difficulty:
            env.risk_level = max(0, env.risk_level - 12)
            env.governance = min(100, env.governance + 5)
            env.engagement = min(100, env.engagement + 2)
            print("✅ Audit Successful: Risk -12 / Governance +5")
        else:
            print("❌ Audit Failed: Anomaly Detected...")
            if random.random() < 0.7:
                self.encounter_risk(env)
            else:
                dmg = random.randint(3, 8)
                self.HP = max(0, self.HP - dmg)
                self.MP = max(0, self.MP - 5)
                env.system_load = min(100, env.system_load + 4)
                print(f"→ Operational Incident: Capacity -{dmg} / Load +4")

    def encounter_risk(self, env: OpEnvironment):
        event = random.choice(RISK_EVENTS)
        name = f"{event['name']} (Impact:{event['impact']})"
        
        print(f"\n🚨 ALERT: {name}")
        print("Action: 1)Log & Mitigate  2)Force Resolve  3)Hold (Defend)")
        choice = input("Select (1/2/3): ").strip()

        if choice == "1":
            env.risk_level = max(0, env.risk_level - (2 + event['impact']))
            self.MP = min(60, self.MP + 2)
            print(f"✅ Mitigated: Risk Reduced.")
        elif choice == "2":
            dmg = random.randint(5, 10) + event['impact']
            self.HP = max(0, self.HP - dmg)
            env.governance = max(0, env.governance - 3)
            print(f"⚔️ Forced Resolution: Capacity -{dmg} / Governance -3")
        else:
            self.MP = min(60, self.MP + 8)
            env.risk_level = min(100, env.risk_level + 3)
            print("🛡️ Hold Position: Cognitive +8 / Risk +3")

    # 6.3 Process Mining
    def execute_mining(self, env: OpEnvironment, current_day: int):
        print(f"\n🔍 {t('ACT3')}")
        self.MP = max(0, self.MP - 6)

        # 1) Collect Evidence
        self.try_collect_evidence(current_day=current_day)

        # 2) Random Event
        if random.random() < 0.35:
            print("ℹ️ System Notification: Minor fluctuations observed.")

    def try_collect_evidence(self, current_day: int):
        remaining = []
        for doc_id, info in AUDIT_LOGS.items():
            if info["name"] in self.evidence:
                continue
            if current_day >= info["unlock_day"]:
                remaining.append(info)

        if not remaining:
            print("🔎 No new anomalies found.")
            return

        info = random.choice(remaining)
        chance = 55 + (self.MP // 3) + self.focus
        
        if random.randint(1, 100) <= chance:
            self.evidence.append(info["name"])
            self.MP = min(60, self.MP + 4)
            print(f"📎 Log Secured: {info['name']} / Cognitive +4")
        else:
            self.MP = max(0, self.MP - 4)
            print("❌ Mining Failed (Noise in data).")


# -----------------------------
# 7) Simulation Endings
# -----------------------------
def finalize_simulation(agent: SimAgent):
    power = 0
    for doc_id, info in AUDIT_LOGS.items():
        if info["name"] in agent.evidence:
            power += info["power"]
    
    threshold = 70 + random.randint(0, 40)
    print("\n--- 🏁 FINAL REVIEW: Governance Committee ---")
    print(f"Proposal Strength (Evidence): {power}  vs  Resistance: {threshold}")

    if power >= threshold:
        print("\n🎉 APPROVED. The new operational model has been ratified.")
        print(f"✅ {t('CLEAR')}")
    else:
        print("\n📉 REJECTED. More data required for optimization.")


# -----------------------------
# 8) Initialization
# -----------------------------
def select_model() -> SimAgent:
    print("\n--- Select Simulation Model ---")
    print(f"1: {t('P1')}")
    print(f"2: {t('P2')}")
    print(f"3: {t('P3')}")
    choice = input("Number: ").strip()

    if choice == "1":
        return SimAgent(t("P1"))
    if choice == "2":
        return SimAgent(t("P2"))
    return SimAgent(t("P3"))

def start_simulation():
    logger = SystemLogger("audit_trail.csv")
    env = OpEnvironment("Main_Branch_Ops")
    agent = select_model()
    day = 1
    max_days = 30

    print("\n==============================================")
    print("  BizOps Simulation Framework v1.0")
    print("==============================================")

    logger.log(day, agent, env, action="init_simulation")

    while agent.HP > 0 and agent.MP > 0 and day <= max_days:
        print(f"\n--- DAY {day} ---")
        agent.display_status()
        env.display_info()

        print("\n--- Select Operation ---")
        print(f"1: {t('ACT1')}")
        print(f"2: {t('ACT2')}")
        print(f"3: {t('ACT3')}")
        print(f"4: {t('ACT4')}")

        choice = input("Input: ").strip()

        if choice == "1":
            agent.execute_allocation(env)
            logger.log(day, agent, env, action="resource_allocation")
        elif choice == "2":
            agent.execute_audit(env)
            logger.log(day, agent, env, action="compliance_audit")
        elif choice == "3":
            agent.execute_mining(env, current_day=day)
            logger.log(day, agent, env, action="process_mining")
        elif choice == "4":
            print("\nDay Concluded.")
            logger.log(day, agent, env, action="end_of_day")
            day += 1
        else:
            print("Invalid Input.")

        # Check Anomalies
        alert = env.check_for_anomaly()
        if alert:
            print(f"\n🚨 SYSTEM ALERT: {alert}")
            logger.log(day, agent, env, action="system_alert", event=alert)
            agent.MP = max(0, agent.MP - 5)

    finalize_simulation(agent)
    generate_reports("audit_trail.csv")
    print("\n[OUTPUT] audit_trail.csv / executive_summary.txt generated.")

if __name__ == "__main__":
    start_simulation()

