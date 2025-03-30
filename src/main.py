import json
import difflib

def ask_fun_mode():
    choice = input("🃏 Do you want to activate FUN mode? (yes/no): ").strip().lower()
    return choice == "yes"

# Load role data
def load_roles(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Load path data
def load_paths(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Ask user for personality keywords
def get_user_input():
    print("Welcome to DevPathFinder 🚀")
    print("Describe yourself with a few keywords (comma-separated):")
    print("Example: creative, organized, bug hunter")
    user_input = input("Your traits: ")
    return [trait.strip().lower() for trait in user_input.split(",")]

# Fuzzy match each user input against known keywords
def fuzzy_match_keywords_weighted(user_traits, roles_data, threshold=0.7):
    role_scores = {role: 0 for role in roles_data}

    for trait in user_traits:
        for role, data in roles_data.items():
            keywords = data["keywords"]
            for keyword, weight in keywords.items():
                match = difflib.get_close_matches(trait, [keyword], n=1, cutoff=threshold)
                if match:
                    role_scores[role] += weight
    return role_scores

# Match user input to roles
def match_role(user_traits, roles_data):
    scores = {}
    for role, data in roles_data.items():
        keywords = data["keywords"]
        match_count = sum(1 for trait in user_traits if trait in keywords)
        scores[role] = match_count
    best_role = max(scores, key=scores.get)
    return best_role, scores[best_role]

# Show learning path
def match_role_fuzzy(user_traits, roles_data):
    scores = fuzzy_match_keywords_weighted(user_traits, roles_data)
    best_role = max(scores, key=scores.get)
    return best_role, scores[best_role]

    for keyword, role in matches:
        role_scores[role] += 1

    best_role = max(role_scores, key=role_scores.get)
    return best_role, role_scores[best_role]

# Show learning path and role description
def show_path(role, roles_data, paths_data, fun_mode=False):
    if fun_mode:
        jokes = {
            "backend": "You’re the silent warrior. People don’t see your work, but nothing runs without you.",
            "frontend": "You probably spend 80% of your time fixing that one pixel that’s off.",
            "security": "You don't trust your own toaster. And you’re probably right."
        }
        print(f"\n🕶️ FUN MODE ENABLED")
        print(f"🎭 Your vibe is: {role.upper()}")
        print(f"{jokes[role]}\n")
        print("📚 But seriously, here's a learning path in case you stop joking:")
    else:
        print(f"\n🔍 Suggested role: {role.upper()}")
        print(f"{roles_data[role]['description']}\n")
        print("📘 Recommended Learning Path:")
    
    for step in paths_data[role]:
        print(f"  - {step}")

# Main logic
def main():
    roles_data = load_roles("data/roles.json")
    paths_data = load_paths("data/paths.json")
    fun_mode = ask_fun_mode()
    user_traits = get_user_input()
    best_role, score = match_role_fuzzy(user_traits, roles_data)

    if score == 0:
        print("\nSorry, we couldn't identify your traits. Try again with different words.")
    else:
        show_path(best_role, roles_data, paths_data, fun_mode)

if __name__ == "__main__":
    main()
