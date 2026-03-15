from logic_utils import check_guess, update_score, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

# --- Tests targeting the bugs that were fixed ---

# Bug 1: update_score was adding +5 on even-numbered attempts for "Too High"
# instead of always subtracting 5.
def test_update_score_too_high_even_attempt_subtracts():
    # On an even attempt number (2), "Too High" must still deduct 5 points.
    # The original code returned current_score + 5 when attempt_number % 2 == 0.
    result = update_score(100, "Too High", 2)
    assert result == 95, "Too High on an even attempt should subtract 5, not add 5"

def test_update_score_too_high_odd_attempt_subtracts():
    result = update_score(100, "Too High", 3)
    assert result == 95

def test_update_score_too_high_always_subtracts():
    # Verify the deduction is consistent across several attempt numbers.
    for attempt in range(1, 7):
        result = update_score(100, "Too High", attempt)
        assert result == 95, f"Too High on attempt {attempt} should always subtract 5"

# Bug 2: get_range_for_difficulty returned (1, 50) for "Hard" instead of (1, 200).
def test_hard_difficulty_range():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200, f"Hard difficulty upper bound should be 200, got {high}"
