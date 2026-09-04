export function LandingSecurity() {
  return (
    <section id="security" className="border-t border-border py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">Security / governance</p>
        <h2 className="mt-3 text-3xl font-medium tracking-tight">Governance is a product feature, not a footnote.</h2>
        <ul className="mt-8 grid gap-6 text-sm leading-6 text-muted-foreground sm:grid-cols-3">
          <li>
            <p className="font-medium text-foreground">Method registry</p>
            Catalog of allowed analytical methods and their preconditions.
          </li>
          <li>
            <p className="font-medium text-foreground">Workspace isolation</p>
            Data and settings will be scoped per workspace once authentication lands.
          </li>
          <li>
            <p className="font-medium text-foreground">No secrets in the client</p>
            API keys and database credentials stay in environment configuration.
          </li>
        </ul>
      </div>
    </section>
  );
}
