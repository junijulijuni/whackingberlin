import os
import re

# Define the start and end markers for the protected section
PROTECTED_SECTION_START = "<!-- PROTECTED_SECTION_START -->"
PROTECTED_SECTION_END = "<!-- PROTECTED_SECTION_END -->"

def extract_protected_section(readme_content):
    """Extract the protected section from the README content."""
    pattern = re.compile(
        f"{PROTECTED_SECTION_START}(.*?){PROTECTED_SECTION_END}",
        re.DOTALL
    )
    match = pattern.search(readme_content)
    return match.group(1).strip() if match else None

def generate_toc(path, indent=0):
    """Generate the table of contents for the repository."""
    toc = []
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            if item.startswith('.'):
                continue
            toc.append("  " * indent + f"- [{item}]({item})")
            toc.extend(generate_toc(item_path, indent + 1))
        elif item.endswith('.md') and item != 'README.md':
            toc.append("  " * indent + f"- [{item[:-3]}]({item})")
    return toc

def main():
    # Generate the new TOC
    toc = ["# whacking berlin github", "![Whacking Berlin Logo](wbLogo.JPG "Whacking Berlin Logo")", "## Table of Contents", ""] + generate_toc('.')

    # Read the existing README (if it exists)
    readme_content = ""
    protected_section = None
    if os.path.exists('README.md'):
        with open('README.md', 'r') as f:
            readme_content = f.read()
        protected_section = extract_protected_section(readme_content)

    # Rebuild the README with the new TOC and preserved section
    new_readme = '\n'.join(toc)
    if protected_section:
        new_readme += f"\n\n{PROTECTED_SECTION_START}\n{protected_section}\n{PROTECTED_SECTION_END}"

    # Write the new README
    with open('README.md', 'w') as f:
        f.write(new_readme)

if __name__ == "__main__":
    main()




