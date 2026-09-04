import { Badge } from "@/components/ui/badge";

type EmptyStateProps = {
  eyebrow: string;
  title: string;
  description: string;
};

export function EmptyState({ eyebrow, title, description }: EmptyStateProps) {
  return (
    <div className="mx-auto flex max-w-xl flex-col items-start gap-4 py-10">
      <Badge variant="outline">{eyebrow}</Badge>
      <div className="space-y-2">
        <h1 className="text-2xl font-medium tracking-tight">{title}</h1>
        <p className="text-sm leading-6 text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}
