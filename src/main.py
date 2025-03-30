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

# Ask user for personality keywords
def get_user_input():
    print("Welcome to DevPathFinder 🚀")
    print("Describe yourself with a few keywords (comma-separated):")
    print("Example: creative, organized, bug hunter")
    user_input = input("Your traits: ")
    return [trait.strip().lower() for trait in user_input.split(",")]

# Fuzzy match each user input against known keywords
def fuzzy_match_keywords(user_traits, roles_data, threshold=0.7):
    matched_traits = []
    all_keywords = {
        role: roles_data[role]["keywords"] for role in roles_data
    }
    for trait in user_traits:
        for role, keywords in all_keywords.items():
            match = difflib.get_close_matches(trait, keywords, n=1, cutoff=threshold)
            if match:
                matched_traits.append((match[0], role))
    return matched_traits

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
    role_scores = {role: 0 for role in roles_data}
    matches = fuzzy_match_keywords(user_traits, roles_data)

    for keyword, role in matches:
        role_scores[role] += 1

    best_role = max(role_scores, key=role_scores.get)
    return best_role, role_scores[best_role]

# Show learning path and role description
def show_path(role, roles_data, paths_data):
    print(f"\n🔍 Suggested role: {role.upper()}")
    print(f"{roles_data[role]['description']}\n")
    print("📘 Recommended Learning Path:")
    for step in paths_data[role]:
        print(f"  - {step}")

# Main logic
def main():
    roles_data = load_roles("data/roles.json")
    paths_data = load_paths("data/paths.json")
    user_traits = get_user_input()
    best_role, score = match_role_fuzzy(user_traits, roles_data)
    
    if score == 0:
        print("\nSorry, we couldn't identify your traits. Try again with different words.")
    else:
        show_path(best_role, roles_data, paths_data)

if __name__ == "__main__":
    main()
