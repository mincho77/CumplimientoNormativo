#!/usr/bin/env python3
"""
Compliance Monitoring Dashboard - Flask App
Reads casos_detectados.csv and tablero_semaforo.csv
"""
import os
import csv
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
ROOT = os.path.abspath(os.path.dirname(__file__))
CASOS_FILE = os.path.join(ROOT, 'data', 'casos_detectados.csv')
SEMAFORO_FILE = os.path.join(ROOT, 'data', 'tablero_semaforo.csv')


def read_csv(filepath):
    """Read CSV and return list of dicts."""
    if not os.path.exists(filepath):
        return []
    rows = []
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_summary():
    """Get count summary by semaforo."""
    casos = read_csv(SEMAFORO_FILE)
    summary = {'ROJO': 0, 'AMARILLO': 0, 'VERDE': 0, 'CONSOLIDADO': 0}
    for caso in casos:
        semaforo = caso.get('semaforo', '').upper()
        if semaforo in summary:
            summary[semaforo] += 1
    return summary


def get_casos_by_filter(semaforo=None, entidad=None, priority=None, link_status=None, search=None):
    """Filter casos by criteria."""
    casos = read_csv(SEMAFORO_FILE)
    filtered = []

    for caso in casos:
        if semaforo and caso.get('semaforo', '').upper() != semaforo.upper():
            continue
        if entidad and caso.get('entidad') != entidad:
            continue
        if priority and caso.get('priority') != priority:
            continue
        if link_status and caso.get('link_status') != link_status:
            continue
        if search:
            search_lower = search.lower()
            searchable = f"{caso.get('entidad', '')} {caso.get('motivo', '')} {caso.get('notes', '')}".lower()
            if search_lower not in searchable:
                continue
        filtered.append(caso)

    return filtered


def get_entities():
    """Get unique entities."""
    casos = read_csv(SEMAFORO_FILE)
    entities = sorted(set(c.get('entidad', '') for c in casos if c.get('entidad')))
    return entities


def get_priorities():
    """Get unique priorities."""
    casos = read_csv(SEMAFORO_FILE)
    priorities = sorted(set(c.get('priority', '') for c in casos if c.get('priority')))
    return [p for p in priorities if p]


def get_link_statuses():
    """Get unique link statuses."""
    casos = read_csv(SEMAFORO_FILE)
    statuses = sorted(set(c.get('link_status', '') for c in casos if c.get('link_status')))
    return [s for s in statuses if s]


@app.route('/')
def index():
    summary = get_summary()
    entities = get_entities()
    priorities = get_priorities()
    link_statuses = get_link_statuses()
    return render_template('index.html',
                         summary=summary,
                         entities=entities,
                         priorities=priorities,
                         link_statuses=link_statuses)


@app.route('/api/casos')
def api_casos():
    """API endpoint to get filtered casos."""
    semaforo = request.args.get('semaforo')
    entidad = request.args.get('entidad')
    priority = request.args.get('priority')
    link_status = request.args.get('link_status')
    search = request.args.get('search')

    casos = get_casos_by_filter(semaforo, entidad, priority, link_status, search)
    return jsonify(casos)


@app.route('/api/summary')
def api_summary():
    """API endpoint for summary."""
    return jsonify(get_summary())


if __name__ == '__main__':
    print(f"[app] iniciando | root={ROOT}")
    print(f"[app] casos={CASOS_FILE}")
    print(f"[app] semaforo={SEMAFORO_FILE}")
    print(f"[app] server en http://localhost:5000")
    app.run(debug=True, host='localhost', port=5000)
