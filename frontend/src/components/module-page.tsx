import { EmptyState } from "@/components/empty-state";

type ModulePageProps = {
  eyebrow: string;
  title: string;
  description: string;
};

export function ModulePage({ eyebrow, title, description }: ModulePageProps) {
  return <EmptyState eyebrow={eyebrow} title={title} description={description} />;
}
