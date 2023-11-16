import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const canvas_scale_factor = 1.2

//Get Rendering Div Dimensions
var divElement;
var divWidth;
var divHeight;

function Get_div_dimensions() {
  divElement = document.getElementById('model-renderer-container');
  divWidth = divElement.offsetWidth;
  divHeight = divElement.offsetHeight;
}
Get_div_dimensions();


var scene;
var canvas;
var renderer;
var camera;


function Create_scene() {
  // Create scene, renderer, and camera
  scene = new THREE.Scene();
  canvas = document.querySelector('#Model-Viewer2');
  renderer = new THREE.WebGLRenderer({antialias: true, canvas});
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
}
Create_scene();

//Test Update canvas
export function updateCanvas() {
  console.log('Updating Canvas');
  canvas = document.querySelector('#Model-Viewer2');
  Get_div_dimensions();
  Create_scene();
  Init();
}

window.updateCanvas = updateCanvas;


//testing diffrent viewing option
//renderer.setSize(window.innerWidth/canvas_scale_factor, window.innerHeight/canvas_scale_factor, true)

var renderer_height_multiplier = 4
var property_model;
var script_tag;
var model_url;
var controls;

function Init() {
  renderer.setSize(divWidth, divHeight * renderer_height_multiplier);

  camera.position.z = 4;
  camera.position.y = 4;
  camera.position.x = 4;

  property_model = new THREE.Mesh();

  // get model url
  script_tag = document.querySelector('#model_3d_script');
  model_url = new String(script_tag.getAttribute("model_url"));
  console.log(model_url);

  // Load and add the GLB model
  const loader = new GLTFLoader();
  loader.load(model_url, function (gltf) {
      property_model = gltf.scene;
    scene.add(property_model);
  }, undefined, function (error) {
    console.error(error);
  });

  /*
  const loader = new GLTFLoader();
  loader.parse(test_var,'',function(gltf){
    property_model = gltf.scene;
    scene.add(property_model);
  }, undefined, function(error) {
    consle.error(error);
  });
  */

  // Add directional light
  const directionalLight = new THREE.DirectionalLight(0xffffff, 3);
  directionalLight.position.set(1, 1, 1);
  directionalLight.rotation.y = 180
  scene.add(directionalLight);

  // Create OrbitControls
  controls = new OrbitControls(camera, canvas);
  //controls.object.position = THREE.Vector3(2.83, 2.46, 3.30)
}

Init();

//load new model
export function load_new_model(url) {
  Get_div_dimensions();
  Create_scene();

  renderer.setSize(divWidth, divHeight * renderer_height_multiplier);

  camera.position.z = 4;
  camera.position.y = 4;
  camera.position.x = 4;

  property_model = new THREE.Mesh();

  // Load and add the GLB model
  const loader = new GLTFLoader();
  loader.load(url, function (gltf) {
      property_model = gltf.scene;
    scene.add(property_model);
  }, undefined, function (error) {
    console.error(error);
  });

  // Add directional light
  const directionalLight = new THREE.DirectionalLight(0xffffff, 3);
  directionalLight.position.set(1, 1, 1);
  directionalLight.rotation.y = 180
  scene.add(directionalLight);

  // Create OrbitControls
  controls = new OrbitControls(camera, canvas);
}

function onWindowResize() {
  //camera.aspect = window.innerWidth / window.innerHeight;
  camera.aspect = divWidth / (divHeight * renderer_height_multiplier);
  camera.updateProjectionMatrix();
  //renderer.setSize(window.innerWidth/canvas_scale_factor, window.innerHeight/canvas_scale_factor);
  renderer.setSize(divWidth, divHeight * renderer_height_multiplier);
}

window.addEventListener('resize', onWindowResize, false);

// Render the scene
function animate() {
  requestAnimationFrame(animate);
  //model_skull.rotation.y += 0.01;
  //model_skull.rotation.x += 0.01;
  controls.update();
  renderer.render(scene, camera);
  //printInfo();
}
animate();

// print Info
function printInfo() {
  console.log('OrbitControls Position:', controls.object.position);
  console.log('OrbitControls Rotation:', controls.object.rotation);
  
  // 3D model position and rotation
  console.log('Model Position:', property_model.position);
  console.log('Model Rotation:', property_model.rotation);
}

function rotate_Model(model, angle){
  var degrees = angle
  var radians = THREE.MathUtils.degToRad(degrees);
  model.rotation.y = radians
}

// View Controls
function FrontView() {
  console.log("Front View");
  rotate_Model(property_model, 0);
}

function RearView() {
  console.log("Rear View");
  rotate_Model(property_model, 180);
}

function LeftView() {
  console.log("Left View");
  rotate_Model(property_model, 90);
}

function RightView() {
  console.log("Right View");
  rotate_Model(property_model, -90);
}

function ResetView() {
  console.log("Reset View");
  rotate_Model(property_model, 0);
}

//link buttons
/*
document.getElementById("FrontView").addEventListener("click", FrontView)
document.getElementById("RearView").addEventListener("click", RearView)
document.getElementById("LeftView").addEventListener("click", LeftView)
document.getElementById("RightView").addEventListener("click", RightView)
document.getElementById("ResetView").addEventListener("click", ResetView)
*/