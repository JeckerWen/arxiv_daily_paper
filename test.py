import arxiv
from datetime import datetime, timezone

# 查询设置
SEARCH_QUERY = '(cat:cs.CL OR cat:cs.AI OR cat:cs.CV) AND ((ti:"Large Language Model" OR abs:"Large Language Model") OR (ti:"Multimodal Model" OR abs:"Multimodal Model") OR (ti:"Vision Large Language Model" OR abs:"Vision Large Language Model"))'
MAX_RESULTS_PER_RUN = 100

# 时间范围（加上 tzinfo=timezone.utc）
START_DATE = datetime(2024, 6, 1, tzinfo=timezone.utc)
END_DATE = datetime(2024, 6, 30, tzinfo=timezone.utc)

# 创建搜索对象
search = arxiv.Search(
    query=SEARCH_QUERY,
    max_results=MAX_RESULTS_PER_RUN,
    sort_by=arxiv.SortCriterion.LastUpdatedDate
)

client = arxiv.Client()
results = []
for result in client.results(search):
    published_date = result.published
    print(published_date)
    if START_DATE <= published_date <= END_DATE:
        results.append(result)

# 打印结果
for r in results:
    print(f"Title: {r.title}")
    print(f"Published: {r.published.strftime('%Y-%m-%d')}")
    print(f"URL: {r.entry_id}")
    print('-' * 40)
