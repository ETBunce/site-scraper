from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Link
from django.http import HttpResponseRedirect

# Create your views here.


def scrape(request):
    if request.method == "POST":
        try:
            site = request.POST.get("site", "")

            page = requests.get(site)
            soup = BeautifulSoup(page.text, "html.parser")

            for link in soup.find_all("a"):
                link_address = link.get("href")
                link_text = link.string
                Link.objects.create(name=link_text, address=link_address)

        except:
            print("invalid url")

        return HttpResponseRedirect("/")
    else:
        data = Link.objects.all()
        return render(request, "myapp/result.html", {"data": data})


def clear(request):
    Link.objects.all().delete()
    return HttpResponseRedirect("/")
