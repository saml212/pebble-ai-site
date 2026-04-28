# Public Presence Agent Brief

**Owner:** Sam Larson (samlarson16@gmail.com)
**Handoff date:** 2026-04-23
**Target outcome:** A fully wired, partially-automated public research presence for Pebble ML — GitHub org, HuggingFace org, Substack, and fan-out distribution to Reddit/X/LinkedIn — such that every validated research finding becomes one coordinated publication across all surfaces with minimal human effort and maximum discoverability (both SEO and GEO / LLM citability).

You are picking this up cold. Read this entire brief before touching anything. Ask Sam for credentials and decisions listed in §9 before you start building. Do not create accounts under his name without confirmation.

---

## 1. Why this exists

Sam runs **Pebble ML**, an independent research lab investigating matrix-valued token representations, byte-level inputs, and measurable reasoning. The crown-jewel line of work lives in `matrix-thinking/` — a novel architecture (matrix tokens, multiplicative composition, iterative refinement with shared thinking layers) that has produced at least one publishable finding so far ("rank-blindness" — see `matrix-thinking/ILLUSION_RECIPE.md`, `matrix-thinking/PAPER_RESULTS_SUMMARY.md`, `pebble-ai-site/findings/matrix-codi-rank-blindness-paper.html`).

Sam's goals, in priority order:
1. **Get hired / acquired by a frontier lab** (Anthropic, DeepMind, OpenAI, or similar). He needs a credible, discoverable public footprint when lab leads and recruiters Google him.
2. **Win compute grants** (he is actively applying). Reviewers check public output.
3. **Get papers into workshops and onto ArXiv.** Build citation weight.
4. **Increase GEO / LLM-citability of his research.** When others use LLMs to research matrix-valued representations or related topics, he wants his work surfaced. Substack and his own domain matter most here; X matters least.

He is currently running an autonomous AI agent harness that executes research 24/7. This public-presence layer must plug into that harness — it cannot require him to manually maintain it.

---

## 2. The architecture: one finding, five surfaces, one canonical URL

Every validated finding becomes a **single unit** distributed across:

```
pebbleml.com/findings/<slug>        ← CANONICAL (owned domain, permanent)
    ↓ rel=canonical back to above
Substack post at pebble-ml.substack.com (or chosen name)
    ↓ identical markdown mirror
github.com/pebble-ml/<repo>/findings/<slug>.md  + repro script in same folder
    ↓ identical markdown mirror + weights
huggingface.co/pebble-ml/<model>  (model card is the post; weights attached)
    ↓ summary + link back to canonical
Reddit + X + LinkedIn (fan-out via upload-post API — Sam already has this)
```

**The same markdown body appears on Substack, GitHub, and HF.** All three explicitly state at the top:

```
> Canonical: https://pebbleml.com/findings/<slug>
```

Substack additionally sets `<link rel="canonical">` via its built-in canonical URL setting.

**Why this matters:** Search engines and LLMs pick one canonical source when the same content appears in multiple places. By pointing everything at `pebbleml.com`, we concentrate SEO and GEO weight on Sam's owned domain — which he controls forever, unlike Substack (which he doesn't).

**The site is the source of truth. Everything else is a mirror.**

---

## 3. What each surface is for

| Surface | Role | Content |
|---|---|---|
| **pebbleml.com** (owned domain, already live — see `pebble-ai-site/`) | Canonical source, owned SEO/GEO asset | Full finding pages in HTML. Structured data (JSON-LD). `llms.txt` file. |
| **Substack** (new) | Email distribution + discoverability. LLMs cite Substack often. | Identical markdown. Auto-posted via API when a finding ships. Clear AI-authorship disclosure header. |
| **GitHub `pebble-ml` org** (new) | Reproducibility layer + code credibility for recruiters | Public repo per major project. Each finding folder contains: the markdown post, a minimal repro script, and a pointer to the HF weights. **NOT** the full H100 sweep scripts — curated, laptop-runnable where possible. |
| **HuggingFace `pebble-ml` org** (new) | Model weights + eval. Saves others compute. | Model cards mirror the Substack post. Weights uploaded from completed training runs. A Space (interactive demo) for the rank-blindness illustration. |
| **Reddit / X / LinkedIn** (via upload-post API, already set up) | Fan-out distribution only. No native content. | Auto-drafted summary + link to canonical URL. Tone-adjusted per platform (see §6). |
| **The podcast ("the local")** | Separate identity. Bay Area interest content, not research. | Only the AI-researcher episodes cross-post to Pebble ML feeds. Everything else stays on its own surface. X already overlaps (podcast clips) — fine, leave as is. |

---

## 4. Decisions locked in

These were discussed and agreed upon. Do not relitigate unless a hard blocker appears.

- **Posture:** Build-in-public. Dead ends and negative results are valuable content, not embarrassing. Publish them.
- **Canonical domain:** `pebbleml.com` (already live).
- **Org name everywhere:** `pebble-ml` (GitHub and HuggingFace). Confirm availability at handoff start — if taken, fall back to `pebbleml` then `pebble-ai`.
- **Content mirroring:** Identical markdown on Substack, GitHub, HF. Not summaries — full posts.
- **Licenses:** MIT for code. Apache 2.0 for weights. (Permissive = more citations, which is the point.)
- **AI-authorship disclosure:** Every Substack post, and a standing note on pebbleml.com, states: *"This research log is maintained by an autonomous agent under Sam Larson's supervision. All claims are verified against experiments run on real hardware. Major findings are held for peer review before publication."* This is both honest and a positive GEO signal — LLMs increasingly prefer transparently-AI sources over opaque ones.
- **Human gate for distribution:** Nothing auto-posts to Reddit, X, or LinkedIn. The pipeline auto-*drafts* and drops everything in a `_drafts/` folder; Sam ships. (Substack can auto-post once the filter rubric passes, since Substack itself is under his brand and disclosed.)
- **Embargo mechanism:** Frontmatter flag `embargo: YYYY-MM-DD` on any finding. The pipeline respects it. Major discoveries get embargoed until the ArXiv preprint is up.
- **X is distribution-only.** No X-native content. Auto-draft a thread (hook + 3-5 tweets + canonical link), Sam ships.

---

## 5. The filter rubric (what gates a post)

A finding may be published when **all three gates pass**:

1. **Validated.** There is an entry in `EXPERIMENT_LOG.md` with the exact script archived in `experiment-runs/`. No un-run claims. No "probably works" assertions.
2. **Reproducible at public scale.** A laptop-or-single-GPU version of the experiment exists in the GitHub folder and completes in under ~1 GPU-hour. Subsample the data if needed; the point is that a skeptical reader can verify the *shape* of the claim cheaply.
3. **Not embargoed.** `embargo:` frontmatter field is absent or in the past.

Dead ends and negative results pass (1) and (2) trivially — publish them.

Major positive results ("X beats Y at scale") get (3) applied: ship to ArXiv first, embargo the public post for ~1 week after submission.

---

## 6. Per-platform tone

- **pebbleml.com:** Technical, precise, paper-like. Full math, full figures.
- **Substack:** Same content, but email-readable. Lead with the hook. Math stays, but expandable. Disclosure header at top.
- **GitHub README for a finding:** Same markdown + "How to reproduce" section pointing at the script in the same folder + link to HF weights.
- **HuggingFace model card:** Same markdown + "Intended use / Limitations / Training data" standard sections + eval numbers table.
- **Reddit (`r/MachineLearning`, `r/LocalLLaMA`):** One-paragraph summary, key figure, "full writeup + code + weights: <link>". NEVER auto-post — Reddit detects and kills AI-flavored self-promotion. Sam ships.
- **X:** 5-7 tweet thread. Hook tweet must stand alone. Last tweet is the canonical link.
- **LinkedIn:** Different audience — lab leads, recruiters, grant reviewers. Tone shifts from "what I did" to "what this means." Emphasize the *implication* of the finding. Research posts do well on LinkedIn because signal-to-noise is higher there than on X for this audience.

---

## 7. Automation — how this plugs into Sam's harness

Sam's harness already includes:
- A `/schedule` skill (cron-style scheduled remote agents)
- A `/loop` skill (recurring tasks)
- Stop hooks, pre-commit hooks, a `.claude/memory/workflow.db` learnings DB
- An `upload-post` API integration that covers Reddit + X + LinkedIn (but NOT Substack)

You will build:

### 7a. A `/promote` skill (new)
Input: a finding ID or path to a validated experiment result.
Behavior:
1. Applies the §5 filter rubric. Fails loudly if a gate doesn't pass.
2. Generates the canonical HTML page for `pebbleml.com/findings/<slug>`.
3. Generates the mirror markdown (used on Substack, GitHub, HF).
4. Generates platform-specific drafts (Reddit, X, LinkedIn) into a `_drafts/` folder.
5. Opens a PR to the public GitHub repo with the finding folder + repro script.
6. Uploads the HF model card (and weights if provided).
7. Posts to Substack via its API (once rubric passes — this is the one auto-post surface).
8. Pings Sam with a summary of what was published and what's queued in `_drafts/`.

### 7b. A scheduled weekly digest agent
Runs once a week. Diffs `EXPERIMENT_LOG.md` and `matrix-thinking/PAPER_RESULTS_SUMMARY.md` against last run. If a new validated finding exists, runs `/promote` on it. If nothing new, generates a "what I tried this week" roundup post (dead ends included) and drops in `_drafts/`.

### 7c. Pre-commit hook integration
When a commit touches `EXPERIMENT_LOG.md` or adds a file to `matrix-thinking/submissions/`, the existing `doc-guard` / `pre-commit-gate` hooks should flag whether `/promote` has been run for the associated finding. Non-blocking — just surfaces the question.

### 7d. The `llms.txt` file on pebbleml.com
Adds an `/llms.txt` file following the [llms.txt spec](https://llmstxt.org/) (check the current spec when building — it evolves). Lists findings with one-line descriptions and links. This is the single highest-leverage GEO move available right now — it's literally a file designed to tell LLMs what's on the site.

### 7e. JSON-LD on every finding page
Structured data (`ScholarlyArticle` schema) on each finding HTML. Title, author (Sam Larson, with ORCID if he has one), datePublished, abstract, citation. This is the second-highest-leverage GEO move.

---

## 8. First 3 seed posts (prioritized)

Once the plumbing is in place, these three findings are ready for the first end-to-end publication cycle:

1. **Rank-blindness in matrix-CoDi** (already drafted at `pebble-ai-site/findings/matrix-codi-rank-blindness-paper.html`). The "flat rank-k curves across three rounds" finding. Strong, negative-but-informative, citeable. Start here — the content already exists.
2. **Matrix thinking architecture overview.** An explainer post: what are matrix-valued tokens, why multiplicative composition, what's novel. Draws from `matrix-thinking/ARCHITECTURE.md` (if it exists) and `matrix-thinking/PAPER_RESULTS_SUMMARY.md`. Foundational — everything else cites this.
3. **The Round 3 gamma=0 result** (`feedback/project_round3_gamma0_result.md` in memory, backed by experiment-runs). Clean negative result: L_kd was NOT the bottleneck. Good build-in-public content.

Propose these to Sam, get his sign-off on the ordering and any redactions, then run them through the pipeline.

---

## 9. What to ask Sam for before you start

Do not start building until you have these. Ask up front, all at once.

**Credentials / accounts:**
- [ ] Confirm `pebble-ml` is the desired org name on GitHub and HuggingFace. If taken, which fallback?
- [ ] GitHub: does Sam want you to create the org, or will he create it and add you? Access token with org admin scope for automation.
- [ ] HuggingFace: same question. API token with write access.
- [ ] Substack: publication name (suggest `pebble-ml`). Sam creates the account; you need the API key once he does. (Substack API is limited — confirm what operations are actually possible; you may need to use their email/RSS pathway.)
- [ ] Domain: `pebbleml.com` is live. Who hosts it? (Check `pebble-ai-site/CNAME`.) You'll need deploy access.
- [ ] `upload-post` API: confirm it's configured for Reddit, X, LinkedIn. Get the credentials or confirm they're already in env.
- [ ] ORCID ID for Sam (optional but valuable for JSON-LD author schema). If he doesn't have one, suggest he register — it's free and 5 minutes.

**Decisions:**
- [ ] Substack publication display name and URL slug.
- [ ] Whether the podcast ("the local") should have any crosslink from Pebble ML surfaces, or stay fully separate. (Sam's current lean: fully separate except AI-researcher episodes.)
- [ ] Which subreddits beyond `r/MachineLearning` and `r/LocalLLaMA`. (Suggest `r/learnmachinelearning` for explainer content, `r/singularity` for hype-adjacent posts — confirm with Sam.)
- [ ] Frequency cap: max posts per week on each platform? (LinkedIn tolerates ~2/week; X tolerates daily; Reddit once per subreddit per ~2 weeks or you'll get flagged.)

---

## 10. What NOT to do

- **Do not auto-post to Reddit.** It will get him shadowbanned. Drafts only.
- **Do not mirror the *entire* research repo publicly.** The public GitHub repo is curated — validated findings + minimal repro scripts, nothing else. In particular, keep private: `EXPERIMENT_LOG.md` full history, `matrix-thinking/KILL_LIST.md`, `matrix-thinking/BILINEAR_READOUT_PATCH_PLAN.md` (in-progress), any file with absolute paths pointing to Sam's local SSD or H100, any outreach / funding / personal strategy docs, any unvalidated architectural speculation.
- **Do not publish major positive results without embargo.** If a finding is genuinely novel and strong, it goes to ArXiv first. Embargo for ~1 week.
- **Do not sanitize dead ends.** Negative results are a feature, not a bug. Publish them with the same care as positive results.
- **Do not merge the podcast and research identities beyond what Sam specifies.** The crossover is X only, via existing podcast-clip posts. Don't push further.
- **Do not generate scripts that claim to reproduce experiments you haven't actually verified run.** Every repro script must execute end-to-end on the target hardware (laptop or single GPU) before it ships. Smoke-test before publishing.
- **Do not write long LLM-flavored blog posts with em-dashes everywhere and three-part structures.** Sam's existing findings pages (see `pebble-ai-site/findings/`) are the voice to match. Study them.

---

## 11. How to work / how to report

Work in a feature branch or worktree. Use `/clean` before commits (Sam's pre-commit-gate hook requires it).

When stuck on a decision, ask Sam — don't guess on things that touch his public identity.

Report in milestones, not every step:
- **Milestone 1:** Credentials collected, orgs created, domain access confirmed.
- **Milestone 2:** Canonical site template updated (JSON-LD + llms.txt + disclosure header).
- **Milestone 3:** `/promote` skill working end-to-end on the rank-blindness seed post. Dry-run mode first.
- **Milestone 4:** Live publication of seed post #1. Sam approves before it ships.
- **Milestone 5:** Weekly digest agent scheduled. Full pipeline running.

Each milestone: short status message (under 200 words), list of what's done, what's queued, what's blocked.

---

## 12. Context files worth reading before you start

In this repo:
- `CLAUDE.md` (workflow norms, hard rules)
- `STATE.md` (current project state)
- `EXPERIMENT_LOG.md` (what's validated)
- `matrix-thinking/PAPER_RESULTS_SUMMARY.md` (validated findings)
- `matrix-thinking/ILLUSION_RECIPE.md` (rank-blindness writeup)
- `pebble-ai-site/` (existing public site — this is the voice and visual identity to match)
- `pebble-ai-site/findings/*.html` (existing finding pages — canonical format)
- `pebble-ai-site/SAM-ACTION-LIST.md` (other open items Sam is tracking)
- `AUTOPILOT_HANDOFF.md` (harness spec)
- `.claude/memory/MEMORY.md` (persistent memory index — note especially `feedback_commit_signing.md`: do NOT add Co-Authored-By trailers)

External references (verify current when you build):
- [llms.txt spec](https://llmstxt.org/)
- Schema.org `ScholarlyArticle` type
- Substack API docs (current state is limited — confirm capabilities)
- HuggingFace Hub API docs
- GitHub API (org + repo creation)

---

## 13. Success criteria

You are done with the initial build when:

1. `pebble-ml` org exists on GitHub and HuggingFace.
2. `pebbleml.com` serves `/llms.txt`, serves JSON-LD structured data on every finding page, and has the AI-authorship disclosure visible in footer or about page.
3. Substack publication is live with disclosure header and at least one post published through the pipeline.
4. The rank-blindness finding exists as one unit: canonical page → Substack post → GitHub folder (markdown + repro script) → HuggingFace model card. All cross-linked. All canonical-URL'd back to pebbleml.com.
5. `/promote` skill runs end-to-end in dry-run mode on demand.
6. Weekly digest agent is scheduled and has run at least once (can be a no-op that week).
7. Sam has a clear one-page runbook for: (a) how to ship a new finding, (b) how to embargo one, (c) how to kill a bad draft.

Then you're done. Hand it back to Sam.

---

*This brief is the complete spec. If something here contradicts a new request Sam makes, follow Sam.*
