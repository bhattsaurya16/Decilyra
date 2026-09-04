/**
 * Illustrative dashboard figures for layout only.
 * Replace this module with API-backed series in a later phase.
 */
export type KpiDatum = {
  id: string;
  label: string;
  value: string;
  delta: string;
  tone: "up" | "down" | "neutral";
  helper: string;
};

export type TimeSeriesPoint = {
  month: string;
  value: number;
};

export type DualSeriesPoint = {
  month: string;
  revenue: number;
  profit: number;
};

export type MixPoint = {
  name: string;
  value: number;
};

export const demoKpis: KpiDatum[] = [
  {
    id: "revenue",
    label: "Revenue",
    value: "$4.82M",
    delta: "+6.4%",
    tone: "up",
    helper: "Trailing 12 months · illustrative",
  },
  {
    id: "gross-margin",
    label: "Gross margin",
    value: "41.8%",
    delta: "-1.2 pts",
    tone: "down",
    helper: "vs prior period · illustrative",
  },
  {
    id: "customers",
    label: "Customers",
    value: "12,480",
    delta: "+3.1%",
    tone: "up",
    helper: "Active accounts · illustrative",
  },
  {
    id: "aov",
    label: "Average order value",
    value: "$186",
    delta: "+2.4%",
    tone: "up",
    helper: "Last 90 days · illustrative",
  },
];

export const demoRevenueTrend: TimeSeriesPoint[] = [
  { month: "Oct", value: 342 },
  { month: "Nov", value: 361 },
  { month: "Dec", value: 398 },
  { month: "Jan", value: 355 },
  { month: "Feb", value: 372 },
  { month: "Mar", value: 401 },
  { month: "Apr", value: 416 },
  { month: "May", value: 409 },
  { month: "Jun", value: 438 },
  { month: "Jul", value: 452 },
  { month: "Aug", value: 441 },
  { month: "Sep", value: 468 },
];

export const demoProfitabilityTrend: DualSeriesPoint[] = [
  { month: "Oct", revenue: 342, profit: 128 },
  { month: "Nov", revenue: 361, profit: 134 },
  { month: "Dec", revenue: 398, profit: 141 },
  { month: "Jan", revenue: 355, profit: 119 },
  { month: "Feb", revenue: 372, profit: 126 },
  { month: "Mar", revenue: 401, profit: 148 },
  { month: "Apr", revenue: 416, profit: 151 },
  { month: "May", revenue: 409, profit: 139 },
  { month: "Jun", revenue: 438, profit: 162 },
  { month: "Jul", revenue: 452, profit: 168 },
  { month: "Aug", revenue: 441, profit: 154 },
  { month: "Sep", revenue: 468, profit: 171 },
];

export const demoCustomerGrowth: TimeSeriesPoint[] = [
  { month: "Oct", value: 10840 },
  { month: "Nov", value: 11020 },
  { month: "Dec", value: 11210 },
  { month: "Jan", value: 11180 },
  { month: "Feb", value: 11340 },
  { month: "Mar", value: 11590 },
  { month: "Apr", value: 11740 },
  { month: "May", value: 11880 },
  { month: "Jun", value: 12010 },
  { month: "Jul", value: 12150 },
  { month: "Aug", value: 12320 },
  { month: "Sep", value: 12480 },
];

export const demoProductMix: MixPoint[] = [
  { name: "Platform", value: 38 },
  { name: "Services", value: 24 },
  { name: "Add-ons", value: 18 },
  { name: "Hardware", value: 12 },
  { name: "Other", value: 8 },
];
