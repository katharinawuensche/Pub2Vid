<template>
  <div class="start">
    <b-container class="mt-5">
      <h1 class="mb-3 font-weight-light" style="color: #006c66;">
        About this project
      </h1>

      <b-row class="mt-3">
        <b-col>
          <p>
            Pub2Vid aims at helping researchers with the creation, especially the planning and structuring, of
            scientific videos to summarize their publications.
          </p>
          <p>
            Since videos can be an effective medium for science communication, more and more researchers are encouraged
            (or required) to submit video summaries of their work to conferences or upload them to their institutions'
            websites or YouTube channels. However, many of them have no experience with video creation and do not know
            where to start. This is where Pub2Vid comes into play.
          </p>
          <p>
            Based on the analysis of 40 computer science videos (ranging from 90 seconds to 9 minutes, mostly in the
            fields of human computer interaction or visualization), our tool makes recommendations with respect to video
            outlines as well as visual and audio elements. We therefore conducted a user study with more than 60
            participants who rated the videos in three categories: informativity, creativity and enthusiasm. The ratings
            and comments of the participants provided us with insights about popular and effective video features which
            were used for the generation of outline templates that fit to the different video styles. These can then be
            used and adapted by the user and should help them with the preparation of their video script. We provide
            real video examples for different elements and sections which can be used as a reference or inspiration for
            the users' own videos.
          </p>
          <!-- <p>
            This project is a collaboration of researchers at the University of Vienna and the Ohio State University. If
            you want to get in touch, feel free to contact us at
            <a href="mailto:katharina.wuensche@unvie.ac.at" class="mail">katharina.wuensche@univie.ac.at</a>.
          </p> -->
        </b-col>
      </b-row>
      <!--  <b-row>
        <b-col class="">
          <b-button squared class="next-button px-5 py-2 mt-3" to="/settings"
            >Get started <b-icon icon="arrow-right" scale="1" class="ml-2"></b-icon>
          </b-button>
        </b-col>
      </b-row> -->
    </b-container>

    <b-navbar type="light" variant="light" fixed="bottom">
      <!-- <b-navbar-brand href="https://univie.ac.at" target="_blank">
        <img
          src="https://communications.univie.ac.at/fileadmin/user_upload/d_oeffentlichkeitsarbeit/Logos/2016-02/Uni_Logo_2016.png"
          height="100"
        />
      </b-navbar-brand>
      <b-navbar-brand href="https://osu.edu/" target="_blank">
        <img src="https://www.moldex3d.com/wp-content/uploads/2014/02/OSU_Horizontal-2nekv1k.png" height="100" />
      </b-navbar-brand> -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item to="#">About this project</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<script>
export default {
  name: "Settings",
  components: {},
  data() {
    return {};
  },
};
</script>
<style>
.start {
  padding-bottom: 100px;
}
.title-icon {
  margin-right: 1rem;
}
a.mail {
  color: #006c66;
}
</style>
