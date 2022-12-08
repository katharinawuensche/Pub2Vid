<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light" fixed="top">
      <b-navbar-brand to="/">Pub2Vid</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/settings">Settings</b-nav-item>
          <!-- <b-nav-item to="/structure">Structure</b-nav-item> -->
          <b-nav-item to="/script">Script</b-nav-item>
          <b-nav-item to="/recommendations">Recommendations</b-nav-item>

          <b-nav-item to="/export">Export</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-button variant="light" class="feedback-button" v-b-modal="'feedback-modal'" size="sm"
            >Give us feedback</b-button
          >
          <b-button variant="light" @click="resetAll" size="sm">Reset all</b-button>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <router-view />
    <b-toast id="autosave-toast" solid variant="success" :auto-hide-delay="10000" toaster="b-toaster-top-center">
      <template #toast-title>
        <div class="d-flex flex-grow-1 align-items-baseline">
          <strong class="mr-auto">Work saved! <b-icon icon="check2"></b-icon></strong>
        </div>
      </template>
      Pub2Vid autosaves your work for you. <br />
      <small
        >Unless you change the browser or clear your cache, your settings and script should be available whenever you
        run the tool.</small
      >
    </b-toast>
    <b-modal id="feedback-modal" size="lg" centered title="Your feedback is important to us!">
      <iframe
        src="https://docs.google.com/forms/d/e/1FAIpQLSdOpyRKNzdu_lXipqKqDAwPYvGV4b4VmnVR5Y-uk_DZ5EOHaA/viewform?embedded=true"
        width="100%"
        height="600px"
        frameborder="0"
        marginheight="0"
        marginwidth="0"
        >Wird geladen…</iframe
      >
      <template #modal-footer><div></div> </template>
    </b-modal>
  </div>
</template>

<script>
import Vue from "vue";

import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
import VueCompositionAPI from "@vue/composition-api";
import VueYoutube from "vue-youtube";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faWindowMaximize,
  faRandom,
  faProjectDiagram,
  faImage,
  faPlayCircle,
  faVideo,
  faStickyNote,
  faHighlighter,
  faPortrait,
  faMicrophone,
  faClosedCaptioning,
  faMusic,
  faStar,
  faLightbulb,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

library.add(
  faWindowMaximize,
  faRandom,
  faProjectDiagram,
  faImage,
  faPlayCircle,
  faVideo,
  faStickyNote,
  faHighlighter,
  faPortrait,
  faMicrophone,
  faClosedCaptioning,
  faMusic,
  faStar,
  faLightbulb
);

Vue.component("font-awesome-icon", FontAwesomeIcon);

Vue.use(VueCompositionAPI);
Vue.use(BootstrapVue);
Vue.use(IconsPlugin);
Vue.use(VueYoutube);

const $ = require("jquery");
require("jquery-ui-bundle");

export default {
  mounted() {
    window.addEventListener("beforeunload", () => {
      this.$store.dispatch("saveStore");
    });
    this.$root.$on("bv::modal::shown", (bvEvent, modalId) => {
      $("#" + modalId).draggable();
    });
    document.addEventListener("keydown", (e) => {
      if (e.ctrlKey && e.key === "s") {
        // Prevent the Save dialog to open
        e.preventDefault();
        // Place your code here
        this.$bvToast.show("autosave-toast");
      }
    });
  },
  methods: {
    resetAll() {
      if (confirm("Are you sure that you want to reset your settings? All changes will get lost."))
        this.$store.dispatch("resetDefaultState");
    },
  },
};
</script>

<style>
html,
body {
  /* height: 100%; */
  margin: 0;
  padding: 0;
  padding-top: 20px;
  padding-bottom: 20px;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  font-weight: normal;
}
h1 {
  font-size: 1.75rem;
}
h2 {
  font-size: 1.25rem;
}
.navbar-nav .nav-link.router-link-exact-active {
  color: #000;
  font-weight: 500;
}
b {
  font-weight: 500;
}
.feedback-button:hover {
  background-color: #673ab7;
  color: white;
}
/* .toast .toast-header {
  background-color: #6aaca8;
  color: white;
}
.toast .toast-body {
  background-color: #b2e4e169;
} */
</style>
