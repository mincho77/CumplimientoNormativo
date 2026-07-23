#!/usr/bin/env python3
"""
Patrón genérico de generación con autodetección y auto-reparación.

Este módulo implementa un loop acotado que:
1) valida la salida,
2) reintenta con contexto de error,
3) aplica fallback seguro,
4) retorna contrato consistente con repair_info,
5) permite persistir trazabilidad.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional, Tuple


GenerateFn = Callable[[Dict[str, Any]], Dict[str, Any]]
ValidateFn = Callable[[Dict[str, Any]], Tuple[bool, str]]
RepairInputFn = Callable[[Dict[str, Any], str, int], Dict[str, Any]]
FallbackFn = Callable[[Dict[str, Any], str], Dict[str, Any]]
NormalizeFn = Callable[[Dict[str, Any]], Dict[str, Any]]
PersistFn = Callable[[Dict[str, Any], Dict[str, Any]], None]


@dataclass
class SelfHealConfig:
    max_repair_attempts: int = 2
    artifact_type: str = "text"
    filename: str = "artifact.txt"
    encoding: str = "plain"
    mime_type: str = "text/plain"


def _default_normalize(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Asegura estructura mínima del contrato de salida."""
    artifact = payload.get("artifact") or {}
    repair_info = payload.get("repair_info") or {}
    payload["artifact"] = {
        "type": artifact.get("type", "text"),
        "filename": artifact.get("filename", "artifact.txt"),
        "content": artifact.get("content", ""),
        "encoding": artifact.get("encoding", "plain"),
        "mime_type": artifact.get("mime_type", "text/plain"),
    }
    payload["repair_info"] = {
        "auto_repaired": bool(repair_info.get("auto_repaired", False)),
        "repair_attempts": int(repair_info.get("repair_attempts", 0)),
        "repair_reason": str(repair_info.get("repair_reason", "")),
        "max_attempts": int(repair_info.get("max_attempts", 0)),
    }
    return payload


def generate_with_self_heal(
    input_payload: Dict[str, Any],
    generate: GenerateFn,
    validate: ValidateFn,
    enrich_for_repair: RepairInputFn,
    build_fallback: FallbackFn,
    *,
    config: Optional[SelfHealConfig] = None,
    normalize: Optional[NormalizeFn] = None,
    persist_history: Optional[PersistFn] = None,
) -> Dict[str, Any]:
    """
    Ejecuta loop de generación con auto-reparación y contrato estándar.

    El callback `generate` debe retornar un dict con, al menos, `content`.
    """
    cfg = config or SelfHealConfig()
    normalize_fn = normalize or _default_normalize

    attempts = 0
    auto_repaired = False
    repair_reason = ""

    generated = generate(input_payload)
    valid, reason = validate(generated)

    while (not valid) and attempts < cfg.max_repair_attempts:
        attempts += 1
        auto_repaired = True
        repair_reason = reason

        repair_input = enrich_for_repair(input_payload, reason, attempts)
        generated = generate(repair_input)
        valid, reason = validate(generated)

    if not valid:
        auto_repaired = True
        repair_reason = reason
        generated = build_fallback(input_payload, reason)

    payload = {
        "artifact": {
            "type": cfg.artifact_type,
            "filename": cfg.filename,
            "content": generated.get("content", ""),
            "encoding": cfg.encoding,
            "mime_type": cfg.mime_type,
        },
        "repair_info": {
            "auto_repaired": auto_repaired,
            "repair_attempts": attempts,
            "repair_reason": repair_reason,
            "max_attempts": cfg.max_repair_attempts,
        },
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "valid": valid,
        },
    }

    payload = normalize_fn(payload)

    if persist_history:
        persist_history(input_payload, payload)

    return payload