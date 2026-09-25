shader_type canvas_item;

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