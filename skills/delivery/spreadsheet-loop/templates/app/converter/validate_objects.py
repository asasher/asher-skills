#!/usr/bin/env python3
"""Validate the declared chart/pivot sidecar before compiling an .xlsx.

This module intentionally uses only the Python standard library.  It implements
the small JSON Schema subset used by objects.schema.json, then adds the
snapshot-dependent closure checks that JSON Schema cannot express.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from typing import Any, Optional


SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "objects.schema.json")
_CELL_RE = re.compile(r"^\$?([A-Za-z]{1,3})\$?([1-9][0-9]*)$")
_QUOTED_SHEET_RE = re.compile(r"^'(?:[^']|'')+'$")
_MAX_EXCEL_COLUMN = 16_384  # XFD
_MAX_EXCEL_ROW = 1_048_576


def _json_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def _stable_value(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _validate_schema(value: Any, schema: dict[str, Any], path: str, errors: list[str]) -> None:
    expected = schema.get("type")
    if expected is not None:
        allowed = expected if isinstance(expected, list) else [expected]
        if not any(_json_type_matches(value, item) for item in allowed):
            label = " or ".join(str(item) for item in allowed)
            errors.append(f"{path}: expected {label}, got {type(value).__name__}")
            return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}, got {value!r}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required property {name!r}")

        if schema.get("additionalProperties") is False:
            for name in value:
                if name not in properties:
                    errors.append(f"{path}.{name}: additional property is not allowed")

        for name, child_schema in properties.items():
            if name in value:
                _validate_schema(value[name], child_schema, f"{path}.{name}", errors)

    if isinstance(value, list):
        minimum = schema.get("minItems")
        if isinstance(minimum, int) and len(value) < minimum:
            errors.append(f"{path}: expected at least {minimum} item(s), got {len(value)}")

        if schema.get("uniqueItems"):
            seen_items: dict[str, int] = {}
            for index, item in enumerate(value):
                key = _stable_value(item)
                if key in seen_items:
                    errors.append(
                        f"{path}[{index}]: duplicate item (first at index {seen_items[key]})"
                    )
                else:
                    seen_items[key] = index

        unique_key = schema.get("x-uniqueBy")
        if isinstance(unique_key, str):
            seen_values: dict[str, int] = {}
            for index, item in enumerate(value):
                if not isinstance(item, dict) or unique_key not in item:
                    continue
                key = _stable_value(item[unique_key])
                if key in seen_values:
                    errors.append(
                        f"{path}[{index}].{unique_key}: duplicate value "
                        f"{item[unique_key]!r} (first at index {seen_values[key]})"
                    )
                else:
                    seen_values[key] = index

        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                _validate_schema(item, item_schema, f"{path}[{index}]", errors)

    if isinstance(value, str) and "pattern" in schema:
        pattern = schema["pattern"]
        try:
            matches = re.search(pattern, value) is not None
        except re.error as exc:
            errors.append(f"schema error at {path}: invalid pattern {pattern!r}: {exc}")
        else:
            if not matches:
                errors.append(f"{path}: value {value!r} does not match {pattern!r}")


def validate_objects(objects: dict) -> list[str]:
    """Return objects.json schema errors; an empty list means valid."""
    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as handle:
            schema = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unable to load schema {SCHEMA_PATH!r}: {exc}"]

    if not isinstance(schema, dict):
        return [f"schema {SCHEMA_PATH!r}: expected a JSON object"]

    errors: list[str] = []
    _validate_schema(objects, schema, "$", errors)
    return errors


def _column_number(column: str) -> int:
    number = 0
    for character in column.upper():
        number = number * 26 + (ord(character) - ord("A") + 1)
    return number


def _parse_a1(reference: str) -> tuple[Optional[str], tuple[int, int], tuple[int, int]]:
    if not isinstance(reference, str):
        raise ValueError("must be a string")

    sheet_name: Optional[str] = None
    cell_range = reference
    if "!" in reference:
        sheet_token, cell_range = reference.rsplit("!", 1)
        if not sheet_token or sheet_token != sheet_token.strip():
            raise ValueError("has an invalid sheet qualifier")
        if sheet_token.startswith("'") or sheet_token.endswith("'"):
            if not _QUOTED_SHEET_RE.fullmatch(sheet_token):
                raise ValueError("has an invalid quoted sheet name")
            sheet_name = sheet_token[1:-1].replace("''", "'")
        else:
            if "'" in sheet_token or "!" in sheet_token:
                raise ValueError("has an invalid sheet qualifier")
            sheet_name = sheet_token

    cells = cell_range.split(":")
    if len(cells) not in (1, 2):
        raise ValueError("must contain one cell or one cell range")

    parsed: list[tuple[int, int]] = []
    for cell in cells:
        match = _CELL_RE.fullmatch(cell)
        if not match:
            raise ValueError(f"contains invalid A1 cell {cell!r}")
        column = _column_number(match.group(1))
        row = int(match.group(2))
        if column > _MAX_EXCEL_COLUMN:
            raise ValueError(f"column {match.group(1).upper()} exceeds XFD")
        if row > _MAX_EXCEL_ROW:
            raise ValueError(f"row {row} exceeds {_MAX_EXCEL_ROW}")
        parsed.append((row, column))

    if len(parsed) == 1:
        parsed.append(parsed[0])
    return sheet_name, parsed[0], parsed[1]


def _snapshot_sheets(snapshot: dict, errors: list[str]) -> tuple[set[str], dict[str, str]]:
    sheets = snapshot.get("sheets")
    if not isinstance(sheets, dict):
        errors.append("$.sheets: expected object in snapshot")
        return set(), {}

    order = snapshot.get("sheetOrder")
    if order is None or order == []:
        sheet_ids = list(sheets)
    elif isinstance(order, list):
        sheet_ids = order
    else:
        errors.append("$.sheetOrder: expected array in snapshot")
        return set(), {}

    names: set[str] = set()
    ids: dict[str, str] = {}
    for index, sheet_id in enumerate(sheet_ids):
        if not isinstance(sheet_id, str):
            errors.append(f"$.sheetOrder[{index}]: expected string sheet id")
            continue
        sheet = sheets.get(sheet_id)
        if not isinstance(sheet, dict):
            errors.append(f"$.sheetOrder[{index}]: sheet id {sheet_id!r} is absent from $.sheets")
            continue
        name = sheet.get("name")
        if not isinstance(name, str):
            errors.append(f"$.sheets.{sheet_id}.name: expected string")
            continue
        names.add(name)
        ids[sheet_id] = name
    return names, ids


def _check_reference(
    reference: Any,
    path: str,
    sheet_names: set[str],
    errors: list[str],
    *,
    default_sheet: Optional[str] = None,
    require_sheet: bool = False,
    anchor: bool = False,
) -> None:
    if not isinstance(reference, str):
        return  # The schema validator reports the type error.
    try:
        sheet_name, start, end = _parse_a1(reference)
    except ValueError as exc:
        errors.append(f"{path}: invalid A1 reference {reference!r}: {exc}")
        return

    if anchor and (sheet_name is not None or start != end):
        errors.append(f"{path}: anchor must be one unqualified A1 cell")
        return
    if require_sheet and sheet_name is None:
        errors.append(f"{path}: source range must include a sheet qualifier")
        return

    resolved_sheet = sheet_name or default_sheet
    if resolved_sheet is not None and resolved_sheet not in sheet_names:
        errors.append(f"{path}: referenced sheet {resolved_sheet!r} does not exist in snapshot")


_COUNT_BEFORE_KIND_RE = re.compile(
    r"\b(?P<count>\d+)\s+(?P<kind>charts?|pivots?|macros?|images?|external[_ -]?links?)\b",
    re.IGNORECASE,
)
_KIND_BEFORE_COUNT_RE = re.compile(
    r"\b(?P<kind>charts?|pivots?|macros?|images?|external[_ -]?links?)\s*[:=]\s*(?P<count>\d+)\b",
    re.IGNORECASE,
)


def _normalise_kind(kind: str) -> str:
    normalised = kind.lower().replace("-", "_").replace(" ", "_")
    if normalised.endswith("s"):
        normalised = normalised[:-1]
    return normalised


def _import_gap_errors(objects: dict) -> list[str]:
    note = objects.get("_import_note")
    if not isinstance(note, str):
        return []

    inventory: dict[str, int] = {}
    matched_inventory = False
    for pattern in (_COUNT_BEFORE_KIND_RE, _KIND_BEFORE_COUNT_RE):
        for match in pattern.finditer(note):
            matched_inventory = True
            kind = _normalise_kind(match.group("kind"))
            count = int(match.group("count"))
            inventory[kind] = max(count, inventory.get(kind, 0))

    errors: list[str] = []
    for singular, collection in (("chart", "charts"), ("pivot", "pivots")):
        detected = inventory.get(singular, 0)
        declared_value = objects.get(collection)
        declared = len(declared_value) if isinstance(declared_value, list) else 0
        if detected > declared:
            errors.append(
                f"$._import_note: unresolved import gap: detected {detected} {collection}, "
                f"but only {declared} are re-declared in $.{collection}"
            )

    if not matched_inventory:
        lowered = note.lower()
        mentions_object = re.search(r"\b(charts?|pivots?)\b", lowered) is not None
        signals_gap = re.search(
            r"\b(detected|unresolved|missing|gap|not reconstructed|re-?declar(?:e|ed|ation))\b",
            lowered,
        ) is not None
        if mentions_object and signals_gap and re.search(r"\bnone\b", lowered) is None:
            errors.append(
                "$._import_note: unresolved chart/pivot import gap has no count that can be "
                "matched to re-declarations"
            )
    return errors


def validate_against_snapshot(objects: dict, snapshot: dict) -> list[str]:
    """Return snapshot-dependent reference and closure errors."""
    if not isinstance(objects, dict):
        return ["$: expected object for objects"]
    if not isinstance(snapshot, dict):
        return ["$: expected object for snapshot"]

    errors: list[str] = []
    sheet_names, sheet_ids = _snapshot_sheets(snapshot, errors)

    seen_ids: dict[str, str] = {}
    for collection in ("charts", "pivots"):
        entries = objects.get(collection)
        if not isinstance(entries, list):
            continue
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            object_id = entry.get("id")
            path = f"$.{collection}[{index}].id"
            if isinstance(object_id, str):
                if object_id in seen_ids:
                    errors.append(
                        f"{path}: duplicate object id {object_id!r} "
                        f"(first declared at {seen_ids[object_id]})"
                    )
                else:
                    seen_ids[object_id] = path

    charts = objects.get("charts")
    if isinstance(charts, list):
        for index, chart in enumerate(charts):
            if not isinstance(chart, dict):
                continue
            base = f"$.charts[{index}]"
            declared_sheet = chart.get("sheet")
            sheet_id = chart.get("sheetId")
            if isinstance(sheet_id, str):
                chart_sheet = sheet_ids.get(sheet_id)
                if chart_sheet is None:
                    errors.append(f"{base}.sheetId: referenced sheet id {sheet_id!r} does not exist in snapshot")
            else:
                chart_sheet = declared_sheet
                if isinstance(chart_sheet, str) and chart_sheet not in sheet_names:
                    errors.append(f"{base}.sheet: referenced sheet {chart_sheet!r} does not exist in snapshot")
            _check_reference(
                chart.get("categories"),
                f"{base}.categories",
                sheet_names,
                errors,
                default_sheet=chart_sheet if isinstance(chart_sheet, str) else None,
            )
            values = chart.get("values")
            if isinstance(values, list):
                for value_index, reference in enumerate(values):
                    _check_reference(
                        reference,
                        f"{base}.values[{value_index}]",
                        sheet_names,
                        errors,
                        default_sheet=chart_sheet if isinstance(chart_sheet, str) else None,
                    )
            _check_reference(chart.get("anchor"), f"{base}.anchor", sheet_names, errors, anchor=True)

    pivots = objects.get("pivots")
    if isinstance(pivots, list):
        for index, pivot in enumerate(pivots):
            if not isinstance(pivot, dict):
                continue
            base = f"$.pivots[{index}]"
            sheet_id = pivot.get("sheetId")
            if isinstance(sheet_id, str) and sheet_id not in sheet_ids:
                errors.append(f"{base}.sheetId: referenced sheet id {sheet_id!r} does not exist in snapshot")
            _check_reference(
                pivot.get("source"),
                f"{base}.source",
                sheet_names,
                errors,
                require_sheet=True,
            )
            _check_reference(pivot.get("anchor"), f"{base}.anchor", sheet_names, errors, anchor=True)

    errors.extend(_import_gap_errors(objects))
    return errors


def _sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest(snapshot_path: str, objects_path: str) -> dict:
    """Return raw-file SHA-256 hashes for a snapshot/objects compile pair."""
    return {
        "snapshot_sha256": _sha256_file(snapshot_path),
        "objects_sha256": _sha256_file(objects_path),
    }


def _read_json(path: str, label: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read {label} {path!r}: {exc}") from exc


def main(argv: Optional[list[str]] = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) not in (1, 2):
        print("usage: validate_objects.py <objects.json> [snapshot.json]", file=sys.stderr)
        return 2

    try:
        objects = _read_json(args[0], "objects file")
        snapshot = _read_json(args[1], "snapshot file") if len(args) == 2 else None
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors = validate_objects(objects)
    if snapshot is not None:
        errors.extend(validate_against_snapshot(objects, snapshot))

    for error in dict.fromkeys(errors):
        print(f"ERROR: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
