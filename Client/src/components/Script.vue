<template>
  <div class="settings">
    <b-container class="mt-5">
      <h1 class="mb-3">
        Write your script
        <span class="float-right" @click="showInfo = true" style="cursor: pointer"
          ><font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange"
        /></span>
      </h1>

      <b-alert :show="showInfo" dismissible variant="" @dismissed="showInfo = false">
        <font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange" class="mr-2" />
        Here, you can refine your video outline by dragging the sections in the timeline below. Afterwards, you can set
        your average voice-over speed via the slider below and listen to sound samples matching your selection. These
        settings should help you writing the video script by providing you with an estimated reading time based on the
        text you enter for the different sections. If you want to annotate parts of your script as instructions or
        additional information, simply highlight the text and choose a background color for it. This part will then not
        be included in the duration estimation.
      </b-alert>
      <b-alert :show="$store.state.videoStructure.length == 0" dismissible variant="info">
        Your video outline is currently empty. Do you want to load a suggestion based on your settings?
        <b-button variant="info" squared class="m-2 ml-auto" @click="$store.dispatch('setOutline')"
          >Load outline</b-button
        >
      </b-alert>

      <b-row class="mt-4" align-v="center">
        <b-col sm="12">
          <b-button class="next-button float-right" squared v-b-modal="'add-section-modal'"
            ><b-icon icon="plus"></b-icon>Add section</b-button
          >
          <VideoOutline
            :outlines="[$store.state.videoStructure]"
            :draggable="true"
            :selectable="false"
            :deletable="true"
          ></VideoOutline>
        </b-col>
      </b-row>
      <b-row class="mb-4" align-v="center">
        <b-col sm="3">
          <b>Average voice-over speed (words per minute)</b>
        </b-col>
        <b-col>
          <vue-slider
            v-model="$store.state.voiceOver"
            :tooltip="'always'"
            :marks="{ 0: '🐢', 100: 'Video average', 200: '🐇' }"
            :min="0"
            :max="200"
            :interval="5"
          ></vue-slider>
        </b-col>
        <!-- <b-col sm="auto"><b-button @click="playSample" squared>Play generated sample</b-button></b-col> -->
        <b-col sm="auto"
          ><b-button v-b-modal="'video-modal'" squared class="next-button">
            <b-icon icon="play-fill"></b-icon>
            Play video sample</b-button
          ></b-col
        >
      </b-row>
      <b-row class="" align-v="center">
        <b-col sm="12">
          <hr />
          <!-- <h2>Your script:</h2> -->
        </b-col>
      </b-row>
      <b-row class="" align-v="center" v-for="(key, idx) in scriptTooLong" :key="key">
        <b-col sm="12">
          <b-alert show dismissible variant="warning">
            <span class="red"
              >Warning: Based on your selected reading speed of {{ $store.state.voiceOver }} words per minute, the
              voice-over for your {{ key }} section might exceed the planned duration of
              {{ sectionDurations[key] }} seconds.
            </span>
            <span class="red" v-if="idx == 0">
              To fix this, you could either
              <ul>
                <li>make the section longer in the timeline above,</li>
                <li>increase the voice-over speed using the slider or</li>
                <li>reduce the amount of text in the script below.</li>
              </ul>
            </span>
          </b-alert>
        </b-col>
      </b-row>
      <b-row
        class="my-2"
        align-v="center"
        v-for="(section, idx) in $store.state.videoStructure"
        :key="section.name + idx"
      >
        <b-col sm="12">
          <div>
            <b>{{ section.name }}</b
            >{{
              questionDict[section.name] && questionDict[section.name].length > 0
                ? ` - ${questionDict[section.name]}`
                : ""
            }}

            <span
              :class="
                `float-right ${sectionDurations[section.name] < readingTimes[getSectionKey(section)] ? 'red' : ''}`
              "
              >Est. reading time: {{ Math.round(readingTimes[getSectionKey(section)]) || 0 }}s/{{
                new Date(section.to - section.from).getMinutes() * 60 +
                  new Date(section.to - section.from).getSeconds()
              }}s</span
            >
            <quill-editor
              ref="myQuillEditor"
              :options="editorOptions"
              @change="logText($event, section)"
              v-model="$store.state.scriptContent[getSectionKey(section)]"
            />
          </div>
        </b-col>
      </b-row>
      <b-row>
        <b-button squared class="mr-auto ml-3" to="/settings">Back to settings</b-button>
        <b-button squared class="next-button ml-auto mr-3" to="/recommendations">Continue to recommendations</b-button>
      </b-row>
    </b-container>
    <b-modal
      id="video-modal"
      size="lg"
      centered
      ok-only
      :title="
        `Video examples for ${Math.max($store.state.voiceOver - 5, 0)} - ${$store.state.voiceOver +
          5} words per minute*`
      "
      @hidden="() => (currentExample = 0)"
    >
      <div v-if="videoMatch.length > 0">
        <b-embed
          type="iframe"
          aspect="16by9"
          :src="`https://www.youtube.com/embed/${video.VideoId}?start=${video.Start}&end=${video.End}`"
          allowfullscreen
        ></b-embed>
      </div>
      <p v-if="videoMatch.length <= 0">There are no video examples for this speed yet.</p>
      <template #modal-footer>
        <div class="w-100" v-if="videoMatch.length > 1">
          <div class="pb-2">
            *The computed words per minute for the presented sections include speech pauses and other interruptions and
            may therefore differ from the perceived velocity.
          </div>
          <b-button
            squared
            class="float-right  next-button"
            @click="currentExample++"
            :disabled="currentExample >= videoMatch.length - 1"
          >
            Next example
          </b-button>
          <b-button
            squared
            variant="secondary"
            class="mr-2 float-right"
            @click="currentExample--"
            :disabled="currentExample <= 0"
          >
            Previous example
          </b-button>
        </div>
      </template>
    </b-modal>
    <b-modal
      id="add-section-modal"
      title="Add a section to your outline"
      ok-only
      ok-title="Cancel"
      ok-variant="secondary"
      centered
    >
      <b-list-group>
        <b-list-group-item
          button
          v-for="section in Object.keys(questionDict)"
          :key="section"
          @click="
            () => {
              $store.dispatch('addSectionToOutline', section);
              $bvModal.hide('add-section-modal');
            }
          "
          ><b>{{ section }}</b
          >{{ questionDict[section].length > 0 ? ` - ${questionDict[section]}` : "" }}
        </b-list-group-item>
      </b-list-group>
    </b-modal>
  </div>
</template>

<script>
import "quill/dist/quill.core.css";
import "quill/dist/quill.snow.css";
import "quill/dist/quill.bubble.css";
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";
import { quillEditor } from "vue-quill-editor";
import VideoOutline from "./VideoOutline.vue";
import transcribedSections from "../assets/transcribedSections";
import questionDict from "../assets/questionDict";

export default {
  name: "Script",
  components: {
    VideoOutline,
    quillEditor,
    VueSlider,
  },
  data() {
    return {
      showInfo: true,
      questionDict,
      currentExample: 0,
      plainTextBackdoor: 0,
      plainScriptText: {},
      editorOptions: {
        modules: {
          toolbar: [[{ header: [1, 2, false] }], ["bold", "italic", "underline"], [{ color: [] }, { background: [] }]],
        },
        placeholder: "Your section content...️ ✏️ ",
        theme: "bubble", // 'snow' or 'bubble'
      },
    };
  },
  computed: {
    readingTimes() {
      this.plainTextBackdoor;
      let cloneObj = Object.assign([], this.$store.state.plainScriptText);
      for (let key in cloneObj) {
        cloneObj[key] =
          ((this.$store.state.plainScriptText[key].match(/( |\n)/g) || []).length * 60) / this.$store.state.voiceOver;
      }

      return cloneObj;
    },
    sectionDurations() {
      this.plainTextBackdoor;
      let cloneObj = Object.assign([], this.$store.state.plainScriptText);
      for (let key in cloneObj) {
        let section = this.$store.state.videoStructure.find((s) => s.name == key);
        if (section)
          cloneObj[key] =
            new Date(section.to - section.from).getMinutes() * 60 + new Date(section.to - section.from).getSeconds();
      }
      return cloneObj;
    },
    scriptTooLong() {
      return Object.keys(this.readingTimes).filter((key) => this.readingTimes[key] > this.sectionDurations[key]);
    },
    videoMatch() {
      let matchingVideos = [];
      for (let video in transcribedSections) {
        transcribedSections[video].forEach((section) => {
          let wpm = Math.round((60 * section.words) / (section.stop - section.start));
          if (
            section.stop - section.start >= 10 &&
            wpm + 5 >= this.$store.state.voiceOver &&
            wpm - 5 <= this.$store.state.voiceOver
          ) {
            matchingVideos.push({
              VideoId: video,
              Start: section.start,
              End: section.stop,
            });
          }
        });
      }
      return matchingVideos;
    },
    video() {
      return this.videoMatch[this.currentExample];
    },
  },
  props: {},
  mounted() {},
  methods: {
    playSample() {
      for (let video in transcribedSections) {
        transcribedSections[video].forEach((section) => {
          let wpm = Math.round((60 * section.words) / (section.stop - section.start));
          if (wpm + 5 >= this.$store.state.voiceOver && wpm - 5 <= this.$store.state.voiceOver)
            console.log(video, section.name);
        });
      }
    },
    getText(node) {
      function recursor(n) {
        var i,
          a = [];
        if (n.nodeType !== 3) {
          if (n.childNodes && n.style?.backgroundColor?.length <= 0)
            for (i = 0; i < n.childNodes.length; ++i) a = a.concat(recursor(n.childNodes[i]));
          if (n.nodeName == "P") a.push("\n");
        } else a.push(n.data);
        return a;
      }
      return recursor(node);
    },
    logText(event, section) {
      let pseudoDiv = document.createElement("div");
      pseudoDiv.innerHTML = event.html;
      let untaggedText = this.getText(pseudoDiv).join("");
      pseudoDiv.remove();
      this.$store.state.plainScriptText[this.getSectionKey(section)] = untaggedText;
      this.plainTextBackdoor++;
    },
    getSectionKey(section) {
      let sameSections = this.$store.state.videoStructure.filter((s) => s.name == section.name);
      if (sameSections.length <= 1) return section.name;
      else {
        let idx = sameSections.findIndex((s) => s == section);
        if (idx > 0) return `${section.name}${idx}`;
        else return section.name;
      }
    },
  },
};
</script>
<style src="@vueform/slider/themes/default.css"></style>

<style>
.red {
  color: #b10000;
}
.gantt-container {
  height: 100%;
  width: 100%;
}
.vue-slider-dot-tooltip-inner {
  background-color: #006c66;
  border-color: #006c66;
}
.vue-slider-process {
  background-color: #006c66;
}
.left-container {
  overflow: hidden;
  position: relative;
  height: 100%;
  min-height: 200px;
}
.card-body {
  padding: 0;
}
.ql-tooltip {
  z-index: 2;
}
.vue-slider-dot-tooltip-inner {
  background-color: #006c66;
  border-color: #006c66;
}
.vue-slider-process {
  background-color: #006c66;
}
</style>
