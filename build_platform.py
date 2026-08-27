import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update index.html
content_index = content.replace('<a href="#">Platform</a>', '<a href="platform.html">Platform</a>')

# Update Logo to be a link
content_index = content_index.replace('<div class="logo">', '<a href="index.html" class="logo" style="text-decoration: none;">')
content_index = content_index.replace('            </div>\n            <div class="nav-links">', '            </a>\n            <div class="nav-links">')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content_index)

# Create platform.html
lines = content_index.split('\n')
nav_end_idx = -1
footer_start_idx = -1

for i, line in enumerate(lines):
    if '</nav>' in line and nav_end_idx == -1:
        nav_end_idx = i
    if '<footer' in line and footer_start_idx == -1:
        footer_start_idx = i

# Inject a placeholder main content
placeholder = """
        <!-- PLATFORM MAIN -->
        <main style="min-height: 80vh; padding: 120px 5% 50px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
            <h1 style="font-size: 3rem; margin-bottom: 20px;">Platform</h1>
            <p style="color: var(--text-muted); max-width: 600px; font-size: 1.1rem;">This section is currently under development. Soon it will be populated with new AI tools and solutions.</p>
        </main>
"""

if nav_end_idx != -1 and footer_start_idx != -1:
    platform_lines = lines[:nav_end_idx+1] + placeholder.strip('\n').split('\n') + lines[footer_start_idx:]
    platform_content = '\n'.join(platform_lines)
    platform_content = platform_content.replace('DSE Marketing Solutions - Home', 'DSE Marketing Solutions - Platform')

    with open('platform.html', 'w', encoding='utf-8') as f:
        f.write(platform_content)
    print("Successfully created platform.html and updated index.html")
else:
    print(f"Error: nav_end_idx={nav_end_idx}, footer_start_idx={footer_start_idx}")
