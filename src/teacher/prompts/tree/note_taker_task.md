<title>
{{ title }}
</title>

<source>
{{ source }}
</source>
{% if problems %}
<draft>
{% for note in draft.notes %}- {{ note }}
{% endfor %}</draft>
{% endif %}{% include "_shared/problems.md" %}
{% if problems %}Revise the notes.{% else %}Take notes on this passage.{% endif %}
