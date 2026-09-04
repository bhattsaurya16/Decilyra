"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState, type DragEvent } from "react";
import { FileSpreadsheet, Loader2, UploadCloud } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { listSources, uploadSource, type Source } from "@/lib/api/datasets";
import { formatBytes, formatDate } from "@/lib/format";

export function SourcesPage() {
  const [sources, setSources] = useState<Source[]>([]); const [loading, setLoading] = useState(true); const [uploading, setUploading] = useState(false); const [error, setError] = useState<string | null>(null); const input = useRef<HTMLInputElement>(null);
  const refresh = useCallback(async () => { try { setSources(await listSources()); setError(null); } catch (err) { setError(err instanceof Error ? err.message : "Could not load sources."); } finally { setLoading(false); } }, []);
  useEffect(() => { void refresh(); }, [refresh]);
  async function upload(file?: File) { if (!file) return; setUploading(true); setError(null); try { await uploadSource(file); await refresh(); } catch (err) { setError(err instanceof Error ? err.message : "Upload failed."); } finally { setUploading(false); if (input.current) input.current.value = ""; } }
  function drop(event: DragEvent<HTMLDivElement>) { event.preventDefault(); void upload(event.dataTransfer.files[0]); }
  return <div className="space-y-6">
    <div><p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">Data</p><h1 className="mt-1 text-2xl font-medium tracking-tight">Sources</h1><p className="mt-1 text-sm text-muted-foreground">Upload CSV data for deterministic schema discovery and quality profiling.</p></div>
    <Card><CardContent className="p-5"><div onDragOver={(event) => event.preventDefault()} onDrop={drop} className="flex flex-col items-center rounded-md border border-dashed border-border px-6 py-10 text-center"><UploadCloud className="h-8 w-8 text-primary"/><p className="mt-3 text-sm font-medium">Drop a CSV file here</p><p className="mt-1 text-xs text-muted-foreground">or choose one from your computer</p><input ref={input} className="hidden" type="file" accept=".csv,text/csv" onChange={(event) => void upload(event.target.files?.[0])}/><Button className="mt-4" variant="outline" disabled={uploading} onClick={() => input.current?.click()}>{uploading ? <Loader2 className="animate-spin"/> : <FileSpreadsheet/>}{uploading ? "Profiling…" : "Choose CSV"}</Button></div>{error ? <p role="alert" className="mt-3 rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive">{error}</p> : null}</CardContent></Card>
    <Card><CardHeader><CardTitle>Connected sources</CardTitle></CardHeader><CardContent>{loading ? <p className="text-sm text-muted-foreground">Loading sources…</p> : sources.length === 0 ? <p className="rounded-md border border-dashed p-6 text-sm text-muted-foreground">No sources yet. Upload a CSV to begin.</p> : <div className="overflow-x-auto"><table className="w-full text-left text-sm"><thead className="border-b text-xs uppercase tracking-wide text-muted-foreground"><tr><th className="pb-3">Source</th><th className="pb-3">Rows</th><th className="pb-3">Columns</th><th className="pb-3">Size</th><th className="pb-3">Status</th><th className="pb-3">Last updated</th></tr></thead><tbody>{sources.map((source) => <tr key={source.id} className="border-b last:border-0"><td className="py-4"><Link className="font-medium text-primary hover:underline" href={`/data/sources/${source.dataset.id}`}>{source.name}</Link><p className="text-xs text-muted-foreground">{source.original_filename}</p></td><td>{source.latest_version.row_count.toLocaleString()}</td><td>{source.latest_version.column_count}</td><td>{formatBytes(source.latest_version.file_size)}</td><td><Badge variant={source.quality_issue_count ? "outline" : "default"}>{source.status}</Badge></td><td className="text-muted-foreground">{formatDate(source.updated_at)}</td></tr>)}</tbody></table></div>}</CardContent></Card>
  </div>;
}
