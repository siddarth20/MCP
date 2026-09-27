# Loyalty Point Dispute Agent

An AI agent that handles customer disputes about loyalty points. It automatically resolves only the
safe cases (small, clearly supported by the ledger) and sends everything else to a human, with a
recommendation.

**The LLM decides, the tools enforce, the policy measures.**

## What happens to one dispute
1. **Interpret.** The LLM reads the complaint: is it a point credit, a tier review, nothing, or unclear?
2. **Investigate.** The LLM calls tools: look up the ledger record, verify the claim, check tier history.
3. **Act.** The LLM picks one final action: credit, schedule a tier review, close, or escalate.
   The tool refuses anything the policy doesn't allow.
4. **Check.** Code compares the LLM's choice with what the rules alone would do, and records the agreement.
5. **Save.** Everything is written to PostgreSQL before the next dispute starts.

**Example:** LP-6263 says *"System error, please fix my balance."* The ledger confirms $22 owed, so
the agent credits $22 automatically. LP-6228 claims $480; the ledger confirms it, but it's over the
$100 limit, so it's escalated with "approve" recommended.

## Setup
1. Install Python 3.10+ and PostgreSQL 15 (database `refogdb` on localhost:5432).
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in the database and LLM settings. Never submit `.env`.
4. Put the 3 CSVs (and `qa-manifest.json`) in `data/`.
5. Test the LLM connection: `python main.py check-llm`

Tables are created automatically in the `loyalty` schema.

## Run
| Command | What it does |
|---|---|
| `python main.py validate` | Checks the data only |
| `python main.py next` | Resolves the next pending dispute |
| `python main.py resolve LP-6263` | Resolves one specific dispute |
| `python main.py run --step` | Resolves all disputes one at a time, pausing after each |
| `python main.py run` | Resolves all disputes one at a time without pausing |
| `python review.py list --status PENDING_REVIEW` | Shows the human review queue |
| `python review.py show LP-6228` | Shows the full reasoning, LLM steps and actions |
| `python review.py agreement` | Shows how often the LLM matched the policy |
| `python review.py override LP-6228 --action approve_credit --reviewer alice --note "checked"` | Records a human decision |
| `python -m pytest -q` | Runs the tests (in throwaway schemas) |

## Key settings (`.env`)
| Setting | Meaning |
|---|---|
| `LLM_BASE_URL`, `LLM_MODEL`, `LLM_API_KEY` | The in-house gateway (the app calls `{LLM_BASE_URL}/chat/completions`) |
| `LLM_VERIFY_SSL` / `LLM_CA_BUNDLE`, `LLM_PROXY` | The same as `verify` and `proxies` in the reference client |
| `AUTO_RESOLVE_LIMIT_USD` | Auto-credit only below this amount (default 100) |
| `TIER_REEVAL_CAP` | Maximum tier reviews per 90 days (default 2) |
| `AGENT_PLANNER` | `llm` (default: the LLM picks every tool) or `rules` (1 LLM call per dispute, same outcomes) |

Without `LLM_BASE_URL`, a rule-based mock is used, for offline testing only.
