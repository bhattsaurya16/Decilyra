export type NavItem = {
  href: string;
  label: string;
};

export type NavSection = {
  title: string;
  items: NavItem[];
};

export const appNav: NavSection[] = [
  {
    title: "Overview",
    items: [{ href: "/dashboard", label: "Overview" }],
  },
  {
    title: "Data",
    items: [
      { href: "/data/sources", label: "Sources" },
      { href: "/data/mappings", label: "Field Mapping" },
      { href: "/data/quality", label: "Data Quality" },
    ],
  },
  {
    title: "Analyze",
    items: [
      { href: "/analysis/accounting", label: "Accounting" },
      { href: "/analysis/finance", label: "Finance" },
      { href: "/analysis/sales", label: "Sales" },
      { href: "/analysis/marketing", label: "Marketing" },
      { href: "/analysis/customers", label: "Customers" },
      { href: "/analysis/operations", label: "Operations" },
      { href: "/analysis/statistics", label: "Statistics" },
    ],
  },
  {
    title: "Decisions",
    items: [
      { href: "/findings", label: "Findings" },
      { href: "/scenarios", label: "Scenarios" },
      { href: "/decisions", label: "Decision Lab" },
    ],
  },
  {
    title: "AI",
    items: [{ href: "/chat", label: "Ask Decilyra" }],
  },
  {
    title: "Reports",
    items: [
      { href: "/reports", label: "Executive Report" },
      { href: "/history", label: "Analysis History" },
    ],
  },
  {
    title: "System",
    items: [
      { href: "/methods", label: "Method Registry" },
      { href: "/settings", label: "Workspace Settings" },
    ],
  },
];
