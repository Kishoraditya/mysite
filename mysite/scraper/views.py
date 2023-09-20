from django.shortcuts import render
from .models import UrlInputPage

#def url_input_page(request):
#    if request.method == 'POST':
#        form = UrlInputPage.get_form_class()(request.POST)
#        if form.is_valid():
#            # Save the form data as a submission
#            submission = form.save(commit=False)
#            submission.page = UrlInputPage.objects.first()  # Assuming you want to associate the submission with the first UrlInputPage instance
#            submission.save()
#    else:
 #       form = UrlInputPage.get_form_class()()

#    return render(request, 'url_input_page.html', {'form': form})

#def url_input_page_landing(request):
    # You can retrieve data from the context in your template
#    return render(request, 'url_input_page_landing.html', context={})
