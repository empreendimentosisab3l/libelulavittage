// Native WebGL prototype: displaced 3D tessellated surface, calculated normals,
// directional illumination and anisotropic highlights. No video or fake CSS 3D.
export function startSilk(host) {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 650px)').matches;
  if (reduce.matches || navigator.connection?.saveData || (navigator.deviceMemory && navigator.deviceMemory <= 4) || (navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4)) {host.dataset.motion='static-device-preference';return;}
  const canvas=host.querySelector('canvas');
  const gl=canvas.getContext('webgl',{alpha:false,antialias:false,depth:false,powerPreference:'low-power',preserveDrawingBuffer:false});
  if(!gl) {host.dataset.motion='static-no-webgl';return;}
  const vertex=`
    precision highp float;
    attribute vec2 position;
    uniform float time;
    uniform vec2 pointer;
    uniform float scroll;
    varying vec3 vNormal;
    varying vec3 vPosition;
    varying vec2 vUv;
    float height(vec2 p){
      float phase=p.x*8.0+p.y*3.0+scroll*.4;
      float folds=sin(phase+sin(p.y*3.0+time*.12)*1.7+time*.18)*.24;
      folds+=sin(p.x*15.0-p.y*4.0+time*.14)*.07;
      folds+=sin(p.y*6.0+p.x*2.0-time*.1)*.1;
      float distance=length(p-pointer);
      folds+=exp(-distance*2.5)*sin(distance*9.0-time*.5)*.065;
      return folds+scroll*.04;
    }
    void main(){
      vec2 p=position;
      float z=height(p);
      float e=.006;
      float dx=(height(p+vec2(e,0.))-height(p-vec2(e,0.)))/(e*2.);
      float dy=(height(p+vec2(0.,e))-height(p-vec2(0.,e)))/(e*2.);
      vNormal=normalize(vec3(-dx,-dy,1.0));
      vPosition=vec3(p,z); vUv=p;
      gl_Position=vec4(p.x,p.y,z*.1,1.0);
    }`;
  const fragment=`
    precision mediump float;
    varying vec3 vNormal;
    varying vec3 vPosition;
    varying vec2 vUv;
    uniform vec3 baseColor;
    void main(){
      vec3 n=normalize(vNormal);
      vec3 light=normalize(vec3(-.9,.7,1.5)-vPosition*.2);
      float diffuse=max(dot(n,light),0.0);
      vec3 halfDir=normalize(light+vec3(0.,0.,1.));
      float sheen=pow(max(dot(n,halfDir),0.0),28.0);
      float broad=pow(max(dot(n,halfDir),0.0),5.0);
      float weave=sin(vUv.y*1600.)*.008;
      vec3 color=baseColor*(.2+diffuse*.92)+vec3(.70,.39,.29)*sheen*.75+baseColor*broad*.5+weave;
      float edge=1.0-length(vUv)*.17;
      gl_FragColor=vec4(color*edge,1.);
    }`;
  function shader(type,source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)){gl.deleteShader(s);throw Error('Shader unavailable');}return s;}
  let vs,fs,program;
  try{vs=shader(gl.VERTEX_SHADER,vertex);fs=shader(gl.FRAGMENT_SHADER,fragment);program=gl.createProgram();gl.attachShader(program,vs);gl.attachShader(program,fs);gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error('Program unavailable');}catch{if(vs)gl.deleteShader(vs);if(fs)gl.deleteShader(fs);if(program)gl.deleteProgram(program);return;}
  gl.useProgram(program);
  const nx=mobile?64:100,ny=mobile?40:64,points=[],indices=[];
  for(let y=0;y<=ny;y++)for(let x=0;x<=nx;x++)points.push(x/nx*2-1,y/ny*2-1);
  for(let y=0;y<ny;y++)for(let x=0;x<nx;x++){let a=y*(nx+1)+x;indices.push(a,a+1,a+nx+1,a+1,a+nx+2,a+nx+1);}
  const vertices=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,vertices);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(points),gl.STATIC_DRAW);
  const pos=gl.getAttribLocation(program,'position');gl.enableVertexAttribArray(pos);gl.vertexAttribPointer(pos,2,gl.FLOAT,false,0,0);
  const indexBuffer=gl.createBuffer();gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,indexBuffer);gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,new Uint16Array(indices),gl.STATIC_DRAW);
  const uniforms=Object.fromEntries(['time','pointer','scroll','baseColor'].map(k=>[k,gl.getUniformLocation(program,k)]));
  gl.uniform3fv(uniforms.baseColor,host.dataset.color==='noir'?[.11,.09,.065]:[.39,.015,.052]);
  let raf=0,visible=true,frame=0,last=0,px=0,py=0,stopped=false,slowFrames=0;
  function resize(){const box=host.getBoundingClientRect();const dpr=Math.min(devicePixelRatio||1,mobile?1:1.5);canvas.width=Math.round(box.width*dpr);canvas.height=Math.round(box.height*dpr);gl.viewport(0,0,canvas.width,canvas.height);}
  function move(e){const box=host.getBoundingClientRect();px=(e.clientX-box.left)/box.width*2-1;py=1-(e.clientY-box.top)/box.height*2;}
  function draw(now){if(stopped||reduce.matches||document.hidden||!visible){raf=0;return;}raf=requestAnimationFrame(draw);if(now-last<(mobile?40:30))return;const elapsed=last?now-last:0;last=now;if(elapsed>100)slowFrames++;else slowFrames=Math.max(0,slowFrames-1);if(slowFrames>8){stop();return;}gl.uniform1f(uniforms.time,now*.001);gl.uniform2f(uniforms.pointer,px,py);gl.uniform1f(uniforms.scroll,Math.min(window.scrollY/innerHeight,2));gl.drawElements(gl.TRIANGLES,indices.length,gl.UNSIGNED_SHORT,0);if(frame++===0)host.classList.add('is-ready');}
  function resume(){if(!raf&&!stopped&&!reduce.matches&&!document.hidden&&visible){last=0;raf=requestAnimationFrame(draw);}}
  function motion(){if(reduce.matches)stop();}
  function stop(){if(stopped)return;stopped=true;cancelAnimationFrame(raf);host.classList.add('is-paused');host.classList.remove('is-ready');observer.disconnect();resizer.disconnect();document.removeEventListener('visibilitychange',resume);window.removeEventListener('pointermove',move);reduce.removeEventListener('change',motion);gl.deleteBuffer(vertices);gl.deleteBuffer(indexBuffer);gl.deleteProgram(program);gl.deleteShader(vs);gl.deleteShader(fs);}
  const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;resume();},{threshold:.01});observer.observe(host);
  const resizer=new ResizeObserver(resize);resizer.observe(host);
  document.addEventListener('visibilitychange',resume);window.addEventListener('pointermove',move,{passive:true});reduce.addEventListener('change',motion);
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();stop();});window.addEventListener('pagehide',stop,{once:true});resize();resume();
}
