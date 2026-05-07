import re


MIN_LENGTH = 8
GOOD_LENGTH = 12
STRONG_LENGTH = 16

WEAK_THRESHOLD = 40
MEDIUM_THRESHOLD = 70


COMMON_PASSWORDS = {
    "password", "123456", "12345678", "password1", "qwerty",
    "abc123", "111111", "letmein", "welcome", "monkey",
    "dragon", "master", "sunshine", "princess", "football",
    "iloveyou", "admin", "login", "passw0rd", "123456789",
}


def analyze_password(password: str) -> dict:

    checks = {}
    suggestions = []
    score = 0

    length = len(password)

    checks["length_ok"] = length >= MIN_LENGTH
    checks["length_good"] = length >= GOOD_LENGTH
    checks["length_strong"] = length >= STRONG_LENGTH

    if length < MIN_LENGTH:
        score += 10
        suggestions.append(
            f"Too short ({length} chars). Use at least {MIN_LENGTH} characters."
        )

    elif length < GOOD_LENGTH:
        score += 20
        suggestions.append(
            f"Consider making it longer ({length} chars). "
            f"{GOOD_LENGTH}+ characters is recommended."
        )

    elif length < STRONG_LENGTH:
        score += 30

    else:
        score += 40

    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(
        re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?`~]", password)
    )

    checks["has_lowercase"] = has_lower
    checks["has_uppercase"] = has_upper
    checks["has_digit"] = has_digit
    checks["has_special"] = has_special

    if has_lower:
        score += 10
    else:
        suggestions.append("Add lowercase letters (a-z).")

    if has_upper:
        score += 10
    else:
        suggestions.append("Add uppercase letters (A-Z).")

    if has_digit:
        score += 10
    else:
        suggestions.append("Include at least one number (0-9).")

    if has_special:
        score += 15
    else:
        suggestions.append("Add a special character (e.g. @, #, $, !, %).")

    is_common = password.lower() in COMMON_PASSWORDS

    checks["not_common"] = not is_common

    if is_common:
        score = max(0, score - 40)

        suggestions.insert(
            0,
            "This is a very commonly used password - avoid it entirely!"
        )

    has_repeat = bool(re.search(r"(.)\1{2,}", password))

    has_seq_nums = any(
        str(i) + str(i + 1) + str(i + 2) in password
        for i in range(0, 8)
    )

    has_seq_alpha = any(
        chr(c) + chr(c + 1) + chr(c + 2) in password.lower()
        for c in range(ord("a"), ord("x") + 1)
    )

    checks["no_repeats"] = not has_repeat
    checks["no_seq_numbers"] = not has_seq_nums
    checks["no_seq_alpha"] = not has_seq_alpha

    if has_repeat:
        score = max(0, score - 10)
        suggestions.append(
            "Avoid repeated characters (e.g. 'aaa', '111')."
        )

    if has_seq_nums:
        score = max(0, score - 10)
        suggestions.append(
            "Avoid sequential numbers (e.g. '123', '456')."
        )

    if has_seq_alpha:
        score = max(0, score - 5)
        suggestions.append(
            "Avoid sequential letters (e.g. 'abc', 'xyz')."
        )

    score = min(100, max(0, score))

    if score < WEAK_THRESHOLD:
        strength = "Weak"

    elif score < MEDIUM_THRESHOLD:
        strength = "Medium"

    else:
        strength = "Strong"

    if not suggestions:
        suggestions.append(
            "Great password! No obvious weaknesses found."
        )

    return {
        "score": score,
        "strength": strength,
        "checks": checks,
        "suggestions": suggestions,
    }


STRENGTH_STYLES = {
    "Weak": "WEAK",
    "Medium": "MEDIUM",
    "Strong": "STRONG",
}


def _bar(score: int) -> str:
    filled = round(score / 100 * 35)
    return "#" * filled + "-" * (35 - filled)


def print_report(password: str, report: dict) -> None:

    score = report["score"]
    strength = report["strength"]
    checks = report["checks"]
    suggs = report["suggestions"]

    style = STRENGTH_STYLES[strength]

    print("\n" + "═" * 50)
    print("PASSWORD STRENGTH REPORT")
    print("═" * 50)

    print(f"  Strength : {style}  {strength}")
    print(f"  Score    : {score}/100")
    print(f"  Progress : [{_bar(score)}]")

    print()
    print("  CHECKS:")

    check_labels = {
        "length_ok": f"Minimum length ({MIN_LENGTH}+)",
        "length_good": f"Recommended length ({GOOD_LENGTH}+)",
        "length_strong": f"Strong length ({STRONG_LENGTH}+)",
        "has_lowercase": "Contains lowercase letters",
        "has_uppercase": "Contains uppercase letters",
        "has_digit": "Contains numbers",
        "has_special": "Contains special characters",
        "not_common": "Not a commonly-used password",
        "no_repeats": "No repeated characters",
        "no_seq_numbers": "No sequential numbers",
        "no_seq_alpha": "No sequential letters",
    }

    for key, label in check_labels.items():

        icon = "[OK]" if checks.get(key) else "[X]"

        print(f"    {icon} {label}")

    print()
    print("  SUGGESTIONS:")

    for s in suggs:
        print(f"    - {s}")

    print("═" * 50 + "\n")


def main():

    print("\nWelcome to the Password Strength Checker")
    print("Type 'quit' or press Ctrl+C to exit.\n")

    while True:

        try:
            password = input("Enter a password to check: ")

        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! Stay secure.\n")
            break

        if password.lower() == "quit":
            print("\nGoodbye! Stay secure.\n")
            break

        if not password:
            print("Please enter a password.\n")
            continue

        report = analyze_password(password)

        print_report(password, report)

        again = input("Check another password? (y/n): ").strip().lower()

        if again != "y":
            print("\nGoodbye! Stay secure.\n")
            break

        print()


if __name__ == "__main__":
    main()