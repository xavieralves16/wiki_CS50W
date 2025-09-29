from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    content = util.get_entry(title)
    
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The entry doesn't exist."
        })

    # Converter Markdown em HTML
    html_content = markdown2.markdown(content)

    # Renderizar a página com o conteúdo
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })