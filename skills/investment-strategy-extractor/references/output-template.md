# Output Template for Investment Strategy Extraction

This document defines the standard format for investment resource summaries. Follow this structure exactly to ensure consistency across all extractions.

## Document Structure

### 1. Title Section

```markdown
# [Book/Resource Title] by [Author Name]
```

- Use H1 heading (#) for the title
- Include author name after "by"
- For articles: Use article title and author/publication
- For videos: Use video title and channel/creator name

### 2. Content Hierarchy

The body follows this structure:

```
Part Level (Optional) → Chapter Level → Content (Summary + Key Ideas)
```

**Part Level (if applicable):**
- Use H2 heading (##) for parts
- Format: `## Part [Number]: [Part Title]`
- Only include if the resource is explicitly organized into parts
- Examples: "Part I: Introduction to Value Investing", "Part II: Advanced Analysis"

**Chapter Level (required):**
- Use H3 heading (###) for chapters
- Format: `### Chapter [Number]: [Chapter Title]`
- For articles: Use section headings instead (e.g., "### Introduction", "### Main Argument")
- For videos: Use timestamps or segment titles (e.g., "### Segment 1 (0:00-15:30): Key Principles")

**Content (required for each chapter):**

1. **Summary** (bold label)
   - 2-4 sentences capturing the chapter's main argument or theme
   - Focus on what the author teaches, not just topics discussed
   - Explain how this chapter contributes to the overall thesis

2. **Key Ideas** (bold label)
   - Bulleted list of specific, actionable principles
   - Each bullet should be concrete and applicable
   - Include formulas, criteria, or decision frameworks
   - Quote memorable phrases when relevant
   - Aim for 3-7 key ideas per chapter

### 3. Master Checklist Section

```markdown
## Master Checklist

| Question/Criteria | Source |
|------------------|--------|
| [Evaluation question or criterion] | Chapter X |
| [Another evaluation criterion] | Chapter Y |
...
```

**Guidelines:**

- **Header**: Use H2 heading (##) with title "Master Checklist"
- **Format**: Markdown table with two columns
- **Column 1 - Question/Criteria**: Frame as actionable yes/no questions or evaluation criteria
- **Column 2 - Source**: Reference the chapter where this principle originated
- **Content**: Consolidate ALL actionable principles from all chapters
- **Quantity**: Aim for 15-30+ items for full books, 5-10 for articles
- **Specificity**: Each item should be specific enough to use in actual investment evaluation

**Example Entries:**

```markdown
| Does the company have a durable competitive advantage? | Chapter 3 |
| Is the ROE consistently above 15%? | Chapter 7 |
| Can I understand what the company does? | Chapter 2 |
| Is management honest and competent? | Chapter 11 |
```

### 4. Bottom Line Section

```markdown
## Bottom Line

[2-3 sentence synthesis of the resource's core philosophy. Should be memorable, actionable, and capture the "big idea" that unifies the entire work.]
```

**Guidelines:**

- **Header**: Use H2 heading (##) with title "Bottom Line"
- **Length**: 2-3 sentences maximum
- **Content**: Synthesize the core philosophy or main takeaway
- **Tone**: Clear, direct, memorable
- **Test**: Can someone understand the resource's essence from this alone?

## Complete Template

```markdown
# [Resource Title] by [Author Name]

## Part I: [Part Title] (if applicable)

### Chapter 1: [Chapter Title]

**Summary:**
[2-4 sentences explaining the chapter's main argument and contribution to the overall thesis.]

**Key Ideas:**
- [Specific principle or actionable insight]
- [Framework or criteria mentioned]
- [Memorable quote or formula]
- [Another concrete takeaway]

### Chapter 2: [Chapter Title]

**Summary:**
[2-4 sentences]

**Key Ideas:**
- [Principle]
- [Insight]
- [Framework]

## Part II: [Part Title] (if applicable)

### Chapter 3: [Chapter Title]

...continue for all chapters...

## Master Checklist

| Question/Criteria | Source |
|------------------|--------|
| [Evaluation question] | Chapter X |
| [Another criterion] | Chapter Y |
| [Framework checkpoint] | Chapter Z |
...all actionable items from all chapters...

## Bottom Line

[2-3 sentence synthesis capturing the resource's core philosophy and main takeaway.]
```

## Field Specifications

### Summary Field

**Purpose**: Capture the chapter's main argument and teaching

**Requirements:**
- Length: 2-4 sentences (no more, no less)
- Focus: What the author is teaching, not just discussing
- Context: How this chapter fits into the larger work
- Clarity: Use simple, direct language

**Good Example:**
"This chapter introduces Warren Buffett's approach to identifying companies with durable competitive advantages. The author explains that such companies can maintain high returns on equity over decades without requiring significant capital reinvestment. Understanding this concept is foundational to the Buffett investment strategy described in later chapters."

**Bad Example:**
"This chapter is about competitive advantages." (Too brief, no substance)

### Key Ideas Field

**Purpose**: Extract specific, actionable principles

**Requirements:**
- Format: Bulleted list (use `-` for bullets)
- Quantity: 3-7 items per chapter (more if chapter is exceptionally rich)
- Specificity: Each bullet should be concrete and applicable
- Actionability: Reader should be able to use this principle
- Diversity: Cover different aspects of the chapter

**Good Examples:**
- "Look for companies with high returns on equity (>15%) sustained over 10+ years"
- "A 'moat' can be: brand power, patents, network effects, or regulatory protection"
- "Ask: 'Will this company still dominate in 10 years?' If uncertain, move on"

**Bad Examples:**
- "Competitive advantages are important" (Too vague)
- "The author discusses various metrics" (Not actionable)
- "Many companies fail to maintain advantages" (Not instructive)

### Master Checklist Field

**Purpose**: Provide a practical evaluation framework

**Requirements:**
- Format: Two-column markdown table
- Question/Criteria Column: Frame as questions or evaluation criteria
- Source Column: Chapter reference (e.g., "Chapter 3" or "Ch. 7")
- Comprehensiveness: Include ALL actionable principles from the resource
- Usability: Each item should be verifiable with available information
- Consistency: Use parallel structure (all questions or all criteria statements)

**Question Format (Preferred):**
```markdown
| Does the company have pricing power? | Chapter 5 |
| Is the debt-to-equity ratio below 0.5? | Chapter 9 |
| Can the business be understood in 5 minutes? | Chapter 2 |
```

**Criteria Format (Alternative):**
```markdown
| Company must have ROE > 15% for 10 years | Chapter 7 |
| Management should own significant equity | Chapter 11 |
| Industry should be stable and predictable | Chapter 4 |
```

**Avoid:**
- Vague items: "Company should be good" ❌
- Unanswerable items: "Will stock price rise?" ❌
- Duplicate items: Check for redundancy across chapters

### Bottom Line Field

**Purpose**: Synthesize the essential philosophy in memorable form

**Requirements:**
- Length: 2-3 sentences (strictly enforced)
- Coverage: Capture the core philosophy that unifies the work
- Clarity: Use simple, powerful language
- Memorability: Should stick in the reader's mind
- Actionability: Should guide investment approach

**Good Example:**
"Buffettology teaches investors to find companies with durable competitive advantages that can compound earnings at high rates without requiring significant capital. The key is to buy these businesses at reasonable prices and hold them for decades, allowing compound interest to work its magic. Patience, discipline, and focus on business quality over price action are the hallmarks of this approach."

**Bad Example:**
"This book is about Warren Buffett's investment strategy and how to pick good stocks." (Too generic, lacks specificity)

## Adaptation Guidelines

### For Articles (vs. Books)

**Changes:**
- Replace "Chapter" with article section headings
- Omit "Part" structure (articles rarely have parts)
- Master checklist will likely be shorter (5-10 items vs. 15-30)
- Bottom line captures the article's thesis, not a full philosophy

**Example:**
```markdown
# The Case for Index Funds by John Bogle

### Introduction
...

### The Cost Problem
...

### Historical Evidence
...

## Master Checklist
(5-10 items from the article)

## Bottom Line
(Article's main thesis in 2-3 sentences)
```

### For YouTube Videos (vs. Books)

**Changes:**
- Replace "Chapter" with segment titles or timestamps
- Format: `### Segment 1 (0:00-15:30): [Title]`
- Use timestamps for source in Master Checklist
- Summaries may be shorter if segments are brief

**Example:**
```markdown
# Warren Buffett on Stock Selection by CNBC

### Segment 1 (0:00-5:45): Introduction to Value Investing
...

### Segment 2 (5:45-12:30): Competitive Advantages
...

## Master Checklist

| Question/Criteria | Source |
|------------------|--------|
| Does the company have a moat? | Segment 2 |
...

## Bottom Line
...
```

## Quality Checklist

Before finalizing any extraction, verify:

- [ ] Title includes resource name and author
- [ ] All chapters/sections are included (none skipped)
- [ ] Each chapter has both Summary (2-4 sentences) and Key Ideas (3-7 bullets)
- [ ] Master Checklist is in table format with two columns
- [ ] Master Checklist includes all actionable principles
- [ ] Bottom Line is exactly 2-3 sentences
- [ ] Bottom Line captures the core philosophy
- [ ] Formatting uses proper markdown hierarchy (H1, H2, H3)
- [ ] No information is duplicated between sections
- [ ] Language is clear, direct, and actionable

## Common Mistakes to Avoid

❌ **Too-brief summaries**: "This chapter discusses valuation." (Need 2-4 sentences)

❌ **Vague key ideas**: "Companies should be good." (Be specific about what "good" means)

❌ **Missing chapters**: Skipping chapters because they seem repetitive (include all)

❌ **Wrong table format**: Using bullets for Master Checklist instead of markdown table

❌ **Overly long bottom line**: More than 3 sentences (keep it concise)

❌ **Generic bottom line**: Could apply to any investment book (be specific to this resource)

❌ **Inconsistent source references**: "Ch. 3" vs "Chapter 3" vs "3" (choose one format)

✅ **Correct approach**: Follow the template exactly, maintain consistency, and prioritize actionability throughout.

## Reference Example

See `examples/format-example.md` for a complete, correctly-formatted example that demonstrates all principles in this template.
