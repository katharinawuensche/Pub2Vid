<template>
  <div class="settings">
    <b-container class="mt-5">
      <h1 class="mb-5">
        Define the overall structure of your video
      </h1>
      <b-row class="my-4" align-v="center">
        <b-col sm="12">
          <div><b>Selected Outline ✏️️</b></div>
          <VideoOutline :outlines="[$store.state.videoStructure]" :draggable="true" :selectable="false"></VideoOutline>
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
            <b
              >{{
                new Date(section.to - section.from).getMinutes() * 60 +
                  new Date(section.to - section.from).getSeconds()
              }}s {{ section.name }}</b
            >
            <p>Section description...</p>
          </div>
        </b-col>
      </b-row>

      <b-row>
        <b-button squared class="mr-auto" to="/" variant="light">Back to settings</b-button>
        <b-button squared class="next-button ml-auto" to="/script">Load and refine outline</b-button>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import VideoOutline from "./VideoOutline.vue";
export default {
  name: "Structure",
  components: {
    VideoOutline,
  },
  data() {
    return {};
  },
  props: {},
  computed: {},
  mounted() {},
  methods: {},
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
</style>
