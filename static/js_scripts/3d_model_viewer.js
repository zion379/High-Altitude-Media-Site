import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const canvas_scale_factor = 1.2

// Create scene, renderer, and camera
const scene = new THREE.Scene();
const canvas = document.querySelector('#Model-Viewer2');
const renderer = new THREE.WebGLRenderer({antialias: true, canvas});
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

renderer.setSize(window.innerWidth/canvas_scale_factor, window.innerHeight/canvas_scale_factor, true)

camera.position.z = 5;

let property_model = new THREE.Mesh();


// Load and add the GLB model

const loader = new GLTFLoader();
loader.load('static/3d_Models/skull.glb', function (gltf) {
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
const directionalLight = new THREE.DirectionalLight(0xffffff, 2);
directionalLight.position.set(1, 1, 1);
directionalLight.rotation.y = 180
scene.add(directionalLight);

// Create OrbitControls
const controls = new OrbitControls(camera, canvas);

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth/canvas_scale_factor, window.innerHeight/canvas_scale_factor);
}

window.addEventListener('resize', onWindowResize, false);

// Render the scene
function animate() {
  requestAnimationFrame(animate);
  //model_skull.rotation.y += 0.01;
  //model_skull.rotation.x += 0.01;
  controls.update();
  renderer.render(scene, camera);
}
animate();

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
document.getElementById("FrontView").addEventListener("click", FrontView)
document.getElementById("RearView").addEventListener("click", RearView)
document.getElementById("LeftView").addEventListener("click", LeftView)
document.getElementById("RightView").addEventListener("click", RightView)
document.getElementById("ResetView").addEventListener("click", ResetView)