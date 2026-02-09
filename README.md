# BizOps Simulation Framework: Resource & Risk Management
### リソース制約下における意思決定とリスク管理のシミュレーションモデル

##  Project Overview
このプロジェクトは、不確実な環境下における**「リソース配分（Resource Allocation）」と「リスク管理（Risk Mitigation）」のトレードオフを検証**するために設計された、Pythonによる業務プロセス・シミュレーターです。

単純な数値計算だけでなく、**「コンプライアンス違反」や「システム障害」といったリスクイベントを確率的に発生**させ、それに対する運用判断（Mitigation Action）が最終的なKPI（資本・安全性）にどう影響するかをモデル化しています。

また、BizOps（業務改善）の実務を想定し、全ての操作とシステム状態を**監査証跡（Audit Trail）としてCSVに記録**する機能を実装しています。

## Core Objectives
このプロジェクトの目的は、以下の3点を技術的に実証することです。

1.  **Process Modeling (業務プロセスの構造化):**
    * 複雑な業務フロー（予算管理、監査、トラブル対応）をオブジェクト指向（クラス設計）によって抽象化・標準化する。
2.  **Audit Logging (監査ログの設計):**
    * 「いつ」「誰が」「何をしたか」を完全な証跡として記録し、事後分析（Post-Mortem）を可能にするデータパイプラインの構築。
3.  **Risk Simulation (リスクの定量化):**
    * 「攻め（利益追求）」と「守り（コンプライアンス）」のバランスをシミュレーションし、最適な運用モデルを探索する。

##  Tech Stack
* **Language:** Python 3.x
* **Design Pattern:** Object-Oriented Programming (OOP), State Pattern
* **Data Handling:** CSV (Standard Library) for Logging & Reporting
* **Visualization:** CUI Dashboard (Console Output with Visual Indicators)

##  Key Features
### 1. Operation Simulation (運用シミュレーション)
日々の業務アクションを選択し、リソース（HP/MP/Capital）を管理します。
* **Resource Allocation:** 予算投下による収益化（リスク増の可能性あり）
* **Compliance Audit:** リスクレベルを下げるための監査活動
* **Process Mining:** 潜在的なリスクや証拠（Evidence）の発見

### 2. Audit Trail System (監査ログ)
実行された全てのアクションは `audit_trail.csv` に自動記録されます。
これにより、ブラックボックス化しやすい運用プロセスを可視化します。

| Timestamp | Day | Model | Action | Risk_Metric | Capital |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 2025-02-09T10:00:00 | 1 | Model-A | Resource_Allocation | 25 | -150,000 |
| 2025-02-09T10:05:00 | 1 | Model-A | Compliance_Audit | 13 | -150,000 |

### 3. Visual Indicators (視認性向上)
CUI環境におけるオペレーターの認知負荷を下げるため、ステータスをアイコンで可視化しています。
* `✅` Success / Normal Operation
* `⚠️` Warning / High Load
* `🚨` Critical Alert / System Failure
* `🛡️` Mitigation Action Taken

## 🚀 How to Run
```bash
# Clone the repository
git clone [https://github.com/your-username/bizops-simulation.git](https://github.com/your-username/bizops-simulation.git)

# Navigate to the directory
cd bizops-simulation

# Run the simulation
python main.py
