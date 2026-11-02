#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Finjustering: titlar under 60 tegn, meta-descriptions utan upprepning,
og 'sliping av parkett' tilbake i teksten.
"""
import io

F = "build_no.py"
s = io.open(F, encoding="utf-8").read()

def rep(old, new, label):
    global s
    assert s.count(old) == 1, "HITTADE %d av [%s]" % (s.count(old), label)
    s = s.replace(old, new, 1)
    print("  ok:", label)

# ---------------------------------------------- 1. TITLAR (under 60 tegn)
rep('"title": "Gulvsliping og gulvsliper i Halden og Østfold | CK Måleri & Golv"',
    '"title": "Gulvsliper i Halden og Østfold | CK Måleri & Golv"', "titel halden")
rep('"title": "Gulvsliping og gulvsliper i Sarpsborg og Østfold | CK Måleri & Golv"',
    '"title": "Gulvsliper i Sarpsborg og Østfold | CK Måleri & Golv"', "titel sarpsborg")
rep('"title": "Gulvsliping og gulvsliper i Fredrikstad og Østfold | CK Måleri & Golv"',
    '"title": "Gulvsliper i Fredrikstad og Østfold | CK Måleri & Golv"', "titel fredrikstad")

# ------------------------------- 2. META DESCRIPTIONS (ulikt titelstarten)
rep('''        "desc": ("Gulvsliper i Halden og Østfold. Vi sliper parkett, fiskebensparkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    '''        "desc": ("Vi er gulvslipere i Halden og Østfold. Sliper parkett, fiskebensparkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    "desc halden")
rep('''        "desc": ("Gulvsliper i Sarpsborg og Østfold. Vi sliper parkett, fiskebensparkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    '''        "desc": ("Vi er gulvslipere i Sarpsborg og Østfold. Sliper parkett, fiskebensparkett og "
                 "gamle tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    "desc sarpsborg")
rep('''        "desc": ("Gulvsliper i Fredrikstad, Hvaler og Østfold. Vi sliper parkett og gamle tregulv "
                 "— støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    '''        "desc": ("Vi er gulvslipere i Fredrikstad, Hvaler og Østfold. Sliper parkett og gamle "
                 "tregulv — støysvakt og nesten støvfritt. Gratis befaring og fastpris."),''',
    "desc fredrikstad")

# --------------------------------- 3. 'sliping av parkett' tilbake i teksten
rep('''      til en overflate som holder. Parkettsliping og sliping av plankegulv er det vi gjør mest, med egne
      Bona-maskiner, støysvakt og tilnærmet støvfritt. Skriftlig fastpris etter befaring i {city}.</p>''',
    '''      til en overflate som holder. Sliping av parkett og gamle plankegulv er det vi gjør mest, med egne
      Bona-maskiner, støysvakt og tilnærmet støvfritt. Skriftlig fastpris etter befaring i {city}.</p>''',
    "sliping av parkett tilbake")

io.open(F, "w", encoding="utf-8").write(s)
print("ok")
