import { apiGet, apiSend } from "@/lib/api/client";

export type VersionSummary = { id: string; version_number: number; file_size: number; row_count: number; column_count: number; duplicate_row_count: number; created_at: string };
export type DatasetSummary = { id: string; name: string; created_at: string; updated_at: string };
export type Source = { id: string; name: string; source_type: string; original_filename: string; status: string; created_at: string; updated_at: string; dataset: DatasetSummary; latest_version: VersionSummary; quality_issue_count: number };
export type QualityIssue = { id: string; column_name: string | null; code: string; severity: "INFO" | "WARNING" | "ERROR"; message: string; details: Record<string, unknown> };
export type ColumnProfile = { null_count: number; null_percentage: number; unique_count: number; numeric_min: number | null; numeric_max: number | null; numeric_mean: number | null; date_min: string | null; date_max: string | null; sample_values: unknown[] };
export type ProfileColumn = { id: string; name: string; position: number; inferred_type: string; generic_role: string; profile: ColumnProfile };
export type DatasetDetail = { id: string; source_id: string; name: string; source_type: string; original_filename: string; created_at: string; updated_at: string; latest_version: VersionSummary; quality_issue_count: number };
export type VersionDetail = VersionSummary & { columns: ProfileColumn[]; quality_issues: QualityIssue[] };
export type Preview = { dataset_id: string; version_id: string; columns: string[]; rows: Record<string, unknown>[]; limit: number };

export const listSources = () => apiGet<Source[]>("/api/v1/sources");
export const getDataset = (id: string) => apiGet<DatasetDetail>(`/api/v1/datasets/${id}`);
export const getVersion = (datasetId: string, versionId: string) => apiGet<VersionDetail>(`/api/v1/datasets/${datasetId}/versions/${versionId}`);
export const getPreview = (id: string, limit = 50) => apiGet<Preview>(`/api/v1/datasets/${id}/preview?limit=${limit}`);
export function uploadSource(file: File) { const body = new FormData(); body.append("file", file); return apiSend<Source>("/api/v1/sources/upload", { method: "POST", body }); }
