import { Badge } from "@/components/ui/badge";
import { CustomerGrowthChart } from "@/components/charts/customer-growth-chart";
import { KpiCard } from "@/components/charts/kpi-card";
import { ProductMixChart } from "@/components/charts/product-mix-chart";
import { ProfitabilityTrendChart } from "@/components/charts/profitability-trend-chart";
import { RevenueTrendChart } from "@/components/charts/revenue-trend-chart";
import {
  demoCustomerGrowth,
  demoKpis,
  demoProductMix,
  demoProfitabilityTrend,
  demoRevenueTrend,
} from "@/lib/demo/dashboard";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">Overview</p>
          <h1 className="mt-1 text-2xl font-medium tracking-tight">Workspace snapshot</h1>
        </div>
        <Badge variant="outline">Illustrative demo data</Badge>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {demoKpis.map((kpi) => (
          <KpiCard key={kpi.id} kpi={kpi} />
        ))}
      </div>
      <div className="grid gap-4 xl:grid-cols-2">
        <RevenueTrendChart data={demoRevenueTrend} />
        <ProfitabilityTrendChart data={demoProfitabilityTrend} />
        <CustomerGrowthChart data={demoCustomerGrowth} />
        <ProductMixChart data={demoProductMix} />
      </div>
    </div>
  );
}
