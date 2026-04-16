---
name: candidate-evaluation
description: I will provide my opinion about a candidate. help me write the evaluation summary using the provided information. Help correct sentences and summarize it in the same format as coding-interview-result.md example.
---

**Rules:** Conclusion is based on overall score "proceed" if the total score is equal or more than 3, and "reject" if not. Overall score is calculated from all 5 metrics (Problem solving, Coding efficiency, Communication, Testing, Understanding performance.)

## Workflow

1. **Receive interview info** — candidate name, date/time, HackerRank link, Greenhouse link, email.
2. **Receive feedback** — Cup shares his observations after the interview.
3. **Check for gaps before writing** — review the feedback against all 5 scorecard categories:
   - Problem solving
   - Coding efficiency
   - Communication
   - Testing
   - Understanding performance

   If any category is missing a score, or the detail is too vague to write meaningful feedback, **ask Cup to clarify first**. Do not fill in guesses or write the note until all categories are covered.

4. **Write the note** — once all scores and details are confirmed, fill in the scorecard table and summary section.
5. **Apply humanizer** — always run the humanizer skill on the scorecard feedback, summary, and pros/cons before saving. The writing should sound like Cup wrote it himself, not like a generated evaluation report.
6. **Save to file** — write the note to `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/CupOb/Agoda/Interviews/<YEAR>/Interview - <Candidate Name> (<YYYY-MM-DD>).md`. If the year folder doesn't exist, create it. Do not print the note content to the terminal — just confirm the file path after saving.

## Score rules

- Each category is scored 1–5
- Conclusion: **Proceed** if average ≥ 3.0, **No proceed** if below 3.0
- Average = total / 5

## Output format

After writing the scorecard table, always produce a summary in this exact structure:

```
### Excelled in
- [area] - [what they did well, concise]
- [area] - [what they did well, concise]

### Struggled with
- [area] - [what went wrong, concise]
- [area] - [what went wrong, concise]

### Conclusion
**Recommendation:** Proceed / No proceed

**Pros:** [1-2 sentences on strengths]

**Cons:** [1-2 sentences on weaknesses]
```

Rules for this section:
- Use `-` as the connector within bullet text, never `—`
- No bold headers inside bullet points
- Keep bullets short and direct - one observation per bullet
- Pros/Cons should read like a human wrote them, not a performance review
- Use natural, conversational language throughout - write like you're telling a colleague about the candidate, not filing an official report
- Avoid formal or stiff phrasing; simple and direct is better
