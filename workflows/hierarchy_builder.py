from collections import deque
from workflows.user_registration import register_and_upgrade
import logging

def build_hierarchy(users, start_referral, children_per_parent=3, max_levels=3, headless=False):
    results = []
    queue = deque([(start_referral, 1)])
    idx = 0
    while queue and idx < len(users):
        parent, level = queue.popleft()
        if level > max_levels:
            break
        for _ in range(children_per_parent):
            if idx >= len(users):
                break
            user = users[idx]
            logging.info(f"Registering user {user.get('Email')} under {parent} (level={level})")
            new_ref, plan = register_and_upgrade(user, parent, headless=False)
            results.append((user, parent, new_ref, level, plan))
            if new_ref:
                queue.append((new_ref, level+1))
            idx += 1
    return results
