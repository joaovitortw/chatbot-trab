import re

CPF_RE_DIGITS = re.compile(r"\D+")
EMAIL_SIMPLE_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def only_digits(s: str) -> str:
    return CPF_RE_DIGITS.sub("", s or "")

def format_cpf_mask(cpf_digits: str) -> str:
    d = only_digits(cpf_digits).zfill(11)[:11]
    return f"{d[0:3]}.{d[3:6]}.{d[6:9]}-{d[9:11]}"

def is_valid_cpf(cpf: str) -> bool:
    d = only_digits(cpf)
    if len(d) != 11 or d == d[0] * 11:
        return False
    s = sum(int(d[i]) * (10 - i) for i in range(9))
    dv1 = (s * 10) % 11
    if dv1 == 10: dv1 = 0
    s = sum(int(d[i]) * (11 - i) for i in range(10))
    dv2 = (s * 10) % 11
    if dv2 == 10: dv2 = 0
    return dv1 == int(d[9]) and dv2 == int(d[10])

def validate_email(email: str) -> bool:
    return bool(email and EMAIL_SIMPLE_RE.match(email))
