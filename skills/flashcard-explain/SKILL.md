---
name: flashcard-explain
description: Use when the user wants to create an English vocabulary flashcard from a word or phrase they encountered — in a sentence, meme, article, headline, or any context. Saves to Obsidian spaced-repetition.
model: sonnet
---

# flashcard-explain

Create a rich English vocabulary flashcard and append it to Obsidian for spaced-repetition review.

## Inputs

The user provides:
- **The word or phrase** they want to learn
- **Context** — a sentence, headline, meme caption, image description, or any surrounding text where they saw it

## Steps

1. Identify the word's part of speech — if the word can function as multiple parts of speech (e.g. both noun and verb), list all of them in the title
2. Generate the full card content using the template below
3. Insert the card at the **top** of `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Learning Vocab.md` using Python:
   ```python
   import os
   path = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Learning Vocab.md")
   with open(path, "r", encoding="utf-8") as f:
       existing = f.read()
   with open(path, "w", encoding="utf-8") as f:
       f.write(card_content + "\n\n---\n\n\n" + existing)
   ```
4. Confirm with: `Added "[word]" to your flashcards.`

## Card Format (spaced-repetition)

Use this exact structure — blank line before and after each card:

```
## [word] ([part of speech])
*"[context sentence with <mark class="hltr-yellow">word highlighted in yellow</mark>]"*
[If image provided: **Context:** 1-2 sentences describing the scene — what it shows, key details, why this word appeared there. Pure scene description only, no word explanation.]
?
**Meaning:** [definition. Use <mark class="hltr-blue">blue highlight</mark> for the core concept.]
───────────────────
#### In your sentence
*"[sentence with <mark class="hltr-yellow">word highlighted in yellow</mark>]"*
→ [explain meaning in context, *italics* for nuance]
→ [one more implication if useful]
───────────────────
#### Common patterns
<mark class="hltr-orange">word + preposition</mark> + noun → *"example sentence"*
<mark class="hltr-orange">word + structure</mark> → *"example sentence"*
[2-3 most useful real-world patterns, no bullet prefix]
───────────────────
#### Alternatives
**simplest** · *simpler, [nuance]* · "example sentence"
**another** · *simpler/neutral, [nuance]* · "example sentence"
**formal option** · *more formal, [nuance]* · "example sentence"
**lookalike** → ~~not the same~~ — brief explanation
───────────────────
#### Tone & register
<mark class="hltr-green">tone label</mark> — [where it's commonly used]
→ [what it implies or signals]
→ [origin or memorable note if useful]
```

> **IMPORTANT:** No blank lines within the card answer — blank lines create separate cards in the spaced-repetition plugin. Keep the entire answer as one unbroken block.

## Notes

- If the user provides an image, include a **Context** line between the sentence and `?` — 1-2 sentences describing the scene (what it shows, key details). Pure scene description only, no explanation of the word itself.
- Keep the definition focused on practical meaning, not textbook definitions
- Patterns should reflect real usage — pick the most common ones
- Tone section should help the user know when/where they'd actually use this word
