import arxiv
from datetime import datetime, timedelta, timezone
import os
import pandas as pd
from tools.llm_generater import llm_generater_ds
from tools.prompt_template import paper_translator_prompt, paper_review_prompt
from tqdm import tqdm

# --- 配置区 ---
# 1. 定义您的新版组合查询
SEARCH_QUERY = '(cat:cs.CL OR cat:cs.AI OR cat:cs.CV) AND ((ti:"Large Language Model" OR abs:"Large Language Model") OR (ti:"Multimodal Model" OR abs:"Multimodal Model") OR (ti:"Vision Large Language Model" OR abs:"Vision Large Language Model"))'

# 3. 设置获取论文的最大数量
MAX_RESULTS_PER_RUN = 20

# 获取昨天的日期（UTC）
yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date()
START_DATE = datetime(yesterday.year, yesterday.month, yesterday.day, tzinfo=timezone.utc)
END_DATE = datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, tzinfo=timezone.utc)
print(yesterday)

# 生成文件名
paper_name = f"/home/c3205/project/arxiv_daily_paper/paper_info/{yesterday.year}-{yesterday.month}-{yesterday.day}-paperInfo.csv"

def main():
    """主执行函数"""
    print(f"[{datetime.now()}] 开始执行多模态与大模型论文跟踪...")
    print(f"查询语句: {SEARCH_QUERY}")

    search = arxiv.Search(
        query=SEARCH_QUERY,
        max_results=MAX_RESULTS_PER_RUN,
        sort_by=arxiv.SortCriterion.LastUpdatedDate
    )
    
    client = arxiv.Client()
    results = []
    for result in client.results(search):
        published_date = result.published
        if START_DATE <= published_date <= END_DATE:
            results.append(result)

    # 检查已存在的paper_id，避免重复写入
    existing_ids = set()
    if os.path.exists(paper_name):
        try:
            existing_df = pd.read_csv(paper_name)
            existing_ids = set(existing_df['paper_id'].astype(str))
        except Exception:
            pass

    for result in tqdm(list(results), desc="Processing papers"):
        paper_id = result.get_short_id()
        if paper_id in existing_ids:
            continue  # 跳过已写入的论文

        result_dict = {
            'paper_id': paper_id,
            'title': result.title,
            'categories': result.categories,
            'published': result.published.strftime('%Y-%m-%d'),
            'pdf_url': result.pdf_url,
            'summary': result.summary
        }
        try:
            summary_zh = llm_generater_ds(paper_translator_prompt(result.summary))
            result_dict['summary_zh'] = summary_zh
        except Exception as e:
            print(f"Error translating paper {result.title}: {e}")
            result_dict['summary_zh'] = '-'

        try:
            score = llm_generater_ds(paper_review_prompt(result.title, result.summary))
            result_dict['score'] = score
        except Exception as e:
            print(f"Error reviewing paper {result.title}: {e}")
            result_dict['score'] = '-'

        # 写入一行到CSV
        df_row = pd.DataFrame([result_dict])
        write_header = not os.path.exists(paper_name) or os.path.getsize(paper_name) == 0
        df_row.to_csv(paper_name, mode='a', header=write_header, index=False, encoding="utf-8")

if __name__ == "__main__":
    main()