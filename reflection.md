# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

What did the game look like the first time you ran it?

  When I first ran the app, it looked like a normal guessing game but immediately felt off. The hints were giving the opposite direction like if I guessed a number that was too low, it said "Go LOWER!" instead of "Go HIGHER!" Every other guess, the secret number seemed to silently change type (alternating between int and string), which made comparisons unpredictable. The score would sometimes go up even when I guessed wrong, which made no sense.

List at least two concrete bugs you noticed at the start
  (for example: "the secret number kept changing" or "the hints were backwards").
  1. The game gave inconsistent response based on input — for example, entering "3" when the secret was 50 said "Go LOWER" (the hints were completely backwards).
  2. Inconsistent score values — the score sometimes increased on wrong guesses because the original `update_score` added 5 points on even numbered attempts for "Too High" instead of always subtracting 5.

---

## 2. How did you use AI as a teammate?

Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  Claude

Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude suggested using `if "secret" not in st.session_state` before generating the random number to prevent it from regenerating on every rerun. I verified this by opening the Developer Debug Info expander and confirming the secret stayed the same across multiple guesses without a "New Game" click. Before the fix, the secret visibly changed in the debug panel every time I interacted with the page.

Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  Claude initially suggested fixing the hint direction by swapping the emoji labels in `check_guess` itself, but the real bug was that `check_guess` was returning the wrong _outcome string_ for the hint map to look up. I verified by running the app and seeing the hints were still wrong I had to trace through the code carefully to find the hint_map in `app.py` was correct, but the original function was paired with the wrong messages inline.

---

## 3. Debugging and testing your fixes

How did you decide whether a bug was really fixed?

  I decided a bug was fixed when I could reproduce the original bad behavior and confirm it no longer happened. For the hints, I picked a secret number from the debug panel, then guessed above and below it to verify the directions were right. For the score bug, I watched the score counter across multiple wrong guesses and confirmed it only ever went down, never up unexpectedly.

Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

  I ran `pytest` against the `check_guess` function directly by writing a few calls in a test file. for example, `assert check_guess(10, 50) == "Too Low"` and `assert check_guess(80, 50) == "Too High"`. This showed me the logic itself was correct after the fix, and helped me confirm that the original bug was in how the secret was passed (alternating int/string) rather than in the comparison logic.

Did AI help you design or understand any tests? How?

  Yes — Claude suggested testing `check_guess` and `update_score` in isolation rather than through the full Streamlit UI. That was a useful frame: it made me realize I could verify the pure logic functions with simple assertions before worrying about whether the UI was calling them correctly.

---

## 4. What did you learn about Streamlit and state?

In your own words, explain why the secret number kept changing in the original app.

  Streamlit reruns the entire Python script from top to bottom every time a user interacts with the page a button click, a text input, anything. In the buggy version, `random.randint()` was called unconditionally at the top of the script, so a brand new secret was generated on every single rerun. Nothing was storing or protecting the value between runs.

How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Imagine your Python script is a recipe that gets cooked from scratch every time someone touches the stove knob all variables reset. Session state is like a sticky note on the fridge: you write a value there once and it survives even when the recipe runs again. So wrapping initialization in `if "secret" not in st.session_state` tells Streamlit "only do this the very first time, then leave it alone."

What change did you make that finally gave the game a stable secret number?

  I wrapped the `random.randint()` call in a guard: `if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high)`. That means the secret is generated exactly once on the first page load. Every subsequent rerun finds the key already in session state and skips the line entirely.

---

## 5. Looking ahead: your developer habits

What is one habit or strategy from this project that you want to reuse in future labs or projects?

  Reading the `git diff` before writing anything new. Seeing exactly what changed in `app.py` and `logic_utils.py` gave me a concrete map of the bugs without guessing. I want to use that as a starting point on every debugging task.

What is one thing you would do differently next time you work with AI on a coding task?

  I would test AI suggestions manually before accepting them, especially for logic bugs. Claude gave me the right direction on session state but was off on where the hint bug actually lived running the app for 30 seconds would have caught that faster than debating it.

In one or two sentences, describe how this project changed the way you think about AI generated code.

  AI generated code can look totally convincing and still have subtle logical errors that only show up at runtime. I now treat AI output as a strong first draft that still needs my eyes on it not a finished product.
