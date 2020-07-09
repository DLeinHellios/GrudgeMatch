#!/usr/bin/env python3
# gm.py - GrudgeMatch: record-keeping for fighting game rivalries
# Just a demonstration GUI, nothing works yet

# Copyright 2020 DLeinHellios
# Logo by ZN
# Provided under the Apache License 2.0


import tkinter as tk
import sys, datetime, os, json
from src import *


def main():
    data = Data()
    window = Window(data)
    window.root.mainloop()


if __name__ == "__main__":
    main()
