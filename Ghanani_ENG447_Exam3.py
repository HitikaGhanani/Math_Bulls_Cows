import random

print("===== BULLS AND COWS GAME RULES =====")
print("1. The computer chooses a secret 4 digit number.")
print("2. All digits in the secret number are different.")
print("3. The secret number cannot start with 0.")
print("4. Your guesses must also follow the same rules:")
print(" It should be exactly 4 digits, with no digits repeating itself and it cannot start with a 0.")
print("5. After each guess, you will get:")
print("     - Bulls: correct digit in the correct position")
print("     - Cows:  correct digit but in the wrong position")
print("6. Your goal is to find the secret number.")
print("7. Also, entropy will be shown before and after each guess.")
print("========================================\n")


# This function is making computer choose a secret code or number

def generate_secret_code():
    digits = list("0123456789")

    # choose first digit (1–9) 
    # First digit should not be zero for a number to be a our digit number
    first = random.choice(digits[1:])
    digits.remove(first)

    # choose second digit
    second = random.choice(digits)
    digits.remove(second)

    # choose third digit
    third = random.choice(digits)
    digits.remove(third)

    # choose fourth digit
    fourth = random.choice(digits)

    return first + second + third + fourth


# Bulls and cows logic:

# Bulls and cows calculation

def bulls_cows(secret: str, guess: str):
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(i in secret for i in guess) - bulls
    return bulls, cows


# Function to calculate all possible secret codes
def generate_candidates_simple():
    candidates = []
    for a in "123456789":        # first digit cannot be zero
        for b in "0123456789":
            if b == a: continue
            for c in "0123456789":
                if c in (a, b): continue
                for d in "0123456789":
                    if d in (a, b, c): continue
                    candidates.append(a + b + c + d)
    return candidates

# Function to Validate a user guess
def valid_guess(g: str) -> bool:
    return g.isdigit() and len(g)==4 and len(set(g))==4 and g[0]!="0"

# Entropy of uncertainty set [H(S) = log₂|S|]
import math
def entropy(cs):  # cs is candidate set
    return math.log2(len(cs)) if cs else 0.0

# Filter candidates after feedback
def filter_candidates(cs, guess, b, c):
    return [s for s in cs if bulls_cows(s, guess) == (b, c)]

def partition_by_feedback(cs, guess):
    parts = {}
    for s in cs:
        r = bulls_cows(s, guess)
        parts.setdefault(r, []).append(s)
    return parts
# How many different feedback results could possibly happen


def expected_info_gain(cs, guess):
    if not cs:
        return 0.0
    H = entropy(cs)
    parts = partition_by_feedback(cs, guess)
    total = len(cs)
    exp_post = 0.0
    for subset in parts.values():
        p = len(subset) / total
        exp_post += p * math.log2(len(subset))
    return H - exp_post

def best_guess(cs, search_space=None):
    if not cs:
        return None, 0.0
    if search_space is None:
        search_space = cs  
    best_g, best_ig = None, -1.0
    for g in search_space:
        ig = expected_info_gain(cs, g)
        if ig > best_ig:
            best_g, best_ig = g, ig
    return best_g, best_ig


# Main game code 
def play():    
    S = generate_candidates_simple()
    secret = generate_secret_code()
    print("The computer has already chosen its secret number.")
    print("Guess the 4 digit secret number. Type 'quit' to exit.\n")

    turn = 1
    while True:
        guess = input(f"[Turn {turn}] Enter your guess: ").strip()

        if guess.lower() in {"q", "quit", "exit"}:
            print("Bye!")
            break

        if not valid_guess(guess):
            print("Invalid: 4 digits, no repeats, no leading zero.\n")
            continue

        # feedback
        b, c = bulls_cows(secret, guess)
        print(f"Result → Bulls: {b}, Cows: {c}")

        # update candidate set
        S = filter_candidates(S, guess, b, c)

        # show entropy before and after the guess
        H_before = entropy(S)
        H_after = entropy(S)
        print(f"Entropy after this guess: {H_after:.3f} bits")
        print(f"Realized information gain: {H_before - H_after:.3f} bits\n")

        # check win
        if b == 4:
            print(f"Correct! The secret was {secret}. You solved it in {turn} turns.")
            break

        # safety edge case
        if not S:
            print("No possible candidates remain. Check your rules.")
            break

        turn += 1

play()