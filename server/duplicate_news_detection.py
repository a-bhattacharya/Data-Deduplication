# -*- coding: utf-8 -*-


import pandas as pd
from sentence_transformers import SentenceTransformer, util
import json


# class created to store articles and their properties
class NewsArticles:
    def __init__(self, url, text, title, date):
        self.url = url
        self.text = text
        self.title = title
        if date == None:
            self.date = 0
        self.date = str(date)


article_list = []
df = pd.read_csv("newsdata.csv")

# with open("./newsdata.json", "w") as json_file:
#     df.to_json(path_or_buf=json_file, orient="index")

# titles = []
for i in range(0, len(df)):
    title = df["Title"][i]
    # titles.append(title)
    text = df["Text"][i]
    date = df["Date"][i]
    url = df["Link"][i]
    ob = NewsArticles(url, text, title, date)
    article_list.append(ob)

# print(titles)

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# final used to store list of deduplicate news
dedupe_news = []

# initially we append the first article
dedupe_news.append([article_list[0]])

# for each artcle in artcle list
for i in range(1, len(article_list)):
    # sz store size of dedupe ie no of non redundant articles
    sz = len(dedupe_news)
    # print(sz)
    inserted = False

    # go through every non redundant article in dedupe
    for j in range(0, sz):
        similar_news_list = dedupe_news[j]

        ar1 = article_list[i]
        # compare the present one with the artcle at front ie most relavant one
        ar2 = similar_news_list[0]

        sentence1 = ar1.text
        sentence2 = ar2.text

        inserted = False

        # encode sentences to get their embeddings
        embedding1 = model.encode(sentence1, convert_to_tensor=True)
        embedding2 = model.encode(sentence2, convert_to_tensor=True)
        # print(len(embedding1))
        # compute similarity scores of two embeddings
        cosine_scores = util.pytorch_cos_sim(embedding1, embedding2)

        score = cosine_scores.item()

        # if score is >0.7 the article is similar to one under consideration
        if score > 0.7:
            # sorting and placing the article according to timestamp

            for k in range(0, len(similar_news_list)):
                # if ar1.date!=None and sim_news_list[0].date.replace(tzinfo=pytz.utc)>ar1.date.replace(tzinfo=pytz.utc):
                if ar1.date != None and similar_news_list[0].date < ar1.date:
                    # append at poistion k
                    dedupe_news[j].insert(k, ar1)
                    inserted = True
                    break

            # append at end
            if inserted == False:
                dedupe_news[j].append(ar1)
                inserted = True

            break
    # no similar news already present in the dedupe list insert this news one
    if inserted == False:
        dedupe_news.append([ar1])


print("Final grouped articles:\n\n")

grouped_news = []

for i in range(0, len(dedupe_news)):
    print("Similar articles group ", i)
    group = {"id": i + 1, "titles": []}
    for j in range(0, len(dedupe_news[i])):
        print(dedupe_news[i][j].title)
        group["titles"].append(dedupe_news[i][j].title)
    print("\n\n")
    grouped_news.append(group)

with open("./grouped_news.json", "w") as json_file:
    json.dump(grouped_news, json_file)
