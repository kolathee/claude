---
name: flashcard-explain
description: Use when the user wants to create an English vocabulary flashcard from a word or phrase they encountered — in a sentence, meme, article, headline, or any context. Saves to Obsidian spaced-repetition.
---

# flashcard-explain

Create a rich English vocabulary flashcard and append it to Obsidian for spaced-repetition review.

## Inputs

The user provides:
- **The word or phrase** they want to learn
- **Context** — a sentence, headline, meme caption, image description, or any surrounding text where they saw it

## Steps

1. Identify the word's part of speech
2. Generate the full card content using the template below
3. Append the card to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Learning Vocab.md`
4. Confirm with: `Added "[word]" to your flashcards.`

## Card Format (spaced-repetition)

Append to the file using this exact structure — blank line before and after each card:

```
## [word] ([part of speech])
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

- If the user provides an image, describe what's shown before generating the card
- Keep the definition focused on practical meaning, not textbook definitions
- Patterns should reflect real usage — pick the most common ones
- Tone section should help the user know when/where they'd actually use this word
