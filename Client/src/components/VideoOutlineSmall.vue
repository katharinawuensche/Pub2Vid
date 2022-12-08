<template>
  <div>
    <youtube
      :video-id="videoId"
      :fitParent="true"
      :resize="true"
      @playing="playing"
      @pause="paused"
      @ended="paused"
      @ready="initChart"
      ref="youtube"
    ></youtube>
    <div :id="`video-timeline${id}`" ref="timelineSmall"></div>
    <!-- Current section(s): {{ currentSection }} -->
  </div>
</template>

<script>
import TimelinesChart from "timelines-chart";
import * as d3 from "d3";
let colorScale = {
  Title: "31, 119, 180",
  Introduction: "255, 127, 14",
  /* Contributions: "44, 160, 44", */
  SystemArchitecture: "214, 39, 40",
  EndingSlide: "148, 103, 189",
  Results: "140, 86 ,75",
  Demo: "227, 119, 194",
  Method: "127, 127, 127",
  Evaluation: "188, 189, 34",
  VideoOutline: "23 ,190 ,207",
  RelatedWork: "255, 255, 179",
  Other: "190, 186, 218",
  /* Conclusion: "251, 128, 114", */
  Reflection: "128, 177, 211",
  ForwardLooking: "147, 147, 224",
};
const d3ColorScale = d3
  .scaleOrdinal()
  .domain(Object.keys(colorScale))
  .range(Object.values(colorScale).map((v) => `rgba(${v},1)`));
export default {
  components: {},
  props: {
    id: String,
    outline: Array,
    videoId: String,
  },
  data() {
    return {
      interval: null,
      myChart: null,
      currentSection: "",
    };
  },
  created() {},
  computed: {
    player() {
      return this.$refs.youtube.player;
    },
  },
  watch: {
    outline() {
      if (!this.myChart) return;
      this.myChart.data([
        {
          group: "",
          data: [
            {
              label: "",
              data: this.outline.map((o) => {
                return {
                  timeRange: [o.from, o.to],
                  val: o.name,
                };
              }),
            },
          ],
        },
      ]);
      this.myChart.refresh();
    },
  },
  methods: {
    useThisOutline() {
      // if (confirm("Do you want to use this video outline and continue with the next step?"))
      this.$store.dispatch("applyOutline", this.$store.state.outlineSuggestions[+this.id]);
    },
    playing() {
      if (!this.interval) this.interval = window.setInterval(this.updateProgressIndicator, 500);
    },
    paused() {
      if (this.interval) window.clearInterval(this.interval);
      this.interval = null;
    },
    async updateProgressIndicator() {
      if (!this.player || typeof this.player.getCurrentTime !== "function") return;
      let currentTime = await this.player.getCurrentTime();
      let progress = currentTime / (await this.player.getDuration());

      document
        .querySelector(`#video-timeline${this.id} svg #timeMarker`)
        ?.setAttribute(
          "transform",
          `translate(${progress * +document.querySelector(`#video-timeline${this.id} svg`)?.getAttribute("width")}, 0)`
        );
      /* this.$refs.sectionLabel?.setAttribute(
        "transform",
        `translate(${progress * +this.$refs.svg.getAttribute("width")}, 0)`
      ); */
      let currentTimeAsDate = new Date(new Date(0).setSeconds(currentTime));
      let currentSectionName = this.outline
        .filter((o) => o.from <= currentTimeAsDate && o.to >= currentTimeAsDate)
        .map((s) => s.name)
        .join(", ");
      this.currentSection = currentSectionName;
      //if (this.$refs.sectionLabel) this.$refs.sectionLabel.innerHTML = currentSectionName;

      //updateCurrentSectionLabels(Object.values(preparedData)[0], this.player.getCurrentTime());
    },
    resizeChart() {
      if (!this.myChart) return;
      this.myChart.width(this.$el.clientWidth);
      //this.$refs.svg.setAttribute("width", this.$el.clientWidth);
      this.myChart.refresh();
    },
    addTimeMarker() {
      let svg = document.querySelector(`#video-timeline${this.id} svg`);
      let g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.innerHTML = `<line id="timeMarker" x1="-1" y1="0" x2="-1" y2="36" style="stroke:rgb(255,0,0);stroke-width:2">`;
      /*   g.setAttribute("transform", "translate(50, 26)"); */
      svg.appendChild(g);
      //console.log(svg);
    },
    initChart() {
      // if (!this.$parent.$refs[`videocard${this.id}`] || this.$parent.$refs[`videocard${this.id}`].length <= 0) return;
      document.querySelector(`#video-timeline${this.id}`).innerHTML = "";
      this.myChart = TimelinesChart();
      this.myChart.data([
        {
          group: "",
          data: [
            {
              label: "",
              data: this.outline.map((o) => {
                return {
                  timeRange: [o.from, o.to],
                  val: o.name,
                };
              }),
            },
          ],
        },
      ]);
      this.myChart.zQualitative(true);
      this.myChart.timeFormat("%M:%S");
      this.myChart.maxHeight(200);
      this.myChart.maxLineHeight(30);
      this.myChart.width(this.$el?.clientWidth);
      this.myChart.rightMargin(0);
      this.myChart.leftMargin(0);
      this.myChart.topMargin(0);
      this.myChart.bottomMargin(0);
      this.myChart.enableOverview(false);
      this.myChart.zColorScale(d3ColorScale);
      this.myChart.segmentTooltipContent((d) => `<span>${d.val}</span>`);
      this.myChart.onSegmentClick(async (d) => {
        let progress =
          ((await this.player.getDuration()) * (d.timeRange[0].getMinutes() * 60 + d.timeRange[0].getSeconds())) /
          this.$store.state.duration;
        this.player.seekTo(progress);
      });
      this.myChart(document.querySelector(`#video-timeline${this.id}`));

      this.addTimeMarker();
      //this.$refs.svg.setAttribute("width", this.$parent.$refs[`videocard${this.id}`][0]?.clientWidth);
    },
  },
  mounted() {
    //console.log(this.$refs);
    //this.initChart();
    window.addEventListener("resize", this.resizeChart);

    //console.log(this.player, this.$refs.svg.getAttribute("width"));
  },
  destroyed() {
    this.paused();
  },
};
</script>

<style>
.chart-tooltip {
  background: #000 !important;
  font-size: 0.875rem;
}
.timelines-chart .series-group,
.timelines-chart .series-segment {
  cursor: pointer !important;
}
</style>
