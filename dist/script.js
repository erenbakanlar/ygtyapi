const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
function closeMenu() { toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Menüyü aç'); nav.classList.remove('open'); }
toggle.addEventListener('click', () => { const open = toggle.getAttribute('aria-expanded') !== 'true'; toggle.setAttribute('aria-expanded', String(open)); toggle.setAttribute('aria-label', open ? 'Menüyü kapat' : 'Menüyü aç'); nav.classList.toggle('open', open); });
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); toggle.focus(); } });
document.querySelector('#year').textContent = new Date().getFullYear();

// A perspective study traced to the room photograph; no video or animation library.
const hero = document.querySelector('.hero');
const heroPhoto = hero.querySelector('.hero-image');
const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const sketchPaths = [
  ['shell', 'M0 0H900L1158 94L1238 64L1305 92L1600 0 M1070 62V755 M1158 94V752 M1238 64V812 M1305 92V812 M1070 950L1920 1310 M0 1180L1070 950'],
  ['shell', 'M20 0V775L1055 750V0 M25 625L1055 647 M20 678L1055 700 M425 0V1015 M465 0V1010 M735 0V942 M775 0V927 M1000 0V817'],
  ['structure', 'M1305 204L1920 30 M1469 48V580 M1674 4V548 M1305 403L1674 340 M1674 548L1920 535 M1305 588L1708 583 M1305 800L1920 861'],
  ['structure', 'M1260 811L1868 870L1870 1004L1258 934Z M1260 811L1812 860L1868 870 M1260 859L1812 918L1812 988 M1284 890L1785 942 M1305 920L1785 968 M1280 938V982 M1830 1000V1043'],
  ['structure', 'M1345 596L1713 584L1710 836L1340 803Z M1360 609L1696 601L1693 819L1355 789Z M1355 805L1341 821 M1700 835L1718 855'],
  ['interior', 'M1014 759Q1130 748 1248 762L1261 950Q1130 984 958 958L967 905Z M966 904Q1100 893 1245 918L1250 962 M958 958L942 1103L956 1106L976 982 M1250 962L1248 1128L1234 1124L1235 982 M979 985L1218 1027 M1004 798L1145 813L1092 897L953 878Z'],
  ['interior', 'M0 796L55 780L239 981 M0 940Q150 965 360 1035 M0 989L574 1192L1151 1130L1200 1184L1205 1348 M0 1075L520 1310L555 1348 M38 1310L525 1306 M0 840L55 805L195 974 M51 802L279 842L278 961'],
  ['interior', 'M557 952C540 914 657 912 731 918C820 919 908 938 907 961C906 993 824 1007 727 1009C641 1008 565 992 557 952Z M557 952C575 986 842 1010 907 961 M572 976L571 1056 M688 1005L688 1172 M883 987L882 1147 M577 1070L881 1107'],
  ['detail', 'M338 1105L873 979L1920 1233 M515 1180L882 1049L1850 1338 M1435 1080L1578 1024 M1591 1140L1738 1080 M0 117L1005 265 M0 165L1005 312'],
  ['dimensions', 'M1094 110L1094 730 M1081 125L1108 99 M1081 743L1108 717 M1328 475L1876 451 M1340 460L1316 490 M1888 436L1864 466 M1328 462V493 M1876 435V469']
];
const layer = document.createElement('div');
layer.className = 'hero-blueprint';
layer.setAttribute('aria-hidden', 'true');
layer.innerHTML = `<svg viewBox="0 0 1920 1348" preserveAspectRatio="xMidYMid slice" fill="none" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="draft-grid" width="56" height="56" patternUnits="userSpaceOnUse"><path d="M56 0H0V56" stroke="currentColor" stroke-width=".55" opacity=".16"/></pattern></defs><rect width="1920" height="1348" fill="url(#draft-grid)"/>${sketchPaths.map(([kind,d],i)=>`<path class="draft-line ${kind}" d="${d}" pathLength="1" style="--line-delay:${i*160}ms"/>`).join('')}</svg>`;
hero.insertBefore(layer, hero.querySelector('.hero-shade'));
const control = document.createElement('button');
control.type = 'button';
control.className = 'hero-motion-control';
control.hidden = true;
hero.append(control);
let running = false;
function labelControl() {
  control.textContent = running ? 'Ⅱ  Animasyonu duraklat' : hero.classList.contains('draft-complete') ? '↻  Dönüşümü yeniden izle' : '▷  Animasyonu sürdür';
}
function finishDraft() {
  running = false;
  hero.classList.remove('draft-paused');
  hero.classList.add('draft-complete');
  labelControl();
}
function startDraft() {
  if (motionPreference.matches) return;
  hero.classList.remove('draft-active', 'draft-paused', 'draft-complete');
  void hero.offsetWidth;
  hero.classList.add('draft-active');
  running = true;
  control.hidden = false;
  labelControl();
}
control.addEventListener('click', () => {
  if (hero.classList.contains('draft-complete')) return startDraft();
  running = !running;
  hero.classList.toggle('draft-paused', !running);
  labelControl();
});
heroPhoto.addEventListener('animationend', event => { if (event.animationName === 'room-reveal') finishDraft(); });
motionPreference.addEventListener('change', () => {
  hero.classList.remove('draft-active', 'draft-paused', 'draft-complete');
  running = false;
  control.hidden = true;
});
if (heroPhoto.complete && heroPhoto.naturalWidth) startDraft();
else heroPhoto.addEventListener('load', startDraft, {once:true});
