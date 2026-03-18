---
name: experiment-integration
description: Integrate or deintegrate experiments in the iOS codebase. Use when the user says "integrate experiment", "deintegrate experiment", "Int", "DeInt", "remove experiment", "add experiment".
---

# Experiment Lifecycle

Handle integration and deintegration of experiments in the iOS codebase.

## Key Terminology

- **A side (control)**: The existing/original behavior — what users see when the experiment is OFF.
- **B side (treatment)**: The new feature/change — what users see when the experiment is ON.
- **Integrate**: The experiment **succeeded** (B side won). Make the feature permanent by treating it as **always ON**. Remove all toggle checks and keep the B-side code.
- **Deintegrate**: The experiment **failed** (A side won). Revert by treating it as **always OFF**. Remove all toggle checks and keep the A-side code.

## Determine Action Type

Ask the user or infer from context:

| Prefix / Keyword | Action | Meaning |
|---|---|---|
| `Int`, "integrate" | **Integrate** | Experiment succeeded — treat as **always ON** (B side wins). Remove all A-side code and toggle checks. |
| `DeInt`, "deintegrate" | **Deintegrate** | Experiment failed — treat as **always OFF** (A side wins). Remove all B-side code and toggle checks. |

**CRITICAL**: Both actions remove the experiment entirely. The difference is which side survives:
- **Integrate** = keep B side (the new feature becomes permanent)
- **Deintegrate** = keep A side (revert to original behavior)

---

## Codebase Structure

### Experiment Definition Locations

| File | Purpose |
|---|---|
| `Modules/Core/Rubin/Toggles/{Team}Toggles.swift` | Team-specific experiment constants as `Experiment` extensions |

### Usage Patterns in Code

```swift
// Toggle check
toggler.isOn(Experiment.experimentName)
toggler.isOff(Experiment.experimentName)
toggler.evaluate(Experiment.experimentName, off: valueA, on: valueB)

// Test mock
mockToggler.states[Experiment.experimentName] = .on
stubToggler.states[Experiment.experimentName] = .off
```

---

## Deintegration Workflow

Deintegration means the experiment failed — the A side (control) remains as the permanent behavior.

### Step 1: Find All References

Search the `Modules/` directory for the experiment name and its JIRA identifier:

```
grep -rl "experimentName" Modules/ --include="*.swift"
grep -rl "JIRA_ID" Modules/ --include="*.swift"
```

Search for both the Swift property name (e.g., `cashbackRemptionNudge`) and the JIRA ID (e.g., `CASH_3558`, `CASH-3558`).

### Step 2: Read and Analyze Each File

For every file found, read the surrounding context (20+ lines) to understand:
- What happens when the experiment is **ON** (B side — to be removed)
- What happens when the experiment is **OFF** (A side — to be kept)
- Whether the removed code leaves dead code (unused methods, properties, imports, views, test cases)

### Step 3: Apply Changes (Always-OFF Logic)

For each usage pattern, apply the OFF/control side:

| Pattern | Before | After |
|---|---|---|
| `guard toggler.isOn(Exp.x) else { return }` then code | Guard + code block | Remove entire method body (or method if only caller is removed) |
| `if toggler.isOn(Exp.x) { B } else { A }` | if/else | Keep only `A` block |
| `toggler.isOn(Exp.x)` in boolean expression | Toggle check | Replace with `false` (then simplify) |
| `toggler.isOff(Exp.x)` in boolean expression | Toggle check | Replace with `true` (then simplify) |
| `toggler.evaluate(Exp.x, off: A, on: B)` | Evaluate call | Replace with `A` |
| `(toggler.isOn(Exp.x), "CODE")` in array | Tuple in list | Remove the tuple entry |
| `mockToggler.states[Exp.x] = .on` in tests | Test setup | Remove (test may need deletion if it only tests B side) |

### Step 4: Remove Experiment Definition

1. **Toggle file** (`{Team}Toggles.swift`): Remove the `public static let` line
2. **Generated file** (`ExperimentIdentifier.generated.swift`): Remove all 3 entries:
   - The `case` in the enum
   - The identifier string return
   - The name string return

### Step 5: Clean Up Dead Code

After removing experiment checks, trace and remove any newly dead code:

- **Unused methods**: If a method was only called from removed code, delete it
- **Unused properties**: If a property was only used by removed code, delete it
- **Unused init parameters**: If removed from a class/struct, update init, callers, and assembly/DI
- **Unused imports**: If no remaining code uses a module, remove the import
- **Dead views/UI**: If a view is never shown, delete the file
- **Dead tests**: If a test only validates removed behavior, delete it
- **Dead test helpers**: Remove mock properties, setup/teardown lines, and helper parameters that served removed tests
- **Snapshot tests**: Remove snapshots that test removed UI
- **View state properties**: If a property is always a constant (e.g., always `""`), remove it from the struct, init, and all call sites
- **Constants**: Remove constants only used by deleted code

### Step 6: Verify

```
grep -rn "experimentName" Modules/ --include="*.swift"
grep -rn "JIRA_ID" Modules/ --include="*.swift"
```

Confirm zero remaining references.

---

## Integration Workflow

Integration means the experiment succeeded — the B side (treatment) becomes the permanent behavior.

### Step 1: Find All References

Search the `Modules/` directory for the experiment name and its JIRA identifier:

```
grep -rl "experimentName" Modules/ --include="*.swift"
grep -rl "JIRA_ID" Modules/ --include="*.swift"
```

Search for both the Swift property name (e.g., `cashbackDatePickerFix`) and the JIRA ID (e.g., `CASH_3625`, `CASH-3625`).

### Step 2: Read and Analyze Each File

For every file found, read the surrounding context (20+ lines) to understand:
- What happens when the experiment is **ON** (B side — to be kept)
- What happens when the experiment is **OFF** (A side — to be removed)
- Whether the removed code leaves dead code (unused methods, properties, imports, views, test cases)

### Step 3: Apply Changes (Always-ON Logic)

For each usage pattern, apply the ON/treatment side:

| Pattern | Before | After |
|---|---|---|
| `if toggler.isOn(Exp.x) { B } else { A }` | if/else | Keep only `B` block |
| `if toggler.isOff(Exp.x) { A } else { B }` | if/else | Keep only `B` block |
| `toggler.isOn(Exp.x)` in boolean expression | Toggle check | Replace with `true` (then simplify) |
| `toggler.isOff(Exp.x)` in boolean expression | Toggle check | Replace with `false` (then simplify) |
| `toggler.evaluate(Exp.x, off: A, on: B)` | Evaluate call | Replace with `B` |
| `toggler.isOn(Exp.x) ? valueB : valueA` | Ternary | Replace with `valueB` |
| `guard toggler.isOn(Exp.x) else { return }` then code | Guard + code block | Remove the guard, keep the code block |
| `(toggler.isOn(Exp.x), "CODE")` in array | Tuple in list | Replace with `(true, "CODE")` or simplify |
| `mockToggler.states[Exp.x] = .on` in tests | Test setup | Remove (test should verify B-side behavior without toggle setup) |
| `mockToggler.states[Exp.x] = .off` in tests | Test setup | Remove (test may need deletion if it only tests A side) |

### Step 4: Remove Experiment Definition

1. **Toggle file** (`{Team}Toggles.swift`): Remove the `public static let` line
2. **Generated file** (`ExperimentIdentifier.generated.swift`): Remove all 3 entries:
   - The `case` in the enum
   - The identifier string return
   - The name string return

### Step 5: Clean Up Dead Code

After removing experiment checks, trace and remove any newly dead code:

- **Unused methods**: If a method was only called from removed A-side code, delete it
- **Unused properties**: If a property was only used by removed A-side code, delete it
- **Unused init parameters**: If removed from a class/struct, update init, callers, and assembly/DI
- **Unused imports**: If no remaining code uses a module (e.g., `import Toggles` when no more `Experiment.` references), remove the import
- **Dead views/UI**: If an A-side view is never shown, delete the file
- **Dead tests**: If a test only validates A-side (OFF) behavior, delete it. Update ON tests to remove toggle setup since the behavior is now unconditional.
- **Dead test helpers**: Remove mock properties, setup/teardown lines, and helper parameters that served removed tests
- **Snapshot tests**: Remove snapshots that test removed A-side UI
- **View state properties**: If a property is always a constant after integration, inline or remove it
- **Constants**: Remove constants only used by deleted code

### Step 6: Verify

```
grep -rn "experimentName" Modules/ --include="*.swift"
grep -rn "JIRA_ID" Modules/ --include="*.swift"
```

Confirm zero remaining references.

---

## Checklist

### Integration (experiment succeeded — always ON)
- [ ] Found ALL references (Swift name + JIRA ID)
- [ ] Applied always-ON logic at every usage site (kept B-side code)
- [ ] Removed experiment definition from toggle file
- [ ] Removed experiment entries from generated file
- [ ] Traced and removed all dead code (A-side methods, properties, views, tests, imports)
- [ ] Updated remaining tests to remove toggle setup (behavior is now unconditional)
- [ ] Verified zero remaining references

### Deintegration (experiment failed — always OFF)
- [ ] Found ALL references (Swift name + JIRA ID)
- [ ] Applied always-OFF logic at every usage site (kept A-side code)
- [ ] Removed experiment definition from toggle file
- [ ] Removed experiment entries from generated file
- [ ] Traced and removed all dead code (B-side methods, properties, views, tests, imports)
- [ ] Updated remaining tests to remove toggle setup (behavior is now unconditional)
- [ ] Verified zero remaining references
