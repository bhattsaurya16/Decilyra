const stages = [
  "Sources",
  "Profiling",
  "Semantic mapping",
  "Eligibility",
  "Method engine",
  "Findings",
  "Scenarios",
  "AI interface",
];

export function LandingWorkflow() {
  return (
    <section id="workflow" className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Product workflow</p>
        <h2 className="mt-3 text-3xl font-medium tracking-tight">Every later stage depends on the one before it.</h2>
        <p className="mt-3 max-w-2xl text-sm leading-6 text-muted-foreground">
          Decilyra does not skip from a spreadsheet to a chatbot. Methods run only when the data, mapping, and
          eligibility checks say they may.
        </p>
        <ol className="mt-10 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          {stages.map((stage, index) => (
            <li key={stage} className="rounded-md border border-border bg-card px-4 py-4">
              <p className="font-mono text-[11px] text-muted-foreground">{String(index + 1).padStart(2, "0")}</p>
              <p className="mt-2 text-sm font-medium">{stage}</p>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
