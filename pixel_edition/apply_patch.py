from pathlib import Path
root = Path("buildsrc/Anima_Survivors_Reborn_v0.8.1_ANDROID_READY")
main = root / "scripts/main.gd"
s = main.read_text()
s = s.replace('var menu_anim_time:=0.0\n', 'var menu_anim_time:=0.0\nvar pixel_layer:ColorRect\n')
s = s.replace(
'''    damage_overlay=ColorRect.new(); damage_overlay.color=Color(1,.02,.02,0); damage_overlay.mouse_filter=Control.MOUSE_FILTER_IGNORE; damage_overlay.set_anchors_preset(Control.PRESET_FULL_RECT); damage_overlay.process_mode=Node.PROCESS_MODE_ALWAYS; ui.add_child(damage_overlay)
''',
'''    damage_overlay=ColorRect.new(); damage_overlay.color=Color(1,.02,.02,0); damage_overlay.mouse_filter=Control.MOUSE_FILTER_IGNORE; damage_overlay.set_anchors_preset(Control.PRESET_FULL_RECT); damage_overlay.process_mode=Node.PROCESS_MODE_ALWAYS; ui.add_child(damage_overlay)
    _install_pixel_filter()
''')
s = s.replace(
'''func _panel()->StyleBoxFlat:
    var s:=StyleBoxFlat.new(); s.bg_color=Color(.035,.055,.08,.93); s.border_color=Color(.25,.75,.9,.45); s.set_border_width_all(1); s.set_corner_radius_all(18); s.shadow_color=Color(0,0,0,.5); s.shadow_size=18; return s

func _button(text:String)->Button:
    var b:=Button.new(); b.text=text; b.custom_minimum_size=Vector2(260,52); b.add_theme_font_size_override("font_size",17)
''',
'''func _install_pixel_filter()->void:
    pixel_layer=ColorRect.new()
    pixel_layer.name="PixelPostProcess"
    pixel_layer.set_anchors_preset(Control.PRESET_FULL_RECT)
    pixel_layer.mouse_filter=Control.MOUSE_FILTER_IGNORE
    pixel_layer.z_index=900
    var mat:=ShaderMaterial.new()
    mat.shader=load("res://shaders/pixel_post.gdshader")
    pixel_layer.material=mat
    ui.add_child(pixel_layer)

func _panel()->StyleBoxFlat:
    var s:=StyleBoxFlat.new(); s.bg_color=Color(0.035,0.04,0.065,0.97); s.border_color=Color(0.95,0.42,0.67,0.78); s.set_border_width_all(3); s.set_corner_radius_all(2); s.shadow_color=Color(0,0,0,.75); s.shadow_size=6; return s

func _button(text:String)->Button:
    var b:=Button.new(); b.text=text; b.custom_minimum_size=Vector2(260,52); b.add_theme_font_size_override("font_size",17)
    var normal:=StyleBoxFlat.new(); normal.bg_color=Color(0.06,0.075,0.12,0.98); normal.border_color=Color(0.32,0.72,0.86,0.85); normal.set_border_width_all(2); normal.set_corner_radius_all(1)
    var hover:=normal.duplicate(); hover.bg_color=Color(0.12,0.10,0.17,1.0); hover.border_color=Color(1.0,0.48,0.72,1.0)
    var pressed:=normal.duplicate(); pressed.bg_color=Color(0.18,0.12,0.20,1.0)
    b.add_theme_stylebox_override("normal",normal); b.add_theme_stylebox_override("hover",hover); b.add_theme_stylebox_override("pressed",pressed); b.add_theme_stylebox_override("focus",hover)
''')
s = s.replace('sub.text="REBORN · HUMANFORM · 3D ACTION SURVIVOR"', 'sub.text="REBORN · PIXEL EDITION · SURVIVAL ACTION"')
s = s.replace('hint.text="WASD / стрелки — движение · SPACE — рывок · Q — ANIMA BURST\\nНа телефоне управление появляется автоматически"', 'hint.text="WASD / СТРЕЛКИ — ДВИЖЕНИЕ · SPACE — РЫВОК · Q — ANIMA BURST\\nANDROID: ВИРТУАЛЬНЫЕ СТИКИ И КНОПКИ"')
main.write_text(s)

shader = root / "shaders/pixel_post.gdshader"
shader.write_text('''shader_type canvas_item;

uniform float pixel_size : hint_range(1.0, 8.0) = 3.0;
uniform float palette_steps : hint_range(2.0, 16.0) = 7.0;
uniform float contrast : hint_range(0.8, 1.5) = 1.08;
uniform sampler2D screen_texture : hint_screen_texture, repeat_disable, filter_nearest;

void fragment() {
    vec2 tex_size = vec2(textureSize(screen_texture, 0));
    vec2 cell = max(vec2(1.0), vec2(pixel_size));
    vec2 uv = floor(SCREEN_UV * tex_size / cell) * cell / tex_size;
    uv += (cell * 0.5) / tex_size;
    vec4 c = texture(screen_texture, uv);
    c.rgb = (c.rgb - 0.5) * contrast + 0.5;
    c.rgb = floor(c.rgb * palette_steps + 0.5) / palette_steps;
    COLOR = c;
}
''')

proj = root / "project.godot"
p = proj.read_text()
p = p.replace('window/size/viewport_width=1280', 'window/size/viewport_width=640')
p = p.replace('window/size/viewport_height=720', 'window/size/viewport_height=360')
p = p.replace('window/stretch/mode="canvas_items"', 'window/stretch/mode="canvas_items"\nwindow/stretch/aspect="keep"')
p = p.replace('textures/default_filters/use_nearest_mipmap_filter=false', 'textures/default_filters/use_nearest_mipmap_filter=true\ntextures/canvas_textures/default_texture_filter=0')
p = p.replace('config/name="Anima Survivors: Reborn — Asset Fusion"', 'config/name="Anima Survivors: Reborn — Pixel Edition"')
proj.write_text(p)

(root / "README_PIXEL_EDITION.md").write_text('''# Anima Survivors: Reborn — Pixel Edition

Pixel-art presentation pass based on the supplied v0.8.1 Android project.

- 640x360 logical viewport with nearest filtering.
- Full-screen pixel post-process with palette quantization.
- Hard-edged pixel-style menu panels and buttons.
- Existing survival gameplay, heroes, maps, progression and Android controls retained.

This build is a production-oriented presentation pass; store approval, commercial certification and device QA still require external testing and release signing.
''')
