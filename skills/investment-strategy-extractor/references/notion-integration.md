# Notion Integration Guide for Investment Strategy Extractor

This guide provides step-by-step instructions for saving investment strategy extractions to the user's Notion "Investment Books" database.

## Overview

After extracting investment principles from a resource, the summary must be saved to Notion for knowledge management. The user maintains an "Investment Books" database in Notion where all book summaries are stored.

## Prerequisites

The user has access to Notion through the MCP integration (`mcp__plugin_productivity_notion__*` tools or `mcp__google-workspace__*` tools). Verify access before attempting to save.

## Workflow

### Step 1: Load Notion Tools

Before using any Notion functionality, load the required tools using ToolSearch:

```
ToolSearch(query="notion create")
```

This will load the necessary Notion MCP tools, including:
- `notion-create-pages` - For creating new database entries
- `notion-search` - For finding databases
- `notion-fetch` - For retrieving page/database details

**Alternative**: If Notion tools don't load, try Google Workspace MCP:
```
ToolSearch(query="google workspace create")
```

### Step 2: Identify the Target Database

The user's target database is named **"Investment Books"**.

**Option A: User provides database URL**
- If user shares a Notion URL like: `https://notion.so/workspace/abc123...`
- Extract the database ID from the URL (the string after the last `/` and before any `?`)

**Option B: Search for database**
- Use notion-search to find the database:
  ```
  notion-search(query="Investment Books", type="database")
  ```
- Select the matching database from results

**Option C: Ask user**
- If database cannot be found: "I need the database ID or URL for your 'Investment Books' database in Notion. You can find this by opening the database and copying the page URL."

### Step 3: Prepare the Content

Convert the markdown extraction into Notion-compatible format.

**Notion Block Structure:**

Notion uses a block-based content model. The markdown summary must be converted to Notion blocks:

1. **Heading blocks**: For titles (# → heading_1, ## → heading_2, ### → heading_3)
2. **Paragraph blocks**: For summary text
3. **Bulleted list blocks**: For key ideas
4. **Table blocks**: For master checklist
5. **Quote blocks**: For bottom line (optional styling)

**Markdown to Notion Conversion:**

```markdown
# Title → heading_1 block
## Section → heading_2 block
### Subsection → heading_3 block
Regular text → paragraph block
- Bullet → bulleted_list_item block
| Table | → table block with rows
```

**Example Conversion:**

Original markdown:
```markdown
### Chapter 1: Value Investing Basics

**Summary:**
This chapter introduces fundamental concepts.

**Key Ideas:**
- Look for undervalued companies
- Focus on intrinsic value
```

Becomes Notion blocks:
```json
[
  {
    "type": "heading_3",
    "heading_3": {"rich_text": [{"text": {"content": "Chapter 1: Value Investing Basics"}}]}
  },
  {
    "type": "paragraph",
    "paragraph": {"rich_text": [{"text": {"content": "Summary: This chapter introduces fundamental concepts."}}]}
  },
  {
    "type": "bulleted_list_item",
    "bulleted_list_item": {"rich_text": [{"text": {"content": "Look for undervalued companies"}}]}
  },
  {
    "type": "bulleted_list_item",
    "bulleted_list_item": {"rich_text": [{"text": {"content": "Focus on intrinsic value"}}]}
  }
]
```

**Simplified Approach:**

Since the Notion MCP tools may handle markdown directly, try passing the markdown content as-is first. The tool may auto-convert:

```
notion-create-pages(
  parent_id="database_id",
  title="Buffettology by Mary Buffett",
  content="[Full markdown content here]"
)
```

If this fails, ask the user if they prefer:
1. Pasting the markdown manually into Notion
2. Saving as a .md file and uploading to Notion
3. Using a simplified format that's easier to convert

### Step 4: Set Database Properties

The "Investment Books" database should have these properties:

**Required Properties:**
- **Title**: Book/resource title and author (e.g., "Buffettology by Mary Buffett")
- **Author**: Author name (e.g., "Mary Buffett")
- **Date Added**: Today's date (use current date)
- **Resource Type**: Type of resource (Book / Article / Video)

**Optional Properties** (if database has them):
- **Status**: Reading status (e.g., "Completed", "In Progress")
- **Rating**: User's rating (ask user if they want to rate)
- **Tags**: Categorization tags (e.g., "Value Investing", "Warren Buffett")
- **Year Published**: Publication year
- **Notes**: Additional notes field

**Example Property Values:**

For "Buffettology by Mary Buffett":
```json
{
  "Title": {"title": [{"text": {"content": "Buffettology by Mary Buffett"}}]},
  "Author": {"rich_text": [{"text": {"content": "Mary Buffett"}}]},
  "Date Added": {"date": {"start": "2026-03-03"}},
  "Resource Type": {"select": {"name": "Book"}}
}
```

### Step 5: Create the Notion Page

Use the `notion-create-pages` tool to create the database entry:

```
notion-create-pages(
  parent_id="[database_id]",
  title="[Book Title] by [Author]",
  properties={
    "Author": "[Author Name]",
    "Date Added": "[Today's Date]",
    "Resource Type": "[Book/Article/Video]"
  },
  content="[Full markdown extraction]"
)
```

**Handle Errors:**

Common errors and solutions:

1. **Database not found**: Ask user for database URL or ID
2. **Permission denied**: User needs to grant integration access in Notion
3. **Invalid property**: Database might have different property names
4. **Content too long**: Notion has limits (~2000 blocks), may need to truncate or split

### Step 6: Confirm Success

After creating the page:

1. **Get the page URL** from the tool response
2. **Show user the URL**: "I've saved the summary to your Investment Books database: [URL]"
3. **Suggest next steps**: "You can review the summary in Notion and add any personal notes or ratings."

## Alternative Workflows

### If Notion MCP Tools Unavailable

**Fallback Option 1: Export as Markdown File**
```
Write(
  file_path="~/Downloads/[BookTitle]-summary.md",
  content="[Full extraction]"
)
```
Instruct user: "I've saved the summary as a markdown file. You can upload this to Notion manually by dragging the file into your Investment Books database."

**Fallback Option 2: Copy-Paste Instructions**
1. Generate the extraction in markdown
2. Display it to the user
3. Instruct: "Copy this content and paste it into a new page in your Investment Books database in Notion."

### If Database Structure is Different

If user's database has different properties:

1. **Ask user**: "I see your database has [properties found]. Which should I use for [purpose]?"
2. **Adapt**: Map the extraction fields to available properties
3. **Document**: Note the customization for future extractions

## Database Setup (If Needed)

If user doesn't have an "Investment Books" database yet:

**Offer to help create it:**

"I notice you don't have an 'Investment Books' database in Notion yet. Would you like me to create one with these properties?

**Suggested Properties:**
- Title (title)
- Author (text)
- Date Added (date)
- Resource Type (select: Book/Article/Video)
- Status (select: To Read/Reading/Completed)
- Rating (number or select: ⭐-⭐⭐⭐⭐⭐)
- Tags (multi-select)

I can set this up for you."

**Create Database:**
```
notion-create-database(
  parent_page_id="[user's workspace]",
  title="Investment Books",
  properties={
    "Title": {"title": {}},
    "Author": {"rich_text": {}},
    "Date Added": {"date": {}},
    "Resource Type": {"select": {"options": [
      {"name": "Book"},
      {"name": "Article"},
      {"name": "Video"}
    ]}},
    "Status": {"select": {"options": [
      {"name": "To Read"},
      {"name": "Reading"},
      {"name": "Completed"}
    ]}},
    "Rating": {"number": {}},
    "Tags": {"multi_select": {}}
  }
)
```

## Best Practices

1. **Always confirm before saving**: "I'll save this to your Investment Books database. Does that look correct?"
2. **Include page URL in response**: Users want quick access to verify
3. **Handle markdown carefully**: Test whether Notion MCP auto-converts or needs manual conversion
4. **Check property names**: Different users may name properties differently
5. **Preserve formatting**: Maintain the structure and hierarchy from the extraction
6. **Ask about optional fields**: "Would you like to add a rating or tags?"

## Troubleshooting

### Issue: Notion tools not found
**Solution**: Load using ToolSearch first, or fall back to file export

### Issue: Permission errors
**Solution**: User needs to share database with Notion integration
**Instruction**: "Please go to your Investment Books database in Notion → Share → Invite → [Integration Name] and grant access."

### Issue: Content too large
**Solution**: Notion has block limits
**Options**:
1. Save as child pages (one per part/section)
2. Truncate less critical sections
3. Link to external markdown file

### Issue: Table formatting breaks
**Solution**: Master Checklist table may need special handling
**Options**:
1. Convert table to simple list in Notion
2. Use Notion's database-within-page feature
3. Link to external spreadsheet

### Issue: User prefers different format
**Solution**: Ask about preferences before saving
**Question**: "How would you like this saved to Notion: as-is, simplified, or broken into sections?"

## Integration Checklist

Before marking the skill complete:

- [ ] ToolSearch used to load Notion tools
- [ ] Database identified (by search, URL, or user input)
- [ ] Content properly formatted for Notion
- [ ] Properties populated correctly (Title, Author, Date, Type)
- [ ] Page created successfully
- [ ] Page URL provided to user
- [ ] User confirmed successful save

## Example Complete Workflow

```
1. Extract investment principles → generate markdown summary
2. ToolSearch(query="notion create") → load Notion tools
3. Ask user: "Should I save this to your Investment Books database?"
4. User confirms: "Yes"
5. notion-search(query="Investment Books") → find database ID
6. notion-create-pages(
     parent_id=database_id,
     title="Buffettology by Mary Buffett",
     properties={Author: "Mary Buffett", Date Added: "2026-03-03", Resource Type: "Book"},
     content=markdown_summary
   )
7. Response: "Saved! View here: https://notion.so/abc123"
8. User: "Great, thanks!"
```

## Future Enhancements

Potential improvements for the integration:

1. **Batch uploads**: Process multiple books at once
2. **Update existing entries**: Check if book already exists and update instead of duplicate
3. **Auto-tagging**: Suggest tags based on content analysis
4. **Reading list sync**: Pull from user's to-read list in Goodreads or similar
5. **Cross-referencing**: Link related books in database
6. **Progress tracking**: Mark chapters as extracted if doing piecemeal analysis

## Summary

The Notion integration workflow:
1. Load tools with ToolSearch
2. Find "Investment Books" database
3. Convert markdown to Notion format
4. Set properties (Title, Author, Date, Type)
5. Create page with notion-create-pages
6. Provide user with page URL
7. Handle errors gracefully with fallbacks

Keep the user informed at each step and offer alternatives if the primary method fails.
