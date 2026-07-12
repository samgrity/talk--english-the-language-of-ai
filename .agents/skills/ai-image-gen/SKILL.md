---
name: ai-image-gen
description: Generate and iterate on images with OpenAI's gpt-4o model via the Responses API. Supports multiple reference images, Pixar-style character iteration, greenscreen-first generation, and separate transparent cutout output. Use when the user wants AI-generated images, hero art, image-to-image iterations, or needs to generate/edit images with OpenAI reference inputs rather than Gemini.
---

# AI Image Generation (OpenAI)

Uses OpenAI's **`gpt-4o`** via the Responses API. Supports multiple reference images as input, with text describing what to generate or how to combine/edit the references.

This skill is especially good for **iterative character design**: generate a master version first, then use that image as a reference while refining style, pose, accessories, and expression.

## How image referencing works

Each reference image (`-i`) is sent with a text label — **"Reference Image 1:"**, **"Reference Image 2:"**, etc. You can refer to these labels directly in your prompt text. This is the simplest and most reliable way to do multi-image composition:

```bash
# "Make the subject look like Image 1, but with the style of Image 2"
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  -d IGNORED/my-post-slug \
  -s "potato-v2" \
  -i IGNORED/old-potato/image-01.jpg \
  -i docs/assets/style-ref.jpg \
  "Create a potato character with the exact same body shape and features as Image 1, but rendered in the art style of Image 2."
```

The model sees both images inline and can reference them by position. You don't need any special annotation format — just say "Image 1" and "Image 2" in your prompt.

## Default model

**`gpt-4o`** — OpenAI's multimodal flagship model with native image generation via the Responses API. It accepts text + images as input and produces images as output.

Override with `-m` if needed.

## Where to write files

Same convention as gemini-image-gen:

- Active blog post: `IGNORED/<post-slug>/` (match the markdown basename under `docs/blog/posts/`)
- No specific post: `IGNORED/images/`

Each invocation saves into a **named subdirectory** under the base output dir. Always supply `-s` with a short, human-readable topic name — e.g. `-s "potato-agent-hero"`. This keeps runs organized by meaning.

Images are numbered sequentially (`image-01`, `image-02`, …) and **never overwrite** existing files — re-running into the same subdir continues from the next available number.

## CLI

Path: `.agents/skills/ai-image-gen/scripts/ai-image-gen`

```bash
# Text-to-image (no references)
OPENAI_API_KEY=$_OPENAI_API_KEY \
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  -d slides/images \
  -s "potato-master-v1" \
  -n 1 \
  "Create a polished Pixar-style potato agent hero image"

# Single reference image — iterate on a previous result
OPENAI_API_KEY=$_OPENAI_API_KEY \
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  -d slides/images \
  -s "potato-v2" \
  -i slides/images/potato-master-v1/image-01-transparent.png \
  "Same character as Image 1, but make the expression more clever and confident"

# Multiple reference images — combine subject and style
OPENAI_API_KEY=$_OPENAI_API_KEY \
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  -d slides/images \
  -s "potato-final" \
  -i path/to/subject-ref.png \
  -i path/to/style-ref.png \
  "Create a character with the subject of Image 1 but in the visual style of Image 2"

# Greenscreen-first generation with separate transparent output
OPENAI_API_KEY=$_OPENAI_API_KEY \
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  -d slides/images \
  -s "potato-master-v1" \
  -n 1 \
  -t \
  "Create the most complete version of the potato agent"

# Greenscreen render only
OPENAI_API_KEY=$_OPENAI_API_KEY \
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  -d slides/images \
  -s "potato-master-v1" \
  -n 1 \
  --greenscreen-only \
  "Create the most complete version of the potato agent"

# Key an existing greenscreen image without regenerating
./.agents/skills/ai-image-gen/scripts/ai-image-gen \
  --key-only slides/images/potato-master-v1/image-01-greenscreen.png
```

Flags:

| Flag | Meaning |
|------|--------|
| `prompt` (positional) | What to generate or how to edit/combine the reference images |
| `-d`, `--output-dir` | Base output directory (required) |
| `-s`, `--subdir` | **Subdirectory name — always set this to a short meaningful topic name** |
| `-n`, `--num-images` | Candidates to produce (default **3**) |
| `-m`, `--model` | Model id (default **gpt-4o**) |
| `-i`, `--reference-image` | Reference image file; **repeat** for multiple references |
| `-q`, `--quality` | Image quality: `low`, `medium`, `high` (default **medium**) |
| `--size` | Image dimensions, e.g. `1024x1024`, `1792x1024`, `1024x1792` (default **1792x1024**) |
| `-t`, `--transparent` | Generate with a flat chroma-key greenscreen and also produce a separately keyed transparent output |
| `--greenscreen-only` | Generate only the greenscreen render |
| `--key-only FILE` | Skip generation and key an existing greenscreen image |

**Dependencies:** `openai` and `Pillow`. The current transparency workflow uses PIL-based greenscreen extraction, not rembg.

## Transparency workflow

When `-t` is used, the workflow is intentionally **two-step**:

1. Generate against a **perfectly flat greenscreen** background (`#00FF00`)
2. Save the original greenscreen render separately
3. Apply PIL-based chroma-key extraction
4. Automatically remove enclosed bright-green islands left in crevices
5. Automatically de-spill green from semi-transparent edge pixels
6. Save the transparent result separately

Current naming convention:
- plain mode: `image-01.png`
- greenscreen-only mode: `image-01-greenscreen.png`
- transparent mode: `image-01-greenscreen.png` + `image-01-transparent.png`

This is better than asking the model for "transparent background" directly, which often causes it to generate a **fake checkerboard** instead of real alpha.

## Agent behavior

- Pick output dir from the user's current task when obvious.
- **Always use `-s` with a short meaningful topic name** that describes the image concept.
- Default to **1–3 candidates** depending on iteration stage; use **1** when working carefully through character design.
- After generation, point the user at saved paths clearly.
- When iterating, pass the prior result as `-i` so the model uses it as a visual anchor.
- Multiple `-i` flags are supported; describe which reference does what in the prompt (e.g. "subject of Image 1, style of Image 2").
- For transparent cutouts, explicitly instruct the model to use a **flat chroma-key green background** with **no gradients, vignettes, shadows, or background texture**.
- The script now automatically performs a second-pass cleanup for enclosed green islands (e.g. elbow bends, prop gaps, leg gaps).
- The script also de-spills green from partially transparent edges.
- If the key still leaves stray green in tight gaps, tune the chroma-key thresholds instead of regenerating immediately.

## Running in the background (required)

Image generation takes 30–120 s. **Always run the CLI via a shell subagent** or backgrounded shell command so it does not block the main agent turn. Use `block_until_ms: 0` or spawn a subagent.

## What we've learned

- `gpt-4o` works well for iterative image generation with references.
- Asking for "transparent background" directly is unreliable; the model may generate a **checkerboard**.
- The best workflow so far is **greenscreen first, transparency second**.
- Preserve the greenscreen original so transparency extraction can be tuned without regenerating.
- Green-island cleanup and edge de-spill are worth automating in the script, not just describing in text.
- Best structure: one script with three modes — generate plain, generate greenscreen only, or key an existing greenscreen image.
- For character work, it helps to make the **most complex canonical version first**, then derive simpler variants from it.

## Comparison with gemini-image-gen

| Feature | ai-image-gen (OpenAI) | gemini-image-gen (Google) |
|---------|----------------------|--------------------------|
| Default model | `gpt-4o` | `gemini-3.1-flash-image-preview` |
| API | Responses API | generateContent |
| Reference images | Yes, with positional labels | Yes, with positional labels |
| Transparency workflow | Greenscreen + separate keyed output | Prompt-only / manual follow-up |
| Strengths | Better instruction following, better iteration | Cheaper, good for quick iterations |
