export function LandingScenarios() {
  return (
    <section className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Scenario modeling</p>
        <h2 className="mt-3 text-3xl font-medium tracking-tight">Change the lever. Keep the lineage.</h2>
        <p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground">
          Scenario Lab will clone a validated baseline, apply controlled assumptions, and show what moved. Phase 1
          reserves the route and navigation so modeling does not get bolted on as a separate product later.
        </p>
        <div className="mt-8 grid gap-4 sm:grid-cols-3">
          {["Baseline", "Assumption set", "Delta"].map((label) => (
            <div key={label} className="rounded-md border border-border bg-card px-4 py-5">
              <p className="text-xs uppercase tracking-[0.14em] text-muted-foreground">{label}</p>
              <div className="mt-4 h-16 border border-dashed border-border" />
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
