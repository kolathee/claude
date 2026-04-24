---
name: flashcard-compare
description: Use when the user provides a group of similar/synonym words and wants to understand the nuanced differences between them. Creates a single comparison flashcard saved to Obsidian.
model: sonnet
---

# flashcard-compare

Create a synonym-group comparison flashcard and save it to Obsidian for spaced-repetition review.

## Inputs

The user provides:
- **A group of similar words** — synonyms or near-synonyms they want to distinguish
- No context sentence required

## Steps

1. Identify the shared core meaning of the group
2. For each word, identify what makes it distinct — tone, strength, formality, connotation, typical context
3. Generate the comparison card using the template below
4. Insert the card at the **top** of `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Learning Vocab.md` using Python:
   ```python
   import os
   path = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Learning Vocab.md")
   with open(path, "r", encoding="utf-8") as f:
       existing = f.read()
   with open(path, "w", encoding="utf-8") as f:
       f.write(card_content + "\n\n---\n\n" + existing)
   ```
5. Confirm with: `Added "[group title]" comparison card to your flashcards.`
6. Then **explain the group to the user inline** — don't just save silently. Give a brief natural-language walkthrough of the key distinctions after confirming.

## Card Format (spaced-repetition)

Use this exact structure. The card title uses the group name or shared concept.

```
## [shared concept] — [word1] vs [word2] vs [word3] ... (adjective / adverb / etc.)
*Which word fits? What makes each one different?*
?
**Shared meaning:** <mark class="hltr-blue">[one sentence — what they all mean]</mark>
───────────────────
**The spectrum**
[arrange words from weakest/most neutral → strongest/most marked, or informal → formal]
<mark class="hltr-yellow">word1</mark> — [one-line distinction] · *"example sentence"*
<mark class="hltr-yellow">word2</mark> — [one-line distinction] · *"example sentence"*
<mark class="hltr-yellow">word3</mark> — [one-line distinction] · *"example sentence"*
[continue for all words]
───────────────────
**Quick decision rule**
→ Default pick: **[word]** — [when to use it, why it's safe]
→ Use **[word]** when [specific situation]
→ Use **[word]** when [specific situation]
→ Avoid **[word]** when [common mistake or trap]
───────────────────
**Memory hooks**
<mark class="hltr-orange">word1</mark> → [memorable association, etymology, or trick]
<mark class="hltr-orange">word2</mark> → [memorable association, etymology, or trick]
[only include if genuinely useful — skip weak ones]
───────────────────
**Tone & register**
<mark class="hltr-green">most formal</mark>: [word(s)]
<mark class="hltr-green">neutral / everyday</mark>: [word(s)]
<mark class="hltr-green">casual / colloquial</mark>: [word(s)]
```

> **IMPORTANT:** No blank lines within the card answer — blank lines create separate cards in the spaced-repetition plugin. Keep the entire answer as one unbroken block.

## Notes

- The spectrum section is the heart of the card — make each distinction concrete and memorable
- Example sentences should show the word in its most natural/typical context
- Quick decision rule should be opinionated — tell the user what to actually do, not just describe
- Memory hooks: only include if genuinely useful (etymology, visual association, contrast trick). Skip filler.
- After saving, explain the group conversationally to the user — use plain language, not card format
- **Use emojis inline throughout the card body AND the inline explanation** — woven into descriptions, not just as section headers. Match emoji to the context: 🔬 medical/research, 📊 data/statistics, ⚖️ legal, 🗣️ casual speech, 🎓 academic/formal, 💬 everyday, 🎯 purpose/focus, 🔗 direct connection, ⚠️ warning/trap, ✅ safe default, 💡 key insight, 🔄 mutual/together. Place emoji right before or after the relevant word or phrase for maximum clarity.
