#%%
import pandas as pd
import json
#%%
df = pd.read_csv("videoData.csv", delimiter="; ")
videoInfo = json.load(open("preparedData.json"))
# %%
def jaccard_similarity(a, b):
    intersection = len(list(set(a).intersection(set(b))))
    union = len(set(a).union(set(b)))
    return float(intersection)/union
#%%

def get_matching_videos(d, c, e, i, v=df, n=3, top=10):
    input_ratings = [c, e, i]
    videos = v[v["duration_in_seconds"] >= d-60]
    videos = videos[videos["duration_in_seconds"] <= d+60]
    videos["weighted_sum"] = c*videos["creativity"] + e*videos["enthusiasm"] + i*videos["informativity"]
    videos = videos[videos["weighted_sum"] >= 3]
    videos["rating_sum"] = videos["creativity"] + videos["enthusiasm"] + videos["informativity"]
    videos["distance"] = 0
    for (idx, category) in enumerate(["creativity", "enthusiasm", "informativity"]):
        rel_val = videos[category]/videos["rating_sum"]
        videos["rel_"+category] = rel_val
        videos["distance"] += (rel_val - input_ratings[idx])**2
    return videos.sort_values("distance").head(top).sort_values("weighted_sum", ascending=False).head(n)

def get_video_outline(id):
    for vi in videoInfo:
        if vi["id"] == id:
            return vi["info"]["normalized_sections"]
    return []

def get_audio_elements(id):
    for vi in videoInfo:
        if vi["id"] == id:
            return vi["info"]["audioElements"]
    return []

def get_visual_elements(id):
    for vi in videoInfo:
        if vi["id"] == id:
            return vi["info"]["visualElements"]
    return []
#%%
matching_vids = list(get_matching_videos(300, 0.1, 0.1, 0.8, df, n=10)["video_id"])
matching_vids

#%%
all_audio_elements= [e for vid in matching_vids for e in get_audio_elements(vid)]
audio_element_count = {}
for e in list(set(all_audio_elements)):
    audio_element_count[e] = all_audio_elements.count(e)

print([e for e in audio_element_count.items() if e[1] >= len(matching_vids)/2])
sorted_elements= sorted(audio_element_count.items(), key=lambda x: x[1], reverse=True)
sorted_elements



#%%

matching_vid_infos = []
for v in matching_vids:
    for vi in videoInfo:
        if vi["id"] == v:
            matching_vid_infos.append(vi["info"]["normalized_sections"])

# %%
outlines = [[section["val"] for section in video] for video in matching_vid_infos]
outline_similarities = {}
for (idx, o1) in enumerate(outlines):
    similarity_sum = 0
    for (oidx, o2) in enumerate(outlines):
        if (oidx != idx):
            similarity_sum += jaccard_similarity(o1, o2)
    outline_similarities[", ".join(o1)] = similarity_sum
# %%
outline_similarities
# %%
for vi in videoInfo:
        if vi["id"] == "KcwjVK8eUdw":
            print([section["val"] for section in vi["info"]["normalized_sections"]])
# %%
def get_best_outline(video_ids):
    outlines = [[section["val"] for section in get_video_outline(id)] for id in video_ids]
    outline_similarities = {}
    for (idx, id) in enumerate(video_ids):
        similarity_sum = 0
        for (oidx, o2) in enumerate(outlines):
            if (oidx != idx):
                similarity_sum += jaccard_similarity(outlines[idx], o2)
        outline_similarities[id] = similarity_sum
    sorted_ids = sorted(outline_similarities.items(), key=lambda x: x[1], reverse=True)
    return get_video_outline(sorted_ids[0][0])

# %%
get_best_outline(matching_vids)
# %%
import datetime
# %%
datetime.datetime(1970, 1, 1) + datetime.timedelta(0, 90)
# %%
