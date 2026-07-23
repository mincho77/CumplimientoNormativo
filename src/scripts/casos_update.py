#!/usr/bin/env python3
import csv
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CASES_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')

VALID_STATUS = {'detectado', 'extraido_ia', 'en_validacion', 'validado', 'rechazado', 'consolidado'}
VALID_PRIORITY = {'', 'baja', 'media', 'alta'}
VALID_APLICA = {'', 'si', 'no', 'parcial'}


def main():
    if len(sys.argv) < 3:
        print('Uso: scripts/casos_update.py <case_id> <status> [priority] [aplica_sura] [notes]')
        sys.exit(1)

    case_id = sys.argv[1].strip()
    status = sys.argv[2].strip().lower()
    priority = sys.argv[3].strip().lower() if len(sys.argv) > 3 else ''
    aplica = sys.argv[4].strip().lower() if len(sys.argv) > 4 else ''
    notes = sys.argv[5].strip() if len(sys.argv) > 5 else ''

    if status not in VALID_STATUS:
        raise SystemExit(f'status invalido: {status}')
    if priority not in VALID_PRIORITY:
        raise SystemExit(f'priority invalida: {priority}')
    if aplica not in VALID_APLICA:
        raise SystemExit(f'aplica_sura invalido: {aplica}')

    with open(CASES_FILE, 'r', encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
        fieldnames = rows[0].keys() if rows else []

    found = False
    for r in rows:
        if r.get('case_id') == case_id:
            r['status'] = status
            if priority:
                r['priority'] = priority
            if aplica:
                r['aplica_sura'] = aplica
            if notes:
                r['notes'] = notes
            found = True
            break

    if not found:
        raise SystemExit(f'case_id no encontrado: {case_id}')

    with open(CASES_FILE, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    print(f'actualizado: {case_id}')


if __name__ == '__main__':
    main()
