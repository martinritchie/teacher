<heard>
{{ heard }}
</heard>

{% include "_shared/outline.md" %}

<key_numbers>
{% for n in key_numbers %}- {{ n }}
{% endfor %}</key_numbers>

{% include "_shared/component.md" %}

<source>
{{ source }}
</source>

<previous>
{{ previous }}
</previous>
{% if problems %}
<draft>
{{ draft }}
</draft>
{% endif %}{% include "_shared/problems.md" %}
Write the part on "{{ component.name }}" in about {{ words }} words.
