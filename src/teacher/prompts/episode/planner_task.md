<heard>
{{ heard }}
</heard>

{% for note in notes %}<chunk number="{{ loop.index }}" heading="{{ headings[loop.index0] }}">
{{ note }}
</chunk>
{% endfor %}
Outline how the method works.
