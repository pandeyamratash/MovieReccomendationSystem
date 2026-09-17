import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Depth — Movie Recommender", layout="wide", page_icon="🌀")

# Hide Streamlit's default chrome so the embedded page reads as the whole app
st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 100% !important; }
    header { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

DEPTH_HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Depth — A 3D Film Carousel</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root{
    --bg: #EDEFF5;
    --surface: #FFFFFF;
    --ink: #14172B;
    --ink-soft: #5A5F78;
    --glow1: #1E9AA8;
    --glow2: #6A5ACD;
    --glow3: #B23A85;
    --line: #D7DAE6;
    --shadow: rgba(20,23,43,0.18);
    font-family: 'Inter', Arial, sans-serif;
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --bg: #0D0F1A;
      --surface: #171A30;
      --ink: #EDEFF5;
      --ink-soft: #9BA0BC;
      --glow1: #4DF0FF;
      --glow2: #9D8CFF;
      --glow3: #FF6FD8;
      --line: #262A44;
      --shadow: rgba(0,0,0,0.6);
    }
  }
  :root[data-theme="dark"]{
    --bg: #0D0F1A;
    --surface: #171A30;
    --ink: #EDEFF5;
    --ink-soft: #9BA0BC;
    --glow1: #4DF0FF;
    --glow2: #9D8CFF;
    --glow3: #FF6FD8;
    --line: #262A44;
    --shadow: rgba(0,0,0,0.6);
  }
  *{ box-sizing:border-box; }
  body{
    margin:0;
    background: var(--bg);
    color: var(--ink);
    overflow-x: hidden;
  }
  .wrap{ max-width: 1200px; margin:0 auto; padding: 44px 24px 90px; }

  header{ text-align:center; margin-bottom: 10px; perspective: 800px; }
  header h1{
    font-family:'Sora', sans-serif;
    font-weight: 800;
    font-size: clamp(2.6rem, 6vw, 4rem);
    margin: 0;
    display:inline-block;
    background: linear-gradient(100deg, var(--glow1), var(--glow2), var(--glow3));
    -webkit-background-clip: text; background-clip:text; color: transparent;
    transform: rotateX(8deg);
    transform-style: preserve-3d;
  }
  header p{ color: var(--ink-soft); margin: 10px 0 34px; font-size: 1.02rem; }

  .toolbar{
    display:flex; gap: 14px; justify-content:center; margin-bottom: 8px; flex-wrap:wrap;
  }
  input[type=text]{
    font-family:'Inter',sans-serif; font-size:1rem; padding: 11px 18px;
    border-radius: 12px; border: 1.5px solid var(--line); background: var(--surface);
    color: var(--ink); min-width: 240px;
  }
  input[type=text]:focus{ outline: 2px solid var(--glow2); }
  .chips{ display:flex; gap:10px; justify-content:center; flex-wrap:wrap; margin: 16px 0 36px; }
  .chip{
    padding: 8px 16px; border-radius: 999px; border: 1.5px solid var(--line);
    background: var(--surface); color: var(--ink-soft); font-size: 0.85rem; cursor:pointer;
    font-family:'Inter',sans-serif;
  }
  .chip.active{
    background: linear-gradient(100deg, var(--glow1), var(--glow2));
    color: #fff; border-color: transparent;
  }

  /* ---- 3D Coverflow Carousel ---- */
  .stage-label{
    text-align:center; font-family:'Sora',sans-serif; font-weight:700; font-size:1.3rem; margin-bottom: 6px;
  }
  .stage-hint{ text-align:center; color: var(--ink-soft); font-size: 0.85rem; margin-bottom: 20px; }
  .stage{
    perspective: 1300px;
    height: 320px;
    position: relative;
    display:flex;
    align-items:center;
    justify-content:center;
    margin-bottom: 20px;
  }
  .carousel{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
  }
  .card3d{
    position:absolute;
    top:50%; left:50%;
    width: 180px; height: 260px;
    margin: -130px 0 0 -90px;
    border-radius: 16px;
    cursor:pointer;
    transition: transform .5s cubic-bezier(.2,.8,.2,1), opacity .5s, filter .5s;
    display:flex; flex-direction:column; align-items:center; justify-content:flex-end;
    box-shadow: 0 20px 40px var(--shadow);
    border: 2px solid rgba(255,255,255,0.15);
    overflow:hidden;
  }
  .card3d .sheen{
    position:absolute; inset:0;
    background: linear-gradient(135deg, rgba(255,255,255,0.28), rgba(255,255,255,0) 55%);
    pointer-events:none;
  }
  .card3d .label{
    position:relative; z-index:2;
    width:100%;
    padding: 12px 10px 14px;
    background: rgba(10,10,20,0.42);
    color:#fff;
    font-family:'Sora',sans-serif;
    font-weight:700;
    font-size: 0.92rem;
    text-align:center;
    line-height:1.2;
  }
  .card3d .year{ font-family:'Inter',sans-serif; font-weight:400; font-size:0.72rem; opacity:0.8; margin-top:3px;}
  .card3d.liked{ box-shadow: 0 0 0 3px var(--glow3), 0 20px 40px var(--shadow); }
  .card3d.liked::after{
    content: "✓ Picked";
    position:absolute; top:8px; right:8px; z-index:3;
    background: var(--glow3); color:#fff; font-size: 0.62rem; font-weight:700;
    padding: 3px 8px; border-radius: 999px;
  }
  .nav-btn{
    background: var(--surface); border: 1.5px solid var(--line); color: var(--ink);
    width: 42px; height:42px; border-radius:50%; cursor:pointer; font-size:1.1rem;
    box-shadow: 0 4px 10px var(--shadow);
  }
  .nav-row{ display:flex; justify-content:center; gap: 20px; margin-bottom: 40px; }

  .liked-band{
    background: var(--surface); border: 1.5px solid var(--line); border-radius: 20px;
    padding: 14px 22px; display:flex; gap:10px; flex-wrap:wrap; align-items:center;
    margin: 0 auto 40px; max-width: 780px; box-shadow: 0 4px 14px var(--shadow);
  }
  .liked-empty{ color: var(--ink-soft); font-style:italic; font-size:0.9rem; }
  .liked-pill{
    background: linear-gradient(100deg, var(--glow2), var(--glow3)); color:#fff;
    padding: 6px 14px; border-radius:999px; font-size:0.82rem; display:flex; align-items:center; gap:8px;
  }
  .liked-pill button{ background:none;border:none;color:#fff;cursor:pointer;font-size:1rem;padding:0; }

  h2.section-title{
    font-family:'Sora',sans-serif; font-weight:700; font-size: 1.5rem; text-align:center; margin: 50px 0 26px;
  }

  .rec-grid{
    display:grid; grid-template-columns: repeat(auto-fill, minmax(230px,1fr)); gap: 24px;
    perspective: 1000px;
  }
  .tilt-card{
    background: var(--surface);
    border: 1.5px solid var(--line);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 10px 24px var(--shadow);
    transition: transform .12s ease-out, box-shadow .12s ease-out;
    will-change: transform;
  }
  .tilt-card .top{ display:flex; gap:12px; align-items:center; margin-bottom: 10px; }
  .tilt-badge{
    width: 48px; height:48px; border-radius: 12px; flex-shrink:0;
    display:flex; align-items:center; justify-content:center; color:#fff; font-weight:700;
    font-family:'Sora',sans-serif;
  }
  .tilt-card .title{ font-family:'Sora',sans-serif; font-weight:700; font-size:1.02rem; }
  .tilt-card .meta{ font-size:0.76rem; color:var(--ink-soft); }
  .tilt-card .why{ font-size:0.8rem; color: var(--glow3); margin: 8px 0 6px; font-weight:600; }
  .tilt-card .blurb{ font-size: 0.84rem; color: var(--ink-soft); line-height:1.4; }

  .empty-state{
    text-align:center; padding: 34px; color: var(--ink-soft); font-style:italic;
    border: 1.5px dashed var(--line); border-radius: 20px; max-width: 640px; margin: 0 auto;
  }

  footer{ text-align:center; margin-top: 60px; color: var(--ink-soft); font-size: 0.82rem; }
  footer button{
    margin-top: 12px; background: var(--surface); border: 1.5px solid var(--line);
    border-radius: 999px; padding: 8px 18px; color: var(--ink); cursor:pointer;
    font-family:'Inter',sans-serif; font-size: 0.8rem;
  }

  @media (max-width: 560px){
    .stage{ height: 280px; }
    .card3d{ width: 150px; height: 220px; margin: -110px 0 0 -75px; }
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>Depth</h1>
    <p>Turn the reel to find what you like, then watch the picks come forward.</p>
  </header>

  <div class="toolbar">
    <input type="text" id="search" placeholder="Search title or director…">
  </div>
  <div class="chips" id="genreChips"></div>

  <div class="stage-label">Turn the Reel</div>
  <div class="stage-hint">Click the front card to pick it. Use the arrows to bring another one forward.</div>
  <div class="stage">
    <div class="carousel" id="carousel"></div>
  </div>
  <div class="nav-row">
    <button class="nav-btn" id="prevBtn" aria-label="previous">‹</button>
    <button class="nav-btn" id="nextBtn" aria-label="next">›</button>
  </div>

  <div class="liked-band" id="likedStrip">
    <span class="liked-empty">Nothing picked yet — bring a card forward and click it.</span>
  </div>

  <h2 class="section-title">Recommended For You</h2>
  <div id="recommendations">
    <div class="empty-state">Pick a few films on the reel above. Depth blends shared genres with what other viewers picked up alongside them, then tilts the matches toward you.</div>
  </div>

  <footer>
    Depth — prototype recommender
    <br>
    <button id="themeToggle">Toggle light / dark</button>
  </footer>
</div>

<script>
const MOVIES = [
  {id:1, title:"Inception", year:2010, genres:["Sci-Fi","Thriller"], director:"Christopher Nolan", blurb:"A thief who steals secrets from the subconscious takes on one final, impossible job.", rating:8.8},
  {id:2, title:"The Matrix", year:1999, genres:["Sci-Fi","Action"], director:"Wachowski Sisters", blurb:"A hacker discovers the world he knows is a simulation built to keep humanity docile.", rating:8.7},
  {id:3, title:"Interstellar", year:2014, genres:["Sci-Fi","Drama"], director:"Christopher Nolan", blurb:"A team travels through a wormhole to find a new home for humanity.", rating:8.6},
  {id:4, title:"The Godfather", year:1972, genres:["Crime","Drama"], director:"Francis Ford Coppola", blurb:"The aging patriarch of a crime family transfers control to his reluctant son.", rating:9.2},
  {id:5, title:"Goodfellas", year:1990, genres:["Crime","Drama"], director:"Martin Scorsese", blurb:"A young man rises through the ranks of the mob, and watches it all unravel.", rating:8.7},
  {id:6, title:"Pulp Fiction", year:1994, genres:["Crime","Drama"], director:"Quentin Tarantino", blurb:"The lives of two hitmen, a boxer and a gangster's wife intertwine in four tales.", rating:8.9},
  {id:7, title:"The Dark Knight", year:2008, genres:["Action","Crime"], director:"Christopher Nolan", blurb:"Batman faces his greatest psychological and physical test against the Joker.", rating:9.0},
  {id:8, title:"Mad Max: Fury Road", year:2015, genres:["Action","Sci-Fi"], director:"George Miller", blurb:"A woman rebels against a tyrannical ruler in a post-apocalyptic wasteland.", rating:8.1},
  {id:9, title:"La La Land", year:2016, genres:["Romance","Musical"], director:"Damien Chazelle", blurb:"A jazz musician and an actress fall in love while pursuing their dreams in LA.", rating:8.0},
  {id:10, title:"Eternal Sunshine of the Spotless Mind", year:2004, genres:["Romance","Sci-Fi"], director:"Michel Gondry", blurb:"A couple erases each other from their memories, only to fall in love again.", rating:8.3},
  {id:11, title:"Amelie", year:2001, genres:["Romance","Comedy"], director:"Jean-Pierre Jeunet", blurb:"A shy Parisian waitress decides to improve the lives of those around her.", rating:8.3},
  {id:12, title:"Superbad", year:2007, genres:["Comedy"], director:"Greg Mottola", blurb:"Two best friends try to buy alcohol for a party on their last day of high school.", rating:7.6},
  {id:13, title:"Bridesmaids", year:2011, genres:["Comedy"], director:"Paul Feig", blurb:"A maid of honor's life unravels as she competes to plan the perfect wedding.", rating:6.8},
  {id:14, title:"The Grand Budapest Hotel", year:2014, genres:["Comedy","Drama"], director:"Wes Anderson", blurb:"A legendary concierge and his protégé get caught up in a jewel theft and murder.", rating:8.1},
  {id:15, title:"Get Out", year:2017, genres:["Horror","Thriller"], director:"Jordan Peele", blurb:"A young man uncovers a disturbing secret when he visits his girlfriend's family.", rating:7.7},
  {id:16, title:"Hereditary", year:2018, genres:["Horror"], director:"Ari Aster", blurb:"A family is haunted by a sinister presence after the death of their grandmother.", rating:7.3},
  {id:17, title:"A Quiet Place", year:2018, genres:["Horror","Thriller"], director:"John Krasinski", blurb:"A family must live in silence to avoid drawing creatures that hunt by sound.", rating:7.5},
  {id:18, title:"Spirited Away", year:2001, genres:["Animation","Fantasy"], director:"Hayao Miyazaki", blurb:"A girl wanders into a spirit world and must find a way to free her parents.", rating:8.6},
  {id:19, title:"Coco", year:2017, genres:["Animation","Family"], director:"Lee Unkrich", blurb:"A boy journeys through the Land of the Dead to uncover his family's history.", rating:8.4},
  {id:20, title:"Spider-Man: Into the Spider-Verse", year:2018, genres:["Animation","Action"], director:"Bob Persichetti", blurb:"A teenager becomes Spider-Man and meets others who share the mantle.", rating:8.4},
  {id:21, title:"Parasite", year:2019, genres:["Thriller","Drama"], director:"Bong Joon-ho", blurb:"A poor family schemes to infiltrate the household of a wealthy family.", rating:8.5},
  {id:22, title:"Se7en", year:1995, genres:["Thriller","Crime"], director:"David Fincher", blurb:"Two detectives hunt a serial killer who uses the seven deadly sins as motives.", rating:8.6},
  {id:23, title:"Whiplash", year:2014, genres:["Drama","Music"], director:"Damien Chazelle", blurb:"A young drummer is pushed to his limits by an abusive, perfectionist instructor.", rating:8.5},
  {id:24, title:"The Shawshank Redemption", year:1994, genres:["Drama"], director:"Frank Darabont", blurb:"Two imprisoned men bond over years, finding redemption through small acts of decency.", rating:9.3}
];

const CO_OCCURRENCE = {
  1:[2,3], 2:[1,7], 3:[1,24], 4:[5,6,24], 5:[4,6,24], 6:[4,5,22],
  7:[8,22], 8:[7,2], 9:[10,11], 10:[9,11], 11:[9,14],
  12:[13], 13:[12], 14:[11,23], 15:[16,21], 16:[15,17], 17:[16,15],
  18:[19,20], 19:[18,20], 20:[18,19], 21:[22,23,15], 22:[7,21,6],
  23:[14,21], 24:[4,5,3]
};

const HUES = {};
MOVIES.forEach((m,i) => HUES[m.id] = (i*47) % 360);
function cardStyle(id){
  const h = HUES[id];
  return `background: linear-gradient(150deg, hsl(${h} 55% 42%), hsl(${(h+50)%360} 50% 26%));`;
}

let liked = new Set();
let activeGenre = null;
let searchTerm = "";
let filteredMovies = MOVIES.slice();
let centerIndex = 0;

function allGenres(){
  const s = new Set();
  MOVIES.forEach(m => m.genres.forEach(g => s.add(g)));
  return [...s].sort();
}

function renderChips(){
  const el = document.getElementById('genreChips');
  el.innerHTML = "";
  allGenres().forEach(g => {
    const chip = document.createElement('button');
    chip.className = 'chip' + (activeGenre===g ? ' active' : '');
    chip.textContent = g;
    chip.onclick = () => { activeGenre = activeGenre===g ? null : g; centerIndex = 0; updateFilter(); renderCarousel(); };
    el.appendChild(chip);
  });
}

function updateFilter(){
  filteredMovies = MOVIES.filter(m => {
    const mg = !activeGenre || m.genres.includes(activeGenre);
    const ms = !searchTerm || (m.title+m.director).toLowerCase().includes(searchTerm.toLowerCase());
    return mg && ms;
  });
  if (centerIndex >= filteredMovies.length) centerIndex = 0;
}

function initials(title){
  return title.split(' ').filter(w => /[A-Za-z]/.test(w[0])).slice(0,2).map(w=>w[0].toUpperCase()).join('');
}

function renderCarousel(){
  const el = document.getElementById('carousel');
  el.innerHTML = "";
  if (filteredMovies.length === 0){
    el.innerHTML = `<div style="text-align:center;color:var(--ink-soft);width:100%;">No films match.</div>`;
    return;
  }
  filteredMovies.forEach((m, i) => {
    const offset = i - centerIndex;
    const abs = Math.abs(offset);
    if (abs > 3) return; // don't render far-off cards, keeps it light
    const card = document.createElement('div');
    card.className = 'card3d' + (liked.has(m.id) ? ' liked' : '');
    card.style.transform = `translateX(${offset*150}px) translateZ(${-abs*140}px) rotateY(${offset*-28}deg)`;
    card.style.opacity = abs > 3 ? 0 : (1 - abs*0.22);
    card.style.zIndex = 100 - abs;
    card.style.background = m.rating ? '' : '';
    card.innerHTML = `
      <div class="sheen"></div>
      <div style="position:absolute;inset:0;${cardStyle(m.id)}"></div>
      <div style="position:relative;z-index:1;color:#fff;font-family:'Sora',sans-serif;font-weight:800;font-size:2.2rem;flex:1;display:flex;align-items:center;justify-content:center;">${initials(m.title)}</div>
      <div class="label">${m.title}<div class="year">${m.year} · ★ ${m.rating}</div></div>
    `;
    card.onclick = () => {
      if (offset === 0){ toggleLike(m.id); }
      else { centerIndex = i; renderCarousel(); }
    };
    el.appendChild(card);
  });
}

function toggleLike(id){
  if (liked.has(id)) liked.delete(id);
  else { if (liked.size >= 6) liked.delete([...liked][0]); liked.add(id); }
  saveLiked();
  renderCarousel();
  renderLikedStrip();
  renderRecommendations();
}

function renderLikedStrip(){
  const strip = document.getElementById('likedStrip');
  if (liked.size === 0){
    strip.innerHTML = `<span class="liked-empty">Nothing picked yet — bring a card forward and click it.</span>`;
    return;
  }
  strip.innerHTML = [...liked].map(id => {
    const m = MOVIES.find(x=>x.id===id);
    return `<span class="liked-pill">${m.title} <button onclick="toggleLike(${id})">×</button></span>`;
  }).join('');
}

function renderRecommendations(){
  const el = document.getElementById('recommendations');
  if (liked.size === 0){
    el.innerHTML = `<div class="empty-state">Pick a few films on the reel above. Depth blends shared genres with what other viewers picked up alongside them, then tilts the matches toward you.</div>`;
    return;
  }
  const likedArr = [...liked];
  const likedMovies = MOVIES.filter(m => likedArr.includes(m.id));
  const genreCounts = {};
  likedMovies.forEach(m => m.genres.forEach(g => genreCounts[g] = (genreCounts[g]||0)+1));

  const scored = MOVIES.filter(m => !liked.has(m.id)).map(m => {
    const overlap = m.genres.filter(g => genreCounts[g]);
    const contentScore = overlap.reduce((s,g)=> s+genreCounts[g], 0);
    let collabScore = 0;
    const collabFrom = [];
    likedMovies.forEach(lm => {
      if ((CO_OCCURRENCE[lm.id]||[]).includes(m.id)){ collabScore += 3; collabFrom.push(lm.title); }
    });
    return { m, total: contentScore*2 + collabScore, overlap, collabFrom };
  }).filter(s => s.total > 0).sort((a,b)=>b.total-a.total).slice(0,8);

  if (scored.length === 0){
    el.innerHTML = `<div class="empty-state">No strong matches yet — try picking one more film in a different genre.</div>`;
    return;
  }

  el.innerHTML = `<div class="rec-grid">` + scored.map(s => {
    let why = [];
    if (s.overlap.length) why.push(`Shares ${s.overlap.join(', ')}`);
    if (s.collabFrom.length) why.push(`Often picked with ${s.collabFrom.join(', ')}`);
    return `
      <div class="tilt-card">
        <div class="top">
          <div class="tilt-badge" style="${cardStyle(s.m.id)}">${initials(s.m.title)}</div>
          <div>
            <div class="title">${s.m.title}</div>
            <div class="meta">${s.m.year} · ${s.m.director} · ★ ${s.m.rating}</div>
          </div>
        </div>
        <div class="why">${why.join(' — ')}</div>
        <div class="blurb">${s.m.blurb}</div>
      </div>`;
  }).join('') + `</div>`;

  attachTilt();
}

function attachTilt(){
  document.querySelectorAll('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      card.style.transform = `perspective(700px) rotateX(${-y*10}deg) rotateY(${x*10}deg) translateZ(6px)`;
      card.style.boxShadow = `${-x*20}px ${10 - y*10}px 30px var(--shadow)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'perspective(700px) rotateX(0) rotateY(0) translateZ(0)';
      card.style.boxShadow = '0 10px 24px var(--shadow)';
    });
  });
}

document.getElementById('prevBtn').addEventListener('click', () => {
  centerIndex = Math.max(0, centerIndex - 1);
  renderCarousel();
});
document.getElementById('nextBtn').addEventListener('click', () => {
  centerIndex = Math.min(filteredMovies.length - 1, centerIndex + 1);
  renderCarousel();
});
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft'){ centerIndex = Math.max(0, centerIndex - 1); renderCarousel(); }
  if (e.key === 'ArrowRight'){ centerIndex = Math.min(filteredMovies.length - 1, centerIndex + 1); renderCarousel(); }
});

function saveLiked(){ try{ localStorage.setItem('depth-liked', JSON.stringify([...liked])); }catch(e){} }
function loadLiked(){ try{ const raw = localStorage.getItem('depth-liked'); if(raw) liked = new Set(JSON.parse(raw)); }catch(e){} }

document.getElementById('search').addEventListener('input', e => { searchTerm = e.target.value; centerIndex = 0; updateFilter(); renderCarousel(); });
document.getElementById('themeToggle').addEventListener('click', () => {
  const root = document.documentElement;
  const cur = root.getAttribute('data-theme');
  if (cur === 'dark') root.setAttribute('data-theme','light');
  else if (cur === 'light') root.removeAttribute('data-theme');
  else root.setAttribute('data-theme','dark');
});

loadLiked();
renderChips();
updateFilter();
renderCarousel();
renderLikedStrip();
renderRecommendations();
</script>
</body>
</html>
'''

components.html(DEPTH_HTML, height=1900, scrolling=True)