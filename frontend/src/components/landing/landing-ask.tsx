export function LandingAsk() {
  return (
    <section id="ask" className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Ask Decilyra</p>
        <h2 className="mt-3 max-w-2xl text-3xl font-medium tracking-tight">
          Talk to the analysis. Do not outsource the analysis.
        </h2>
        <p className="mt-4 max-w-2xl text-sm leading-6 text-muted-foreground">
          The chat surface is designed to attach evidence, open the underlying method, and launch a scenario. In this
          phase it is a shell — the contract for a later AI provider is already visible in the product.
        </p>
        <div className="mt-8 max-w-xl space-y-2 rounded-lg border border-border bg-card p-4">
          <div className="rounded-md bg-muted px-3 py-2 text-sm">Why did profitability decline?</div>
          <div className="rounded-md border border-border px-3 py-2 text-sm text-muted-foreground">
            Future answers will cite method outputs, not invent a margin path.
          </div>
        </div>
      </div>
    </section>
  );
}
