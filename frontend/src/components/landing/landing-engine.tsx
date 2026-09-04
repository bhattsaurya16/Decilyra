export function LandingEngine() {
  return (
    <section className="border-t border-border py-20">
      <div className="mx-auto grid max-w-6xl gap-10 px-4 sm:px-6 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Analytics engine</p>
          <h2 className="mt-3 text-3xl font-medium tracking-tight">Python is the truth engine. SQL is the data engine.</h2>
          <p className="mt-4 text-sm leading-6 text-muted-foreground">
            Calculations live in typed services, not in prompt text. The method registry will govern what may run.
            Pandas, NumPy, SciPy, and statsmodels are reserved for later phases — the foundation already separates
            UI from analysis so those libraries can land in the right place.
          </p>
        </div>
        <div className="rounded-lg border border-border bg-card p-5 font-mono text-xs leading-6 text-muted-foreground">
          <p>Business data</p>
          <p>→ understanding & quality</p>
          <p>→ semantic mapping</p>
          <p>→ method eligibility</p>
          <p>→ deterministic analytics</p>
          <p>→ findings & scenarios</p>
          <p>→ AI explanation</p>
        </div>
      </div>
    </section>
  );
}
