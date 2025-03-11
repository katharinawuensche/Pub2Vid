import Vue from "vue";
import Vuex from "vuex";
import App from "./App.vue";
import router from "./router";
Vue.use(Vuex);

const backendURL = "https://katharinawunsche.pythonanywhere.com";
//const backendURL = "http://127.0.0.1:5000";

Vue.config.productionTip = false;
const scaleOutline = (outline, duration) => {
  let inputDuration = Math.max.apply(
    null,
    outline.map((s) => new Date(s.timeRange[1]))
  );
  let factor = (1000 * duration) / inputDuration;
  let newOutline = outline.slice();
  newOutline.forEach((o) => {
    let o_duration = new Date(o.timeRange[1]) - new Date(o.timeRange[0]);
    let new_duration = o_duration * factor;
    let old_start = new Date(o.timeRange[0]);
    o.timeRange[0] = new Date(0).setMilliseconds(
      factor * (old_start.getMilliseconds() + old_start.getSeconds() * 1000 + old_start.getMinutes() * 60 * 1000)
    );
    o.timeRange[1] = new Date(new Date(o.timeRange[0]).setMilliseconds(new_duration));
  });
  return newOutline.sort((b, a) => a.timeRange[1] - a.timeRange[2] - (b.timeRange[1] - b.timeRange[2]));
};

function getDefaultState() {
  return {
    backendURL,
    selectedOutlineIdx: null,
    duration: 240,
    voiceOver: 100,
    priorities: {
      creativity: 0.33,
      enthusiasm: 0.33,
      informativity: 0.33,
    },
    recommendedVideoIds: [],
    videoStructure: [],
    outlineSuggestions: [],
    recommendedOutline: [],
    recommendedOutlines: [],
    audioElements: [],
    visualElements: [],
    scriptContent: {},
    plainScriptText: {},
  };
}

function loadStore() {
  let localState = localStorage.getItem("state");
  if (localState && localState.length > 0) {
    let fullStorage = JSON.parse(localState);
    fullStorage.videoStructure.forEach((s) => {
      if (typeof s.from == "string") s.from = new Date(Date.parse(s.from));
      if (typeof s.to == "string") s.to = new Date(Date.parse(s.to));
    });
    return fullStorage;
  } else return getDefaultState();
}

const state = loadStore();

const store = new Vuex.Store({
  state,
  actions: {
    getRecommendedVideos() {
      fetch(backendURL + "/matchingVideos", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify({
          duration: Math.min(this.state.duration, 570),
          creativity: this.state.priorities.creativity,
          enthusiasm: this.state.priorities.enthusiasm,
          informativity: this.state.priorities.informativity,
        }),
      })
        .then((res) => res.json())
        .then((res) => {
          //console.log(res);
          this.state.recommendedVideoIds = res["videoRecommendations"];
          this.state.audioElements = res["audio_recommendations"].sort();
          this.state.visualElements = res["visual_recommendations"].sort();
          this.state.outlineSuggestions = res["normalized_outlines"].map((o) =>
            scaleOutline(o, this.state.duration).filter((s) => s.timeRange[1] - s.timeRange[0] > 0)
          );
          this.state.recommendedOutlines = res["generated_outline"].map((o) =>
            scaleOutline(o, this.state.duration).filter((s) => s.timeRange[1] - s.timeRange[0] > 0)
          );
          this.state.recommendedOutline = scaleOutline(res["generated_outline"][0], this.state.duration).filter(
            (s) => s.timeRange[1] - s.timeRange[0] > 0
          );
        });
    },

    scaleSelectedOutline() {
      if (this.state.videoStructure.length <= 0) return;
      this.state.videoStructure = scaleOutline(
        this.state.videoStructure.map((o) => {
          return {
            name: o.name,
            timeRange: [o.from, o.to],
          };
        }),
        this.state.duration
      )
        .filter((s) => s.timeRange[1] - s.timeRange[0] > 0)
        .map((o) => {
          return {
            name: o.name,
            from: new Date(o.timeRange[0]),
            to: new Date(o.timeRange[1]),
          };
        });
      this.state.videoStructure.sort((a, b) => a.from - b.from);
      this.state.videoStructure[0].from = new Date(0);
      this.state.videoStructure[this.state.videoStructure.length - 1].to = new Date(
        new Date(0).setSeconds(this.state.duration)
      );
      this.state.videoStructure.forEach((s, idx) => {
        if (idx > 0) s.from = this.state.videoStructure[idx - 1].to;
        if (idx < this.state.videoStructure.length - 1) s.to = this.state.videoStructure[idx + 1].from;
      });
    },

    addSectionToOutline(_, section) {
      this.state.videoStructure.push({
        name: section,
        from: new Date(new Date(0).setSeconds(this.state.duration - 20)),
        to: new Date(new Date(0).setSeconds(this.state.duration)),
      });
      this.state.videoStructure.sort((a, b) => a.from - b.from);
      this.state.videoStructure[0].from = new Date(0);
      this.state.videoStructure[this.state.videoStructure.length - 1].to = new Date(
        new Date(0).setSeconds(this.state.duration)
      );
      this.state.videoStructure.forEach((s, idx) => {
        if (idx > 0) s.from = this.state.videoStructure[idx - 1].to;
        if (idx < this.state.videoStructure.length - 1) s.to = this.state.videoStructure[idx + 1].from;
      });
      /* this.state.videoStructure = scaleOutline(this.state.videoStructure, this.state.duration).filter(
        (s) => s.timeRange[1] - s.timeRange[0] > 0
      ); */
    },
    setOutline() {
      this.state.videoStructure = this.state.recommendedOutline.map((s) => {
        return {
          from: new Date(s.timeRange[0]),
          to: new Date(s.timeRange[1]),
          name: s.val,
        };
      });
    },
    applyOutline(_, outline) {
      //console.log(outline);
      this.state.videoStructure = outline.slice();
    },

    resetDefaultState() {
      this.replaceState(getDefaultState());
      this.dispatch("getRecommendedVideos");
    },
    saveStore() {
      localStorage.setItem("state", JSON.stringify(this.state));
    },
  },
});

new Vue({
  router,
  render: (h) => h(App),
  store: store,
}).$mount("#app");
