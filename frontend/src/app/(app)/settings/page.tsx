import { HealthStatus } from "@/components/health-status";
import { Badge } from "@/components/ui/badge";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-xl space-y-6 py-6">
      <div>
        <Badge variant="outline">System</Badge>
        <h1 className="mt-3 text-2xl font-medium tracking-tight">Workspace settings</h1>
        <p className="mt-2 text-sm leading-6 text-muted-foreground">
          Authentication, members, and workspace preferences are not implemented yet. The API health check below
          confirms that the Next.js app can reach FastAPI.
        </p>
      </div>
      <HealthStatus />
    </div>
  );
}
