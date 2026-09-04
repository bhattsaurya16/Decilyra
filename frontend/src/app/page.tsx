import { LandingAsk } from "@/components/landing/landing-ask";
import { LandingCapabilities } from "@/components/landing/landing-capabilities";
import { LandingCta } from "@/components/landing/landing-cta";
import { LandingEngine } from "@/components/landing/landing-engine";
import { LandingFooter } from "@/components/landing/landing-footer";
import { LandingHero } from "@/components/landing/landing-hero";
import { LandingHowItWorks } from "@/components/landing/landing-how-it-works";
import { LandingLineage } from "@/components/landing/landing-lineage";
import { LandingNav } from "@/components/landing/landing-nav";
import { LandingScenarios } from "@/components/landing/landing-scenarios";
import { LandingSecurity } from "@/components/landing/landing-security";
import { LandingWorkflow } from "@/components/landing/landing-workflow";

export default function HomePage() {
  return (
    <div className="bg-background">
      <LandingNav />
      <LandingHero />
      <LandingHowItWorks />
      <LandingWorkflow />
      <LandingCapabilities />
      <LandingEngine />
      <LandingAsk />
      <LandingScenarios />
      <LandingLineage />
      <LandingSecurity />
      <LandingCta />
      <LandingFooter />
    </div>
  );
}
