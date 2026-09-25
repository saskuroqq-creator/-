from pathlib import Path

root = Path("buildsrc/Anima_Survivors_Reborn_v0.8.1_ANDROID_READY")
proj = root / "project.godot"
p = proj.read_text()

# Preserve the existing landscape/renderer fixes.
repls = {
    "window/size/viewport_width=1280": "window/size/viewport_width=960",
    "window/size/viewport_height=720": "window/size/viewport_height=540",
    "window/handheld/orientation=1": "window/handheld/orientation=0",
    'renderer/rendering_method="forward_plus"': 'renderer/rendering_method="gl_compatibility"',
    'renderer/rendering_method.mobile="mobile"': 'renderer/rendering_method.mobile="gl_compatibility"',
    'config/features=PackedStringArray("4.7", "Forward Plus")': 'config/features=PackedStringArray("4.7", "GL Compatibility")',
}
for a,b in repls.items():
    p=p.replace(a,b)

if "window/handheld/orientation=" not in p:
    p=p.replace('window/stretch/aspect="keep"','window/stretch/aspect="keep"
window/handheld/orientation=0')

# Galaxy A57 landscape profile.
p=p.replace("window/size/viewport_width=960","window/size/viewport_width=1170")
p=p.replace("window/size/viewport_height=540","window/size/viewport_height=540")
p=p.replace("window/size/window_width_override=1280","window/size/window_width_override=1560")
p=p.replace("window/size/window_height_override=720","window/size/window_height_override=720")
p=p.replace('config/name="Anima Survivors: Reborn — Asset Fusion"','config/name="Anima Survivors: Reborn — Galaxy A57"')
p=p.replace('config/name="Anima Survivors: Reborn — Top Down"','config/name="Anima Survivors: Reborn — Galaxy A57"')

lines=p.splitlines()
for i,line in enumerate(lines):
    if line.startswith("config/features="):
        lines[i]='config/features=PackedStringArray("4.7", "GL Compatibility")'
    elif line.startswith("window/size/viewport_width="):
        lines[i]="window/size/viewport_width=1170"
    elif line.startswith("window/size/viewport_height="):
        lines[i]="window/size/viewport_height=540"
    elif line.startswith("window/size/window_width_override="):
        lines[i]="window/size/window_width_override=1560"
    elif line.startswith("window/size/window_height_override="):
        lines[i]="window/size/window_height_override=720"
    elif line.startswith("window/handheld/orientation="):
        lines[i]="window/handheld/orientation=0"
    elif line.startswith("renderer/rendering_method="):
        lines[i]='renderer/rendering_method="gl_compatibility"'
    elif line.startswith("renderer/rendering_method.mobile="):
        lines[i]='renderer/rendering_method.mobile="gl_compatibility"'
p="\n".join(lines)+"\n"
proj.write_text(p)

# Main scene: first frame must be 2D-only.
main=root/"scripts/main.gd"
s=main.read_text()
s=s.replace('''func _ready()->void:
    process_mode=Node.PROCESS_MODE_ALWAYS
    AnimaAudio.play_music()
    rng.randomize()
    _build_background_world()
    _build_ui()
    _show_main_menu()
''','''func _ready()->void:
    process_mode=Node.PROCESS_MODE_ALWAYS
    rng.randomize()
    # Android-safe bootstrap: construct only 2D UI during the first frame.
    _build_ui()
    _show_main_menu()
''')
s=s.replace("REBORN · PIXEL EDITION · SURVIVAL ACTION","REBORN · TOP-DOWN SURVIVAL ACTION")
s=s.replace('    _install_pixel_filter()\n','')
if "_build_background_world()" in s and "Android-safe bootstrap" in s:
    s=s.replace("    _build_background_world()\n","")
main.write_text(s)

# Keep the existing top-down camera fix.
player=root/"scripts/player.gd"
s=player.read_text()
old='''    camera=Camera3D.new(); camera.name="CombatCamera"; get_tree().current_scene.add_child(camera)
    camera.global_position=global_position+Vector3(0,11.7,11.7); camera.rotation_degrees=Vector3(-43,0,0); camera.fov=51.5; camera.current=true'''
new='''    camera=Camera3D.new(); camera.name="CombatCamera"; get_tree().current_scene.add_child(camera)
    camera.projection=Camera3D.PROJECTION_ORTHOGONAL
    camera.size=11.5
    camera.global_position=global_position+Vector3(0,18.0,0)
    camera.rotation_degrees=Vector3(-90,0,0)
    camera.current=true'''
s=s.replace(old,new)
if "func _update_camera(delta: float) -> void:" in s:
    start=s.index("func _update_camera(delta: float) -> void:")
    end=s.index("\nfunc take_hit",start)
    s=s[:start]+'''func _update_camera(delta: float) -> void:
    if not is_instance_valid(camera):
        return
    camera_shake=max(0.0,camera_shake-delta*2.35)
    var desired_pos:=global_position+Vector3(0,18.0,0)
    camera_velocity+=(desired_pos-camera.global_position)*14.0*delta
    camera_velocity*=exp(-9.0*delta)
    camera.global_position+=camera_velocity*delta
    camera.projection=Camera3D.PROJECTION_ORTHOGONAL
    camera.size=lerp(camera.size,11.5,1.0-exp(-6.0*delta))
    camera.rotation_degrees=Vector3(-90,0,0)
    if camera_shake>0.0:
        camera.global_position+=Vector3(randf_range(-1,1),0,randf_range(-1,1))*camera_shake
'''+s[end:]
player.write_text(s)

# Reduce Android visual load.
world=root/"scripts/world_builder.gd"
w=world.read_text()
w=w.replace('var count:=360 if OS.get_name()!="Android" else 170','var count:=220 if OS.get_name()!="Android" else 90')
w=w.replace('motes.amount=90','motes.amount=40')
w=w.replace('weather.amount=54 if map_id!="desert" else 34','weather.amount=26 if map_id!="desert" else 18')
w=w.replace('for i in range(96):','for i in range(56):')
world.write_text(w)

(root/"shaders/pixel_post.gdshader").write_text('''shader_type canvas_item;
// Compatibility placeholder. The Android build does not install this post-process.
void fragment(){ COLOR=texture(TEXTURE,UV); }
''')

(root/"QA_REPORT_GRAYSCREEN_HARDENED_v1.4.txt").write_text("""ANIMA SURVIVORS: REBORN — GRAY-SCREEN HARDENED v1.4
====================================================
- First frame is 2D-only; 3D world creation is not performed during boot.
- Android uses Godot GL Compatibility rendering.
- Landscape logical canvas is 1170x540 for the target wide display.
- Perspective camera/FOV dependency is removed from combat.
- Pixel post-process remains disabled.
- Android environment density remains reduced.

Purpose: add a second defensive layer against renderer/framebuffer startup failures that
previously manifested as a gray screen.

Runtime verification still requires installation on an Android device.
""")
