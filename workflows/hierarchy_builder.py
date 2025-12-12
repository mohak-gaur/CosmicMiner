from collections import deque
from workflows.user_registration import register_and_upgrade
import logging
from collections import defaultdict

def build_hierarchy(users, start_referral, children_per_parent=3, max_levels=3, headless=False):
    results = []
    queue = deque([(start_referral, 1)])
    idx = 0
    child_counter = defaultdict(int)  # track per-parent child index

    while queue and idx < len(users):
        parent, level = queue.popleft()
        if level > max_levels:
            break

        for _ in range(children_per_parent):
            if idx >= len(users):
                break

            user = users[idx]
            # Increment count for this parent
            child_counter[parent] += 1
            user_index = child_counter[parent]  # 1, 2, 3

            logging.info(f"Registering user {user.get('Email')} under {parent} "
                         f"(level={level}, child_index={user_index})")

            # Pass user_index for 40-30-30 split logic
            new_ref, plan = register_and_upgrade(user, parent, user_index=user_index, headless=headless)
            results.append((user, parent, new_ref, level, plan))

            if new_ref:
                queue.append((new_ref, level + 1))

            idx += 1

    return results