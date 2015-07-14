from django.contrib import messages



class SuccessMessageMixin(object):

    success_message = ''

    def form_valid(self, form):
        response = super(SuccessMessageMixin, self).form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)

        if  form.has_changed() and success_message:
            messages.success(self.request, success_message)

        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data
