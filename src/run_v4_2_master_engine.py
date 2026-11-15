"""
PROJECT RR-EDGE V4.2: MASTER ENGINE ORCHESTRATOR
Executes all 5 analytical sub-engines in sequence:
1. v4_2_canonical_squad_registry
2. v4_2_trade_and_news_intelligence
3. v4_2_financial_and_rules_engine
4. v4_2_performance_and_dependency_engine
5. v4_2_matchup_and_lineup_optimizer
6. v4_2_franchise_market_and_scouting
7. v4_2_match_and_tournament_simulator
8. v4_2_decision_governance_and_validation
"""

import sys
import os
import time

# Ensure src/ is in python path
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from v4_2_canonical_squad_registry import build_canonical_squad_registry
from v4_2_trade_and_news_intelligence import build_trade_and_news_intelligence
from v4_2_financial_and_rules_engine import build_financial_and_rules_engine
from v4_2_performance_and_dependency_engine import build_performance_and_dependency_engine
from v4_2_matchup_and_lineup_optimizer import build_matchup_and_lineup_optimizer
from v4_2_franchise_market_and_scouting import build_franchise_market_and_scouting
from v4_2_match_and_tournament_simulator import build_match_and_tournament_simulator
from v4_2_decision_governance_and_validation import build_decision_governance_and_validation

def main():
    print("=" * 80)
    print("PROJECT RR-EDGE V4.2: FRANCHISE DECISION INTELLIGENCE SYSTEM")
    print("Execution Cut-off: 13 November 2026, 18:30 IST")
    print("=" * 80)

    start_time = time.time()
    build_canonical_squad_registry()
    build_trade_and_news_intelligence()
    build_financial_and_rules_engine()
    build_performance_and_dependency_engine()
    build_matchup_and_lineup_optimizer()
    build_franchise_market_and_scouting()
    build_match_and_tournament_simulator()
    build_decision_governance_and_validation()
    elapsed = time.time() - start_time

    print("=" * 80)
    print(f"All RR-EDGE V4.2 sub-engines executed successfully in {elapsed:.2f} seconds!")
    print("=" * 80)

if __name__ == "__main__":
    main()
