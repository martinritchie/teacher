<component>
Name: {{ component.name }}
{% if component.purpose %}Purpose: {{ component.purpose }}
{% endif %}{% if component.inputs %}Inputs: {{ component.inputs }}
{% endif %}Steps:
{% for s in component.steps %}{{ loop.index }}. {{ s }}
{% endfor %}{% if component.outputs %}Outputs: {{ component.outputs }}
{% endif %}</component>
