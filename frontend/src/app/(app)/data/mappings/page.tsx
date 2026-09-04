import { MappingPage } from "@/components/data/mapping-page";

export default async function FieldMappingPage({ searchParams }: { searchParams: Promise<{ dataset?: string }> }) {
  const { dataset } = await searchParams;
  return <MappingPage initialDatasetId={dataset} />;
}
