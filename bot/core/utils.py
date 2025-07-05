def parse_max_quantity(qty: str) -> tuple[str, int | None]:
    qty = str(qty).strip().lower()

    if qty == 'есть':
        return 'any', None

    if qty.startswith('<'):
        try:
            value = int(qty[1:])
            return 'lt', value
        except ValueError:
            pass

    if qty.startswith('>'):
        return 'any', None

    try:
        value = int(qty)
        return 'max', value
    except ValueError:
        pass

    return 'any', None
