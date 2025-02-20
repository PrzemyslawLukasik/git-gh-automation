def filter_names(branches_list: list[dict], target: str) -> bool:
    for item in branches_list:
        if target in item.values():
            return True
    return False
