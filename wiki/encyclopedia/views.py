from django.shortcuts import render, redirect
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

    # Convert markdown to HTML
    html_content = markdown2.markdown(content)

    # Render the entry page with HTML content
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html_content
    })

def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()

    for entry in entries:
        if entry.lower() == query.lower() and query:
            return redirect("entry", title=entry)

    matching_entries = [entry for entry in entries if query.lower() in entry.lower()] if query else []

    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": matching_entries
    })

def create_entry(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        content = request.POST.get("content", "").strip()

        if not title or not content:
            return render(request, "encyclopedia/create_entry.html", {
                "error": "Title and content cannot be empty. ",
            })
        
        if util.get_entry(title) is not None:
            return render (request, "encyclopedia/create_entry.html", {
                "error": "An entry with this title already exists."
            })
        
        util.save_entry(title, content)
        return redirect("entry", title=title)
    
    return render(request, "encyclopedia/create_entry.html")

