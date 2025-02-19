def filter_names_branches(branches_list: list[dict], target: str) -> bool:
    for item in branches_list:
        if target in item.keys():
            return True
        else:
            return False
