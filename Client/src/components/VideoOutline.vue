<template>
  <div :id="`example-gantt${id}`" class="mt-3"></div>
</template>

<script>
import { SvelteGantt, SvelteGanttTable } from "svelte-gantt";
import moment from "moment";
import "svelte-gantt/css/svelteGantt.css";

export default {
  components: {},
  props: {
    id: String,
    outlines: Array,
    draggable: Boolean,
    selectable: Boolean,
    deletable: Boolean,
    seconds: Number,
    outlineNames: Array,
  },
  data() {
    return {
      gantt: {},
      selectedRow: 0,
      backdoor: 0,
      options: {
        rows: [],
        tasks: [],
        headers: [
          /* { unit: "day", format: "MMMM Do" }, */
          { unit: "second", format: "mm:ss", sticky: false, offset: 10 },
        ],
        fitWidth: true,
        minWidth: 100,
        magnetUnit: "second",
        magnetOffset: 0,
        from: moment("1970-01-01 00:00:00Z"),
        to: moment(
          `1970-01-01 00:${Math.floor(this.$store.state.duration / 60)}:${0 +
            Math.floor(this.$store.state.duration % 60)}Z`
        ),
        tableHeaders: [{ title: "", property: "label" }],
        ganttBodyModules: [],
        ganttTableModules: this.outlineNames && this.outlineNames.length > 0 ? [SvelteGanttTable] : [],
      },
      interval: null,
    };
  },
  created() {
    window.moment = moment;
  },
  destroyed() {
    delete window.moment;
    window.clearInterval(this.interval);
    /* this.gantt.$set({
      rows: [],
    }); */
    console.log("unmount");
  },
  computed: {
    rows() {
      this.backdoor;
      return this.outlines
        .map((_, idx) => {
          return {
            id: idx,
            label: this.outlineNames ? `${this.outlineNames[idx]}` : "",
            classes: `${this.$store.state.selectedOutlineIdx == idx && this.selectable ? "rowSelected" : ""}`,
            contentHtml:
              this.outlines.length > 1
                ? "<div style='text-align: center; top: 50%; transform: translateY(-50%); position: relative;'>🖱️ Click on an outline below to select it</div>"
                : "",
          };
        })
        .concat(
          this.deletable
            ? [
                {
                  label: "",
                  id: this.outlines.length,
                  enableDragging: true,
                  contentHtml: "<div style='text-align: center'>🗑 Drag here to remove section</div>",
                },
              ]
            : []
        );
    },
    tasks() {
      this.backdoor;
      return this.outlines
        .map((o, oIdx) =>
          o.map((section, sIdx) => {
            return {
              id: oIdx * 10 + sIdx,
              resourceId: oIdx,
              label: section.name,
              //html: `<p contenteditable oninput="document.querySelector('#exampleModal').modal()">${section.name}</p>`,
              from: this.time(section.from),
              to: this.time(section.to),
              classes: `${section.name.toLowerCase()} ${this.draggable ? "" : "noDrag"} ${
                this.$store.state.selectedOutlineIdx == oIdx && this.selectable ? "rowSelected" : ""
              }  ${this.selectable ? "selectable" : ""}`,
              enableDragging: this.draggable,
            };
          })
        )
        .flat();
    },
  },
  watch: {
    rows() {
      this.gantt.$set({
        rows: this.rows,
        to: moment(
          `1970-01-01 00:${Math.floor(this.$store.state.duration / 60)}:${Math.floor(this.$store.state.duration % 60)}Z`
        ),
      });
      this.gantt.unselectTasks();
    },
    tasks() {
      this.gantt.$set({
        tasks: this.tasks,
        to: moment(
          `1970-01-01 00:${Math.floor(this.$store.state.duration / 60)}:${Math.floor(this.$store.state.duration % 60)}Z`
        ),
      });
      this.gantt.unselectTasks();
    },
    selectedRow() {
      this.gantt.$set({
        rows: this.rows,
      });
    },
  },
  methods: {
    time(dateTime) {
      if (typeof dateTime == "string") dateTime = moment(dateTime).toDate();
      return moment(
        `1970-01-01 00:${dateTime
          .getMinutes()
          .toString()
          .padStart(2, "0")}:${dateTime
          .getSeconds()
          .toString()
          .padStart(2, "0")}Z`
      );
    },
    setEndOfContenteditable(contentEditableElement) {
      let range, selection;
      if (document.createRange) {
        //Firefox, Chrome, Opera, Safari, IE 9+
        range = document.createRange(); //Create a range (a range is a like the selection but invisible)
        range.selectNodeContents(contentEditableElement); //Select the entire contents of the element with the range
        range.collapse(false); //collapse the range to the end point. false means collapse to end rather than the start
        selection = window.getSelection(); //get the selection object (allows you to change selection)
        selection.removeAllRanges(); //remove any selections already made
        selection.addRange(range); //make the range you have just created the visible selection
      } else if (document.selection) {
        //IE 8 and lower
        range = document.body.createTextRange(); //Create a range (a range is a like the selection but invisible)
        range.moveToElementText(contentEditableElement); //Select the entire contents of the element with the range
        range.collapse(false); //collapse the range to the end point. false means collapse to end rather than the start
        range.select(); //Select the range (make it the visible selection
      }
    },
  },
  mounted() {
    this.gantt = new SvelteGantt({
      target: document.getElementById("example-gantt" + this.id),
      props: this.options,
    });
    this.gantt.$set({
      rows: this.rows,
      tasks: this.tasks,
    });
    if (this.selectable)
      this.gantt.api.tasks.on.select((task) => {
        if (
          this.$store.state.videoStructure.length == 0 ||
          confirm("Do you want to replace your current outline with this one?")
        ) {
          //this.$store.state.selectedOutlineIdx = task[0].model.resourceId;
          this.$store.state.videoStructure = this.outlines[task[0].model.resourceId];
        }
      });
    if (this.draggable) {
      this.gantt.api.tasks.on.changed((obj) => {
        let task = obj[0].task;
        if (this.deletable && obj[0].targetRow != obj[0].sourceRow) {
          // delete task
          this.$store.state.videoStructure.splice(task.model.id, 1);
          this.$store.state.videoStructure.sort((a, b) => a.from - b.from);
          this.$store.state.videoStructure[0].from = this.options.from.toDate();
          this.$store.state.videoStructure[this.$store.state.videoStructure.length - 1].to = this.options.to.toDate();
          this.$store.state.videoStructure.forEach((s, idx) => {
            if (idx > 0) s.from = this.$store.state.videoStructure[idx - 1].to;
            if (idx < this.$store.state.videoStructure.length - 1)
              s.to = this.$store.state.videoStructure[idx + 1].from;
          });
          return;
        }
        let structureComponent = this.$store.state.videoStructure[task.model.id];
        structureComponent.from = task.model.from._d;
        structureComponent.to = task.model.to._d;

        this.$store.state.videoStructure.sort((a, b) => a.from - b.from);
        this.$store.state.videoStructure[0].from = this.options.from.toDate();
        this.$store.state.videoStructure[this.$store.state.videoStructure.length - 1].to = this.options.to.toDate();

        let idx = this.$store.state.videoStructure.indexOf(structureComponent);
        if (idx > 0) this.$store.state.videoStructure[idx - 1].to = structureComponent.from;
        if (idx < this.$store.state.videoStructure.length - 1)
          this.$store.state.videoStructure[idx + 1].from = structureComponent.to;
        this.$store.state.videoStructure.forEach((s, idx) => {
          if (idx > 0) s.from = this.$store.state.videoStructure[idx - 1].to;
          if (idx < this.$store.state.videoStructure.length - 1) s.to = this.$store.state.videoStructure[idx + 1].from;
          if (s.to < s.from) s.to = s.from;
        });
      });
      if (this.draggable) {
        this.interval = window.setInterval(() => {
          this.$store.state.videoStructure.forEach((section, idx) => {
            let e = document.getElementById(`example-gantt${this.id}`).querySelectorAll(".sg-task-content")[idx];
            e.setAttribute("contenteditable", "true");
            e.oninput = () => {
              section.name = e.innerText;
            };
            e.parentElement.onclick = () => {
              e.focus();
              this.setEndOfContenteditable(e);
            };
            e.parentElement.ondrag = () => {
              e.focus();
              this.setEndOfContenteditable(e);
            };
          });
        }, 500);
      }
    }
    console.log(this.gantt);
    this.backdoor++;
    this.gantt.api.gantt.on.viewChanged();
  },
};
</script>

<style>
.sg-header {
  pointer-events: none;
}
/* .sg-header-scroller {
  border-right: 1px solid #ababab !important;
  border-left: 1px solid #ababab;
} */
/* .sg-row.rowSelected {
  border: 3px solid #006c66;
} */
.sg-task.noDrag:hover::before,
.sg-task.noDrag:hover::after {
  display: none !important;
}
.sg-task.selected {
  outline: none !important;
}
.sg-task.rowSelected {
  font-weight: bold;
  /* border-top: 3px solid black;
  border-bottom: 3px solid black; */
}
.sg-task.selectable {
  cursor: pointer;
  /* border-top: 3px solid black;
  border-bottom: 3px solid black; */
}
.sg-task {
  background: #333333;
  border: 1px solid white;
  color: white;
  text-align: center;
}
.sg-task.title {
  background: rgba(31, 119, 180, 1);
}
.sg-task.introduction {
  background: rgba(255, 127, 14, 1);
}
.sg-task.systemarchitecture {
  background: rgba(214, 39, 40, 1);
}
.sg-task.endingslide,
.sg-task.end {
  background: rgba(148, 103, 189, 1);
}
.sg-task.results {
  background: rgba(140, 86, 75, 1);
}
.sg-task.demo {
  background: rgba(227, 119, 194, 1);
}
.sg-task.method {
  background: rgba(127, 127, 127, 1);
}
.sg-task.evaluation {
  background: rgba(188, 189, 34, 1);
}
.sg-task.videooutline {
  background: rgba(23, 190, 207, 1);
}
.sg-task.relatedwork {
  background: rgba(210, 210, 159, 1);
}
.sg-task.other {
  background: rgba(190, 186, 218, 1);
}
.sg-task.reflection {
  background: rgba(128, 177, 211, 1);
}
.sg-task.forwardlooking {
  background: rgba(147, 147, 224, 1);
}
.sg-task-content.svelte-19txnoa {
  position: relative;
  padding-left: unset;
  justify-content: center;
  overflow: hidden;
}
/* .column-header-cell-label {
  left: 0 !important;
} */
.column-header-cell {
  justify-content: flex-end !important;
}
.column-header-row .column-header-cell:first-child {
  visibility: hidden;
}
.column-header-row {
  float: right;
  margin-right: 5px;
}
.deleteButton {
  position: absolute;
  top: -7px;
  right: -7px;
  width: 15px;
  height: 15px;
  background: url("https://icons.getbootstrap.com/assets/icons/dash-circle-fill.svg");
  background-size: contain;
  /* filter: invert(); */
  /* z-index: 2; */
}
.sg-task-content {
  overflow: visible !important;
  /* z-index: -1; */
}
.sg-table-rows .sg-table-row:first-of-type {
  font-weight: bold !important;
}
</style>
