# Game Glitch Investigator — Bug Analysis & Fix Plan

## Context
`logic_utils.py` has stub `NotImplementedError` placeholders for all 4 game logic functions. The tests in `tests/test_game_logic.py` import from `logic_utils`, so they fail until the stubs are implemented. `app.py` also contains several bugs to investigate and fix.

---

## Bugs Found in app.py

### Bug 1 — CRITICAL: `check_guess` hints are inverted ([app.py:38-41](app.py))
```python
if guess > secret:
    return "Too High", "📈 Go HIGHER!"   # ← wrong! should be Go LOWER
else:
    return "Too Low", "📉 Go LOWER!"     # ← wrong! should be Go HIGHER
```
If your guess is *above* the secret, the correct hint is "Go LOWER", not "Go HIGHER". The messages are swapped.

**Fix:** Swap the messages:
- `"Too High"` → `"📉 Go LOWER!"`
- `"Too Low"` → `"📈 Go HIGHER!"`

---

### Bug 2 — CRITICAL: Secret type-switches every even attempt ([app.py:159-162](app.py))
```python
if st.session_state.attempts % 2 == 0:
    secret = str(st.session_state.secret)   # ← converts to string!
else:
    secret = st.session_state.secret
```
On even attempts, the secret becomes a string. `check_guess` then compares `int` vs `str`, triggers the TypeError fallback, and uses *lexicographic* string comparison — e.g., `"9" > "50"` because `"9" > "5"`. This causes completely wrong outcomes.

**Fix:** Always pass the integer secret: `secret = st.session_state.secret`

---

### Bug 3 — Hard difficulty range is easier than Normal ([app.py:10](app.py))
```python
if difficulty == "Hard":
    return 1, 50    # ← range of 50, smaller than Normal's 100 = easier!
```
Hard should be *harder* (larger range = harder to guess).

**Fix:** Change Hard range to `1, 200`.

---

### Bug 4 — UI hardcodes "1 to 100" regardless of difficulty ([app.py:111](app.py))
```python
st.info(f"Guess a number between 1 and 100. ...")
```
Ignores `low` and `high` variables already computed above.

**Fix:** `f"Guess a number between {low} and {high}. ..."`

---

### Bug 5 — New Game ignores difficulty ([app.py:137](app.py))
```python
st.session_state.secret = random.randint(1, 100)
```
Always uses 1–100 even on Easy (1–20) or Hard.

**Fix:** Use `random.randint(low, high)` instead.

---

### Bug 6 — `attempts` starts at 1 but resets to 0 ([app.py:97](app.py) vs [app.py:136](app.py))
Initial session state sets `attempts = 1`, but New Game resets to `0`. They should both use `0`.

**Fix:** Change line 97 to `st.session_state.attempts = 0`.

---

### Bug 8 — Changing difficulty does not reset the secret ([app.py:35-36](app.py))
```python
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
```
The secret is only generated once on first load. Switching difficulty leaves the old secret (and game state) unchanged, so the secret may be outside the new difficulty's range.

**Fix:** Track `st.session_state.difficulty` and regenerate the secret (plus reset all game state) whenever the selected difficulty differs from the stored one.

---

### Bug 7 — `update_score` rewards wrong "Too High" guesses ([app.py:58-61](app.py))
```python
if outcome == "Too High":
    if attempt_number % 2 == 0:
        return current_score + 5    # ← adds points for a wrong guess!
    return current_score - 5
```
**Fix:** Always subtract for wrong guesses: `return current_score - 5`.

---

## Refactoring Task: Populate logic_utils.py

Move the corrected versions of all 4 functions into `logic_utils.py`:

| Function | Changes needed |
|---|---|
| `get_range_for_difficulty` | Copy + fix Bug 3 (Hard range) |
| `parse_guess` | Copy as-is |
| `check_guess` | Copy + fix Bug 1 + **return only outcome string**, not tuple |
| `update_score` | Copy + fix Bug 7 |

> **Important:** Tests expect `check_guess` to return just `"Win"` / `"Too High"` / `"Too Low"` — not the `("Win", "🎉 Correct!")` tuple that `app.py` currently returns.

Then update `app.py` to:
1. Import the 4 functions from `logic_utils`
2. Remove the inline function definitions
3. Apply fixes for Bugs 2, 4, 5, 6 in the UI/game loop code

---

## Files to Modify
- [`logic_utils.py`](logic_utils.py) — implement all 4 functions (with fixes)
- [`app.py`](app.py) — import from logic_utils + fix Bugs 2, 4, 5, 6
- [`conftest.py`](conftest.py) — already created (fixes the pytest import path)

## Verification
1. `pytest tests/test_game_logic.py` — all 3 tests should pass
2. `streamlit run app.py` and verify:
   - Hints say "Go LOWER" when guess is too high (and vice versa)
   - Hard difficulty uses a larger range than Normal
   - UI shows correct range for each difficulty
   - New Game respects the selected difficulty