{% if problems %}
<problems>
{% for problem in problems %}- {{ problem }}
{% endfor %}</problems>

Your last version had these problems. Fix every one and keep the rest.
{% endif %}
