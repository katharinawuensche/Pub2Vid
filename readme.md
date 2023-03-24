# Pub2Vid

This repository contains both frontend and backend code of the video script editing tool Pub2Vid.

## Frontend

The frontend application was built in Vue.js and can be run locally using the following commands:

```shell
cd Client
npm install
npm run serve
```

In production, the application is hosted on Google Firebase and can be accessed at [pub2vid.web.app](https://pub2vid.web.app).

## Backend

The backend code is located in the "Server" directory and was built using python and Flask. It provides two endpoints: `/slides` and `/matchingVideos`.

### Recommendations

The `/matchingVideos` endpoint is responsible for loading all suggestions and recommendations based on the user's settings. This includes:

- video recommendations and the recommended videos' outlines
- generated outlines based on the selected video style
- recommendations for audio and visual elements

#### `get_matching_videos(d, c, e, i)`

The matching videos returned as video recommendations are determined by computing the weighted sum of average ratings for all videos with a duration of $d-60s$ to $d+60s$, where d is the desired duration entered by the user.
The weighted sum is computed as
$c \times c_{rating} + e \times e_{rating} + i \times i_{rating}$, where $c, e$ and $i$ stand for the three dimensions creativity, enthusiasm and informativity, $input$ indicates that the value was entered by the user via the triangle picker (ranging from 0 to 1) and $rating$ means the average video rating determined through the user study (ranging from 1 to 5). After sorting the videos by their weighted sum, the top 5 results are returned.

#### `generate_video_outline(duration_in_seconds, creativity, informativity, enthusiasm)`

The function defines a set of predefined outlines based on the video analysis results: [https://twominutepapersanalysis.web.app/#/sections/orders](https://twominutepapersanalysis.web.app/#/sections/orders). There are three predefined outlines for each of the dimensions as well as a list of three outlines for a "generic" input that does not focus on either on one dimension in particular. If the weight for one of the dimensions is larger than the sum of the two others, the corresponding list of outlines is scaled to the given duration and returned to the user. If none of the dimensions clearly outweights the others, the generic list of outlines is returned instead.

#### `get_visual_recommendations(video_ids, frac=0.6)` and `get_audio_recommendations(video_ids, frac=0.5)`

The two functions for determining the list of visual and audio recommendations receive the list of matching videos and determine the visual or audio elements that are present withing these videos and meet a threshhold of frac. With frac=0.6, the given element needs to be present in at least 60% of the recommended videos.

### Slide generation

The `/slides` endpoints is used for generating a presentation template based on the user's video outline and script. It uses the [pptx](https://python-pptx.readthedocs.io/en/latest/) module for composing a presentation based on the selected sections and corresponding slide templated. Moreover, it sets the slide durations according to the selected section durations and sets the slides' speaker notes to the user-written script. The presentdation is then sent to the client application as an [Office Open XML](https://en.wikipedia.org/wiki/Office_Open_XML) document.
