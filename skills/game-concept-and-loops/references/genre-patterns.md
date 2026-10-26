# Genre patterns and tradeoffs

These are original design heuristics. Select a pattern based on the intended player, production capacity and play context; test the actual game. None of the examples is a retention benchmark or a guaranteed monetisation strategy.

| Genre | Core decision | Session/return structure | Optional rewarded-ad fit | Main tradeoff to test |
|---|---|---|---|---|
| Idle/incremental | Choose a bottleneck to improve, allocate production, decide when to reset | Short planning sessions; offline results; new production or prestige choices | A clearly valued boost, a capped offline bonus or an optional acceleration | Passive income can make active choices irrelevant; boost value can dwarf ordinary play or become meaningless late-game |
| Tower defence | Position or prioritise defences against changing threats | Wave/run outcome; persistent unlocks; new enemy combinations | A bounded recovery or post-run bonus with explicit consequences | Permanent power can conceal weak strategy teaching; revival can erase the challenge that made the run interesting |
| Puzzle | Infer a rule, plan moves, choose when to use information | Complete a level or attempt; advance a puzzle sequence or mastery goal | An optional hint, extra attempt or post-level offer | A hint can remove the satisfying insight; difficulty spikes can feel engineered to sell rescue |
| Casual action | Make a legible timing, movement or risk/reward decision | Short rounds; score/skill goals; variations and cosmetic collection | A limited continue or post-round reward | Too many menus break quick retries; a continue can invalidate a score comparison unless rules account for it |

## Idle/incremental design questions

Define what the player does when production is running. Distinguish a new strategic choice from simply buying the next larger number. Record the clock for production, boosts, timers and offline accrual; a real-time boost and an active-play boost are different products. A prestige reset should explain what is lost, what is retained and what new decision becomes available. Simulate no-ad, occasional-ad and high-engagement profiles before setting reward values.

## Tower defence design questions

Give enemy threats visible counters and enough feedback to explain why a defence failed. Test an uninformed strategy as well as an efficient one; an optimal solver can hide a tutorial problem. Separate path/targeting/upgrade mistakes from insufficient permanent power. Preserve information about damage, threat type and what a different build could change. For long runs, support interruptions and resume behaviour before using duration as a retention objective.

## Puzzle design questions

Define the puzzle's learning sequence: demonstrate, practise, combine, then vary. Include dead-end and solvability checks where applicable. Prefer hint levels that expose useful information without automatically solving the puzzle. If a level is procedural, test the generator across seeds and report invalid or repetitive outcomes. Avoid treating moves left, seconds played and puzzle understanding as interchangeable difficulty measures.

## Casual action design questions

Make hazards, hitboxes, feedback and restart controls legible on the smallest supported phone. Let players distinguish their own error from latency, visual clutter or a control problem. Test whether adding a meta-progression menu helps the target audience or adds friction to the main attraction. Decide whether assisted runs qualify for competitive scores and explain that rule.

## Mixing genres

Write which loop supplies the skill challenge and which supplies long-term goals. Budget the extra menus, content and balancing work. A second progression system should create a useful decision; two overlapping currencies with identical purposes usually add explanation cost without adding much choice.

## Ad fit is a hypothesis

A natural transition creates an opportunity to assess an ad placement; it does not prove that the placement should be used. Compare completion, return behaviour, reward value and cohort revenue in the actual game. Never use an assumed eCPM or ads-per-player rate as evidence that the concept is commercially viable.
