<template>
  <div class="export">
    <b-container class="mt-5">
      <h1 class="my-3">
        Recommended visual and audio elements
        <span class="float-right" @click="showInfo = true" style="cursor: pointer"
          ><font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange"
        /></span>
      </h1>
      <b-alert :show="showInfo" dismissible variant="" @dismissed="showInfo = false">
        <font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange" class="mr-2" />
        Based on your settings, you can find recommendations for the visual and audio elements of your video below.
        Click on an element to see a usage example of the element in a real video. You can also find a list of
        potentially useful image and audio resources below.
      </b-alert>
      <b-row class="mb-3">
        <b-col>
          <b-list-group>
            <div class="pb-2">
              <h2 v-b-toggle.collapse-3>
                Visual elements
                <b-icon icon="chevron-up" class="when-open"></b-icon>
                <b-icon icon="chevron-down" class="when-closed"></b-icon>
              </h2>
            </div>

            <b-collapse id="collapse-3" visible>
              <b-list-group-item
                button
                v-for="e in $store.state.visualElements"
                :key="e"
                @click="
                  () => {
                    setElementAndOpenModal(e);
                  }
                "
                v-b-modal="'video-modal'"
              >
                <font-awesome-icon :icon="['fas', elem_to_icon[e]]" class="mr-1" />
                {{ e == "UI" ? "User Interface" : e }}
              </b-list-group-item>
            </b-collapse>
          </b-list-group>
        </b-col>
        <hr />
        <b-col>
          <b-list-group>
            <div class="pb-2">
              <h2 v-b-toggle.collapse-4>
                Audio elements <b-icon icon="chevron-up" class="when-open"></b-icon>
                <b-icon icon="chevron-down" class="when-closed"></b-icon>
              </h2>
            </div>
            <b-collapse id="collapse-4" visible>
              <b-list-group-item
                button
                v-for="e in $store.state.audioElements"
                :key="e"
                @click="
                  () => {
                    setElementAndOpenModal(e);
                  }
                "
                v-b-modal="'video-modal'"
              >
                <font-awesome-icon :icon="['fas', elem_to_icon[e]]" class="mr-1" />
                {{ e == "UI" ? "User Interface" : e }}
              </b-list-group-item>
            </b-collapse>
          </b-list-group>
        </b-col>
      </b-row>
      <!--    </b-card> -->
      <b-row>
        <b-col>
          <h2 class="my-3" v-b-toggle.collapse-1>
            Useful image resources
            <b-icon icon="chevron-up" class="when-open"></b-icon>
            <b-icon icon="chevron-down" class="when-closed"></b-icon>
          </h2>
          <b-collapse id="collapse-1" visible>
            <b-card-group columns>
              <b-card
                v-for="item in graphicsLinkItems"
                :key="item.name"
                :img-src="item.imgUrl"
                :img-alt="item.name"
                img-top
                img-height="100px"
                tag="article"
                style="max-width: 20rem;"
                class="mb-2"
              >
                <b-card-title
                  ><a :href="item.url" target="blank">{{ item.name }}</a></b-card-title
                >
                <b-card-text>
                  {{ item.description }}
                </b-card-text>
              </b-card>
            </b-card-group>
          </b-collapse>
        </b-col>
        <b-col>
          <h2 class="my-3" v-b-toggle.collapse-2>
            Useful audio resources
            <b-icon icon="chevron-up" class="when-open"></b-icon>
            <b-icon icon="chevron-down" class="when-closed"></b-icon>
          </h2>
          <b-collapse id="collapse-2" visible>
            <b-card-group columns>
              <b-card
                v-for="item in musicLinkItems"
                :key="item.name"
                :img-src="item.imgUrl"
                :img-alt="item.name"
                img-top
                img-height="100px"
                tag="article"
                style="max-width: 20rem;"
                class="mb-2"
              >
                <b-card-title
                  ><a :href="item.url" target="blank">{{ item.name }}</a></b-card-title
                >
                <b-card-text>
                  {{ item.description }}
                </b-card-text>
              </b-card>
            </b-card-group>
          </b-collapse>
        </b-col>
      </b-row>
      <b-row>
        <b-button squared class="mr-auto ml-3" to="/script">Back to script</b-button>
        <b-button squared class="next-button ml-auto mr-3" to="/export">Continue to export</b-button>
      </b-row>
    </b-container>
    <b-modal
      id="video-modal"
      size="lg"
      centered
      ok-only
      :title="`Usage example for ${selectedElement == 'UI' ? 'User Interface' : selectedElement}`"
    >
      <div v-if="videoMatch.length > 0">
        <b-embed
          type="iframe"
          aspect="16by9"
          :src="`https://www.youtube.com/embed/${video.VideoId}?start=${video.Start}&end=${video.End}`"
          allowfullscreen
        ></b-embed>
      </div>
      <p v-if="videoMatch.length <= 0">There are no video examples for this element yet.</p>
      <template #modal-footer>
        <div class="w-100" v-if="videoMatch.length > 1">
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
  </div>
</template>

<script>
import elementTimestamps from "../assets/elementTimestamps";

const elem_to_icon = {
  UI: "window-maximize",
  Transitions: "random",
  Diagrams: "project-diagram",
  "Pictures/Photos": "image",
  Animations: "play-circle",
  Videos: "video",
  Slides: "sticky-note",
  Subtitles: "closed-captioning",
  "Highlighting in the visualizations": "highlighter",
  "Video-over": "portrait",
  "Voice-over": "microphone",
  Music: "music",
  "Sound effects": "star",
};

export default {
  name: "Recommendations",
  components: {},
  data() {
    return {
      showInfo: true,
      elem_to_icon: elem_to_icon,
      selectedElement: "",
      currentExample: 0,
      musicLinkItems: [
        {
          name: "ccMixter",
          description: "Creative Commons music",
          url: "http://beta.ccmixter.org/",
          imgUrl:
            "https://i0.wp.com/www.techjunkie.com/wp-content/uploads/2016/12/Where-to-find-free-legal-music-downloads-3.png?w=600&ssl=1",
        },
        {
          name: "Free Music Archive",
          description: "Creative Commons music",
          url: "https://freemusicarchive.org/",
          imgUrl: "https://freemusicarchive.org/assets/images/fma-logo-orange-250x129.png",
        },
        {
          name: "Freesound",
          description: "Free music and sound effects",
          url: "https://freesound.org/",
          imgUrl: "https://freesound.org/media/images/logo.png",
        },
      ],
      graphicsLinkItems: [
        {
          name: "CC Search",
          description: "Creative Commons images",
          url: "https://search.creativecommons.org/",
          imgUrl:
            "https://d15omoko64skxi.cloudfront.net/wp-content/uploads/2017/02/Screen-Shot-2017-02-07-at-8.39.13-AM-1024x462.png",
        },
        {
          name: "Iconfinder",
          description: "Free icons, different licenses",
          url: "https://www.iconfinder.com/search/?price=free",
          imgUrl: "https://www.iconfinder.com/static/img/logo/black.svg?7cfe2038c8",
        },

        {
          name: "Unsplash",
          description: "Free photos",
          url: "https://unsplash.com/",
          imgUrl:
            "https://images.unsplash.com/photo-1549706844-30ea8cad811b?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1789&q=80",
        },
      ],
    };
  },
  computed: {
    videoMatch() {
      return elementTimestamps.filter((e) => e.Element == this.selectedElement);
    },
    video() {
      if (this.videoMatch.length > 0) return this.videoMatch[Math.min(this.videoMatch.length - 1, this.currentExample)];
      else return {};
    },
  },
  props: {},
  mounted() {},
  methods: {
    setElementAndOpenModal(el) {
      this.selectedElement = el;
      this.currentExample = 0;
      if (elementTimestamps.find((e) => e.Element == el))
        this.$nextTick(() => {
          this.$bvModal.show("video-modal");
        });
    },
  },
};
</script>
<style scoped>
.card-body {
  padding: 12px;
}
a {
  color: black;
}
a.btn {
  color: white;
}
.collapsed > .when-open,
.not-collapsed > .when-closed {
  display: none;
}
</style>
