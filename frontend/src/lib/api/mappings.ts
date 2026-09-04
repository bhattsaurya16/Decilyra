import { apiGet, apiSend } from "@/lib/api/client";
import type { ProfileColumn } from "@/lib/api/datasets";

export type CanonicalField = { id: string; code: string; domain: string; name: string; description: string; expected_data_type: string; expected_grain: string; unit_type: string; entity_type: string; aliases: string[]; active: boolean };
export type MappingStatus = "SUGGESTED" | "CONFIRMED" | "REJECTED" | "UNMAPPED" | "NEEDS_REVIEW";
export type Mapping = { id: string; dataset_version_id: string; source_column_id: string; status: MappingStatus; confidence: number | null; confidence_level: "HIGH" | "MEDIUM" | "LOW" | null; mapping_method: string; evidence: { kind: string; message: string }[]; alternatives: { canonical_field_id: string; code: string; score: number }[]; confirmed_by_user: boolean; grain: string; source_column: ProfileColumn; canonical_field: CanonicalField | null };
export type MappingCollection = { dataset_id: string; dataset_version_id: string; mappings: Mapping[]; summary: { total: number; confirmed: number; needs_review: number; suggested: number; rejected: number; unmapped: number; domains: { domain: string; confirmed_fields: number; catalog_fields: number; status: "PARTIAL" | "MISSING" }[] } };

export const getCanonicalFields = () => apiGet<CanonicalField[]>("/api/v1/canonical-fields");
export const getMappings = (datasetId: string) => apiGet<MappingCollection>(`/api/v1/datasets/${datasetId}/mappings`);
export const suggestMappings = (datasetId: string) => apiSend<MappingCollection>(`/api/v1/datasets/${datasetId}/mappings/suggest`, { method: "POST", body: JSON.stringify({}) });
export const updateMapping = (mappingId: string, status: MappingStatus, canonicalFieldId?: string | null) => apiSend<Mapping>(`/api/v1/mappings/${mappingId}`, { method: "PATCH", body: JSON.stringify({ status, canonical_field_id: canonicalFieldId ?? null }) });
export const confirmMapping = (mappingId: string, canonicalFieldId?: string | null) => apiSend<Mapping>(`/api/v1/mappings/${mappingId}/confirm`, { method: "POST", body: JSON.stringify({ canonical_field_id: canonicalFieldId ?? null }) });
export const rejectMapping = (mappingId: string) => apiSend<Mapping>(`/api/v1/mappings/${mappingId}/reject`, { method: "POST", body: JSON.stringify({}) });
