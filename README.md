# Password Strength Checker

A Python CLI tool and a web interface that evaluates how secure a password is without sending any data anywhere

# Features

- Length analysis — does checks minimum, recommended, and strong thresholds
- Character variety — detects uppercase, lowercase, numbers, and special characters
- Pattern detection — flags repeated characters (i.e. aaa, 111) and sequential patterns (i.e. abc, 123)
- Common password blacklist — warns against the most widely-used passwords
- Strength classification — Weak / Medium / Strong with a score out of 100
- Suggestions — tells you exactly how to improve the password
- Web UI — a browser-based platform, for user interactions

# Project Structure

password-strength-checker
 - password_checker.py   - Python CLI version
 - index.html            - Web interface (open in any browser) 
 - README.md




# How's the Scoring Works

| Criterion                        | Points  |
|----------------------------------|---------|
| Length ≥ 16 characters           | +40     |
| Length ≥ 12 characters           | +30     |
| Length ≥ 8 characters            | +20     |
| Length < 8 characters            | +10     |
| Contains lowercase letters       | +10     |
| Contains uppercase letters       | +10     |
| Contains digits                  | +10     |
| Contains special characters      | +15     |
| Is a commonly-used password      | −40     |
| Has repeated characters (aaa…)   | −10     |
| Has sequential numbers (123…)    | −10     |
| Has sequential letters (abc…)    | −5      |

Final Score → Strength:
- 0–39   =>  Weak
- 40–69  =>  Medium
- 70–100 => Strong
