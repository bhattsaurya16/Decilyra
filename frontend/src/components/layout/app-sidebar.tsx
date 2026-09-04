"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { PanelLeft } from "lucide-react";

import { BrandMark } from "@/components/brand-mark";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { appNav } from "@/lib/navigation";
import { cn } from "@/lib/utils";

type AppSidebarProps = {
  collapsed: boolean;
  onToggle: () => void;
  onNavigate?: () => void;
};

export function AppSidebar({ collapsed, onToggle, onNavigate }: AppSidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "flex h-full flex-col border-r border-sidebar-border bg-sidebar text-sidebar-foreground transition-[width] duration-200",
        collapsed ? "w-[72px]" : "w-64",
      )}
    >
      <div className={cn("flex h-14 items-center border-b border-sidebar-border px-3", collapsed ? "justify-center" : "justify-between")}>
        <Link href="/dashboard" className="flex items-center gap-2.5" onClick={onNavigate}>
          <BrandMark className="h-7 w-7" />
          {!collapsed ? <span className="text-sm font-medium tracking-tight">Decilyra</span> : null}
        </Link>
        {!collapsed ? (
          <Button variant="ghost" size="icon" onClick={onToggle} aria-label="Collapse sidebar">
            <PanelLeft />
          </Button>
        ) : null}
      </div>
      {collapsed ? (
        <div className="flex justify-center py-2">
          <Button variant="ghost" size="icon" onClick={onToggle} aria-label="Expand sidebar">
            <PanelLeft />
          </Button>
        </div>
      ) : null}
      <ScrollArea className="flex-1">
        <nav className="space-y-5 px-2 py-4">
          {appNav.map((section) => (
            <div key={section.title}>
              {!collapsed ? (
                <p className="mb-1.5 px-2 text-[11px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
                  {section.title}
                </p>
              ) : null}
              <ul className="space-y-0.5">
                {section.items.map((item) => {
                  const active = pathname === item.href;
                  const link = (
                    <Link
                      href={item.href}
                      onClick={onNavigate}
                      className={cn(
                        "flex items-center rounded-md px-2 py-1.5 text-sm transition-colors",
                        collapsed && "justify-center px-0",
                        active
                          ? "bg-accent text-accent-foreground"
                          : "text-muted-foreground hover:bg-muted hover:text-foreground",
                      )}
                    >
                      {collapsed ? item.label.slice(0, 1) : item.label}
                    </Link>
                  );

                  if (!collapsed) {
                    return <li key={item.href}>{link}</li>;
                  }

                  return (
                    <li key={item.href}>
                      <Tooltip>
                        <TooltipTrigger asChild>{link}</TooltipTrigger>
                        <TooltipContent side="right">{item.label}</TooltipContent>
                      </Tooltip>
                    </li>
                  );
                })}
              </ul>
            </div>
          ))}
        </nav>
      </ScrollArea>
    </aside>
  );
}
