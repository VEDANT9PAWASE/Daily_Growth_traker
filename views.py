from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import DailyReflectionForm, HabitForm, ProgressForm, SignUpForm
from .models import DailyReflection, Habit, Progress


def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully. Start building your discipline!')
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


class UserHabitQuerySetMixin:
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    form_class = HabitForm
    template_name = 'tracker/habit_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Habit added successfully.')
        return super().form_valid(form)


class HabitUpdateView(LoginRequiredMixin, UserHabitQuerySetMixin, UpdateView):
    model = Habit
    form_class = HabitForm
    template_name = 'tracker/habit_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Habit updated successfully.')
        return super().form_valid(form)


class HabitDeleteView(LoginRequiredMixin, UserHabitQuerySetMixin, DeleteView):
    model = Habit
    template_name = 'tracker/habit_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Habit deleted successfully.')
        return super().form_valid(form)


@login_required
def toggle_today(request, pk):
    if request.method != 'POST':
        return redirect('dashboard')

    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    progress, created = Progress.objects.get_or_create(
        habit=habit,
        date=timezone.localdate(),
        defaults={'done': True},
    )

    if not created:
        progress.done = not progress.done
        progress.save(update_fields=['done'])

    return redirect('dashboard')


@login_required
def progress_note(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    progress, _ = Progress.objects.get_or_create(habit=habit, date=timezone.localdate())

    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progress note saved.')
            return redirect('dashboard')
    else:
        form = ProgressForm(instance=progress)

    return render(request, 'tracker/progress_form.html', {'form': form, 'habit': habit})


@login_required
def reflection_today(request):
    today = timezone.localdate()
    reflection = DailyReflection.objects.filter(user=request.user, date=today).first()

    if request.method == 'POST':
        form = DailyReflectionForm(request.POST, instance=reflection)
        if form.is_valid():
            daily_reflection = form.save(commit=False)
            daily_reflection.user = request.user
            daily_reflection.date = today
            daily_reflection.save()
            messages.success(request, 'Daily reflection saved.')
        else:
            messages.error(request, 'Please fix the errors in your reflection form.')

    return redirect('dashboard')
