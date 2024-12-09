import sys
sys.path.append('MainProzori')
sys.path.append('Queries')
sys.path.append('Mics')

from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import os
import ctypes
import datetime
import random
import sqlite3
import re

# Project-specific imports
import helperFunctions
import widgets as wid
import queries
import winLogin
import winSignup
import winMain
