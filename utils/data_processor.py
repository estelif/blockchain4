def process_coin_data(coin_data):
    if not coin_data:
        return None
    
    quote = coin_data.get("quote", {}).get("USD", {})
    
    return {
        "name": coin_data.get("name"),
        "symbol": coin_data.get("symbol"),
        "rank": coin_data.get("cmc_rank"),
        "price": quote.get("price"),
        "market_cap": quote.get("market_cap"),
        "volume_24h": quote.get("volume_24h"),
        "percent_change_1h": quote.get("percent_change_1h"),
        "percent_change_24h": quote.get("percent_change_24h"),
        "percent_change_7d": quote.get("percent_change_7d"),
        "last_updated": quote.get("last_updated")
    }

def process_news_data(news_items):
    processed_news = []
    for item in news_items:
        processed_news.append({
            "title": item.get("title"),
            "url": item.get("url"),
            "source": item.get("source", {}).get("title"),
            "published_at": item.get("published_at"),
            "votes": item.get("votes", {}).get("positive", 0)
        })
    return sorted(processed_news, key=lambda x: x["votes"], reverse=True)