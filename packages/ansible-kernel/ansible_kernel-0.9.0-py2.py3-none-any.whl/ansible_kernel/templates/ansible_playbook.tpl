{%- extends 'null.tpl' -%}

{%- block header -%}
---
{% endblock header %}

{% block input -%}
{% if cell.source.strip().startswith("#inventory")-%}
{% elif cell.source.strip().startswith("#ansible.cfg")-%}
{% elif cell.source.strip().startswith("#template")-%}
{% elif cell.source.strip().startswith("#vars")-%}
{% elif cell.source.strip().startswith("#host_vars")-%}
{% elif cell.source.strip().startswith("#group_vars")-%}
{% elif cell.source.strip().startswith("#play") %}
{% if cell.source.strip()[5:].strip() %}- {%endif%}{{cell.source.strip()[5:].strip() | indent(2) | trim}}
  tasks:
{% elif cell.source.strip().startswith("#task") %}
{% if cell.source.strip()[5:].strip() %}  - {%endif%}{{cell.source.strip()[5:].strip() | indent(4) | trim}}
{%else%}
{% if cell.source.strip() %}  - {%endif%}{{cell.source.strip() | indent(4) | trim}}
{%endif%}
{% endblock input %}

{% block markdowncell scoped %}
{{ cell.source | comment_lines }}
{% endblock markdowncell %}

{%- block footer -%}
...
{% endblock footer %}
