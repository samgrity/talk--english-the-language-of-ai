## Tasks

* [x] outline  
* [ ] walkthrough code approach  
    * [x] replace all samples w/ real people  
    * [x] `.agent/skills/screen-candidate/references/template/` is missing - so get rid of the skill definitions?  
    * [ ] delete teh sandbox dir ( be careful about the fact that it's writing elsewhere and it's shuffling around directories)  
    * [ ] make the review application more realistic  
    * [ ] replace linkedin API w/ fake data for those people  
    * [ ] rewrite README w/ the assumption that it's for students  
    * [ ] strip out non-AI decisions?  
* [ ] rename talk and redescribe and send email  
* [ ] Write talk  
* [ ] Make QR codes  
    * [ ] for repo  
    * [ ] arcturus labs  
    * [ ] next show  
* [ ] commit code publicly  
* [ ] make slides  
* [ ] send them

## Notes

* uv run --directory backend ../scripts/review_from_seed_data.py ../scripts/db/seed_data/john_berryman.json  
    * uv run --directory backend ../scripts/review_from_seed_data.py ../scripts/db/seed_data/greg_ceccarelli.json  
    * uv run --directory backend ../scripts/review_from_seed_data.py ../scripts/db/seed_data/doug_turnbull.json  
* scripts/navigate_traces.py  
* tail -n2 /Users/johnberryman/projects/github/arcturus-labs/talk--agents-are-the-core/logs/agent_traces.jsonl | head -n1 | jq .