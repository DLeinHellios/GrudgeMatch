#!/usr/bin/env python3
# gm.py - GrudgeMatch: record-keeping for fighting game rivalries
# Just a demonstration GUI, nothing works yet

# Copyright 2020 Dylan Lein-Hellios
# Logo by ZN
# Provided under the Apache 2.0 license


import tkinter as tk
import sys, datetime, os, json
from src import *


def main():
    data = Data()
    window = Window(data)
    window.root.mainloop()


if __name__ == "__main__":
    main()
