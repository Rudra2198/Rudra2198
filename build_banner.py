import json, os, random
random.seed(2198)

# stats come from the environment when CI supplies them, else these fallbacks
REPOS = os.environ.get("STAT_REPOS", "33")
STARS = os.environ.get("STAT_STARS", "30")
YEARS = os.environ.get("STAT_YEARS", "5")

F = json.load(open("fontdata.json"))
ORB, RAJ = F["b64"]["orbitron.woff2"], F["b64"]["rajdhani.woff2"]

BYTES = ['1C', '55', 'BD', 'E9', '7A', 'FF', 'A3', '0D', 'C4', '2F', '9B', 'E1']
noise = []

# breach-protocol hex matrix, right side, behind the type
for r in range(8):
    for c in range(13):
        x, y = 668 + c * 37, 100 + r * 22
        op = round(random.uniform(0.10, 0.30), 2)
        fill = '#fcee0a' if random.random() < 0.13 else '#2f6f9e'
        noise.append(f'<text class="d" x="{x}" y="{y}" font-size="12" fill="{fill}" '
                     f'opacity="{op}" letter-spacing="1.8">{random.choice(BYTES)}</text>')

# drifting binary column, right edge
for i in range(11):
    bits = ' '.join(''.join(random.choice('01') for _ in range(4)) for _ in range(2))
    noise.append(f'<text class="d" x="1186" y="{96 + i * 21}" font-size="10" fill="#2f6f9e" '
                 f'text-anchor="end" letter-spacing="1.4" '
                 f'opacity="{round(random.uniform(0.14, 0.34), 2)}">{bits}</text>')

# corrupted data blocks
for _ in range(7):
    x, y = random.randint(640, 1130), random.randint(92, 268)
    c = random.choice(['#fcee0a', '#00f0ff', '#ff003c'])
    noise.append(f'<rect x="{x}" y="{y}" width="{random.choice([14, 22, 30])}" '
                 f'height="{random.choice([3, 5])}" fill="{c}" '
                 f'opacity="{round(random.uniform(0.12, 0.3), 2)}"/>')

NOISE = '\n      '.join(noise)

# 12 RAM units, top right. 8 committed, 4 free.
ram = []
for i in range(12):
    x = 916 + i * 20
    body = f'M {x + 4},22 L {x + 15},22 L {x + 15},48 L {x},48 L {x},26 Z'
    if i < 8:
        pulse = ''
        if i in (6, 7):
            begin = '0s' if i == 6 else '0.45s'
            pulse = (f'<animate attributeName="opacity" values="1;0.18;0.18;1;1" '
                     f'dur="2.6s" begin="{begin}" repeatCount="indefinite"/>')
        ram.append(f'<path d="{body}" fill="#00f0ff">{pulse}</path>')
    else:
        ram.append(f'<path d="{body}" fill="#0a1730" stroke="#1b4f7a" stroke-width="1.5"/>')
RAM = '\n      '.join(ram)

# typing clip: real Rajdhani advances, offset by the 30px prompt gutter
steps = ';'.join(['0', '30'] + [str(round(30 + a, 1)) for a in F["steps"]])
full_w = round(30 + F["steps"][-1], 1)
cursor_x = round(102 + F["steps"][-1], 1)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1200 340" width="1200" height="340" role="img" aria-label="man rudra">
  <defs>
    <style>
      @font-face {{ font-family: "Orb"; font-weight: 800;
        src: url(data:font/woff2;base64,{ORB}) format("woff2"); }}
      @font-face {{ font-family: "Raj"; font-weight: 600;
        src: url(data:font/woff2;base64,{RAJ}) format("woff2"); }}
      text {{ font-family: "Orb", "Arial Narrow", sans-serif; font-weight: 800; }}
      text.d {{ font-family: "Raj", "Arial Narrow", sans-serif; font-weight: 600; }}
    </style>
    <clipPath id="frame">
      <path d="M 30,0 L 1200,0 L 1200,310 L 1170,340 L 0,340 L 0,30 Z"/>
    </clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="0.6" y2="1">
      <stop offset="0%" stop-color="#0a1730"/>
      <stop offset="55%" stop-color="#060d1c"/>
      <stop offset="100%" stop-color="#040812"/>
    </linearGradient>
    <radialGradient id="haze" cx="22%" cy="62%" r="55%">
      <stop offset="0%" stop-color="#1b4f7a" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="#1b4f7a" stop-opacity="0"/>
    </radialGradient>
    <pattern id="scan" width="3" height="3" patternUnits="userSpaceOnUse">
      <rect width="3" height="1" fill="#000" opacity="0.30"/>
    </pattern>
    <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fcee0a" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#fcee0a" stop-opacity="0"/>
    </linearGradient>
    <filter id="hot" x="-25%" y="-50%" width="150%" height="200%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="type">
      <rect x="72" y="126" width="{full_w}" height="42">
        <animate attributeName="width" values="{steps}" dur="1s" calcMode="discrete" fill="freeze"/>
      </rect>
    </clipPath>
    <clipPath id="tearA">
      <rect x="-190" y="0" width="190" height="340">
        <animate attributeName="x" from="-190" to="1200" dur="3.4s" repeatCount="indefinite"/>
      </rect>
    </clipPath>
    <clipPath id="tearB">
      <rect x="-70" y="0" width="70" height="340">
        <animate attributeName="x" from="-70" to="1200" dur="2.3s" repeatCount="indefinite"/>
      </rect>
    </clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="1200" height="340" fill="url(#bg)"/>
    <rect width="1200" height="340" fill="url(#haze)"/>

    <g id="content">
      {NOISE}

      <path d="M 42,20 L 270,20 L 258,52 L 42,52 Z" fill="#fcee0a"/>
      <text x="58" y="41" font-size="15" fill="#050505" letter-spacing="1.6">SYS://RUDRA2198</text>
      <text class="d" x="296" y="41" font-size="13" fill="#2f6f9e" opacity="0.6" letter-spacing="2">0x{random.randint(4096, 65535):04X}</text>
      <text class="d" x="392" y="41" font-size="13" fill="#2f6f9e" opacity="0.6" letter-spacing="2">MEM {random.randint(60, 94)}%</text>

      <text x="846" y="41" font-size="13" fill="#00f0ff" opacity="0.8" letter-spacing="1.4">RAM</text>
      {RAM}

      <rect x="42" y="66" width="1116" height="2" fill="url(#fade)"/>
      <g stroke="#fcee0a" stroke-width="2" fill="none" opacity="0.8">
        <path d="M 42,320 L 20,320 L 20,298"/>
      </g>

      <g clip-path="url(#type)" font-size="26">
        <text class="d" x="72" y="156" fill="#00f0ff">&gt;</text>
        <text class="d" x="102" y="156" fill="#fcee0a" filter="url(#hot)">man rudra</text>
      </g>
      <rect x="{cursor_x}" y="135" width="12" height="25" fill="#fcee0a">
        <animate attributeName="x" values="102;{cursor_x}" dur="1s" calcMode="discrete" keyTimes="0;0.99" fill="freeze"/>
        <animate attributeName="opacity" values="1;1;0;0" dur="0.9s" repeatCount="indefinite"/>
      </rect>
      <text class="d" x="102" y="186" font-size="13" fill="#fcee0a" opacity="0.4" letter-spacing="2.6">[ {REPOS} REPO / {YEARS} YR / {STARS} STAR ]</text>

      <g opacity="1" font-size="58" letter-spacing="3">
        <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.85;1" dur="1.3s" fill="freeze"/>
        <text x="67" y="248" fill="#00f0ff" opacity="0.85">RUDRA PATEL
          <animate attributeName="x" values="70;70;62;77;64;67" keyTimes="0;0.66;0.73;0.81;0.9;1" dur="1.65s" calcMode="discrete" fill="freeze"/>
        </text>
        <text x="73" y="248" fill="#ff003c" opacity="0.85">RUDRA PATEL
          <animate attributeName="x" values="70;70;78;63;76;73" keyTimes="0;0.66;0.73;0.81;0.9;1" dur="1.65s" calcMode="discrete" fill="freeze"/>
        </text>
        <text x="70" y="248" fill="#fcee0a" filter="url(#hot)">RUDRA PATEL</text>
      </g>

      <g opacity="1">
        <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.9;1" dur="1.75s" fill="freeze"/>
        <rect x="70" y="272" width="3" height="20" fill="#ff003c"/>
        <text class="d" x="86" y="288" font-size="18" fill="#b8c4d4" letter-spacing="0.4">games, mobile apps, data pipelines. generalist on purpose.</text>
      </g>

      <g opacity="1">
        <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.91;1" dur="1.9s" fill="freeze"/>
        <g fill="#fcee0a">
          <rect x="900" y="272" width="26" height="6"/><rect x="932" y="272" width="26" height="6"/>
          <rect x="964" y="272" width="26" height="6"/><rect x="996" y="272" width="26" height="6"/>
        </g>
        <g fill="#fcee0a" opacity="0.22">
          <rect x="1028" y="272" width="26" height="6"/><rect x="1060" y="272" width="26" height="6"/>
          <rect x="1092" y="272" width="26" height="6"/>
        </g>
      </g>

      <g font-size="12" fill="#2f6f9e" letter-spacing="3.2">
        <text class="d" x="48" y="320" opacity="0.5">41.8349 N   87.6270 W</text>
        <text class="d" x="372" y="320" opacity="0.34">BUF   {random.randint(100, 999)} / 1024</text>
        <text class="d" x="672" y="320" opacity="0.34">SEQ   {random.randint(1, 9):02d} / 12</text>
        <text class="d" x="1158" y="320" opacity="0.5" text-anchor="end">TRACE   {random.randint(10, 99)} ms</text>
      </g>
    </g>

    <g clip-path="url(#tearA)">
      <rect width="1200" height="340" fill="url(#bg)"/>
      <rect width="1200" height="340" fill="url(#haze)"/>
      <use href="#content" xlink:href="#content" transform="translate(9,-3)"/>
      <rect width="1200" height="340" fill="#00f0ff" opacity="0.035"/>
    </g>
    <g clip-path="url(#tearB)">
      <rect width="1200" height="340" fill="url(#bg)"/>
      <rect width="1200" height="340" fill="url(#haze)"/>
      <use href="#content" xlink:href="#content" transform="translate(-7,2)"/>
      <rect width="1200" height="340" fill="#ff003c" opacity="0.03"/>
    </g>

    <rect x="-4" y="0" width="2" height="340" fill="#00f0ff" opacity="0.55">
      <animate attributeName="x" from="0" to="1390" dur="3.4s" repeatCount="indefinite"/>
    </rect>
    <rect x="-4" y="0" width="2" height="340" fill="#ff003c" opacity="0.4">
      <animate attributeName="x" from="0" to="1270" dur="2.3s" repeatCount="indefinite"/>
    </rect>

    <rect width="1200" height="340" fill="url(#scan)"/>
  </g>
  <path d="M 30,0 L 1200,0 L 1200,310 L 1170,340 L 0,340 L 0,30 Z" fill="none" stroke="#fcee0a" stroke-width="2" opacity="0.55"/>
</svg>
'''

open("assets/banner.svg", "w").write(svg)
print("written", len(svg), "bytes")
