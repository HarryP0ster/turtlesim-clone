#version 420

layout(location=0) out vec2 UV;

uniform mat4 transform;

vec2 vertices[4] = {
    vec2(-0.1, 0.07),
    vec2(0.1, 0.07),
    vec2(-0.1, -0.07),
    vec2(0.1, -0.07)
};

vec2 UVs[4] = {
    vec2(1.0, 0.0),
    vec2(1.0, 1.0),
    vec2(0.0, 0.0),
    vec2(0.0, 1.0)
};

uint indices[6] = {
    0, 1, 2,
    1, 2, 3
};

void main() 
{
    UV = UVs[indices[gl_VertexID]];
	gl_Position = transform * vec4(vertices[indices[gl_VertexID]], 0.0, 1.0);
}
