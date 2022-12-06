import json
import time

from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from .models import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import UpdateView, DeleteView
from django import forms
import pygal
import random as rand
from datetime import datetime
import threading
import time


def database_read(id_odczytu):
    odczyt = Odczyty.objects.get(id=id_odczytu)
    return odczyt.czas.strftime("%H:%M:%S"), odczyt.temperatura, odczyt.prad, odczyt.napiecie


def ploter(title, wart_x, wart_y):
    line_chart = pygal.Line()
    line_chart.title = title
    line_chart.x_labels = wart_x
    line_chart.add(None, wart_y)
    char = line_chart.render_data_uri()
    return char


def nowy_odczyt(temp, amp, volt):
    new_reading = Odczyty(temperatura=temp, prad=amp, napiecie=volt)
    new_reading.save()


def index(request):
    liczba_odczytow = Odczyty.objects.all()
    odczyty_ids = Odczyty.objects.values_list('id', flat=True)
    odczyty_ids = list(odczyty_ids)
    print(liczba_odczytow)
    lod = liczba_odczytow.count()
    nowy_odczyt(rand.randint(1, 100), rand.randint(1, 100), rand.randint(1, 100))
    if request.method == "POST":
        Odczyty.objects.all().delete()
        return redirect("/")
    if lod > 2:
        time_table = []
        temp_table = []
        amp_table = []
        volt_table = []
        first = 1
        if lod > 10:
            first = lod - 10
        for x in range(first, lod + 1):
            tim, temp, amp, volt = database_read(odczyty_ids[x-1])
            time_table.append(tim)
            temp_table.append(temp)
            amp_table.append(amp)
            volt_table.append(volt)
        plot_temp = ploter("Temperatura", time_table, temp_table)
        plot_amp = ploter("Natężenie Prądu", time_table, amp_table)
        plot_volt = ploter("Napięcie", time_table, volt_table)
        return render(request, 'index.html', {"plot_temp": plot_temp,
                                              "plot_amp": plot_amp,
                                              "plot_volt": plot_volt, })
    return render(request, 'blank.html')
