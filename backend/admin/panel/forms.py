from collections import Counter

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


class TagsForm(forms.BaseInlineFormSet):
    def clean(self) -> None:
        queryset = self.get_queryset()
        tags_id = [data.tag.id for data in queryset]

        result = Counter(tags_id)
        is_repeat = any(count > 1 for count in result.values())
        if is_repeat:
            raise forms.ValidationError("Теги не должны повторяться")
        return super().clean()
