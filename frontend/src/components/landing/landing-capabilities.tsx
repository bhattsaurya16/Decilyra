const capabilities = [
  {
    title: "Domain analysis",
    body: "Accounting, finance, sales, marketing, customers, operations, and statistics — each behind eligibility.",
  },
  {
    title: "Findings, not dashboards alone",
    body: "The product is built to surface claims with support, not only charts without interpretation.",
  },
  {
    title: "Scenario modeling",
    body: "Change assumptions against a known baseline instead of rebuilding a model from scratch.",
  },
  {
    title: "Ask Decilyra",
    body: "A conversational layer that reasons over results the engine already computed.",
  },
];

export function LandingCapabilities() {
  return (
    <section id="capabilities" className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Major capabilities</p>
        <h2 className="mt-3 text-3xl font-medium tracking-tight">Built for operators who have to stand behind the number.</h2>
        <div className="mt-10 grid gap-6 md:grid-cols-2">
          {capabilities.map((item) => (
            <div key={item.title} className="border-t border-border pt-5">
              <h3 className="text-base font-medium">{item.title}</h3>
              <p className="mt-2 text-sm leading-6 text-muted-foreground">{item.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
