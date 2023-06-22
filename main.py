import json5 as json
import asyncio
import aiohttp
import pandas as pd
import bilibili_api as bapi

videolist: dict = json.load(open('./videolist.json5'))
label = videolist
videolist = [int(x) for x in videolist.keys()]
df = pd.DataFrame(columns=['uname', 'message', 'like', 'oid', 'label'])

async def fetch_a_page(oid: int, page: int):
    # parse comment
    try:
        comment = dict(await bapi.comment.get_comments(oid, bapi.comment.CommentResourceType.VIDEO, page))
        
        for c in comment['replies']:
            # label 列的数值根据label值来确定
            df.loc[c['rpid']] = [c['member']['uname'], c['content']['message'], c['like'], oid, label[str(oid)]]
            
        print(f'oid: {oid}, page: {page}, count: {len(comment["replies"])}')
    except:
        pass
    

async def fetch_all_page(oid: int):
    page = 1
    
    count = int(dict(await bapi.comment.get_comments(oid, bapi.comment.CommentResourceType.VIDEO, 1))['page']['count'] / 20)
    
    print(f'oid: {oid}, count: {count}')
    
    tasks = []
    
    while page <= count:
        # await fetch_a_page(oid, page)
        # print(f'oid: {oid}, page: {page}')
        
        tasks.append(asyncio.create_task(fetch_a_page(oid, page)))
        
        page += 1
    
    await asyncio.gather(*tasks)

async def main():
    tasks = []
    
    for oid in videolist:
        tasks.append(asyncio.create_task(fetch_all_page(oid)))
        await asyncio.sleep(3)
    
    await asyncio.gather(*tasks)
    
    # await fetch_all_page(418788911)
    
if __name__ == '__main__':
    asyncio.run(main())
    df.to_csv('./comments.csv', encoding='utf-8-sig')