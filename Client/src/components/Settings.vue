<template>
  <div class="settings">
    <b-container class="mt-5">
      <h1 class="mb-3">
        Set your preferences
        <span class="float-right" @click="showInfo = true" style="cursor: pointer"
          ><font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange"
        /></span>
      </h1>
      <b-alert :show="showInfo" dismissible variant="" @dismissed="showInfo = false">
        <font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange" class="mr-2" />
        Use the slider below to set the desired video duration. The triangle picker lets you define the style of your
        video - do you want to focus on informativity, creativity or enthusiasm? Based on your settings, you get a
        number of suggested outlines to choose from and you can watch similar videos together with their structure.
      </b-alert>
      <!--  <b-row>
        <b-col>
          <b-button v-b-modal="'video-modal'" squared class="next-button float-right">
            <b-icon icon="play-fill"></b-icon>
            Show matching videos</b-button
          >
        </b-col>
      </b-row> -->
      <b-row class="mb-4">
        <b-col md="4">
          <!-- </b-col>
        <b-col sm="6"> -->
          <div class="float-left"><b>Video style:</b></div>
          <triangle-picker class="float-left" :height="400" :width="400"></triangle-picker>
        </b-col>
        <b-col class="float-right ml-auto" md="6">
          <b-row
            ><b-col>
              <b>Expected duration in minutes:</b>
              <vue-slider
                class="my-5"
                v-model="duration"
                :tooltip="'always'"
                :marks="{ 60: '01:00', 420: '07:00' }"
                :min="60"
                :max="420"
                :interval="10"
                :tooltipFormatter="format"
              ></vue-slider></b-col
          ></b-row>
          <b-row
            ><b-col>
              <!-- <b class="mr-3">Matching videos:</b> -->
              <b-button v-b-modal="'video-modal'" squared class="next-button float-md-right mt-4">
                <b-icon icon="play-fill"></b-icon>
                Show matching videos</b-button
              ></b-col
            ></b-row
          >
        </b-col>
        <!-- </b-row>

      <b-row class="my-4" align-v="top"> -->
      </b-row>
      <hr />
      <b-row class="my-4" align-v="center">
        <b-col sm="12">
          <div>
            <b>Suggested Outlines:</b
            ><b-icon icon="info-circle" scale="0.8" shift-v="6" id="tooltip-target-outline"></b-icon>
            <b-tooltip target="tooltip-target-outline" triggers="hover">
              These outlines are based on your settings and the matching videos in our database. You can select one as a
              template and refine it in the next step.
            </b-tooltip>
          </div>

          <VideoOutline
            :outlines="[$store.state.videoStructure].concat(recommendedOutlines)"
            :draggable="false"
            :selectable="true"
            :outlineNames="['Current', 'Suggestion 1', 'Suggestion 2', 'Suggestion 3']"
            id="full"
          ></VideoOutline>
        </b-col>
      </b-row>

      <b-row>
        <b-button squared class="next-button ml-auto mr-3" to="/script">Continue to script</b-button>
      </b-row>
    </b-container>
    <b-modal id="video-modal" size="lg" centered ok-only :title="`Video examples that match your settings`" static lazy>
      <div v-if="videoMatch.length > 0">
        <VideoOutlineSmall
          :outline="video.outline"
          :id="`${video.VideoId}`"
          :videoId="video.VideoId"
        ></VideoOutlineSmall>
        <!-- <b-embed
          type="iframe"
          aspect="16by9"
          :src="`https://www.youtube.com/embed/${video.VideoId}?start=${video.Start}&end=${video.End}`"
          allowfullscreen
        ></b-embed> -->
      </div>
      <p v-if="videoMatch.length <= 0">There are no matching videos.</p>
      <template #modal-footer>
        <div class="w-100" v-if="videoMatch.length > 1">
          <b-button
            squared
            class="float-left  next-button"
            @click="
              () => {
                setOutline(video.outline);
              }
            "
          >
            Use this outline for your video
          </b-button>
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
        <div class="w-100" v-if="videoMatch.length <= 1"></div>
      </template>
    </b-modal>
    <b-sidebar id="sidebar-1" title="Sidebar" shadow lazy>
      <div class="px-3 py-2">
        <b-row class="my-4" align-v="center">
          <b-col sm="12">
            <div><b>Matching video examples:</b></div>
            <!-- <b-card-group deck class="mt-2"> -->
            <b-card
              v-for="(id, idx) in $store.state.recommendedVideoIds"
              :key="id"
              :ref="`videocard${idx}`"
              class="videocard"
            >
              <VideoOutlineSmall :outline="outlines[idx]" :id="`${idx}`" :videoId="id"></VideoOutlineSmall>
            </b-card>
            <!--  </b-card-group> -->
          </b-col>
        </b-row>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import VueSlider from "vue-slider-component";
import "vue-slider-component/theme/default.css";
import TrianglePicker from "./TrianglePicker.vue";
import VideoOutline from "./VideoOutline.vue";
import VideoOutlineSmall from "./VideoOutlineSmall.vue";

export default {
  name: "Settings",
  components: {
    VueSlider,
    TrianglePicker,
    VideoOutline,
    VideoOutlineSmall,
  },
  data() {
    return {
      showInfo: true,
      currentExample: 0,
    };
  },
  computed: {
    duration: {
      get: function() {
        return this.$store.state.duration;
      },
      set: function(newVal) {
        this.$store.state.duration = newVal;
      },
    },
    outlines() {
      return this.$store.state.outlineSuggestions.map((o) =>
        o.map((s) => {
          return {
            from: new Date(s.timeRange[0]),
            to: new Date(s.timeRange[1]),
            name: s.val,
          };
        })
      );
    },
    recommendedOutline() {
      return this.$store.state.recommendedOutline.map((s) => {
        return {
          from: new Date(s.timeRange[0]),
          to: new Date(s.timeRange[1]),
          name: s.val,
        };
      });
    },
    recommendedOutlines() {
      return this.$store.state.recommendedOutlines?.map((o) =>
        o.map((s) => {
          return {
            from: new Date(s.timeRange[0]),
            to: new Date(s.timeRange[1]),
            name: s.val,
          };
        })
      );
    },
    videoMatch() {
      return this.$store.state.recommendedVideoIds.map((id, idx) => {
        return { VideoId: id, outline: this.outlines[idx] };
      });
    },
    video() {
      if (this.videoMatch.length > 0) return this.videoMatch[Math.min(this.videoMatch.length - 1, this.currentExample)];
      else return {};
    },
  },
  watch: {
    duration() {
      this.$store.dispatch("getRecommendedVideos");
      this.$store.dispatch("scaleSelectedOutline");
    },
    videoMatch() {
      this.currentExample = 0;
    },
  },
  props: {},
  mounted() {
    if (this.$store.state.recommendedOutline.length <= 0) this.$store.dispatch("getRecommendedVideos");
  },
  methods: {
    setOutline(outline) {
      if (
        this.$store.state.videoStructure.length == 0 ||
        confirm("Do you want to replace your current outline with this one?")
      ) {
        this.$store.dispatch("applyOutline", outline);

        this.$bvModal.hide("video-modal");
      }
    },
    format(value) {
      return `${Math.floor(value / 60)
        .toString()
        .padStart(2, "0")}:${Math.round(value % 60)
        .toString()
        .padStart(2, "0")}`;
    },
  },
};
</script>
<style src="@vueform/slider/themes/default.css"></style>

<style>
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
.next-button {
  background: #006c66;
}
.next-button:hover,
.next-button:focus,
.next-button:active {
  background-color: #013b38 !important;
}

.videocard {
  border: none;
}
</style>
