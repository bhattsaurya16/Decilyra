from __future__ import annotations

import csv
import io
import math
import re
from dataclasses import dataclass, field
from typing import Any, Literal

import pandas as pd
from pandas.api.types import is_bool_dtype, is_float_dtype, is_integer_dtype

InferredType = Literal["integer", "decimal", "boolean", "datetime", "date", "text", "categorical", "unknown"]
GenericRole = Literal["possible_id", "possible_date", "possible_numeric_measure", "possible_category", "free_text", "unknown"]
Severity = Literal["INFO", "WARNING", "ERROR"]
NULL_TOKENS = {"", "null", "none", "na", "n/a", "nan"}


@dataclass(slots=True)
class ProfileIssue:
    code: str
    severity: Severity
    message: str
    column_name: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ColumnProfile:
    name: str
    position: int
    inferred_type: InferredType
    generic_role: GenericRole
    null_count: int
    null_percentage: float
    unique_count: int
    numeric_min: float | None = None
    numeric_max: float | None = None
    numeric_mean: float | None = None
    date_min: str | None = None
    date_max: str | None = None
    sample_values: list[Any] = field(default_factory=list)


@dataclass(slots=True)
class DatasetProfile:
    dataframe: pd.DataFrame
    columns: list[ColumnProfile]
    issues: list[ProfileIssue]
    duplicate_row_count: int


def _json_value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        value = value.item()
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def _parse_header(content: bytes) -> list[str]:
    text = content.decode("utf-8-sig")
    reader = csv.reader(io.StringIO(text), strict=True)
    try:
        return next(reader)
    except StopIteration:
        return []


def parse_csv(content: bytes) -> tuple[pd.DataFrame, list[str]]:
    if not content or not content.strip():
        raise ValueError("The CSV file is empty.")
    try:
        header = _parse_header(content)
        if not header or all(not name.strip() for name in header):
            raise ValueError("The CSV must contain a header row.")
        frame = pd.read_csv(
            io.BytesIO(content),
            dtype_backend="numpy_nullable",
            keep_default_na=True,
            na_values=list(NULL_TOKENS),
            on_bad_lines="error",
        )
    except (UnicodeDecodeError, csv.Error, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
        raise ValueError("The CSV is malformed or not UTF-8 encoded.") from exc
    return frame, header


def _infer_string(series: pd.Series, name: str) -> tuple[InferredType, GenericRole, pd.Series | None, list[ProfileIssue]]:
    values = series.dropna().astype("string").str.strip()
    issues: list[ProfileIssue] = []
    if values.empty:
        return "unknown", "unknown", None, issues
    lowered = values.str.lower()
    if lowered.isin({"true", "false", "yes", "no", "y", "n"}).all():
        return "boolean", "possible_category", None, issues
    numeric = pd.to_numeric(values.str.replace(",", "", regex=False), errors="coerce")
    numeric_ratio = float(numeric.notna().mean())
    if numeric_ratio >= 0.9:
        if numeric_ratio < 1:
            issues.append(ProfileIssue("invalid_numeric_strings", "WARNING", "Some values could not be parsed as numbers.", name, {"invalid_count": int(numeric.isna().sum())}))
        valid = numeric.dropna()
        inferred: InferredType = "integer" if ((valid % 1) == 0).all() else "decimal"
        return inferred, _role(name, inferred, len(values), int(values.nunique())), numeric, issues
    date_hint = bool(re.search(r"(^|_)(date|time|timestamp|created|updated)(_|$)", name.lower()))
    date_shapes = float(values.str.match(r"^\d{4}[-/]\d{1,2}[-/]\d{1,2}(?:[ T].*)?$|^\d{1,2}[-/]\d{1,2}[-/]\d{4}(?:[ T].*)?$").mean())
    if date_hint or date_shapes >= 0.9:
        date_values = pd.to_datetime(values, errors="coerce", utc=False)
        date_ratio = float(date_values.notna().mean())
        if date_hint and date_ratio < 0.6:
            issues.append(ProfileIssue("date_parsing_issues", "WARNING", "Most values in this date-like column could not be parsed as dates.", name, {"invalid_count": int(date_values.isna().sum())}))
        if date_ratio >= 0.6:
            if date_ratio < 1:
                issues.append(ProfileIssue("date_parsing_issues", "WARNING", "Some values could not be parsed as dates.", name, {"invalid_count": int(date_values.isna().sum())}))
            has_time = any(value.hour or value.minute or value.second for value in date_values.dropna())
            inferred = "datetime" if has_time else "date"
            return inferred, "possible_date", date_values, issues
    unique = int(values.nunique())
    ratio = unique / max(len(values), 1)
    average_length = float(values.str.len().mean())
    inferred = "categorical" if unique <= 50 and ratio <= 0.5 else "text"
    role: GenericRole = _role(name, inferred, len(values), unique)
    if inferred == "text" and ratio > 0.9 and not _looks_like_id(name) and average_length < 80:
        issues.append(ProfileIssue("suspicious_high_cardinality_text", "INFO", "Text values are almost all unique; this may be an identifier.", name, {"cardinality_ratio": round(ratio, 4)}))
    return inferred, role, None, issues


def _looks_like_id(name: str) -> bool:
    lower = name.lower()
    return lower == "id" or lower.endswith("_id") or lower.startswith("id_")


def _role(name: str, inferred: InferredType, count: int, unique: int) -> GenericRole:
    if _looks_like_id(name) or (count > 0 and unique == count and inferred in {"integer", "text"}):
        return "possible_id"
    if inferred in {"date", "datetime"}:
        return "possible_date"
    if inferred in {"integer", "decimal"}:
        return "possible_numeric_measure"
    if inferred == "categorical":
        return "possible_category"
    if inferred == "text":
        return "free_text"
    return "unknown"


def profile_csv(content: bytes) -> DatasetProfile:
    frame, raw_header = parse_csv(content)
    issues: list[ProfileIssue] = []
    duplicate_names = sorted({name for name in raw_header if raw_header.count(name) > 1})
    if duplicate_names:
        issues.append(ProfileIssue("duplicate_column_names", "ERROR", "Duplicate column names were renamed during parsing.", details={"columns": duplicate_names}))
    if frame.empty:
        issues.append(ProfileIssue("empty_dataset", "ERROR", "The dataset contains no data rows."))
    duplicate_rows = int(frame.duplicated().sum())
    if duplicate_rows:
        issues.append(ProfileIssue("duplicate_rows", "WARNING", f"{duplicate_rows} duplicate row(s) detected.", details={"count": duplicate_rows}))
    columns: list[ColumnProfile] = []
    row_count = len(frame)
    for position, name in enumerate(frame.columns):
        series = frame[name]
        null_count = int(series.isna().sum())
        null_percentage = round((null_count / row_count * 100) if row_count else 0.0, 2)
        unique_count = int(series.nunique(dropna=True))
        parsed: pd.Series | None = None
        column_issues: list[ProfileIssue] = []
        if series.dropna().empty:
            inferred, role = "unknown", "unknown"
            issues.append(ProfileIssue("empty_column", "ERROR", "Column contains no values.", str(name)))
        elif is_bool_dtype(series.dtype):
            inferred, role = "boolean", "possible_category"
        elif is_integer_dtype(series.dtype):
            inferred, role = "integer", _role(str(name), "integer", row_count - null_count, unique_count)
            parsed = pd.to_numeric(series, errors="coerce")
        elif is_float_dtype(series.dtype):
            inferred, role = "decimal", _role(str(name), "decimal", row_count - null_count, unique_count)
            parsed = pd.to_numeric(series, errors="coerce")
        else:
            inferred, role, parsed, column_issues = _infer_string(series, str(name))
        issues.extend(column_issues)
        non_null_count = row_count - null_count
        if row_count and null_percentage >= 50:
            issues.append(ProfileIssue("high_missingness", "WARNING", f"{null_percentage}% of values are missing.", str(name), {"null_percentage": null_percentage}))
        if non_null_count > 1 and unique_count == 1:
            issues.append(ProfileIssue("single_value_column", "INFO", "Column contains only one distinct value.", str(name)))
        if series.dtype == object or str(series.dtype).startswith("string"):
            kinds = set()
            for value in series.dropna().astype(str):
                kinds.add("number" if pd.notna(pd.to_numeric(value, errors="coerce")) else "text")
            if len(kinds) > 1 and not any(item.code in {"invalid_numeric_strings", "date_parsing_issues"} for item in column_issues):
                issues.append(ProfileIssue("mixed_data_types", "WARNING", "Column contains mixed numeric and text values.", str(name)))
        numeric_min = numeric_max = numeric_mean = None
        date_min = date_max = None
        if inferred in {"integer", "decimal"} and parsed is not None and parsed.notna().any():
            numeric_min, numeric_max, numeric_mean = map(float, (parsed.min(), parsed.max(), parsed.mean()))
        if inferred in {"date", "datetime"} and parsed is not None and parsed.notna().any():
            date_min = parsed.min().isoformat()
            date_max = parsed.max().isoformat()
        samples = [_json_value(value) for value in series.dropna().drop_duplicates().head(5).tolist()]
        columns.append(ColumnProfile(str(name), position, inferred, role, null_count, null_percentage, unique_count, numeric_min, numeric_max, numeric_mean, date_min, date_max, samples))
    return DatasetProfile(frame, columns, issues, duplicate_rows)
