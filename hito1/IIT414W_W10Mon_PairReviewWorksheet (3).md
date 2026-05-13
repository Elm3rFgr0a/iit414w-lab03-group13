# Pair Review Worksheet — Capstone Hito 1
### IIT414W · Block 5 · Mon May 4, 2026 · 15:45–16:05

> **The point of this exchange is structured scrutiny, not feedback.** Polite reviews are useless. Your job for the next 14 minutes is to find the weakest decision in the partner team's framing and name it concretely. The team being reviewed commits the critique they received to GitHub at 16:00 — public artifact, no escape.

**Reviewing team:** Instructor review
**Reviewed team:** Group 13

---

## How this works (instructor reads aloud at 15:45)

1. **Minutes 1–7:** read the partner team's `framing.md` and look at their dataset-load notebook. Write your answers below to at least 3 of the 5 questions.
2. **Minutes 8–14:** structured conversation. Each team gives the other ONE concrete critique — the strongest one you found. Not three. Not five. ONE that lands.
3. **Minutes 15–18:** each team writes the critique they RECEIVED into their own `framing.md` under section 8 ("Critique Received").
4. **Minute 19:** instructor calls time. Critique-received sections committed to GitHub.

There is no debate phase. The reviewed team writes down the critique, decides whether they agree, and writes a 1-line plan for how they'll address it. The reviewer's job is to deliver the critique, not to defend it.

---

## The Five Required Review Questions

For each question, write a concrete answer based on what you read in the partner team's framing.md. "Looks good" is not a concrete answer. You must give answers to at least 3 of the 5.

### Q1. Does their target match their decision context, or is `is_top10` chosen because it's the easiest binary?

> *Look at their Section 1 (decision context) and Section 2 (target). If their decision is about podiums, is_top10 is too coarse. If their decision is about points generally, is_top10 might be reasonable. Is_top10 is locked for Hito 1, but their framing should still acknowledge if a different target would fit better.*

Concrete answer:

> `is_top10` is reasonable for Hito 1 because their stated decision is about scoring points, and in F1 points begin at P10. However, their concrete scenario uses a P4 starter in a tier-1 constructor, where Top 10 probability may already be high enough that the target will not expose the real conservative-vs-aggressive strategy tradeoff. They should acknowledge that `is_top10` is a locked Hito 1 target, but that `is_top5`, expected points, or finish position may better match the decision value in Hito 2.

---

### Q2. Is their baseline plan F1-defendable? Could they justify it WITHOUT ever seeing 2023–2024 data?

> *Look at their Section 3. Did they describe the baseline based on F1 logic (qualifying → grid → constructor tier → recent form), or did they describe it based on what they think will work on the test set? The first is defendable. The second is contaminated reasoning.*

Concrete answer:

> Mostly yes. `qualifying_position` and `constructor_tier` are defendable pre-race signals from F1 domain logic: starting position and car performance strongly affect point-scoring probability before the formation lap. The risky part is that Section 3 cites Lab 3 performance on the 2023 test season to justify the baseline, which weakens the claim that the baseline was chosen without looking at 2023-2024 outcomes.

---

### Q3. Are their what-if scenarios specific enough to RUN, or are they generic?

> *Look at their Section 4. Do their scenarios have actual feature values (e.g. "n_stops=1, compound_sequence=M-H, stint_lengths=[35, 35]")? Or do they say something vague like "we'll compare 1-stop vs 2-stop strategies"? Generic scenarios cannot be executed against the model on Wednesday.*

Concrete answer:

> Yes, the scenarios are specific enough to run: they define qualifying position, constructor tier, circuit, stop count, compound sequence, and approximate stint lengths. The execution risk is that Section 3 says the baseline uses only `qualifying_position` and `constructor_tier`, while Section 4 varies `n_stops`, `compound_sequence`, and `stint_lengths`; unless the Wednesday model actually includes these strategy variables, the what-if comparison will not change when those values change.

---

### Q4. Which of the five known limitations did they NOT acknowledge that they should have?

> *The five disclosed limitations: (1) coverage starts 2019, (2) qualifying_position is a stand-in, (3) safety_car is binary not interval-counted, (4) strategy features are post-race observations, (5) strategy choice is confounded with car/driver/weather. Look at their Section 5. Which one bites their specific approach but they didn't write down?*

Concrete answer:

> They acknowledge the two most important limitations for their approach: post-race strategy features and confounding. The missing limitation that bites them is that `qualifying_position` is being used as a stand-in for grid position; since their decision is explicitly after qualifying and before the formation lap, they need to state that this is an available proxy but not a true grid-position or qualifying-time signal. They also do not mention 2019-only coverage start, but that is less central to their framing.

---

### Q5. If their model lands at Brier 0.20 on the test set (worse than docent grid-rule 0.208 — close to it but not better), what does their framing currently say to defend that scenario?

> *This is the "what if my model isn't good enough" question. Look at their Section 6 (experiment plan). If their framing doesn't currently have a path for "we did not beat the docent baseline, here's what we'd say," they will be exposed in Demo Day. The strongest framings have a fallback story.*

Concrete answer:

> Their current framing does not defend that scenario strongly enough. It predicts Brier around 0.165-0.18 and says the model should beat the grid-rule baseline, but it does not say what they will conclude if the model lands around 0.20 or fails to beat the calibrated docent model. They need a fallback interpretation: for example, keep the model as a calibrated scenario probe, report that the simple grid/constructor model is not sufficient for recommendation strength, and use Hito 2 targets/error slices to explain where the advisor is unreliable.

---

## The ONE Concrete Critique We Will Deliver

After answering 3+ questions above, decide: which critique is the most important for this team to hear? Write it as one sentence, framed as an observation, not an attack.

**Format:** "Your [section X] doesn't [specific issue]. The consequence is [what happens in Hito 1 or Demo Day]. One thing to do: [concrete action]."

> Your Sections 3-4 do not align the baseline feature set with the what-if variables you plan to vary. The consequence is that Wednesday's scenario comparison may produce no strategy-relevant change, or may rely on post-race features without a clear modeling contract. One thing to do: explicitly define the Hito 1 scenario model features, including `n_stops` and a pre-encoded `compound_sequence`, then add a fallback sentence for what you will conclude if Brier stays near 0.20.

**Example of a strong critique:** "Your Section 4 lists 'compare 1-stop vs 2-stop' but doesn't specify driver, circuit, or compound. The consequence is your Hito 1 won't have an executable what-if — Wednesday's TA can't help with that. One thing to do: pick three rows from the dataset (one driver, one circuit, three n_stops values) and write the specific scenarios in Section 4 before 15:40."

**Example of a weak critique:** "Your framing is good but could be more specific in Section 4."

---

## Notes for Reviewing Team (your records, not committed)

What did you learn from reading their framing that informs your own?

> Their framing is strongest when it separates calibrated probability quality from classification accuracy; Brier Score is correctly connected to strategy confidence instead of only model ranking.

What is one thing they did better than you did?

> They gave concrete, runnable what-if scenarios with actual feature values instead of stopping at a generic "1-stop vs 2-stop" comparison.

---

## After the Exchange

The reviewed team writes the critique they received into their own `framing.md` Section 8 by 16:00. The reviewing team's worksheet is for their own records — keep it as a learning artifact.

Instructor records pair review participation in the session log. Pairs that visibly went through the questions vs pairs that just chatted will be visible from the artifact (the critique-received section).
