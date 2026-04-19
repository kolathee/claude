---
name: flashcard-translate
description: Use when the user wants to create a Thai-to-English translation practice flashcard from a Thai sentence they want to learn to say in English. Saves to Obsidian spaced-repetition.
---

# flashcard-translate

Create a Thai→English translation practice flashcard and append it to Obsidian for spaced-repetition review.

## Inputs

The user provides:
- **A Thai sentence** they want to practice translating to English
- Optionally: **context or tone** (formal, casual, work email, texting a friend, etc.)

## Steps

1. Generate the card content using the template below
2. Append to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Translation (TH-EN).md`
3. Use Python via Bash to write (iCloud path has spaces that break shell tools):
   ```python
   import os
   path = os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Eng FlashCard/Translation (TH-EN).md")
   with open(path, "a", encoding="utf-8") as f:
       f.write("\n" + card_content)
   ```
4. Confirm with: `Added translation card to your flashcards.`

## Card Format (spaced-repetition)

> **IMPORTANT:** No blank lines within the card answer — blank lines create separate cards in the plugin. Keep the entire answer as one unbroken block. Use `────────────────` as section dividers. Never use `---` (plugin treats it as card separator).

> **No bullet lists** — bullet lists (`-`) don't close without a blank line, which would split the card. Use plain lines only.

```
## [Thai sentence]
?
**English:** *"[most natural, everyday translation with <mark class="hltr-yellow">key word highlighted yellow</mark>]"*
────────────────
#### Alternatives (with tone)
*"[version with <mark class="hltr-yellow">key distinctive word/structure highlighted yellow</mark>]"* — <mark class="hltr-green">tone label</mark>
*"[version with <mark class="hltr-yellow">key distinctive word/structure highlighted yellow</mark>]"* — <mark class="hltr-green">tone label</mark>
*"[version with <mark class="hltr-yellow">key distinctive word/structure highlighted yellow</mark>]"* — <mark class="hltr-green">tone label</mark>
*"[version with <mark class="hltr-yellow">key distinctive word/structure highlighted yellow</mark>]"* — <mark class="hltr-green">tone label</mark>
────────────────
#### Why this phrasing
→ [one key structural or word choice difference from Thai — highlight Thai word in <mark class="hltr-blue">blue</mark> if useful]
→ [second note if useful — implied subject, idiom, register shift]
```

## Highlight color scheme

- **Yellow** (`hltr-yellow`): the key word or structure in each version — the thing that makes it different from the others. In the main English line, highlight the most important translated word.
- **Green** (`hltr-green`): tone/register label after each alternative (natural, casual, professional, etc.)
- **Blue** (`hltr-blue`): Thai word being explained in the "Why this phrasing" section

## Notes

- **English** line = the most natural, go-to version a native speaker would say
- **Alternatives** = 3-5 options covering different tones: natural, slightly formal, soft/collaborative, casual, professional, Slack/team chat, written. Pick the most useful combos for the sentence.
- In each alternative, highlight the word or phrase that makes it distinctive — what you'd swap out to change the tone or emphasis. This is what the user should learn to recognize.
- **Why this phrasing** = focus on things that differ from Thai structure — not obvious word-for-word translations
- If context/tone is given by the user, lead with that version as the main **English** line
