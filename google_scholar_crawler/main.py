# from scholarly import scholarly
# import jsonpickle
# import json
# from datetime import datetime
# import os

# author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
# scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
# name = author['name']
# author['updated'] = str(datetime.now())
# author['publications'] = {v['author_pub_id']:v for v in author['publications']}
# print(json.dumps(author, indent=2))
# os.makedirs('results', exist_ok=True)
# with open(f'results/gs_data.json', 'w') as outfile:
#     json.dump(author, outfile, ensure_ascii=False)

# shieldio_data = {
#   "schemaVersion": 1,
#   "label": "citations",
#   "message": f"{author['citedby']}",
# }
# with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
#     json.dump(shieldio_data, outfile, ensure_ascii=False)


import requests
import json
import os
import re

def get_citations():
    # 你的 Google Scholar ID
    scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID', '5Rh3yn4AAAAJ')
    url = f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
    
    # 伪装成普通浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    # 用正则精准提取引用总数
    match = re.search(r'Citations</a></td><td class="gsc_rsb_std">(\d+)</td>', response.text)
    
    if match:
        citations = match.group(1)
        # 确保 results 文件夹存在
        os.makedirs('results', exist_ok=True)
        
        # 专门为 Shields.io Badge 生成的 JSON 格式
        shieldio_data = {
          "schemaVersion": 1,
          "label": "citations",
          "message": citations,
          "color": "9cf"
        }
        with open('results/gs_data_shieldsio.json', 'w') as f:
            json.dump(shieldio_data, f)
        print(f"🎉 成功抓取！当前引用数: {citations}")
    else:
        print("❌ 抓取失败，可能被 Google 拦截了。")
        exit(1)

if __name__ == '__main__':
    get_citations()