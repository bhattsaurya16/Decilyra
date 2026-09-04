import { DatasetDetailView } from "@/components/data/dataset-detail";

export default async function DatasetPage({ params }: { params: Promise<{ datasetId: string }> }) {
  const { datasetId } = await params;
  return <DatasetDetailView datasetId={datasetId} />;
}
