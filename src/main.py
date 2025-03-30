import json

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
    best_role, score = match_role(user_traits, roles_data)
    
    if score == 0:
        print("\nSorry, we couldn't identify your traits. Try again with different words.")
    else:
        show_path(best_role, roles_data, paths_data)

if __name__ == "__main__":
    main()
