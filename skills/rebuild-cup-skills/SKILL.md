---
name: rebuild-cup-skills
description: Rebuild and repackage the cup-skills Cowork plugin from ~/.claude/skills/. Use when the user says "rebuild my skills plugin", "rebuild cup skills", "update skills plugin", "/rebuild-cup-skills", or "repack skills". Run this after adding, editing, or removing any skill in ~/.claude/skills/.
---

# Rebuild Cup Skills Plugin

Repack all skills from `~/.claude/skills/` into a fresh `cup-skills.plugin` ready to install in Cowork.

## Steps

Run this bash block exactly as written — it is self-contained and needs no external script file:

```bash
set -e

SKILLS_SRC="$HOME/.claude/skills"
OUTPUT="$HOME/cup-skills.zip"
TMP_DIR=$(mktemp -d)
PLUGIN_DIR="$TMP_DIR/cup-skills"

mkdir -p "$PLUGIN_DIR/.claude-plugin"
mkdir -p "$PLUGIN_DIR/skills"

cat > "$PLUGIN_DIR/.claude-plugin/plugin.json" << 'EOF'
{
  "name": "cup-skills",
  "version": "0.1.0",
  "description": "Cup's personal skills for Agoda PAYFLEX work — calendar planning, cashback testing, Obsidian, investments, and more.",
  "author": { "name": "Kolathee Payuhawattana" }
}
EOF

COUNT=0
for skill_dir in "$SKILLS_SRC"/*/; do
  skill_name=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    cp -r "$skill_dir" "$PLUGIN_DIR/skills/"
    echo "  ✓ $skill_name"
    COUNT=$((COUNT + 1))
  else
    echo "  ⚠ $skill_name — no SKILL.md, skipped"
  fi
done

cd "$PLUGIN_DIR"
zip -r /tmp/cup-skills.zip . -x "*.DS_Store" > /dev/null
cp /tmp/cup-skills.zip "$OUTPUT"
rm -rf "$TMP_DIR" /tmp/cup-skills.zip

echo ""
echo "✅ cup-skills.zip rebuilt with $COUNT skills → $OUTPUT"
```

After running, report:
- How many skills were packed
- Which skills were skipped (if any)
- Remind the user to install the updated plugin via **Cowork Settings → Plugins** to apply changes
