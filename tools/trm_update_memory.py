#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Update Memory – Päivittää TRM-muistin kierroksen jälkeen.

Päivittää trm/state.json (kierros, insights) ja tulostaa progress barin.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def update_memory(round_number: int, insights: str):
    """Päivittää TRM-muistin kierroksen jälkeen."""
    
    # Polut
    script_dir = Path(__file__).parent
    trm_dir = script_dir.parent / "trm"
    state_file = trm_dir / "state.json"
    
    if not state_file.exists():
        print("❌ Virhe: trm/state.json ei löydy. Aloita sessio ensin: python tools/trm_start_session.py \"Tehtävä\"")
        return
    
    # Lataa tila
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    if state["status"] != "in-progress":
        print(f"⚠️  Varoitus: Sessio ei ole aktiivinen (status: {state['status']}).")
        return
    
    # Päivitä
    state["current_round"] = round_number
    state["updated_at"] = datetime.now().isoformat()
    
    if insights:
        state["insights"].append({
            "round": round_number,
            "text": insights,
            "timestamp": state["updated_at"]
        })
    
    # Tallenna
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    # Progress bar
    progress = round_number * 10
    bar_length = 50
    filled = int(bar_length * progress / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    # Kierroksen kuvaus
    if round_number <= 3:
        phase = "THINK"
        desc = "Ongelma ymmärretty ja analysoitu"
    elif round_number <= 8:
        phase = "REFINE"
        desc = "Ratkaisu kehitetty iteratiivisesti"
    else:
        phase = "MASTER"
        desc = "Lopullinen viimeistely ja validointi"
    
    print("\n─────────────────────────────────────────────────────────────")
    print(f"🔄 KIERROS {round_number}/10 – {phase}")
    print(f"   {desc}")
    print(f"   [{bar}] {progress}%")
    print("─────────────────────────────────────────────────────────────")
    
    if insights:
        print(f"\n💡 Opit kierrokselta {round_number}:")
        print(f"   {insights}\n")
    
    if round_number < 10:
        print(f"✅ Kierros {round_number}/10 valmis.")
        print(f"📁 Tila tallennettu: {state_file}\n")
        print("💡 Seuraavaksi:")
        print(f"   1. Työstä kierros {round_number + 1}.")
        print(f"   2. Päivitä tila: python tools/trm_update_memory.py {round_number + 1} \"Kierroksen {round_number + 1} opit\"\n")
    else:
        print(f"\n🎉 TRM-analyysi valmis!")
        print(f"   Kierroksia suoritettu: {round_number}")
        print(f"   Malli: Thinking ➜ Reasoning ➜ Memory\n")
        print("💡 Viimeistele sessio:")
        print("   python tools/trm_finalize_session.py \"Lopputulos ja hyväksymiskriteerit\"\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Käyttö: python trm_update_memory.py <kierros> [\"opit\"]")
        sys.exit(1)
    
    try:
        round_num = int(sys.argv[1])
    except ValueError:
        print("❌ Virhe: Kierroksen tulee olla numero (1-10).")
        sys.exit(1)
    
    if round_num < 1 or round_num > 10:
        print("❌ Virhe: Kierroksen tulee olla 1-10.")
        sys.exit(1)
    
    insights_text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
    update_memory(round_num, insights_text)
