# Guard Against Dirty Working Tree When Cloning/Committing

## Pattern: Always check for unrelated staged changes

When cloning a repo that already exists locally, or when committing to a freshly checked-out branch, always verify the diff only contains intended changes.

### What happened
Cloned `messaging-client-messages` which had a pre-existing uncommitted change to a Cashback file. Running `git add -A` picked up this unrelated change and included it in the commit.

### Prevention
```bash
# After committing, verify only expected files are in the diff
git diff HEAD~1 --stat

# If unrelated files appear, remove them from the commit
git checkout HEAD~1 -- path/to/unrelated/file
git add path/to/unrelated/file
git commit --amend --no-edit
git push --force-with-lease
```

### Better approach
Before committing, always use `git add <specific-files>` instead of `git add -A` when working in repos with pre-existing dirty state.
