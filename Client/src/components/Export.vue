<template>
  <div class="export">
    <b-container class="mt-5">
      <h1 class="mb-3">
        Export your template
        <span class="float-right" @click="showInfo = true" style="cursor: pointer"
          ><font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange"
        /></span>
      </h1>
      <b-alert :show="showInfo" dismissible variant="" @dismissed="showInfo = false">
        <font-awesome-icon :icon="['fas', 'lightbulb']" style="color: orange" class="mr-2" />
        If you are happy with your outline, you can export it as a presentation template that contains an unformatted
        version of your script in the speaker notes. If you want to keep the formatting such as font styles and colors,
        you can also download the script as a word document.
      </b-alert>
      <b-alert :show="$store.state.videoStructure.length == 0" dismissible variant="info">
        Your video outline is currently empty. Do you want to load a suggestion based on your settings?
        <b-button variant="info" squared class="m-2 ml-auto" @click="$store.dispatch('setOutline')"
          >Load outline</b-button
        >
      </b-alert>
      <!-- <b-row class="mb-3">
        <b-col>
          <b-button squared class="next-button ml-2 float-right" @click="exportFromServer"
            >Download customized slide deck</b-button
          >

          <b-button squared class="next-button ml-auto float-right" @click="exportWord">Download script only</b-button>
        </b-col>
      </b-row> -->
      <div>
        <b-card
          no-body
          class="overflow-hidden"
          v-for="(section, idx) in $store.state.videoStructure"
          :key="section.name + idx"
        >
          <b-row no-gutters>
            <b-col md="auto">
              <b-card-img
                :src="thumbnailMap[section.name] || demoThumbnail"
                alt="Image"
                class="rounded-0"
                style="max-width: 240px; max-height: 135px; object-fit: cover; object-position: center"
              ></b-card-img>
            </b-col>
            <b-col>
              <b-card-body :title="section.name" class="p-2">
                <b-card-text v-html="$store.state.scriptContent[getSectionKey(section)]"> </b-card-text>
              </b-card-body>
            </b-col>
          </b-row>
        </b-card>
      </div>
      <b-row class="mt-3">
        <b-col>
          <b-button squared class="mr-auto" to="/recommendations">Back to recommendations</b-button>
        </b-col>
        <b-col>
          <!-- <b-button squared class="next-button float-right" to="/recommendations">Continue to recommendations</b-button> -->
          <b-button squared class="next-button ml-2 float-right" @click="exportFromServer"
            >Download customized slide deck</b-button
          >

          <b-button squared class="next-button ml-auto float-right" @click="exportWord">Download script only</b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import pptxgen from "pptxgenjs";
import titleThumbnail from "../assets/titleThumbnail.jpg";
import introductionThumbnail from "../assets/introductionThumbnail.jpg";
import relatedWorkThumbnail from "../assets/relatedWorkThumbnail.jpg";
import demoThumbnail from "../assets/demoThumbnail.jpg";
import evaluationThumbnail from "../assets/evaluationThumbnail.jpg";
import methodThumbnail from "../assets/methodThumbnail.jpg";
import systemArchitectureThumbnail from "../assets/systemArchitectureThumbnail.jpg";
import resultsThumbnail from "../assets/resultsThumbnail.jpg";
import forwardLookingThumbnail from "../assets/forwardLookingThumbnail.jpg";
import reflectionThumbnail from "../assets/reflectionThumbnail.jpg";
import otherThumbnail from "../assets/otherThumbnail.jpg";
export default {
  name: "Script",
  components: {},
  data() {
    return {
      showInfo: true,
      titleThumbnail,
      relatedWorkThumbnail,
      demoThumbnail,
      evaluationThumbnail,
      methodThumbnail,
      systemArchitectureThumbnail,
      resultsThumbnail,
      forwardLookingThumbnail,
      reflectionThumbnail,
      introductionThumbnail,
      otherThumbnail,
      thumbnailMap: {
        Title: titleThumbnail,
        Introduction: introductionThumbnail,
        Demo: demoThumbnail,
        RelatedWork: relatedWorkThumbnail,
        Evaluation: evaluationThumbnail,
        Method: methodThumbnail,
        SystemArchitecture: systemArchitectureThumbnail,
        Results: resultsThumbnail,
        ForwardLooking: forwardLookingThumbnail,
        Reflection: reflectionThumbnail,
        EndingSlide: titleThumbnail,
        End: titleThumbnail,
        Other: otherThumbnail,
      },
    };
  },
  computed: {},
  props: {},
  mounted() {},
  methods: {
    getSectionKey(section) {
      let sameSections = this.$store.state.videoStructure.filter((s) => s.name == section.name);
      if (sameSections.length <= 1) return section.name;
      else {
        let idx = sameSections.findIndex((s) => s == section);
        if (idx > 0) return `${section.name}${idx}`;
        else return section.name;
      }
    },
    b64toBlob(b64Data, contentType = "", sliceSize = 512) {
      const byteCharacters = atob(b64Data);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);

        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      const blob = new Blob(byteArrays, { type: contentType });
      return blob;
    },
    exportFromServer() {
      let exportBody = this.$store.state.videoStructure.map((s) => {
        return {
          section: s.name,
          duration: new Date(s.to - s.from).getMinutes() * 60 + new Date(s.to - s.from).getSeconds(),
          notes: this.$store.state.plainScriptText[this.getSectionKey(s)] || "",
        };
      });
      fetch(this.$store.state.backendURL + "/slides", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: JSON.stringify(exportBody),
      })
        .then((res) => res.json())
        .then((data) => {
          let fileName = "PresentationTemplate.pptx";
          //console.log(data["slides"]);
          let fullTextAsBlob = this.b64toBlob(data["slides"].substr(2, data["slides"].length - 3));
          //console.log(fullTextAsBlob);
          var a = document.createElement("a");
          document.body.appendChild(a);
          a.style = "display: none";
          let url = window.URL.createObjectURL(fullTextAsBlob);
          a.href = url;
          a.download = fileName;
          a.click();
          window.URL.revokeObjectURL(url);
        });
    },
    exportPPT() {
      // 1. Create a Presentation
      let pres = new pptxgen();

      this.$store.state.videoStructure.forEach((section) => {
        // 2. Add a Slide to the presentation
        let slide = pres.addSlide();

        // 3. Add 1+ objects (Tables, Shapes, etc.) to the Slide
        slide.addText(section.name, {
          x: 1.5,
          y: 1.5,
          color: "363636",
          fill: { color: "F1F1F1" },
          align: pres.AlignH.center,
          placeholder: "body",
        });

        if (section.name in this.$store.state.plainScriptText) {
          slide.addNotes(this.$store.state.plainScriptText[section.name]);
          slide._slideObjects[slide._slideObjects.length - 1].options = {
            x: 1.5,
            y: 1.5,
            color: "AA7777",
            fill: { color: "F1F1F1" },
            align: pres.AlignH.center,
          };
        }
        console.log(slide);
      });

      // 4. Save the Presentation
      let fileName = "test.pptx";
      console.log(pres);
      pres.write("arraybuffer").then((data) => {
        /* console.log("write as base64: Here are 0-100 chars of `data`:\n");
      let decoded = new TextDecoder().decode(data);
      decoded = decoded.substring(decoded.indexOf("<?xml"));
      console.log(decoded); */
        let fullText = new TextDecoder().decode(data);
        //console.log(fullText.split("<?xml"));
        var a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";
        var blob = new Blob([new Uint8Array(new TextEncoder().encode(fullText))]),
          url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        //a.click();
        window.URL.revokeObjectURL(url);
      });
      pres.writeFile({ fileName: "Sample Presentation.pptx" });
    },
    exportWord() {
      var header =
        "<html xmlns:o='urn:schemas-microsoft-com:office:office' " +
        "xmlns:w='urn:schemas-microsoft-com:office:word' " +
        "xmlns='http://www.w3.org/TR/REC-html40'>" +
        "<head><meta charset='utf-8'><title>Export HTML to Word Document with JavaScript</title></head><body>";
      var footer = "</body></html>";
      var sourceHTML = header;
      this.$store.state.videoStructure.forEach((section) => {
        sourceHTML += `<h1>${section.name}</h1>`;
        let sectionKey = this.getSectionKey(section);
        if (sectionKey in this.$store.state.scriptContent) sourceHTML += this.$store.state.scriptContent[sectionKey];
      });
      sourceHTML += footer;
      var source = "data:application/vnd.ms-word;charset=utf-8," + encodeURIComponent(sourceHTML);
      var fileDownload = document.createElement("a");
      document.body.appendChild(fileDownload);
      fileDownload.href = source;
      fileDownload.download = "script.doc";
      fileDownload.click();
      document.body.removeChild(fileDownload);
    },
  },
};
</script>
