#!/usr/bin/env python3
import csv
import json
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
NOTIF_STATE = os.path.join(ROOT, 'data', 'state', 'notifications.json')

def load_notif_state():
    if not os.path.exists(NOTIF_STATE):
        return {'notified_ids': []}
    with open(NOTIF_STATE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_notif_state(state):
    with open(NOTIF_STATE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def notify_teams(case):
    print(f"[TEAMS] Notificando norma: {case.get('Título', 'Sin título')} | Emisor: {case.get('Emisor')}")
    print(f"       URL: {case.get('URL')}")

def notify_email(case, reason):
    print(f"[EMAIL] Notificando por {reason}: {case.get('Título', 'Sin título')}")
    print(f"        Vínculo: {case.get('URL')}")

def main():
    if not os.path.exists(CASES_FILE):
        return

    state = load_notif_state()
    notified_ids = set(state['notified_ids'])
    
    new_notifs = 0
    with open(CASES_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row['case_id']
            if cid in notified_ids:
                continue
            
            # Solo notificar casos 'detectado' (no errores de fuente)
            if row.get('status') == 'detectado':
                notify_teams(row)
                
                # Reglas especiales para Email (ejemplo basado en prioridad o SOX)
                if row.get('Control SOX') == 'SÍ':
                    notify_email(row, "Relevancia Financiera / SOX")
                
                notified_ids.add(cid)
                new_notifs += 1

    state['notified_ids'] = list(notified_ids)
    save_notif_state(state)
    print(f"[notificador] Fin | Notificaciones enviadas: {new_notifs}")

if __name__ == '__main__':
    main()
