#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Finalize Session – Sulkee TRM-session ja tallentaa opit memory.md-tiedostoon.

Kopioi opit trm/memory.md-tiedostoon ja resetoi trm/state.json.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def finalize_session(conclusion: str):
    """Sulkee TRM-session ja tallentaa opit."""
    
    # Polut
    script_dir = Path(__file__).parent
    trm_dir = script_dir.parent / "trm"
    state_file = trm_dir / "state.json"
    memory_file = trm_dir / "memory.md"
    
    if not state_file.exists():
        print("❌ Virhe: trm/state.json ei löydy. Ei aktiivista sessiota.")
        return
    
    # Lataa tila
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    if state["status"] != "in-progress":
        print(f"⚠️  Varoitus: Sessio ei ole aktiivinen (status: {state['status']}).")
        return
    
    # Rakenna session-tiivistelmä
    now = datetime.now().strftime("%Y-%m-%d")
    task = state["task"]
    insights = state["insights"]
    completed_round = int(state.get("current_round") or 0)
    
    session_entry = f"\n\n---\n\n## Session: {now} – {task}\n\n"
    session_entry += f"**Ongelma**: {task}\n\n"
    session_entry += f"**Ratkaisu**: {conclusion}\n\n"
    session_entry += "**Opit**:\n\n"
    
    for insight in insights:
        session_entry += f"- **Kierros {insight['round']}**: {insight['text']}\n"
    
    session_entry += "\n**Hyväksymiskriteerit täyttyneet**:\n"
    session_entry += "- ✅ (Täytä hyväksymiskriteerit tähän)\n"
    
    # Lisää memory.md-tiedostoon
    if memory_file.exists():
        with open(memory_file, "r", encoding="utf-8") as f:
            memory_content = f.read()
        
        # Etsi "(Lisää tulevat sessionit tänne)" ja lisää ennen sitä
        marker = "## (Lisää tulevat sessionit tänne)"
        if marker in memory_content:
            memory_content = memory_content.replace(marker, session_entry + "\n" + marker)
        else:
            memory_content += session_entry
    else:
        memory_content = f"# TRM Memory (Codesphere Website)\n{session_entry}"
    
    with open(memory_file, "w", encoding="utf-8") as f:
        f.write(memory_content)
    
    # Resetoi state.json
    state["current_round"] = 0
    state["status"] = "idle"
    state["task"] = ""
    state["insights"] = []
    state["started_at"] = None
    state["updated_at"] = None
    
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    
    # Tulosta yhteenveto
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║  ✅ TRM-SESSIO SULJETTU                                     ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    print(f"Tehtävä: {task}")
    print(f"Kierroksia suoritettu: {completed_round}/10")
    print("Malli: Thinking ➜ Reasoning ➜ Memory\n")
    print("─────────────────────────────────────────────────────────────")
    print("📄 TULOKSEN RAKENNE:\n")
    print("   1. Thinking (Ajattelu)")
    print("       Ongelma ymmärretty ja analysoitu\n")
    print("   2. Reasoning (Päättely)")
    print("       Ratkaisu kehitetty iteratiivisesti\n")
    print("   3. Memory (Muisti)")
    print("       Opit tallennettu tulevaa käyttöä varten\n")
    print("─────────────────────────────────────────────────────────────")
    print(f"✅ Opit tallennettu: {memory_file}")
    print(f"✅ Tila nollattu: {state_file}\n")
    print("💡 Voit nyt aloittaa uuden session:")
    print("   python tools/trm_start_session.py \"Uusi tehtävä\"\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Käyttö: python trm_finalize_session.py \"Lopputulos ja hyväksymiskriteerit\"")
        sys.exit(1)
    
    conclusion_text = " ".join(sys.argv[1:])
    finalize_session(conclusion_text)
