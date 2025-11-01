## Templates Reference

## Base Template (`app/templates/base.html`)

## Home Page (`app/templates/index.html`)

## Search Page (`app/templates/search/search.html`)

## Search Results (`app/templates/search/results.html`)

## Upload Page (`app/templates/search/upload.html`)

## RL Task Overview (`app/templates/rl_task/overview.html`)

## RL Task Submit (`app/templates/rl_task/submit.html`)

## RL Task Results (`app/templates/rl_task/results.html`)

## Testing Dashboard (`app/templates/testing/dashboard.html`)

## Admin Dashboard (`app/templates/admin/dashboard.html`)

## Admin Documents (`app/templates/admin/documents.html`)

## Document Detail (`app/templates/search/document_detail.html`)

### 404 Page (`app/templates/errors/404.html`)

### 500 Page (`app/templates/errors/500.html`)

## Template Macros (`app/templates/macros/forms.html`)

## Common Template Patterns

### Flash Messages Pattern
```jinja2
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        <div class="flash-messages">
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">
                    {{ message }}
                    <button class="alert-close" onclick="this.parentElement.remove()">×</button>
                </div>
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

### Pagination Pattern
```jinja2
{% if items.pages > 1 %}
    <div class="pagination">
        {% if items.has_prev %}
            <a href="{{ url_for(endpoint, page=items.prev_num) }}">Previous</a>
        {% endif %}
        <span>Page {{ items.page }} of {{ items.pages }}</span>
        {% if items.has_next %}
            <a href="{{ url_for(endpoint, page=items.next_num) }}">Next</a>
        {% endif %}
    </div>
{% endif %}
```

### Empty State Pattern
```jinja2
{% if items %}
    <!-- Display items -->
{% else %}
    <div class="empty-state">
        <div class="empty-icon">📭</div>
        <h2>No Items Found</h2>
        <p>Try a different search or upload some documents.</p>
    </div>
{% endif %}
```

### Loading State Pattern
```jinja2
<div id="content">
    <div class="loading-spinner" id="loading">
        <div class="spinner"></div>
        <p>Loading...</p>
    </div>
    <div id="results" style="display: none;">
        <!-- Results go here -->
    </div>
</div>
```

---

## Jinja2 Template Best Practices

1. **Use Template Inheritance**: All pages extend `base.html`
2. **Block Organization**: Define clear blocks (title, content, extra_css, extra_js)
3. **URL Generation**: Always use `url_for()` instead of hardcoded URLs
4. **Escaping**: Jinja2 auto-escapes HTML; use `| safe` filter only when necessary
5. **Filters**: Use built-in filters for formatting (date, number, string manipulation)
6. **Macros**: Create reusable components in separate macro files
7. **Comments**: Use `{# comment #}` for template comments
8. **Conditionals**: Keep template logic simple; move complex logic to routes
9. **Whitespace Control**: Use `{%-` and `-%}` to control whitespace
10. **Context Variables**: Pass all needed data from routes; avoid database queries in templates
```
