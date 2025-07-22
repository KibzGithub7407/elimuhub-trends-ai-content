import os
import datetime

def publish_post(title, content, tags):
    # 🔧 Replace this with Blogger API later
    today = datetime.date.today().isoformat()
    filename = f"logs/{today}_{title.replace(' ', '_')[:50]}.html"

    html_content = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
        <h1>{title}</h1>
        <p><em>Tags: {tags}</em></p>
        <div>{content}</div>
    </body>
    </html>
    """

    os.makedirs("logs", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"📁 Saved post to: {filename}")
