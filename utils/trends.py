from pytrends.request import TrendReq

def fetch_trending_topics(country='KE', num_topics=5):
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=["education"], geo=country)
    
    trending = pytrends.trending_searches(pn='kenya')
    topics = trending.head(num_topics)[0].tolist()

    print(f"✅ Top {num_topics} Kenya trends: {topics}")
    return topics
