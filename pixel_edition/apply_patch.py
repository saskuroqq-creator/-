from pathlib import Path

root = Path("buildsrc/Anima_Survivors_Reborn_v0.8.1_ANDROID_READY")

# Landscape 16:9, clean 3D presentation. No full-screen pixel/post quantization.
proj = root / "project.godot"
p = proj.read_text()
repls = {
    "window/size/viewport_width=1280": "window/size/viewport_width=960",
    "window/size/viewport_height=720": "window/size/viewport_height=540",
    "window/size/window_width_override=1280": "window/size/window_width_override=1280",
    "window/size/window_height_override=720": "window/size/window_height_override=720",
    "window/handheld/orientation=1": "window/handheld/orientation=0",
    "config/name=\"Anima Survivors: Reborn — Asset Fusion\"": "config/name=\"Anima Survivors: Reborn — Top Down\"",
    "textures/default_filters/use_nearest_mipmap_filter=true": "textures/default_filters/use_nearest_mipmap_filter=false",
    "textures/canvas_textures/default_texture_filter=0": "textures/canvas_textures/default_texture_filter=1",
}
for a,b in repls.items(): p=p.replace(a,b)
if "window/handheld/orientation=" not in p:
    p=p.replace('window/stretch/aspect="keep"','window/stretch/aspect="keep"\nwindow/handheld/orientation=0')
if 'config/icon="res://icon.svg"' not in p:
    p=p.replace('run/main_scene="res://scenes/main.tscn"','run/main_scene="res://scenes/main.tscn"\nconfig/icon="res://icon.svg"')
proj.write_text(p)

# Main UI: landscape-safe panels, remove muddy full-screen pixel filter.
main = root/"scripts/main.gd"
s = main.read_text()
s = s.replace("REBORN · PIXEL EDITION · SURVIVAL ACTION","REBORN · TOP-DOWN SURVIVAL ACTION")
s = s.replace('    _install_pixel_filter()\n','')
s = s.replace('panel.custom_minimum_size=Vector2(_ui_width(580,326),_ui_width(610,560))','panel.custom_minimum_size=Vector2(_ui_width(600,326),_ui_width(500,560))')
s = s.replace('panel.custom_minimum_size=Vector2(_ui_width(520,326),_ui_width(420,560))','panel.custom_minimum_size=Vector2(_ui_width(600,326),_ui_width(430,560))')
s = s.replace('''hint.text="WASD / СТРЕЛКИ — ДВИЖЕНИЕ · SPACE — РЫВОК · Q — ANIMA BURST\nANDROID: ВИРТУАЛЬНЫЕ СТИКИ И КНОПКИ"''','''hint.text="WASD / СТРЕЛКИ — ДВИЖЕНИЕ · SPACE — РЫВОК · Q — ANIMA BURST\nANDROID: ЛЕВЫЙ СТИК · DASH · ANIMA"''')
main.write_text(s)

# Combat camera: strict top-down orthographic view, tuned for landscape.
player = root/"scripts/player.gd"
s = player.read_text()
old='''    camera=Camera3D.new(); camera.name="CombatCamera"; get_tree().current_scene.add_child(camera)
    camera.global_position=global_position+Vector3(0,11.7,11.7); camera.rotation_degrees=Vector3(-43,0,0); camera.fov=51.5; camera.current=true'''
new='''    camera=Camera3D.new(); camera.name="CombatCamera"; get_tree().current_scene.add_child(camera)
    camera.projection=Camera3D.PROJECTION_ORTHOGONAL
    camera.size=11.5
    camera.global_position=global_position+Vector3(0,18.0,0)
    camera.rotation_degrees=Vector3(-90,0,0)
    camera.current=true'''
s=s.replace(old,new)
start=s.index("func _update_camera(delta: float) -> void:")
end=s.index("\nfunc try_dash()", start)
newfunc='''func _update_camera(delta: float) -> void:
    if not is_instance_valid(camera):
        return
    camera_shake = max(0.0,camera_shake-delta*2.35)
    var desired_pos := global_position + Vector3(0,18.0,0)
    camera_velocity += (desired_pos-camera.global_position) * 14.0 * delta
    camera_velocity *= exp(-9.0*delta)
    camera.global_position += camera_velocity * delta
    camera.projection=Camera3D.PROJECTION_ORTHOGONAL
    camera.size=lerp(camera.size,11.5,1.0-exp(-6.0*delta))
    camera.rotation_degrees=Vector3(-90,0,0)
    if camera_shake > 0.0:
        camera.global_position += Vector3(randf_range(-1,1),0,randf_range(-1,1))*camera_shake
'''
s=s[:start]+newfunc+s[end:]
player.write_text(s)

# Cleaner environment density on Android; retain depth without visual overload.
world = root/"scripts/world_builder.gd"
w = world.read_text()
w = w.replace('var count:=360 if OS.get_name()!="Android" else 170','var count:=220 if OS.get_name()!="Android" else 90')
w = w.replace('motes.amount=90','motes.amount=40')
w = w.replace('weather.amount=54 if map_id!="desert" else 34','weather.amount=26 if map_id!="desert" else 18')
w = w.replace('for i in range(96):','for i in range(56):')
world.write_text(w)

# Disable old pixel post-process shader completely; keep the file for compatibility.
(root/"shaders/pixel_post.gdshader").write_text('''shader_type canvas_item;
// Retained for backwards compatibility. Top Down build intentionally does not install this filter.
void fragment(){ COLOR = texture(TEXTURE, UV); }
''')

# Updated launcher icon.
(root/"icon.svg").write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" rx="96" fill="#07111f"/><circle cx="256" cy="250" r="154" fill="#102c45" stroke="#69e8ff" stroke-width="12"/><path d="M256 112l35 82 89 8-68 57 21 87-77-47-77 47 21-87-68-57 89-8z" fill="#ff5b9a"/><circle cx="256" cy="250" r="34" fill="#69e8ff"/><path d="M104 416h304" stroke="#69e8ff" stroke-width="18" stroke-linecap="round" opacity=".8"/></svg>''')

(root/"QA_REPORT_TOPDOWN_LANDSCAPE_v1.2.txt").write_text('''ANIMA SURVIVORS: REBORN — TOP-DOWN LANDSCAPE v1.2
================================================
CHANGES
- Android orientation locked to landscape.
- Logical viewport 960x540 with 1280x720 desktop override.
- Combat camera changed to orthographic, exact top-down (90 degrees).
- Camera follows player smoothly with no perspective tilt/FOV pumping.
- Full-screen pixel quantization/post-process removed: 3D colors and silhouettes stay clean.
- Texture filtering restored to linear for cleaner 3D presentation.
- Android grass/particles/weather density reduced to remove visual clutter.
- Mobile controls remain landscape-first and use left stick + right action buttons.
- Launcher icon updated.

NOTE
Runtime/device QA requires an exported APK on a real Android device.
''')
