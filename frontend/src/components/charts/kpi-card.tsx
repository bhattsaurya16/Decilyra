import { Card, CardContent } from "@/components/ui/card";
import type { KpiDatum } from "@/lib/demo/dashboard";
import { cn } from "@/lib/utils";

export function KpiCard({ kpi }: { kpi: KpiDatum }) {
  return (
    <Card>
      <CardContent className="p-5">
        <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground">{kpi.label}</p>
        <div className="mt-3 flex items-end justify-between gap-3">
          <p className="font-mono text-2xl tracking-tight">{kpi.value}</p>
          <span
            className={cn(
              "text-xs",
              kpi.tone === "up" && "text-emerald-700 dark:text-emerald-400",
              kpi.tone === "down" && "text-destructive",
              kpi.tone === "neutral" && "text-muted-foreground",
            )}
          >
            {kpi.delta}
          </span>
        </div>
        <p className="mt-2 text-xs text-muted-foreground">{kpi.helper}</p>
      </CardContent>
    </Card>
  );
}
