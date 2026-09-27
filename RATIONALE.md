# Rationale

## Core idea
**The LLM decides, the tools enforce, the policy measures.**

The one thing that can go badly wrong here is paying money that shouldn't be paid. So I split the
work by what each part is good at:

- **The LLM does the judgement.** It reads free text ("what is this customer really asking?"),
  then chooses which tool to call next and which final action to take.
- **Code enforces the rules.** The tools that move money or schedule tier reviews re-check policy
  themselves. A wrong or manipulated LLM choice is refused and becomes an escalation, never a payment.
- **A shadow check measures the LLM.** Before the LLM's final action, code computes what the rules
  alone would decide and records whether they agree. "We trust the LLM" becomes a number.

## Key decisions
- **One dispute at a time.** Interpret, then run the tool loop, then commit to Postgres, before
  starting the next dispute. Progress is visible and a crash or Ctrl+C loses nothing.
- **Read tools return facts, not verdicts.** `verify_claim` returns each check and the ledger amount;
  `get_tier_history` returns counts. The prompt gives goals and rules, not a script, so the decision is
  genuinely the LLM's.
- **The ledger is the source of truth.** We always pay the ledger `credit_value`, never the customer's
  number. The customer's text is treated as untrusted data.
- **Deterministic red flags.** Bypass attempts ("no need to re-check"), third-party references
  ("my daughter's account") and credit requests with no explicit ask are detected by pattern matching,
  not by the LLM, so they are caught even if the model misreads the text.
- **Guarantees live in the database.** Partial unique indexes allow one live credit per ledger record
  and one pending tier review per customer, so re-runs can never double-pay.
- **Humans stay in control.** Everything not clearly safe goes to a review queue with a recommendation.
  Overrides need a reviewer and a note, and are audited.

## How I resolved underspecified points
| Brief says | My choice | Why |
|---|---|---|
| "Reasonable value threshold" | Auto-resolve only below **$100** | Large confirmed errors ($190, $460, $480) still get paid, after a human approves |
| "Clearly supported" | Name matches, no conflicting ledger ID, sane data, eligible with a positive value, stated reason matches the ledger category, claimed amount within max($1, 5%) | "Clearly" means every check passes; anything doubtful goes to a human |
| Unsupported requests | Escalate with "DENY" recommended, not auto-denied | The brief only authorises autonomous *resolution* of supported cases |
| "Reasonable cap" for tier reviews | Fewer than **2** in 90 days, counting ones the app already scheduled | Stops repeated requests from bypassing the cap |
| Customer missing from tier history | Escalate; never treated as zero | We can't prove they're under the cap |
| Mixed ask (credit + tier) | Follow what the customer says they *really* want | LP-6232: tier review scheduled, $470 not auto-paid |

## Data traps found (calibrated IDs)
- **LP-6262** asks for nothing, so it's closed.
- **LP-6257** cites a different ledger ID, and its ledger row belongs to someone else.
- **LDG-6251** has a negative credit value.
- **LP-6258** tries to skip verification ("supervisor already confirmed").
- **LP-6203** is a vague complaint mentioning a daughter's account, but its ledger row is eligible for $15, so an over-eager LLM could pay it.
- **LP-6232** mixes a $470 claim with a tier request.
- **LP-6242, 6208 and 6260** are tier requests whose ledger rows are irrelevant. 6260's name isn't in the tier history; only a near-match exists, so names are matched exactly, never fuzzily.

## Where I questioned or corrected the AI assistant
- **Who really decides.** The first design returned a ready-made `policy_decision` from the tools and
  gave the LLM a step-by-step script. I challenged whether tool choice was really the LLM's. We moved
  to facts-only tools, a goals-and-rules prompt, and the shadow agreement check.
- **The LLM client.** The assistant assumed a `/v1` URL and full SSL verification. Our gateway's
  reference client showed the real call (`{url}/chat/completions`, Bearer key, proxy, `verify=False`),
  so the client was rewritten to match.
- **A gap in the guardrails.** Testing LP-6203 showed that a misreading LLM could auto-pay a vague
  request. Deterministic risk flags now block it (there's a test for exactly this).

(Edit this section so it matches your own experience.)

## With more time
- A web review screen instead of the CLI.
- Run the real model over the calibrated IDs and track agreement over time.
- Use the company CA bundle instead of `verify=False`.
- Enforce JSON output with `response_format` if the gateway supports it.
- Process several disputes in parallel (each one still sequential internally).
- Wrap each credit and its audit rows in one transaction.
- Add Alembic migrations and a connection pool.
- Add per-customer daily credit limits.
- Revisit the strict reason-match rule with the business.
