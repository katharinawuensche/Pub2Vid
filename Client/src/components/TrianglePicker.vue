<template>
  <div style="width: 200px; position: relative;">
    <div style="position: absolute; vertical-align: top; text-align: center; width: 100%">
      Informativity<b-icon icon="info-circle" scale="0.8" shift-v="6" id="tooltip-target-informativity"></b-icon>
      <b-tooltip target="tooltip-target-informativity" triggers="hover click">
        How much information about the publication and its content do you want to communicate through your video?
      </b-tooltip>
    </div>
    <canvas id="trianglePicker"></canvas>
    <div style="float: left; margin-top: -35px; position: relative; z-index: 1;">
      Creativity<b-icon icon="info-circle" scale="0.8" shift-v="6" id="tooltip-target-creativity"></b-icon>
      <b-tooltip target="tooltip-target-creativity" triggers="hover click" placement="bottom">
        How creative do you want the video to be?
      </b-tooltip>
    </div>
    <div style="float: right; margin-top: -35px; position: relative; z-index: 1;">
      Enthusiasm<b-icon icon="info-circle" scale="0.8" shift-v="6" id="tooltip-target-enthusiasm"></b-icon>
      <b-tooltip target="tooltip-target-enthusiasm" triggers="hover click" placement="bottom">
        How much enthusiasm about the topic and your project do you want to communicate through your video?
      </b-tooltip>
    </div>
  </div>
</template>

<script>
export default {
  name: "TrianglePicker",
  data() {
    return {
      touched: false,
      selectedPoint: null,
      g: null,
      vec2: {},
      height: 600,
      width: 600,
      scalingFactor: 3,
      tri_point_names: ["Informativity", "Creativity", "Enthusiasm"],
      tri_colors: [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
      ],
    };
  },
  computed: {
    initCoords() {
      return [
        this.$store.state.priorities.informativity,
        this.$store.state.priorities.creativity,
        this.$store.state.priorities.enthusiasm,
      ];
    },
    tri() {
      return [
        [this.width * 0.5, 35 * this.scalingFactor],
        [35 * this.scalingFactor, this.height - 35 * this.scalingFactor],
        [this.width - 35 * this.scalingFactor, this.height - 35 * this.scalingFactor],
      ];
    },
    bary_point() {
      return this.bary_to_cartesian(this.initCoords);
    },
  },
  props: {},
  methods: {
    bary_to_cartesian(coefficients) {
      let result = [0, 0];
      coefficients.forEach((coeff, idx) => {
        result[0] += coeff * this.tri[idx][0];
        result[1] += coeff * this.tri[idx][1];
      });
      return result;
    },
    initPicker() {
      let g = document.querySelector("#trianglePicker").getContext("2d");
      g.canvas.width = this.width;
      g.canvas.height = this.height;
      g.canvas.className = "touchable";
      this.g = g;
      let vec2 = {};
      vec2.add = function(a, b) {
        return [a[0] + b[0], a[1] + b[1]];
      };
      vec2.sub = function(a, b) {
        return [a[0] - b[0], a[1] - b[1]];
      };
      vec2.scale = function(v, k) {
        return [v[0] * k, v[1] * k];
      };
      vec2.length = function(v) {
        return Math.sqrt(v[0] * v[0] + v[1] * v[1]);
      };
      vec2.distance = function(a, b) {
        let dx = b[0] - a[0];
        let dy = b[1] - a[1];
        return Math.sqrt(dx * dx + dy * dy);
      };
      vec2.dot = function(a, b) {
        return a[0] * b[0] + a[1] * b[1];
      };
      vec2.normalize = function(v) {
        let d = Math.sqrt(v[0] * v[0] + v[1] * v[1]);
        return d > 0 ? [v[0] / d, v[1] / d] : v;
      };
      vec2.area = function(a, b) {
        return a[0] * b[1] - b[0] * a[1];
      };
      vec2.angle = function(a, b) {
        return Math.acos(vec2.dot(a, b) / (vec2.length(a) * vec2.length(b)));
      };
      this.vec2 = vec2;

      window.addEventListener("mousedown", this.touchstart, false);
      window.addEventListener("mouseup", this.touchend, false);
      window.addEventListener("mousemove", this.touchmove, false);
      window.addEventListener("touchstart", this.touchstart, false);
      window.addEventListener("touchend", this.touchend, false);
      window.addEventListener("touchmove", this.touchmove, false);

      this.loop();
    },
    loop() {
      this.draw();
      window.requestAnimationFrame(this.loop);
    },
    touchmove(e) {
      if (e.target.className === "touchable") {
        e.preventDefault();
        let p = this.getTouchCoord(e);
        if (this.touched) {
          if (this.selectedPoint) {
            this.selectedPoint[0] = p[0];
            this.selectedPoint[1] = p[1];
          }
        } else {
          let bary_coords = this.barycentric(this.tri, p);
          if (bary_coords.find((e) => e > 1 || e < 0)) {
            this.g.canvas.style.cursor = "default";
          } else {
            this.g.canvas.style.cursor = "crosshair";
          }
        }
      }
    },
    touchend(e) {
      if (e.target.className === "touchable") {
        e.preventDefault();
        this.touched = false;
        this.selectedPoint = null;
        this.g.canvas.style.cursor = "crosshair";
        let p = this.getTouchCoord(e);
        let bary_coords = this.barycentric(this.tri, p);
        if (!e.targetTouches) {
          this.$store.state.priorities = {
            creativity: bary_coords[1],
            enthusiasm: bary_coords[2],
            informativity: bary_coords[0],
          };
        }
        this.$store.dispatch("getRecommendedVideos");
      }
    },
    touchstart(e) {
      if (e.target.className === "touchable") {
        e.preventDefault();
        let p = this.getTouchCoord(e);
        let bary_coords = this.barycentric(this.tri, p);
        if (!bary_coords.find((e) => e > 1 || e < 0)) {
          this.touched = true;
          this.bary_point[0] = p[0];
          this.bary_point[1] = p[1];
          let bary_coords = this.barycentric(this.tri, p);
          if (e.targetTouches && e.targetTouches.length > 0) {
            console.log("touch");
            this.$store.state.priorities = {
              creativity: bary_coords[1],
              enthusiasm: bary_coords[2],
              informativity: bary_coords[0],
            };
          }
        }
      }
      //}
    },
    getTouchCoord(e) {
      let p = [0, 0];
      if (e.targetTouches) {
        if (e.targetTouches.length > 0) {
          console.log(e);
          let rect = e.target.getBoundingClientRect();
          let x = e.targetTouches[0].pageX - rect.left;
          let y = e.targetTouches[0].pageY - rect.top;
          p[0] = x * this.scalingFactor;
          p[1] = y * this.scalingFactor;
        }
      } else {
        p[0] = e.offsetX * this.scalingFactor;
        p[1] = e.offsetY * this.scalingFactor;
      }
      return p;
    },
    draw() {
      this.g.clearRect(0, 0, this.width, this.height);

      let bary_coords = this.barycentric(this.tri, this.bary_point);

      this.g.strokeStyle = "rgba(255, 255, 255, 1)";
      this.g.lineWidth = 0;
      this.drawTriangle(this.tri);
      this.g.stroke();
      this.g.lineWidth = 1;

      this.g.fillStyle = this.getColorString(bary_coords, 1);
      this.g.beginPath();
      this.g.strokeStyle = "rgba(0, 0, 0, 0.5)";
      this.g.lineWidth = 1;
      this.g.arc(this.bary_point[0], this.bary_point[1], 5 * this.scalingFactor, 0, Math.PI * 2);
      this.g.fillStyle = "white";
      this.g.fill();
      this.g.stroke();

      this.g.fillStyle = "black";
      /* this.g.font = `${window.getComputedStyle(document.body).fontSize.replace("px", "") *
        0.85 *
        this.scalingFactor}px Arial`;
      for (let i = 0; i < this.tri_point_names.length; i++) {
        let p = this.tri[i];
        let name = this.tri_point_names[i];
        this.g.textAlign = "center";
        this.g.fillText(name, p[0], i == 0 ? p[1] - 8 * this.scalingFactor : p[1] + 16 * this.scalingFactor);
        let textWidth = this.g.measureText(name).width / 2 + 32;
        this.g.fillText("ⓘ", p[0] + textWidth, i == 0 ? p[1] - 8 * this.scalingFactor : p[1] + 16 * this.scalingFactor);
      } */

      /* let bary_string = bary_coords
        .map(function(item) {
          return item.toFixed(2);
        })
        .join(", ");
 */
      /* this.g.font = `${window.getComputedStyle(document.body).fontSize.replace("px", "") *
        0.5 *
        this.scalingFactor}px Arial`;
      this.g.fillText(bary_string, this.bary_point[0], this.bary_point[1] + 18 * this.scalingFactor); */
    },
    getColorString(c, a) {
      let r = Math.floor(c[0] * 255);
      let g = Math.floor(c[1] * 255);
      let b = Math.floor(c[2] * 255);
      "rgba(" + r + "," + g + "," + b + "," + a + ")";
      return "rgb(0,0,0)";
    },

    drawTriangle(tri) {
      let pa = tri[0],
        pb = tri[1],
        pc = tri[2];
      this.g.beginPath();
      this.g.moveTo(pa[0], pa[1]);
      this.g.lineTo(pb[0], pb[1]);
      this.g.lineTo(pc[0], pc[1]);
      let grd = this.g.createRadialGradient(
        this.bary_to_cartesian([0.33, 0.33, 0.33])[0],
        this.bary_to_cartesian([0.33, 0.33, 0.33])[1],
        this.scalingFactor,
        this.bary_to_cartesian([0.33, 0.33, 0.33])[0],
        this.bary_to_cartesian([0.33, 0.33, 0.33])[1],
        120 * this.scalingFactor
      );
      grd.addColorStop(0, "#006c66");
      grd.addColorStop(1, "white");
      this.g.fillStyle = grd;
      this.g.fill();
      this.g.closePath();
    },

    barycentric(tri, p) {
      let v0 = this.vec2.sub(tri[1], tri[0]);
      let v1 = this.vec2.sub(tri[2], tri[0]);
      let v2 = this.vec2.sub(p, tri[0]);
      let d00 = this.vec2.dot(v0, v0);
      let d01 = this.vec2.dot(v0, v1);
      let d11 = this.vec2.dot(v1, v1);
      let d20 = this.vec2.dot(v2, v0);
      let d21 = this.vec2.dot(v2, v1);
      let denom = d00 * d11 - d01 * d01;
      let v = (d11 * d20 - d01 * d21) / denom;
      let w = (d00 * d21 - d01 * d20) / denom;
      let u = 1 - v - w;
      return [u, v, w];
    },
    lerp(a, b, t) {
      return a + (b - a) * t;
    },
  },
  mounted() {
    this.initPicker();
  },
};
</script>
<style scoped>
canvas {
  cursor: crosshair;
  width: 200px;
  height: 200px;
}
</style>
