# Workflow Execution v1

* Goal  
    * Apply `Slide Workflow.md` to `Outline v1.md` while preserving the slide structure already implied by the outline.  
    * This version stays close to the exact sequence and grouping in `Outline v1.md`.  

* Recommended visual system  
    * Palette  
        * **Sea Indigo**  
    * Overall tone  
        * dark, technical, slightly editorial  
        * sparse slides when possible  
        * a few intentionally dense walkthrough slides  
        * recurring mascot / schematic: **potato agent**  
    * Recurring visual rules  
        * the potato agent is a true recurring mascot  
        * it is the same character every time  
        * for the first draft, use a placeholder SVG / crude line drawing  
        * final visual target: Pixar-like, cute, endearing, identifiable, expressive  
        * keep the same lighting / silhouette / proportions across final image generations  
        * vary props / pose / expression, not identity  
        * comic relief is part of the function, but the character should be able to read as dumb, clever, or serious depending on the slide  

* Image-system note  
    * Biggest production dependency: the recurring potato-agent imagery.  
    * Best practice for this deck  
        * define the most complex / final version of the potato agent first  
        * derive simpler variants from that same design  
        * keep the visual language stable across all slides  
    * That means these image variants should all feel like the same character  
        * brain-only computer version  
        * chat-bot version with lips / legs  
        * tool-using version with eyes / hands / toolbelt  
        * software-agent / general version at a computer  
        * dumb cardboard-cutout version  
        * dumb-but-real version  
        * smart version with thick skill manual  
        * mountain ending version  
        * zoomed-out mountain version  
        * iceberg version  

* Slide plan  
    * Slide 1 — Cover  
        * Source: `Cover - English is the programming language of AI workflows.`  
        * Purpose: land the talk title and event context immediately  
        * Type: cover slide  
        * On-slide content  
            * title  
            * O'Reilly event / date  
            * speaker name  
            * O'Reilly logo  
            * John face image  
            * Arcturus logo  
        * Visual concept  
            * strong title-first cover  
            * speaker + event metadata secondary  
        * Asset needs  
            * O'Reilly logo  
            * John image from Arcturus Labs  
            * Arcturus logo  

    * Slide 2 — What will you learn  
        * Source: `What will you learn`  
        * Purpose: establish the three main audience takeaways  
        * Type: intro / promise slide  
        * On-slide content  
            * what an agent really is  
            * why English is now a practical language for AI workflows  
            * how to build modern AI products by iterating from dumb to smart  
        * Production note  
            * tighten these into clean audience-facing promises  
        * Visual concept  
            * clean promise slide  
            * probably no complex image needed  

    * Slide 3 — What an AI agent was in 2023: LLM on the inside  
        * Source: first sub-bullet under `Here's what an AI agent was in 2023`  
        * Purpose: begin the anatomy sequence simply  
        * Type: sequence slide 1  
        * On-slide content  
            * LLM on the inside (text in → text out)  
        * Visual concept  
            * computer-brain / brain-core image  
            * this is the base form for the sequence  

    * Slide 4 — Add the outer user loop: now it’s a chatbot  
        * Source: second sub-bullet under `Here's what an AI agent was in 2023`  
        * Purpose: extend the same visual model by one step  
        * Type: sequence slide 2  
        * On-slide content  
            * while loop around the agent for user input  
            * now you have a chatbot  
        * Visual concept  
            * same base character / object  
            * add lips / legs / wrapper shape  

    * Slide 5 — Add the inner tool loop: now it’s an agent  
        * Source: third sub-bullet under `Here's what an AI agent was in 2023`  
        * Purpose: complete the sequence  
        * Type: sequence slide 3  
        * On-slide content  
            * while loop for tools  
            * can see / act through APIs  
        * Visual concept  
            * same potato character  
            * eyeballs, hands, wrench, toolbelt  

    * Slide 6 — But they sucked  
        * Source: `But they sucked.`  
        * Purpose: explain why early agents were disappointing  
        * Type: contrast / problem slide  
        * On-slide content  
            * lost track after a few tool iterations  
            * wandered off task  
            * state machines / LangGraph constrained them  
        * Visual concept  
            * one strong “agent wandering off course” illustration  
            * or a simple “free agent vs state machine rails” diagram  
        * Production note  
            * this can stay as a single slide  

    * Slide 7 — Coding harnesses made agents useful  
        * Source: `Nevertheless work on the agent progressed...` intro  
        * Purpose: transition from “agents were flaky” to “agent harnesses made them useful”  
        * Type: transition slide  
        * On-slide content  
            * coding agent harnesses improved the situation  
        * Visual concept  
            * probably text-led bridge slide  

    * Slide 8 — Read / Write / Shell made agents powerful  
        * Source: first sub-bullet under `Nevertheless...`  
        * Purpose: explain why coding agents became broadly capable  
        * Type: sequence slide 1  
        * On-slide content  
            * Read  
            * Write  
            * Shell  
            * agents became general because they can create commands and access the internet  
        * Visual concept  
            * potato agent at computer  
            * general’s hat  
            * software / terminal props  

    * Slide 9 — Skills are job descriptions for agents  
        * Source: second sub-bullet under `Nevertheless...`  
        * Purpose: introduce skills conceptually  
        * Type: sequence slide 2  
        * On-slide content  
            * skills serve as a job description for the task  
        * Visual concept  
            * same potato agent  
            * thick instruction manual labeled `Skillz`  

    * Slide 10 — The Christmas Miracle of 2025  
        * Source: third sub-bullet under `Nevertheless...`  
        * Purpose: explain the late-2025 capability jump, especially for coding models and agentic workflows  
        * Type: statement slide  
        * On-slide content  
            * coding models got significantly better  
            * they stayed on target more reliably  
            * longer-horizon coding and agent tasks became much more practical  
            * supporting references should come from late-2025 discussion / blog posts, especially prominent AI bloggers  
        * Research notes  
            * Simon Willison, `2025: The year in LLMs` (Dec 31, 2025) frames 2025 as `the year of agents` and says the real unlock was reasoning + tools, which let models plan multi-step tasks and stay productively on task longer.  
            * Andrej Karpathy, `2025 LLM Year in Review` (Dec 19, 2025) explains that most of 2025's progress came from RLVR / reasoning improvements and describes a real qualitative shift in what models could do on difficult tasks.  
            * Simon Willison, `OpenAI are quietly adopting skills, now available in ChatGPT and Codex CLI` (Dec 17, 2025) is useful supporting evidence that by late 2025, skills were becoming a mainstream packaging format for agent behavior.  
            * Anthropic, `Introducing Claude Opus 4.5` (Nov 24, 2025) is a useful official reference: it explicitly claims major gains in coding, agents, and long-horizon autonomous tasks, including fewer dead ends and better task planning.  
            * Use these as sober evidence for the step change in coding-model quality; keep `Christmas Miracle of 2025` as the spoken, informal label.  
        * Production note  
            * “Christmas Miracle of 2025” is primarily spoken framing; the slide itself should stay more sober  
        * Visual concept  
            * same agent, but visibly more competent / stable  
            * avoid cheesy holiday visuals unless intentionally funny  

    * Slide 11 — You no longer needed the state machine  
        * Source: final roundup note under `Nevertheless...`  
        * Purpose: land the consequence of the capability jump  
        * Type: conclusion slide for the sequence  
        * On-slide content  
            * instructions can now live in the skill  
        * Visual concept  
            * state machine falls away, skill doc remains  

    * Slide 12 — Reflect on the anatomy of the agent  
        * Source: `Reflect on the anatomy of the agent.`  
        * Purpose: recap the anatomy after the historical sequence  
        * Type: schematic slide  
        * On-slide content  
            * same thing as before  
            * better tools  
            * more powerful brain  
        * Visual concept  
            * close-up schematic of same potato agent  
            * labeled components  

    * Slide 13 — The Dawn of Recognition  
        * Source: `The Dawn of Recognition ...`  
        * Purpose: tell the key personal insight story  
        * Type: story / recognition slide  
        * Framing  
            * this is a personal story of technical insight conveyed to the audience  
        * On-slide content  
            * Shawn wrote the crux in English as a skill  
            * thin software wrapper for Zoom API integration  
            * key insight: agents are the runtime, skills are the software, English is the language  
        * Visual concept  
            * funny hacked-together image of you + Shawn + Zoom-ish potato motif  
        * Asset needs  
            * Shawn image reference  
        * Importance  
            * this is a key-point slide and should be visually strong  

    * Slide 14 — Demo intro: the app  
        * Source: `So we've come to the demo...`  
        * Purpose: transition into the concrete example  
        * Type: demo intro slide  
        * On-slide content  
            * job application review app  
            * UI image  
        * Visual concept  
            * screenshot / product image  
        * Spoken support  
            * most of the human-reviewer details are spoken, not necessarily on-slide  
        * Assets available  
            * review queue screenshot  
            * application review page screenshot  

    * Slide 15 — Why this workflow is expensive for humans  
        * Source: spoken bullets under demo intro  
        * Purpose: explain why the workflow is a good fit for AI help  
        * Type: problem-definition slide  
        * On-slide content  
            * reviewers must inspect candidate background  
            * look at LinkedIn  
            * understand candidate role and company  
            * understand target company  
            * this is research-heavy and labor-intensive  
        * Visual concept  
            * likely text-led or supported by the two UI screenshots  
        * Open question  
            * still needs clarification on the exact human-reviewer steps you want emphasized  

    * Slide 16 — Our build sequence  
        * Source: `Our approach to building this is to`  
        * Purpose: introduce the iterative build pattern  
        * Type: sequence intro slide  
        * On-slide content  
            * create the UI  
            * add mock agent  
            * create real dumb agent  
            * update skills to make it smart  
        * Visual concept  
            * pipeline / progression slide  

    * Slides 17–20 — Progressive reveal sequence  
        * Global rule  
            * these should be built as a progressive reveal set  
            * same base layout each time  
            * each slide adds one bullet  
            * each slide updates the illustration  

    * Slide 17 — Create the UI  
        * Source: first sub-bullet under `Our approach...`  
        * Purpose: isolate step 1  
        * Type: sequence slide 1  
        * On-slide content  
            * create the UI  
        * Visual concept  
            * use UI screenshot(s) or stylized app shell  

    * Slide 18 — Add the mock agent  
        * Source: second sub-bullet under `Our approach...`  
        * Purpose: isolate step 2  
        * Type: sequence slide 2  
        * On-slide content  
            * static text, same form factor as final agent  
        * Visual concept  
            * cardboard-cutout potato at a chair  
            * blank / crayon expression  

    * Slide 19 — Add a real but still dumb agent  
        * Source: third sub-bullet under `Our approach...`  
        * Purpose: isolate step 3  
        * Type: sequence slide 3  
        * On-slide content  
            * real agent, not yet skillful  
        * Visual concept  
            * real potato agent, still silly / dumb expression  

    * Slide 20 — Update the skills to make it smart  
        * Source: fourth sub-bullet under `Our approach...`  
        * Purpose: isolate step 4  
        * Type: sequence slide 4  
        * On-slide content  
            * improve skill / instructions  
        * Visual concept  
            * same agent, now clever  
            * thick instruction manual beside it  

    * Slide 21 — Test drive intro  
        * Source: `Let's take it for a test drive.`  
        * Purpose: transition into the code walkthrough / demo logic  
        * Type: demo transition slide  
        * On-slide content  
            * test drive intro only  
        * Visual concept  
            * likely restrained intro slide  
        * Production note  
            * speaker notes later should include exact reproduction steps  

    * Slide 22 — Code walkthrough, sub slide 1  
        * Source: `Sub slide 1`  
        * Purpose: explain dumb review function → first real agent harness  
        * Type: dense code walkthrough slide  
        * On-slide content  
            * dummy review function  
            * request comes in  
            * prompt gets assembled  
            * result gets returned into `service.add_update(...)`  
            * `__init__` contains model / output type / capabilities / instruction  
            * mention modularity / Lego blocks  
            * mention `get_linkedin_profile` custom tool  
        * Visual concept  
            * intentionally word-dense  
            * split layout: bullets on one side, code anchors / labels on the other  
        * Production note  
            * keep dense on purpose  
            * these are detail / click-through slides, not primary presentation slides  
            * links should be GitHub permalinks to current `main` head, not Zed links  

    * Slide 23 — Code walkthrough, sub slide 2  
        * Source: `Sub slide 2`  
        * Purpose: explain how smartness moves into the skill file  
        * Type: dense code walkthrough slide  
        * On-slide content  
            * skill file is where the agent gets smart  
            * screening flow is ordered and debuggable  
            * output is crisply defined  
            * `AIReviewOutput` mirrors the structure in code  
            * `internal_notes` checklist structure  
        * Visual concept  
            * intentionally dense  
            * skill file + output contract + checklist framing  
        * Production note  
            * keep dense on purpose  
            * links should be GitHub permalinks to current `main` head, not Zed links  

    * Slides 24–26 — Staircase ending  
        * Global rule  
            * these must increase in intensity  
            * keep QR codes present across the last 2–3 slides  
            * highlight the relevant code / CTA as the spoken point changes  

    * Slide 24 — Wrap-up: what have we learned  
        * Source: `Wrapup - what have we learned`  
        * Purpose: recap the talk’s main learnings  
        * Type: wrap-up slide  
        * On-slide content  
            * concise takeaway bullets, not slogans  
            * agents aren’t that complicated  
            * agent skills are the new programs  
            * English is their programming language  
            * AI workflows can be built by wrapping the right agent + skill  
        * Visual concept  
            * potato agent standing on top of a mountain with a flag, explorer style  
            * optional schematic inset  
        * Asset needs  
            * QR codes on bottom for  
                * this codebase — `https://github.com/arcturus-labs/talk--agents-are-the-core`  
                * AI product consulting — `https://arcturus-labs.com/#contact-blog`  
                * I build AI product live — `https://www.youtube.com/watch?v=4PVKLcNPyj8&list=PLP7D6wmkiBCA`  
                * O'Reilly Superstream July 23 — `https://learning.oreilly.com/live-events/ai-superstream-ai-harnesses/0642572392017/0642572392000`  

    * Slide 25 — This is only the start  
        * Source: `But this is only the start...`  
        * Purpose: expand from the core pattern into the improvement loop  
        * Type: future-work slide  
        * On-slide content  
            * evaluate workflow quality  
            * generate test and training data  
            * iteratively improve  
            * virtuous cycle  
            * follow me and I’ll show you how  
        * Visual concept  
            * same potato / mountain image, but zoomed out so the mountain is much larger  
            * keep QR codes on screen  

    * Slide 26 — And soon you’ll see there’s even more  
        * Source: `And soon you'll see that there's even more.`  
        * Purpose: end on the inversion / personal agent future  
        * Type: closing vision slide  
        * On-slide content  
            * today: agent at the core of apps  
            * next: your personal agent becomes your interface to apps and the world  
            * upcoming O’Reilly Superstream July 23  
        * Framing  
            * primary emphasis is the future of agents broadly  
            * Superstream remains present as the CTA, but not the main conceptual point  
        * Visual concept  
            * zoom out again: the mountain is actually a large iceberg  
            * vaguely agent-potato-shaped underwater mass  
            * potato still on top with flag  
            * highlight Superstream QR code  

* Slide count summary  
    * This version yields **26 slides** if we preserve the existing structure closely.  
    * That is a lot, but still workable if  
        * several slides are quick visual sequence slides  
        * the demo walkthrough moves briskly  
        * the dense code slides are limited to only the 2 places already intended  

* Notes on places that may eventually compress  
    * most compressible areas if runtime gets tight  
        * Slides 7–11 (`Nevertheless...` sequence)  
        * Slides 17–20 (`Our approach...` sequence)  
        * Slides 24–26 (wrap / future / superstream ending)  
    * But for now, preserving structure is reasonable.  

* Asset checklist implied by this version  
    * Logos / real images  
        * O'Reilly logo  
        * John image  
        * Arcturus logo  
        * Shawn image  
        * UI screenshot(s)  
    * Generated-image families  
        * potato agent base design  
        * 2023 agent sequence variants  
        * coding-agent / general variant  
        * skill-manual variant  
        * dumb mock-agent variant  
        * dumb real-agent variant  
        * smart-agent variant  
        * Shawn + John hacking scene  
        * mountain ending image  
        * zoomed-out mountain image  
        * iceberg image  
    * Utility assets  
        * QR codes for 4 destinations  
            * `https://github.com/arcturus-labs/talk--agents-are-the-core`  
            * `https://arcturus-labs.com/#contact-blog`  
            * `https://www.youtube.com/watch?v=4PVKLcNPyj8&list=PLP7D6wmkiBCA`  
            * `https://learning.oreilly.com/live-events/ai-superstream-ai-harnesses/0642572392017/0642572392000`  
        * GitHub permalinks for code references instead of Zed links  
        * placeholder SVG potato for first draft  

* Recommendation  
    * This structure is workable as-is.  
    * We do **not** need to split any top-level bullet yet.  
    * Hardest production parts now  
        * keeping the potato imagery consistent  
        * preparing the code-reference slides cleanly  
        * clarifying Slide 15’s exact human-reviewer workflow emphasis  
        * gathering real assets and QR codes  

* Summary  
    * `Outline v1.md` can be executed directly into a deck plan.  
    * This `Workflow Execution v1.md` preserves the outline’s structure closely and currently maps to a **26-slide deck** with  
        * a strong historical setup  
        * a visual recurring mascot  
        * a concrete demo arc  
        * two dense walkthrough slides  
        * a staircase ending  
