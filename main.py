from utils.trends import fetch_trending_topics
from utils.generator import generate_elimuhub_post
from utils.blogger import publish_post

def main():
    print("📊 Fetching trending topics in Kenya...")
    topics = fetch_trending_topics()

    for topic in topics:
        print(f"\n📝 Generating Elimuhub content for: {topic}")
        title, content, tags = generate_elimuhub_post(topic)

        print(f"🚀 Publishing blog post: {title}")
        publish_post(title, content, tags)

if __name__ == "__main__":
    main()
