I don't know when your training cutoff is, but if you don't understand any of the terms here ask me about them and I'll tell you which ones you should look up. 

Also, you can see where I'm incorporating instructions for pictures that I want. We'll deal with that too. One thing that will be challenging is that we have to have consistent imagery. So I want us to think through all of the images and make sure that we're coming up with something that's going to look appropriate in the end. We'll probably make the most complicated version of the image first and then dim it down for the easier versions. 

- Cover - English is the programming language of AI workflows.
	- Event: O'Reilly "Zero to Agent" July 15 {include O'Reilly logo}
	- Speaker: John Berryman {include image of johns face from https://arcturus-labs.com/ and arcturus logo} 
* What will you learn  
	* What an agent really is. (hint it's simpler than you think )
	* Why English is now the programming language of AI applications. 
	* How to build general AI products that take advantage of the state of the art. 
* Here's what an AI agent was in 2023 (this can be presented as a series of slides that keep the exact same format and introduce the text and images as of the sub-bullets )
	* LLM on the inside (text in - text out) {picture of computer brain thing}
	* There's a while loop around the agent that gets user input and puts it into the prompt. Now you have a chat bot. {image of potato-like thing that wraps the LLM brain and has talking lips and legs}
	* Simply stick a while loop inside of that which still wraps the LLM and it calls tools and incorporates that text into the prompt. Now you have an agent that can see the world around it through APIs and interact with the world through APIs {Take the same potato-y image and put eyeballs on it and give it hands with wrenches and a toolbelt}
* But they sucked. Agents weren't very good because in about four or five tool iterations it lost track of what it was doing and was doing its own thing. They had worse ADHD than me. So instead, we resorted to using state machines to control the processing steps in complicated workflows so that the agent couldn't get off course - things like LangGraph {Maybe there's a good illustration here.}
* Nevertheless work on the agent progressed in the form of coding agent harnesses. (again, multi-slides that follow same layout and introduce a bullet each)
	* Agents were given tools that made them really good at software specifically. Read (Reading a file.), Write (Writing a file.), and Shell (Running shell commands.). And because an agent, in principle, can create their own commands and access anything on the internet, this made them general agents. {And the potato image from before - replace the tools with a computer that the potato is using and then give him a general's hat like something that maybe looks like a revolutionary general. }
	* Because agents were trained to be so good with file and operating system interactions, the introduction of agent skills was an obvious good fit. Skills basically serve as a job description for the task to be done. {Place a thick instruction manual labeled "Skillz" next to the agent Potato.  } 
	* Then came the "Christmas Miracle of 2025" – Several AI news sources and bloggers independently started reporting that something happened with the new models that were out at around that time. They were suddenly significantly better. The agents no longer wandered around when you gave them a task. They did a much better job of staying on target and really doing it. 
	* (Maybe this isn't a bullet, but it's just a final roundup message on the slide.) You no longer needed to use state machine style workflow processing. You could put the instructions in the skill. 
* Reflect on the anatomy of the agent. Do a close-up schematic of him and show that it's just the same thing. We've just changed out the tools and given him a more powerful brain. 
* The Dawn of Recognition (This is a cheesy title, I don't like it.) - For a fun side project, I was building a video conferencing assistant that could look up things on the internet for you. I was going to build it with some sort of bespoke workflow, but then Shawn Simister, my GitHub colleague, took the wheel and started writing the crux, the core of the program in English as a skill to be executed by Claude Code. All that was left to do was to wrap it in a thin layer of traditional software so that it could integrate with the Zoom API. This is when it dawned on me that agents were the new software runtime, that agent skills were the new software, and that English was the new programming language of AI applications. (highlight this - it's a key point!) {Here's an image of Shawn https://media.licdn.com/dms/image/v2/C4D03AQFdgPA4NsT8Qg/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1638918509648?e=1785369600&v=beta&t=JGfngX6-dDfv0cc5JmWDI5NQdUCKRtznQrcirM7R-7Y We can make a funny picture of me and him hacking on something together. Maybe a Zoom potato thing.  }
- So we've come to the demo and here's the outline. We are going to build a job application review app. {We'll get a picture of the UI here}. The following is probably just spoken:
	- Applications come in alongside details about the job opening and it's the job of our reviewers, our human reviewers, to look at the people and compare their background and qualifications against the job opening. 
	- But it's work intensive because they have to understand enough about this person. They have to look them up on LinkedIn, they have to understand what their role is at their current company, they have to know about the new company, and pulling down all this information is really intensive. 
	- {I'm sure I'm missing bullet points here, so ask me about them in a moment. }
- Our approach to building this is to (Again, this is a multi-slide. )
	- Create the UI
	- Add in a mock agent that just returns static text but has the same form factor as the final agent { Have a cardboard cutout of our potato agent sitting at a chair. Give it a dumb blank expression on its face, maybe drawn in crayon.  }
	- Create a real agent there instead, but one that's not quite as skillful { Now replace it with a real agent, but still give it kind of a silly dumb expression on its face.  }
	- And then update the skills to make sure it's really smart. { Put a really thick instruction manual next to it and then make it look clever and smart.  }
- Let's take it for a test drive. { And the speaker notes that I'm imagining we're gonna have to add in some instructions about how to how to reproduce this ... Ask me about it.  } This is basically the intro slide to the demo itself. The following sub bullets should probably be The following sub-blotches should be added to two different slides. We're going to make them look as nice as they can, but these are going to be word dense and I don't care. I want to make sure that we also have the links the links links below correspond to zed, but we need to get the corresponding links for a permalink to the GitHub pages for these. 
	- Sub slide 1
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
	* Sub slide 2
		* Make your agent smarter  
			* The [skill file](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:1) is where you actually make the agent smart. These days it's often enough to implement the workflow in English.  
			* The [Screening flow](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:54) lays out an ordered set of steps. For workflows, defined steps make the agent easier to steer and much easier to debug when something goes wrong.  
			* Be crisp about output. The [Your output section](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:16) defines it in English, and [AIReviewOutput](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/backend/app/services/ai_reviewer.py:60) defines that exact shape in code.  PydanticAI enforces this structure as well, so it's a great way to make sure the model returns the required structure.
			* [Also not this line in the skill](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/SKILL.md:20), where I require `internal_notes` to conform to its own checklist structure. See [internal-notes-checklist.md](zed://file/Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/skills/screen-candidate/references/internal-notes-checklist.md:1).  
* Wrapup   - what have we learned
	* { close up image of potato agent standing at the peak of a mountain with a flag stuck in the ground}
	* Agent really aren't that complicated {schema again of potato agent}
	* How Agent Skills are the new programs for AI Applications  and English is their programming language.
	* How you can easily build AI workflow (or any AI Product) by wrapping an Agent that is running the correct skill
	* {on the bottom - we need python generated QR codes
		* for this codebase - label: "this codebase"
		* arcturus labs - label: "AI product consulting" 
		* rook streams - label: "I build AI product live"
		* superstream link - label: "O'Reilly Superstream July 23" 
	 maybe find better labels that are more consistent}
* But this is only the start, we haven't talked about {Keep the same QR codes on the screen. }
	* {Zoom out of the above image to show that the potato is actually standing on top of a very large mountain. }
	* evaluating the workflow to make sure that it's doing the right thing
	* generating test and training data
	* iteratively improve it
	* it turns out that this is a virtuous cycle, there are neat patterns you can follow
	* Follow me and I'll show you how. (point to QR code)
* And soon you'll see that there's even more. {Keep the same QR codes. }In this conversation we talked about how An AI agent can serve as the core for many types of AI applications. But in the next couple years you'll see that this will also be inverted and your personal agent will be your interface to all the applications you use into the world around you. And that's what I'm talking about at the upcoming a O'Reily Superstream on July 23 {Highlight the SuperStream QR code. }.    {We'll zoom out again to show that it's not really a mountain, it's just the peak of a really large iceberg most of which is underwater. the potato agent is still on top with a flag stuck in the peak. }



