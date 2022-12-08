from flask import Flask, jsonify, request
from authoring_backend import *
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def prepare_response(content):
    response = jsonify(content)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

@app.route('/')
def hello():
    return prepare_response({"greeting": "Hello, World!"})

@app.route('/matchingVideos', methods=["GET", "POST"])
def getMatchingVideos():
    json_data = request.json
    print(json_data)
    matching_videos = get_matching_videos(float(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    matching_outlines = [get_video_outline(id) for id in list(matching_videos["video_id"])[:5]]
    best_outline = get_best_outline(list(matching_videos["video_id"]))
    generated_outline = generate_video_outline(float(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    audio_recommendations = get_audio_recommendations(list(matching_videos["video_id"]))
    visual_recommendations = get_visual_recommendations(list(matching_videos["video_id"]))

    return prepare_response({"videoRecommendations": list(matching_videos["video_id"])[:5], "normalized_outlines": matching_outlines, "generated_outline": generated_outline, "best_outline": best_outline, "audio_recommendations": audio_recommendations, "visual_recommendations": visual_recommendations})

@app.route('/slides', methods=["GET", "POST"])
def getSlidesFromSectionlist():
    json_data = request.json
    print(json_data)
    res = get_presentation_from_layout(json_data)
    return prepare_response({"slides": str(res)})

""" @app.route('/videoOutlines', methods=["GET", "POST"])
def createOutlineSuggestions():
    json_data = request.json
    print(json_data)
    outlines = generate_video_outline(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    audioElements = get_audio_recommendations_old(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    visualElements = get_visual_recommendations_old(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    videoRecommendations = get_video_recommendations(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    return prepare_response({"outlines": outlines, "audioElements": audioElements, "visualElements": visualElements, "videoRecommendations": videoRecommendations})

@app.route('/videoSuggestions', methods=["GET", "POST"])
def createVideoSuggestions():
    json_data = request.json
    print(json_data)
    videosIn, videosOut = get_num_videos(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    outlines = get_section_recommendations(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    audioElements = get_audio_recommendations(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    visualElements = get_visual_recommendations(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    videoRecommendations = get_video_recommendations(int(json_data["duration"]), float(json_data["creativity"]), float(json_data["enthusiasm"]), float(json_data["informativity"]))
    return prepare_response({"videosIn": videosIn, "videosOut": videosOut, "outlines": outlines, "audioElements": audioElements, "visualElements": visualElements, "videoRecommendations": videoRecommendations})

@app.route('/slidesFromSections', methods=["GET", "POST"])
def getSlidesFromSectionlist():
    json_data = request.json
    print(json_data)
    res = get_presentation_from_length_and_sections(int(json_data["duration"]), json_data["sections"])
    return prepare_response({"slide": str(res)})

@app.route('/slide', methods=["GET", "POST"])
def getSlide():
    json_data = request.json
    print(json_data)
    #else:
    res = get_presentation_from_layout(json_data)
    return prepare_response({"slide": str(res)}) """