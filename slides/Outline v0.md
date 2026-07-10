
Keep it FAST paced

* Intro  
    * Who am I  
    * What will you learn  
        * Really solid pattern for building AI product in 2026  
        * ??? need 3 even learnings - that link it back to English  
* The way things were - 2025, building things w/ LangGraph  
* Discovery  
    * Sinister hack  
        * you can program in English! - you just need a shim in traditional code  
        * you can now implement workflows in skills b/c of the AI Christmas miracle of 2025  
    * MaterialLabs whatever project  
        * wow, it really works, and the benefit is that the subject matter experts can read and even correct the content  
    * The new AI product  
        * LLM on the inside (brain)  
        * While loops of LLM+user (talking head)  
        * While loop around tools (body w/ hands and eyes)  
        * tools or read/write/edit/bash basically generate a completely capable agent  
        * agent skills  
* The build out  
    * We're going to build out a version of that clientwork.  
    * Here's the approach  
        * Build the UI  
        * Add in a zombie (just performs the function)  
        * Build the agent - with dumb brains (basic skills)  
        * Add smart brains  
            * have an LLM extract the steps from the SME discussion of the steps  
            * point out some structure to the file and why it's important (evaluation of particular steps)  
            * point out how we lead the agent in this case to match structure expected  
    * Do that  
        * Describe UI and explain the application itself  
            * Job application review app.  
            * Human reviewers go through these steps: ?????  
            * We want an AI to gather the research and recommend instead.  
        * Test drive  
            * Review Doug  
            * Monitor it via scripts/navigate_traces.py  
        * We just need to connect a new automated review process to it  
            * the review function (and signature)  
            * the hooks that dump into it (upon user message, or when AI is summoned)  
                * A [recruiter-driven update that sets `should_trigger_ai_review`](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/application_service.py:212) calls `review`.  
                * An [ingested candidate message](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/application_service.py:306) calls `review`.  
                * The [trigger-ai-screen hook](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/api/routes/hooks.py:24) flows into [the service method that calls `review`](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/application_service.py:321).  
        * Making it smart  
            * Note at the top: we used the Pydantic AI skill here while building this, which made it much easier to get the agent doing the right thing immediately.  
            * Start w/ dumb review function – A [good first dummy implementation for `review`](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/ai_reviewer.py:130) would be to sleep briefly and then return a canned follow-up recommendation.  
            * Then add an agent w/ dumb skills  
                * The goal here is just to show how a Pydantic AI agent is put together. 
                * Note, we used PydanticAI build and agent skill
                * Whenever the request to review an application comes through, we [create a prompt and hand it off to our agent](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/ai_reviewer.py:154).  
	                * So now it's already a little bit smarter: instead of a canned answer, it can read the application context and do the workflow.  But the workflow is dumb.
	                * Once the agent responds, it returns structured data that we use to call `service.add_update(...)`.  
                * The [agent implementation itself starts here in `__init__`](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/ai_reviewer.py:89).  
                    * All we do is specify the model, the output type, the capabilities, and a basic instruction.  
                    * One thing that's really interesting is how modular everything is - it all pops in like Lego blocks.  
                    * We point it at a bunch of skills with `SkillsCapability(...)`.  
                    * We give it the ability to think with `Thinking(...)`.  
                    * We give it web search with `WebSearch()`.  
	            * You can also easily add tools to these models now. We add [`get_linkedin_profile`](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/ai_reviewer.py:106) because you can't use web search and web fetch to directly get at LinkedIn, so we had to trick it out. 
            * Make your agent smarter  
                * The [skill file](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:1) is where you actually make the agent smart. These days it's often enough to implement the workflow in English.  
                * The [Screening flow](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:54) lays out an ordered set of steps. For workflows, defined steps make the agent easier to steer and much easier to debug when something goes wrong.  
                * Be crisp about output. The [Your output section](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:16) defines it in English, and [AIReviewOutput](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/ai_reviewer.py:60) defines that exact shape in code.  PydanticAI enforces this structure as well, so it's a great way to make sure the model returns the required structure.
                * [Also not this line in the skill](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:20), where I require `internal_notes` to conform to its own checklist structure. See [internal-notes-checklist.md](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/references/internal-notes-checklist.md:1).  
* Wrapup  
    * Restate learnings  
        * Steps:  
            * Create UI/UX that has hooks out into whatever the agent will do  
            * Make a really dumb version first (no AI)  
            * Make a dumb AI version  
                * AI is composed of little pieces  
            * Iteratively make the AI smarter  
                * Add more pieces and approaches as needed  
                    * FileSystem - for complicated workflows, have it keep track of them in a file with a checklist of todos that it is required to update  
                    * Sandbox - safety  
                    * Other Tools (like LinkedIn)  
        * Applicability - Any place where you want human judgement, especially around text, voice, or image processing.  
            * Backend workflows.  
            * AI Search and Research.  
            * ??????? Moar!  
        * Gotchas  
            * Latency  
            * Cost  
            * Non-determinism  
    * Broader discussion  
        * how to iteratively evaluate and improve - "the virtuous cycle"  
        * eventually have the AI not just recommend but actually do the next step - if it's accurate enough and if it's not "risky"  
    * We're just getting warmed up  
        * logical follow-on from this where I turn this inside out (add horrible picture of agent turned inside out) - rather than stick an agent inside of an app, make the agent the UX that helps you operate any app - Rook and "unharnessing the agent"  
        * Advertise super stream (QR Code?)
        * Advertise Rook and Arcturus Labs (blog) using QR Codes

