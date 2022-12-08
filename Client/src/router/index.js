import Vue from "vue";
import VueRouter from "vue-router";
import About from "../components/About";
import Start from "../components/Start";
import Settings from "../components/Settings";
import Structure from "../components/Structure";
import Script from "../components/Script";
import Export from "../components/Export";
import Recommendations from "../components/Recommendations";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Start",
    component: Start,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
  {
    path: "/settings",
    name: "Settings",
    component: Settings,
  },
  {
    path: "/structure",
    name: "Structure",
    component: Structure,
  },
  {
    path: "/script",
    name: "Script",
    component: Script,
  },
  {
    path: "/export",
    name: "Export",
    component: Export,
  },
  {
    path: "/recommendations",
    name: "Recommendations",
    component: Recommendations,
  },
  {
    path: "/about",
    name: "About",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ "../views/About.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
