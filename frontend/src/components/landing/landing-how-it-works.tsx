const steps = [
  {
    n: "01",
    title: "Connect",
    body: "Bring in operational and financial data without forcing a warehouse rewrite on day one.",
  },
  {
    n: "02",
    title: "Understand",
    body: "Profile fields, map meaning, and assess quality before any method is allowed to run.",
  },
  {
    n: "03",
    title: "Analyze",
    body: "Eligible methods execute deterministically in Python. Results are findings, not guesses.",
  },
  {
    n: "04",
    title: "Decide",
    body: "Scenarios, Decision Lab, and Ask Decilyra sit on top of evidence you can inspect.",
  },
];

export function LandingHowItWorks() {
  return (
    <section id="how-it-works" className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">How it works</p>
        <h2 className="mt-3 max-w-xl text-3xl font-medium tracking-tight">A governed path from tables to judgment.</h2>
        <div className="mt-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step) => (
            <div key={step.n} className="space-y-3">
              <p className="font-mono text-xs text-muted-foreground">{step.n}</p>
              <h3 className="text-base font-medium">{step.title}</h3>
              <p className="text-sm leading-6 text-muted-foreground">{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
