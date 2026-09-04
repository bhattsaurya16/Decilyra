"use client";

import { useState, type FormEvent } from "react";
import { ArrowUp, FileSearch, FlaskConical, LineChart } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";

const suggestedQuestions = [
  "Why did profitability decline?",
  "What is driving revenue growth?",
  "Which products need attention?",
  "What changed compared with last month?",
  "What should I investigate next?",
];

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
};

export function AskDecilyraShell() {
  const [draft, setDraft] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  function queuePrompt(text: string) {
    setDraft(text);
  }

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = draft.trim();
    if (!trimmed) return;
    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", content: trimmed },
      {
        id: crypto.randomUUID(),
        role: "assistant",
        content:
          "Ask Decilyra is not connected to an AI provider yet. When wired, answers will cite validated analytics rather than inventing figures.",
      },
    ]);
    setDraft("");
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[minmax(0,1fr)_280px]">
      <div className="flex min-h-[70vh] flex-col rounded-lg border border-border bg-card">
        <div className="border-b border-border px-5 py-4">
          <p className="text-xs uppercase tracking-[0.16em] text-muted-foreground">AI</p>
          <h1 className="mt-1 text-2xl font-medium tracking-tight">Ask Decilyra</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Conversational interface over validated analytical results. No model is connected in Phase 1.
          </p>
        </div>
        <ScrollArea className="flex-1">
          <div className="space-y-4 px-5 py-5">
            {messages.length === 0 ? (
              <div className="rounded-md border border-dashed border-border px-4 py-8 text-sm text-muted-foreground">
                Conversation history will appear here. Suggested questions can be copied into the composer.
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={cn(
                    "max-w-[85%] rounded-md border px-3 py-2 text-sm leading-6",
                    message.role === "user"
                      ? "ml-auto border-border bg-muted"
                      : "border-border bg-background",
                  )}
                >
                  <p className="mb-1 text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
                    {message.role === "user" ? "You" : "Decilyra"}
                  </p>
                  {message.content}
                </div>
              ))
            )}
          </div>
        </ScrollArea>
        <div className="space-y-3 border-t border-border p-4">
          <div className="flex flex-wrap gap-2">
            {suggestedQuestions.map((question) => (
              <button
                key={question}
                type="button"
                onClick={() => queuePrompt(question)}
                className="rounded-full border border-border px-3 py-1 text-xs text-muted-foreground transition-colors hover:bg-muted hover:text-foreground"
              >
                {question}
              </button>
            ))}
          </div>
          <form onSubmit={onSubmit} className="flex items-end gap-2">
            <textarea
              value={draft}
              onChange={(event) => setDraft(event.target.value)}
              placeholder="Ask about a finding, trend, or scenario…"
              rows={2}
              className="min-h-[44px] flex-1 resize-none rounded-md border border-input bg-transparent px-3 py-2 text-sm outline-none focus-visible:ring-2 focus-visible:ring-ring"
            />
            <Button type="submit" size="icon" aria-label="Queue message">
              <ArrowUp />
            </Button>
          </form>
        </div>
      </div>
      <div className="space-y-4">
        <Card>
          <CardHeader>
            <CardTitle>Evidence</CardTitle>
            <CardDescription>Citations and lineage cards will attach to answers here.</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-md border border-dashed border-border px-3 py-6 text-sm text-muted-foreground">
              No evidence yet. Future responses will link methods, inputs, and outputs.
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Actions</CardTitle>
            <CardDescription>Reserved for later wiring. Not active in Phase 1.</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <Button variant="outline" disabled>
              <FileSearch />
              View evidence
            </Button>
            <Button variant="outline" disabled>
              <LineChart />
              Open analysis
            </Button>
            <Button variant="outline" disabled>
              <FlaskConical />
              Run scenario
            </Button>
            <Badge variant="muted">Requires connected analytics</Badge>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
