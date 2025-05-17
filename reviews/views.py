# reviews/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseBadRequest

from .models import Review
from .forms import ReviewForm

@login_required
def add_review(request, content_type_id, object_id):
    content_type = get_object_or_404(ContentType, id=content_type_id)
    obj = get_object_or_404(content_type.model_class(), pk=object_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.content_type = content_type
            review.object_id = object_id
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            # Redirect back to the object's detail page
            return redirect(obj.get_absolute_url())
        else:
            # If the form is not valid, re-render the template with the form and errors
            # This part might not be strictly necessary given the template structure,
            # but it's good practice for form handling.
            # For now, we'll just redirect back to the object's detail page
            # and rely on messages to show errors if needed.
            messages.error(request, 'There was an error with your review form.')
            return redirect(obj.get_absolute_url())

    # This view is primarily for POST requests from the form.
    # GET requests to this URL might indicate direct access or an issue,
    # so we can redirect or return a bad request response.
    # Given the template handles form display, redirecting might be simpler.
    # However, for robustness, returning HttpResponseBadRequest is also an option.
    # For now, let's assume GET requests shouldn't hit this view directly
    # and redirect to the object's detail page.
    return redirect(obj.get_absolute_url())
