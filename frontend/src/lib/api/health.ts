import { apiGet } from "@/lib/api/client";

export type HealthResponse = {
  status: string;
  service: string;
};

export type SystemInfoResponse = {
  service: string;
  version: string;
  environment: string;
  database_configured: boolean;
  api_prefix: string;
};

export function getHealth() {
  return apiGet<HealthResponse>("/api/v1/health");
}

export function getSystemInfo() {
  return apiGet<SystemInfoResponse>("/api/v1/system");
}
