import json
import os
from typing import List
from openpyxl import Workbook

from .game_object import GameObject

def export_to_json(games: List[GameObject], output_path: str):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump([g.to_dict() for g in games], f, indent=4, ensure_ascii=False)

"""
Used to use this to load the json for export:
for game, details in game_DB.items():
    export_DB[game] = json.loads(json.dumps(details.__dict__))
    
and then json.dump export_DB
"""

def export_to_excel(games: List[GameObject], output_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Game List"

    # Header row
    headers = list(games[0].to_dict().keys())
    ws.append(headers)

    for game in games:
        ws.append([game.to_dict().get(h, "") for h in headers])

    wb.save(output_path)

def export_to_text(games: List[GameObject], output_path: str):
    #Add logic for completed games
    with open(output_path, 'w', encoding='utf-8') as f:
        for game in games:
            f.write(f"[{game.igdb_ID}] {game.title}: {game.ranked_score}\n")
