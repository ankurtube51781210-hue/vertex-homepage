import json
import os

# Load the database
with open('articles.json', 'r') as f:
    articles = json.load(f)

os.makedirs('articles', exist_ok=True)

# 1. Generate Individual Article Pages
article_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | The Vertex</title>
    <meta name="description" content="{excerpt}">
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;500;600&family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
    <style>.page-content {{ max-width: 800px; margin: 4rem auto; padding: 3rem; background: rgba(18, 20, 24, 0.85); backdrop-filter: blur(10px); border: 1px solid var(--border-color); border-radius: 8px; }} img {{ width: 100%; height: 400px; object-fit: cover; border: 1px solid var(--neon-cyan); margin: 2rem 0; }} p {{ margin-bottom: 1.5rem; font-size: 1.1rem; }}</style>
</head>
<body>
    <div class="bg-noise"></div><div class="bg-grid"></div>
    <nav class="navbar"><div class="nav-container"><a href="../index.html" class="logo scramble-text">THE VERTEX</a></div></nav>
    <main class="container">
        <div class="page-content reveal">
            <span class="meta-tag">[{category}]</span>
            <h1 class="headline-xl scramble-text">{title}</h1>
            <img src="{image}" alt="{title}">
            <div class="article-text"><p>{content}</p></div>
            <a href="../index.html" style="color: var(--neon-cyan); font-family: var(--font-mono); text-decoration: none;">[<] RETURN_TO_BASE</a>
        </div>
    </main>
    <script src="../script.js"></script>
</body>
</html>
"""

sitemap_urls = []

for article in articles:
    html_content = article['content'].replace('\\n\\n', '</p><p>')
    html = article_template.format(
        title=article['title'],
        excerpt=article['excerpt'],
        image=article['image'],
        category=article['category'],
        content=html_content
    )
    file_path = f"articles/{article['id']}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    sitemap_urls.append(f"https://ankurtube51781210-hue.github.io/vertex-homepage/{file_path}")

# 2. Generate Category & Archive Pages
category_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} | The Vertex</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;500;600&family=Outfit:wght@700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
    <style>.page-header {{ text-align: center; margin: 4rem 0; }} .article-card {{ background: rgba(18, 20, 24, 0.85); backdrop-filter: blur(10px); border: 1px solid var(--border-color); }}</style>
</head>
<body>
    <div class="bg-noise"></div><div class="bg-grid"></div>
    <nav class="navbar">
        <div class="nav-container">
            <a href="index.html" class="logo scramble-text">THE VERTEX</a>
            <div class="nav-links">
                <a href="tech.html" class="scramble-text">// TECH</a>
                <a href="ai.html" class="scramble-text">// AI</a>
                <a href="crypto.html" class="scramble-text">// CRYPTO</a>
                <a href="business.html" class="scramble-text">// BUSINESS</a>
                <a href="archive.html" class="scramble-text">// ARCHIVE</a>
            </div>
        </div>
    </nav>
    <main class="container">
        <div class="page-header reveal">
            <span class="meta-tag">[SYS.INDEX]</span>
            <h1 class="headline-xl scramble-text">{page_title}</h1>
        </div>
        <section class="latest-grid reveal">
            {article_cards}
        </section>
    </main>
    <script src="script.js"></script>
</body>
</html>
"""

def build_card(article):
    return f"""
    <a href="articles/{article['id']}.html" class="grid-card article-card">
        <div class="image-wrapper"><img src="{article['image']}" alt="News"></div>
        <div class="card-content">
            <span class="meta-tag">[{article['category']}]</span>
            <h3 class="headline-md scramble-text">{article['title']}</h3>
            <p class="excerpt">{article['excerpt']}</p>
        </div>
    </a>
    """

# Map internal categories to page names
categories_map = {
    "tech": [a for a in articles if "TECH" in a['category']],
    "ai": [a for a in articles if "AI" in a['category']],
    "crypto": [a for a in articles if "CRYPTO" in a['category']],
    "business": [a for a in articles if "BIZ" in a['category']],
    "archive": articles # All articles
}

for cat_slug, cat_articles in categories_map.items():
    cards_html = "\\n".join([build_card(a) for a in cat_articles])
    page_title = f"{cat_slug.upper()} NEWS" if cat_slug != "archive" else "THE ARCHIVE"
    
    html = category_template.format(page_title=page_title, article_cards=cards_html)
    with open(f"{cat_slug}.html", 'w', encoding='utf-8') as f:
        f.write(html)
    sitemap_urls.append(f"https://ankurtube51781210-hue.github.io/vertex-homepage/{cat_slug}.html")

# 3. Generate Sitemap.xml
sitemap_template = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {urls}
</urlset>
"""
url_blocks = ""
for url in sitemap_urls:
    url_blocks += f"<url><loc>{url}</loc></url>\\n"

with open('sitemap.xml', 'w', encoding='utf-8') as f:
    f.write(sitemap_template.format(urls=url_blocks))

print("Build Complete! Archive and Category pages generated.")
