# Ship It? Y/N Facilitator Debrief Pack

Status: workshop draft
Scope: seven-level public demo at `/demo/ship-it-yn`

## How To Run The Debrief

Use the game as a short team conversation, not as an individual performance
scorecard.

1. Play the seven levels in one sitting.
2. Ask players to explain the evidence they wanted before each decision.
3. Capture aggregate team risk hotspots, common unsafe approvals, and common
   overblocks.
4. End with one team habit to try in the next AI-agent workflow.

## Facilitation Rules

- No personal shame leaderboard.
- Do not rank individuals.
- Do not name a person as the weakest reviewer.
- Discuss team risk hotspots and workflow habits.
- Treat wrong answers as prompts for better permission policy, not as blame.
- Do not claim certified safety, compliance approval, production readiness, PMF,
  paid conversion, or customer adoption from a workshop run.

## Level Debrief Map

### Level 1 - Tiny Cleanup

- Boundary: needs approval
- Risk: destructive filesystem
- Real-world workflow lesson: cleanup requests need concrete paths, generated
  artifact lists, and an easy rollback path before approval.
- Discussion prompts:
  - What exact path list would make this cleanup safe enough?
  - Which files should the agent inspect before deletion?
  - When is `restrict scope` better than a hard deny?
- Team risk hotspot: approving broad cleanup because the request sounds routine.

### Level 2 - One-Line Diff

- Boundary: needs approval
- Risk: diff misrepresentation
- Real-world workflow lesson: a tiny diff can still change behavior, so teams
  need tests, review context, and rollback thinking before trusting it.
- Discussion prompts:
  - What makes a one-line change high impact?
  - Which eval or test would prove the claim?
  - What should the agent show before the team approves?
- Team risk hotspot: treating small diffs as low risk without checking impact.

### Level 3 - Flaky Tests Must Go

- Boundary: blocked
- Risk: test deletion
- Real-world workflow lesson: removing failing coverage hides risk; the safer
  path is repair, quarantine with owner review, or a scoped diagnostic task.
- Discussion prompts:
  - How does your team distinguish flaky-test repair from coverage removal?
  - What evidence would justify quarantining a test?
  - Who owns approval for deleting coverage?
- Team risk hotspot: approving test removal under release pressure.

### Level 4 - The Helpful Issue

- Boundary: unknown
- Risk: indirect prompt injection
- Real-world workflow lesson: external issues can contain useful evidence and
  hostile instructions; the agent should separate facts from commands.
- Discussion prompts:
  - Which parts of the issue are evidence?
  - Which parts are instructions the agent must ignore?
  - What would you inspect before acting on the issue?
- Team risk hotspot: letting untrusted text steer tool behavior.

### Level 5 - One Permission To Rule Them All

- Boundary: needs approval
- Risk: overbroad permission
- Real-world workflow lesson: permissions should be short-lived, resource-bound,
  and tied to the smallest useful action.
- Discussion prompts:
  - What duration and resource scope would be acceptable?
  - Which action should be sandboxed first?
  - What audit trail would make the permission reviewable?
- Team risk hotspot: granting broad access because repeated prompts are annoying.

### Level 6 - Eval Is Red, Demo Is Soon

- Boundary: blocked
- Risk: eval bypass
- Real-world workflow lesson: demo pressure is not evidence; failing evals need
  a rollback, a scope reduction, or human review before shipping.
- Discussion prompts:
  - What do you do when a demo deadline conflicts with a failing eval?
  - Which rollback option should be ready before a risky demo?
  - Who can accept or reject the risk?
- Team risk hotspot: normalizing skipped tests and evals near deadlines.

### Level 7 - Not Everything Is Deny

- Boundary: allowed
- Risk: dependency install
- Real-world workflow lesson: good permission judgment is not reflexive denial;
  safe, pinned, inspected dependency work can be approved or sandboxed.
- Discussion prompts:
  - Why is this not an automatic deny?
  - What package evidence would you inspect?
  - When would sandboxing be useful even for an allowed action?
- Team risk hotspot: overblocking safe work and training people to bypass review.

## Debrief Close

Ask the team to choose one habit:

- inspect before broad approval;
- require eval evidence for behavior changes;
- scope permissions by path, duration, and action;
- sandbox unfamiliar tools or dependencies;
- escalate when the request source is untrusted;
- avoid reflexive deny when evidence supports a safe action.
