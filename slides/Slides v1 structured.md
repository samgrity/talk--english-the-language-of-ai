slides:
  - slide: 1
    kind: cover
    title: "English is the language of AI software."
    eyebrow: "Opening thesis"
    top_notes:
      - "O'Reilly · Zero to Agent · July 15"
      - "Opening frame"
    speaker:
      name: "John Berryman"
      org: "Arcturus Labs"
    assets:
      - "assets/john_berryman_face.jpg"
      - "assets/arcturus_logo.png"
    footer: "Talk thesis first. Everything else follows from it."

  - slide: 2
    kind: promise
    title: "What you'll learn"
    cards:
      - number: "01"
        text: "What an agent really is."
        subtext: "It's actually pretty simple."
      - number: "02"
        text: "Why English is now the language for AI software."
      - number: "03"
        text: "How to incrementally build AI products that actually work."
    footer: "What · Why · How"

  - slide: 3
    kind: sequence
    sequence: "2023 anatomy"
    step: "1/3"
    eyebrow: "What an AI agent was in 2023"
    title: "In the beginning was the LLM."
    emphasis: "Text in -> text out."
    visual: "Base mascot form with brain/computer core"
    footer: "Base form for the recurring mascot sequence"

  - slide: 4
    kind: sequence
    sequence: "2023 anatomy"
    step: "2/3"
    eyebrow: "Add the outer loop"
    title: "Wrap it in a while loop with user input."
    emphasis: "Poof, it's a chat bot."
    visual: "Same mascot with outer user loop"
    footer: "Same character, one added concept"

  - slide: 5
    kind: sequence
    sequence: "2023 anatomy"
    step: "3/3"
    eyebrow: "Add the inner loop"
    title: "Add a tools loop."
    emphasis: "Now it's an agent."
    body:
      - "It can see the world through APIs and act on the world through APIs."
    visual: "Same mascot with tools"
    footer: "The only real difference is the loops and the tools"

  - slide: 6
    kind: problem
    eyebrow: "BUT 2023 AGENTS ACTUALLY SUCKED"
    title: "They were terrible at following instructions."
    left_box:
      title: "Here was the problem"
      bullets:
        - "they would start on the right track"
        - "then get distracted by their own tool output"
        - "or get distracted by examples in the context"
        - "and soon wander off solving a problem you never asked for"
    right_box:
      title: "What we did instead"
      bullets:
        - "constrain the workflow with explicit state machines"
        - "force the processing steps to happen in a fixed order"
        - "use things like LangGraph to keep the model on rails"
    footer: "Technical problem: not enough long-horizon reliability"

  - slide: 7
    kind: transition
    eyebrow: "... but nevertheless"
    title: "Agents lived on in coding harnesses, and improved significantly."
    footer: "This is where agents got practically useful"

  - slide: 8
    kind: sequence
    sequence: "Harness era"
    step: "1/4"
    eyebrow: "Read · Write · Shell"
    title: "Coding agents became general agents."
    body:
      - "Because once an agent can read and write files, and run shell commands, it can then build its own tools and in principle accomplish nearly any online activity."
    visual: "Mascot with computer and general's hat"
    footer: "Read, write, and shell changed the game."

  - slide: 9
    kind: sequence
    sequence: "Harness era"
    step: "2/4"
    eyebrow: "Skills"
    title: "Skills are basically an onboarding manual."
    body:
      - "Once agents became good at files and OS interactions, agent skills were a spectacularly good idea."
    visual: "Mascot with manual labeled Skillz"
    footer: "The procedure becomes data the agent can read"

  - slide: 10
    kind: capability-shift
    top_notes:
      - "Late 2025"
      - "Capability shift"
    eyebrow: "late-2025 capability step change"
    title: "Coding models got much better at long-horizon work in late 2025."
    left_box:
      title: "What changed"
      bullets:
        - "stayed on target longer"
        - "handled ambiguity with less hand-holding"
        - "made fewer dead-end tool decisions"
        - "became much more practical for coding + agent workflows"
    right_box:
      title: "Late-2025 references"
      bullets:
        - "Simon Willison — 2025: The year in LLMs"
        - "Andrej Karpathy — 2025 LLM Year in Review"
        - "Anthropic — Claude Opus 4.5"
    footer: "The Christmas miracle of 2025"

  - slide: 11
    kind: consequence
    eyebrow: "The payoff"
    title: "You don't need bespoke state machine workflows."
    emphasis: "Just place the instructions in the agent skill."
    footer: "This is the turning point"

  - slide: 12
    kind: recap
    eyebrow: "Agent anatomy review"
    title: "The agent is still just an LLM wrapped in a tool loop wrapped in a user loop."
    body:
      - "The real differences: we gave it the right tools, we taught it to read SKILL.md, and we improved the models considerably."
    visual: "Annotated mascot schematic"

  - slide: 13
    kind: story
    eyebrow: "The dawn of recognition"
    title: "In an afternoon of hacking I suddenly realized that English is now the language of AI software."
    body:
      - "We were building a video conferencing assistant just for fun. Shawn took the wheel when we started programming it. He implemented the core of it as a skill to be run by Claude Code. All that was left was a thin wrapper to interface it with a Zoom API."
      - "Then it clicked for me: agents were the runtime, skills were the software, and English was the programming language."
    people:
      - name: "Shawn Simister"
        asset: "assets/shawn_simister.jpg"
      - name: "Nick"
        asset: "assets/nick_chouard.jpg"
      - name: "Me"
        asset: "assets/john_berryman_face.jpg"
    footer: "Agents were the runtime. Skills were the software."

  - slide: 14
    kind: demo-intro
    eyebrow: "So we've come to the demo"
    title: "Let's build a job application review app."
    assets:
      - "assets/review_queue.png"
      - "assets/review_page.png"
    footer: "Applications flow in. Reviewers work them down."

  - slide: 15
    kind: research-problem
    status: "candidate for removal"
    eyebrow: "The expensive part"
    title: "This is cross-source research, not résumé reading."
    left_box:
      title: "What reviewers do"
      bullets:
        - "research the candidate"
        - "research the candidate's current company"
        - "research the hiring company"
        - "compare background against the role"
    right_box:
      title: "Where they look"
      bullets:
        - "LinkedIn"
        - "company websites"
        - "blog posts"
        - "other public sources that prove out fit and honesty"
    footer: "They have to prove out the match, not just skim the application"

  - slide: 16
    kind: approach
    eyebrow: "Here's our approach"
    title: "Build the system in the same shape it will eventually have."
    bullets:
      - "Build the UI"
      - "Connect it to a Mock Agent"
      - "Connect it to a real agent (but not a smart one)"
      - "Make the agent smart"
    visual: "Base mascot"

  - slide: 17
    kind: approach-reveal
    step: "1/4"
    eyebrow: "Here's our approach"
    bullets:
      - "Build the UI"
    assets:
      - "assets/review_queue.png"
      - "assets/review_page.png"

  - slide: 18
    kind: approach-reveal
    step: "2/4"
    eyebrow: "Here's our approach"
    bullets:
      - "Build the UI"
      - "Connect it to a Mock Agent"
    visual: "Mock agent mascot"

  - slide: 19
    kind: approach-reveal
    step: "3/4"
    eyebrow: "Here's our approach"
    bullets:
      - "Build the UI"
      - "Connect it to a Mock Agent"
      - "Connect it to a real agent (but not a smart one)"
    visual: "Real but basic agent mascot"

  - slide: 20
    kind: approach-reveal
    step: "4/4"
    eyebrow: "Here's our approach"
    bullets:
      - "Build the UI"
      - "Connect it to a Mock Agent"
      - "Connect it to a real agent (but not a smart one)"
      - "Make the agent smart"
    visual: "Smarter mascot with skill manual"

  - slide: 21
    kind: walkthrough-intro
    eyebrow: "Let's take it for a test drive"
    title: "Let's take a code tour of the AI application reviewer."
    footer: "The next two slides are intentionally dense and link out to the code"

  - slide: 22
    kind: dense-walkthrough
    eyebrow: "Iterative implementation"
    bullets:
      - "Start w/ simple review function — a good first mock implementation for review would be to sleep briefly and then return a canned follow-up recommendation."
      - "Then add an agent w/ basic skills."
      - "The goal here is just to show how a Pydantic AI agent is put together."
      - "Note, we used PydanticAI build and agent skill."
      - "Whenever the request to review an application comes through, we create a prompt and hand it off to our agent."
      - "So now it's already a little bit smarter: instead of a canned answer, it can read the application context and do the workflow. But the workflow is still basic."
      - "Once the agent responds, it returns structured data that we use to call service.add_update(...)."
      - "The agent implementation itself starts here in __init__."
      - "All we do is specify the model, the output type, the capabilities, and a basic instruction."
      - "One thing that's really interesting is how modular everything is — it all pops in like Lego blocks."
      - "We point it at a bunch of skills with SkillsCapability(...)."
      - "We give it the ability to think with Thinking(...)."
      - "We give it web search with WebSearch()."
      - "You can also easily add tools to these models now. We add get_linkedin_profile because you can't use web search and web fetch to directly get at LinkedIn, so we had to trick it out."
    links:
      - "review mock implementation"
      - "review function"
      - "agent __init__"
      - "get_linkedin_profile"

  - slide: 23
    kind: dense-walkthrough
    eyebrow: "Make your agent smarter"
    bullets:
      - "The skill file is where you actually make the agent smart. These days it's often enough to implement the workflow in English."
      - "The Screening flow lays out an ordered set of steps. For workflows, defined steps make the agent easier to steer and much easier to debug when something goes wrong."
      - "Be crisp about output. The Your output section defines it in English, and AIReviewOutput defines that exact shape in code. PydanticAI enforces this structure as well, so it's a great way to make sure the model returns the required structure."
      - "Also note this line in the skill, where I require internal_notes to conform to its own checklist structure."
    links:
      - "skill file"
      - "screening flow"
      - "your output"
      - "AIReviewOutput"
      - "internal-notes-checklist"

  - slide: 24
    kind: wrap-up
    eyebrow: "Wrap-up"
    title: "Let's review what we've learned."
    bullets:
      - "agents really aren't that complicated"
      - "agent skills are the new programs for AI applications, and English is their programming language"
      - "you can build AI workflows by wrapping the right agent with the right skill"
    visual: "Mascot on mountain peak with flag"
    qr_codes:
      - label: "this codebase"
        asset: "assets/qr_codebase.png"
        highlighted: true
      - label: "AI product consulting"
        asset: "assets/qr_arcturus.png"
      - label: "I build AI product live"
        asset: "assets/qr_live.png"
      - label: "O'Reilly Superstream July 23"
        asset: "assets/qr_superstream.png"

  - slide: 25
    kind: future-work
    eyebrow: "But this is only the start"
    title: "There is much yet to learn."
    bullets:
      - "gathering or generating test and training data"
      - "evaluating the workflow"
      - "establishing a virtuous cycle of iterative improvement"
    visual: "Zoomed-out mountain"
    qr_codes:
      - label: "this codebase"
        asset: "assets/qr_codebase.png"
      - label: "AI product consulting"
        asset: "assets/qr_arcturus.png"
        highlighted: true
      - label: "I build AI product live"
        asset: "assets/qr_live.png"
        highlighted: true
      - label: "Superstream"
        asset: "assets/qr_superstream.png"

  - slide: 26
    kind: closing-vision
    eyebrow: "And soon you'll see there's even more"
    title: "The agent is the core of AI applications. Soon, your personal agent will be the full user experience."
    body:
      - "That's the broader future: not just agentic features, but agentic interfaces to the world around you."
    visual: "Iceberg reveal with mascot on top"
    qr_codes:
      - label: "this codebase"
        asset: "assets/qr_codebase.png"
      - label: "AI product consulting"
        asset: "assets/qr_arcturus.png"
      - label: "I build AI product live"
        asset: "assets/qr_live.png"
        highlighted: true
      - label: "O'Reilly Superstream July 23"
        asset: "assets/qr_superstream.png"
        highlighted: true
