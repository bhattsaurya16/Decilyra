export function LandingLineage() {
  return (
    <section className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Evidence and lineage</p>
        <h2 className="mt-3 text-3xl font-medium tracking-tight">If you cannot trace it, it is not a finding.</h2>
        <p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground">
          Every claim should point back to source fields, mappings, method versions, and outputs. The UI already
          leaves room for evidence cards beside Ask Decilyra and in Decision Lab.
        </p>
      </div>
    </section>
  );
}
