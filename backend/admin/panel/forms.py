from django import forms
from .models import QuizAnswer


class AnswerForm(forms.BaseInlineFormSet):
    class Meta:
        model = QuizAnswer

    def clean(self) -> None:
        count_correct = 0

        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                if form.cleaned_data.get("is_correct"):
                    count_correct += 1

        if count_correct == 0:
            raise forms.ValidationError("Хотя бы один ответ должен быть корректным.")
        return super().clean()
