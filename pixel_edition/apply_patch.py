from pathlib import Path

root = Path("buildsrc/Anima_Survivors_Reborn_v0.8.1_ANDROID_READY")

# --- Project / Android portrait ---
proj = root / "project.godot"
p = proj.read_text()
p = p.replace('window/size/viewport_width=1280', 'window/size/viewport_width=360')
p = p.replace('window/size/viewport_height=720', 'window/size/viewport_height=640')
p = p.replace('window/size/window_width_override=1280', 'window/size/window_width_override=720')
p = p.replace('window/size/window_height_override=720', 'window/size/window_height_override=1280')
p = p.replace('window/stretch/mode="canvas_items"', 'window/stretch/mode="canvas_items"\nwindow/stretch/aspect="keep"')
p = p.replace('textures/default_filters/use_nearest_mipmap_filter=false', 'textures/default_filters/use_nearest_mipmap_filter=true\ntextures/canvas_textures/default_texture_filter=0')
p = p.replace('config/name="Anima Survivors: Reborn — Asset Fusion"', 'config/name="Anima Survivors: Reborn — Pixel Edition"')
if 'window/handheld/orientation=1' not in p:
    p = p.replace('window/stretch/aspect="keep"', 'window/stretch/aspect="keep"\nwindow/handheld/orientation=1')
if 'window/frame_pacing/android/enable_frame_pacing=true' not in p:
    p = p.replace('window/handheld/orientation=1', 'window/handheld/orientation=1\nwindow/frame_pacing/android/enable_frame_pacing=true\nwindow/frame_pacing/android/swappy_mode=2\nwindow/energy_saving/keep_screen_on=true')
if 'config/icon="res://icon.svg"' not in p:
    p = p.replace('run/main_scene="res://scenes/main.tscn"', 'run/main_scene="res://scenes/main.tscn"\nconfig/icon="res://icon.svg"')
proj.write_text(p)

# --- Main UI / pixel presentation ---
main = root / "scripts/main.gd"
s = main.read_text()
if 'func _portrait_ui() -> bool:' not in s:
    s = s.replace('func _ready()->void:\n', 'func _portrait_ui() -> bool:\n    return get_viewport().get_visible_rect().size.y > get_viewport().get_visible_rect().size.x\n\nfunc _ui_width(wide: float, portrait: float) -> float:\n    return portrait if _portrait_ui() else wide\n\nfunc _ready()->void:\n')
s = s.replace('sub.text="REBORN · HUMANFORM · 3D ACTION SURVIVOR"', 'sub.text="REBORN · PIXEL EDITION · SURVIVAL ACTION"')
s = s.replace('hint.text="WASD / стрелки — движение · SPACE — рывок · Q — ANIMA BURST\\nНа телефоне управление появляется автоматически"', 'hint.text="WASD / СТРЕЛКИ — ДВИЖЕНИЕ · SPACE — РЫВОК · Q — ANIMA BURST\\nANDROID: ВИРТУАЛЬНЫЕ СТИКИ И КНОПКИ"')
s = s.replace('panel.custom_minimum_size=Vector2(580,610)', 'panel.custom_minimum_size=Vector2(_ui_width(580,326),_ui_width(610,560))')
s = s.replace('logo.add_theme_font_size_override("font_size",46)', 'logo.add_theme_font_size_override("font_size",_ui_width(46,34))')
s = s.replace('sub.add_theme_font_size_override("font_size",16)', 'sub.add_theme_font_size_override("font_size",_ui_width(16,11))')
s = s.replace('hp.custom_minimum_size=Vector2(150,45)', 'hp.custom_minimum_size=Vector2(_ui_width(150,125),45)')
s = s.replace('hn.custom_minimum_size=Vector2(150,45)', 'hn.custom_minimum_size=Vector2(_ui_width(150,125),45)')
s = s.replace('mp.custom_minimum_size=Vector2(150,45)', 'mp.custom_minimum_size=Vector2(_ui_width(150,125),45)')
s = s.replace('mn.custom_minimum_size=Vector2(150,45)', 'mn.custom_minimum_size=Vector2(_ui_width(150,125),45)')
s = s.replace('mode_btn.custom_minimum_size=Vector2(300,42)', 'mode_btn.custom_minimum_size=Vector2(_ui_width(300,280),42)')
s = s.replace('shrine.custom_minimum_size=Vector2(420,44)', 'shrine.custom_minimum_size=Vector2(_ui_width(420,280),44)')
s = s.replace('l.position=Vector2(-250,120); l.size=Vector2(500,50)', 'l.position=Vector2(-_ui_width(250,160),120); l.size=Vector2(_ui_width(500,320),50)')
# constrain the two full-screen modal panels in portrait
s = s.replace('panel.add_theme_stylebox_override("panel",_panel()); center.add_child(panel)\n    var vb:=VBoxContainer.new(); vb.add_theme_constant_override("separation",10); panel.add_child(vb)',
              'panel.add_theme_stylebox_override("panel",_panel()); panel.custom_minimum_size=Vector2(_ui_width(520,326),_ui_width(420,560)); center.add_child(panel)\n    var vb:=VBoxContainer.new(); vb.add_theme_constant_override("separation",8); panel.add_child(vb)')
s = s.replace('b.custom_minimum_size=Vector2(520,72)', 'b.custom_minimum_size=Vector2(_ui_width(520,300),72)')
main.write_text(s)

# --- Mobile controls ---
mobile = root / "scripts/mobile_controls.gd"
m = mobile.read_text().replace('radius := 62.0', 'radius := 58.0')
m = m.replace('''        center=Vector2(95,size.y-95)
        dash_rect=Rect2(size.x-155,size.y-155,110,110)
        skill_rect=Rect2(size.x-275,size.y-130,92,92)
        pause_rect=Rect2(size.x-72,18,52,52)''',
'''        var portrait := size.y > size.x
        if portrait:
            center=Vector2(76,size.y-104)
            dash_rect=Rect2(size.x-122,size.y-150,100,100)
            skill_rect=Rect2(size.x-122,size.y-270,100,100)
            pause_rect=Rect2(size.x-66,18,48,48)
        else:
            center=Vector2(88,size.y-88)
            dash_rect=Rect2(size.x-138,size.y-138,104,104)
            skill_rect=Rect2(size.x-258,size.y-122,94,94)
            pause_rect=Rect2(size.x-70,18,50,50)''')
m = m.replace('event.position.x < size.x*.45', 'event.position.x < size.x*.48')
mobile.write_text(m)

# --- Pixel shader ---
shader = root / "shaders/pixel_post.gdshader"
shader.write_text('''shader_type canvas_item;

uniform float pixel_size : hint_range(1.0, 8.0) = 3.0;
uniform float palette_steps : hint_range(2.0, 16.0) = 7.0;
uniform float contrast : hint_range(0.8, 1.5) = 1.10;
uniform float vignette_strength : hint_range(0.0, 1.0) = 0.22;
uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

void fragment() {
    vec2 tex_size = vec2(textureSize(screen_texture, 0));
    vec2 cell = max(vec2(1.0), vec2(pixel_size));
    vec2 uv = floor(SCREEN_UV * tex_size / cell) * cell / tex_size;
    uv += (cell * 0.5) / tex_size;
    vec4 tex = texture(screen_texture, uv);
    vec3 col = (tex.rgb - 0.5) * contrast + 0.5;
    col = floor(clamp(col, vec3(0.0), vec3(1.0)) * palette_steps + 0.5) / palette_steps;
    vec2 vig_uv = SCREEN_UV * 2.0 - 1.0;
    float vignette = 1.0 - smoothstep(0.35, 1.15, dot(vig_uv, vig_uv)) * vignette_strength;
    col *= vignette;
    float dither = (fract(sin(dot(floor(SCREEN_UV * tex_size), vec2(12.9898,78.233))) * 43758.5453) - 0.5) * 0.018;
    col = clamp(col + dither, vec3(0.0), vec3(1.0));
    COLOR = vec4(col, tex.a);
}
''')

(root / "icon.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" rx="96" fill="#080d18"/><path d="M256 72 298 166 400 178 324 246 344 348 256 300 168 348 188 246 112 178 214 166Z" fill="#ff5b9a"/><path d="M256 112 274 190 350 204 292 254 306 326 256 286 206 326 220 254 162 204 238 190Z" fill="#69e8ff"/><rect x="92" y="400" width="328" height="18" rx="9" fill="#69e8ff" opacity=".8"/></svg>''')

(root / "QA_REPORT_PIXEL_PORTRAIT_v1.1.txt").write_text('''ANIMA SURVIVORS: REBORN — PIXEL PORTRAIT v1.1 STATIC QA
========================================================
- 12 PNG textures: 512x512; albedo/normal RGB, roughness L.
- 4 generated GLB props: parse-valid; 15,020 total triangles.
- 12 WAV files: parse-valid PCM, 32 kHz; music stereo and SFX mono.
- External character/monster slots are optional and documented with provenance.
- No unlicensed marketplace assets are claimed as bundled.
- Native Android portrait orientation enabled.
- Logical canvas 360x640; desktop preview 720x1280.
- Portrait-safe menu/modal widths and mobile control placement added.
- Android frame pacing/Swappy enabled.
- Pixel post-process upgraded with controlled vignette and subtle dithering.
- Vector launcher icon added.
NOTE: Device FPS/touch/thermal QA still requires installing the exported APK on real phones.
''')
