# Manifest

**Design:** the LLM decides, the tools enforce, the policy measures. Disputes are resolved one at a
time, and each is committed to PostgreSQL before the next starts.

## Flow per dispute
```
main.py ──> agent.process_dispute(dispute)
             1. llm.interpret()            LLM reads the text -> intent, reason, amount
                sanitize_interpretation()  code grounds the output + computes risk flags
             2. loop (max 8 steps):
                  llm.next_step()          LLM picks the next tool
                  tools.<tool>()           tool runs; write tools re-check policy
                  (before the final action: policy.reference_decision() -> shadow check)
             3. db.finalize_decision()     reasoning, trace, agreement, status saved
```

## Agent and orchestration
| File | What it does |
|---|---|
| `agent.py` | `process_dispute`: interpretation, the bounded tool loop (the LLM picks every tool), shadow policy check, forced escalation if no safe action is reached, reasoning builder. `iter_resolve` yields results one at a time. |
| `llm.py` | `InHouseLLM`: `requests` client for the LiteLLM gateway (Bearer key, proxy, timeout, SSL verify / CA bundle, retries, no retry on 4xx, token stats, Qwen `<think>` stripping). `sanitize_interpretation`: validates and grounds LLM output, adds risk flags. `MockLLM` and `RulePlanner`: offline and deterministic alternatives. |
| `prompts.py` | `INTERPRET_SYSTEM` (strict JSON, untrusted input) and `AGENT_SYSTEM` (goals and rules, limit and cap injected). |

## Tool definitions (`tools.py`)
| Tool | Type | Guardrail |
|---|---|---|
| `get_ledger_record(ledger_id)` | read | — |
| `verify_claim()` | read, facts only | needs the ledger lookup first; always verifies the dispute's own record |
| `get_tier_history()` | read, facts only | the dispute's own customer only; adds reviews the app already scheduled |
| `issue_credit(amount_usd)` | write | re-checks policy; amount must equal the ledger value; DB unique index |
| `schedule_tier_reevaluation()` | write | re-checks the tier policy; one pending review per customer |
| `escalate_to_human(reason, recommended_action)` | write | recommendation limited to an allow-list |
| `close_no_action(reason)` | write | only when the customer needs nothing |

## Business rules
| File | What it does |
|---|---|
| `policy.py` | `verify_claim` (the ordered checks), `decide_credit`, `decide_tier`, `decide_no_action` (enforced by the write tools), `reference_decision` and `classify_agreement` (shadow check). |
| `config.py` | All thresholds and settings: $100 limit, amount tolerance, tier cap 2 per 90 days, step limits, LLM and Postgres settings. Loads `.env`. |

## Persistence (`db.py`, PostgreSQL 15, schema `loyalty`)
| Table | Holds |
|---|---|
| `requests` | Each dispute as received |
| `decisions` | Interpretation, verification, full trace, reasoning, LLM-vs-policy `shadow` and `agreement`, status (JSONB) |
| `actions` | Credits, reversals, escalations, closures (who, amount, status) |
| `tier_reevaluations` | Scheduled tier reviews |
| `overrides` | Human overrides with reviewer and note |
| `tool_calls` | Every tool call with arguments and result |

Guarantees in the database: CHECK constraints on statuses; one live credit per ledger record; one
pending tier review per customer; override notes can't be empty.

## Ingestion and interfaces
| File | What it does |
|---|---|
| `data_loader.py` | Loads the 3 CSVs, checks columns and types, detects duplicate ledger IDs, runs the foreign-key check from `qa-manifest.json`. |
| `main.py` | `validate`, `check-llm`, `next`, `resolve <ids>`, `run [--step]`. |
| `review.py` | `list`, `show`, `agreement`, `override`. |

## Tests
| File | What it does |
|---|---|
| `tests/test_agent.py` | 37 tests: all 13 calibrated IDs, idempotency, overrides, sanitisation, risk flags, the real HTTP client, and good, reckless and overcautious model behaviour (the reckless model pays nothing). |
| `tests/fake_llm_server.py` | An OpenAI/LiteLLM-compatible fake gateway for end-to-end tests. |
