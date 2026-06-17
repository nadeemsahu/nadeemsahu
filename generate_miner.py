import urllib.request
import re

def build_miner_svg():
    url = "https://ghchart.rshah.org/40c463/nadeemsahu"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            svg_data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching SVG: {e}")
        return
        
    w_m = re.search(r'width="(\d+)"', svg_data)
    h_m = re.search(r'height="(\d+)"', svg_data)
    orig_w = int(w_m.group(1)) if w_m else 663
    orig_h = int(h_m.group(1)) if h_m else 104
    
    new_w = orig_w + 40
    new_h = orig_h + 80
    
    active_blocks = []
    
    color_map = {
        '#c6e48b': '#0e4429',
        '#7bc96f': '#006d32',
        '#239a3b': '#26a641',
        '#196127': '#39d353'
    }
    
    # We will modify the rects to add IDs and change colors
    def replace_rect(match):
        rect_str = match.group(0)
        x_m = re.search(r'x="(\d+)"', rect_str)
        y_m = re.search(r'y="(\d+)"', rect_str)
        fill_m = re.search(r'fill:#([a-fA-F0-9]+)', rect_str)
        
        if x_m and y_m and fill_m:
            x, y = int(x_m.group(1)), int(y_m.group(1))
            fill_hex = '#' + fill_m.group(1).lower()
            
            # Change colors to dark mode equivalents
            if fill_hex.upper() == '#EEEEEE':
                rect_str = rect_str.replace('fill:#EEEEEE', 'fill:#161B22')
            else:
                new_color = color_map.get(fill_hex, '#39d353') # default to brightest if not found
                rect_str = rect_str.replace(f'fill:{fill_hex}', f'fill:{new_color}')
                rect_str = rect_str.replace(f'fill:{fill_hex.upper()}', f'fill:{new_color}')
                # Add ID for CSS targeting
                rect_str = rect_str.replace('<rect ', f'<rect id="block-{x}-{y}" ')
                active_blocks.append((x, y, new_color))
        return rect_str

    svg_data = re.sub(r'<rect([^>]+)>', replace_rect, svg_data)
    
    if not active_blocks:
        active_blocks = [(10, 10, '#39d353')]
        
    active_blocks.sort(key=lambda b: (b[0], b[1]))
    
    time_per_block = 0.6
    keyframes = ""
    block_animations = ""
    total_points = len(active_blocks)
    anim_duration = max(time_per_block, total_points * time_per_block)
    
    for i, (x, y, color) in enumerate(active_blocks):
        start_percent = (i / total_points) * 100
        end_percent = ((i + 1) / total_points) * 100 - 0.001
        keyframes += f"            {start_percent:.3f}%, {end_percent:.3f}% {{ transform: translate({x-4}px, {y-14}px); }}\n"
        
        disappear_percent = ((i + 0.5) / total_points) * 100
        
        block_animations += f"""
        @keyframes mine_block_{x}_{y} {{
            0% {{ fill: {color}; }}
            {max(0, disappear_percent - 0.1):.3f}% {{ fill: {color}; }}
            {disappear_percent:.3f}% {{ fill: #161B22; }}
            100% {{ fill: #161B22; }}
        }}
        #block-{x}-{y} {{
            animation: mine_block_{x}_{y} {anim_duration}s linear infinite;
        }}
        """
        
    style = f"""
    <style>
        @keyframes walkPath {{
{keyframes}
        }}
        .miner-char {{
            animation: walkPath {anim_duration}s linear infinite;
            font-size: 18px;
            text-shadow: 0 0 5px rgba(0,255,0,0.5);
        }}
        @keyframes swingAxe {{
            0%, 100% {{ transform: rotate(0deg); }}
            35% {{ transform: rotate(45deg); }}
            48% {{ transform: rotate(50deg); }}
            50% {{ transform: rotate(-50deg); }}
            53% {{ transform: rotate(-35deg); }}
            75% {{ transform: rotate(0deg); }}
        }}
        .axe {{
            animation: swingAxe {time_per_block}s linear infinite;
            transform-origin: -7px 8px;
        }}
        @keyframes boinkFade {{
            0%, 49.9% {{ opacity: 0; transform: translateY(0) scale(0.5); }}
            50% {{ opacity: 1; transform: translateY(-2px) scale(1.4); }}
            55% {{ opacity: 1; transform: translateY(-8px) scale(1); }}
            75% {{ opacity: 0; transform: translateY(-20px) scale(0.8); }}
            100% {{ opacity: 0; transform: translateY(0) scale(0.5); }}
        }}
        .boink {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 11px;
            font-weight: 900;
            fill: #ffcc00;
            text-shadow: 0 0 2px #ff0000;
            opacity: 0;
            animation: boinkFade {time_per_block}s ease-out infinite;
            transform-origin: -5px -5px;
        }}
        .title-text {{
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 16px;
            font-weight: bold;
            fill: #7ee787;
        }}
        .bg-rect {{
            fill: #0d1117;
            rx: 10px;
        }}
        .grid-group {{
            transform: translate(20px, 40px);
        }}
{block_animations}
    </style>
    """
    
    miner_svg = f'''
        <g class="miner-char">
            <!-- Steve Back Arm & Leg -->
            <rect x="-13" y="14" width="4" height="6" fill="#242485"/>
            <rect x="-8" y="6" width="4" height="8" fill="#008080"/>
            
            <!-- Steve Body -->
            <rect x="-14" y="6" width="8" height="8" fill="#00a8a8"/>
            <rect x="-14" y="14" width="8" height="6" fill="#3d3dbd"/>
            
            <!-- Steve Head -->
            <rect x="-15" y="-2" width="10" height="10" fill="#dca982"/>
            <rect x="-15" y="-2" width="10" height="2" fill="#312219"/>
            <rect x="-15" y="0" width="3" height="3" fill="#312219"/>
            <rect x="-9" y="1" width="2" height="2" fill="#ffffff"/>
            <rect x="-8" y="1" width="1" height="2" fill="#463a89"/>
            <rect x="-9" y="5" width="4" height="1" fill="#9e6e58"/> <!-- Mouth -->

            <!-- Swinging Front Arm + Pickaxe -->
            <g class="axe">
                <!-- Steve Front Arm -->
                <rect x="-9" y="6" width="4" height="6" fill="#00a8a8"/>
                <rect x="-9" y="12" width="4" height="4" fill="#dca982"/>
                <!-- Pickaxe Emoji (Flipped to face right) -->
                <text x="9" y="18" font-size="16" transform="scale(-1, 1)">⛏️</text>
            </g>
            
            <g class="boink"><text x="5" y="-5">boink!</text></g>
        </g>
    '''
    
    inner_content = re.sub(r'<svg[^>]*>', '', svg_data)
    inner_content = inner_content.replace('</svg>', '')
    
    # CRITICAL FIX: Remove XML declaration and DOCTYPE from inner content
    inner_content = re.sub(r'<\?xml[^>]*\?>', '', inner_content)
    inner_content = re.sub(r'<!DOCTYPE[^>]*>', '', inner_content)
    
    inner_content = inner_content.replace('fill:#767676', 'fill:#8B949E')
    
    new_svg = f'''<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{new_w}" height="{new_h}" viewBox="0 0 {new_w} {new_h}">
    {style}
    <rect class="bg-rect" width="{new_w}" height="{new_h}" />
    
    <text class="title-text" x="20" y="25">🦊 Mined Commits In Real-Time</text>
    
    <rect fill="#3b2d20" x="0" y="{new_h - 15}" width="{new_w}" height="15" />
    <rect fill="#2a823b" x="0" y="{new_h - 20}" width="{new_w}" height="5" />
    
    <g class="grid-group">
        {inner_content}
        {miner_svg}
    </g>
</svg>'''

    with open('animated_miner.svg', 'w', encoding='utf-8') as f:
        f.write(new_svg)
        
    print("Successfully generated super awesome CSS-animated animated_miner.svg!")

if __name__ == "__main__":
    build_miner_svg()
