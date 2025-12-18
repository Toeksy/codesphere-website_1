#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Start Session – Aloittaa uuden TRM 10x -session.

Alustaa trm/state.json -tilan ja tulostaa briefin.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def start_session(task_description: str):
    """Aloittaa uuden TRM-session."""
    
    # Polut
    script_dir = Path(__file__).parent
    trm_dir = script_dir.parent / "trm"
    state_file = trm_dir / "state.json"
    
    # Lataa nykyinen tila
    if state_file.exists():
        with open(state_file, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        if state["status"] != "idle":
            print(f"⚠️  Varoitus: Edellinen sessio ({state['task']}) on vielä auki (status: {state['status']}).")
            response = input("Haluatko sulkea sen ja aloittaa uuden? (y/n): ")
            if response.lower() != "y":
                print("❌ Session aloitus peruutettu.")
                return
    else:
        state = {
            "current_round": 0,
            "status": "idle",
            "task": "",
            "insights": [],
            "started_at": None,
            "updated_at": None
        }
    
    # Alusta uusi sessio
    now = datetime.now().isoformat()
    state["current_round"] = 0
    state["status"] = "in-progress"
    state["task"] = task_description
    state["insights"] = []
    state["started_at"] = now
    state["updated_at"] = now
    
    # Tallenna
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    # Tulosta brief
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  🚀 TRM-AJATTELUMALLI (Thinking, Reasoning, Memory)        ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    print(f"Tehtävä: {task_description}")
    print("Kierrokset: 10\n")
    print("─────────────────────────────────────────────────────────────")
    print("🔄 KIERROS 1/10 – ALKUPERÄINEN SUUNNITELMA (THINK)")
    print("   • Ymmärrä ongelma")
    print("   • Tunnista keskeiset haasteet")
    print("   • Luo alustava ratkaisu")
    print("─────────────────────────────────────────────────────────────\n")
    print(f"✅ Sessio aloitettu: {now}")
    print(f"📁 Tila tallennettu: {state_file}\n")
    print("💡 Seuraavaksi:")
    print("   1. Työstä kierros 1.")
    print("   2. Päivitä tila: python tools/trm_update_memory.py 1 \"Kierroksen 1 opit\"\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Käyttö: python trm_start_session.py \"Tehtävän kuvaus\"")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    start_session(task)
