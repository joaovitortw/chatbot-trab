
# Improved CPF validation
def validate_cpf(cpf: str) -> bool:
    # Validates CPF format and checks for known invalid numbers
    if not is_valid_cpf(cpf):
        raise ValueError("CPF inválido, por favor insira um CPF correto.")
    return True
