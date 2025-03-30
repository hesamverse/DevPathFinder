import json
import difflib

# Load role data
def load_roles(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Load path data
def load_paths(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Load funlines (jokes)
def load_funlines(filepath):
    with open(filepath, "r") as file:
        return json.load(file)

# Ask user for personality keywords
def get_user_input():
    print("Welcome to DevPathFinder 🚀")
    print("Describe yourself with a few keywords (comma-separated):")
    print("Example: creative, organized, bug hunter")
    user_input = input("Your traits: ")
    return [trait.strip().lower() for trait in user_input.split(",")]

# Ask for fun mode
def ask_fun_mode():
    choice = input("🃏 Do you want to activate FUN mode? (yes/no): ").strip().lower()
    return choice == "yes"

# Fuzzy match keywords with weights
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

# Match user traits to role
def match_role_fuzzy(user_traits, roles_data):
    scores = fuzzy_match_keywords_weighted(user_traits, roles_data)
    best_role = max(scores, key=scores.get)
    return best_role, scores[best_role]

# Print fun comebacks based on user traits
def fun_comebacks(user_traits, fun_dict):
    print("\n🤣 Fun Reactions to Your Traits:")
    for trait in user_traits:
        for key in fun_dict:
            if difflib.get_close_matches(trait, [key], n=1, cutoff=0.8):
                print(f"  - {fun_dict[key]}")

# Show learning path and description
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
    fun_dict = load_funlines("data/funlines.json")
    fun_mode = ask_fun_mode()
    user_traits = get_user_input()
    best_role, score = match_role_fuzzy(user_traits, roles_data)

    if score == 0:
        print("\nSorry, we couldn't identify your traits. Try again with different words.")
    else:
        if fun_mode:
            fun_comebacks(user_traits, fun_dict)
        show_path(best_role, roles_data, paths_data, fun_mode)

if __name__ == "__main__":
    main()
