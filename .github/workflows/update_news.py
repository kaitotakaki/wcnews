import feedparser
import json
from datetime import datetime

# ================== CẤU HÌNH ==================
FEEDS = [
    "http://feeds.bbci.co.uk/sport/football/rss.xml",           # BBC Football
    "https://www.theguardian.com/football/rss",                 # The Guardian
    "http://www.goal.com/en/feeds/news?fmt=rss",                # Goal.com
    "https://www.skysports.com/rss/football",                   # Sky Sports
    # Thêm nguồn tiếng Việt nếu muốn:
    # "https://vnexpress.net/rss/the-thao.rss",
    # "https://tuoitre.vn/rss/the-thao.rss",
]

KEYWORDS = ["World Cup", "FIFA", "Mundial", "Bàn thắng", "Kết quả", "Worldcup"]  # Lọc tin liên quan

all_news = []

for url in FEEDS:
    try:
        feed = feedparser.parse(url)
        source_name = feed.feed.get("title", "Unknown Source")
        
        for entry in feed.entries:
            title = entry.title
            summary = entry.get("summary", "")
            
            # Lọc tin có từ khóa World Cup
            if any(kw.lower() in (title + summary).lower() for kw in KEYWORDS):
                all_news.append({
                    "title": title,
                    "link": entry.link,
                    "published": entry.get("published", entry.get("updated", datetime.now().isoformat())),
                    "source": source_name,
                    "summary": summary[:300] + "..." if len(summary) > 300 else summary
                })
    except Exception as e:
        print(f"Lỗi khi lấy {url}: {e}")

# Sắp xếp theo thời gian mới nhất
all_news.sort(key=lambda x: x["published"], reverse=True)

# Giới hạn 50 tin mới nhất
data = {
    "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    "total_news": len(all_news),
    "news": all_news[:50]
}

with open("news.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Đã cập nhật {len(data['news'])} tin tức World Cup")
