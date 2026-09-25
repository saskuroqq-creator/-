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
    'renderer/rendering_method="forward_plus"': 'renderer/rendering_method="gl_compatibility"',
    'renderer/rendering_method.mobile="mobile"': 'renderer/rendering_method.mobile="gl_compatibility"',
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
s = s.replace('''func _ready()->void:
    process_mode=Node.PROCESS_MODE_ALWAYS
    AnimaAudio.play_music()
    rng.randomize()
    _build_background_world()
    _build_ui()
    _show_main_menu()
''','''func _ready()->void:
    process_mode=Node.PROCESS_MODE_ALWAYS
    AnimaAudio.play_music()
    rng.randomize()
    # Build UI first so a world/render initialization issue never leaves a blank screen.
    _build_ui()
    _show_main_menu()
    call_deferred("_finish_boot")

func _finish_boot()->void:
    _build_background_world()
    _build_menu_showcase()
''')
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
end=s.index("\nfunc take_hit", start)
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


# Samsung Galaxy A57 5G target profile.
# Native landscape is 2340x1080 (19.5:9), so 1170x540 is an exact 2x logical canvas.
proj = root / "project.godot"
p = proj.read_text()
p = p.replace("window/size/viewport_width=960", "window/size/viewport_width=1170")
p = p.replace("window/size/viewport_height=540", "window/size/viewport_height=540")
p = p.replace("window/size/window_width_override=1280", "window/size/window_width_override=1560")
p = p.replace("window/size/window_height_override=720", "window/size/window_height_override=720")
p = p.replace('config/name="Anima Survivors: Reborn — Top Down"', 'config/name="Anima Survivors: Reborn — Galaxy A57"')
proj.write_text(p)

# Rebuild the main menu as a landscape two-column layout.
main = root / "scripts/main.gd"
s = main.read_text()
start = s.index("func _show_main_menu()->void:")
end = s.index("\nfunc _refresh_selection()->void:", start)
menu = '''func _show_main_menu()->void:
    running=false
    _build_menu_showcase()
    for c in ui.get_children():
        if c is MarginContainer:
            c.visible=false
    main_overlay=ColorRect.new(); main_overlay.color=Color(.015,.025,.045,.58); main_overlay.set_anchors_preset(Control.PRESET_FULL_RECT); ui.add_child(main_overlay)
    var center:=CenterContainer.new(); center.set_anchors_preset(Control.PRESET_FULL_RECT); center.offset_left=24; center.offset_right=-24; center.offset_top=18; center.offset_bottom=-18; main_overlay.add_child(center)
    var panel:=PanelContainer.new(); panel.add_theme_stylebox_override("panel",_panel()); panel.custom_minimum_size=Vector2(900,488); panel.size_flags_horizontal=Control.SIZE_SHRINK_CENTER; panel.size_flags_vertical=Control.SIZE_SHRINK_CENTER; center.add_child(panel)
    var columns:=HBoxContainer.new(); columns.add_theme_constant_override("separation",28); panel.add_child(columns)

    var left:=VBoxContainer.new(); left.custom_minimum_size=Vector2(430,0); left.add_theme_constant_override("separation",9); columns.add_child(left)
    var logo:=Label.new(); logo.text="ANIMA\nSURVIVORS"; logo.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; logo.add_theme_font_size_override("font_size",40); logo.modulate=Color(1,.55,.78); left.add_child(logo)
    var sub:=Label.new(); sub.text="REBORN · TOP-DOWN SURVIVAL"; sub.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; sub.modulate=Color(.55,.92,1); sub.add_theme_font_size_override("font_size",15); left.add_child(sub)
    left.add_child(HSeparator.new())
    selected_hero_label=Label.new(); selected_hero_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; selected_hero_label.add_theme_font_size_override("font_size",20); left.add_child(selected_hero_label)
    var hr:=HBoxContainer.new(); hr.alignment=BoxContainer.ALIGNMENT_CENTER; hr.add_theme_constant_override("separation",10); left.add_child(hr)
    var hp=_button("◀ ГЕРОЙ"); hp.custom_minimum_size=Vector2(190,46); hr.add_child(hp); hp.pressed.connect(func(): hero_index=(hero_index-1+hero_ids.size())%hero_ids.size(); _refresh_selection())
    var hn=_button("ГЕРОЙ ▶"); hn.custom_minimum_size=Vector2(190,46); hr.add_child(hn); hn.pressed.connect(func(): hero_index=(hero_index+1)%hero_ids.size(); _refresh_selection())
    selected_map_label=Label.new(); selected_map_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; selected_map_label.add_theme_font_size_override("font_size",19); left.add_child(selected_map_label)
    var mr:=HBoxContainer.new(); mr.alignment=BoxContainer.ALIGNMENT_CENTER; mr.add_theme_constant_override("separation",10); left.add_child(mr)
    var mp=_button("◀ КАРТА"); mp.custom_minimum_size=Vector2(190,46); mr.add_child(mp); mp.pressed.connect(func(): map_index=(map_index-1+map_ids.size())%map_ids.size(); _refresh_selection())
    var mn=_button("КАРТА ▶"); mn.custom_minimum_size=Vector2(190,46); mr.add_child(mn); mn.pressed.connect(func(): map_index=(map_index+1)%map_ids.size(); _refresh_selection())

    var right:=VBoxContainer.new(); right.custom_minimum_size=Vector2(390,0); right.add_theme_constant_override("separation",9); columns.add_child(right)
    var mode_title:=Label.new(); mode_title.text="РЕЖИМ И ЗАПУСК"; mode_title.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; mode_title.add_theme_font_size_override("font_size",20); mode_title.modulate=Color(.55,.92,1); right.add_child(mode_title)
    mode_label=Label.new(); mode_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; mode_label.add_theme_font_size_override("font_size",17); right.add_child(mode_label)
    var mode_btn=_button("СМЕНИТЬ РЕЖИМ"); mode_btn.custom_minimum_size=Vector2(360,44); right.add_child(mode_btn); mode_btn.pressed.connect(func(): game_mode="waves" if game_mode=="arcade" else "arcade"; _refresh_selection())
    meta_label=Label.new(); meta_label.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; meta_label.modulate=Color(1,.82,.35); right.add_child(meta_label)
    var shrine=_button("СВЯТИЛИЩЕ · УЛУЧШЕНИЯ"); shrine.custom_minimum_size=Vector2(360,44); right.add_child(shrine); shrine.pressed.connect(_show_meta)
    var start_btn:=_button("ВОЙТИ В РАЗЛОМ"); start_btn.custom_minimum_size=Vector2(360,56); start_btn.add_theme_font_size_override("font_size",20); right.add_child(start_btn); start_btn.pressed.connect(start_run)
    var hint:=Label.new(); hint.text="ANDROID · ЛЕВЫЙ СТИК · DASH · ANIMA\nLANDSCAPE · 2340×1080 · 120 Hz"; hint.horizontal_alignment=HORIZONTAL_ALIGNMENT_CENTER; hint.modulate=Color(.72,.78,.86); hint.add_theme_font_size_override("font_size",13); right.add_child(hint)
    _refresh_selection()
'''
s=s[:start]+menu+s[end:]
s=s.replace('panel.custom_minimum_size=Vector2(_ui_width(600,326),_ui_width(430,560))','panel.custom_minimum_size=Vector2(650,430)')
s=s.replace('b.custom_minimum_size=Vector2(_ui_width(520,300),72)','b.custom_minimum_size=Vector2(600,68)')
s=s.replace('hud.add_theme_constant_override("margin_top",18)','hud.add_theme_constant_override("margin_top",16)')
s=s.replace('hud.add_theme_constant_override("margin_left",24); hud.add_theme_constant_override("margin_right",24)','hud.add_theme_constant_override("margin_left",28); hud.add_theme_constant_override("margin_right",28)')
main.write_text(s)

mobile = root / "scripts/mobile_controls.gd"
m = mobile.read_text()
m = m.replace('radius := 58.0','radius := 66.0')
m = m.replace('center=Vector2(88,size.y-88)','center=Vector2(98,size.y-98)')
m = m.replace('dash_rect=Rect2(size.x-138,size.y-138,104,104)','dash_rect=Rect2(size.x-136,size.y-136,110,110)')
m = m.replace('skill_rect=Rect2(size.x-258,size.y-122,94,94)','skill_rect=Rect2(size.x-270,size.y-128,104,104)')
m = m.replace('pause_rect=Rect2(size.x-70,18,50,50)','pause_rect=Rect2(size.x-74,18,54,54)')
mobile.write_text(m)

(root/'QA_REPORT_GALAXY_A57_LANDSCAPE_v1.3.txt').write_text('''ANIMA SURVIVORS: REBORN — GALAXY A57 LANDSCAPE v1.3
========================================================
TARGET
- Samsung Galaxy A57 5G landscape.
- Native display: 2340x1080, 19.5:9, Super AMOLED+.
- Logical game canvas: 1170x540 (exact 2x scale to native resolution).

UI
- Main menu rebuilt as a two-column landscape layout.
- Menu panel, buttons, text and touch targets fit inside the 540 logical-pixel height.
- Secondary upgrade/level overlays use landscape-safe dimensions.
- HUD margins and mobile controls adjusted for the short/wide screen.

GRAPHICS
- Clean 3D rendering; old pixel post-process remains disabled.
- Orthographic top-down combat camera.
- Android particle/decoration density kept controlled for a cleaner battlefield.

DEVICE NOTE
- The A57 has a 1080x2340 portrait panel; landscape is 2340x1080.
- Exact device appearance can still vary slightly with system navigation/cutout settings.
''')
