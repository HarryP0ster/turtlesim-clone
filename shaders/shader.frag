#version 420

layout(location=0) in vec2 UV;

layout(location=0) out vec4 color;

uniform vec3 color_mask;
uniform sampler2D turtle;

void main()
{
    color = texture(turtle, UV);
    color.rgb *= color_mask;
}
