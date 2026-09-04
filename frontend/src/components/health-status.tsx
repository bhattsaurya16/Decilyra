"use client";

import { useEffect, useState } from "react";

import { getHealth } from "@/lib/api/health";
import { cn } from "@/lib/utils";

type Status = "checking" | "ok" | "error";

export function HealthStatus({ compact = false }: { compact?: boolean }) {
  const [status, setStatus] = useState<Status>("checking");
  const [detail, setDetail] = useState("Checking API");

  useEffect(() => {
    let cancelled = false;

    getHealth()
      .then((payload) => {
        if (cancelled) return;
        if (payload.status === "ok") {
          setStatus("ok");
          setDetail(payload.service);
        } else {
          setStatus("error");
          setDetail("Unexpected response");
        }
      })
      .catch(() => {
        if (cancelled) return;
        setStatus("error");
        setDetail("API unreachable");
      });

    return () => {
      cancelled = true;
    };
  }, []);

  const color =
    status === "ok" ? "bg-emerald-500" : status === "error" ? "bg-destructive" : "bg-muted-foreground/50";

  if (compact) {
    return (
      <span className="inline-flex items-center gap-2 text-xs text-muted-foreground" title={detail}>
        <span className={cn("h-1.5 w-1.5 rounded-full", color)} />
        {status === "ok" ? "API" : status === "error" ? "API offline" : "API"}
      </span>
    );
  }

  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <p className="text-xs font-medium uppercase tracking-[0.14em] text-muted-foreground">API health</p>
      <div className="mt-2 flex items-center gap-2">
        <span className={cn("h-2 w-2 rounded-full", color)} />
        <p className="text-sm">{detail}</p>
      </div>
      <p className="mt-2 text-xs text-muted-foreground">
        Development check against <code className="font-mono">GET /api/v1/health</code>.
      </p>
    </div>
  );
}
