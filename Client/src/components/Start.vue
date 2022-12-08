<template>
  <div class="start">
    <b-container class="mt-5">
      <h1 class="mb-3 font-weight-light title">
        Welcome to Pub2Vid!
      </h1>
      <h2 class="font-weight-light subtitle">Plan and structure scientific videos within minutes</h2>

      <b-row class="w-75 mx-auto mt-3">
        <b-col>
          <b-list-group flush class="mx-auto mt-3">
            <b-list-group-item class="align-items-center my-2">
              <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-3"><b-icon icon="gear" scale="1.5" class="title-icon"></b-icon>Set your preferences</h5>
              </div>
              <p class="mb-2">
                Set your preferences such as video style and duration and choose between multiple recommendations for
                your video outline.
              </p>
            </b-list-group-item>
            <b-list-group-item class="align-items-center my-2">
              <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-3"><b-icon icon="pencil" scale="1.5" class="title-icon"></b-icon>Write your script</h5>
              </div>
              <p class="mb-2">
                Modify the outline according to your needs and write a video script that matches your desired length.
              </p>
            </b-list-group-item>
            <b-list-group-item class="align-items-center my-2">
              <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-3">
                  <b-icon icon="collection-play" scale="1.5" class="title-icon"></b-icon>View examples and
                  recommendations
                </h5>
              </div>
              <p class="mb-2">
                Get some inspiration by viewing examples for complete videos, single sections or individual visual and
                audio elements that match your needs.
              </p>
            </b-list-group-item>
            <b-list-group-item class="align-items-center my-2">
              <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-3">
                  <b-icon icon="download" scale="1.5" class="title-icon"></b-icon>Export your template
                </h5>
              </div>
              <p class="mb-2">
                Export the script or a customized slide deck to use it with any presentation or video editing software
                of your choice.
              </p>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
      <b-row>
        <b-col class="d-flex justify-content-center">
          <b-button squared class="next-button mx-auto px-5 py-2 mt-3" to="/settings"
            ><h5 class="mb-0 py-1 px-3">Get started <b-icon icon="arrow-right" scale="1" class="ml-2"></b-icon></h5>
          </b-button>
        </b-col>
      </b-row>
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
        <b-nav-item to="/about">About this project</b-nav-item>
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
h1.title {
  font-size: 3rem;
  text-align: center;
  color: #006c66;
}
h2.subtitle {
  font-size: 2rem;
  text-align: center;
  color: #006c66;
}
.title-icon {
  margin-right: 1rem;
}
h5 {
  font-weight: normal;
}
</style>
