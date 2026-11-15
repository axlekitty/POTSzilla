"""
POTS dashboard (PotsZilla) - version 4.8.7   <- bump VERSION below and add a line here whenever the script changes

Changelog
  4.8.7  Calendar: the word for stability 1 is now "lowest" so it no longer wraps onto a second line in the day squares.
  4.8.6  The mascot dino is now the icon on the app's windows (instead of Tk's default feather).
  4.8.5  Period days in the Timeline events strip are a red circle instead of the blood-drop emoji (which did not show on some systems).
  4.8.4  Calendar days show a small word next to the stability number (lowest, low, mid, good, great); the key under the calendar is set off with a divider line.
  4.8.3  Calendar days are now square.
  4.8.2  The calendar squares are all the same, smaller size (date and symbols on top, stability below; strain is in the hover text).
  4.8.1  Today cards: the sleep cards now sit in the Right now row, and the cycle cards share a row with the other signals.
  4.8.0  Today card graphs: the up/down bars are replaced by dots on a shaded band of your usual range (ringed dot = today). Bars with a dashed usual line are a Settings choice.
  4.7.9  Today cards no longer stretch across two columns; every card is the same width. Fixed alert-level cards (4.7.7) dropping out of their groups, so Flare status is back under Right now.
  4.7.8  The little line graphs on the Today cards are now up/down bars: each of the last 14 days as distance above or below your usual. Blue is better than usual, orange is worse (where better and worse apply), today is solid.
  4.7.7  Today cards that are yellow, orange or red now also get an emoji, a WATCH / HIGH / ALERT tag, a light tint and a thicker top border, so the level shows without relying on colour. A Settings checkbox turns the tint and emoji off (the word tag stays).
  4.6.0  A pixel-art mascot in the top banner reacts to your day (walks when steady, startled when strained, sleeps with Zs when you need rest, hops on a good day). The tabs are now a pixel-style menu with icons. Animation can be switched off in Settings.
  4.5.3  Sleep and pace chart legends moved above the plot (they were drawing over it).
  4.5.2  HRV on days with no Visible reading is estimated from the overnight watch data (scaled to your Visible readings, shown as hollow markers) when the two clearly agree. Period markers in the events strip stay pink.
  4.5.1  Pink is now only for period/cycle data (the worst-case color is red). "How it works" is a set of collapsible cards; rounder, outlined panels and cards.
  4.5.0  Modernized the top banner: pills for date, place and data status, a status dot, a sans-serif headline and the key facts as tiles.
  4.4.5  Login window is bigger so the skip button shows; if Garmin rejects the login, the app offers to use the saved data instead.
  4.4.4  If the script sits inside garmin_cache, the app uses the folder above it (so saved data, tokens, delete and skip-login find your files). Plain-language message for a rejected Garmin login.
  4.4.3  The login window has a "Skip login: use saved data" button whenever saved Garmin data exists.
  4.4.2  Delete popup shows which folder it is searching and lets you pick another; results name the folder. The script folder is resolved to a full path.
  4.4.1  Delete-period-data popup is larger, scrolls, and keeps the confirmation box and buttons pinned at the bottom.
  4.4.0  Settings window: turn cycle data off, and permanently delete all period-related data stored by this app. When cycle data is off, nothing about periods is requested from Garmin or read from saved files.
  4.3.2  Garmin cycle calendar is fetched in 90-day pieces (Garmin rejects ranges over 92 days).
  4.3.1  Histamine background reworded as evidence only, no usage guidance.
  4.3.0  The page is split into tabs: Today, Cycle, Sleep, Pace, Timeline, Patterns, How it works.
  4.2.7  Footer disclaimer reworded.
  4.2.6  Histamine card: removed the trials commentary.
  4.2.5  Histamine card: reworded to reflect widespread reports of H1 + H2 blocker relief and the lack of trials.
  4.2.4  Cycle tracker: histamine / mast cell and H1-H2 blocker note added (menstrual and luteal descriptions plus a sourced card).
  4.2.3  Cycle tracker moved to the top (under the summary cards); section headings larger with a divider, descriptions slightly larger.
  4.2.2  Linked-to-what section: removed hedging language, made the status messages larger and the background notes clearly separate, added a "Period start and flares" card.
  4.2.1  Range buttons sit a few lines above the chart titles so they no longer overlap them. Pace points matched to Visible's documented names (PacePoints, PacePoint budget).
  4.2.0  Top cards: explanations moved to hover text (with an info mark); resting heart rate card shows Garmin resting HR, Visible's morning reading and today's average;
         pace points card reads used/ceiling. If your Visible export has pace points (premium), they replace the app's own numbers. (Visible's pace-point format is untested.)
  4.1.1  period_cycles.csv now says which lengths are estimated (carried forward from the first logged day) and which gaps are too long to count.
  4.1.0  Garmin cycle parser now reads the cycle start date Garmin reports (so a period that began with spotting is dated correctly), shows Garmin's own cycle
         summary, and lists long gaps between periods. Version number added (shown at the top of this file, in the window titles and on the dashboard).
  4.0.0  Everything built on top of v3: Visible CSV import and cache, flare detection, pace points (own section, "REST!" verdict), colorblind-safe palette,
         events strip, cycle tracker with wheel and phase notes, Garmin cycle/steps pulls, saved-data option, before/after comparisons, low-HRV and
         low-step cards, and the flare-prediction backtest.

POTS dashboard v3

What changed from v2 (v3):
  * After the Garmin fetch (and barometric pressure) a window asks for an optional Visible export CSV.
    Visible's HRV, stability, crash, period, infection, sleep rating and every symptom tracker it finds are
    read modularly, so it works for any user's tracker list.
  * Baselines are now a 60-day, flare-resistant baseline on log-HRV (lnRMSSD), so a multi-day flare cannot
    silently become your "normal".
  * Stability (1-5) is direction-aware (only worse-than-usual HR/HRV/stress/sleep lowers it) and is calibrated
    to your own Visible stability history when available. Visible's own score overrides it on days you have one.
  * Active flare detection and daytime nap detection (possible crash).

What changed from v1:
  * Uses Garmin's own sleep stages, sleep score and overnight HRV when available.
    The HR-only sleep detector is now just a fallback for nights Garmin has no data for.
  * One shared date axis: every panel lines up, hovering shows all metrics for that day,
    and shading marks pressure-drop days across the whole stack.
  * Baselines are "your last 28 days" (excluding the day itself), not a hand-picked best window.
  * Plain-language summary, a "what seems linked to what" section, and a fixed calendar.
  * Today's data is re-fetched each run, pressure uses the forecast API for recent days,
    errors are logged instead of swallowed, and Garmin login tokens are reused.

Not medical advice. The score compares you with your own recent normal; it is not a diagnosis.
"""
import itertools
import os
import math
import json
import re
import sys
import webbrowser
import traceback
import urllib.request
import urllib.parse
import datetime as dt
import time
from datetime import date, timedelta
from pathlib import Path
from html import escape as _esc

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, simpledialog, filedialog
except ImportError:  # headless / tests
    tk = None

# ----------------------------------------------------------------- settings
DAYS = 120
BASELINE_DAYS = 28           # used for the pace-point ceiling
BASELINE_LONG = 60           # "your normal" window for HRV / HR / stress / sleep (days)
BASELINE_MIN = 5             # fewest readings in that window before a baseline is shown (Visible readings are sparse)
ANCHOR_Q = 0.60              # baseline = this quantile of the window for "higher is better" metrics (0.40 for the others),
                             # so a run of bad days cannot drag "normal" down with it. A heuristic, not a published standard.
VISIBLE_MIN_HRV_DAYS = 5     # use Visible HRV as the HRV series once at least this many days are in the window
# Naps. Heart rate alone cannot reliably tell a nap from quiet resting when your sleep times move around and your daytime resting HR sits
# close to your sleeping HR (true for the data this was tuned on), so the HR-only guess is OFF by default. Garmin's own nap total (when the
# watch reports one) and a "nap" column in symptoms.csv are used instead. Set AUTO_NAP_DETECT = True to add the heart-rate guess.
AUTO_NAP_DETECT = False
NAP_MIN_MINUTES = 30         # shortest daytime rest that counts as a nap
NAP_MAX_MINUTES = 240
NAP_HOURS = (9.0, 19.5)      # the HR guess only looks between these clock hours
NAP_HR_OFFSET = 2            # HR guess: heart rate at or below resting HR + this many bpm
FLARE_HRV_Z = -1.0           # flare signals (each worth 1 point per day)
FLARE_RHR_Z = 1.5
FLARE_STABILITY = 2          # Visible/estimated stability at or below this
FLARE_SYMPTOM_Z = 1.0        # symptom burden this many SD above your usual
FLARE_DAY_POINTS = 2         # a day with this many signals counts as a flare day
FLARE_SOLO_STABILITY = 1     # a stability score this low is a flare day on its own
FLARE_WINDOW = 4             # active flare = flare days on at least 2 of the last this-many days
# Visible's sleep question stores a number, not a label, and the direction is not documented. In your export higher
# codes line up with worse days, so labels are left as raw codes. Fill this in once you are sure, e.g. {1: "Fair"}.
SLEEP_LABELS = {}
BAND_SD = 1.5                # shaded "normal range" half-width
BACKTEST_HORIZON = 7         # the flare backtest asks: will a flare start within this many days?
BACKTEST_MIN_LABELED = 50    # labeled days needed before the backtest reports accuracy
BACKTEST_MIN_FLARES = 8      # separate flares (a flare day after a non-flare day) needed
CACHE_FRESH_HOURS = 12        # if the Garmin data was pulled this recently, offer to skip the login and use the saved data (0 = never ask)
VERSION = "4.8.7"
VISIBLE_PACE_MIN_DAYS = 5    # use Visible's own pace points once at least this many days of them are in the export
TRACK_PERIOD = True          # set False here to switch cycle tracking off for good; otherwise use the Settings window (saved in garmin_cache/settings.json)
TRACK_PERIOD_DEFAULT = TRACK_PERIOD
PERIOD_LENGTH_DEFAULT = 5    # days of flow used when your own logs are too sparse to tell
CYCLE_LENGTH_DEFAULT = 28    # used until you have two logged period starts 21-45 days apart
LUTEAL_DAYS = 14             # ovulation is guessed to be this many days before the next period
PRESSURE_DROP_HPA = -3.0     # day-over-day drop that gets flagged
SLEEP_MIN_MINUTES = 180      # fallback detector: shortest night it will report
# Pace-point zones, relative to YOUR resting HR (not % of max HR, which is often above the
# anaerobic threshold in ME/CFS). Based on user-reported descriptions of Visible and the
# Workwell "resting HR + ~15" rule of thumb. These are NOT official Visible numbers: adjust to taste.
ACTIVITY_OFFSET = 8          # bpm above resting HR where the "activity" zone starts
OVEREXERT_OFFSET = 15        # bpm above resting HR where "over-exertion" starts
POINTS_PER_MIN = 0.05        # points per minute in the activity zone
OVEREXERT_MULT = 4.0         # over-exertion minutes cost this many times more
CEILING_ADJUST = ((2.5, 0.60), (1.5, 0.75), (0.5, 0.90))   # (strain >=, share of usual) heuristic, not validated
# Daily pace ceiling = this quantile of your recent points on NON-flare days (a median would be exceeded on half of ordinary days).
CEILING_QUANTILE = 0.75
CEILING_MIN_DAYS = 7         # fewest usable days before a ceiling is shown
MIN_AWAKE_MINUTES = 240      # a day needs this much awake heart-rate coverage to count toward your usual (a missing-data day looks like a rest day)
FLARE_CEILING = {"active": 0.60, "watch": 0.80}   # share of the ceiling kept while flare signals are showing, heuristic, not validated

HERE = Path(__file__).resolve().parent
if HERE.name.lower() == "garmin_cache":      # the script was dropped inside garmin_cache: use the folder above it, where the rest of the app's files live
    HERE = HERE.parent
OUTPUT = HERE / "garmin_dashboard.html"
CACHE_DIR = HERE / "garmin_cache"
TOKEN_DIR = CACHE_DIR / "tokens"
CACHES = {k: CACHE_DIR / f"{k}.json" for k in ("stats", "hr", "sleep", "hrv", "stresstl", "weather", "menstrual")}
LAST_PULL = CACHE_DIR / "last_pull.txt"
EXPORT_CSV = HERE / "garmin_export.csv"
EXPORT_TXT = HERE / "garmin_export_summary.txt"
SYMPTOMS_CSV = HERE / "symptoms.csv"
PERIOD_EXPORT = HERE / "period_cycles.csv"
PERIOD_OFF = CACHE_DIR / "no_period_question.txt"
SETTINGS_FILE = CACHE_DIR / "settings.json"
PERIOD_WORDS = ("period", "menstru", "spotting", "ovulat", "cervical", "fertil", "pregnan", "pms", "cycle")   # Visible rows with these words in the name or category count as period data
PERIOD_SYMPTOM_COLS = ("period", "mood", "discharge", "period_symptoms")                                  # symptoms.csv columns that hold cycle information
VISIBLE_DIR_FILE = CACHE_DIR / "visible_last_folder.txt"
VISIBLE_CACHE = CACHE_DIR / "visible_history.csv"      # every Visible row you have ever imported, merged (newest import wins)
SLEEP_CHECKED = CACHE_DIR / "sleep_checked.txt"       # nights you told the app "Garmin is right" about
SYMPTOM_COLS = ["date", "symptoms", "pem", "stand_hr_rise", "period", "nap", "flare", "bed", "wake", "sleep_h", "mood", "discharge", "period_symptoms"]
ERROR_LOG = HERE / "garmin_error_log.txt"

BG, PANEL, GRID, TEXT, MUTED = "#12161c", "#1a2029", "#252d38", "#e4e2dc", "#8d96a3"
# Colour-blind-safe status colours (Okabe-Ito based). There is no red or green anywhere: "better" is blue, "typical" is neutral grey, and
# "worse" climbs yellow -> orange -> red. Pink is kept for period and cycle data only. Checked with colour-blindness simulations (deuteranopia, protanopia, tritanopia): every
# pair stays clearly apart. Every flag also has a text label or a hover value, so colour is never the only cue.
BETTER, TYPICAL, WATCH, WARN, ALERT = "#56B4E9", "#C9D0D9", "#F0E442", "#E08A00", "#D1432C"
DEEP, LIGHT, REM, AWAKE, EST = "#4b3a9e", "#7d6fd6", "#bc8cff", "#e3b341", "#8d96a3"

LOG = []


def log(msg):
    if msg not in LOG:
        LOG.append(msg)
        print(msg)


# ----------------------------------------------------------------- helpers
def load_cache(path):
    try:
        return json.loads(path.read_text()) if path.exists() else {}
    except Exception as e:
        log(f"Could not read {path.name}: {e}")
        return {}


def save_cache(name, data):
    CACHE_DIR.mkdir(exist_ok=True)
    CACHES[name].write_text(json.dumps(data))


def zone(s):
    """s = strain-style number: 0 is your normal, positive means body working harder."""
    if s is None or pd.isna(s):
        return "No data", MUTED
    if s < -0.5:
        return "Better than usual", BETTER
    if s < 0.5:
        return "Typical for you", TYPICAL
    if s < 1.5:
        return "A little off", WATCH
    if s < 2.5:
        return "Clearly off, go easy", WARN
    return "Danger zone: rest", ALERT


def hhmm(ts):
    return ts.strftime("%H:%M") if isinstance(ts, (dt.datetime, pd.Timestamp)) else ""


# ----------------------------------------------------------------- Garmin fetch
def garmin_login(email, password):
    from garminconnect import Garmin
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)

    def mfa():
        if tk:
            return simpledialog.askstring("Garmin", "Enter the verification code Garmin sent you:")
        return input("Garmin verification code: ")

    try:
        g = Garmin(email, password, prompt_mfa=mfa)
    except TypeError:
        g = Garmin(email, password)
    try:
        g.login(str(TOKEN_DIR))      # reuses saved tokens when present
    except TypeError:
        g.login()
    return g


def _call(fn, *args):
    try:
        return fn(*args)
    except Exception as e:
        log(f"{getattr(fn, '__name__', 'call')} failed: {type(e).__name__}: {e}")
        return None


def load_settings():
    try:
        d = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def save_settings(d):
    CACHE_DIR.mkdir(exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(d, indent=1), encoding="utf-8")


def apply_settings():
    """Reads garmin_cache/settings.json. Cycle data is on unless you turned it off here or set TRACK_PERIOD = False at the top of the script."""
    global TRACK_PERIOD
    TRACK_PERIOD = bool(TRACK_PERIOD_DEFAULT and load_settings().get("track_period", True))
    return TRACK_PERIOD


def _wipe(path):
    """Overwrites a file with zeros before it is removed or rewritten, so the old contents are not left sitting on the disk."""
    try:
        size = Path(path).stat().st_size
        with open(path, "r+b") as fh:
            done = 0
            while done < size:
                n = min(1 << 20, size - done)
                fh.write(b"\0" * n)
                done += n
            fh.flush()
            os.fsync(fh.fileno())
    except OSError:
        pass


def delete_forever(path):
    """Permanent delete (never the recycle bin). Returns True if a file was removed."""
    path = Path(path)
    if not path.exists():
        return False
    _wipe(path)
    path.unlink()
    return True


def is_period_row(df):
    """True for Visible rows that are about periods or cycles (by tracker name or category)."""
    txt = (df["tracker_name"].fillna("") + " " + df["tracker_category"].fillna("")).str.lower()
    m = pd.Series(False, index=df.index)
    for w in PERIOD_WORDS:
        m |= txt.str.contains(w, regex=False)
    return m


def erase_period_data(base=None):
    """Permanently removes everything period-related this app stored on this computer. Returns a list of plain-language lines saying what was done.
    base = the folder holding the app's files (the script's own folder unless you pick another one)."""
    base = Path(base) if base else HERE
    cache = base / "garmin_cache"
    mens, p_exp, outp, exp_csv = cache / "menstrual.json", base / "period_cycles.csv", base / "garmin_dashboard.html", base / "garmin_export.csv"
    sym_csv, vis_cache = base / "symptoms.csv", cache / "visible_history.csv"
    out = [f"Folder searched: {base}"]
    for path, what in ((mens, "Garmin cycle-tracking data (menstrual.json)"), (p_exp, "period_cycles.csv"),
                       (outp, "the last dashboard page (garmin_dashboard.html)"), (exp_csv, "garmin_export.csv")):
        try:
            out.append(("Deleted " if delete_forever(path) else "Not found, nothing to delete: ") + what)
        except OSError as ex:
            out.append(f"COULD NOT DELETE {what}: {ex}")
    try:                                                    # symptoms.csv: clear only the cycle columns, keep everything else
        if sym_csv.exists():
            d = pd.read_csv(sym_csv, dtype=str, keep_default_na=False)
            cols = [c for c in PERIOD_SYMPTOM_COLS if c in d.columns]
            n = int((d[cols] != "").any(axis=1).sum()) if cols else 0
            for c in cols:
                d[c] = ""
            _wipe(sym_csv)
            d.to_csv(sym_csv, index=False, encoding="utf-8")
            out.append(f"Cleared the period, mood, discharge and period-symptom columns on {n} day(s) in symptoms.csv (your other entries are kept)")
        else:
            out.append("Not found, nothing to clean: symptoms.csv")
    except Exception as ex:
        out.append(f"COULD NOT CLEAN symptoms.csv: {ex}")
    try:                                                    # saved Visible history: drop the period rows, keep the rest
        if vis_cache.exists():
            v = pd.read_csv(vis_cache, dtype=str, keep_default_na=False)
            m = is_period_row(v)
            _wipe(vis_cache)
            v[~m].to_csv(vis_cache, index=False, encoding="utf-8")
            out.append(f"Removed {int(m.sum())} period/cycle row(s) from your saved Visible history")
        else:
            out.append("Not found, nothing to clean: saved Visible history")
    except Exception as ex:
        out.append(f"COULD NOT CLEAN the saved Visible history: {ex}")
    return out


def parse_daily_stats(raw):
    """Garmin's daily summary: total steps and intensity minutes (None when the call failed)."""
    if not isinstance(raw, dict):
        return None, None
    steps = raw.get("totalSteps")
    mins = (raw.get("moderateIntensityMinutes") or 0) + 2 * (raw.get("vigorousIntensityMinutes") or 0)
    return (int(steps) if steps is not None else None), (int(mins) if steps is not None else None)


def parse_hr(raw):
    if not isinstance(raw, dict):
        return None, []
    pts = [[p[0], p[1]] for p in (raw.get("heartRateValues") or []) if p and len(p) > 1 and p[1]]
    return raw.get("restingHeartRate"), pts


def parse_stress(raw):
    if not isinstance(raw, dict):
        return None
    v = raw.get("avgStressLevel")
    return v if isinstance(v, (int, float)) and v >= 0 else None


def parse_sleep(raw):
    s = (raw or {}).get("dailySleepDTO") if isinstance(raw, dict) else None
    if not s or not s.get("sleepTimeSeconds") or not s.get("sleepStartTimestampLocal"):
        return {}
    score = ((s.get("sleepScores") or {}).get("overall") or {}).get("value")
    levels = []
    try:  # stage timeline; stage names are inferred by matching totals to Garmin's stage totals
        off = (s["sleepStartTimestampLocal"] - s["sleepStartTimestampGMT"]) / 1000.0
        segs, tot = [], {}
        for x in raw.get("sleepLevels") or []:
            a = dt.datetime.fromisoformat(str(x["startGMT"]).split(".")[0]) + timedelta(seconds=off)
            b = dt.datetime.fromisoformat(str(x["endGMT"]).split(".")[0]) + timedelta(seconds=off)
            v = float(x["activityLevel"])
            segs.append((a, b, v))
            tot[v] = tot.get(v, 0.0) + (b - a).total_seconds()
        stages = ["deep", "light", "rem", "awake"]
        want = [s.get("deepSleepSeconds") or 0, s.get("lightSleepSeconds") or 0, s.get("remSleepSeconds") or 0,
                s.get("awakeSleepSeconds") or 0]
        vals = sorted(tot)
        if segs and len(vals) <= 4:
            def err(p):
                return sum(abs(tot[v] - want[stages.index(n)]) for v, n in zip(vals, p))
            best = min(itertools.permutations(stages, len(vals)), key=err)
            if err(best) <= 0.25 * sum(tot.values()):
                m = dict(zip(vals, best))
                levels = [[a.isoformat(), b.isoformat(), m[v]] for a, b, v in segs]
    except Exception as e:
        log(f"Could not read sleep stage timeline: {type(e).__name__}: {e}")
    movement = []
    try:  # how much you moved each minute (the wrist's motion sensor), the line Garmin draws under the stages
        moff = (s["sleepStartTimestampLocal"] - s["sleepStartTimestampGMT"]) / 1000.0
        for x in raw.get("sleepMovement") or []:
            lvl = x.get("activityLevel")
            if lvl is None:
                continue
            a = dt.datetime.fromisoformat(str(x["startGMT"]).split(".")[0]) + timedelta(seconds=moff)
            movement.append([a.isoformat(), round(float(lvl), 2)])
    except Exception as e:
        log(f"Could not read sleep movement: {type(e).__name__}: {e}")
    return {"onset_ms": s["sleepStartTimestampLocal"], "offset_ms": s["sleepEndTimestampLocal"], "movement": movement,
            "asleep_s": s.get("sleepTimeSeconds"), "deep_s": s.get("deepSleepSeconds"),
            "light_s": s.get("lightSleepSeconds"), "rem_s": s.get("remSleepSeconds"),
            "awake_s": s.get("awakeSleepSeconds"), "score": score,
            "resp": s.get("averageRespirationValue"), "nap_s": s.get("napTimeSeconds"), "levels": levels}


def parse_stress_timeline(raw):
    """[[epoch_ms, stress 0-100], ...] with unmeasured (negative) readings dropped."""
    if not isinstance(raw, dict):
        return []
    return [[int(a), int(b)] for a, b in (raw.get("stressValuesArray") or []) if a is not None and b is not None and b >= 0]


def parse_hrv(raw):
    if not isinstance(raw, dict):
        return None
    return (raw.get("hrvSummary") or {}).get("lastNightAvg")


def fetch_weather(zip_code, cache, start, end):
    def get(url):
        last = None
        for wait in (0, 2, 5):                      # a slow or briefly unavailable weather service gets two more tries
            if wait:
                time.sleep(wait)
            try:
                with urllib.request.urlopen(url, timeout=30) as r:
                    return json.loads(r.read().decode())
            except Exception as e:
                last = e
        raise last

    loc = cache.get("_loc")
    if not loc or loc.get("zip") != zip_code:
        try:
            p = get("https://api.zippopotam.us/us/" + zip_code)["places"][0]
            loc = {"zip": zip_code, "lat": p["latitude"], "lon": p["longitude"],
                   "city": p["place name"], "state": p["state abbreviation"]}
            cache["_loc"] = loc
        except Exception as e:
            log(f"Zip lookup failed: {e}")
            return cache.get("_loc")

    def merge(data):
        by_day = {}
        h = data.get("hourly", {})
        for t, v in zip(h.get("time", []), h.get("surface_pressure", [])):
            if v is not None:
                by_day.setdefault(t[:10], []).append(v)
        for d, vals in by_day.items():
            cache[d] = {"mean": round(float(np.mean(vals)), 1), "min": round(min(vals), 1),
                        "max": round(max(vals), 1)}

    base = {"latitude": loc["lat"], "longitude": loc["lon"], "hourly": "surface_pressure", "timezone": "auto"}
    try:  # archive lags ~5 days, so ask it only for older dates
        a_end = end - timedelta(days=7)
        q = dict(base, start_date=start.isoformat(), end_date=a_end.isoformat())
        merge(get("https://archive-api.open-meteo.com/v1/archive?" + urllib.parse.urlencode(q)))
    except Exception as e:
        log(f"Pressure archive fetch failed ({type(e).__name__}: {e}). Older days come from the saved cache.")
    try:  # recent days from the forecast API
        q = dict(base, past_days=10, forecast_days=1)
        merge(get("https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(q)))
    except Exception as e:
        log(f"Pressure recent fetch failed ({type(e).__name__}: {e}). The weather service did not answer, so recent days use what was saved earlier; it retries next run.")
    return loc


def fetch_all(email, password, zip_code, progress, offline=False):
    end = date.today()
    start = end - timedelta(days=DAYS)
    all_dates = [(start + timedelta(days=i)).isoformat() for i in range(DAYS + 1)]
    C = {k: load_cache(p) for k, p in CACHES.items()}
    refresh = set(all_dates[-2:])                       # today and yesterday are never final
    todo = [d for d in all_dates if d not in C["stats"] or d in refresh]
    sleep_only = [d for d in all_dates if d not in todo and C["sleep"].get(d) and ("levels" not in C["sleep"][d] or "nap_s" not in C["sleep"][d] or "movement" not in C["sleep"][d])]

    stress_only = [d for d in all_dates if d not in todo and d not in C["stresstl"]]
    steps_only = [d for d in all_dates if d not in todo and not C["stats"].get(d, {}).get("steps_checked")]

    if offline:
        progress.update("Using saved Garmin data (no login)...", 60)
    elif todo or sleep_only or stress_only or steps_only:
        progress.update("Logging in to Garmin Connect...", 3)
        g = garmin_login(email, password)
        for n, d in enumerate(todo):
            progress.update("Fetching Garmin data...", 5 + 80 * n / len(todo), f"{d}  ({n + 1}/{len(todo)})")
            hr_raw = _call(g.get_heart_rates, d)
            sleep_raw = _call(g.get_sleep_data, d)
            if hr_raw is None and sleep_raw is None:
                continue                                  # looks like a failure, retry next run
            rhr, pts = parse_hr(hr_raw)
            sleep = parse_sleep(sleep_raw)
            st_raw = _call(g.get_stress_data, d)
            if st_raw is not None:
                C["stresstl"][d] = parse_stress_timeline(st_raw)
            stp, imin = parse_daily_stats(_call(g.get_stats, d))
            C["stats"][d] = {"rhr": rhr, "stress": parse_stress(st_raw),
                             "resp": sleep.get("resp"), "steps": stp, "imin": imin, "steps_checked": True}
            C["sleep"][d] = sleep
            C["hrv"][d] = {"hrv": parse_hrv(_call(g.get_hrv_data, d))}
            if pts:
                C["hr"][d] = pts
            if n % 15 == 14:
                for k in ("stats", "hr", "sleep", "hrv", "stresstl"):
                    save_cache(k, C[k])
        for n, d in enumerate(stress_only):
            progress.update("Adding overnight stress timelines (one time)...", 85 + 4 * n / len(stress_only), d)
            st_raw = _call(g.get_stress_data, d)
            if st_raw is not None:
                C["stresstl"][d] = parse_stress_timeline(st_raw)
        for n, d in enumerate(steps_only):
            progress.update("Adding daily steps (one time)...", 89 + 1 * n / max(1, len(steps_only)), d)
            stp, imin = parse_daily_stats(_call(g.get_stats, d))
            C["stats"][d].update({"steps": stp, "imin": imin, "steps_checked": True})
        for n, d in enumerate(sleep_only):
            progress.update("Adding sleep stage and movement timelines (one time)...", 85 + 5 * n / len(sleep_only), d)
            raw_s = _call(g.get_sleep_data, d)
            if raw_s is not None:
                C["sleep"][d] = parse_sleep(raw_s)
        for k in ("stats", "hr", "sleep", "hrv", "stresstl"):
            save_cache(k, C[k])
        if TRACK_PERIOD:
            try:
                fetch_menstrual(g, C["menstrual"], start, end, progress)
                save_cache("menstrual", C["menstrual"])
            except Exception as ex:
                log(f"Cycle-tracking pull failed: {type(ex).__name__}: {ex}")
        else:
            log("Cycle data is turned off in Settings, so nothing about periods was requested from Garmin.")
        try:
            CACHE_DIR.mkdir(exist_ok=True)
            LAST_PULL.write_text(dt.datetime.now().isoformat(timespec="seconds"))
        except OSError:
            pass
    else:
        progress.update("All data cached.", 85)

    loc = None
    if zip_code and not offline:
        progress.update("Fetching barometric pressure...", 90)
        loc = fetch_weather(zip_code, C["weather"], start, end)
        save_cache("weather", C["weather"])
    elif C["weather"].get("_loc"):
        loc = C["weather"]["_loc"]

    raw = {k: {d: v for d, v in C[k].items() if d in set(all_dates)} for k in ("stats", "hr", "sleep", "hrv", "stresstl")}
    raw["weather"] = {d: v for d, v in C["weather"].items() if not d.startswith("_")}
    raw["menstrual"] = C["menstrual"] if TRACK_PERIOD else {}
    raw["loc"] = loc
    return raw, start, end


# ----------------------------------------------------------------- analysis
def detect_sleep_fallback(hr_by_date, rhr, skip):
    """HR-only sleep finder for nights Garmin has no sleep record. Returns {wake_date: record}."""
    nights = {}
    for d, pts in hr_by_date.items():
        for t, v in pts:
            ts = dt.datetime.fromtimestamp(t / 1000)
            nights.setdefault((ts + timedelta(hours=12)).strftime("%Y-%m-%d"), []).append((ts, v))
    out = {}
    for key, pts in nights.items():
        if key in skip:
            continue
        s = pd.Series({t: v for t, v in sorted(pts)}, dtype=float)
        k = pd.Timestamp(key)
        s = s[(s.index >= k - pd.Timedelta(hours=4)) & (s.index <= k + pd.Timedelta(hours=11))]
        if len(s) < 60:
            continue
        r = rhr.get(k, np.nan)
        r = float(r) if not pd.isna(r) else float(rhr.median()) if rhr.notna().any() else 60.0
        smooth = s.rolling(5, center=True, min_periods=3).median()
        # asleep = near resting HR AND near this night's own lowest readings
        thr = min(r + 6, float(s.quantile(0.10)) + 10)
        asleep = (smooth < thr).values
        idx = s.index
        gap_min = np.diff(idx.values).astype("timedelta64[s]").astype(float) / 60
        dur = np.append(np.minimum(gap_min, 5.0), 2.0)
        n = len(s)
        runs, i = [], 0
        while i < n:
            if asleep[i]:
                j = i
                while j + 1 < n and asleep[j + 1] and gap_min[j] <= 30:
                    j += 1
                runs.append([i, j])
                i = j + 1
            else:
                i += 1
        merged = []
        for a, b in runs:
            if merged and (idx[a] - idx[merged[-1][1]]).total_seconds() / 60 <= 25:
                merged[-1][1] = b
            else:
                merged.append([a, b])
        if not merged:
            continue
        a, b = max(merged, key=lambda r_: idx[r_[1]] - idx[r_[0]])
        span = (idx[b] - idx[a]).total_seconds() / 60 + 2
        asleep_min = float(dur[a:b + 1][asleep[a:b + 1]].sum())
        if asleep_min < SLEEP_MIN_MINUTES:
            continue
        seg = asleep[a:b + 1]
        wakes = int(((seg[:-1]) & (~seg[1:])).sum())
        eff = asleep_min / span
        out[key] = {"onset": idx[a].to_pydatetime(), "offset": idx[b].to_pydatetime(),
                    "sleep_h": asleep_min / 60, "awake_h": max(0, span - asleep_min) / 60,
                    "score": int(round(min(1, asleep_min / 480) * 70 + eff * 30)), "src": "est", "wakes": wakes}
    return out


def compute_pace(hr_by_date, rhr_series, sleep_windows=()):
    """Pace points per 'waking day' from time spent above your own resting HR.
    Rest (<= RHR + ACTIVITY_OFFSET) is free; activity zone costs POINTS_PER_MIN; over-exertion (>= RHR + OVEREXERT_OFFSET) costs
    OVEREXERT_MULT times more. Time Garmin recorded as sleep is never counted, and each awake sample belongs to the day of the wake-up
    before it, so your day starts when you wake (not at midnight) whatever hours you keep. sleep_windows = [(onset, offset, day_key)]."""
    rhr14 = rhr_series.rolling(14, min_periods=5).mean()
    samples = {}
    for pts in hr_by_date.values():
        for p_ in pts:
            samples[int(p_[0])] = p_[1]
    if not samples:
        return {}
    ts_ms = np.array(sorted(samples), dtype=float)
    hr = np.array([samples[int(t)] for t in ts_ms], dtype=float)
    mins = np.append(np.minimum(np.diff(ts_ms) / 60000.0, 5.0), 2.0)
    when = [dt.datetime.fromtimestamp(t / 1000) for t in ts_ms]
    wins = sorted((a, b, k) for a, b, k in sleep_windows if a and b)
    offs = [b for _, b, _ in wins]
    asleep = np.zeros(len(when), dtype=bool)
    keys = []
    j = 0
    for i_, w in enumerate(when):
        while j < len(wins) and offs[j] <= w:
            j += 1
        # j = number of wake-ups at or before this sample; the one before it is the current waking day
        in_sleep = any(a <= w <= b for a, b, _ in wins[max(0, j - 1): j + 2])
        asleep[i_] = in_sleep
        key = None
        if j > 0:                       # awake time belongs to the wake-up before it, up to the next sleep (days can run past midnight)
            span_end = wins[j][0] if j < len(wins) else w
            if (span_end - offs[j - 1]).total_seconds() <= 30 * 3600 and (w - offs[j - 1]).total_seconds() <= 30 * 3600:
                key = wins[j - 1][2]
        keys.append(key or w.strftime("%Y-%m-%d"))
    out = {}
    df = pd.DataFrame({"key": keys, "hr": hr, "mins": mins, "asleep": asleep, "t": when})
    df = df[~df["asleep"]]
    for d, g in df.groupby("key"):
        r = rhr14.get(pd.Timestamp(d), np.nan)
        if pd.isna(r):
            continue
        over = g["hr"].values >= r + OVEREXERT_OFFSET
        act = (g["hr"].values > r + ACTIVITY_OFFSET) & ~over
        m = g["mins"].values
        out[d] = {"act": round(float(m[act].sum() * POINTS_PER_MIN), 2),
                  "over": round(float(m[over].sum() * POINTS_PER_MIN * OVEREXERT_MULT), 2),
                  "min_act": float(m[act].sum()), "min_over": float(m[over].sum()),
                  "awake_min": float(m.sum()), "last": g["t"].max().strftime("%H:%M"),
                  "avg_hr": float((g["hr"].values * m).sum() / m.sum()) if m.sum() > 0 else float("nan")}
    return out


def ensure_symptoms_header():
    """Creates symptoms.csv, or adds the new columns to its header when the file has nothing but a header line."""
    head = ",".join(SYMPTOM_COLS)
    try:
        if not SYMPTOMS_CSV.exists():
            SYMPTOMS_CSV.write_text(head + "\n")
        else:
            lines = [x for x in SYMPTOMS_CSV.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
            if len(lines) == 1 and lines[0].strip() != head and lines[0].lower().startswith("date"):
                SYMPTOMS_CSV.write_text(head + "\n")
    except OSError:
        pass


def parse_clock(x):
    """'07:30', '7:30 am', '7am' -> datetime.time, or None."""
    x = str(x).strip()
    for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p", "%I %p", "%I%p"):
        try:
            return dt.datetime.strptime(x.upper(), fmt).time()
        except ValueError:
            continue
    return None


def load_sleep_overrides():
    """Nights you corrected in symptoms.csv: {'YYYY-MM-DD': {'bed': time|None, 'wake': time|None, 'sleep_h': float|None}}.
    The date is the day you woke up. Garmin's sleep times can be wrong, so anything here replaces them for that night."""
    out = {}
    try:
        if not SYMPTOMS_CSV.exists():
            return out
        d = pd.read_csv(SYMPTOMS_CSV, dtype=str, keep_default_na=False)
        for c in ("bed", "wake", "sleep_h"):
            if c not in d:
                d[c] = ""
        for _, r in d.iterrows():
            day = pd.to_datetime(str(r["date"]).strip(), errors="coerce")
            if pd.isna(day):
                continue
            bed, wake = parse_clock(r["bed"]) if r["bed"].strip() else None, parse_clock(r["wake"]) if r["wake"].strip() else None
            try:
                hrs = float(r["sleep_h"]) if r["sleep_h"].strip() else None
            except ValueError:
                hrs = None
            if (bed and wake) or hrs:
                out[day.strftime("%Y-%m-%d")] = {"bed": bed, "wake": wake, "sleep_h": hrs}
    except Exception as e:
        log(f"Could not read sleep corrections from symptoms.csv: {e}")
    return out


def apply_sleep_overrides(rows, overrides):
    """Replaces Garmin's (or the heart-rate guess's) sleep for the nights you corrected. Stages and score are dropped for those nights."""
    for d, ov in overrides.items():
        base = rows.get(d)
        hrs = ov.get("sleep_h")
        if ov.get("bed") and ov.get("wake"):
            day = dt.datetime.strptime(d, "%Y-%m-%d").date()
            off = dt.datetime.combine(day, ov["wake"])
            on = dt.datetime.combine(day - timedelta(days=1) if ov["bed"] > ov["wake"] else day, ov["bed"])
            span = (off - on).total_seconds() / 3600.0
            h = min(hrs, span) if hrs else span
            rows[d] = {"onset": on, "offset": off, "sleep_h": h, "awake_h": max(0.0, span - h), "score": None, "src": "manual"}
        elif hrs and base:
            span = (base["offset"] - base["onset"]).total_seconds() / 3600.0
            rows[d] = {"onset": base["onset"], "offset": base["offset"], "sleep_h": hrs, "awake_h": max(0.0, span - hrs), "score": None, "src": "manual"}
    return rows


def load_symptoms(idx):
    """Optional symptoms.csv: date, symptoms (0-10), pem (0/1), stand_hr_rise (bpm after 10 min standing), period (1 on flow days),
    nap (1 if you napped, 0 if not), flare (1 if you are in a flare that day, 0 if not). Anything you enter here wins over the Visible import for that day.
    Optional sleep corrections (bed, wake as HH:MM, sleep_h hours actually asleep) are read by load_sleep_overrides()."""
    cols = ["symptoms", "pem", "stand_hr_rise", "period", "nap", "flare", "mood"]
    ensure_symptoms_header()
    if not SYMPTOMS_CSV.exists():
        return pd.DataFrame(np.nan, index=idx, columns=cols)
    try:
        d = pd.read_csv(SYMPTOMS_CSV)
        d["date"] = pd.to_datetime(d["date"])
        d = d.drop_duplicates("date", keep="last").set_index("date")
        for c in cols:
            d[c] = pd.to_numeric(d[c], errors="coerce") if c in d else np.nan
        return d[cols].reindex(idx)
    except Exception as e:
        log(f"Could not read symptoms.csv: {e}")
        return pd.DataFrame(np.nan, index=idx, columns=cols)


def fill_hrv_from_watch(vis, alt, log_alt=False, min_overlap=6, min_r=0.35):
    """Estimates Visible-style HRV (ms) on days with no Visible reading from the watch-based overnight series.
    The watch series is put on Visible's scale with a straight-line fit on the days you have both (in log units, since HRV is skewed).
    Returns (series in ms or None, correlation). None when there are too few shared days or the two do not move together."""
    a = np.log(alt.where(alt > 0)) if log_alt else alt.astype(float)
    v = np.log(vis.where(vis > 0))
    both = pd.concat([a, v], axis=1).dropna()
    if len(both) < min_overlap or both.iloc[:, 0].std() == 0:
        return None, float("nan")
    r = float(both.iloc[:, 0].corr(both.iloc[:, 1]))
    if not (r >= min_r):
        return None, r
    slope = r * both.iloc[:, 1].std() / both.iloc[:, 0].std()            # least-squares line
    icpt = both.iloc[:, 1].mean() - slope * both.iloc[:, 0].mean()
    return np.exp(icpt + slope * a), r


def estimate_hrv(raw, windows, idx):
    """Best-effort HRV stand-in when the watch gives no HRV. True HRV needs beat-to-beat intervals,
    which the Garmin feed does not include, so this builds a relative index (50 = your typical night)
    from three overnight signals:
      stress  - Garmin's stress score is derived from beat timing, so lower overnight stress = higher HRV  (weight 0.6)
      steady  - RMSSD of the 2-minute sleeping HR samples; a smoother night suggests calmer autonomic tone   (weight 0.2)
      low_hr  - how low your sleeping HR sits (mean of the lowest 20% of samples); lower is better        (weight 0.2)
    """
    comp = {"stress": {}, "steady": {}, "low_hr": {}}
    for d, (on, off) in windows.items():
        days = [(pd.Timestamp(d) - pd.Timedelta(days=1)).strftime("%Y-%m-%d"), d]
        st = [v for day in days for t, v in raw.get("stresstl", {}).get(day, [])
              if on <= dt.datetime.fromtimestamp(t / 1000) <= off]
        if len(st) >= 10:
            comp["stress"][d] = float(np.mean(st))
        hr = sorted((t, v) for day in days for t, v in raw["hr"].get(day, [])
                    if on <= dt.datetime.fromtimestamp(t / 1000) <= off)
        if len(hr) >= 30:
            arr = np.array([v for _, v in hr], dtype=float)
            comp["steady"][d] = float(np.sqrt(np.mean(np.diff(arr) ** 2)))
            comp["low_hr"][d] = float(np.sort(arr)[: max(5, len(arr) // 5)].mean())
    cdf = pd.DataFrame({k: pd.Series({pd.Timestamp(d): v for d, v in c.items()}, dtype=float) for k, c in comp.items()}).reindex(idx)
    z = (cdf - cdf.mean()) / cdf.std().replace(0, np.nan)
    wts = {"stress": -0.6, "steady": 0.2, "low_hr": -0.2}      # sign = direction that means "higher HRV"
    num = sum(z[k].fillna(0) * w for k, w in wts.items())
    den = sum(z[k].notna() * abs(w) for k, w in wts.items())
    est = (num / den.replace(0, np.nan))
    if est.notna().sum() < 14 or not est.std() > 0:
        return pd.Series(np.nan, index=idx), cdf
    return 50 + 10 * (est - est.mean()) / est.std(), cdf


def _series(src, key, idx):
    vals = {pd.Timestamp(k): v.get(key) for k, v in src.items() if isinstance(v, dict) and v}
    return pd.Series(vals, dtype=float).reindex(idx)


# ----------------------------------------------------------------- Visible import
NON_SYMPTOM_CATS = {"measurement", "sleep", "experience", "note", "physical"}


VIS_NEED = ["observation_date", "tracker_name", "tracker_category", "observation_value"]


def read_visible_rows(path):
    """Reads a Visible export into a plain 4-column table (checks that it really is one)."""
    raw = pd.read_csv(path, dtype=str, keep_default_na=False)
    raw.columns = [c.strip().lower().lstrip("\ufeff") for c in raw.columns]
    if not set(VIS_NEED).issubset(raw.columns):
        raise ValueError("This does not look like a Visible export. Missing columns: " + ", ".join(sorted(set(VIS_NEED) - set(raw.columns))))
    return raw[VIS_NEED].copy()


def read_visible_cache():
    try:
        return read_visible_rows(VISIBLE_CACHE) if VISIBLE_CACHE.exists() else None
    except Exception as e:
        log(f"Could not read the saved Visible history: {e}")
        return None


def visible_cache_last_date():
    c = read_visible_cache()
    if c is None or c.empty:
        return None
    d = pd.to_datetime(c["observation_date"].str.strip(), errors="coerce").dropna()
    return d.max() if len(d) else None


def load_visible_csv(path=None):
    """Visible data = what is saved from earlier imports + the new export (if you picked one). The merged history is saved back to
    garmin_cache/visible_history.csv, so skipping the file picker later still uses everything you have imported before."""
    new = read_visible_rows(path) if path else None
    if new is not None and not TRACK_PERIOD:
        new = new[~is_period_row(new)]                      # cycle data is off: period rows in a new export are not saved
    old = read_visible_cache()
    parts = [x for x in (old, new) if x is not None and len(x)]
    if not parts:
        raise ValueError("There is no Visible data to read yet.")
    merged = pd.concat(parts, ignore_index=True)
    merged["observation_date"] = merged["observation_date"].str.strip()
    for c in ("tracker_name", "tracker_category"):
        merged[c] = merged[c].str.strip()
    merged = merged.drop_duplicates(["observation_date", "tracker_name", "tracker_category"], keep="last")   # a newer export wins
    if new is not None:
        try:
            CACHE_DIR.mkdir(exist_ok=True)
            merged.to_csv(VISIBLE_CACHE, index=False, encoding="utf-8")
        except OSError as e:
            log(f"Could not save the Visible history: {e}")
    if not TRACK_PERIOD:
        merged = merged[~is_period_row(merged)]            # and saved ones are ignored while it is off
    return parse_visible(merged)


def parse_visible(rows):
    """Reads Visible rows (long format: observation_date, tracker_name, tracker_category, observation_value).
    Nothing about the user's tracker list is hard-coded: the measurements, sleep, experience flags and notes are picked up by
    name, and EVERY other category (Pain, Brain, Gastrointestinal, a custom one...) is treated as a symptom tracker.
    Returns a dict with a per-day table, the symptom matrix, notes and a short description of what was found."""
    raw = rows.copy()
    raw["date"] = pd.to_datetime(raw["observation_date"].str.strip(), errors="coerce").dt.normalize()
    raw = raw.dropna(subset=["date"])
    raw["name"] = raw["tracker_name"].str.strip()
    raw["cat"] = raw["tracker_category"].str.strip()
    raw["catl"], raw["namel"] = raw["cat"].str.lower(), raw["name"].str.lower()
    raw["num"] = pd.to_numeric(raw["observation_value"].str.strip(), errors="coerce")

    notes = raw[(raw["catl"] == "note") & (raw["observation_value"].str.strip() != "")]
    notes = notes.groupby("date")["observation_value"].apply(lambda v: " / ".join(x.strip() for x in v))
    num = raw[(raw["catl"] != "note")].dropna(subset=["num"])

    def pick(cat, name):
        return num[(num["catl"] == cat) & (num["namel"] == name)].groupby("date")["num"].last()

    daily = pd.concat({"vis_hrv": pick("measurement", "hrv"), "vis_rhr": pick("measurement", "resting hr"),
                       "vis_stab": pick("measurement", "stability score"), "vis_sleep": pick("sleep", "sleep"),
                       "vis_crash": pick("experience", "crash"), "vis_period": pick("experience", "period"),
                       "vis_infection": pick("experience", "infection")}, axis=1).astype(float)
    phys = num[num["catl"] == "physical"].groupby("date")["num"].mean()
    daily["vis_active"] = phys.reindex(daily.index)
    pace_rows = num[num["namel"].str.contains("pace", na=False)]                       # Visible premium: pace points (name and category not documented, so matched by name)
    is_lim = pace_rows["namel"].str.contains("limit|max|target|budget|ceiling|goal|allowance", na=False)
    daily["vis_pace"] = pace_rows[~is_lim].groupby("date")["num"].last().reindex(daily.index)
    daily["vis_pace_limit"] = pace_rows[is_lim].groupby("date")["num"].last().reindex(daily.index)

    fc = num[num["catl"].str.startswith("funcap")]
    if len(fc):                                           # Funcap items are 0-6, higher = more able
        scale = max(6.0, float(fc["num"].max()))
        daily["vis_funcap"] = (fc.groupby("date")["num"].mean() / scale * 10).reindex(daily.index)
    else:
        daily["vis_funcap"] = np.nan

    sym = num[~num["catl"].isin(NON_SYMPTOM_CATS) & ~num["catl"].str.startswith("funcap") & ~num["namel"].str.contains("pace", na=False)]
    if len(sym):
        mat = sym.pivot_table(index="date", columns="name", values="num", aggfunc="last")
        sym_cat = sym.drop_duplicates("name").set_index("name")["cat"].to_dict()
        scale = max(3.0, float(mat.max().max()))          # Visible rates symptoms 0-3; adapts if a tracker uses more
        logged = mat.notna().sum(axis=1) >= min(3, mat.shape[1])
        burden = (mat.mean(axis=1) / scale * 10).where(logged)
    else:
        mat, sym_cat, scale, burden = pd.DataFrame(), {}, 3.0, pd.Series(dtype=float)
    daily["vis_burden"] = burden.reindex(daily.index) if len(burden) else np.nan
    daily = daily.reindex(daily.index.union(mat.index)).sort_index()
    daily["vis_burden"] = burden.reindex(daily.index) if len(burden) else np.nan
    flags = sorted({n for n in num[num["catl"] == "experience"]["name"] if n.lower() not in ("crash", "period", "infection")})
    info = (f"{raw['date'].nunique()} days from {raw['date'].min():%b %d, %Y} to {raw['date'].max():%b %d, %Y}; "
            f"{len(sym_cat)} symptom trackers in {len(set(sym_cat.values()))} categories"
            + (f"; extra experience flags: {', '.join(flags)}" if flags else "")
            + (f"; pace points on {int(daily['vis_pace'].notna().sum())} days" if daily["vis_pace"].notna().any() else ""))
    return {"daily": daily, "symptoms": mat, "sym_cat": sym_cat, "scale": scale, "notes": notes, "info": info}


def visible_full_tips(vis, idx):
    """Every Visible symptom logged for the day (value above 0) plus the full note, for the calendar hover."""
    mat = vis["symptoms"]
    out = []
    for d in idx:
        parts = []
        if len(mat) and d in mat.index:
            row = mat.loc[d].dropna()
            row = row[row > 0].sort_values(ascending=False)
            if len(row):
                parts.append("Visible symptoms: " + ", ".join(f"{n} {int(round(v))}" for n, v in row.items()))
        if d in vis["notes"].index:
            parts.append("Note: " + vis["notes"][d][:300])
        out.append(" | ".join(parts))
    return out


def visible_tooltips(vis, idx):
    """Per-day hover text: the symptoms rated 2+ (scale-aware) and the Visible note, for any tracker list."""
    mat = vis["symptoms"]
    tips = []
    for d in idx:
        parts = []
        if len(mat) and d in mat.index:
            row = mat.loc[d].dropna()
            top = row[row >= max(2.0, vis["scale"] * 2 / 3)].sort_values(ascending=False).head(4)
            if len(top):
                parts.append("; ".join(f"{n} {int(v)}" for n, v in top.items()))
        if d in vis["notes"].index:
            parts.append("Note: " + vis["notes"][d][:110])
        tips.append(" | ".join(parts))
    return tips


# ----------------------------------------------------------------- baselines, stability, flares, naps
def anchored_z(series, floor, good_high, log=False):
    """Flare-resistant personal baseline. HRV is log-transformed (lnRMSSD is the usual scale in HRV research because raw RMSSD is
    skewed). The baseline is the previous BASELINE_LONG days (today excluded) at quantile ANCHOR_Q (or 1-ANCHOR_Q), not the median,
    so a run of bad days cannot drag your 'normal' down with it. Returns base/lo/hi in the series' own units plus the z-score."""
    s = np.log(series.where(series > 0)) if log else series
    prior = s.shift(1)
    roll = prior.rolling(BASELINE_LONG, min_periods=BASELINE_MIN)
    base = roll.quantile(ANCHOR_Q if good_high else 1 - ANCHOR_Q)
    sd = roll.std().clip(lower=floor)
    conv = np.exp if log else (lambda x: x)
    return pd.DataFrame({"base": conv(base), "lo": conv(base - BAND_SD * sd), "hi": conv(base + BAND_SD * sd), "z": (s - base) / sd})


def adverse_score(hrv_z=None, rhr_z=None, stress_z=None, sleep_z=None):
    """Direction-aware strain on a Visible-like scale: positive = worse than your usual. Only worse-than-usual HRV, resting HR,
    stress and sleep push it up; better-than-usual readings pull it down a little (30%), so a good day is not penalised.
    Weights are renormalised over whatever is available that day."""
    comps = [(hrv_z, -1, 0.45), (rhr_z, 1, 0.35), (stress_z, 1, 0.10), (sleep_z, -1, 0.10)]
    num = den = None
    for z, sign, w in comps:
        if z is None:
            continue
        v = sign * z
        v = v.where(v > 0, 0.3 * v)
        num = v.fillna(0) * w if num is None else num + v.fillna(0) * w
        den = v.notna() * w if den is None else den + v.notna() * w
    if num is None:
        return None
    core = (hrv_z.notna() if hrv_z is not None else False) | (rhr_z.notna() if rhr_z is not None else False)
    return (num / den.replace(0, np.nan)).where(core)


DEFAULT_CUTS = (-0.25, 0.25, 1.0, 2.0)      # adverse-score edges for stability 5|4, 4|3, 3|2, 2|1 when there is no Visible history


def calibrate_cuts(adverse, vis_stab):
    """Matches the share of days at each stability level to YOUR Visible history, so the estimate lands on Visible's scale."""
    ok = adverse.notna() & vis_stab.notna()
    if ok.sum() < 30:
        return DEFAULT_CUTS, False
    shares = vis_stab[ok].round().value_counts(normalize=True)
    cum, run = [], 0.0
    for lvl in (5, 4, 3, 2):
        run += float(shares.get(lvl, 0))
        cum.append(min(max(run, 0.02), 0.98))
    cuts = [float(adverse[ok].quantile(c)) for c in cum]
    for i in range(1, 4):
        if cuts[i] <= cuts[i - 1]:
            cuts[i] = cuts[i - 1] + 1e-6
    return tuple(cuts), True


def to_stability(adverse, cuts):
    return pd.cut(adverse, [-np.inf, *cuts, np.inf], labels=[5, 4, 3, 2, 1]).astype(float)


def detect_daytime_naps(hr_by_date, rhr, wake_by_date, stress_tl, sleep_windows=()):
    """Daytime rest that looks like a nap: heart rate down at your resting level for NAP_MIN_MINUTES or more, between
    NAP_HOURS, after you were up for 45 minutes, with low stress when stress data exists. This is a guess from heart rate: quiet
    sitting can look the same, so treat it as 'possible nap'. Log naps in symptoms.csv (nap = 1) to overrule it."""
    out = {}
    r_med = rhr.rolling(14, min_periods=3).median()
    for d, pts in hr_by_date.items():
        k = pd.Timestamp(d)
        r = rhr.get(k, np.nan)
        r = r_med.get(k, np.nan) if pd.isna(r) else r
        if pd.isna(r) or not pts:
            continue
        day0 = k.to_pydatetime()
        lo, hi = day0 + timedelta(hours=NAP_HOURS[0]), day0 + timedelta(hours=NAP_HOURS[1])
        if wake_by_date.get(d):
            lo = max(lo, wake_by_date[d] + timedelta(minutes=45))
        s = pd.Series({dt.datetime.fromtimestamp(t / 1000): v for t, v in pts}, dtype=float).sort_index()
        s = s[(s.index >= lo) & (s.index <= hi)]
        for a, b in sleep_windows:                          # time Garmin already recorded as sleep is not a nap
            s = s[(s.index < a - timedelta(minutes=15)) | (s.index > b + timedelta(minutes=45))]
        if len(s) < 12:
            continue
        low = (s.rolling(3, center=True, min_periods=2).median() <= r + NAP_HR_OFFSET).values
        idx = s.index
        runs, i = [], 0
        while i < len(s):
            if low[i]:
                j = i
                while j + 1 < len(s) and (low[j + 1] or (j + 2 < len(s) and low[j + 2])) and (idx[j + 1] - idx[j]).total_seconds() <= 420:
                    j += 1
                runs.append([idx[i], idx[j]])
                i = j + 1
            else:
                i += 1
        merged = []
        for a, b in runs:
            if merged and (a - merged[-1][1]).total_seconds() <= 600:
                merged[-1][1] = b
            else:
                merged.append([a, b])
        st = stress_tl.get(d) or []
        naps = []
        for a, b in merged:
            mins = (b - a).total_seconds() / 60 + 2
            if not NAP_MIN_MINUTES <= mins <= NAP_MAX_MINUTES:
                continue
            sv = [v for t, v in st if a <= dt.datetime.fromtimestamp(t / 1000) <= b]
            if len(sv) >= 3 and np.mean(sv) > 35:        # not calm enough to be asleep
                continue
            naps.append((a, mins))
        if naps:
            out[d] = {"min": float(sum(m for _, m in naps)), "n": len(naps), "first": naps[0][0].strftime("%H:%M")}
    return out


def detect_flares(f):
    """Flags days that look like a flare from several signals (each is a plain yes/no, so you can see why):
      body   - stability <= FLARE_STABILITY, HRV z <= FLARE_HRV_Z, or resting-HR z >= FLARE_RHR_Z (counts once; a second point
               if two of the three agree)
      crash  - you logged a crash (Visible or symptoms.csv pem)
      nap    - a daytime nap (detected or logged)
      symptoms - symptom burden >= FLARE_SYMPTOM_Z SD above your usual
      you    - you said you are in a flare (flare = 1 in symptoms.csv, or the startup check-in); worth 3 points on its own
    2+ points (or a stability of FLARE_SOLO_STABILITY) = a flare day. Active = flare days on 2 of the last FLARE_WINDOW days (or 3+ points
    today); "Possible flare symptoms" = one flare day recently.
    "Clear" is only said when there is real evidence to say it: Visible HRV or stability, real HRV from the watch, logged symptoms or a
    crash, or an answer from you within the last FLARE_WINDOW days. Resting heart rate alone cannot see a flare, so without any of those the
    status is "unknown" (shown as "Not enough data") rather than a false all-clear.
    This is pattern tracking for pacing and for your doctors, not a diagnosis."""
    b_stab = (f["stability"] <= FLARE_STABILITY).fillna(False)
    b_hrv = (f["hrv_z"] <= FLARE_HRV_Z).fillna(False)
    b_rhr = (f["rhr_z"] >= FLARE_RHR_Z).fillna(False)
    body = b_stab.astype(int) + b_hrv.astype(int) + b_rhr.astype(int)
    crash = (f["pem"] == 1).fillna(False)
    nap = ((f["nap_min"] >= NAP_MIN_MINUTES) | (f["nap_logged"] == 1)).fillna(False)
    symp = (f["symptom_z"] >= FLARE_SYMPTOM_Z).fillna(False)
    you = (f["flare_manual"] == 1).fillna(False)
    score = ((body >= 1).astype(int) + (body >= 2).astype(int) + crash.astype(int) + nap.astype(int) + symp.astype(int) + 3 * you.astype(int))
    has = f[["stability", "hrv_z", "rhr_z", "pem", "nap_min", "symptom_z", "flare_manual"]].notna().any(axis=1)
    score = score.where(has)
    day = ((score >= FLARE_DAY_POINTS) | (f["stability"] <= FLARE_SOLO_STABILITY)).fillna(False)
    recent = day.astype(int).rolling(FLARE_WINDOW, min_periods=1).sum()
    status = pd.Series("clear", index=f.index)
    status[recent >= 1] = "watch"
    status[(recent >= 2) | (score >= 3)] = "active"
    # evidence that makes a "Clear" trustworthy
    real_hrv = f["hrv"].notna() if f.attrs.get("hrv_src") == "garmin" else pd.Series(False, index=f.index)
    evidence = (f["vis_hrv"].notna() | f["vis_stab"].notna() | real_hrv | f["symptoms"].notna() | f["pem"].notna() | f["flare_manual"].notna())
    recent_evidence = evidence.astype(int).rolling(FLARE_WINDOW, min_periods=1).sum() >= 1
    status[(~recent_evidence) & (status != "active")] = "unknown"
    why = []
    for i in range(len(f)):
        r = []
        if you.iloc[i]: r.append("you reported a flare")
        if b_stab.iloc[i]: r.append("low stability")
        if b_hrv.iloc[i]: r.append("low HRV")
        if b_rhr.iloc[i]: r.append("high resting HR")
        if crash.iloc[i]: r.append("crash logged")
        if nap.iloc[i]: r.append("daytime nap")
        if symp.iloc[i]: r.append("symptoms up")
        why.append(", ".join(r))
    return score, day, status, why


VIS_COLS = ["vis_hrv", "vis_rhr", "vis_stab", "vis_sleep", "vis_crash", "vis_period", "vis_infection", "vis_active", "vis_funcap", "vis_burden", "vis_pace", "vis_pace_limit"]


def load_symptom_text(idx):
    """discharge and period_symptoms (free text) from symptoms.csv, aligned to idx."""
    out = pd.DataFrame("", index=idx, columns=["discharge", "period_symptoms"])
    try:
        if SYMPTOMS_CSV.exists():
            d = pd.read_csv(SYMPTOMS_CSV, dtype=str, keep_default_na=False)
            d["date"] = pd.to_datetime(d["date"], errors="coerce")
            d = d.dropna(subset=["date"]).drop_duplicates("date", keep="last").set_index("date")
            for c in out.columns:
                if c in d:
                    out[c] = d[c].reindex(idx).fillna("").astype(str).str.strip()
    except Exception as e:
        log(f"Could not read the discharge/symptom columns of symptoms.csv: {e}")
    return out


def _walk(o, path=""):
    yield path, o
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _walk(v, path + "." + str(k).lower())
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v, path + "[]")


def _names(v):
    """Strings out of a Garmin value that may be a string, a number, a dict or a list of those."""
    out = []
    if isinstance(v, str):
        out.append(v)
    elif isinstance(v, dict):
        for k in ("name", "displayName", "type", "symptomType", "title", "value", "key"):
            if isinstance(v.get(k), str):
                out.append(v[k]); break
    elif isinstance(v, list):
        for x in v:
            out += _names(x)
    return out


def parse_menstrual(M, idx):
    """Best-effort read of whatever Garmin's cycle-tracking pages returned (stored raw in menstrual.json). The exact layout is not documented, so this
    looks for periods, flow, symptoms, mood and discharge by name instead of by position. Returns a frame on idx and a short summary line."""
    cols = ["g_period", "g_flow", "g_symptoms", "g_mood", "g_discharge"]
    out = pd.DataFrame({"g_period": np.nan, "g_flow": "", "g_symptoms": "", "g_mood": "", "g_discharge": ""}, index=idx)
    if not isinstance(M, dict) or not (M.get("days") or M.get("calendar")):
        return out, ""
    today = idx[-1]
    for d, raw in (M.get("days") or {}).items():
        try:
            k = pd.Timestamp(d)
        except Exception:
            continue
        if k not in out.index or not raw:
            continue
        syms, mood, disc, flow, per, predicted = [], [], [], [], False, False
        ds = raw.get("daySummary") if isinstance(raw, dict) else None
        if isinstance(ds, dict):
            sd = ds.get("startDate")
            if isinstance(sd, str) and re.match(r"\d{4}-\d{2}-\d{2}", sd) and not ds.get("predictedCycle"):
                kk = pd.Timestamp(sd[:10])
                if kk in out.index and kk <= today:
                    out.loc[kk, "g_period"] = 1.0                    # the day Garmin counts as day 1 of the cycle
            if d == max(M["days"]):
                out.attrs["summary"] = {key: ds.get(key) for key in ("startDate", "dayInCycle", "periodLength", "predictedCycleLength", "cycleType")}
        for path, v in _walk(raw):
            leaf = path.rsplit(".", 1)[-1].rstrip("[]")
            if "predict" in leaf and v is True:
                predicted = True
            if "symptom" in path and isinstance(v, (str, list, dict)) and not isinstance(v, bool):
                syms += _names(v) if not isinstance(v, dict) or len(v) < 6 else []
            elif "mood" in path and isinstance(v, (str, list)):
                mood += _names(v)
            elif ("discharge" in path or "mucus" in path) and isinstance(v, (str, list)):
                disc += _names(v)
            elif ("flow" in leaf or "bleed" in leaf) and isinstance(v, (str, int, float)) and not isinstance(v, bool):
                if str(v).strip().lower() not in ("", "0", "none", "no_flow", "null"):
                    flow.append(str(v)); per = True
            elif leaf in ("isperiod", "periodday", "onperiod", "isperiodday") and v is True:
                per = True
            elif leaf in ("currentphase", "phase", "phasetype") and isinstance(v, str) and ("menstr" in v.lower() or v.lower() in ("period", "bleeding")):
                per = per or not predicted
        clean = lambda xs: ", ".join(dict.fromkeys(x.strip().replace("_", " ").lower() for x in xs if x and x.strip()))
        if per and not predicted:
            out.loc[k, "g_period"] = 1.0
        out.loc[k, "g_flow"], out.loc[k, "g_symptoms"], out.loc[k, "g_mood"], out.loc[k, "g_discharge"] = clean(flow), clean(syms), clean(mood), clean(disc)
    for path, v in _walk(M.get("calendar") or {}):
        if isinstance(v, dict) and not any("predict" in str(k).lower() and val is True for k, val in v.items()):
            st = next((val for k, val in v.items() if "start" in str(k).lower() and isinstance(val, str) and re.match(r"\d{4}-\d{2}-\d{2}", val)), None)
            ln = next((val for k, val in v.items() if "period" in str(k).lower() and "length" in str(k).lower() and isinstance(val, (int, float))), None)
            if st and ln and 0 < ln <= 14:
                for k in pd.date_range(pd.Timestamp(st[:10]), periods=int(ln)):
                    if k in out.index and k <= today:
                        out.loc[k, "g_period"] = 1.0
    n_p = int((out["g_period"] == 1).sum())
    n_s, n_m, n_d = int((out["g_symptoms"] != "").sum()), int((out["g_mood"] != "").sum()), int((out["g_discharge"] != "").sum())
    return out, f"Garmin cycle tracking: {n_p} period days, {n_s} days with symptoms, {n_m} with mood, {n_d} with discharge."


def fetch_menstrual(g, M, start, end, progress):
    """Pulls Garmin's cycle-tracking calendar and daily pages into menstrual.json (raw), so nothing has to be fetched twice."""
    days = M.setdefault("days", {})
    today = date.today().isoformat()
    if M.get("_none") and (date.today() - date.fromisoformat(M["_none"])).days < 7 and not days:
        return
    cal_fn, day_fn = getattr(g, "get_menstrual_calendar_data", None), getattr(g, "get_menstrual_data_for_date", None)
    got = False
    if cal_fn:
        progress.update("Fetching Garmin cycle tracking...", 86)
        chunks, a0 = [], start
        while a0 <= end:                                        # Garmin allows at most 92 days per call, so ask in 90-day pieces
            a1 = min(a0 + timedelta(days=89), end)
            c = _call(cal_fn, a0.isoformat(), a1.isoformat())
            if c:
                chunks.append(c)
            a0 = a1 + timedelta(days=1)
        if chunks:
            M["calendar"], got = {"chunks": chunks}, True
    if day_fn:
        want = [(start + timedelta(days=i)).isoformat() for i in range(DAYS + 1)]
        todo = [d for d in want if d not in days or d >= (end - timedelta(days=2)).isoformat()]
        misses = 0
        for n, d in enumerate(reversed(todo)):                 # newest first
            progress.update("Fetching Garmin cycle tracking...", 86 + 3 * n / max(1, len(todo)), d)
            r = _call(day_fn, d)
            if r is None:
                misses += 1
                if misses >= 3 and not got and not days:
                    break                                       # probably no cycle tracking on this account
                continue
            days[d] = r
            got = True
    if not got and not days:
        M["_none"] = today
        log("Garmin returned no cycle-tracking data for this account, so only Visible and your own entries are used for periods.")
    else:
        M.pop("_none", None)



def infer_cycle(idx, logged, disc=None, today=None):
    """Turns sparse period logs into whole periods, cycle lengths and a cycle phase for every day.
    idx may reach back further than the dashboard window so older cycles count. logged: 1 = period/spotting day recorded (by you, Garmin or Visible),
    0 = you said no, NaN = not logged. disc: optional text per day (cervical mucus). A run of logged days is one period (gaps of up to 8 days join),
    carried forward for the usual length, or through today while you keep logging it; a later 'no' ends it.
    Completed cycles use their own length (ovulation is about 14 days before the next period starts); the current cycle uses your typical length.
    Phases are estimates from the calendar, not measured ovulation."""
    nan = lambda: pd.Series(np.nan, index=idx)
    out = {"period": nan(), "period_est": pd.Series(False, index=idx), "cycle_day": nan(), "phase": pd.Series(None, index=idx, dtype=object),
           "cycle_id": nan(), "premens": pd.Series(False, index=idx)}
    info = {"episodes": [], "cycle_len": CYCLE_LENGTH_DEFAULT, "cycle_len_src": "default", "period_len": PERIOD_LENGTH_DEFAULT,
            "next_start": None, "next_range": None, "starts": [], "gaps": [], "ov_day": None, "ov_src": "calendar", "stats": None}
    ones = list(logged.index[logged == 1])
    if not ones:
        return out, info
    today = today if today is not None else idx[-1]
    eps, cur = [], [ones[0]]
    for d in ones[1:]:
        if (d - cur[-1]).days <= 8:
            cur.append(d)
        else:
            eps.append(cur)
            cur = [d]
    eps.append(cur)
    lens = [(e[-1] - e[0]).days + 1 for e in eps if len(e) >= 4 and (today - e[-1]).days > 2 and (e[-1] - e[0]).days <= 9]
    plen = int(np.clip(round(float(np.median(lens))), 3, 8)) if lens else PERIOD_LENGTH_DEFAULT
    info["period_len"] = plen
    per = pd.Series(0.0, index=idx)
    est = pd.Series(False, index=idx)
    starts = []
    for e in eps:
        start, last = e[0], e[-1]
        end = max(last, start + pd.Timedelta(days=plen - 1))
        if (today - last).days <= 1:
            end = max(end, min(today, start + pd.Timedelta(days=10)))
        end = min(end, today)
        d = start
        while d <= end:
            if d > last and logged.get(d, np.nan) == 0:
                end = d - pd.Timedelta(days=1)
                break
            d += pd.Timedelta(days=1)
        for d in pd.date_range(start, end):
            if d in per.index:
                per[d] = 1.0
                if logged.get(d, np.nan) != 1:
                    est[d] = True
        starts.append(start)
        info["episodes"].append({"start": start, "end": end, "logged_days": len(e), "length": (end - start).days + 1})
    out["period"], out["period_est"] = per, est
    gaps = [(a, b, (b - a).days) for a, b in zip(starts, starts[1:]) if 18 <= (b - a).days <= 60]   # longer gaps are probably unlogged periods
    info["gaps"] = gaps
    recent = [g[2] for g in gaps][-6:]
    if recent:
        L = int(round(float(np.median(recent))))
        info["cycle_len"], info["cycle_len_src"] = L, "your logs"
        allg = [g[2] for g in gaps]
        info["stats"] = {"n": len(allg), "mean": float(np.mean(allg)), "median": float(np.median(allg)), "min": min(allg), "max": max(allg),
                         "sd": float(np.std(allg)) if len(allg) > 1 else 0.0, "recent_min": min(recent), "recent_max": max(recent)}
    L = info["cycle_len"]
    last_start = starts[-1]
    lo, hi = (min(recent), max(recent)) if len(recent) >= 2 else (L, L)
    lo, hi = min(lo, L - 2), max(hi, L + 2)
    info["next_start"] = last_start + pd.Timedelta(days=L)
    info["next_range"] = (last_start + pd.Timedelta(days=lo), last_start + pd.Timedelta(days=hi))
    # per-cycle length and ovulation day
    cyc_len, ov_by = {}, {}
    nxt = {a: b for a, b in zip(starts, starts[1:])}
    for a in starts:
        done = a in nxt and 18 <= (nxt[a] - a).days <= 60
        Lc = (nxt[a] - a).days if done else L
        cyc_len[a] = (Lc, done)
        ov = max(Lc - LUTEAL_DAYS, plen + 3)
        src = "calendar"
        if disc is not None:                                       # cervical mucus: the last wet, stretchy day is close to ovulation
            seg = disc[(disc.index >= a) & (disc.index < a + pd.Timedelta(days=Lc))].fillna("").str.lower()
            peak = seg[seg.str.contains("egg|stretch|clear", regex=True)]
            if peak.empty:
                peak = seg[seg.str.contains("water", regex=True)]
            if len(peak):
                ov, src = int((peak.index[-1] - a).days) + 1, "discharge"
        ov_by[a] = (ov, src)
    info["ov_day"], info["ov_src"] = ov_by[last_start]
    st = pd.Series(idx.where(idx.isin(starts)), index=idx).ffill()
    cd = (idx.to_series() - st).dt.days + 1
    cd[st.isna()] = np.nan
    cd[cd > 60] = np.nan
    cid = st.where(cd.notna()).map(lambda v: v.toordinal() if pd.notna(v) else np.nan)
    phase, prem = [], []
    for d, c, s0 in zip(idx, cd, st):
        if pd.isna(c):
            phase.append(None); prem.append(False); continue
        Lc, done = cyc_len[s0]
        ov = ov_by[s0][0]
        ph = "Menstrual" if (per.get(d, 0) == 1 or c <= plen) else "Follicular" if c <= ov - 2 else "Ovulation window" if c <= ov + 1 else "Luteal"
        phase.append(ph)
        prem.append(bool(done and c > Lc - 5))
    out["cycle_day"], out["cycle_id"] = cd, cid
    out["phase"] = pd.Series(phase, index=idx, dtype=object)
    out["premens"] = pd.Series(prem, index=idx)
    info["starts"] = starts
    return out, info


def build_frame(raw, start, end, visible=None):
    idx = pd.date_range(start, end, freq="D", name="date")
    f = pd.DataFrame(index=idx)
    f["rhr"] = _series(raw["stats"], "rhr", idx)
    f["stress"] = _series(raw["stats"], "stress", idx)
    f["resp"] = _series(raw["stats"], "resp", idx)
    f["steps"] = _series(raw["stats"], "steps", idx)
    f["imin"] = _series(raw["stats"], "imin", idx)
    f["hrv"] = _series(raw["hrv"], "hrv", idx)
    f.attrs["hrv_src"] = "garmin"
    vd = visible["daily"] if visible else None
    for c in VIS_COLS:                                   # Visible columns (all NaN when no file was imported)
        f[c] = vd[c].reindex(idx) if visible else np.nan
    wide = pd.date_range(min(idx[0], vd.index.min()), idx[-1], freq="D") if visible and len(vd) else idx
    use_visible_hrv = f["vis_hrv"].notna().sum() >= VISIBLE_MIN_HRV_DAYS
    if not any(v for v in raw["sleep"].values()):
        log("No Garmin sleep stages were found, so sleep is estimated from heart rate and shown without stages.")

    rows = {}
    for d, s in raw["sleep"].items():
        if not s:
            continue
        on = dt.datetime.fromtimestamp(s["onset_ms"] / 1000, tz=dt.timezone.utc).replace(tzinfo=None)
        off = dt.datetime.fromtimestamp(s["offset_ms"] / 1000, tz=dt.timezone.utc).replace(tzinfo=None)
        h = lambda k: (s.get(k) or 0) / 3600.0
        rows[d] = {"onset": on, "offset": off, "sleep_h": h("asleep_s"), "deep_h": h("deep_s"),
                   "light_h": h("light_s"), "rem_h": h("rem_s"), "awake_h": h("awake_s"),
                   "score": s.get("score"), "src": "garmin"}
    hr_pts = raw["hr"]
    for d, rec in detect_sleep_fallback(hr_pts, f["rhr"], set(rows)).items():
        rows[d] = rec
    overrides = load_sleep_overrides()
    if overrides:
        rows = apply_sleep_overrides(rows, overrides)
        n_fixed = sum(1 for d in overrides if rows.get(d, {}).get("src") == "manual" and pd.Timestamp(d) in idx)
        if n_fixed:
            log(f"{n_fixed} night(s) use sleep times you corrected in symptoms.csv instead of Garmin's.")
    f["sleep_h"] = f["deep_h"] = f["rem_h"] = f["light_h"] = f["awake_h"] = f["sleep_score"] = np.nan
    f["bed"] = f["wake"] = f["sleep_src"] = ""
    for d, r in rows.items():
        k = pd.Timestamp(d)
        if k not in f.index:
            continue
        for col, key in (("sleep_h", "sleep_h"), ("deep_h", "deep_h"), ("rem_h", "rem_h"), ("light_h", "light_h"),
                         ("awake_h", "awake_h"), ("sleep_score", "score")):
            if r.get(key) is not None:
                f.loc[k, col] = r[key]
        f.loc[k, "bed"], f.loc[k, "wake"], f.loc[k, "sleep_src"] = hhmm(r["onset"]), hhmm(r["offset"]), r["src"]
    if f["sleep_src"].isin(["est", "manual"]).any():     # stages unknown for estimated or corrected nights
        f.loc[f["sleep_src"].isin(["est", "manual"]), ["deep_h", "rem_h", "light_h"]] = np.nan
    f.attrs["has_rem"] = bool((f["rem_h"].fillna(0) > 0).any())     # some watches (e.g. Forerunner 735XT) never report REM
    f["night_stress"] = f["night_move"] = np.nan                    # inputs to the dashboard's own sleep score
    for d, r in rows.items():
        k = pd.Timestamp(d)
        if k not in f.index or not r.get("onset") or not r.get("offset"):
            continue
        on, off = r["onset"], r["offset"]
        days = [(k - pd.Timedelta(days=1)).strftime("%Y-%m-%d"), d]
        st = [v for day in days for t, v in raw.get("stresstl", {}).get(day, []) if on <= dt.datetime.fromtimestamp(t / 1000) <= off]
        if len(st) >= 10:
            f.loc[k, "night_stress"] = float(np.mean(st))
        mv = [lv for _, lv in ((raw.get("sleep", {}).get(d) or {}).get("movement") or [])]
        if len(mv) >= 30:
            f.loc[k, "night_move"] = float(np.mean(mv))

    if f["hrv"].notna().sum() < 14:       # no usable HRV from the watch: build the best estimate from what we have
        windows = {d: (r["onset"], r["offset"]) for d, r in rows.items()}
        est, cdf = estimate_hrv(raw, windows, idx)
        f["hrv_c_stress"], f["hrv_c_steady"], f["hrv_c_low_hr"] = cdf["stress"], cdf["steady"], cdf["low_hr"]
        if est.notna().any():
            f["hrv"], f.attrs["hrv_src"] = est, "estimate"
            if not use_visible_hrv:
                log("Your watch did not provide overnight HRV, so the HRV panel shows an estimate (relative index, 50 = your typical night) "
                    "built from overnight stress, how steady your sleeping heart rate is, and how low it sits. It is not RMSSD in milliseconds.")
        elif not use_visible_hrv:
            log("No overnight HRV from Garmin and not enough overnight stress or heart-rate data to estimate it yet.")
    f["hrv_alt"], alt_src = f["hrv"], f.attrs["hrv_src"]      # the watch-based series (Garmin HRV or the estimate)
    f["hrv_filled"] = False
    if use_visible_hrv:
        f["hrv"], f.attrs["hrv_src"] = f["vis_hrv"], "visible"
        fill, r_ = fill_hrv_from_watch(f["vis_hrv"], f["hrv_alt"], log_alt=(alt_src == "garmin"))
        if fill is not None:
            gap = f["vis_hrv"].isna() & fill.notna()
            f["hrv"] = f["vis_hrv"].where(~gap, fill)
            f["hrv_filled"] = gap
            log(f"HRV is Visible's morning reading in ms ({int(f['vis_hrv'].notna().sum())} days in this window). On {int(gap.sum())} days with no Visible reading, "
                f"your overnight watch data was used to estimate it (scaled to your Visible readings; the two agreed with correlation {r_:.2f} on days you have both). "
                "Estimated days are drawn as hollow markers.")
        else:
            log(f"HRV is Visible's morning reading in ms ({int(f['vis_hrv'].notna().sum())} days in this window). Days without a Visible reading are left blank because "
                "the overnight watch data did not track your Visible readings closely enough to estimate from (needs at least 6 days with both and a clear match).")
    elif visible:
        log("The Visible file has fewer than %d HRV readings in this window, so Visible HRV was not used." % VISIBLE_MIN_HRV_DAYS)
    pace_windows = [(r["onset"], r["offset"], d) for d, r in rows.items() if r.get("onset") and r.get("offset")]
    pace = compute_pace(hr_pts, f["rhr"], pace_windows)
    pdf = pd.DataFrame.from_dict(pace, orient="index") if pace else pd.DataFrame(columns=["act", "over", "min_act", "min_over", "awake_min", "last", "avg_hr"])
    pdf.index = pd.to_datetime(pdf.index)
    pdf = pdf.reindex(idx)
    f["pace_asof"] = pdf["last"].fillna("")
    pdf = pdf.drop(columns=["last"]).astype(float)
    f["pace_act"], f["pace_over"], f["min_act"], f["min_over"], f["pace_awake_min"] = pdf["act"], pdf["over"], pdf["min_act"], pdf["min_over"], pdf["awake_min"]
    f["hr_avg"] = pdf["avg_hr"]
    f["spoons"] = f["pace_act"] + f["pace_over"]      # total pace points
    f.attrs["pace_src"] = "estimate"
    if visible and f["vis_pace"].notna().sum() >= VISIBLE_PACE_MIN_DAYS:        # Visible premium pace points replace the app's own estimate
        hv = f["vis_pace"].notna()
        f["pace_act"], f["pace_over"] = f["vis_pace"], pd.Series(np.where(hv, 0.0, np.nan), index=f.index)
        f["min_act"], f["min_over"], f["pace_asof"] = np.nan, np.nan, ""
        f["spoons"] = f["vis_pace"]
        f.attrs["pace_src"] = "visible"
        log(f"Pace points: using Visible's own numbers ({int(hv.sum())} days in this window, latest {f.index[hv][-1]:%b %d}); the app's heart-rate estimate is switched off.")
    elif visible and f["vis_pace"].notna().any():
        log(f"Visible pace points were found for only {int(f['vis_pace'].notna().sum())} days, so the app's own estimate is used.")
    wake_by_date = {d: r["offset"] for d, r in rows.items() if r.get("offset")}
    windows = [(r["onset"], r["offset"]) for r in rows.values() if r.get("onset") and r.get("offset")]
    det = detect_daytime_naps(hr_pts, f["rhr"], wake_by_date, raw.get("stresstl", {}), windows) if AUTO_NAP_DETECT else {}
    nap = pd.Series({pd.Timestamp(d): v["min"] for d, v in det.items()}, dtype=float).reindex(idx)
    g_nap = pd.Series({pd.Timestamp(d): (x.get("nap_s") or 0) / 60.0 for d, x in raw["sleep"].items() if x}, dtype=float).reindex(idx)
    nap = pd.concat([nap, g_nap.where(g_nap >= NAP_MIN_MINUTES)], axis=1).max(axis=1)
    if AUTO_NAP_DETECT:
        has_hr = pd.Series({pd.Timestamp(d): True for d in hr_pts}).reindex(idx).fillna(False).astype(bool)
        nap[nap.isna() & has_hr] = 0.0
    f["nap_min"] = nap
    f["nap_first"] = pd.Series({pd.Timestamp(d): v["first"] for d, v in det.items()}).reindex(idx).fillna("")
    f["p_mean"] = _series(raw["weather"], "mean", idx)
    f["p_change"] = f["p_mean"].diff()

    def put(key, z):
        f[key + "_base"], f[key + "_lo"], f[key + "_hi"], f[key + "_z"] = z["base"], z["lo"], z["hi"], z["z"]
        f[key + "_sd"] = (z["hi"] - z["lo"]) / (2 * BAND_SD)

    put("rhr", anchored_z(f["rhr"], 2.0, False))
    if f["steps"].notna().sum() >= 14:
        put("steps", anchored_z(f["steps"], 1500.0, True))
        f.loc[f.index[-1], "steps_z"] = np.nan         # today is only partly over
    if visible:                                           # Visible's morning resting HR only fills days Garmin has none
        vr = anchored_z(vd["vis_rhr"].reindex(wide), 2.0, False)["z"].reindex(idx)
        f["rhr_z"] = f["rhr_z"].fillna(vr)
    if f.attrs["hrv_src"] == "visible":
        put("hrv", anchored_z(vd["vis_hrv"].reindex(wide), 0.05, True, log=True).reindex(idx))
        alt_log = alt_src == "garmin"
        alt_z = anchored_z(f["hrv_alt"], 0.05 if alt_log else 4.0, True, log=alt_log)["z"]
        f["hrv_z"] = f["hrv_z"].fillna(0.6 * alt_z)       # watch-only estimate is a weaker signal, so it counts for less
    else:
        is_g = f.attrs["hrv_src"] == "garmin"
        put("hrv", anchored_z(f["hrv"], 0.05 if is_g else 4.0, True, log=is_g))
    put("stress", anchored_z(f["stress"], 4.0, False))
    f["sleep_z"] = anchored_z(f["sleep_score"], 5.0, True)["z"]

    weights = {"rhr_z": 0.5, "hrv_z": -0.3, "stress_z": 0.2}
    num = sum(f[c].fillna(0) * w for c, w in weights.items())
    den = sum(f[c].notna() * abs(w) for c, w in weights.items())
    f["strain"] = (num / den.replace(0, np.nan)).where(f["rhr_z"].notna() | f["hrv_z"].notna())
    adv = adverse_score(f["hrv_z"], f["rhr_z"], f["stress_z"], f["sleep_z"])
    cuts, calibrated = DEFAULT_CUTS, False
    if visible and vd["vis_stab"].notna().any():          # learn Visible's scale from your own history
        zh_w = anchored_z(vd["vis_hrv"].reindex(wide), 0.05, True, log=True)["z"]
        zr_w = anchored_z(vd["vis_rhr"].reindex(wide), 2.0, False)["z"]
        cuts, calibrated = calibrate_cuts(adverse_score(zh_w, zr_w), vd["vis_stab"].reindex(wide))
    f["stab_est"] = to_stability(adv, cuts) if adv is not None else np.nan
    has_v = f["vis_stab"].notna()
    f["stability"] = f["vis_stab"].where(has_v, f["stab_est"])
    f["stab_src"] = np.where(has_v, "visible", np.where(f["stab_est"].notna(), "estimate", ""))
    ov = f["stab_est"].notna() & has_v
    f.attrs["stab_calibrated"] = calibrated
    f.attrs["stab_match"] = (int(((f["stab_est"] - f["vis_stab"]).abs() <= 1)[ov].sum()), int(ov.sum()))

    man = load_symptoms(idx)
    f["symptoms"] = man["symptoms"].combine_first(f["vis_burden"])
    f["pem"] = man["pem"].combine_first(f["vis_crash"])
    first = [idx[0]]
    if visible and len(vd):
        first.append(vd.index.min())
    ext = pd.date_range(min(first), idx[-1], freq="D")
    gm, gm_line = parse_menstrual(raw.get("menstrual") if TRACK_PERIOD else None, ext)
    if gm_line:
        log(gm_line)
    f.attrs["garmin_cycle"] = gm.attrs.get("summary")
    man_ext = load_symptoms(ext)
    txt_ext = load_symptom_text(ext)
    vis_p = (vd["vis_period"].reindex(ext) if visible and len(vd) else pd.Series(np.nan, index=ext))
    logged_ext = man_ext["period"].combine_first(gm["g_period"].reindex(ext)).combine_first(vis_p.where(vis_p == 1))
    disc_ext = txt_ext["discharge"].where(txt_ext["discharge"] != "", gm["g_discharge"].reindex(ext).fillna(""))
    if TRACK_PERIOD:
        cyc, cinfo = infer_cycle(ext, logged_ext, disc_ext, today=idx[-1])
    else:
        cyc, cinfo = infer_cycle(ext, pd.Series(np.nan, index=ext))
    for k_ in ("period", "period_est", "cycle_day", "phase", "cycle_id", "premens"):
        f[k_] = cyc[k_].reindex(idx)
    f["period_est"] = f["period_est"].fillna(False).astype(bool)
    f["premens"] = f["premens"].fillna(False).astype(bool)
    f["mood"] = man["mood"]
    f["discharge"] = disc_ext.reindex(idx).fillna("")
    sx = txt_ext["period_symptoms"].where(txt_ext["period_symptoms"] != "", gm["g_symptoms"].reindex(ext).fillna(""))
    f["period_symptoms"] = sx.reindex(idx).fillna("")
    f["g_mood"] = gm["g_mood"].reindex(idx)
    f.attrs["cycle"] = cinfo
    f["stand_hr_rise"], f["nap_logged"], f["flare_manual"] = man["stand_hr_rise"], man["nap"], man["flare"]
    sy = vd["vis_burden"].reindex(wide) if visible else f["symptoms"].copy()
    sy.update(f["symptoms"])
    f["symptom_z"] = anchored_z(sy, 0.7, False)["z"].reindex(idx)
    if visible and len(visible["symptoms"]):               # your most-logged, varying symptoms become columns for the correlations
        m = visible["symptoms"].reindex(idx)
        keep = [c for c in m.columns if m[c].notna().sum() >= 15 and m[c].std() > 0]
        for c in sorted(keep, key=lambda c: -m[c].mean())[:8]:
            f["sym_" + c] = m[c]
    f["flare_score"], f["flare_day"], f["flare_status"], f["flare_why"] = detect_flares(f)
    # Daily pace ceiling: the upper end of your recent NON-flare days, lowered while flare signals are showing.
    usable = f["spoons"].where((~f["flare_day"]) & (f["pace_awake_min"] >= MIN_AWAKE_MINUTES))
    base = usable.shift(1).rolling(BASELINE_DAYS, min_periods=CEILING_MIN_DAYS).quantile(CEILING_QUANTILE)
    f["spoons_base"] = base
    adj = pd.Series(np.select([f["strain"] >= t for t, _ in CEILING_ADJUST], [a for _, a in CEILING_ADJUST], 1.0), index=f.index)
    adj = np.minimum(adj, f["flare_status"].map(FLARE_CEILING).fillna(1.0))
    f["pace_ceiling"] = base * adj
    if f.attrs.get("pace_src") == "visible" and f["vis_pace_limit"].notna().any():
        f["pace_ceiling"] = f["vis_pace_limit"].where(f["vis_pace_limit"].notna(), f["pace_ceiling"])
    f["tip"] = visible_tooltips(visible, idx) if visible else ""
    f["tip_full"] = visible_full_tips(visible, idx) if visible else ""
    return f


def latest(f, col, max_age=2):
    s = f[col].iloc[-(max_age + 1):].dropna()
    return (float(s.iloc[-1]), s.index[-1]) if len(s) else (np.nan, None)


INSIGHT_OUTCOMES = {   # key: (label, format, unit, which way is worse: +1 higher is worse, -1 lower is worse, 0 neutral)
    "rhr": ("resting heart rate", "{:.0f}", " bpm", 1), "hrv": ("HRV", "{:.0f}", "", -1), "strain": ("strain", "{:+.1f}", "", 1),
    "sleep_h": ("sleep", "{:.1f}", " h", -1), "spoons": ("pace points", "{:.0f}", "", 0), "stability": ("stability", "{:.1f}", "/5", -1),
    "flare": ("flare days", "{:.0f}", "%", 1),
}


def compute_insights(f):
    """Before-and-after comparisons: the average of a measure on days with a factor (a short night, a day over your ceiling, a pressure drop, a
    cycle phase) against all other days, same day or next day, with a rough Welch t-statistic. Returns (factor cards, factors with too few days, notes)."""
    n = len(f)
    known = f["flare_status"].ne("unknown")
    out_series = {k: f[k].astype(float) for k in ("rhr", "hrv", "strain", "sleep_h", "spoons", "stability")}
    flare = (f["flare_day"].fillna(False).astype(float) * 100.0).where(known)
    out_series["flare"] = flare
    notes = []
    if known.sum() < 15:
        out_series.pop("flare")
        notes.append(f"Flare-day comparisons are hidden: only {int(known.sum())} days have a known flare status. Import your Visible export and answer the daily flare question to unlock them.")
    if f["stab_src"].eq("visible").sum() < 15:
        out_series["stability"] = out_series["stability"].where(f["stab_src"] == "visible")
    over = (f["spoons"] > f["pace_ceiling"]).where(f["spoons"].notna() & f["pace_ceiling"].notna())
    short = (f["sleep_h"] < 6).where(f["sleep_h"].notna())
    drop = (f["p_change"] < PRESSURE_DROP_HPA).where(f["p_change"].notna())
    ph = f["phase"].where(f["phase"].notna())
    factors = [
        ("Days over your pace-point ceiling", over, (1,)),      # next day only: same-day heart rate would just restate the factor
        ("Short nights (under 6 hours)", short, (0, 1)),
        ("Pressure drops of 3+ hPa", drop, (0, 1)),
        ("Menstrual phase days", (ph == "Menstrual").where(ph.notna()), (0,)),
        ("Follicular phase days", (ph == "Follicular").where(ph.notna()), (0,)),
        ("Luteal phase days", (ph == "Luteal").where(ph.notna()), (0,)),
        ("Last 5 days before a period", f["premens"].astype(float).where(ph.notna()), (0,)),
    ]
    cards, thin = [], []
    for title, fac, lags in factors:
        fac = fac.astype(float)
        npres = int((fac == 1).sum())
        if npres < 4 or int((fac == 0).sum()) < 10:
            thin.append(f"{title} ({npres} day{'s' if npres != 1 else ''})")
            continue
        rows, quiet = [], []
        for key, ser in out_series.items():
            for lag in lags:
                y = ser.shift(-lag)
                d = pd.concat([fac, y], axis=1).dropna()
                a_, b_ = d[d.iloc[:, 0] == 1].iloc[:, 1], d[d.iloc[:, 0] == 0].iloc[:, 1]
                if len(a_) < 4 or len(b_) < 10:
                    continue
                diff = float(a_.mean() - b_.mean())
                se = math.sqrt(a_.var(ddof=1) / len(a_) + b_.var(ddof=1) / len(b_)) if len(a_) > 1 else np.nan
                t = diff / se if se and not np.isnan(se) and se > 0 else 0.0
                lab, fmt, unit, worse = INSIGHT_OUTCOMES[key]
                if title.startswith("Short nights") and key == "sleep_h" and lag == 0:
                    continue                                            # the factor is defined by this measure
                if key == "sleep_h":
                    nm_ = "sleep the night before" if lag == 0 else ("sleep the next night" if title.startswith("Short nights") else "sleep that night")
                else:
                    nm_ = ("next-day " if lag == 1 else "") + lab
                if key == "flare" and abs(diff) < 15:
                    t = min(abs(t), 1.0) * np.sign(t)
                verdict = "pattern" if abs(t) >= 2.0 else "maybe" if abs(t) >= 1.3 else ""
                row = {"label": nm_, "a": fmt.format(a_.mean()) + unit, "b": fmt.format(b_.mean()) + unit,
                       "diff": diff, "unit": (" pts" if unit == "%" and key == "flare" else unit), "t": t, "verdict": verdict, "worse": worse, "na": len(a_)}
                (rows if verdict else quiet).append(row)
        rows.sort(key=lambda r: -abs(r["t"]))
        cards.append({"title": title, "n": npres, "rows": rows, "quiet": sorted({q["label"] for q in quiet}), "score": max([abs(r["t"]) for r in rows] or [0])})
    cards.sort(key=lambda c: -c["score"])
    return cards, thin, notes


# ----------------------------------------------------------------- figure
def range_buttons(n_days):
    return [dict(count=7, label="1 week", step="day", stepmode="backward"),
            dict(count=14, label="2 weeks", step="day", stepmode="backward"),
            dict(count=30, label="30 days", step="day", stepmode="backward"),
            dict(count=60, label="60 days", step="day", stepmode="backward"),
            dict(count=int(n_days) + 1, label="All", step="day", stepmode="backward")]


def x_range(f):
    """Fixed axis range that ends with today, so the range buttons count back from today and never show future dates."""
    return [(f.index[0] - pd.Timedelta(hours=12)).isoformat(), (f.index[-1] + pd.Timedelta(hours=12)).isoformat()]


def build_sleep_figure(f):
    """Sleep history as its own chart: hours by stage (or estimated), dots colored by Garmin sleep score."""
    if not f["sleep_h"].notna().any():
        return None
    x = f.index
    fig = go.Figure()
    est = f["sleep_h"].where(f["deep_h"].isna())
    stages = [("deep_h", "Deep", DEEP)] + ([("rem_h", "REM", REM)] if f.attrs.get("has_rem") else []) + [("light_h", "Light", LIGHT), ("awake_h", "Awake", AWAKE)]
    for col, name, color in stages:
        fig.add_trace(go.Bar(x=x, y=f[col], name=name, marker_color=color, hovertemplate=name + " %{y:.1f}h"))
    fig.add_trace(go.Bar(x=x, y=est, name="Asleep (no stages)", marker_color=EST, hovertemplate="Asleep, estimated %{y:.1f}h"))
    tops = f[["sleep_h", "awake_h"]].fillna(0).sum(axis=1).where(f["sleep_h"].notna())
    tips = [f"Bed {b} to wake {w} | score {'' if pd.isna(sc) else int(sc)}{' (estimated)' if src == 'est' else ' (entered by you)' if src == 'manual' else ''}"
            + ("" if pd.isna(vs) else f" | Visible sleep rating {sleep_label(vs)}")
            for b, w, sc, src, vs in zip(f["bed"], f["wake"], f["sleep_score"], f["sleep_src"], f["vis_sleep"])]
    fig.add_trace(go.Scatter(x=x, y=tops + 0.5, mode="markers", name="Garmin sleep score",
                             marker=dict(size=8, color=f["sleep_score"], colorscale=[[0, WARN], [0.5, TYPICAL], [1, BETTER]],
                                         cmin=40, cmax=95, line=dict(width=0)),
                             customdata=tips, hovertemplate="%{customdata}", showlegend=False))
    fl_ = f.index[f["flare_day"].fillna(False)]
    if len(fl_):
        top_ = float(tops.max()) + 1.4 if tops.notna().any() else 10.0
        fig.add_trace(go.Scatter(x=fl_, y=[top_] * len(fl_), mode="markers", name="Flare day",
                                 marker=dict(symbol="diamond", size=10, color=WARN), hovertemplate="Flare day"))
    fig.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=TEXT, size=12), height=340,
                      margin=dict(l=55, r=20, t=110, b=50), barmode="stack", bargap=0.25, hovermode="x unified",
                      hoverlabel=dict(bgcolor="#0e1217"), legend=dict(orientation="h", x=0, xanchor="left", y=1.03, yanchor="bottom", bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
                      yaxis=dict(title="hours", rangemode="tozero", gridcolor=GRID, zerolinecolor=GRID))
    fig.update_xaxes(gridcolor=GRID, showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=1, spikecolor=MUTED, spikedash="dot",
                     range=x_range(f),
                     rangeselector=dict(bgcolor=PANEL, activecolor=GRID, font=dict(color=TEXT), x=1, xanchor="right", y=1 + 50 / 180, yanchor="bottom",
                                        buttons=range_buttons(len(f))))
    return fig


def pace_status(f):
    """Today's pace-point verdict: (level, headline, detail, color). level: over / near / room / none."""
    last = f.index[-1]
    v, d = latest(f, "spoons", 1)
    if pd.isna(v):
        return "none", "No activity data yet today", "Pace points need Garmin heart-rate data since you woke up.", MUTED
    ceil = f.loc[d, "pace_ceiling"]
    if pd.isna(ceil) or ceil <= 0:
        return "none", f"{v:.0f} pace points so far", "No ceiling yet: it needs about a week of ordinary, non-flare days to learn yours.", MUTED
    ratio, left = v / ceil, ceil - v
    vis_p = f.attrs.get("pace_src") == "visible"
    live = (" From Visible's own pace points." + ("" if d == last else f" Your latest Visible value is from {d:%b %d}; re-import your export for today's.")) if vis_p else \
           (f" Counted since you woke, as of {f.loc[d, 'pace_asof']}." if d == last and f.loc[d, "pace_asof"] else "")
    vis_lim = f.attrs.get("pace_src") == "visible" and not pd.isna(f.loc[d, "vis_pace_limit"])
    low = " Your ceiling is lowered today because of flare signals." if (f.loc[d, "flare_status"] in FLARE_CEILING and not vis_lim) else ""
    over_min = f.loc[d, "min_over"]
    ov_txt = f" About {over_min:.0f} minutes were in the over-exertion zone, which costs {OVEREXERT_MULT:.0f}x." if not pd.isna(over_min) and over_min >= 10 else ""
    if ratio > 1.0:
        return "over", "OVERDOING IT. REST!", f"{v:.0f} points used, {ratio * 100:.0f}% of today's ceiling of {ceil:.0f} (over by {-left:.0f}). Lie down or sit quietly for the rest of the day if you can.{ov_txt}{live}{low}", ALERT
    if ratio >= 0.8:
        return "near", "Close to your limit: slow down", f"{v:.0f} of {ceil:.0f} points ({ratio * 100:.0f}%), about {left:.0f} left. Pick one more thing at most, then rest.{ov_txt}{live}{low}", WATCH
    return "room", "Room left today", f"{v:.0f} of {ceil:.0f} points ({ratio * 100:.0f}%), about {left:.0f} left. Pace yourself and stop before the ceiling.{ov_txt}{live}{low}", BETTER


def build_exertion_html(f):
    """Garmin's intensity minutes so far today against a usual and a heavy day, plus yesterday and the last 7 days.
    Garmin counts a moderate minute once and a vigorous minute twice. Today is partial and says so."""
    if "imin" not in f or not f["imin"].notna().any():
        return ("<div class='panel muted'>No intensity minutes saved yet. They come from the same Garmin summary as your steps and are filled in "
                "on your next Garmin pull.</div>")
    tv = f["imin"].iloc[-1]
    prev = f["imin"].iloc[:-1].dropna()
    usual = float(prev.median()) if len(prev) >= 7 else np.nan
    heavy = float(prev.quantile(0.75)) if len(prev) >= 7 else np.nan
    yv = f["imin"].iloc[-2] if len(f) > 1 else np.nan
    wk = f["imin"].iloc[-8:-1].dropna()
    scale = max([x for x in (heavy * 1.6 if not pd.isna(heavy) else 0, (tv if not pd.isna(tv) else 0) + 5, 30) if not pd.isna(x)])
    head = ("<b>" + (f"{int(tv)}" if not pd.isna(tv) else "no data yet") + "</b> intensity minutes so far today")
    fill = "" if pd.isna(tv) else f"<i class='ex-fill' style='width:{min(tv / scale, 1) * 100:.0f}%;background:{SCORE_POOR if (not pd.isna(heavy) and tv > heavy) else '#7d6fd6'}'></i>"
    marks = ""
    if not pd.isna(usual):
        marks += f"<span class='ex-mk' style='left:{usual / scale * 100:.0f}%;border-color:#e4e2dc'></span>"
    if not pd.isna(heavy):
        marks += f"<span class='ex-mk' style='left:{heavy / scale * 100:.0f}%;border-color:{SCORE_POOR}'></span>"
    key = []
    if not pd.isna(usual):
        key.append(f"<span style='color:#e4e2dc'>|</span> a usual full day ({usual:.0f})")
    if not pd.isna(heavy):
        key.append(f"<span style='color:{SCORE_POOR}'>|</span> a heavy day ({heavy:.0f}+)")
    facts = []
    if not pd.isna(yv):
        facts.append(f"Yesterday: {int(yv)}")
    if len(wk):
        facts.append(f"Last 7 days average: {wk.mean():.0f}")
    return (f"<div class='panel'><div style='font-size:16px;margin-bottom:14px'>{head}</div>"
            f"<div class='ex-bar'>{fill}{marks}</div>"
            f"<div class='muted' style='margin-top:12px;font-size:13px'>{' &nbsp; '.join(key)}</div>"
            f"<div class='muted' style='margin-top:4px;font-size:13px'>{' &nbsp; '.join(facts)}</div>"
            f"<div class='muted' style='margin-top:12px;font-size:12px;line-height:1.5'>Garmin's own count of moderate and vigorous activity from your wrist heart rate and movement "
            f"(a vigorous minute counts twice). It is separate from the pace points above: pace points are measured against your resting heart rate, intensity minutes against fixed thresholds, "
            f"so the two can disagree. Today is not finished, and Garmin updates after your watch syncs. A usual day is your median day; a heavy day is heavier than three quarters of your days.</div></div>")


def build_pace_figure(f):
    """Pace points per day as stacked bars like the sleep chart: activity zone plus over-exertion, the daily ceiling, and a status dot above each bar."""
    if not f["spoons"].notna().any():
        return None
    x = f.index
    fig = go.Figure()
    if f.attrs.get("pace_src") == "visible":
        fig.add_trace(go.Bar(x=x, y=f["pace_act"], name="Pace points (Visible)", marker_color=BETTER, hovertemplate="Visible pace points %{y:.1f}"))
    else:
        fig.add_trace(go.Bar(x=x, y=f["pace_act"], name="Activity zone", marker_color=BETTER, customdata=f["min_act"],
                             hovertemplate="Activity %{y:.1f} pts (%{customdata:.0f} min)"))
    if f.attrs.get("pace_src") != "visible":
        fig.add_trace(go.Bar(x=x, y=f["pace_over"], name="Over-exertion (costs %dx)" % OVEREXERT_MULT, marker_color=ALERT, customdata=f["min_over"],
                             hovertemplate="Over-exertion %{y:.1f} pts (%{customdata:.0f} min)"))
    fig.add_trace(go.Scatter(x=x, y=f["pace_ceiling"], mode="lines+markers", name="Daily ceiling", line=dict(color=TEXT, width=1.5, dash="dash"),
                             marker=dict(size=4, color=TEXT), hovertemplate="ceiling %{y:.1f}"))
    tot = f["spoons"]
    ratio = tot / f["pace_ceiling"].where(f["pace_ceiling"] > 0)
    dot = [MUTED if pd.isna(r) else ALERT if r > 1.0 else WATCH if r >= 0.8 else BETTER for r in ratio]
    top = pd.concat([tot, f["pace_ceiling"]], axis=1).max(axis=1)
    tips = [("no ceiling yet" if pd.isna(r) else f"{r * 100:.0f}% of ceiling" + (": OVERDID IT" if r > 1.0 else ": close to limit" if r >= 0.8 else "")) for r in ratio]
    fig.add_trace(go.Scatter(x=x, y=top + max(float(top.max()) * 0.06, 1.5), mode="markers", name="Status", showlegend=False,
                             marker=dict(size=9, color=dot, line=dict(width=0)), customdata=tips, hovertemplate="%{customdata}"))
    lv = pace_status(f)
    if lv[0] == "over":
        fig.add_annotation(x=x[-1], y=float(top.iloc[-1]) + max(float(top.max()) * 0.2, 4), text="REST!", showarrow=False,
                           font=dict(color=ALERT, size=15, family="Segoe UI, sans-serif"))
    fig.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=TEXT, size=12), height=340,
                      margin=dict(l=55, r=20, t=110, b=50), barmode="stack", bargap=0.25, hovermode="x unified",
                      hoverlabel=dict(bgcolor="#0e1217"), legend=dict(orientation="h", x=0, xanchor="left", y=1.03, yanchor="bottom", bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
                      yaxis=dict(title="pace points", rangemode="tozero", gridcolor=GRID, zerolinecolor=GRID))
    fig.update_xaxes(gridcolor=GRID, showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=1, spikecolor=MUTED, spikedash="dot",
                     range=x_range(f), rangeselector=dict(bgcolor=PANEL, activecolor=GRID, font=dict(color=TEXT), x=1, xanchor="right", y=1 + 50 / 180,
                                                          yanchor="bottom", buttons=range_buttons(len(f))))
    return fig


def sleep_label(v):
    v = int(v)
    return f"{SLEEP_LABELS[v]} ({v})" if v in SLEEP_LABELS else f"code {v}"


def build_figure(f):
    panels = []
    if f["strain"].notna().any():
        panels.append(("strain", "Daily strain: 0 is your normal; higher means your body is working harder. Orange bars are 1.5 or more (clearly off)"))
    if f["stability"].notna().any():
        panels.append(("stability", "Stability (1 to 5, higher is steadier). Solid = Visible's own score, striped = estimated by the app. Orange = 2 or lower"))
    ev_any = bool(f["flare_day"].any() or (f["period"] == 1).any() or (f["p_change"] < PRESSURE_DROP_HPA).any())
    if ev_any:
        panels.append(("events", "Events: flare days, period days (open circle = estimated from your logs), pressure drops of 3 hPa or more"))
    if f["rhr"].notna().any():
        panels.append(("rhr", "Resting heart rate (bpm)" + (". Dot size = Garmin intensity minutes that day, amber = heavy day, ring = against your usual, hollow = today" if ("imin" in f and f["imin"].notna().sum() >= 7) else "")))
    if f["hrv"].notna().any():
        hs = f.attrs.get("hrv_src")
        panels.append(("hrv", {"estimate": "Overnight HRV estimate (index, 50 = your typical night, higher is better)",
                               "visible": "HRV from Visible (ms), higher is better. Hollow markers = estimated from overnight watch data on days with no Visible reading. Grey band = your flare-resistant normal range"}.get(hs, "Overnight HRV (ms), higher is better")))
    if f["stress"].notna().any():
        panels.append(("stress", "Average stress (0 to 100)"))
    if f["steps"].notna().sum() >= 14 and "steps_z" in f:
        panels.append(("steps", "Steps per day (higher is better; grey band = your usual range; today is only partly counted)"))
    if f["nap_min"].fillna(0).gt(0).any():
        panels.append(("nap", "Possible daytime naps (minutes of resting-level heart rate between 9 am and 7:30 pm)"))
    if f["p_change"].notna().any():
        panels.append(("pressure", "Barometric pressure change from the day before (hPa)"))
    if f["stand_hr_rise"].notna().any():
        panels.append(("stand", "Standing test: heart-rate rise after 10 minutes standing (bpm). 30+ is the adult POTS threshold"))
    if not panels:
        return go.Figure()
    n = len(panels)
    fig = make_subplots(rows=n, cols=1, shared_xaxes=True, vertical_spacing=0.035,
                        subplot_titles=[t for _, t in panels],
                        row_heights=[1.3 if k == "strain" else 0.62 if k == "events" else 1 for k, _ in panels])
    for a in fig.layout.annotations:
        a.update(x=0, xanchor="left", font=dict(size=13, color=TEXT))
    fig.update_xaxes(gridcolor=GRID, showspikes=True, spikemode="across", spikesnap="cursor", spikethickness=1,
                     spikecolor=MUTED, spikedash="dot")
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID)
    x = f.index

    def add(tr, row):
        fig.add_trace(tr, row=row, col=1)

    def band(row, base, lo, hi, color="rgba(141,150,163,0.14)"):
        add(go.Scatter(x=x, y=hi, mode="lines", line=dict(width=0), hoverinfo="skip", showlegend=False), row)
        add(go.Scatter(x=x, y=lo, mode="lines", line=dict(width=0), fill="tonexty",
                       fillcolor=color, hoverinfo="skip", showlegend=False), row)
        add(go.Scatter(x=x, y=base, mode="lines", line=dict(color=MUTED, width=1.5, dash="dot"), name="your usual",
                       hovertemplate="%{y:.1f}", showlegend=False), row)

    for row, (key, _) in enumerate(panels, start=1):
        if key == "strain":
            cols = [MUTED if pd.isna(v) else ALERT if v >= 2.5 else WARN if v >= 1.5 else "#7F90A8" for v in f["strain"]]
            add(go.Bar(x=x, y=f["strain"], marker_color=cols, name="Strain", hovertemplate="%{y:+.1f}",
                       showlegend=False), row)
            fig.add_hline(y=1.5, line=dict(color=WARN, width=1, dash="dot"), row=row, col=1)
            fig.update_yaxes(zeroline=True, zerolinecolor=TEXT, zerolinewidth=1, row=row, col=1)
        elif key == "stability":
            stv = f["stability"]
            est_ = (f["stab_src"] != "visible").values
            cols = [MUTED if pd.isna(v) else WARN if v <= 2 else "#7F90A8" for v in stv]
            recent_ = np.arange(len(stv)) >= len(stv) - 30
            txt = [("" if pd.isna(v) or not r_ else f"{int(v)}") for v, r_ in zip(stv, recent_)]
            add(go.Bar(x=x, y=stv, marker=dict(color=cols, pattern=dict(shape=["/" if e_ else "" for e_ in est_], bgcolor=PANEL, size=5, solidity=0.45)),
                       text=txt, textposition="outside", textfont=dict(size=10, color=TEXT), cliponaxis=False,
                       customdata=["estimated by the app" if e_ else "Visible's score" for e_ in est_],
                       name="Stability", hovertemplate="%{y:.0f}/5 (%{customdata})", showlegend=False), row)
            fig.update_yaxes(range=[0, 5.9], dtick=1, row=row, col=1)
        elif key == "nap":
            add(go.Bar(x=x, y=f["nap_min"], marker_color=WARN, customdata=f["nap_first"],
                       hovertemplate="%{y:.0f} min, from about %{customdata}", name="Nap", showlegend=False), row)
        elif key in ("rhr", "hrv", "stress", "steps"):
            sign = -1 if key in ("hrv", "steps") else 1
            cols = [zone(sign * v)[1] if not pd.isna(v) else MUTED for v in f[key + "_z"]]
            band(row, f[key + "_base"], f[key + "_lo"], f[key + "_hi"])
            hollow = f["hrv_filled"].values if key == "hrv" and "hrv_filled" in f else np.zeros(len(f), dtype=bool)
            if key == "rhr" and "imin" in f and f["imin"].notna().sum() >= 7:
                # intensity overlay: dot size = Garmin intensity minutes, amber = a heavy day (top quarter of your days),
                # ring colour = resting HR against your usual, hollow = today (not finished)
                im_ = f["imin"]
                heavy_ = float(im_.iloc[:-1].dropna().quantile(0.75))
                n_ = len(f)
                sizes = [7.0 if pd.isna(v) else float(np.clip(7 + v * 0.3, 7, 24)) for v in im_]
                fills = ["rgba(0,0,0,0)" if i == n_ - 1 else (MUTED if pd.isna(v) else "#e3b341" if v > heavy_ else "#7d6fd6") for i, v in enumerate(im_)]
                rings = ["#cfc8ff" if i == n_ - 1 else cols[i] for i in range(n_)]
                tips_ = ["" if pd.isna(v) else f"| {int(v)} intensity min" + (" so far (day not over)" if i == n_ - 1 else " (heavy day)" if v > heavy_ else "")
                         for i, v in enumerate(im_)]
                add(go.Scatter(x=x, y=f[key], mode="lines+markers", line=dict(color="rgba(228,226,220,0.35)", width=1),
                               marker=dict(size=sizes, color=fills, line=dict(width=[2.4 if i == n_ - 1 else 1.8 for i in range(n_)], color=rings)),
                               customdata=tips_, name="Resting HR", connectgaps=False, hovertemplate="%{y:.0f} bpm %{customdata}", showlegend=False), row)
            else:
                add(go.Scatter(x=x, y=f[key], mode="lines+markers", line=dict(color="rgba(228,226,220,0.35)", width=1),
                               marker=dict(size=7, color=[("rgba(0,0,0,0)" if h_ else c_) for c_, h_ in zip(cols, hollow)],
                                           line=dict(width=[1.6 if h_ else 0 for h_ in hollow], color=cols)),
                               customdata=["estimated from overnight data" if h_ else "Visible reading" if key == "hrv" else "" for h_ in hollow],
                               name={"rhr": "Resting HR", "hrv": "HRV", "stress": "Stress", "steps": "Steps"}[key],
                               connectgaps=False, hovertemplate="%{y:.0f} %{customdata}" if key == "hrv" else "%{y:.0f}", showlegend=False), row)
        elif key == "spoons":
            add(go.Bar(x=x, y=f["pace_act"], name="Activity zone", marker_color=WATCH, customdata=f["min_act"],
                       hovertemplate="Activity %{y:.1f} pts (%{customdata:.0f} min)", showlegend=False), row)
            add(go.Bar(x=x, y=f["pace_over"], name="Over-exertion", marker_color=ALERT, customdata=f["min_over"],
                       hovertemplate="Over-exertion %{y:.1f} pts (%{customdata:.0f} min)", showlegend=False), row)
            add(go.Scatter(x=x, y=f["pace_ceiling"], mode="lines", line=dict(color=TEXT, width=1.5, dash="dash"),
                           name="rough ceiling", hovertemplate="ceiling %{y:.1f}", showlegend=False), row)
        elif key == "events":
            rows_ = [("Flare", 3, "diamond", WARN, f["flare_day"].fillna(False).values, None),
                     ("Period", 2, "circle", PHASE_COLORS["Menstrual"], (f["period"] == 1).values, f["period_est"].values),
                     ("Pressure drop", 1, "triangle-down", "#AAB4C0", (f["p_change"] < PRESSURE_DROP_HPA).fillna(False).values, None)]
            for name, yv, sym, col, mask, est_ in rows_:
                if not mask.any():
                    continue
                full = mask if est_ is None else mask & ~est_
                for sel, symbol, fill in ((full, sym, col), (mask & est_ if est_ is not None else np.zeros(len(mask), bool), sym + "-open", col)):
                    if not sel.any():
                        continue
                    tips_ = [f"{name}" + (f" ({f.loc[d, 'phase']}, cycle day {int(f.loc[d, 'cycle_day'])})" if name == "Period" and pd.notna(f.loc[d, 'cycle_day']) else "")
                             + (f": {f.loc[d, 'flare_why']}" if name == "Flare" and f.loc[d, 'flare_why'] else "")
                             + (f": {f.loc[d, 'p_change']:+.1f} hPa" if name == "Pressure drop" else "")
                             + (" (estimated)" if symbol.endswith("-open") else "") for d in f.index[sel]]
                    if name == "Period":                                   # a plain red circle (the emoji drop did not render on every system)
                        add(go.Scatter(x=x[sel], y=[yv] * int(sel.sum()), mode="markers", name=name, showlegend=False,
                                       marker=dict(symbol="circle", size=11, color=PERIOD_RED, line=dict(width=0)),
                                       opacity=0.45 if symbol.endswith("-open") else 1.0,
                                       customdata=tips_, hovertemplate="%{customdata}"), row)
                        continue
                    add(go.Scatter(x=x[sel], y=[yv] * int(sel.sum()), mode="markers", name=name, showlegend=False,
                                   marker=dict(symbol=symbol, size=11, color=fill, line=dict(width=2, color=fill)),
                                   customdata=tips_, hovertemplate="%{customdata}"), row)
            fig.update_yaxes(range=[0.4, 3.6], tickvals=[1, 2, 3], ticktext=["Pressure", "Period", "Flare"], showgrid=False, row=row, col=1)
        elif key == "pressure":
            cols = ["#E4E2DC" if v < PRESSURE_DROP_HPA else "#9AA5B4" if v < -2 else "#4a5666" for v in f["p_change"].fillna(0)]
            add(go.Bar(x=x, y=f["p_change"], marker_color=cols, name="Pressure change", hovertemplate="%{y:+.1f} hPa",
                       showlegend=False), row)

        elif key == "symptoms":
            cols = [MUTED if pd.isna(v) else BETTER if v <= 3 else WATCH if v <= 6 else ALERT for v in f["symptoms"]]
            add(go.Bar(x=x, y=f["symptoms"], marker_color=cols, name="Symptoms", customdata=f["tip"],
                       hovertemplate="%{y:.1f}/10 %{customdata}", showlegend=False), row)
            pem = f["pem"] == 1
            add(go.Scatter(x=x[pem], y=[10.8] * int(pem.sum()), mode="markers", marker=dict(symbol="diamond", size=9, color=ALERT),
                           name="PEM day", hovertemplate="PEM day", showlegend=False), row)
            fig.update_yaxes(range=[0, 11.5], row=row, col=1)
        elif key == "stand":
            add(go.Scatter(x=x, y=f["stand_hr_rise"], mode="lines+markers", line=dict(color="rgba(228,226,220,0.35)", width=1),
                           marker=dict(size=8, color=[WARN if v >= 30 else BETTER for v in f["stand_hr_rise"].fillna(0)]),
                           name="Standing HR rise", connectgaps=True, hovertemplate="+%{y:.0f} bpm", showlegend=False), row)
            fig.add_hline(y=30, line=dict(color=WARN, width=1, dash="dash"), row=row, col=1)

    fig.update_layout(template="plotly_dark", paper_bgcolor=BG, plot_bgcolor=PANEL, font=dict(color=TEXT, size=12),
                      height=140 * n + 220, margin=dict(l=55, r=20, t=120, b=40), barmode="stack", bargap=0.25,
                      hovermode="x unified", hoverlabel=dict(bgcolor="#0e1217"))
    fig.update_xaxes(range=x_range(f))
    fig.update_xaxes(rangeselector=dict(bgcolor=PANEL, activecolor=GRID, font=dict(color=TEXT),
                     x=1, xanchor="right", y=1 + 60 / (140 * n + 60), yanchor="bottom", buttons=range_buttons(len(f))), row=1, col=1)
    return fig


# ----------------------------------------------------------------- html pieces
def _spark_data(series):
    ser = pd.Series(series, dtype=float) if not isinstance(series, pd.Series) else series.astype(float)
    t = ser.iloc[-14:]
    if t.notna().sum() < 2:
        return None
    prior = ser.iloc[:-1].dropna().iloc[-30:]
    base = float(prior.median()) if len(prior) >= 3 else float(t.dropna().median())
    sd = float(prior.std()) if len(prior) >= 3 and prior.std() > 0 else (float(t.dropna().std()) or 1.0)
    return t.to_numpy(), base, sd


def _spark_bars(series, color):
    """Style A: the last 14 days as bars, today in the card colour, a dashed line for your usual."""
    d = _spark_data(series)
    if d is None:
        return ""
    t, base, sd = d
    v = t[~np.isnan(t)]
    lo = v.min() - (v.max() - v.min()) * 0.3
    r = (v.max() - lo) or 1.0
    w = 230.0 / len(t)
    out = ["<svg viewBox='0 0 230 44' preserveAspectRatio='none' class='spark'><title>Last 14 days. Bars are each day, the coloured bar is today, the dashed line is your usual.</title>"]
    for k, a in enumerate(t):
        if np.isnan(a):
            continue
        h = max(2.0, (a - lo) / r * 38)
        out.append(f"<rect x='{k * w + w * 0.1:.1f}' y='{42 - h:.1f}' width='{w * 0.8:.1f}' height='{h:.1f}' rx='1.5' fill='{color if k == len(t) - 1 else '#3a4658'}'/>")
    y = 42 - (base - lo) / r * 38
    out.append(f"<line x1='0' x2='230' y1='{y:.1f}' y2='{y:.1f}' stroke='#8d96a3' stroke-dasharray='2 3' stroke-width='1' vector-effect='non-scaling-stroke'/></svg>")
    return "".join(out)


def _spark_dots(series, color, hb):
    """Style C: each of the last 14 days as a dot on a shaded band of your usual range. Unusual days are coloured
    (blue better, orange worse; grey if neither applies); today is ringed."""
    d = _spark_data(series)
    if d is None:
        return ""
    t, base, sd = d
    v = t[~np.isnan(t)]
    lo = min(v.min(), base - sd) - 0.3 * sd
    hi = max(v.max(), base + sd) + 0.3 * sd
    r = (hi - lo) or 1.0
    Y = lambda a: 40 - (a - lo) / r * 36
    w = 230.0 / len(t)
    out = ["<svg viewBox='0 0 230 44' class='spark'><title>Last 14 days. The shaded band is your usual range. Blue dots are better than usual, orange worse. The ringed dot is today.</title>"
           f"<rect x='0' y='{Y(base + sd):.1f}' width='230' height='{max(Y(base - sd) - Y(base + sd), 2):.1f}' rx='3' fill='#ffffff' opacity='.09'/>"]
    last = len(t) - 1
    for k, a in enumerate(t):
        if np.isnan(a):
            continue
        if abs(a - base) <= sd or hb is None:
            col = "#8d96a3"
        else:
            col = BETTER if ((a > base) == bool(hb)) else WARN
        out.append(f"<circle cx='{k * w + w / 2:.1f}' cy='{Y(a):.1f}' r='{4.6 if k == last else 3.6}' fill='{col}'/>")
        if k == last:
            out.append(f"<circle cx='{k * w + w / 2:.1f}' cy='{Y(a):.1f}' r='7.5' fill='none' stroke='#e6edf3' stroke-width='1.4'/>")
    return "".join(out) + "</svg>"


def spark(series, color, hb=None):
    """Both graph styles are drawn; a Settings choice (saved in the browser) shows one: C (dots on your usual band) or A (bars)."""
    a, c = _spark_bars(series, color), _spark_dots(series, color, hb)
    if not a:
        return ""
    return f"<span class='spA'>{a}</span><span class='spC'>{c}</span>"


HRV_TIP = ("Tip: take your HRV with the Visible app first thing after waking, before you move around much or take medicine, "
           "with a warm, dry finger on the camera. The same routine every day makes readings comparable.")


ALERT_LEVELS = {WATCH: (1, "\U0001F440", "WATCH", 3), WARN: (2, "\u26A0\uFE0F", "HIGH", 4), ALERT: (3, "\U0001F6D1", "ALERT", 5)}


def card(title, value, unit, sub, color, sp="", hint="", tip=""):
    """Summary card. Short text stays on the card; explanations (tip and hint) appear when you hover, marked by an info symbol."""
    unit_html = f"<span class='unit'>{unit}</span>" if unit else ""
    tt = " ".join(x for x in (tip, hint) if x)
    tt_attr = f" title=\"{_esc(tt, quote=True)}\"" if tt else ""
    icon = "<span class='ci'>&#9432;</span>" if tt else ""
    small = " style=\"font-size:19px;line-height:1.25\"" if len(str(value)) > 10 else ""
    lv = ALERT_LEVELS.get(color)
    lvl_attr = f" data-lv='{lv[0]}'" if lv else ""
    if lv:
        title = f"<span class='lve'>{lv[1]} </span>{title}<span class='lvt'>{lv[2]}</span>"
    return (f"<div class='card'{lvl_attr}{tt_attr} style='border-top:{lv[3] if lv else 3}px solid {color}'>{icon}<div class='ct'>{title}</div>"
            f"<div class='cv'{small}>{value}{unit_html}</div><div class='cs'>{sub}</div>{sp}</div>")


CARD_GROUPS = [("Right now", ("Flare status", "Pace points", "Sleep score", "Last sleep")),
               ("Body", ("Resting heart rate", "Overnight HRV", "HRV", "Stability", "Strain today", "Stress")),
               ("Cycle and other signals", ("Cycle phase", "Cycle flare", "Period", None))]
WIDE_CARDS = ("Flare status", "Sleep score")


def group_cards(cards):
    """Sorts the summary cards under small headings (Right now, Body, Sleep, Cycle, then anything else). Flare status and the sleep score are drawn wide."""
    def title(c):
        m = re.search(r"<div class='ct'>(.*?)</div>", c)
        t = m.group(1) if m else ""
        return re.sub(r"<span class='lv[et]'>.*?</span>", "", t)
    left, out = list(cards), []
    groups = list(CARD_GROUPS)
    for name, prefixes in groups:
        picked = []
        for pre in prefixes or [None]:
            for c in list(left):
                t = title(c)
                if (pre is None) or t.startswith(pre):
                    picked.append(c)
                    left.remove(c)
        if not picked:
            continue
        if name.startswith("Cycle") and not any(title(c).startswith(("Cycle", "Period")) for c in picked):
            name = "Other signals"
        html = []
        for c in picked:
            if title(c).startswith(WIDE_CARDS):
                c = c.replace("<div class='card'", "<div class='card wide'", 1)
            html.append(c)
        out.append(f"<div class='tg'><div class='tgh'><h3>{name}</h3><i></i></div><div class='cards'>{''.join(html)}</div></div>")
    return "".join(out)


def build_cards_and_story(f):
    last = f.index[-1]
    strain, _ = latest(f, "strain", 1)
    label, zc = zone(strain)
    tail = f.iloc[-14:]
    cards, notes = [], []

    s_txt = "no data" if pd.isna(strain) else f"{strain:+.1f}"
    cards.append(card("Strain today", s_txt, "", label, zc, spark(f["strain"], zc, False),
                      tip="Strain compares today's resting heart rate, HRV and stress with your own usual over the previous 60 days. 0 is your normal; higher means your body is working harder than usual. Orange starts at 1.5."))
    fl = f["flare_status"].iloc[-1]
    flc = {"active": ALERT, "watch": WARN, "clear": BETTER}.get(fl, MUTED)
    watch_only = f["vis_stab"].iloc[-FLARE_WINDOW:].isna().all() and f["vis_hrv"].iloc[-FLARE_WINDOW:].isna().all() and f.attrs.get("hrv_src") != "garmin"
    why = ", ".join(dict.fromkeys(w for row in f["flare_why"].iloc[-FLARE_WINDOW:] for w in row.split(", ") if w))
    flsub = {"active": f"flare days on 2 of the last {FLARE_WINDOW} days", "watch": f"a flare day in the last {FLARE_WINDOW} days",
             "clear": "no flare pattern right now",
             "unknown": "needs your Visible export or your answer"}.get(fl, "not enough data")
    said = "you reported a flare" in f["flare_why"].iloc[-1]
    if fl == "active" and said:
        flsub, why = "you told the app you are in a flare", ""
    fl_tip = ("A day counts as a flare day with 2 or more signals: low HRV, high resting HR, low stability, a crash, a nap, high symptoms, or you saying you are in a flare (3 points). "
              "Active = flare days on 2 of the last 4 days." + (f" Signals right now: {why}." if why and fl in ("active", "watch") else "")
              + (" Your watch has no HRV, so it can't see flares on its own: add your Visible export or answer the daily flare question." if fl == "unknown" else ""))
    cards.append(card("Flare status", {"active": "Active", "watch": "Possible flare symptoms", "clear": "Clear", "unknown": "Not enough data"}.get(fl, "No data"), "",
                      flsub, flc, spark(f["flare_score"], flc, False), tip=fl_tip))
    st, sd_ = latest(f, "stability", 1)
    if not pd.isna(st):
        sc_ = TYPICAL if st >= 4 else WATCH if st == 3 else WARN if st == 2 else ALERT
        src = f.loc[sd_, "stab_src"]
        sub = "from Visible" if src == "visible" else "estimated"
        st_tip = ("Visible's own stability score." if src == "visible" else "Estimated by the app from your HR, HRV, stress and sleep, calibrated to your Visible history when you have one.")
        if src != "visible" and watch_only:
            sc_, sub = MUTED, "watch-only guess"
            st_tip = "A rough guess from watch data only, so it can miss flares. Import your Visible export for the real score."
        cards.append(card("Stability (1 to 5)", f"{st:.0f}", "/5", sub, sc_, spark(f["stability"], sc_, True), tip=st_tip))

    v, d = latest(f, "rhr", 1)
    vv = f["vis_rhr"].iloc[-2:].dropna()
    vis_v, vis_d = (float(vv.iloc[-1]), vv.index[-1]) if len(vv) else (np.nan, None)
    avg_v = f["hr_avg"].iloc[-1] if "hr_avg" in f else np.nan
    if not pd.isna(v) or not pd.isna(vis_v):
        main = v if not pd.isna(v) else vis_v
        dd = d if not pd.isna(v) else vis_d
        base = f.loc[dd, "rhr_base"]
        diff = main - base if not pd.isna(base) else np.nan
        zz = f.loc[dd, "rhr_z"]
        c = zone(zz)[1] if not pd.isna(zz) else MUTED
        parts = []
        if not pd.isna(vis_v):
            parts.append(f"Visible morning {vis_v:.0f}" + ("" if vis_d == last else f" ({vis_d:%b %d})"))
        if not pd.isna(avg_v):
            parts.append(f"avg today {avg_v:.0f}")
        sub = " | ".join(parts) if parts else ("no baseline yet" if pd.isna(diff) else f"{abs(diff):.0f} bpm {'above' if diff > 0 else 'below'} usual")
        tip = ("Big number: Garmin's resting heart rate, its own all-day estimate (roughly your lowest sustained heart rate). Visible's is one reading taken when you wake. "
               "'Avg today' is the average of all Garmin heart-rate readings since you woke, so it is naturally higher than resting and reflects activity, posture and stress."
               + ("" if pd.isna(diff) else f" The big number is {abs(diff):.0f} bpm {'above' if diff > 0 else 'below'} your usual ({base:.0f})."))
        cards.append(card("Resting heart rate" + ("" if not pd.isna(v) else " (Visible)"), f"{main:.0f}", "bpm", sub, c, spark(f["rhr"], c, False), tip=tip))
        if not pd.isna(diff):
            notes.append(f"Resting heart rate is {main:.0f} bpm, {abs(diff):.0f} {'above' if diff > 0 else 'below'} your usual {base:.0f}.")

    v, d = latest(f, "hrv", 2)
    if not pd.isna(v):
        base = f.loc[d, "hrv_base"]
        diff = v - base if not pd.isna(base) else np.nan
        est_ = f.attrs.get("hrv_src") == "estimate"
        u = "pts" if est_ else "ms"
        if f.attrs.get("hrv_src") == "visible" and d != last:
            notes.append(f"Your latest Visible HRV reading is from {d:%b %d}.")
        c = zone(-f.loc[d, "hrv_z"])[1] if not pd.isna(f.loc[d, "hrv_z"]) else MUTED
        filled = bool(f.loc[d, "hrv_filled"]) if "hrv_filled" in f else False
        sub = "no baseline yet" if pd.isna(diff) else f"{abs(diff):.0f} {u} {'above' if diff > 0 else 'below'} usual ({base:.0f})"
        if filled:
            sub = "estimated from overnight data | " + sub
        cards.append(card("HRV estimate" if est_ else "Overnight HRV" if not filled else "HRV (estimated)", ("~" if filled else "") + f"{v:.0f}", u, sub, c, spark(f["hrv"], c, True), hint=HRV_TIP,
                          tip=("A relative index (50 = your typical night), built from overnight stress and heart rate because the watch has no HRV." if est_ else
                               "No Visible reading for this day, so this is estimated from your overnight watch data and scaled to your own Visible readings. Take a Visible reading when you can for the real number." if filled else "")))
        if not pd.isna(diff) and abs(diff) >= 0.5 * f.loc[d, "hrv_sd"]:
            notes.append(f"{'HRV estimate' if est_ else 'Overnight HRV'} is {'down' if diff < 0 else 'up'} {abs(diff):.0f} {u} from usual.")

    cn = cycle_now(f) if TRACK_PERIOD else None
    if cn:
        cards.append(card("Cycle phase", str(cn["phase"]), "", f"day {cn['day']} of about {cn['L']}", PHASE_COLORS.get(cn["phase"], TYPICAL),
                          tip=f"Next period expected {cn['range'][0]:%b %d} to {cn['range'][1]:%b %d}. A calendar estimate from your logged period starts, not measured hormones. See the Cycle tracker section for the wheel and what each phase usually means."))
        ol = cycle_outlook(f, cn)
        if ol and ol[0] in ("elevated", "soon"):
            cards.append(card("Cycle flare heads-up", "Higher risk" if ol[0] == "elevated" else "Coming up", "", "from your history by phase", ol[1], tip=ol[2]))
            notes.append(ol[2])
    elif f["period"].iloc[-1] == 1:
        cards.append(card("Period", "Today", "", "logged or carried forward from your last entry", PHASE_COLORS["Menstrual"]))

    v, d = latest(f, "sleep_h", 2)
    if not pd.isna(v):
        sc = f.loc[d, "sleep_score"]
        est = f.loc[d, "sleep_src"] == "est"
        c = BETTER if v >= 7 else WATCH if v >= 6 else WARN
        sub = f"{f.loc[d, 'bed']} to {f.loc[d, 'wake']}" + ("" if pd.isna(sc) else f" | score {int(sc)}" + (" (est.)" if est else ""))
        cards.append(card("Last sleep", f"{v:.1f}", "h", sub, c, spark(f["sleep_h"], c, True),
                          tip=("Estimated from heart rate because Garmin had no sleep record for this night. " if est else "") + "Hours asleep. Garmin's sleep times are not always right: you can correct them in the check-in popup."))
        notes.append(f"You slept {v:.1f} hours" + ("." if pd.isna(sc) else f" (score {int(sc)})."))
    try:
        tbl_ = sleep_score_table(f)
        okv = tbl_["total"].dropna()
        if len(okv) and okv.index[-1] >= last - pd.Timedelta(days=1):
            d_ = okv.index[-1]
            lab_, _, txtc_ = score_band(okv.iloc[-1])
            cards.append(card("Sleep score", ("~" if tbl_.loc[d_, "approx"] else "") + f"{int(okv.iloc[-1])}", "/100", f"{lab_} | the dashboard's estimate", txtc_,
                              spark(tbl_["total"], txtc_, True),
                              tip="The dashboard's own estimate from sleep time, overnight stress and heart rate, movement and deep sleep. Your watch gives no sleep score. A ~ means a part had no data that night. Details on the Sleep tab."))
    except Exception as ex:
        log(f"Could not build the sleep score card: {ex}")

    v, d = latest(f, "stress", 1)
    if not pd.isna(v):
        c = zone(f.loc[d, "stress_z"])[1]
        cards.append(card("Stress", f"{v:.0f}", "/100", "daily average", c, spark(f["stress"], c, False), tip="Garmin's average stress for the day, derived from heartbeat timing. Lower is calmer."))

    v, d = latest(f, "spoons", 1)
    if not pd.isna(v):
        ceil = f.loc[d, "pace_ceiling"]
        ratio = v / ceil if not pd.isna(ceil) and ceil > 0 else np.nan
        c = MUTED if pd.isna(ratio) else BETTER if ratio < 0.8 else WATCH if ratio <= 1.0 else ALERT
        vis_p = f.attrs.get("pace_src") == "visible"
        live = d == last and f.loc[d, "pace_asof"]
        if pd.isna(ratio):
            sub, unit_ = "no ceiling yet", ""
            tip = "The ceiling needs about a week of ordinary, non-flare days to learn yours."
        else:
            left = ceil - v
            unit_ = f" / {ceil:.0f}"
            sub = f"{ratio * 100:.0f}% of ceiling | " + (f"about {left:.0f} left" if left > 0 else f"over by {-left:.0f}, rest")
            tip = ("Used so far / today's ceiling. " + ("Visible's own pace points. " if vis_p else "Estimated from time with your heart rate well above resting, counted since you woke"
                   + (f" (as of {f.loc[d, 'pace_asof']}). " if live else ". "))
                   + ("The ceiling is Visible's own limit." if vis_p and not pd.isna(f.loc[d, "vis_pace_limit"]) else
                      "The ceiling is the upper end of your usual non-flare days" + (", lowered today because of flare signals." if f.loc[d, "flare_status"] in FLARE_CEILING else ".")))
            if d != last:
                tip += f" Latest value is from {d:%b %d}."
        pbar = "" if pd.isna(ratio) else f"<div class='pbar'><i style='width:{min(ratio, 1.0) * 100:.0f}%;background:{c}'></i></div>"
        cards.append(card("Pace points" + (" (Visible)" if vis_p else ""), f"{v:.1f}", unit_, sub, c, pbar or spark(f["spoons"], c), tip=tip))
        if not pd.isna(ratio) and ratio > 1.0:
            notes.append(f"You have used {ratio * 100:.0f}% of today's pace-point ceiling, so resting is reasonable.")

    v, d = latest(f, "nap_logged", 1)
    if not pd.isna(v) and f["nap_min"].isna().all():
        cards.append(card("Daytime nap", "Yes" if v == 1 else "No", "", f"logged {d:%b %d} in symptoms.csv", WARN if v == 1 else BETTER,
                          spark(f["nap_logged"], WARN)))
        if v == 1:
            notes.append("You logged a daytime nap.")
    v, d = latest(f, "nap_min", 1)
    if not pd.isna(v):
        first = f.loc[d, "nap_first"]
        cards.append(card("Daytime rest", f"{v:.0f}", "min", f"possible nap from about {first}" if v > 0 and first else ("nap reported by Garmin" if v > 0 else "no nap detected"),
                          WARN if v >= NAP_MIN_MINUTES else BETTER, spark(f["nap_min"], WARN)))
        if v >= NAP_MIN_MINUTES:
            notes.append(f"Your heart rate looked like a nap of about {v:.0f} minutes today.")
    v, d = latest(f, "symptoms", 7)
    if not pd.isna(v):
        c = BETTER if v <= 3 else WATCH if v <= 6 else ALERT
        cards.append(card("Symptom burden", f"{v:.1f}", "/10", f"logged {d:%b %d}",
                          c, spark(f["symptoms"], c, False), tip=(f.loc[d, "tip"] or "")))

    v, d = latest(f, "p_change", 1)
    if not pd.isna(v):
        c = ALERT if v < PRESSURE_DROP_HPA else WARN if v < -2 else TYPICAL
        cards.append(card("Pressure change", f"{v:+.1f}", "hPa", f"{f.loc[d, 'p_mean']:.0f} hPa today", c, spark(f["p_change"], c),
                          tip="Change from yesterday. Drops of 3 hPa or more are flagged because some people with POTS are sensitive to them."))
        if v < -2:
            notes.append(f"Barometric pressure fell {abs(v):.1f} hPa since yesterday, which some people with POTS notice.")

    if not notes:
        notes = ["Not enough recent data yet to compare with your baseline."]
    headline = {"Typical for you": "Today looks typical for you.", "Better than usual": "Today looks better than usual.",
                "A little off": "Today is a little off your normal.", "Clearly off, go easy": "Today is clearly off your normal. Consider going easy.",
                "Danger zone: rest": "Today is in your danger zone. Resting is reasonable.",
                "No data": "No strain score yet."}[label]
    if fl == "unknown":
        headline, zc = "Not enough data to judge how you are doing today.", MUTED
        notes.insert(0, "Your watch can't measure HRV, so on its own it can't tell whether you are in a flare. "
                        "Add your Visible export, or tell the app how you feel, to get flare tracking.")
    elif fl == "active":
        headline, zc = "Your data points to an active flare. Resting is reasonable.", ALERT
        notes.insert(0, f"Flare signals: {why}." if why else f"Several flare signals have shown up over the last {FLARE_WINDOW} days.")
    elif fl == "watch":
        notes.insert(0, f"Possible flare symptoms: {why}." if why else f"There was a flare day in the last {FLARE_WINDOW} days.")
    return headline, zc, " ".join(notes), group_cards(cards)


def signal_card(f, zcol, title, what, lit, color):
    """Do your own low-HRV days (z <= -1 against your usual) come before worse days? Outcomes are things HRV does not define: Visible's stability score
    (2 or lower) and the 'I'm in a flare' answers you give. Compared for the same day, the next day and two days later."""
    z = f[zcol]
    low = (z <= FLARE_HRV_Z).where(z.notna())
    n_low = int((low == 1).sum())
    outs = [("Visible stability of 2 or lower", (f["vis_stab"] <= 2).where(f["vis_stab"].notna())),
            ("You answered \"in a flare\"", (f["flare_manual"] == 1).where(f["flare_manual"].notna()))]
    rows, shown = "", 0
    for label, y in outs:
        for lag, when in ((0, "the same day"), (1, "the next day"), (2, "two days later")):
            d = pd.concat([low, y.shift(-lag)], axis=1).dropna()
            a_, b_ = d[d.iloc[:, 0] == 1].iloc[:, 1], d[d.iloc[:, 0] == 0].iloc[:, 1]
            if len(a_) < 4 or len(b_) < 8:
                continue
            ra, rb = 100 * a_.mean(), 100 * b_.mean()
            se = math.sqrt(max(a_.var(ddof=1) / len(a_) + b_.var(ddof=1) / len(b_), 0)) if len(a_) > 1 else 0
            t = (a_.mean() - b_.mean()) / se if se > 0 else 0.0
            chip = "pattern" if abs(t) >= 2 else "maybe" if abs(t) >= 1.3 else "no clear difference"
            col = (WARN if ra > rb else BETTER) if abs(t) >= 1.3 else MUTED
            rows += (f"<div style='margin-top:8px;font-size:13px'><b>{label}, {when}:</b> {ra:.0f}% after {what} days ({len(a_)} days) vs {rb:.0f}% otherwise "
                     f"<span class='chip' style='border-color:{col};color:{col}'>{chip}</span></div>")
            shown += 1
    if not shown:
        rows = (f"<div class='msg'>You have {n_low} {what} day{'s' if n_low != 1 else ''} in this window. To compare them with your flares, the app needs at least 4 such days and 8 other days "
                "that have a Visible stability score or a flare answer. Keep importing your Visible export and answering the daily flare question, and the results will appear here.</div>")
    return (f"<div class='card' style='border-top:3px solid {color};grid-column:1/-1'><div class='ct'><b style='color:var(--text);font-size:14px'>{title}</b> "
            f"({n_low} days at or below {FLARE_HRV_Z:+.0f} SD of your usual)</div>{rows}<div class='lit'><b>Background</b>{lit}</div></div>")


AUTOIMMUNE_LINK = ("Why this applies across your conditions: the signal here is the inflammation-to-autonomic link, which autoimmune conditions share. In lupus, lower HRV went with higher "
                   "inflammatory markers (sTNFRII, MIG; Thanou 2016, 53 patients with active disease), and in rheumatoid arthritis HRV shifted before CRP rose (preliminary preprint, 53 patients). "
                   "Autoimmune mechanisms are also being studied in POTS. Evidence from one disease is a reasonable guide for another, not proof for each. ")


def hrv_outlier_card(f):
    lit = (AUTOIMMUNE_LINK + "What it shows: lower HRV goes with more active lupus and follows disease activity over weeks. In POTS, HRV differs by subtype (Gibbons 2013). "
           "In Visible's 4,244 users with ME/CFS or long COVID, falling HRV and rising resting heart rate against a person's own baseline predicted crashes. "
           "This card checks the same idea against your own days.")
    return signal_card(f, "hrv_z", "Low HRV days: an autoimmune flare signal", "low-HRV", lit, BETTER)


def steps_outlier_card(f):
    if "steps_z" not in f or f["steps_z"].notna().sum() < 14:
        return ""
    lit = (AUTOIMMUNE_LINK + "What it shows: in the rheumatoid arthritis preprint (Apple Watch, Fitbit or Oura; not yet peer reviewed), step counts fell before and during symptomatic flares, and a model combining "
           "steps with heart rate flagged flares up to 28 days ahead. This card checks whether your own low-step days line up with your flares.")
    return signal_card(f, "steps_z", "Low step days: an autoimmune flare signal", "low-step", lit, BETTER)


def period_flare_card(f):
    """Do flare days gather around the start of your periods? Window = 2 days before to 3 days after each logged period start, compared with all other days that have a known flare status.
    Reports each period separately plus the overall rate, so you can see whether it repeats cycle after cycle."""
    if not TRACK_PERIOD or "cycle" not in f.attrs:
        return ""
    known = f["flare_status"].ne("unknown")
    flare = f["flare_day"].fillna(False).astype(bool)
    starts = [e["start"] for e in f.attrs["cycle"].get("episodes", []) if e["start"] >= f.index[0]]
    inwin = pd.Series(False, index=f.index)
    per, lines = [], ""
    for st in starts:
        w = f.index[(f.index >= st - pd.Timedelta(days=2)) & (f.index <= st + pd.Timedelta(days=3))]
        w = [d for d in w if known[d]]
        inwin[w] = True
        if len(w) >= 3:
            hit = [d for d in w if flare[d]]
            per.append((st, len(hit), len(w)))
            lines += (f"<div style='margin-top:6px;font-size:13px'><b>Period starting {st:%b %d}:</b> "
                      + (f"flare day{'s' if len(hit) != 1 else ''} on {', '.join(f'{d:%b %d}' for d in hit)}" if hit else "no flare day recorded around it")
                      + f" <span class='muted'>({len(w)} days with flare data)</span></div>")
    a_, b_ = flare[inwin & known].astype(float), flare[~inwin & known].astype(float)
    n_hit = sum(1 for _, h, _ in per if h)
    color = BETTER
    if not per:
        body = ("<div class='msg'>No period start in this window has flare data around it yet. Log your period starts (daily check-in or Garmin cycle tracking) and answer the flare question or import "
                "Visible, and each period will be compared here.</div>")
    else:
        ra, rb = 100 * a_.mean(), (100 * b_.mean() if len(b_) else float("nan"))
        se = math.sqrt(a_.var(ddof=1) / len(a_) + b_.var(ddof=1) / len(b_)) if len(a_) > 1 and len(b_) > 1 else 0
        t = (a_.mean() - b_.mean()) / se if se > 0 else 0.0
        color = WARN if ra > rb and abs(t) >= 1.3 else BETTER if abs(t) >= 1.3 and ra < rb else MUTED
        chip = "pattern" if abs(t) >= 2 else "maybe" if abs(t) >= 1.3 else ""
        chip_html = f" <span class='chip' style='border-color:{color};color:{color}'>{chip}</span>" if chip else ""
        body = (f"<div class='msg'>A flare day showed up around the start of <b>{n_hit} of {len(per)}</b> logged period{'s' if len(per) != 1 else ''}. "
                + (f"In the window from 2 days before to 3 days after a period starts, {ra:.0f}% of days were flare days, against {rb:.0f}% on other days{chip_html}." if len(b_) else "")
                + f"</div>{lines}")
    lit = (" Many people with POTS, lupus and other autoimmune conditions report flares and symptoms that peak around menstruation. In POTS, lightheadedness was worst during menstruation (Peggs 2012), "
           "and resting heart rate and HRV shift with the cycle in wearable data (WHOOP; Schmalenberger 2020). This card checks your own history so you can see how consistent it is for you.")
    return (f"<div class='card' style='border-top:3px solid {color};grid-column:1/-1'><div class='ct'><b style='color:var(--text);font-size:14px'>Period start and flares</b> "
            f"(2 days before to 3 days after each period starts)</div>{body}<div class='lit'><b>Background</b>{lit}</div></div>")


def build_insights_html(f):
    cards, thin, notes = compute_insights(f)
    try:
        hrv_card = hrv_outlier_card(f) + steps_outlier_card(f) + period_flare_card(f)
    except Exception as ex:
        hrv_card = ""
        log(f"Could not build the low-HRV comparison: {ex}")
    if not cards:
        return ("<div class='cards' style='grid-template-columns:1fr'>" + hrv_card + "</div><p class='muted'>Not enough days yet. Each comparison needs at least 4 days with the factor (a short night, a day over your ceiling, a pressure drop, a cycle phase) "
                "and 10 without, with data on the other side. " + (" ".join(notes)) + "</p>")
    html = "<div class='cards' style='grid-template-columns:repeat(auto-fill,minmax(300px,1fr))'>" + hrv_card
    for c in cards:
        body = ""
        for r in c["rows"][:6]:
            if r["worse"] == 0:
                col, word = MUTED, "more" if r["diff"] > 0 else "less"
            else:
                bad = (r["diff"] > 0) == (r["worse"] > 0)
                col, word = (WARN, "worse") if bad else (BETTER, "better")
            chip = "pattern" if r["verdict"] == "pattern" else "maybe"
            body += (f"<div style='margin-top:8px'><div style='font-size:13px'><b>{r['label'].capitalize()}</b>: {r['a']} vs {r['b']} on other days "
                     f"<span style='color:{col}'>({word}, {r['diff']:+.1f}{r['unit']})</span> <span class='chip' style='border-color:{col};color:{col}'>{chip}</span></div></div>")
        if not body:
            body = f"<div class='msg'>{c['n']} days with this factor are being tracked. Patterns will show here as more days are logged.</div>"
        html += (f"<div class='card' style='border-top:3px solid {MUTED}'><div class='ct'><b style='color:var(--text);font-size:14px'>{c['title']}</b> "
                 f"({c['n']} days)</div>{body}</div>")
    html += "</div>"
    if thin:
        html += f"<p class='muted' style='margin-top:10px'>Too few days to compare yet: {'; '.join(thin)}.</p>"
    for n_ in notes:
        html += f"<p class='muted'>{n_}</p>"
    html += ("<p class='muted' style='margin-top:8px'>Each card compares the average on days with that factor against all other days (same day, or the next day where it says so). "
             "<b>Pattern</b> means the difference is large compared with your normal day-to-day swings; <b>maybe</b> is an early hint that firms up as you log more days.</p>")
    return html


PHASE_COLORS = {"Menstrual": "#CC79A7", "Follicular": "#56B4E9", "Ovulation window": "#F0E442", "Luteal": "#E69F00"}
PHASE_ORDER = ["Menstrual", "Follicular", "Ovulation window", "Luteal"]
PHASE_INFO = {
    "Menstrual": ("Estrogen and progesterone are at their lowest and the uterine lining sheds. Cramps come from prostaglandins, and blood loss can leave some people low on iron.",
                  "Often the hardest days. In the one POTS study I found (Peggs 2012), lightheadedness was worst during menstruation, in patients and in healthy controls. "
                  "Wearable data (WHOOP) shows the opposite for the numbers: resting heart rate is lowest and HRV highest around days 2 to 7, so your watch can look fine on a day you feel bad. "
                  "Histamine: estrogen makes mast cells more reactive, so more histamine can be released around your period (see the histamine note below)."),
    "Follicular": ("Estrogen climbs toward ovulation as a follicle matures.",
                   "Many people feel more energy and a steadier mood. In the same POTS study this was the best phase, with the least lightheadedness. "
                   "A reasonable time to use more of your pace-point ceiling, as long as today's stability and strain agree."),
    "Ovulation window": ("A surge of LH triggers the egg's release roughly a day later. Estrogen peaks, then dips. Discharge is often clear and stretchy.",
                         "Some people feel a one-sided lower-belly twinge or ache (mittelschmerz) for hours to a day or two, plus a bump in libido. "
                         "Counting days can't pinpoint ovulation, and with cycles that vary it can be off by several days, so treat this as a window, not a date."),
    "Luteal": ("Progesterone takes over. Resting body temperature rises a few tenths of a degree, and if there is no pregnancy the hormones fall again before the period.",
               "Often the weaker, more sluggish phase. In wearable data resting heart rate runs about 2 to 3 bpm higher and HRV about 4 to 5 ms lower than in the follicular phase (WHOOP), "
               "and in lab studies higher-than-usual progesterone goes with lower HRV (Schmalenberger 2020). Sleep, mood and energy often dip, and PMS-type symptoms peak in the last days before the period. "
               "Some people with POTS or lupus report feeling worse premenstrually. Histamine is one proposed reason: the enzyme that breaks it down (DAO) is higher in the luteal phase in one study, but estrogen also makes mast cells release more, "
                "and flushing, itching, headaches, hives or a racing heart before a period are the kind of symptoms people link to it (see the histamine note below). Your own table below shows whether the pattern holds for you."),
}


def _pt(cx, cy, r, deg):
    a_ = math.radians(deg - 90)
    return cx + r * math.cos(a_), cy + r * math.sin(a_)


def _arc(cx, cy, ro, ri, a0, a1):
    a1 = min(a1, a0 + 359.99)
    big = 1 if a1 - a0 > 180 else 0
    p0, p1, p2, p3 = _pt(cx, cy, ro, a0), _pt(cx, cy, ro, a1), _pt(cx, cy, ri, a1), _pt(cx, cy, ri, a0)
    return (f"M{p0[0]:.1f},{p0[1]:.1f} A{ro},{ro} 0 {big} 1 {p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} "
            f"A{ri},{ri} 0 {big} 0 {p3[0]:.1f},{p3[1]:.1f} Z")


def cycle_now(f):
    """Where today sits in the cycle, or None when there is no recent logged period start."""
    ci = f.attrs.get("cycle") or {}
    if not ci.get("starts") or pd.isna(f["cycle_day"].iloc[-1]):
        return None
    day, L, P = int(f["cycle_day"].iloc[-1]), int(ci["cycle_len"]), int(ci["period_len"])
    ov = int(ci["ov_day"] or max(L - LUTEAL_DAYS, P + 3))
    total = max(L, day + 2)
    return {"day": day, "phase": f["phase"].iloc[-1], "L": L, "P": P, "ov": ov, "total": total, "start": ci["starts"][-1],
            "ov_src": ci.get("ov_src", "calendar"), "range": ci.get("next_range"), "next": ci.get("next_start"), "stats": ci.get("stats")}


def build_wheel_svg(cn):
    cx = cy = 130
    ro, ri = 118, 80
    tot = float(cn["total"])
    deg = 360.0 / tot
    P, ov = cn["P"], cn["ov"]
    bounds = [("Menstrual", 0, P), ("Follicular", P, ov - 2), ("Ovulation window", ov - 2, ov + 1), ("Luteal", ov + 1, tot)]
    parts = []
    for name, d0, d1 in bounds:
        if d1 > d0:
            parts.append(f"<path d='{_arc(cx, cy, ro, ri, d0 * deg, d1 * deg)}' fill='{PHASE_COLORS[name]}' stroke='#12161c' stroke-width='2'><title>{name}: days {int(d0) + 1} to {int(d1)}</title></path>")
    fs, fe = max(ov - 5, 0), ov + 1                       # fertile window: the 5 days before ovulation and the day of it
    parts.append(f"<path d='{_arc(cx, cy, ro + 8, ro + 3, fs * deg, fe * deg)}' fill='#E4E2DC'><title>Fertile window (estimated), days {int(fs) + 1} to {int(fe)}</title></path>")
    mx, my = _pt(cx, cy, (ro + ri) / 2, (cn["day"] - 0.5) * deg)
    parts.append(f"<circle cx='{mx:.1f}' cy='{my:.1f}' r='11' fill='#12161c' stroke='#fff' stroke-width='3'><title>Today: day {cn['day']}</title></circle>")
    parts.append(f"<text x='{cx}' y='{cy - 6}' text-anchor='middle' fill='#e4e2dc' font-size='34' font-weight='600'>Day {cn['day']}</text>")
    parts.append(f"<text x='{cx}' y='{cy + 18}' text-anchor='middle' fill='{PHASE_COLORS.get(cn['phase'], '#8d96a3')}' font-size='15'>{cn['phase']}</text>")
    parts.append(f"<text x='{cx}' y='{cy + 38}' text-anchor='middle' fill='#8d96a3' font-size='11'>of about {cn['L']}</text>")
    return f"<svg viewBox='-14 -14 288 288' width='270' role='img' aria-label='Cycle wheel, day {cn['day']}, {cn['phase']}'>{''.join(parts)}</svg>"


def _grp_stats(f):
    """Per-phase table values: days, cycles, flare share, symptoms, strain, mood. Plus a Premenstrual row (last 5 days before a period)."""
    ok = f["flare_status"].ne("unknown")
    groups = {ph: f["phase"] == ph for ph in PHASE_ORDER}
    groups["Premenstrual"] = f["premens"]
    res = {}
    for k, m in groups.items():
        sub = f[m & ok] if k != "Premenstrual" else f[m & ok]
        if sub.empty:
            continue
        res[k] = {"n": len(sub), "cycles": int(sub["cycle_id"].nunique()), "flare": 100.0 * sub["flare_day"].fillna(False).mean(),
                  "sym": sub["symptoms"].mean(), "strain": sub["strain"].mean(), "sub": sub}
    base_sub = f[f["phase"].notna() & ok]
    base = 100.0 * base_sub["flare_day"].fillna(False).mean() if len(base_sub) else np.nan
    return res, base, len(base_sub)


def cycle_outlook(f, cn, stats=None):
    """Plain-language heads-up about whether a harder window is here or coming, based on your own flare history by phase, with general research as the fallback."""
    if cn is None:
        return None
    res, base, nbase = stats if stats is not None else _grp_stats(f)
    risky = {k: v for k, v in res.items() if v["n"] >= 5 and v["cycles"] >= 2 and not np.isnan(base)
             and v["flare"] >= 1.5 * base and v["flare"] >= base + 10}
    today = f.index[-1]
    nr = cn["range"]
    days_to = (nr[0] - today).days if nr else None
    in_prem = days_to is not None and days_to <= 5 and cn["day"] >= cn["L"] - 7
    if cn["phase"] in risky or (in_prem and "Premenstrual" in risky):
        k = cn["phase"] if cn["phase"] in risky else "Premenstrual"
        return ("elevated", ALERT, f"Higher-risk window: on {risky[k]['n']} past {k.lower()} days across {risky[k]['cycles']} cycles you were in a flare {risky[k]['flare']:.0f}% of the time, "
                f"against {base:.0f}% overall. Consider a lighter day.")
    if "Premenstrual" in risky and days_to is not None and 0 < days_to <= 10:
        return ("soon", WARN, f"Heads-up: the days just before your period have been rough for you ({risky['Premenstrual']['flare']:.0f}% flare days vs {base:.0f}% overall). "
                f"Your period is expected between {nr[0]:%b %d} and {nr[1]:%b %d}, so that window starts in roughly {max(days_to - 5, 0)} days.")
    if nbase >= 40 and len(res) >= 3 and all(v["n"] >= 5 for k, v in res.items() if k in PHASE_ORDER):
        return ("none", TYPICAL, "Your logged history doesn't show a phase with clearly more flare days yet. Keep logging: patterns need several cycles.")
    gen = ("General research, not your data: lightheadedness in POTS was worst during menstruation and best in the follicular phase (Peggs 2012), and many people feel "
           "worse in the days before a period. Not enough of your own history yet to say whether that holds for you.")
    return ("general", MUTED, gen)


HISTAMINE_HTML = (
    "<div class='card' style='border-top:3px solid #CC79A7;grid-column:1/-1;margin-top:12px'>"
    "<div class='ct'><b style='color:var(--text);font-size:14px'>Histamine, mast cells and your cycle</b></div>"
    "<div class='msg'>Estrogen makes mast cells more reactive, so more histamine can be released around your period, and H1 and H2 blockers have helped people with POTS and mast cell activation.</div>"
    "<div class='lit'><b>Background</b>"
    "Estrogen increases mast cell reactivity and strengthens histamine-triggered skin reactions. DAO, the enzyme that clears histamine from the gut, was higher in the luteal phase in one study, "
    "which suggests the cycle interacts with histamine handling (Jackson 2025 review, <i>Int J Mol Sci</i>, summarizing earlier work). "
    "Falling hormones just before a period are linked to PMS-type symptoms, and flushing, hives, headaches, itching, nausea and a faster heartbeat are among the symptoms people with histamine problems report at that time. "
    "In a group of POTS patients with mast cell activation, urinary histamine breakdown product was about twice the normal level, and premenstrual timing was a reported trigger in 2 of 8 (Shibao 2005, <i>Hypertension</i>). "
    "In that report, patients improved on H1 and H2 blockers, with or without a second medicine (uncontrolled, 6 treated). "
    "Many women report relief from premenstrual and period symptoms with an H1 antihistamine (cetirizine, loratadine or fexofenadine) combined with famotidine, an H2 blocker.</div></div>")


def build_cycle_html(f):
    if not TRACK_PERIOD:
        return ""
    ci = f.attrs.get("cycle") or {}
    head = ("<h2>Cycle tracker</h2><p class='sub'>Period days come from everything you have recorded: the daily check-in, <code>period</code> in symptoms.csv, Garmin's cycle tracking and "
            "Visible's Period tracker, all saved locally. A period is carried forward from its first logged day, and a \"no\" ends it. "
            "Phases are calendar estimates, not measured hormones.</p>")
    cn = cycle_now(f)
    if not ci.get("starts"):
        return head + ("<div class='panel'>No period dates yet. Answer the daily question when the app starts (say when it began), or put <code>1</code> in the "
                       "<code>period</code> column of symptoms.csv on the first day.</div>")
    st = ci.get("stats")
    gs = f.attrs.get("garmin_cycle")
    garmin_line = ""
    if gs and gs.get("cycleType"):
        garmin_line = (f"<div class='muted' style='margin:0 0 10px'>Garmin's own cycle tracking says: cycle type <b style='color:var(--text)'>{str(gs['cycleType']).lower()}</b>, "
                       f"predicted cycle length {gs.get('predictedCycleLength')} days, period length {gs.get('periodLength')} days, current cycle started {gs.get('startDate')}.</div>")
    if cn is None:
        last = ci["starts"][-1]
        top = (f"<div class='panel'>Your most recent logged period began {last:%b %d, %Y}, which is too long ago to place today in a cycle. "
               "Log your latest start (the daily question asks for the start date) and the wheel will appear.</div>")
    else:
        stats = _grp_stats(f)
        ol = cycle_outlook(f, cn, stats)
        fert = f"{(cn['start'] + pd.Timedelta(days=max(cn['ov'] - 5, 0))):%b %d} to {(cn['start'] + pd.Timedelta(days=cn['ov'])):%b %d}"
        ovd = cn["start"] + pd.Timedelta(days=cn["ov"] - 1)
        ov_note = ("from your discharge entries" if cn["ov_src"] == "discharge" else
                   ("a rough guess" if st is None or (st["recent_max"] - st["recent_min"]) > 7 else "an estimate") + " counted back from your typical cycle length")
        rng = cn["range"]
        right = (f"<div><div style='font-size:15px;margin-bottom:8px'><b>{cn['phase']}</b>, day {cn['day']} of about {cn['L']}</div>"
                 f"<div class='muted' style='margin-bottom:4px'>Next period expected: <b style='color:var(--text)'>{rng[0]:%b %d} to {rng[1]:%b %d}</b> (most likely about {cn['next']:%b %d}).</div>"
                 f"<div class='muted' style='margin-bottom:4px'>Ovulation, {ov_note}: around <b style='color:var(--text)'>{ovd:%b %d}</b>. Fertile window about {fert} (pale outer arc).</div>"
                 + (f"<div style='margin-top:10px;padding:10px 12px;border-left:4px solid {ol[1]};background:#1a2029;border-radius:4px;font-size:13.5px'>{ol[2]}</div>" if ol else "")
                 + "<div class='legend' style='margin-top:10px'>" + "".join(f"<span><i style='background:{PHASE_COLORS[p]}'></i>{p}</span>" for p in PHASE_ORDER) + "</div></div>")
        top = f"<div class='panel cyc'>{build_wheel_svg(cn)}{right}</div>"
    # how long between periods
    hist = ""
    if st:
        irregular = (st["max"] - st["min"]) > 9
        rows = "".join(f"<tr><td>{a_:%b %d, %Y}</td><td>{b_:%b %d, %Y}</td><td>{d_} days</td></tr>" for a_, b_, d_ in ci["gaps"][-8:])
        hist = ("<h3 style='font-size:14px;margin:18px 0 6px'>Time between periods</h3><div class='panel' style='overflow-x:auto'>"
                f"<div style='margin-bottom:8px'>{st['n']} logged cycle{'s' if st['n'] != 1 else ''}: usually <b>{st['median']:.0f} days</b> "
                f"(shortest {st['min']}, longest {st['max']}, average {st['mean']:.0f}).</div>"
                + ("<div class='muted' style='margin-bottom:8px'>Your cycle length varies by more than about 9 days, which is generally considered irregular, so predictions are shown as ranges and "
                   "the ovulation estimate is rough. Worth mentioning to your doctor, especially with lupus.</div>" if irregular else "")
                + f"<table class='tbl'><tr><th>Period began</th><th>Next period began</th><th>Cycle length</th></tr>{rows}</table>"
                "<div class='muted' style='margin-top:6px'>Gaps over 60 days are left out because a period was probably not logged.</div></div>")
    # phase descriptions
    res, base, nb = _grp_stats(f)
    cards = ""
    for ph in PHASE_ORDER:
        what, feel = PHASE_INFO[ph]
        mine = ""
        if ph in res and res[ph]["n"] >= 3:
            r_ = res[ph]
            mine = (f"<div class='ch'>Your data: {r_['n']} days over {r_['cycles']} cycle{'s' if r_['cycles'] != 1 else ''}, in a flare {r_['flare']:.0f}% of days"
                    + ("" if np.isnan(r_["sym"]) else f", symptoms {r_['sym']:.1f}/10") + ".</div>")
        here = cn is not None and cn["phase"] == ph
        cards += (f"<div class='card' style='border-top:3px solid {PHASE_COLORS[ph]};{'outline:2px solid #fff;' if here else ''}'>"
                  f"<div class='ct'><b style='color:var(--text);font-size:14px'>{ph}</b>{' (you are here)' if here else ''}</div>"
                  f"<div class='cs' style='margin-top:6px'>{what}</div><div class='cs' style='margin-top:6px'>{feel}</div>{mine}</div>")
    phases = ("<h3 style='font-size:18px;margin:22px 0 8px'>What each phase usually means</h3><div class='cards' style='grid-template-columns:repeat(auto-fill,minmax(250px,1fr))'>" + cards + "</div>"
              + HISTAMINE_HTML)
    # by phase table
    cols = [("symptoms", "Symptoms", "{:.1f}"), ("strain", "Strain", "{:+.1f}"), ("mood", "Mood (1-5)", "{:.1f}"), ("hrv", "HRV", "{:.0f}"),
            ("rhr", "Resting HR", "{:.0f}"), ("spoons", "Pace points", "{:.1f}"), ("sleep_h", "Sleep (h)", "{:.1f}")]
    cols = [c for c in cols if f[c[0]].notna().sum() >= 5]
    th = "".join(f"<th>{n}</th>" for _, n, _ in cols)
    body = ""
    for k in PHASE_ORDER + ["Premenstrual"]:
        if k not in res:
            continue
        sub = res[k]["sub"]
        cells = "".join(f"<td>{fmt.format(sub[c].mean()) if sub[c].notna().any() else '-'}</td>" for c, _, fmt in cols)
        lab = k if k != "Premenstrual" else "Last 5 days before a period"
        body += f"<tr><td>{lab}</td><td>{res[k]['n']} ({res[k]['cycles']})</td><td>{res[k]['flare']:.0f}%</td>{cells}</tr>"
    tbl = ""
    if body:
        tbl = ("<h3 style='font-size:14px;margin:18px 0 6px'>Your numbers by phase</h3><div class='panel' style='overflow-x:auto'><table class='tbl'>"
               f"<tr><th>Phase (estimated)</th><th>Days (cycles)</th><th>Flare days</th>{th}</tr>{body}</table>"
               "<div class='muted' style='margin-top:6px'>Flare days compare with "
               + ("" if np.isnan(base) else f"{base:.0f}% across all days with a known phase. ") + "The premenstrual row overlaps the luteal row. Early cycles are few, so treat gaps as noise until several cycles are logged.</div></div>")
    starts_ = ci["starts"]
    longg = [(a_, b_, (b_ - a_).days) for a_, b_ in zip(starts_, starts_[1:]) if (b_ - a_).days > 60]
    if longg:
        hist += ("<div class='muted' style='margin-top:8px'>Gaps over 60 days are not counted in your typical cycle length: "
                 + "; ".join(f"{d_} days ({a_:%b %d, %Y} to {b_:%b %d, %Y})" for a_, b_, d_ in longg[-4:])
                 + ". If you really had no period in those stretches (rather than not logging it), that is worth telling your doctor. "
                 "Long gaps can come from many causes, and menstrual changes are common in lupus.</div>")
    return head + garmin_line + top + hist + phases + tbl


def drop_svg(est=False, size=12):
    """Red teardrop for period days. Outlined instead of filled when the day is estimated."""
    fill = "none" if est else PERIOD_RED
    return (f"<svg class='drop' viewBox='0 0 10 14' width='{size}' height='{round(size * 1.4)}' aria-label='period day'>"
            f"<path d='M5 .6C5 .6 .9 6 .9 9a4.1 4.1 0 0 0 8.2 0C9.1 6 5 .6 5 .6Z' fill='{fill}' stroke='{PERIOD_RED}' stroke-width='1.3' stroke-linejoin='round'/></svg>")


def build_calendar_html(f):
    """Last 8 weeks. Each day shows Visible's (or the estimated) stability, since that is what tracks flares, with strain underneath."""
    last = f.index[-1]
    start = last - timedelta(days=last.weekday()) - timedelta(weeks=7)
    head = "".join(f"<div class='dow'>{d}</div>" for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    cells, d = "", start
    while d <= last + timedelta(days=6 - last.weekday()):
        if d > last or d not in f.index:
            cells += "<div class='day empty'></div>"
        else:
            r = f.loc[d]
            stab, strain = r["stability"], r["strain"]
            flare = bool(r["flare_day"])
            if flare or (not pd.isna(stab) and stab <= 2):
                c = WARN
            elif not pd.isna(stab) and stab >= 4:
                c = BETTER
            elif pd.isna(stab) and pd.isna(strain):
                c = MUTED
            else:
                c = TYPICAL
            drop = (not pd.isna(r["p_change"])) and r["p_change"] < PRESSURE_DROP_HPA
            est = r["stab_src"] != "visible"
            big = "-" if pd.isna(stab) else f"{'~' if est else ''}{int(stab)}"
            small = "" if pd.isna(strain) else f"strain {strain:+.1f}"
            word = "" if pd.isna(stab) else {1: "lowest", 2: "low", 3: "mid", 4: "good", 5: "great"}.get(int(stab), "")
            bits = [f"{d:%a %b %d}", "Stability " + ("no data" if pd.isna(stab) else f"{int(stab)}/5 ({'estimated' if est else 'Visible'})")]
            if not pd.isna(strain): bits.append(f"strain {strain:+.1f}")
            if flare: bits.append(f"FLARE DAY ({r['flare_why']})")
            for nm, col, fm in (("HRV", "hrv", "{:.0f}"), ("resting HR", "rhr", "{:.0f}"), ("sleep h", "sleep_h", "{:.1f}"), ("symptoms", "symptoms", "{:.1f}/10"), ("mood", "mood", "{:.0f}/5")):
                if not pd.isna(r[col]): bits.append(f"{nm} {fm.format(r[col])}")
            if not pd.isna(r["p_change"]): bits.append(f"pressure {r['p_change']:+.1f} hPa")
            if not pd.isna(r["cycle_day"]): bits.append(f"cycle day {int(r['cycle_day'])} ({r['phase']})")
            if r["period"] == 1: bits.append("period day" + (" (estimated)" if r["period_est"] else ""))
            if r["discharge"]: bits.append(f"discharge {r['discharge']}")
            if r["period_symptoms"]: bits.append(f"cycle symptoms: {r['period_symptoms']}")
            if r["tip_full"]: bits.append(r["tip_full"])
            tip = " | ".join(bits).replace("'", "&#39;")
            today = " today" if d == last else ""
            tags = (("<span style='color:#E08A00'>&#9670;</span> " if flare else "") + (drop_svg(bool(r["period_est"]), 11) + " " if r["period"] == 1 else "") + ("<span style='color:#AAB4C0'>&#9660;</span>" if drop else "")).strip()
            cells += (f"<div class='day{today}' title='{tip}' style='background:{c}2e;border-color:{c if d == last else '#2a323d'}'>"
                      f"<span class='dt'><span class='dn'>{d.day}</span><span class='dp'>{tags}</span></span>"
                      f"<span class='dv' style='color:{c}'>{big}<small class='dw'>{word}</small></span></div>")
        d += timedelta(days=1)
    return (f"<div class='cal'>{head}{cells}</div><p class='muted' style='margin-top:16px;padding-top:12px;border-top:1px solid var(--line)'>Big number = stability from 1 to 5, and the small word beside it says what that means (~ means estimated); hover a day for strain and the rest. "
            "Orange = flare day or stability 2 or lower, blue = 4 or higher. <span style='color:#E08A00'>&#9670;</span> flare, "+drop_svg(False, 10)+" period, <span style='color:#AAB4C0'>&#9660;</span> pressure drop. </p>")


CSS = """
:root{--bg:#12161c;--panel:#1a2029;--line:#2a323d;--text:#e4e2dc;--muted:#8d96a3}
*{box-sizing:border-box}body{background:var(--bg);color:var(--text);margin:0;padding:24px 16px 60px;
font-family:'Segoe UI',system-ui,sans-serif;line-height:1.5}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0 6px;position:sticky;top:0;z-index:5;background:var(--bg);padding:10px 0;border-bottom:2px solid var(--line)}
.tabs button{display:inline-flex;align-items:center;gap:8px;background:#161c26;color:var(--muted);border:2px solid #2f3b4a;border-radius:4px;padding:7px 13px 7px 11px;font-size:12.5px;font-family:Consolas,'Cascadia Mono','Courier New',monospace;letter-spacing:.07em;text-transform:uppercase;cursor:pointer;box-shadow:0 3px 0 #0b0f15}
.tabs button .ti{width:16px;height:16px}
.tabs button:hover{color:var(--text);border-color:#56B4E9}
.tabs button.on{background:#56B4E9;color:#0b1018;border-color:#9bd6f5;font-weight:700;box-shadow:0 3px 0 #2c7fae;transform:translateY(1px)}
.tabs button.on::before{content:"\\25B6";font-size:9px;margin-right:-2px}
section.tab h2:first-child{margin-top:26px}
.wrap{max-width:1040px;margin:0 auto}h2{font-size:24px;font-weight:600;letter-spacing:-.01em;margin:52px 0 6px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.sub{color:var(--muted);font-size:14px;line-height:1.55;max-width:90ch;margin:10px 0 16px}.muted{color:var(--muted);font-size:12.5px}
.hero{background:linear-gradient(135deg,var(--panel),#161b22);border:1px solid var(--line);border-left:5px solid var(--hc);border-radius:12px;padding:20px 24px 18px;margin:0 0 14px}
.hero-top{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.pill{background:rgba(255,255,255,.06);border:1px solid var(--line);border-radius:999px;padding:3px 12px;font-size:12.5px;color:var(--muted)}
.pill.big{color:var(--text);font-weight:600;font-size:13px}
.ver{margin-left:auto;font-size:12px;color:var(--muted);opacity:.8}
.hero-main{display:flex;gap:22px;align-items:center;margin-top:16px}
.dot{flex:none;width:14px;height:14px;border-radius:50%;background:var(--hc);margin-top:15px;box-shadow:0 0 0 5px color-mix(in srgb,var(--hc) 25%,transparent)}
.hero h1{font-family:'Segoe UI',system-ui,sans-serif;font-weight:650;font-size:32px;letter-spacing:-.015em;line-height:1.2;margin:0;color:var(--text)}
.hero p.lead{font-size:15.5px;color:var(--muted);margin:4px 0 0;max-width:70ch}
.facts{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0;padding:0}
.facts li{background:rgba(255,255,255,.05);border-radius:8px;padding:6px 12px;font-size:13.5px;line-height:1.35}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}

.tg{margin-top:22px}.tg:first-child{margin-top:20px}.tgh{display:flex;align-items:center;gap:12px;margin-bottom:10px}.tgh h3{margin:0;font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}.tgh i{flex:1;height:1px;background:var(--line)}
.pbar{height:9px;background:#232c39;border-radius:6px;margin-top:8px;overflow:hidden}.pbar i{display:block;height:100%;border-radius:6px}

.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px;position:relative}.ci{position:absolute;top:8px;right:10px;color:var(--muted);font-size:13px;cursor:help}.ct{color:var(--muted);font-size:13px}
.card[data-lv='1']{background:linear-gradient(rgba(240,228,66,.10),rgba(240,228,66,.10)),var(--panel)}.card[data-lv='2']{background:linear-gradient(rgba(224,138,0,.11),rgba(224,138,0,.11)),var(--panel)}.card[data-lv='3']{background:linear-gradient(rgba(209,67,44,.13),rgba(209,67,44,.13)),var(--panel)}
.lvt{font-size:10px;letter-spacing:.08em;border:1px solid currentColor;border-radius:4px;padding:1px 5px;margin-left:6px;vertical-align:1px}
html.nolv .card[data-lv]{background:var(--panel)}html.nolv .lve{display:none}
.cv{font-size:30px;font-weight:600;margin-top:2px}.unit{font-size:13px;color:var(--muted);margin-left:4px;font-weight:400}
.cs{color:var(--muted);font-size:12px;min-height:18px}.spark{width:100%;height:46px;margin-top:6px;display:block}
html.spA-on .spC{display:none}html:not(.spA-on) .spA{display:none}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.howbar{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}
.howbar button{background:rgba(255,255,255,.06);color:var(--text);border:1px solid var(--line);border-radius:999px;padding:4px 14px;margin-left:6px;font-size:12.5px;cursor:pointer;font-family:inherit}
.howbar button:hover{border-color:#56B4E9;color:#56B4E9}
.howlist{display:grid;gap:8px}
details.how{background:rgba(255,255,255,.03);border:1px solid var(--line);border-radius:10px;overflow:hidden}
details.how[open]{border-color:#56B4E9;background:rgba(86,180,233,.05)}
details.how summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:12px;padding:11px 14px;font-size:15px;font-weight:600}
details.how summary::-webkit-details-marker{display:none}
details.how summary::after{content:"+";margin-left:auto;color:#56B4E9;font-size:20px;font-weight:400}
details.how[open] summary::after{content:"\\2212"}
.hn{font-family:Consolas,monospace;font-size:12px;color:#56B4E9;background:rgba(86,180,233,.12);border-radius:6px;padding:2px 7px}
.hb{padding:2px 16px 14px 52px;font-size:14px;line-height:1.6;color:var(--muted)}.hb b{color:var(--text)}
.legend{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:var(--muted);margin:6px 0 10px}
.legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.ins{display:grid;grid-template-columns:minmax(0,1.3fr) 120px minmax(0,1.5fr);gap:14px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.bar{background:var(--line);height:8px;border-radius:4px}.bar span{display:block;height:8px;border-radius:4px}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;max-width:560px}.dow{text-align:center;color:var(--muted);font-size:12px}
.drop{vertical-align:-2px}.day{aspect-ratio:1/1;overflow:hidden;border:1px solid var(--line);border-radius:4px;padding:3px 6px;display:flex;flex-direction:column;justify-content:space-between}.dt{display:flex;justify-content:space-between;align-items:center;line-height:1}.dt .dp{white-space:nowrap}
.day.empty{border:none}.day.today{border-width:2px}.dn{font-size:11px;color:var(--muted)}.dv{font-size:18px;font-weight:600}.dw{font-size:10px;font-weight:400;color:var(--muted);margin-left:4px;white-space:nowrap}
.msg{font-size:14px;line-height:1.5;color:var(--text);margin-top:8px}.lit{font-size:12.5px;line-height:1.5;color:var(--muted);margin-top:12px;padding-left:10px;border-left:3px solid var(--line)}.lit b{display:block;color:var(--text);font-size:12.5px;margin-bottom:2px}.chip{font-size:10.5px;border:1px solid;border-radius:9px;padding:0 6px;margin-left:4px}.cyc{display:flex;gap:26px;flex-wrap:wrap;align-items:center}.cyc>div{flex:1;min-width:260px}.cyc>svg{flex:none}
.dp{font-size:10px;color:#CC79A7}.ch{color:#8d96a3;font-size:11.5px;margin-top:6px;line-height:1.35;border-top:1px solid #2a323d;padding-top:5px}.sl{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:22px}
.big{font-size:40px;font-weight:600;line-height:1.1}.pill{display:inline-block;padding:2px 10px;border-radius:12px;font-size:13px;font-weight:600;margin-left:8px;vertical-align:6px}
.st{display:grid;grid-template-columns:62px 1fr 150px;gap:10px;align-items:center;margin:9px 0;font-size:13.5px}
.track{position:relative;background:var(--line);height:10px;border-radius:5px}.track .rng{position:absolute;top:-2px;height:14px;background:rgba(228,226,220,.18);border-radius:3px}
.track .fill{position:absolute;top:0;height:10px;border-radius:5px}.hyp{width:100%;height:auto;margin-top:6px}
.week{display:flex;gap:8px;align-items:flex-end;height:110px;margin-top:8px}.wk{flex:1;text-align:center;font-size:11.5px;color:var(--muted)}
.wk .b{border-radius:3px 3px 0 0;margin:2px auto 3px;width:70%}.notes li{margin:6px 0}.notes{font-size:13.5px;padding-left:18px;max-width:90ch}
@media(max-width:760px){.sl{grid-template-columns:1fr}.st{grid-template-columns:50px 1fr}.st div:last-child{grid-column:1/3}}
.tbl{border-collapse:collapse;width:100%;font-size:13.5px}.tbl th,.tbl td{text-align:left;padding:6px 12px;border-bottom:1px solid var(--line)}.tbl th{color:var(--muted);font-weight:500}
.foot{margin-top:30px;color:var(--muted);font-size:12.5px;max-width:80ch}
@media(max-width:640px){.ins{grid-template-columns:1fr}.hero h1{font-size:28px}.dp{display:none}}
"""


BENCH = {"deep": (13, 23), "rem": (20, 25), "light": (50, 60)}   # approximate typical adult share of sleep time
STAGE_COL = {"deep": DEEP, "light": LIGHT, "rem": REM, "awake": AWAKE}


SCORE_WEIGHTS = {"dur": 35, "recov": 30, "rest": 25, "depth": 10}
SCORE_GOOD, SCORE_FAIR, SCORE_POOR, SCORE_GOOD_TXT = "#3a73d1", "#4b3a9e", "#e3b341", "#6fa0ee"


def score_band(v):
    """(label, bar colour, text colour) for a 0-100 score or a part's share of its points."""
    return (("Excellent", SCORE_GOOD, SCORE_GOOD_TXT) if v >= 90 else ("Good", SCORE_GOOD, SCORE_GOOD_TXT) if v >= 80
            else ("Fair", SCORE_FAIR, "#a79bf0") if v >= 60 else ("Poor", SCORE_POOR, SCORE_POOR))


def sleep_score_table(f):
    """The dashboard's own 0-100 sleep score, for watches that give none. It blends Fitbit's duration-first layout with the
    factors Garmin says it uses. Parts: duration 35 (full at 8 h), recovery 30 (overnight stress, resting heart rate and
    Visible HRV against your own usual), restfulness 25 (movement and time awake), sleep depth 10 (deep-sleep share against your own usual, since a wrist watch's stage split is rough).
    A part with no data is left out of the total (the rest is scaled up to 100) and the night is flagged approx. It never feeds the flare score.
    Returns a DataFrame: points per part (dur, recov, rest, depth), total, approx, and the fractions behind them."""
    n = len(f)
    out = pd.DataFrame(index=f.index, columns=["dur", "recov", "rest", "depth", "total", "approx", "f_stress", "f_hr", "f_hrv", "f_move", "f_awake", "f_depth"], dtype=float)
    out["approx"] = False
    if n == 0 or "sleep_h" not in f:
        return out

    def z_of(col, minn=10):
        x = f[col] if col in f else pd.Series(np.nan, index=f.index)
        return ((x - x.mean()) / x.std()) if x.notna().sum() >= minn and x.std() > 0 else pd.Series(np.nan, index=f.index)
    z_stress = z_of("night_stress")
    z_hrv = z_of("vis_hrv", 8)
    share = f["deep_h"] / f["sleep_h"] if "deep_h" in f else pd.Series(np.nan, index=f.index)
    z_deep = ((share - share.mean()) / share.std()) if share.notna().sum() >= 10 and share.std() > 0 else pd.Series(np.nan, index=f.index)
    mv = f["night_move"] if "night_move" in f else pd.Series(np.nan, index=f.index)
    mv_med = mv.median() if mv.notna().sum() >= 10 else np.nan
    base = f["rhr"].rolling(30, min_periods=10).mean() if "rhr" in f else pd.Series(np.nan, index=f.index)
    for d, r in f.iterrows():
        h = r["sleep_h"]
        if pd.isna(h) or h <= 0:
            continue
        fr = {"dur": min(1.0, h / 8.0)}
        rec = {}
        if not pd.isna(z_stress.get(d, np.nan)):
            rec["f_stress"] = float(np.clip(0.7 - 0.25 * z_stress[d], 0, 1))
        if "rhr" in f and not pd.isna(r["rhr"]) and not pd.isna(base.get(d, np.nan)):
            rec["f_hr"] = float(np.clip(0.6 + (base[d] - r["rhr"]) / 12.0, 0, 1))
        if not pd.isna(z_hrv.get(d, np.nan)):
            rec["f_hrv"] = float(np.clip(0.6 + 0.2 * z_hrv[d], 0, 1))
        if rec:
            fr["recov"] = float(np.mean(list(rec.values())))
        res = {}
        if not pd.isna(r.get("awake_h")):
            res["f_awake"] = 1 - min(1.0, r["awake_h"] / 0.75)
        if not pd.isna(mv.get(d, np.nan)) and not pd.isna(mv_med) and mv_med > 0:
            res["f_move"] = float(np.clip(1 - 0.5 * (mv[d] / mv_med - 0.5), 0, 1))
        if res:
            fr["rest"] = float(np.mean(list(res.values())))
        if not pd.isna(r.get("deep_h")):
            ds = r["deep_h"] / h
            if not pd.isna(z_deep.get(d, np.nan)):          # a wrist watch's stage split is rough, so deep sleep is judged against your own usual share
                out.loc[d, "f_depth"] = float(np.clip(0.75 + 0.25 * z_deep[d], 0, 1))
            else:
                out.loc[d, "f_depth"] = (1.0 if 0.13 <= ds <= 0.30 else max(0.0, 1 - (0.13 - ds) / 0.10) if ds < 0.13 else max(0.0, 1 - (ds - 0.30) / 0.20))
            fr["depth"] = out.loc[d, "f_depth"]
        for k, v in {**rec, **res}.items():
            out.loc[d, k] = v
        got = sum(SCORE_WEIGHTS[k] for k in fr)
        out.loc[d, "total"] = round(100 * sum(SCORE_WEIGHTS[k] * v for k, v in fr.items()) / got)
        for k, v in fr.items():
            out.loc[d, k] = SCORE_WEIGHTS[k] * v                    # points out of the part's own maximum
        out.loc[d, "approx"] = got < 100 or "f_stress" not in rec or "f_move" not in res
    return out


def estimate_sleep_scores(f):
    return sleep_score_table(f)["total"]


def _uc(t):
    return t[:1].upper() + t[1:]


def sleep_score_card_html(f):
    """Ring, four coloured part bars and the last 7 nights. Bars are coloured by how much of their own points they earned."""
    tbl = sleep_score_table(f)
    ok = tbl["total"].dropna()
    if ok.empty:
        return ""
    d = ok.index[-1]
    r, row = tbl.loc[d], f.loc[d]
    tot = int(r["total"])
    label, col, txt = score_band(tot)
    circ = 2 * 3.14159 * 52
    h = row["sleep_h"]

    def part(name, key, why, miss):
        mx = SCORE_WEIGHTS[key]
        v = r[key]
        if pd.isna(v):
            return (f"<div class='sc-part'><div class='sc-pt'><b>{name}</b><span>not measured</span></div><div class='sc-tr'></div><div class='sc-pd'>{miss}</div></div>")
        c = score_band(v / mx * 100)[1]
        return (f"<div class='sc-part'><div class='sc-pt'><b>{name}</b><span>{v:.0f}/{mx}</span></div>"
                f"<div class='sc-tr'><i style='width:{v / mx * 100:.0f}%;background:{c}'></i></div><div class='sc-pd'>{why}</div></div>")
    bits = []
    if not pd.isna(r["f_stress"]):
        bits.append("overnight stress " + ("lower than" if r["f_stress"] >= 0.7 else "about the same as" if r["f_stress"] >= 0.55 else "higher than") + " usual")
    if not pd.isna(r["f_hr"]):
        bits.append("sleeping heart rate " + ("below" if r["f_hr"] >= 0.65 else "near" if r["f_hr"] >= 0.5 else "above") + " your usual")
    if not pd.isna(r["f_hrv"]):
        bits.append("Visible HRV " + ("above" if r["f_hrv"] >= 0.65 else "near" if r["f_hrv"] >= 0.5 else "below") + " usual")
    rbits = []
    if not pd.isna(row.get("awake_h")):
        rbits.append(f"{int(round(row['awake_h'] * 60))} min awake")
    if not pd.isna(r["f_move"]):
        rbits.append("movement " + ("lighter than" if r["f_move"] >= 0.8 else "about like" if r["f_move"] >= 0.55 else "heavier than") + " usual")
    deep = ""
    if not pd.isna(row.get("deep_h")) and h:
        ds = row["deep_h"] / h * 100
        fd = r["f_depth"]
        deep = f"deep sleep {ds:.0f}% of the night, " + ("above" if fd >= 0.85 else "near" if fd >= 0.6 else "below") + " your usual"
    parts = (part("Duration", "dur", f"{int(h)} h {int(round((h % 1) * 60)):02d} m asleep, full marks at about 8 h", "")
             + part("Recovery", "recov", _uc("; ".join(bits)) if bits else "", "needs overnight stress or heart-rate data")
             + part("Restfulness", "rest", _uc(", ".join(rbits)) if rbits else "", "needs movement or awake time")
             + part("Sleep depth", "depth", _uc(deep), "this watch gave no stages for the night"))
    wk = ""
    for day, v in tbl["total"].iloc[-7:].items():
        if pd.isna(v):
            wk += f"<div class='sc-d'><div class='sc-n'>&nbsp;</div><div class='sc-b'></div><div>{day:%a}</div></div>"
            continue
        c = score_band(v)[1]
        wk += (f"<div class='sc-d'><div class='sc-n'>{'~' if tbl.loc[day, 'approx'] else ''}{int(v)}</div>"
               f"<div class='sc-b'><i style='height:{v:.0f}%;background:{c}'></i></div><div>{day:%a}</div></div>")
    miss = []
    if f["night_move"].notna().sum() == 0:
        miss.append("movement (it is saved from the next Garmin pull)")
    if f["night_stress"].notna().sum() == 0:
        miss.append("overnight stress")
    note = ("A part with no data is left out and the rest scaled to 100; those nights show a ~. "
            + (f"Not yet available: {' and '.join(miss)}. " if miss else "")
            + "This is the dashboard's own estimate, not a Garmin number, and the weights are a judgment call, not a validated formula.")
    return (f"<div class='panel sc'><div class='sc-top'><div class='sc-ring'><svg width='150' height='150' viewBox='0 0 150 150'>"
            f"<circle cx='75' cy='75' r='52' fill='none' stroke='#232c39' stroke-width='12'/>"
            f"<circle cx='75' cy='75' r='52' fill='none' stroke='{col}' stroke-width='12' stroke-linecap='round' stroke-dasharray='{circ:.1f}' "
            f"stroke-dashoffset='{circ * (1 - tot / 100):.1f}' transform='rotate(-90 75 75)'/></svg>"
            f"<div class='sc-v'><b>{tot}</b><span style='color:{txt}'>{label}</span><em>{'estimate' if r['approx'] else 'estimate'}</em></div></div>"
            f"<div class='sc-parts'>{parts}</div></div><div class='sc-wk'>{wk}</div>"
            f"<div class='muted' style='margin-top:12px;font-size:12px;line-height:1.5'>Night ending {d:%A, %b %d}. 90+ Excellent, 80 to 89 Good, 60 to 79 Fair, under 60 Poor. "
            f"Bars: deep blue is 80% or more of that part's points, purple 60 to 79%, amber under 60%. {note}</div></div>")


SCORE_CSS = """
.sc-top{display:flex;gap:28px;align-items:center;flex-wrap:wrap}
.sc-ring{position:relative;width:150px;height:150px;flex:none}
.sc-v{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.sc-v b{font-size:44px;line-height:1}.sc-v span{font-weight:600;margin-top:4px;font-size:14px}.sc-v em{font-style:normal;color:var(--muted);font-size:11px;margin-top:2px}
.sc-parts{flex:1;min-width:260px}.sc-part{margin-bottom:11px}
.sc-pt{display:flex;justify-content:space-between;font-size:14px}.sc-pt span{color:var(--muted)}
.sc-tr{height:8px;background:#232c39;border-radius:5px;margin:5px 0 3px;overflow:hidden}.sc-tr i{display:block;height:100%;border-radius:5px}
.sc-pd{font-size:11.5px;color:var(--muted)}
.sc-wk{display:flex;gap:12px;margin-top:20px}.sc-d{flex:1;text-align:center;font-size:12px;color:var(--muted)}
.sc-b{height:70px;background:#202835;border-radius:6px;display:flex;align-items:flex-end;margin:3px 0}.sc-b i{display:block;width:100%;border-radius:6px}
.sc-n{color:var(--text);font-weight:600;min-height:16px}
.ex-bar{position:relative;height:14px;background:#232c39;border-radius:8px}.ex-fill{position:absolute;left:0;top:0;height:100%;border-radius:8px}
.ex-mk{position:absolute;top:-4px;height:22px;border-left:2px solid}
"""


def hypnogram(levels, has_rem=True, movement=None):
    segs = [(dt.datetime.fromisoformat(a), dt.datetime.fromisoformat(b), st) for a, b, st in levels]
    t0, t1 = min(a for a, _, _ in segs), max(b for _, b, _ in segs)
    span = (t1 - t0).total_seconds() or 1.0
    rows, x0, x1 = ["awake", "rem", "light", "deep"] if has_rem else ["awake", "light", "deep"], 46, 636
    segs = [x for x in segs if x[2] in rows]
    if not segs:
        return ""
    height = 26 + len(rows) * 28 + (14 if movement else 0)
    axis_y = height - 4 - (14 if movement else 0)
    out = [f"<svg viewBox='0 0 640 {height}' class='hyp'>"]
    for i, name in enumerate(rows):
        y = 6 + i * 28
        out.append(f"<text x='0' y='{y + 15}' fill='{MUTED}' font-size='11'>{'REM' if name == 'rem' else name.title()}</text>"
                   f"<line x1='{x0}' x2='{x1}' y1='{y + 10}' y2='{y + 10}' stroke='#2a323d' stroke-width='1'/>")
    for a, b, st in segs:
        x = x0 + (a - t0).total_seconds() / span * (x1 - x0)
        w = max(1.5, (b - a).total_seconds() / span * (x1 - x0))
        out.append(f"<rect x='{x:.1f}' y='{6 + rows.index(st) * 28}' width='{w:.1f}' height='20' rx='2' fill='{STAGE_COL[st]}'/>")
    if movement:                                                                  # white movement line over the stages, like Garmin's
        mv = []
        for ts, lv in movement:
            try:
                mv.append((dt.datetime.fromisoformat(ts), float(lv)))
            except ValueError:
                pass
        mv = [m for m in mv if t0 <= m[0] <= t1]
        if len(mv) > 2:
            top = max(1.0, max(v for _, v in mv))
            y_top, y_bot = 6, 6 + (len(rows) - 1) * 28 + 20
            pts = " ".join(f"{x0 + (a - t0).total_seconds() / span * (x1 - x0):.1f},{y_bot - min(v / top, 1) * (y_bot - y_top):.1f}" for a, v in mv)
            out.append(f"<polyline fill='none' stroke='#ffffff' stroke-width='1.4' stroke-linejoin='round' opacity='0.85' points='{pts}'/>")
            out.append(f"<line x1='{x1 - 74}' x2='{x1 - 56}' y1='{height - 8}' y2='{height - 8}' stroke='#ffffff' stroke-width='1.6'/>"
                       f"<text x='{x1 - 52}' y='{height - 4}' fill='{MUTED}' font-size='10'>Movement</text>")
    t = t0.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    while t < t1:
        x = x0 + (t - t0).total_seconds() / span * (x1 - x0)
        out.append(f"<text x='{x:.1f}' y='{axis_y}' fill='{MUTED}' font-size='10' text-anchor='middle'>{t:%I %p}</text>")
        t += timedelta(hours=2 if span > 6 * 3600 else 1)
    return "".join(out) + "</svg>"


def build_sleep_panel(f, raw_sleep):
    s = f["sleep_h"].dropna()
    if s.empty:
        return "<div class='panel muted'>No sleep data yet.</div>"
    d = s.index[-1]
    r = f.loc[d]
    hrs = r["sleep_h"]
    sc = r["sleep_score"]
    est = r["sleep_src"] == "est"
    manual = r["sleep_src"] == "manual"
    has_rem = bool(f.attrs.get("has_rem"))
    est_sc = estimate_sleep_scores(f)
    guessed = pd.isna(sc) and not pd.isna(est_sc.get(d, np.nan))
    if guessed:
        sc = est_sc[d]
    scol = MUTED if pd.isna(sc) else BETTER if sc >= 80 else WATCH if sc >= 60 else WARN
    pill = "" if pd.isna(sc) else (f"<span class='pill' style='background:{scol}33;color:{scol}' title='The dashboard's own estimate from your sleep time, deep sleep, time awake and resting heart rate. Your watch does not give a sleep score.'>"
                                   f"{int(sc)}{' est.' if (est or guessed) else ''}</span>")
    left = (f"<div class='muted'>Night ending {d:%A, %b %d}</div><div class='big'>{int(hrs)}h {int(round((hrs % 1) * 60)):02d}m{pill}</div>"
            f"<div class='muted'>{r['bed']} to {r['wake']}"
            f"{' | estimated from heart rate only, no stages' if est else ' | times you entered, no stages' if manual else ''}</div>")
    stages = ""
    if not pd.isna(r["deep_h"]) and hrs > 0:
        for key, col in (("deep", "deep_h"), ("rem", "rem_h"), ("light", "light_h")):
            if key == "rem" and not has_rem:
                continue
            pct = r[col] / hrs * 100
            lo, hi = BENCH[key]
            verdict = "within typical range" if lo <= pct <= hi else ("below typical" if pct < lo else "above typical")
            stages += (f"<div class='st'><div>{'REM' if key == 'rem' else key.title()}</div><div class='track'>"
                       f"<div class='rng' style='left:{lo}%;width:{hi - lo}%'></div>"
                       f"<div class='fill' style='width:{min(pct, 100):.0f}%;background:{STAGE_COL[key]}'></div></div>"
                       f"<div class='muted'>{int(r[col])}h {int(round((r[col] % 1) * 60)):02d}m, {pct:.0f}% ({verdict})</div></div>")
        stages += (f"<div class='st'><div>Awake</div><div></div><div class='muted'>{int(round(r['awake_h'] * 60))} min in bed awake</div></div>"
                   "<div class='muted'>Shaded band = approximate typical adult range.</div>")
    levels = (raw_sleep.get(d.strftime("%Y-%m-%d")) or {}).get("levels")
    hyp = hypnogram(levels, has_rem, (raw_sleep.get(d.strftime('%Y-%m-%d')) or {}).get('movement')) if levels else ""
    right = stages + hyp
    wk = f.iloc[-7:]
    bars = ""
    for day, row in wk.iterrows():
        if pd.isna(row["sleep_h"]):
            bars += f"<div class='wk'><div style='height:70px'></div>{day:%a}</div>"
            continue
        c = BETTER if row["sleep_h"] >= 7 else WATCH if row["sleep_h"] >= 6 else WARN
        wsc = row["sleep_score"] if not pd.isna(row["sleep_score"]) else est_sc.get(day, np.nan)
        bars += (f"<div class='wk'>{'' if pd.isna(wsc) else ('~' if pd.isna(row['sleep_score']) else '') + str(int(wsc))}"
                 f"<div class='b' style='height:{min(row['sleep_h'] / 10, 1) * 70:.0f}px;background:{c}'></div>{row['sleep_h']:.1f}h<br>{day:%a}</div>")
    avg = wk["sleep_h"].mean()
    week = (f"<div class='muted' style='margin-top:14px'>Last 7 nights, average "
            f"{'n/a' if pd.isna(avg) else f'{avg:.1f}h'} (number above each bar is the sleep score; ~ means the dashboard's estimate)</div><div class='week'>{bars}</div>")
    return f"<div class='panel'><div class='sl'><div>{left}{week}</div><div>{right}</div></div></div>"


def build_evidence_html(f):
    """Turns the explanation list into collapsible cards so the page is easy to scan."""
    raw_html = _evidence_ul(f)
    items = re.findall(r"<li>(.*?)</li>", raw_html, flags=re.S)
    cards = ""
    for n, it in enumerate(items, 1):
        m = re.match(r"\s*<b>(.*?)</b>(.*)", it, flags=re.S)
        title, body = (m.group(1).strip().rstrip("."), m.group(2).strip()) if m else (f"Note {n}", it)
        cards += (f"<details class='how'><summary><span class='hn'>{n:02d}</span><span class='ht'>{title}</span></summary>"
                  f"<div class='hb'>{body}</div></details>")
    if not cards:
        return raw_html
    return ("<div class='howbar'><span class='muted'>How each number is worked out, and the research behind it.</span>"
            "<span><button type='button' onclick=\"document.querySelectorAll('details.how').forEach(d=>d.open=true)\">Expand all</button>"
            "<button type='button' onclick=\"document.querySelectorAll('details.how').forEach(d=>d.open=false)\">Collapse all</button></span></div>"
            f"<div class='howlist'>{cards}</div>")


def _evidence_ul(f):
    return ("<ul class='notes'>"
            "<li><b>Colors.</b> The palette avoids green and is checked against the common kinds of color blindness (the red is a deep, dark red that stays distinct from the orange): blue means better than usual, grey "
            "is typical, and yellow, orange and red mean progressively worse. Flags always have words too (card labels and hover text). "
            "Stability bars in blue are estimates; the other colors are Visible's own score.</li>"
            f"<li><b>Your normal.</b> Every baseline is built from your previous {BASELINE_LONG} days (today excluded) at the "
            f"{int(ANCHOR_Q * 100)}th percentile for higher-is-better measures (HRV, sleep score) and the {int((1 - ANCHOR_Q) * 100)}th for "
            "lower-is-better ones (resting HR, stress). That keeps a multi-day flare from turning into your new normal, which is what made "
            "v2 read 5/5 while you felt awful. HRV is log-transformed first (lnRMSSD), the usual scale in HRV research. The window and "
            "percentile are a design choice, not a published standard, and are set at the top of the script.</li>"
            "<li><b>Strain</b> compares resting heart rate, overnight HRV and stress with that baseline "
            "(weights 0.5 / 0.3 / 0.2). 0 is your normal; higher means your body is working harder than usual.</li>"
            "<li><b>Stability (1 to 5)</b> is Visible's own score on days you have one. Otherwise it is estimated: worse-than-usual HRV (0.45), "
            "resting HR (0.35), stress (0.10) and sleep score (0.10) raise a strain-like number, while better-than-usual readings only lower it a little. "
            + ("The cut-offs between 1 to 5 are matched to the spread of your own Visible stability history. " if f.attrs.get("stab_calibrated")
               else "No Visible history was imported, so generic cut-offs are used. ")
            + (f"On the {f.attrs['stab_match'][1]} recent days with both, the estimate landed within 1 point of Visible on {f.attrs['stab_match'][0]}. "
               if f.attrs.get("stab_match", (0, 0))[1] else "") + "</li>"
            f"<li><b>Flare status</b> adds up yes/no signals per day: a body signal (stability at or below {FLARE_STABILITY}, HRV z at or below {FLARE_HRV_Z}, "
            f"or resting-HR z at or above {FLARE_RHR_Z}; a second point if two agree), a logged crash, a daytime nap, and symptom burden "
            f"{FLARE_SYMPTOM_Z} SD above your usual. {FLARE_DAY_POINTS}+ points (or a stability of {FLARE_SOLO_STABILITY}) is a flare day; flare days on 2 of the last {FLARE_WINDOW} days is an active flare. "
            "These thresholds are my starting guesses, not clinical cut-offs. It is a pacing and discussion aid, not a lupus diagnosis.</li>"
            + (f"<li><b>Daytime rest</b> (heart-rate guess is on): {NAP_MIN_MINUTES}+ minutes with heart rate within {NAP_HR_OFFSET} bpm of your resting rate "
               f"between {NAP_HOURS[0]:.0f}:00 and {NAP_HOURS[1]:.0f}:30, outside Garmin's recorded sleep. Quiet sitting can look the same.</li>"
               if AUTO_NAP_DETECT else
               "<li><b>Naps</b> come from Garmin's own nap total when the watch reports one, and from <code>nap</code> in symptoms.csv (1 = napped). "
               "A heart-rate-only nap guess exists but is off by default (AUTO_NAP_DETECT at the top of the script) because it was not reliable on "
               "irregular sleep schedules.</li>")
            + 
            "<li><b>Visible import</b> reads HRV, resting HR, stability, crash, period, infection, sleep rating, functional capacity and every "
            "symptom tracker in the file. Symptom burden is the average of the symptoms logged that day, scaled to 0 to 10. Visible's sleep rating "
            "is shown as the raw code because the scale direction is not documented.</li>"
            f"<li><b>Pace points</b> count time above your own resting heart rate: activity zone from +{ACTIVITY_OFFSET} bpm, "
            f"over-exertion from +{OVEREXERT_OFFSET} bpm at {OVEREXERT_MULT:.0f}x the cost. The offsets follow user-reported descriptions of "
            "Visible and the Workwell resting-HR-plus-15 guideline, and you can change them at the top of the script. "
            "Your day starts when you wake (from Garmin's sleep record), so it works for any sleep schedule, and time recorded as sleep is not counted. "
            f"The ceiling is the {int(CEILING_QUANTILE * 100)}th percentile of your recent days that were not flare days and had enough heart-rate data "
            f"(a median would be passed on half of ordinary days), kept to {int(FLARE_CEILING['active'] * 100)}% while the flare status is Active and "
            f"{int(FLARE_CEILING['watch'] * 100)}% on Possible flare symptoms, and also lowered on high-strain days. These percentages are my starting guesses. "
            "This is an approximation of Visible-style pacing, not Visible's own formula, and a watch cannot tell whether a high heart rate came from "
            "activity or from sitting up or standing, which in POTS can raise it by itself.</li>"
            + ("<li><b>HRV estimate.</b> HRV is the variation in time between heartbeats. The Garmin feed has no beat-to-beat intervals, so this is a relative "
               "index (50 = your typical night, about 10 points per standard deviation) built from overnight stress (0.6), how steady your sleeping heart rate is (0.2) "
               "and how low it sits (0.2). Garmin derives stress from heartbeat timing, which is why it is the main input. "
               "Use it for your own trend, not to compare with milliseconds from another app.</li>"
               if f.attrs.get("hrv_src") == "estimate" else
               "<li><b>HRV</b> here is Garmin's overnight average, so it is a different measurement from a morning spot reading in another app.</li>")
            +
            "<li><b>Taking your HRV.</b> Take it first thing after waking, in the Visible app, before you have moved around much or taken medicine, with a warm, dry "
            "finger fully covering the camera. A cold or damp finger gives noisy readings, and measuring at a different time each day makes the numbers less comparable.</li>"
            "<li><b>Cycle tracking.</b> Period days come from everything recorded: your daily check-in and symptoms.csv, Garmin's cycle tracking (pulled when you log in and saved raw in "
            "<code>garmin_cache/menstrual.json</code>) and Visible's Period tracker. A period is carried forward from its first logged day for your usual length, or through today while you keep "
            "answering yes, until you answer no. Cycle length is the median of your last 6 gaps between logged starts (gaps over 60 days are ignored as missed logs); the next period is shown as a range "
            "because irregular cycles can't be pinned to a day. Ovulation is placed about 14 days before the next period starts (using the cycle's real length once it is over), or at the last "
            "stretchy or egg-white discharge day if you log it. Phases: menstrual = the period; follicular = until 2 days before ovulation; ovulation window = ovulation &plusmn;1 day; luteal = after. "
            "These are calendar guesses, not measured hormones. The flare heads-up only fires when your own history shows a phase with at least 1.5 times your usual flare rate "
            "over 5 or more days in 2 or more cycles; otherwise it shows general research. Garmin's cycle data layout is not documented, so it is read by field name; "
            "if something is missing, the saved menstrual.json shows what Garmin sent. Periods are also saved to period_cycles.csv. Set TRACK_PERIOD = False to turn all this off.</li>"
            "<li><b>Research used.</b> Peggs et al. 2012 (65 POTS patients and 95 controls): lightheadedness worst in menstruation, best in the follicular phase. "
            "Schmalenberger et al. 2020 (two within-person studies): HRV lowest in the mid-luteal phase and tied to progesterone. WHOOP wearable data: resting heart rate about 2.7 bpm higher "
            "and HRV about 4.7 ms lower in the luteal phase than the follicular. Lupus: no study I found tested cycle phase directly. "
            "<b>HRV and lupus.</b> Thanou et al. 2016 (53 patients with active lupus, 5-minute ECG): lower HRV went with higher disease activity, and a rising RMSSD between visits went with falling SLEDAI. "
            "Flare was only compared at the same visit, so it does not show that low HRV comes before a flare. A 2015 ACR abstract from the same group found the flare link vanished after adjustment. "
            "A 55-woman study with mild or inactive lupus (PMC7766283) found no link between HRV and SLEDAI, and exercise did not change HRV. Visible's study of 4,244 users (ME/CFS and long COVID) found that falling HRV and rising resting heart rate "
            "against your own baseline predicted crashes, mainly once each person's own history was included. Because inflammation is the shared thread in autoimmune conditions, this dashboard treats low HRV (and, from the RA preprint, falling steps) as flare warning signs for all of them, compared with your own usual, and tests it on your own days in the linked-to-what section. In POTS the picture also depends on subtype (Gibbons 2013: lower HRV only in the neuropathic group).</li>"
            "<li><b>Garmin activity.</b> The dashboard uses Garmin heart-rate samples (for pace points), daily steps (timeline and the low-step comparison), sleep, stress, HRV and resting heart rate. "
            "Intensity minutes are saved in the cache but not used, and workouts and Body Battery are not used.</li>"
            "<li><b>Heart rate and posture:</b> a watch can't tell posture, so sitting up or standing counts as activity if it raises your heart rate.</li>"
            "<li><b>symptoms.csv</b> (next to the script): one line a day with <code>date, symptoms (0-10), pem (0 or 1), stand_hr_rise (bpm), "
            "period (1 on flow days), nap (1 or 0), bed and wake (HH:MM, 24-hour), sleep_h (hours actually asleep), mood (1-5), discharge, period_symptoms</code>. Leave any column empty when you have "
            "nothing to enter. <b>Sleep corrections:</b> Garmin's sleep times are sometimes wrong. If you enter bed and wake (or just sleep_h) on the row for "
            "the day you woke up, those replace Garmin's for that night everywhere: sleep hours, the sleep chart, and where your pace-point day starts. "
            "The app also offers to fix your most recent night when it starts. Corrected nights show no sleep stages or score.</li>"
            "<li><b>Saved Visible data.</b> Every Visible file you import is merged into <code>garmin_cache/visible_history.csv</code> (a newer export "
            "wins for any date it covers), so you can skip the file picker later and still see all of it. That file includes your Visible notes, "
            "so keep it private.</li></ul>")


# ----------------------------------------------------------------- flare-prediction backtest
def _fit_logit(X, y, l2=1.0, iters=40):
    Xb = np.column_stack([np.ones(len(X)), X])
    w = np.zeros(Xb.shape[1])
    reg = l2 * np.eye(Xb.shape[1]); reg[0, 0] = 0
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(Xb @ w, -30, 30)))
        W = p * (1 - p) + 1e-6
        step = np.linalg.solve(Xb.T @ (Xb * W[:, None]) + reg + 1e-9 * np.eye(len(w)), Xb.T @ (y - p) - reg @ w)
        w = w + step
        if np.abs(step).max() < 1e-6:
            break
    return w


def _predict_logit(w, X):
    return 1 / (1 + np.exp(-np.clip(np.column_stack([np.ones(len(X)), X]) @ w, -30, 30)))


def _auc(y, p):
    y, p = np.asarray(y), np.asarray(p)
    pos, neg = (y == 1).sum(), (y == 0).sum()
    if pos == 0 or neg == 0:
        return np.nan
    r = pd.Series(p).rank().values
    return float((r[y == 1].sum() - pos * (pos + 1) / 2) / (pos * neg))


def backtest_flares(f, horizon=None):
    """Walk-forward test of a small step + heart-rate model, in the spirit of the RA wearable preprint: from a day you were NOT in a flare, will one start within the
    next `horizon` days? Features use only data up to that day (7-day mean steps and resting-HR z-scores, plus HRV z when you have it). Labels are what you reported
    (the daily flare question) or Visible's stability score (2 or lower = bad day). For every test day the model is refit on days that ended before the
    prediction window began, so nothing from the future leaks in. Returns a dict of counts and, when there is enough data, accuracy figures."""
    H = horizon or BACKTEST_HORIZON
    lab = (f["flare_manual"].where(f["flare_manual"].notna())).combine_first((f["vis_stab"] <= 2).astype(float).where(f["vis_stab"].notna()))
    res = {"H": H, "labeled": int(lab.notna().sum()), "flare_days": int((lab == 1).sum()), "steps_days": int(f["steps"].notna().sum()) if "steps" in f else 0}
    feats = {}
    if "steps_z" in f and f["steps_z"].notna().sum() >= 14:
        feats["steps (7-day average vs your usual)"] = f["steps_z"].rolling(7, min_periods=4).mean()
    feats["resting heart rate (7-day average vs your usual)"] = f["rhr_z"].rolling(7, min_periods=4).mean()
    if f["hrv_z"].notna().sum() >= 20:
        feats["HRV (7-day average vs your usual)"] = f["hrv_z"].rolling(7, min_periods=4).mean()
    res["features"] = list(feats)
    X = pd.DataFrame(feats)
    fut = pd.concat([lab.shift(-k) for k in range(1, H + 1)], axis=1)
    known = fut.notna().sum(axis=1)
    y = pd.Series(np.nan, index=f.index)
    y[(fut == 1).any(axis=1)] = 1.0
    y[(known >= max(3, H // 2)) & ~(fut == 1).any(axis=1)] = 0.0
    last_ok = f.index[-1] - pd.Timedelta(days=H)
    y[y.index > last_ok] = np.where(y[y.index > last_ok] == 1, 1.0, np.nan)      # recent days whose window is incomplete count only if a flare already happened
    eligible = X.notna().all(axis=1) & y.notna() & (lab != 1)                      # start from a non-flare day
    onset = (lab == 1) & (lab.shift(1) != 1)
    res["eligible"], res["eligible_flares"] = int(eligible.sum()), int(onset.sum())
    res["flare_windows"] = int((y[eligible] == 1).sum())
    res["ready"] = res["labeled"] >= BACKTEST_MIN_LABELED and res["eligible_flares"] >= BACKTEST_MIN_FLARES and len(feats) >= 2
    if not res["ready"]:
        return res
    idx = list(f.index[eligible])
    Xs, ys = X[eligible], y[eligible]
    preds, truth, warn_thr = [], [], []
    for i, t in enumerate(idx):
        tr = [d for d in idx if d <= t - pd.Timedelta(days=H)]
        if len(tr) < 30 or int((ys[tr] == 1).sum()) < 4 or int((ys[tr] == 0).sum()) < 4:
            continue
        mu, sd = Xs.loc[tr].mean(), Xs.loc[tr].std().replace(0, 1)
        w = _fit_logit(((Xs.loc[tr] - mu) / sd).values, ys[tr].values)
        ptr = _predict_logit(w, ((Xs.loc[tr] - mu) / sd).values)
        best_j, thr = -1, 0.5
        for c in np.unique(np.round(ptr, 3)):                       # threshold that best separates the training days
            tp = ((ptr >= c) & (ys[tr].values == 1)).sum(); fn = ((ptr < c) & (ys[tr].values == 1)).sum()
            tn = ((ptr < c) & (ys[tr].values == 0)).sum(); fp = ((ptr >= c) & (ys[tr].values == 0)).sum()
            j = tp / max(tp + fn, 1) + tn / max(tn + fp, 1) - 1
            if j > best_j:
                best_j, thr = j, c
        pt = float(_predict_logit(w, ((Xs.loc[[t]] - mu) / sd).values)[0])
        preds.append(pt); truth.append(float(ys[t])); warn_thr.append(thr)
    if len(preds) < 20 or sum(truth) < 5 or len(preds) - sum(truth) < 5:
        res["ready"] = False
        res["note"] = "Not enough test days yet after holding back the training days."
        return res
    p, t_, th = np.array(preds), np.array(truth), np.array(warn_thr)
    warn = p >= th
    tp, fn = int((warn & (t_ == 1)).sum()), int((~warn & (t_ == 1)).sum())
    tn, fp = int((~warn & (t_ == 0)).sum()), int((warn & (t_ == 0)).sum())
    res.update(n_test=len(p), pos=int(t_.sum()), auc=_auc(t_, p), sens=tp / max(tp + fn, 1), spec=tn / max(tn + fp, 1), ppv=tp / max(tp + fp, 1),
               warnings=int(warn.sum()), base_rate=float(t_.mean()), tp=tp, fn=fn, tn=tn, fp=fp)
    rng_ = np.random.default_rng(0)
    aucs = []
    for _ in range(300):
        b_ = rng_.integers(0, len(p), len(p))
        a_ = _auc(t_[b_], p[b_])
        if not np.isnan(a_):
            aucs.append(a_)
    res["auc_lo"], res["auc_hi"] = (float(np.percentile(aucs, 5)), float(np.percentile(aucs, 95))) if aucs else (np.nan, np.nan)
    # today's reading, from a model fit on everything that has a known outcome
    try:
        tr = idx
        mu, sd = Xs.loc[tr].mean(), Xs.loc[tr].std().replace(0, 1)
        w = _fit_logit(((Xs.loc[tr] - mu) / sd).values, ys[tr].values)
        xl = X.iloc[[-1]]
        if xl.notna().all(axis=1).iloc[0]:
            res["today"] = float(_predict_logit(w, ((xl - mu) / sd).values)[0])
    except Exception:
        pass
    return res


def build_backtest_html(f):
    r = backtest_flares(f)
    H = r["H"]
    intro = (f"<h2>Can your own data predict a flare? (backtest)</h2><p class='sub'>Modeled on the rheumatoid arthritis wearable preprint, which used steps and heart rate to predict flares ahead of time. "
             f"Here the same idea is tested honestly on you: for each past day, a small model sees only your steps, resting heart rate and HRV up to that day (as 7-day averages against your usual) and "
             f"guesses whether a flare starts in the next {H} days. It is refit as time goes on using only days that were already over, then scored against what really happened. "
             "That is called a walk-forward test, and it is why the numbers can be trusted more than the ones a model reports about the data it learned from.</p>")
    def row(k, v): return f"<tr><td>{k}</td><td>{v}</td></tr>"
    if not r["ready"]:
        need = []
        if r["labeled"] < BACKTEST_MIN_LABELED:
            need.append(f"{BACKTEST_MIN_LABELED - r['labeled']} more labeled days (days with a flare answer from the daily check-in, or a Visible stability score)")
        if r["eligible_flares"] < BACKTEST_MIN_FLARES:
            need.append(f"{BACKTEST_MIN_FLARES - r['eligible_flares']} more separate flares")
        if r["steps_days"] < 14:
            need.append("daily steps (the next login with Garmin fills these in for the last 120 days)")
        if len(r["features"]) < 2:
            need.append("at least two signals with enough history")
        tbl = ("<table class='tbl'>" + row("Days with a known label (flare answer or Visible stability)", f"{r['labeled']} of {BACKTEST_MIN_LABELED} needed")
               + row("Of those, flare or bad days", r["flare_days"])
               + row("Separate flares that began after a non-flare day", f"{r['eligible_flares']} of {BACKTEST_MIN_FLARES} needed")
               + row("Days of Garmin steps", r["steps_days"])
               + row("Signals available", ", ".join(r["features"]) or "none yet") + "</table>")
        return (intro + "<div class='panel'><div style='font-size:15px;margin-bottom:8px'><b>Not enough of your own history to test yet.</b> "
                "A backtest on a handful of flares would just be noise, so it waits." + (" Still needed: " + "; ".join(need) + "." if need else "") + "</div>" + tbl
                + "<div class='muted' style='margin-top:8px'>The fastest way to get there is answering the daily flare question every day and importing your Visible export regularly. "
                  + (r.get("note", "") or "") + "</div></div>")
    auc = r["auc"]
    lo, hi = r["auc_lo"], r["auc_hi"]
    good = lo > 0.55
    verdict = ("better than chance" if good else "a hint, but not reliable yet" if auc >= 0.62 else "not better than chance yet")
    col = BETTER if good else WATCH if auc >= 0.62 else MUTED
    tbl = ("<table class='tbl'>" + row("Test days (each scored out-of-sample)", r["n_test"])
           + row(f"Test days with a flare starting within {H} days", f"{r['pos']} of {r['n_test']} ({100 * r['base_rate']:.0f}%)")
           + row("Ranking score (AUC): 0.5 = coin flip, 1.0 = perfect", f"{auc:.2f} (plausible range {lo:.2f} to {hi:.2f} given how few days there are)")
           + row("Flares it warned about (sensitivity)", f"{r['tp']} of {r['tp'] + r['fn']} ({100 * r['sens']:.0f}%)")
           + row("Calm stretches it left alone (specificity)", f"{r['tn']} of {r['tn'] + r['fp']} ({100 * r['spec']:.0f}%)")
           + row("When it warned, a flare followed (precision)", f"{100 * r['ppv']:.0f}% of {r['warnings']} warnings (a no-skill guess would be {100 * r['base_rate']:.0f}%)")
           + row("Signals used", ", ".join(r["features"])) + "</table>")
    today = ""
    if "today" in r and good:
        today = (f"<div style='margin-top:10px;padding:10px 12px;border-left:4px solid {col};background:#1a2029;border-radius:4px'>Today's reading: the model puts the chance of a flare "
                 f"starting within {H} days at <b>{100 * r['today']:.0f}%</b> (your usual is {100 * r['base_rate']:.0f}%).</div>")
    return (intro + f"<div class='panel'><div style='font-size:16px;margin-bottom:8px;color:{col}'><b>On your own data so far: {verdict}</b></div>{tbl}{today}"
            "<div class='muted' style='margin-top:8px'>For comparison, the RA preprint reported 96 to 97% sensitivity and specificity, but on the same data it was built on, so expect real-world numbers to be lower. "
            "Your flare labels come from your own answers and Visible's stability score, which is itself partly based on HRV and resting heart rate, so the HRV signal can look better than it is. "
            "A flare you were already in is excluded: this only counts new flares starting from a day you were not in one. Small numbers swing a lot, so watch whether the result holds as more days come in.</div></div>")


# ----------------------------------------------------------------- mascot
PERIOD_RED = "#D9344F"        # period days: a red teardrop in the calendar, a plain red circle in the timeline strip
PERIOD_GLYPH = "\U0001FA78"   # drop of blood emoji, used in the Plotly timeline strip because Plotly has no teardrop marker
PET_BODY = "#8793A8"          # the mascot's main colour (change this to recolour him)
PET_N = 32                    # the sprite is drawn on a 32 x 32 grid


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _dk(c, f):
    return tuple(int(v * f) for v in c)


def _lt(c, f):
    return tuple(min(255, int(v + (255 - v) * f)) for v in c)


def _ellipse(x0, y0, x1, y1):
    yy, xx = np.mgrid[0:PET_N, 0:PET_N]
    cx, cy, rx, ry = (x0 + x1) / 2.0, (y0 + y1) / 2.0, (x1 - x0 + 1) / 2.0, (y1 - y0 + 1) / 2.0
    return ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0


def _poly(pts):
    yy, xx = np.mgrid[0:PET_N, 0:PET_N]
    m = np.zeros((PET_N, PET_N), dtype=bool)
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi, xj, yj = pts[i][0], pts[i][1], pts[j][0], pts[j][1]
        cond = ((yi > yy) != (yj > yy)) & (xx < (xj - xi) * (yy - yi) / ((yj - yi) or 1e-9) + xi)
        m ^= cond
        j = i
    return m


class _Sprite:
    def __init__(self):
        self.px = {}
        self.alpha = np.zeros((PET_N, PET_N), dtype=bool)

    def shape(self, mask, col, shade=True):
        col = _hex(col) if isinstance(col, str) else col
        sh, hi = _dk(col, 0.80), _lt(col, 0.28)
        out = lambda x, y: not (0 <= x < PET_N and 0 <= y < PET_N and mask[y, x])
        for y, x in zip(*np.nonzero(mask)):
            c = col
            if shade:
                if out(x + 1, y + 1) or out(x, y + 2) or out(x + 2, y):
                    c = sh
                if out(x - 1, y - 1) and not out(x + 1, y + 1):
                    c = hi
            self.px[(int(x), int(y))] = c
        self.alpha |= mask

    def put(self, x, y, c):
        if 0 <= x < PET_N and 0 <= y < PET_N:
            self.px[(x, y)] = _hex(c) if isinstance(c, str) else c
            self.alpha[y, x] = True

    def finish(self):
        src = dict(self.px)
        for y in range(PET_N):
            for x in range(PET_N):
                if (x, y) in src:
                    continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    n = src.get((x + dx, y + dy))
                    if n:
                        self.px[(x, y)] = _dk(n, 0.40)
                        break
        return self.px


def _svg(px, extra="", cls=""):
    """Merges horizontal runs of one colour into rectangles."""
    rows = {}
    for (x, y), c in px.items():
        rows.setdefault((y, c), []).append(x)
    parts = []
    for (y, c), xs in sorted(rows.items()):
        xs.sort()
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            parts.append(f"<rect x='{start}' y='{y}' width='{prev - start + 1}' height='1' fill='#{c[0]:02x}{c[1]:02x}{c[2]:02x}'/>")
            if x is not None:
                start = prev = x
    return f"<svg class='{cls}' viewBox='0 0 {PET_N} {PET_N}' shape-rendering='crispEdges' xmlns='http://www.w3.org/2000/svg'>{''.join(parts)}{extra}</svg>"


INK, WHITE, CHEEK = "#26303b", "#ffffff", "#f4b08a"


def _pet_px(state, frame=0):
    """One pose of the mascot: a derpy little T-rex-style dinosaur, side view facing right, as {(x, y): colour}.
    States: walk (frame 0 or 1), rest, blanket, strain, happy."""
    body = _hex(PET_BODY)
    belly, spike, foot, tooth = _hex("#ddd5c2"), _hex("#f2b134"), _dk(body, 0.88), _hex("#ffffff")
    s = _Sprite()
    lying = state in ("rest", "blanket")
    oy = -2 if state == "happy" else (3 if lying else 0)
    lift = 1 if (state == "walk" and frame == 1) else 0
    # tail, body, neck
    s.shape(_ellipse(0, 19 + oy, 8, 24 + oy), body)
    s.shape(_ellipse(4, 16 + oy, 13, 25 + oy), body)
    s.shape(_ellipse(7, 11 + oy, 22, 27 + oy), body)
    s.shape(_ellipse(14, 7 + oy, 24, 19 + oy), body)
    # back spikes: tall upright points along the spine, tail to neck
    tops = {}
    for (xx, yy) in s.px:
        tops[xx] = min(tops.get(xx, 99), yy)
    for x, h in ((2, 2), (6, 3), (10, 4), (14, 4), (18, 3)):
        if x not in tops:
            continue
        base = min(tops.get(x + d, 99) for d in (-1, 0, 1))
        for dx in (-1, 0, 1):
            col_top = tops.get(x + dx, tops[x])
            peak = base - h + (0 if dx == 0 else max(1, h - 1))
            for y in range(peak, col_top):
                s.put(x + dx, y, spike)
    s.shape(_ellipse(9, 19 + oy, 21, 27 + oy), belly, False)                                          # belly
    if not lying:                                                                                       # thick legs with forward feet
        for lx, ly in ((7 + lift, 0), (15 - lift, 0)):
            s.shape(_ellipse(lx, 22, lx + 7, 29), body)
            s.shape(_ellipse(lx - 1, 28 - lift * (lx < 12), lx + 8, 31 - lift * (lx < 12)), foot)
    s.shape(_ellipse(20, 17 + oy, 24, 20 + oy), body)                                                   # tiny T-rex arm
    s.put(24, 19 + oy, tooth); s.put(24, 20 + oy, tooth)                                                # claws
    s.shape(_ellipse(15, 1 + oy, 31, 14 + oy), body)                                                    # big derpy head
    s.put(30, 6 + oy, _dk(body, 0.5))                                                                   # nostril
    ex, ey = 23, 5 + oy                                                                                  # eye
    if state == "walk":
        for dy in range(3):
            for dx in range(3):
                s.put(ex + dx, ey + dy, WHITE)
        s.put(ex + 2, ey + 1, INK); s.put(ex + 2, ey + 2, INK)                                          # pupil drifting off to the side
    elif state == "strain":                                                                             # eyes squeezed shut: > <
        s.put(ex, ey, INK); s.put(ex + 1, ey + 1, INK); s.put(ex, ey + 2, INK)
        s.put(ex + 3, ey, INK); s.put(ex + 2, ey + 1, INK); s.put(ex + 3, ey + 2, INK)
    elif state == "happy":
        s.put(ex, ey + 2, INK); s.put(ex + 1, ey + 1, INK); s.put(ex + 2, ey + 1, INK); s.put(ex + 3, ey + 2, INK)
    elif state == "blanket":                                                                            # awake and miserable: big teary eyes, worried brows
        for dy in range(4):
            for dx in range(4):
                s.put(ex + dx, ey + dy, WHITE)
        s.put(ex + 2, ey, INK); s.put(ex + 3, ey, INK); s.put(ex + 2, ey + 1, INK); s.put(ex + 3, ey + 1, INK)   # looking up, pleading
        s.put(ex, ey - 3, INK); s.put(ex + 1, ey - 3, INK); s.put(ex + 2, ey - 2, INK); s.put(ex + 3, ey - 2, INK)
        for dy in (4, 5):
            s.put(ex + 1, ey + dy, "#7cc8ff")
    else:                                                                                               # asleep
        for dx in range(4):
            s.put(ex + dx, ey + 2, INK)
    my = 10 + oy
    if state == "strain":                                                                               # gritted teeth
        for x in range(24, 30):
            s.put(x, my, INK); s.put(x, my + 2, INK)
            s.put(x, my + 1, tooth if x % 2 == 0 else INK)
    elif state == "happy":
        for x in range(24, 30):
            s.put(x, my, INK)
        for x in range(26, 29):
            s.put(x, my + 1, "#e0585f"); s.put(x, my + 2, "#e0585f")                                    # tongue out
        s.put(25, my - 1, tooth); s.put(28, my - 1, tooth)
    elif state == "blanket":                                                                            # wobbly frown
        for x in range(25, 29):
            s.put(x, my + 1, INK)
        s.put(24, my + 2, INK); s.put(29, my + 2, INK)
    else:
        for x in range(24, 30):
            s.put(x, my + 1, INK)
        if state == "walk":
            s.put(25, my, tooth); s.put(28, my, tooth)
    if state == "strain":                                                                               # red-faced, and something coming out the back
        for x in range(20, 24):
            s.put(x, 9 + oy, "#e0585f"); s.put(x, 8 + oy, "#e0585f")
        brown, brown2 = _hex("#7a4a2a"), _hex("#9a643a")
        for x, y, c in ((1, 25, brown), (2, 25, brown), (1, 26, brown), (2, 26, brown2), (3, 26, brown), (0, 27, brown), (1, 27, brown2), (2, 27, brown), (3, 27, brown2), (4, 27, brown)):
            s.put(x, y, c)
    elif state != "blanket":
        s.put(21, 9 + oy, CHEEK); s.put(22, 9 + oy, CHEEK)
    if state == "blanket":
        b, b2, b3 = _hex("#6f93d8"), _hex("#93b4ee"), _hex("#4c6fb5")
        for y in range(21, 31):
            for x in range(4, 27):
                s.px[(x, y)] = b2 if ((x + y) // 3) % 2 == 0 else b
                s.alpha[y, x] = True
        for x in range(4, 27):
            s.px[(x, 21)] = _lt(b2, 0.3)
            s.px[(x, 30)] = b3
    return s.finish()


_Z = ["11111", "00010", "00100", "01000", "11111"]
_BANG = ["010", "010", "010", "010", "000", "010"]


def _glyph(bits, x, y, color, cls=""):
    rects = "".join(f"<rect x='{x + i}' y='{y + j}' width='1' height='1'/>" for j, row in enumerate(bits) for i, ch in enumerate(row) if ch == "1")
    return f"<g class='{cls}' fill='{color}'>{rects}</g>"


def pet_html(state, caption):
    """state: walk, rest, blanket, strain, happy. Returns the stage (animated with CSS only) plus a caption."""
    if state == "walk":
        inner = (f"<div class='pet-walker'><div class='bob'>"
                 f"<div class='fa'>{_svg(_pet_px('walk', 0))}</div><div class='fb'>{_svg(_pet_px('walk', 1))}</div></div></div>")
    elif state == "blanket":
        sweat = "".join(f"<i class='sw s{i}'></i>" for i in (1, 2))
        meteors = "".join(f"<i class='met mt{i}'></i><i class='imp ip{i}'></i>" for i in (1, 2, 3))
        inner = f"{meteors}<div class='pet-still shiver'>{_svg(_pet_px('blanket'))}{sweat}<i class='tear'></i></div>"
    elif state == "rest":
        zs = "".join(f"<svg class='zz z{i}' viewBox='0 0 5 5' shape-rendering='crispEdges'>{_glyph(_Z, 0, 0, '#b9c4ff')}</svg>" for i in (1, 2, 3))
        inner = f"<div class='pet-still breathe'>{_svg(_pet_px(state))}{zs}</div>"
    elif state == "strain":
        sweat = "".join(f"<i class='sw s{i}'></i>" for i in (1, 2))
        bang = f"<svg class='bang' viewBox='-1 -1 5 8' shape-rendering='crispEdges'><rect x='-1' y='-1' width='5' height='8' fill='#fff' opacity='0'/>{_glyph(_BANG, 0, 0, '#ffd84d')}</svg>"
        inner = f"<div class='pet-still shock'>{_svg(_pet_px('strain'))}{bang}{sweat}</div>"
    else:
        inner = f"<div class='pet-still hopper'>{_svg(_pet_px('happy'))}<i class='sp sa'></i><i class='sp sb'></i></div>"
    return (f"<div class='mascot m-{state}' role='img' aria-label='{_esc(caption)}'><div class='stage'>{inner}<div class='ground'></div></div>"
            f"<div class='mcap'>{_esc(caption)}</div></div>")


def pet_state(f):
    """Picks the mascot's pose and a caption from today's data. Rest comes first, then strain, then a good day, otherwise he walks."""
    last = f.index[-1]
    fl = f["flare_status"].iloc[-1] if "flare_status" in f else "unknown"
    ceil = f["pace_ceiling"].iloc[-1] if "pace_ceiling" in f else np.nan
    sp = f["spoons"].iloc[-1] if "spoons" in f else np.nan
    over = (not pd.isna(sp)) and (not pd.isna(ceil)) and ceil > 0 and sp > ceil
    sl = f["sleep_h"].dropna()
    short = len(sl) > 0 and sl.index[-1] >= last - pd.Timedelta(days=1) and sl.iloc[-1] < 6
    strain = f["strain"].dropna()
    st = float(strain.iloc[-1]) if len(strain) and strain.index[-1] >= last - pd.Timedelta(days=1) else np.nan
    stab = f["stability"].dropna()
    sb = float(stab.iloc[-1]) if len(stab) and stab.index[-1] >= last - pd.Timedelta(days=1) else np.nan
    if fl == "active":
        return "blanket", "Flare signals: time to rest"
    if over:
        return "rest", "Over today's pace ceiling: rest"
    if short:
        return "rest", "Short night: take it easy"
    if fl == "watch" or (not pd.isna(st) and st >= 1.5):
        return "strain", "Feeling the strain"
    if (not pd.isna(sb) and sb >= 4) and (pd.isna(st) or st < 0):
        return "happy", "Good day so far"
    return "walk", "Steady: out for a stroll"


MASCOT_CSS = """
.mascot{display:flex;flex-direction:column;align-items:center;flex:none;width:250px}
.stage{position:relative;width:250px;height:132px;overflow:hidden;border-radius:10px;background:linear-gradient(#10151d,#171e29);border:1px solid var(--line)}
.ground{position:absolute;left:0;right:0;bottom:0;height:14px;background:repeating-linear-gradient(90deg,#26323f 0 8px,#202a36 8px 16px);border-top:2px solid #35455a}
.stage svg{display:block;width:100px;height:100px}
.pet-walker{position:absolute;left:8px;bottom:10px;width:100px;height:100px;animation:stroll 11s linear infinite}
.pet-walker .bob{position:relative;width:100px;height:100px;animation:bob .8s steps(1) infinite}
.pet-walker .fa,.pet-walker .fb{position:absolute;inset:0}
.pet-walker .fa{animation:fa .8s steps(1) infinite}.pet-walker .fb{animation:fb .8s steps(1) infinite}
.pet-still{position:absolute;left:75px;bottom:10px;width:100px;height:100px}
@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
@keyframes bob{0%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes stroll{0%{transform:translateX(0) scaleX(1)}46%{transform:translateX(134px) scaleX(1)}50%{transform:translateX(134px) scaleX(-1)}96%{transform:translateX(0) scaleX(-1)}100%{transform:translateX(0) scaleX(1)}}
.met{position:absolute;width:8px;height:8px;background:#ffd84d;opacity:0;animation:meteor 8s linear infinite;
 box-shadow:3px -5px 0 -1px #f0a030,6px -10px 0 -1.5px #d1612c,9px -15px 0 -2px #7a2a1c}
.mt1{left:70px;top:-14px;--dx:-36px;animation-delay:.6s}.mt2{left:104px;top:-14px;--dx:-46px;animation-delay:3.2s}.mt3{left:46px;top:-14px;--dx:-24px;animation-delay:5.8s}
@keyframes meteor{0%{opacity:0;transform:translate(0,0)}2%{opacity:1}13%{opacity:1;transform:translate(var(--dx),122px)}14%,100%{opacity:0;transform:translate(var(--dx),122px)}}
.imp{position:absolute;bottom:13px;width:28px;height:12px;border-radius:50%;background:radial-gradient(#ffd84d 0,#e08a3c 38%,rgba(224,138,60,0) 72%);opacity:0;animation:impact 8s ease-out infinite}
.ip1{left:24px;animation-delay:.6s}.ip2{left:48px;animation-delay:3.2s}.ip3{left:14px;animation-delay:5.8s}
@keyframes impact{0%,12%{opacity:0;transform:scale(.4)}16%{opacity:.95;transform:scale(1)}34%{opacity:0;transform:scale(2)}100%{opacity:0}}
.shiver{animation:shiver 1.8s ease-in-out infinite}
@keyframes shiver{0%,100%{transform:translateX(-1px)}50%{transform:translateX(1px)}}
.tear{position:absolute;left:61px;top:36px;width:6px;height:9px;background:#7cc8ff;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;animation:tear 1.1s ease-in infinite;opacity:0}
@keyframes tear{0%{transform:translateY(0);opacity:0}20%{opacity:1}100%{transform:translateY(34px);opacity:0}}
.breathe{animation:breathe 3.2s ease-in-out infinite;transform-origin:50% 100%}
@keyframes breathe{0%,100%{transform:scaleY(1)}50%{transform:scaleY(1.035)}}
.zz{position:absolute;width:20px!important;height:20px!important;right:-4px;top:6px;opacity:0;animation:zfloat 3.6s ease-in infinite}
.z2{animation-delay:1.2s;right:6px}.z3{animation-delay:2.4s;right:-14px}
@keyframes zfloat{0%{transform:translate(0,14px) scale(.6);opacity:0}15%{opacity:1}100%{transform:translate(12px,-36px) scale(1.3);opacity:0}}
.shock{animation:shock 4s ease-in-out infinite}
@keyframes shock{0%,40%,100%{transform:translate(0,0)}6%{transform:translateY(-16px)}14%{transform:translateY(0)}50%{transform:translateX(-2px)}62%{transform:translateX(2px)}74%{transform:translateX(-2px)}86%{transform:translateX(0)}}
.bang{position:absolute;width:22px!important;height:34px!important;right:-6px;top:-2px;animation:bangpop 4s infinite;transform-origin:50% 100%}
@keyframes bangpop{0%{opacity:0;transform:scale(.2)}6%{opacity:1;transform:scale(1.3)}14%,70%{opacity:1;transform:scale(1)}80%,100%{opacity:0;transform:scale(.6)}}
.sw{position:absolute;top:18px;width:8px;height:11px;background:#7cc8ff;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;animation:sweat 1.3s ease-in infinite;opacity:0}
.s1{left:6px}.s2{left:84px;animation-delay:.6s}
@keyframes sweat{0%{transform:translate(0,0);opacity:0}20%{opacity:1}100%{transform:translate(-8px,26px);opacity:0}}
.hopper{animation:hop 1.1s ease-in-out infinite}
@keyframes hop{0%,100%{transform:translateY(0)}40%{transform:translateY(-14px)}}
.sp{position:absolute;width:8px;height:8px;background:#ffe27a;clip-path:polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%);animation:twinkle 1.1s steps(2) infinite}
.sa{left:4px;top:10px}.sb{right:2px;top:2px;animation-delay:.5s}
@keyframes twinkle{0%{opacity:1;transform:scale(1)}50%{opacity:.2;transform:scale(.6)}}
.mcap{margin-top:8px;font-family:Consolas,'Cascadia Mono','Courier New',monospace;font-size:12.5px;letter-spacing:.04em;color:var(--muted);text-align:center;text-transform:uppercase}
.noanim .mascot *{animation:none!important}
@media(max-width:700px){.mascot,.stage{width:100%}.hero-main{flex-wrap:wrap}}
"""

_TAB_ICONS = {
    "today": ["00011000", "00111100", "01111110", "11111111", "01100110", "01100110", "01100110", "01111110"],
    "cycle": ["00111100", "01110000", "11100000", "11100000", "11100000", "11100000", "01110000", "00111100"],
    "sleep": ["11111110", "00000110", "00001100", "00011000", "00110000", "01100000", "11111110", "00000000"],
    "pace": ["00001110", "00011100", "00111000", "01111110", "00011100", "00111000", "01110000", "11100000"],
    "timeline": ["00000000", "00000010", "00000101", "10001000", "01010000", "00100000", "11111111", "00000000"],
    "patterns": ["11100111", "10000001", "10000001", "11100111", "11100111", "10000001", "10000001", "11100111"],
    "notes": ["01111110", "11000011", "11011011", "11011011", "11011011", "11011011", "11000011", "01111110"],
    "settings": ["00100100", "01111110", "11000011", "10011001", "10011001", "11000011", "01111110", "00100100"],
}


def tab_icon(key):
    bits = _TAB_ICONS.get(key)
    if not bits:
        return ""
    rects = "".join(f"<rect x='{i}' y='{j}' width='1' height='1'/>" for j, row in enumerate(bits) for i, ch in enumerate(row) if ch == "1")
    return f"<svg class='ti' viewBox='0 0 8 8' shape-rendering='crispEdges' fill='currentColor'>{rects}</svg>"


def build_settings_html():
    state = "ON" if TRACK_PERIOD else "OFF"
    anim = ("<div class='panel' style='margin-bottom:12px'><label style='font-size:15px;cursor:pointer'><input type='checkbox' id='anim-toggle' checked style='margin-right:8px'>"
            "Animate the mascot</label><div class='muted' style='margin-top:4px'>Turn this off for a still picture. "
            "This setting is remembered in this browser only.</div>"
            "<div style='margin-top:12px'><label style='font-size:15px;cursor:pointer'><input type='checkbox' id='lv-toggle' checked style='margin-right:8px'>Emoji and tint on alert cards</label>"
            "<div class='muted' style='margin-top:4px'>Turn this off to keep only the WATCH / HIGH / ALERT word tag and the thicker border. Remembered in this browser only.</div></div>"
            "<div style='margin-top:12px'><label style='font-size:15px'>Graph on the Today cards: <select id='sp-style' style='margin-left:6px'><option value='C'>Dots on your usual range</option><option value='A'>Bars</option></select></label>"
            "<div class='muted' style='margin-top:4px'>Remembered in this browser only.</div></div></div>")
    return (f"<h2>Settings</h2>{anim}<p class='sub'>A web page cannot change settings or delete files on your computer, so the controls live in the PotsZilla app window. "
            f"Open the app and click <b>Settings</b> on the first window (or start it with <code>--settings</code>).</p>"
            f"<div class='panel'><div class='msg'>Cycle data is currently <b>{state}</b>.</div>"
            f"<div class='lit'><b>In the app's Settings window</b>"
            f"<b style='display:inline;font-weight:600;color:var(--text)'>Turn off cycle data</b>: for people who do not have periods or do not want them tracked. When it is on, nothing about periods is requested from Garmin, "
            f"read from saved files, asked in the daily check-in or shown here.<br><br>"
            f"<b style='display:inline;font-weight:600;color:var(--text)'>Delete period data</b>: permanently erases the period, cycle, mood, discharge and cycle-symptom information this app saved on your computer "
            f"(garmin_cache/menstrual.json, period_cycles.csv, the cycle columns in symptoms.csv, period rows in the saved Visible history, and the generated page and CSV). "
            f"It is not sent to the recycle bin and cannot be undone unless you pull the data from its sources again. You must type <i>delete</i> to confirm. "
            f"It does not touch your Garmin account, original Visible export files you downloaded, or any backups or synced copies.</div></div>")


TAB_JS = """
(function(){
  var btns=[].slice.call(document.querySelectorAll('.tabs button')), secs=[].slice.call(document.querySelectorAll('section.tab'));
  function show(k){
    if(!secs.some(function(s){return s.id==='tab-'+k;})) k='today';
    secs.forEach(function(s){s.style.display=(s.id==='tab-'+k)?'block':'none';});
    btns.forEach(function(b){b.classList.toggle('on',b.dataset.tab===k);});
    try{history.replaceState(null,'','#'+k);}catch(e){}
    setTimeout(function(){
      if(window.Plotly){[].slice.call(document.querySelectorAll('#tab-'+k+' .js-plotly-plot')).forEach(function(g){try{Plotly.Plots.resize(g);}catch(e){}});}
      window.dispatchEvent(new Event('resize'));
    },30);
  }
  btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.tab);window.scrollTo(0,0);});});
  var at=document.getElementById('anim-toggle');
  function setAnim(on){document.documentElement.classList.toggle('noanim',!on);if(at)at.checked=on;}
  try{if(localStorage.getItem('pz_anim')==='off')setAnim(false);}catch(e){}
  if(at)at.addEventListener('change',function(){setAnim(at.checked);try{localStorage.setItem('pz_anim',at.checked?'on':'off');}catch(e){}});
  var ss=document.getElementById('sp-style');
  function setSp(v){document.documentElement.classList.toggle('spA-on',v==='A');if(ss)ss.value=v;}
  try{var sv=localStorage.getItem('pz_sp');if(sv==='A')setSp('A');}catch(e){}
  if(ss)ss.addEventListener('change',function(){setSp(ss.value);try{localStorage.setItem('pz_sp',ss.value);}catch(e){}});
  var lt=document.getElementById('lv-toggle');
  function setLv(on){document.documentElement.classList.toggle('nolv',!on);if(lt)lt.checked=on;}
  try{if(localStorage.getItem('pz_lv')==='off')setLv(false);}catch(e){}
  if(lt)lt.addEventListener('change',function(){setLv(lt.checked);try{localStorage.setItem('pz_lv',lt.checked?'on':'off');}catch(e){}});
  show((location.hash||'#today').slice(1));
})();
"""


def build_page(f, fig, loc, raw_sleep, sleep_fig=None, pace_fig=None):
    headline, zc, story, cards = build_cards_and_story(f)
    place = f"{loc['city']}, {loc['state']}" if loc else ""
    cfg = {"displayModeBar": False, "responsive": True}
    sleep_html = ""
    pace_html = ""
    first_js = {"v": True}

    def inc():
        r = "cdn" if first_js["v"] else False
        first_js["v"] = False
        return r
    if sleep_fig is not None:                      # first chart on the page carries the plotly script
        sleep_html = (f"<h2>Sleep history</h2><p class='sub'>Hours slept each night, split by stage when Garmin has stages. The dot above each bar is "
                      f"the Garmin sleep score when your watch has one (blue is better, orange is worse). Hover for bed and wake times. Orange diamonds mark flare days.</p>"
                      f"<div class='panel'>{sleep_fig.to_html(full_html=False, include_plotlyjs=inc(), config=cfg)}</div>")
    if pace_fig is not None:
        lvl, head_, det_, col_ = pace_status(f)
        pace_intro = ("These are the pace points from your Visible export, which replace the app's own heart-rate estimate. The dashed line is today's ceiling: "
                      if f.attrs.get("pace_src") == "visible" else
                      f"Your activity budget, counted from when you wake: time with your heart rate well above your resting rate, "
                      f"similar in spirit to Visible's pacing. Blue is the activity zone, red is over-exertion (costs {OVEREXERT_MULT:.0f}x). The dashed line is today's ceiling: ")
        pace_html = (f"<h2>Pace points</h2><p class='sub'>{pace_intro}"
                     f"the upper end of your usual non-flare days, lowered during flares. The dot above each bar shows how that day went: blue under 80% of the ceiling, yellow 80 to 100%, pink-purple over it.</p>"
                     f"<div class='panel' style='border-left:6px solid {col_};margin-bottom:12px'><div style='font-size:22px;font-weight:700;color:{col_}'>{head_}</div>"
                     f"<div style='font-size:14px;margin-top:4px'>{det_}</div></div>"
                     f"<div class='panel'>{pace_fig.to_html(full_html=False, include_plotlyjs=inc(), config=cfg)}</div>"
                     f"<h2>How much you actually exerted</h2><p class='sub'>Garmin's intensity minutes today, to set beside the pace points above.</p>{build_exertion_html(f)}")
    fig_html = fig.to_html(full_html=False, include_plotlyjs=inc(), config=cfg)
    try:
        backtest_html = build_backtest_html(f)
    except Exception as ex:
        backtest_html = ""
        log(f"Could not run the flare backtest: {ex}")
    legend = (f"<div class='legend'><span><i style='background:{BETTER}'></i>better than usual</span>"
              f"<span><i style='background:{TYPICAL}'></i>typical for you</span>"
              f"<span><i style='background:{WATCH}'></i>a little off</span><span><i style='background:{WARN}'></i>clearly off</span>"
              f"<span><i style='background:{ALERT}'></i>far from usual: rest</span>"
              f"<span><i style='background:rgba(141,150,163,0.35)'></i>grey band = your normal range</span>"
              f"<span>&#9670; flare day &nbsp; {drop_svg(False, 10)} period day (outlined = estimated) &nbsp; &#9660; pressure drop of 3+ hPa: see the Events strip</span>"
              f"<span>Better to worse: blue, grey, yellow, orange, red. Hover or read the card text for exact values.</span></div>")
    vl = f["vis_hrv"].last_valid_index() or f["vis_stab"].last_valid_index()
    vis_line = (f"Visible data loaded, latest reading {vl:%b %d}." if vl is not None else
                "No Visible data loaded, so flare tracking is limited. Run again and choose your Visible export.")
    tabs = [("today", "Today"), ("cycle", "Cycle"), ("sleep", "Sleep")]
    if pace_html:
        tabs.append(("pace", "Pace"))
    tabs += [("timeline", "Timeline"), ("patterns", "Patterns"), ("notes", "How it works"), ("settings", "Settings")]
    if not TRACK_PERIOD:
        tabs = [t for t in tabs if t[0] != "cycle"]
    tab_bar = "<nav class='tabs'>" + "".join(f"<button type='button' data-tab='{k}'>{tab_icon(k)}<span>{n}</span></button>" for k, n in tabs) + "</nav>"
    pace_tab = f"<section class='tab' id='tab-pace'>{pace_html}</section>" if pace_html else ""
    facts = [x.strip() for x in re.split(r"(?<=\.)\s+(?=[A-Z])", story) if x.strip()]
    lead = facts[0] if facts else ""
    chips = "".join(f"<li>{_esc(x)}</li>" for x in facts[1:])
    hero_html = (f"<div class='hero' style='--hc:{zc}'>"
                 f"<div class='hero-top'><span class='pill big'>{f.index[-1]:%A, %B %d, %Y}</span>"
                 + (f"<span class='pill'>&#128205; {_esc(place)}</span>" if place else "")
                 + f"<span class='pill'>{_esc(vis_line)}</span><span class='ver'>PotsZilla v{VERSION}</span></div>"
                 f"<div class='hero-main'>{pet_html(*pet_state(f))}<div><h1>{headline}</h1>"
                 + (f"<p class='lead'>{_esc(lead)}</p>" if lead else "") + "</div></div>"
                 + (f"<ul class='facts'>{chips}</ul>" if chips else "") + "</div>")
    warn = ("<div class='foot'><b>Data notes:</b><br>" + "<br>".join(LOG[:8]) + "</div>") if LOG else ""
    return (f"<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>POTS dashboard v{VERSION}</title><style>{CSS}{MASCOT_CSS}{SCORE_CSS}</style></head><body><div class='wrap'>"
            f"{hero_html}"
            f"{tab_bar}"
            f"<section class='tab' id='tab-today'>{cards}"
            f"<h2 style='margin-top:30px'>Last 8 weeks</h2><p class='sub'>Each day is colored by stability and flares. Hover a day for details.</p><div class='panel'>{build_calendar_html(f)}</div></section>"
            f"<section class='tab' id='tab-cycle'>{build_cycle_html(f)}</section>"
            f"<section class='tab' id='tab-sleep'><h2>Last night's sleep</h2><p class='sub'>Stages, score and the last week at a glance.</p>{build_sleep_panel(f, raw_sleep)}<h2>Sleep score</h2><p class='sub'>The dashboard's own 0 to 100 estimate, built like Fitbit's from duration, recovery, restfulness and depth. Your watch does not give a score.</p>{sleep_score_card_html(f)}"
            f"{sleep_html}</section>"
            f"{pace_tab}"
            f"<section class='tab' id='tab-timeline'><h2>Everything on one timeline</h2><p class='sub'>Every panel shares the same dates. Hover anywhere to see all metrics for that day. "
            f"Strain combines resting heart rate, HRV and stress compared with your own previous {BASELINE_LONG} days.</p>{legend}"
            f"<div class='panel'>{fig_html}</div></section>"
            f"<section class='tab' id='tab-patterns'><h2>What seems linked to what</h2><p class='sub'>Before-and-after comparisons from your own days: what tends to be different after a short night, a day over your ceiling, a pressure drop, or in a cycle phase.</p>"
            f"<div class='panel'>{build_insights_html(f)}</div>{backtest_html}</section>"
            f"<section class='tab' id='tab-settings'>{build_settings_html()}</section>"
            f"<section class='tab' id='tab-notes'><h2>How the numbers are calculated</h2><div class='panel'>{build_evidence_html(f)}</div></section>"
            f"<div class='foot'><b>A friendly note:</b> PotsZilla is a personal tracking tool. It is not designed to diagnose, treat or manage any medical condition, "
            f"and it is not a substitute for advice from your doctor or other healthcare provider. Flare flags, pace points and cycle phases are patterns found in your own data and estimates, not medical findings. "
            f"Please talk with your healthcare team before changing any medication, supplement or treatment plan. The CSV exports may be useful to share with them. "
            f"If you feel seriously unwell, seek medical care. Nights marked estimated come from heart rate alone, and pace points are a heart-rate estimate inspired by Visible, not a Garmin or Visible metric.</div>{warn}"
            f"</div><script>{TAB_JS}</script></body></html>")


def write_exports(f, loc):
    cols = ["rhr", "rhr_z", "stress", "stress_z", "hrv", "hrv_z", "resp", "sleep_h", "deep_h", "rem_h", "light_h",
            "awake_h", "sleep_score", "sleep_src", "bed", "wake", "spoons", "pace_act", "pace_over", "min_act", "min_over", "pace_ceiling",
            "period", "period_est", "cycle_day", "phase", "mood", "discharge", "period_symptoms", "hrv_c_stress", "hrv_c_steady", "hrv_c_low_hr", "p_mean", "p_change", "strain", "stability", "symptoms", "pem", "stand_hr_rise",
            "stab_src", "stab_est", "vis_hrv", "vis_rhr", "vis_stab", "vis_sleep", "vis_infection", "vis_funcap", "nap_min", "flare_score", "flare_status", "flare_why"]
    cols = [c for c in cols if c in f.columns]
    if not TRACK_PERIOD:
        cols = [c for c in cols if c not in ("period", "period_est", "cycle_day", "phase", "mood", "discharge", "period_symptoms")]
    f[cols].round(2).to_csv(EXPORT_CSV)
    try:
        ci = f.attrs.get("cycle") or {}
        if TRACK_PERIOD and ci.get("episodes"):
            st = [e["start"] for e in ci["episodes"]]
            rows = []
            for i, e in enumerate(ci["episodes"]):
                gap = (st[i + 1] - st[i]).days if i + 1 < len(st) else ""
                rows.append({"period_start": e["start"].date(), "period_end_estimated": e["end"].date(), "length_days_used": e["length"], "days_you_logged": e["logged_days"],
                             "cycle_length_days": gap,
                             "note": ("" if gap == "" or gap <= 60 else "gap over 60 days: a period was probably not logged, so this gap is not used for your typical cycle length")
                                     + ("; length is carried forward from the first logged day, not measured" if e["logged_days"] < e["length"] else "")})
            pd.DataFrame(rows).to_csv(PERIOD_EXPORT, index=False)
    except Exception as ex:
        log(f"Could not write period_cycles.csv: {ex}")
    last30 = f.iloc[-30:]
    lines = ["POTS DASHBOARD - DOCTOR SUMMARY", "=" * 40, f"Generated: {date.today()}", ""]
    if loc:
        lines.append(f"Location for pressure data: {loc['city']}, {loc['state']}")
    for name, col, fmt in (("Resting HR (bpm)", "rhr", "{:.0f}"), ("HRV (" + ("estimate index" if f.attrs.get("hrv_src") == "estimate" else "ms") + ")", "hrv", "{:.0f}"), ("Stress", "stress", "{:.0f}"),
                           ("Sleep (h)", "sleep_h", "{:.1f}")):
        s = last30[col].dropna()
        if len(s):
            lines.append(f"Last 30 days {name}: avg {fmt.format(s.mean())}, range {fmt.format(s.min())} to {fmt.format(s.max())}")
    lines.append(f"Days with strain above 1.5 (last {len(f)} days): {int((f['strain'] > 1.5).sum())}")
    lines.append(f"Flare days flagged (last {len(f)} days): {int(f['flare_day'].sum())}; current status: {f['flare_status'].iloc[-1]}")
    lines.append(f"Days with a possible daytime nap: {int((f['nap_min'] >= NAP_MIN_MINUTES).sum())}")
    if f["vis_stab"].notna().any():
        lines.append(f"Visible data in this window: {int(f['vis_hrv'].notna().sum())} HRV readings, {int(f['vis_stab'].notna().sum())} stability scores")
    lines.append(f"Days with pressure drop of 3+ hPa: {int((f['p_change'] < PRESSURE_DROP_HPA).sum())}")
    lines += ["", "Sleep stages and HRV: Garmin, when the watch provides them. Nights flagged 'est' in the CSV were estimated from heart rate only.",
              f"Strain compares each day with the person's previous {BASELINE_LONG} days. Flare flags combine HRV, resting HR, stability, crashes, naps and symptoms. "
              "Personal tracking only, not a medical evaluation."]
    EXPORT_TXT.write_text("\n".join(lines))


def build_report(raw, start, end, visible=None):
    f = build_frame(raw, start, end, visible)
    if f[["rhr", "hrv", "stress", "sleep_h"]].notna().sum().sum() == 0:
        return None, f
    return build_page(f, build_figure(f), raw.get("loc"), raw["sleep"], build_sleep_figure(f), build_pace_figure(f)), f


# ----------------------------------------------------------------- GUI
def dino_icon(win):
    """Puts the mascot dino in a window's title-bar/taskbar icon (replaces Tk's default feather). Never stops the app if it fails."""
    try:
        px = _pet_px("walk", 0)
        xs, ys = [k[0] for k in px], [k[1] for k in px]
        x0, y0 = min(xs), min(ys)
        img = tk.PhotoImage(width=max(xs) - x0 + 1, height=max(ys) - y0 + 1)
        for (x, y), c in px.items():
            img.put("#%02x%02x%02x" % tuple(int(v) for v in c[:3]), (x - x0, y - y0))
        img = img.zoom(2)
        win.iconphoto(True, img)
        win._dino_icon = img            # keep a reference, or Tk drops the image
    except Exception:
        pass


def show_error(title, text):
    """Errors go to the console, to garmin_error_log.txt, and to a window whose text you can select and copy."""
    print(text, file=sys.stderr)
    try:
        ERROR_LOG.write_text(text, encoding="utf-8")
    except OSError:
        pass
    if not tk:
        return
    w = tk.Tk()
    dino_icon(w)
    w.title(title)
    box = tk.Text(w, width=100, height=26, wrap="word")
    box.insert("1.0", text + f"\n\n(Also saved to {ERROR_LOG})")
    box.pack(padx=10, pady=10)

    def copy():
        w.clipboard_clear()
        w.clipboard_append(text)
        w.update()
    tk.Button(w, text="Copy to clipboard", command=copy).pack(side="left", padx=10, pady=(0, 10))
    tk.Button(w, text="Close", command=w.destroy).pack(side="left", pady=(0, 10))
    w.mainloop()



class Progress:
    def __init__(self):
        self.root = tk.Tk()
        dino_icon(self.root)
        self.root.title(f"POTS dashboard v{VERSION}")
        self.root.configure(bg="#12161c")
        self.root.geometry("380x170")
        self.status = tk.Label(self.root, text="Starting...", font=("Segoe UI", 11), bg="#12161c", fg="white")
        self.status.pack(pady=(25, 10))
        self.bar = ttk.Progressbar(self.root, length=320, mode="determinate")
        self.bar.pack(pady=5)
        self.detail = tk.Label(self.root, text="", font=("Segoe UI", 9), bg="#12161c", fg="#8d96a3")
        self.detail.pack(pady=5)
        self.root.update()

    def update(self, status, pct=None, detail=""):
        self.status.config(text=status)
        if pct is not None:
            self.bar.config(value=pct)
        self.detail.config(text=detail)
        self.root.update()

    def destroy(self):
        try:
            self.root.destroy()
        except Exception:
            pass


def settings_window(parent=None):
    """Settings: turn cycle data off, or permanently delete everything period-related stored by this app."""
    if not tk:
        return
    BG_, FG_, MU_ = "#12161c", "white", "#8d96a3"
    own = parent is None
    win = tk.Tk() if own else tk.Toplevel(parent)
    dino_icon(win)
    win.title("PotsZilla settings")
    win.configure(bg=BG_)
    win.resizable(False, False)
    tk.Label(win, text="Settings", font=("Segoe UI", 15, "bold"), bg=BG_, fg=FG_).pack(padx=24, pady=(18, 4), anchor="w")
    off_v = tk.BooleanVar(value=not apply_settings() if TRACK_PERIOD_DEFAULT else True)
    note = tk.Label(win, text="", bg=BG_, fg=MU_, font=("Segoe UI", 9), justify="left", wraplength=430)

    def refresh_note():
        note.config(text=("Cycle data is OFF. Nothing about periods is requested from Garmin, read from saved files, asked in the daily check-in or shown on the dashboard."
                          if off_v.get() else "Cycle data is ON."))

    def toggle():
        d = load_settings()
        d["track_period"] = not off_v.get()
        try:
            save_settings(d)
        except OSError as ex:
            messagebox.showerror("Settings", f"Could not save the setting: {ex}", parent=win)
        apply_settings()
        refresh_note()
    tk.Checkbutton(win, text="Turn off cycle data", variable=off_v, command=toggle, bg=BG_, fg=FG_, selectcolor="#1a2029", activebackground=BG_,
                   activeforeground=FG_, font=("Segoe UI", 11)).pack(padx=24, pady=(10, 0), anchor="w")
    tk.Label(win, text="For people who do not have periods or do not want them tracked. Data already saved stays on this computer until you delete it below; it is just not used.",
             bg=BG_, fg=MU_, font=("Segoe UI", 9), justify="left", wraplength=430).pack(padx=46, pady=(0, 4), anchor="w")
    note.pack(padx=46, pady=(0, 10), anchor="w")
    refresh_note()

    def delete_clicked():
        confirm_delete_period_data(win)
    tk.Frame(win, bg="#2a323d", height=1).pack(fill="x", padx=24, pady=6)
    tk.Label(win, text="Today's check-in", font=("Segoe UI", 11, "bold"), bg=BG_, fg=FG_).pack(padx=24, anchor="w")
    tk.Label(win, text="Already answered the flare or period question today and want to change it? Your answers are shown and can be edited. "
                       "The dashboard picks up the change the next time you run it.", bg=BG_, fg=MU_, font=("Segoe UI", 9), justify="left",
             wraplength=430).pack(padx=24, pady=(0, 8), anchor="w")

    def change_today():
        try:
            ask_flare_checkin(win, force=True)
        except Exception as ex:
            messagebox.showerror("Check-in", f"Could not open the check-in: {ex}", parent=win)
    tk.Button(win, text="Change today's answers...", command=change_today, font=("Segoe UI", 10, "bold"), padx=14, pady=5).pack(padx=24, pady=(0, 10), anchor="w")
    tk.Frame(win, bg="#2a323d", height=1).pack(fill="x", padx=24, pady=6)
    tk.Label(win, text="Delete period data", font=("Segoe UI", 11, "bold"), bg=BG_, fg=FG_).pack(padx=24, anchor="w")
    tk.Label(win, text="Permanently erases the period, cycle, mood, discharge and cycle-symptom information this app has saved on this computer. "
                       "Your other data is kept.", bg=BG_, fg=MU_, font=("Segoe UI", 9), justify="left", wraplength=430).pack(padx=24, pady=(0, 8), anchor="w")
    tk.Button(win, text="Delete period data...", command=delete_clicked, bg="#b3261e", fg="white", relief="flat", font=("Segoe UI", 10, "bold"),
              padx=14, pady=5).pack(padx=24, pady=(0, 6), anchor="w")
    tk.Button(win, text="Close", command=win.destroy, font=("Segoe UI", 10), padx=14).pack(padx=24, pady=(10, 18), anchor="e")
    if own:
        win.mainloop()
    else:
        win.transient(parent)
        win.grab_set()
        parent.wait_window(win)


def confirm_delete_period_data(parent):
    """Warning plus a typed 'delete' before anything is erased."""
    BG_, FG_, MU_ = "#12161c", "white", "#8d96a3"
    win = tk.Toplevel(parent)
    win.title("Delete period data")
    win.configure(bg=BG_)
    win.resizable(False, False)
    win.geometry("600x600")
    win.minsize(560, 520)
    # the typing box and the buttons are packed first, at the bottom, so they can never be pushed off the window
    row = tk.Frame(win, bg=BG_)
    row.pack(side="bottom", padx=24, pady=(6, 16), fill="x")
    v = tk.StringVar()
    ent = tk.Entry(win, textvariable=v, width=24, font=("Segoe UI", 13))
    ent.pack(side="bottom", padx=24, pady=(2, 8), anchor="w")
    folder = {"p": str(HERE)}
    folder_lbl = tk.Label(win, text="", bg=BG_, fg=MU_, font=("Segoe UI", 9), justify="left", wraplength=540)

    def show_folder():
        folder_lbl.config(text=f"Will look for the app's files in:  {folder['p']}")

    def choose_folder():
        d = filedialog.askdirectory(parent=win, title="Choose the folder that holds garmin_cache and symptoms.csv", initialdir=folder["p"])
        if d:
            folder["p"] = d
            show_folder()
    show_folder()
    tk.Button(win, text="Look in a different folder...", command=choose_folder, font=("Segoe UI", 9)).pack(side="bottom", padx=24, pady=(0, 6), anchor="w")
    folder_lbl.pack(side="bottom", padx=24, anchor="w")
    tk.Label(win, text="Type  delete  to confirm:", bg=BG_, fg=FG_, font=("Segoe UI", 11, "bold")).pack(side="bottom", padx=24, anchor="w")
    tk.Label(win, text="Permanently delete period data?", font=("Segoe UI", 14, "bold"), bg=BG_, fg="#ff8a80").pack(side="top", padx=24, pady=(18, 6), anchor="w")
    msg = ("This is a PERMANENT delete. It does not go to the recycle bin and it cannot be undone. The only way to get any of it back is to pull it from "
           "its sources again (your Garmin account, a Visible export, or by logging it again).\n\n"
           "What will be erased on this computer:\n"
           "  - Garmin cycle-tracking data saved by this app (menstrual.json)\n"
           "  - period_cycles.csv\n"
           "  - the period, mood, discharge and period-symptom columns in symptoms.csv\n"
           "  - period and cycle rows in your saved Visible history\n"
           "  - the last dashboard page and garmin_export.csv (they contain cycle information; the next run recreates them)\n\n"
           "What this does NOT touch: your Garmin Connect account, the original Visible export files you downloaded, "
           "and any copies, backups or cloud-synced folders. Remove period data there yourself if you want it gone everywhere.\n\n"
           "Cycle data will stay ON unless you also tick \"Turn off cycle data\"; otherwise the next run fetches it again.")
    box = tk.Text(win, wrap="word", height=14, bg="#1a2029", fg=FG_, relief="flat", font=("Segoe UI", 10), padx=10, pady=8)
    box.insert("1.0", msg)
    box.config(state="disabled")
    sb = tk.Scrollbar(win, command=box.yview)
    box.config(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y", padx=(0, 12), pady=(0, 8))
    box.pack(side="top", fill="both", expand=True, padx=(24, 0), pady=(0, 8))

    def do_delete():
        res = erase_period_data(folder["p"])
        win.destroy()
        messagebox.showinfo("Period data deleted", "Done.\n\n" + "\n".join(res), parent=parent)
    btn = tk.Button(row, text="Delete permanently", command=do_delete, state="disabled", bg="#b3261e", fg="white", relief="flat",
                    font=("Segoe UI", 10, "bold"), padx=14, pady=5, disabledforeground="#777777")
    btn.pack(side="right")
    tk.Button(row, text="Cancel", command=win.destroy, font=("Segoe UI", 10), padx=14, pady=4).pack(side="right", padx=8)
    v.trace_add("write", lambda *a: btn.config(state="normal" if v.get().strip().lower() == "delete" else "disabled"))
    win.transient(parent)
    win.grab_set()
    ent.focus_set()
    parent.wait_window(win)


def pick_visible_csv(parent):
    """Optional popup: do you have a Visible export? Returns a path or None."""
    if not tk:
        return None
    last = visible_cache_last_date()
    saved = (f"\n\nYour earlier Visible imports are already saved (through {last:%b %d, %Y}) and will be used either way. "
             "Choose Yes only to add a newer export." if last is not None else
             "\n\nNo Visible data is saved yet. Without it the dashboard can't see your HRV or Visible's stability score, so it can't track "
             "flares. Choose Yes and pick your export.")
    if not messagebox.askyesno("Visible export", "Do you have a Visible export (CSV) to add?\n\nIt brings in your Visible HRV, stability, "
                               "crashes and symptoms. Choose No to skip.\n\nTip for your daily HRV reading: take it with Visible first thing after waking, before you "
                               "get active or take medicine, with a warm, dry finger on the camera." + saved, parent=parent):
        return None
    start_dir = None
    try:
        start_dir = VISIBLE_DIR_FILE.read_text().strip() or None
    except OSError:
        pass
    path = filedialog.askopenfilename(parent=parent, title="Choose your Visible export (.csv)", initialdir=start_dir,
                                      filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
    if not path:
        return None
    try:
        CACHE_DIR.mkdir(exist_ok=True)
        VISIBLE_DIR_FILE.write_text(str(Path(path).parent))
    except OSError:
        pass
    return path


def get_credentials():
    root = tk.Tk()
    dino_icon(root)
    root.title(f"POTS dashboard v{VERSION}")
    root.resizable(False, False)
    root.configure(bg="#12161c")
    root.geometry("440x520")
    tk.Label(root, text="Garmin Connect login", font=("Segoe UI", 15, "bold"), bg="#12161c", fg="white").pack(pady=(18, 10))
    vars_ = {}
    for key, label, show in (("email", "Email", ""), ("password", "Password", "*"), ("zip", "Zip code (optional, for pressure)", "")):
        tk.Label(root, text=label, font=("Segoe UI", 10), bg="#12161c", fg="white").pack(anchor="w", padx=30)
        vars_[key] = tk.StringVar()
        tk.Entry(root, textvariable=vars_[key], show=show, width=32, font=("Segoe UI", 11)).pack(padx=30, pady=(0, 8))
    result = {"ok": False}

    def go_():
        z = vars_["zip"].get().strip()
        if not vars_["email"].get() or not vars_["password"].get():
            messagebox.showwarning("Missing", "Enter your email and password.")
        elif z and not (z.isdigit() and len(z) == 5):
            messagebox.showwarning("Zip code", "Enter a 5-digit US zip code, or leave it blank.")
        else:
            result.update(ok=True, email=vars_["email"].get(), password=vars_["password"].get(), zip=z or None)
            root.destroy()

    tk.Button(root, text="Build dashboard", command=go_, font=("Segoe UI", 11, "bold"), bg="#4a90d9", fg="white",
              relief="flat", padx=20, pady=5).pack(pady=(14, 6))

    def skip_():
        result.update(ok=True, email=None, password=None, zip=None, offline=True)
        root.destroy()
    if CACHES["stats"].exists():
        ts = last_pull_time()
        when = f" (last pulled {ts:%b %d, %I:%M %p})" if ts else ""
        tk.Button(root, text="Skip login: use saved data" + when, command=skip_, font=("Segoe UI", 10), padx=14, pady=3).pack(pady=(0, 10))
    tk.Button(root, text="Settings", command=lambda: settings_window(root), font=("Segoe UI", 9), padx=10).pack(pady=(0, 14))
    root.bind("<Return>", lambda e: go_())
    root.mainloop()
    return result


def last_pull_time():
    try:
        return dt.datetime.fromisoformat(LAST_PULL.read_text().strip())
    except Exception:
        try:
            return dt.datetime.fromtimestamp(CACHES["stats"].stat().st_mtime)
        except OSError:
            return None


def ask_use_saved_data():
    """If the Garmin data was pulled recently, offer to skip the login and just rebuild the dashboard from the saved data."""
    if not tk or CACHE_FRESH_HOURS <= 0 or not CACHES["stats"].exists() or "--refresh" in sys.argv:
        return "--cached" in sys.argv
    if "--cached" in sys.argv:
        return True
    ts = last_pull_time()
    if ts is None:
        return False
    mins = (dt.datetime.now() - ts).total_seconds() / 60.0
    if mins > CACHE_FRESH_HOURS * 60 or mins < 0:
        return False
    age = f"{mins:.0f} minutes" if mins < 90 else f"{mins / 60:.1f} hours"
    BG_, FG_, MU_ = "#12161c", "white", "#8d96a3"
    root = tk.Tk()
    dino_icon(root)
    root.title(f"POTS dashboard v{VERSION}")
    root.configure(bg=BG_)
    root.resizable(False, False)
    choice = {"use": None}
    tk.Label(root, text="Saved Garmin data", font=("Segoe UI", 14, "bold"), bg=BG_, fg=FG_).pack(padx=26, pady=(18, 4))
    tk.Label(root, text=f"Your Garmin data was last pulled {age} ago.", bg=BG_, fg=FG_, font=("Segoe UI", 10)).pack(padx=26)
    tk.Label(root, text="Use the saved data: no login, opens right away.\nOr log in and refresh from Garmin.", bg=BG_, fg=MU_, font=("Segoe UI", 9)).pack(padx=26, pady=(2, 12))

    def pick(v):
        choice["use"] = v
        root.destroy()
    row = tk.Frame(root, bg=BG_)
    row.pack(padx=26, pady=(0, 6))
    tk.Button(row, text="Use saved data", command=lambda: pick(True), bg="#4a90d9", fg="white", relief="flat", font=("Segoe UI", 10, "bold"), padx=14, pady=5).pack(side="left", padx=4)
    tk.Button(row, text="Log in and refresh", command=lambda: pick(False), font=("Segoe UI", 10), padx=14, pady=4).pack(side="left", padx=4)
    tk.Button(root, text="Settings", command=lambda: settings_window(root), font=("Segoe UI", 9), padx=10).pack(pady=(4, 16))
    root.protocol("WM_DELETE_WINDOW", lambda: pick(False))
    root.mainloop()
    return bool(choice["use"])


def last_garmin_sleep(raw):
    """(date_key, record) of the most recent night Garmin recorded, or None."""
    best = None
    for d in sorted(raw.get("sleep", {})):
        r = raw["sleep"][d]
        if r and r.get("onset_ms") and r.get("offset_ms"):
            best = (d, r)
    return best


def save_symptom_fields(date_key, fields):
    """Writes (or updates) some columns for one date in symptoms.csv, keeping everything else in the file."""
    ensure_symptoms_header()
    d = pd.read_csv(SYMPTOMS_CSV, dtype=str, keep_default_na=False) if SYMPTOMS_CSV.exists() else pd.DataFrame(columns=SYMPTOM_COLS)
    for c in SYMPTOM_COLS:
        if c not in d:
            d[c] = ""
    d["date"] = d["date"].str.strip()
    if not (d["date"] == date_key).any():
        d = pd.concat([d, pd.DataFrame([{c: (date_key if c == "date" else "") for c in d.columns}])], ignore_index=True)
    m = d["date"] == date_key
    for c, v in fields.items():
        d.loc[m, c] = v
    d.to_csv(SYMPTOMS_CSV, index=False, encoding="utf-8")


def save_sleep_correction(date_key, bed, wake, hours):
    """Writes (or updates) the bed / wake / sleep_h columns for one night in symptoms.csv."""
    save_symptom_fields(date_key, {"bed": bed or "", "wake": wake or "", "sleep_h": hours or ""})


def answered_today(col):
    try:
        if not SYMPTOMS_CSV.exists():
            return False
        d = pd.read_csv(SYMPTOMS_CSV, dtype=str, keep_default_na=False)
        if col not in d:
            return False
        return bool(((d["date"].str.strip() == date.today().isoformat()) & (d[col].str.strip() != "")).any())
    except Exception:
        return False


def today_value(col):
    """Today's saved answer for one symptoms.csv column, or '' if there is none."""
    try:
        if not SYMPTOMS_CSV.exists():
            return ""
        d = pd.read_csv(SYMPTOMS_CSV, dtype=str, keep_default_na=False)
        if col not in d:
            return ""
        v = d.loc[d["date"].str.strip() == date.today().isoformat(), col].astype(str).str.strip()
        return v[v != ""].iloc[-1] if (v != "").any() else ""
    except Exception:
        return ""


def flare_answered_today():
    return answered_today("flare")


def parse_date_text(txt):
    """Accepts 2026-11-02, 11/02/2026 or 11/02 (this year, or last year if that would be in the future). Returns a date or None."""
    t = (txt or "").strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return dt.datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    try:
        d = dt.datetime.strptime(t + f"/{date.today().year}", "%m/%d/%Y").date()
        return d if d <= date.today() else d.replace(year=d.year - 1)
    except ValueError:
        return None


def period_question_off():
    return (not TRACK_PERIOD) or PERIOD_OFF.exists()


def ask_flare_checkin(parent, force=False):
    """Once a day, one small window: are you in a flare, and is your period happening? Answers are saved in symptoms.csv
    (flare = 1/0 and period = 1/0 for today; a period start date back-fills the days since).
    force=True (from Settings) asks both questions again, showing today's saved answers so they can be changed."""
    if not tk:
        return
    ask_flare = force or not flare_answered_today()
    ask_period = not period_question_off() and (force or not answered_today("period"))
    if not (ask_flare or ask_period):
        return
    win = tk.Toplevel(parent)
    win.title("Change today's answers" if force else "How are you today?")
    win.configure(bg="#12161c")
    win.resizable(False, False)
    BG_, FG_, MU_ = "#12161c", "white", "#8d96a3"
    tk.Label(win, text=("Your answers for today are filled in. Change them and press Save; Skip leaves a question as it was." if force
                        else "Quick check-in. Answers are saved to symptoms.csv on your computer."),
             bg=BG_, fg=MU_, font=("Segoe UI", 9), justify="left", wraplength=420).pack(padx=20, pady=(14, 6), anchor="w")
    flare_v = tk.StringVar(value=today_value("flare") if force else "")
    period_v = tk.StringVar(value=today_value("period") if force else "")
    start_v = tk.StringVar(value=date.today().isoformat())
    off_v = tk.IntVar(value=0)
    mood_v = tk.StringVar(value=today_value("mood") if force else "")
    disc_v = tk.StringVar(value=today_value("discharge") if force else "")
    sym_v = tk.StringVar(value=today_value("period_symptoms") if force else "")

    def radios(parent_, var, items):
        r = tk.Frame(parent_, bg=BG_)
        r.pack(anchor="w", padx=20, pady=(0, 8))
        for text, val in items:
            tk.Radiobutton(r, text=text, variable=var, value=val, bg=BG_, fg=FG_, selectcolor="#1a2029", activebackground=BG_,
                           activeforeground=FG_, font=("Segoe UI", 10)).pack(side="left", padx=(0, 12))

    if ask_flare:
        tk.Label(win, text="Are you in a flare today?", bg=BG_, fg=FG_, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
        radios(win, flare_v, [("Yes", "1"), ("No", "0"), ("Skip", "")])
    if ask_period:
        tk.Label(win, text="Is your period happening today? (spotting counts)", bg=BG_, fg=FG_, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
        radios(win, period_v, [("Yes", "1"), ("No", "0"), ("Skip", "")])
        tk.Label(win, text="If yes, it started on (YYYY-MM-DD or MM/DD). Change this if it began earlier:", bg=BG_, fg=MU_,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        tk.Entry(win, textvariable=start_v, width=14, font=("Segoe UI", 11)).pack(anchor="w", padx=20, pady=(0, 6))
        tk.Label(win, text="Optional: mood today (1 low to 5 great)", bg=BG_, fg=MU_, font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        radios(win, mood_v, [("1", "1"), ("2", "2"), ("3", "3"), ("4", "4"), ("5", "5"), ("Skip", "")])
        tk.Label(win, text="Optional: discharge today", bg=BG_, fg=MU_, font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        tk.OptionMenu(win, disc_v, "", "none or dry", "sticky", "creamy", "watery", "egg-white (clear, stretchy)").pack(anchor="w", padx=20, pady=(0, 6))
        tk.Label(win, text="Optional: cycle symptoms (cramps, bloating, headache...)", bg=BG_, fg=MU_, font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        tk.Entry(win, textvariable=sym_v, width=34, font=("Segoe UI", 10)).pack(anchor="w", padx=20, pady=(0, 6))
        tk.Checkbutton(win, text="Don't ask about periods again", variable=off_v, bg=BG_, fg=MU_, selectcolor="#1a2029", activebackground=BG_,
                       activeforeground=MU_, font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(0, 6))

    def save():
        today = date.today()
        try:
            if ask_flare and flare_v.get() != "":
                save_symptom_fields(today.isoformat(), {"flare": flare_v.get()})
            if ask_period and period_v.get() == "1":
                sd = parse_date_text(start_v.get())
                if sd is None or sd > today or (today - sd).days > 20:
                    messagebox.showwarning("Period start", "Please type the start date like 2026-11-02 or 11/02 (within the last 20 days).", parent=win)
                    return
                for k in range((today - sd).days + 1):
                    day = (sd + timedelta(days=k)).isoformat()
                    save_symptom_fields(day, {"period": "1"})
            elif ask_period and period_v.get() == "0":
                save_symptom_fields(today.isoformat(), {"period": "0"})
            if ask_period:
                extra = {k: v for k, v in (("mood", mood_v.get()), ("discharge", disc_v.get().split(" (")[0]), ("period_symptoms", sym_v.get().strip())) if v}
                if extra:
                    save_symptom_fields(today.isoformat(), extra)
            if ask_period and off_v.get():
                CACHE_DIR.mkdir(exist_ok=True)
                PERIOD_OFF.write_text("off")
        except Exception as ex:
            log(f"Could not save your check-in: {ex}")
        win.destroy()

    row = tk.Frame(win, bg=BG_)
    row.pack(pady=(4, 16))
    tk.Button(row, text="Save", command=save, bg="#4a90d9", fg="white", relief="flat", padx=14, pady=4).pack(side="left", padx=6)
    tk.Button(row, text="Skip for now", command=win.destroy, padx=12, pady=4).pack(side="left", padx=6)
    win.transient(parent)
    win.grab_set()
    parent.wait_window(win)


def ask_sleep_correction(parent, raw):
    """Optional popup about the most recent night: Garmin's sleep times are not always right, so you can replace them."""
    if not tk:
        return
    last = last_garmin_sleep(raw)
    if not last:
        return
    d, r = last
    try:
        done = set(SLEEP_CHECKED.read_text().split()) if SLEEP_CHECKED.exists() else set()
    except OSError:
        done = set()
    if d in done or d in load_sleep_overrides():
        return
    utc = dt.timezone.utc
    on = dt.datetime.fromtimestamp(r["onset_ms"] / 1000, tz=utc).replace(tzinfo=None)
    off = dt.datetime.fromtimestamp(r["offset_ms"] / 1000, tz=utc).replace(tzinfo=None)
    asleep = (r.get("asleep_s") or 0) / 3600.0
    win = tk.Toplevel(parent)
    win.title("Check last sleep")
    win.configure(bg="#12161c")
    win.resizable(False, False)
    tk.Label(win, text=f"Garmin recorded your sleep ending {off:%a %b %d} as {on:%I:%M %p} to {off:%I:%M %p}, "
                       f"{asleep:.1f} hours asleep.\nWatch sleep times are not always right. Is that about right?",
             bg="#12161c", fg="white", font=("Segoe UI", 10), justify="left").pack(padx=20, pady=(16, 8))
    vals = {"bed": tk.StringVar(value=f"{on:%H:%M}"), "wake": tk.StringVar(value=f"{off:%H:%M}"), "hrs": tk.StringVar(value="")}
    for key, label in (("bed", "Went to bed (24-hour, e.g. 02:30)"), ("wake", "Woke up (24-hour, e.g. 10:00)"),
                       ("hrs", "Hours you actually slept (optional, e.g. 4.5)")):
        tk.Label(win, text=label, bg="#12161c", fg="#8d96a3", font=("Segoe UI", 9)).pack(anchor="w", padx=20)
        tk.Entry(win, textvariable=vals[key], width=16, font=("Segoe UI", 11)).pack(anchor="w", padx=20, pady=(0, 6))
    result = {"saved": False}

    def mark_checked():
        try:
            CACHE_DIR.mkdir(exist_ok=True)
            with open(SLEEP_CHECKED, "a") as fh:
                fh.write(d + "\n")
        except OSError:
            pass

    def save():
        bed, wake, hrs = vals["bed"].get().strip(), vals["wake"].get().strip(), vals["hrs"].get().strip()
        if bed and wake and not (parse_clock(bed) and parse_clock(wake)):
            messagebox.showwarning("Sleep times", "Please type times like 02:30 or 10:00.", parent=win)
            return
        if bool(bed) != bool(wake):
            messagebox.showwarning("Sleep times", "Enter both a bed time and a wake time, or clear both and enter only the hours.", parent=win)
            return
        if hrs:
            try:
                if not 0 < float(hrs) <= 24:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Sleep hours", "Hours slept should be a number such as 4.5.", parent=win)
                return
        try:
            save_sleep_correction(d, bed, wake, hrs)
            result["saved"] = True
        except Exception as ex:
            log(f"Could not save the sleep correction: {ex}")
        win.destroy()

    def keep():
        mark_checked()
        win.destroy()

    row = tk.Frame(win, bg="#12161c")
    row.pack(pady=(6, 16))
    tk.Button(row, text="Save my correction", command=save, bg="#4a90d9", fg="white", relief="flat", padx=12, pady=4).pack(side="left", padx=6)
    tk.Button(row, text="Garmin is right", command=keep, padx=12, pady=4).pack(side="left", padx=6)
    tk.Button(row, text="Ask me later", command=win.destroy, padx=12, pady=4).pack(side="left", padx=6)
    win.transient(parent)
    win.grab_set()
    parent.wait_window(win)


def main():
    apply_settings()
    if "--settings" in sys.argv and tk:
        settings_window()
        apply_settings()
    offline = False
    try:
        offline = ask_use_saved_data()
    except Exception as ex:
        log(f"Skipped the saved-data question: {ex}")
    creds = {"ok": True, "email": None, "password": None, "zip": None} if offline else get_credentials()
    if not creds["ok"]:
        sys.exit(0)
    if creds.get("offline"):
        offline = True
    progress = Progress()
    try:
        try:
            raw, start, end = fetch_all(creds["email"], creds["password"], creds["zip"], progress, offline=offline)
        except Exception as ex:
            auth = "authentication" in type(ex).__name__.lower() or "401" in str(ex)
            if auth and not offline and CACHES["stats"].exists() and messagebox.askyesno(
                    "Garmin login failed", "Garmin did not accept the login. This can happen even with the right password, because Garmin sometimes blocks "
                    "programs from signing in.\n\nUse your saved data instead? (No login needed.)", parent=progress.root):
                log("Garmin did not accept the login, so the dashboard was built from the saved data.")
                raw, start, end = fetch_all(None, None, None, progress, offline=True)
            else:
                raise
        visible = None
        path = pick_visible_csv(progress.root)
        if path:
            progress.update("Reading Visible export...", 93)
        try:
            if path or VISIBLE_CACHE.exists():
                visible = load_visible_csv(path)
                log(("Visible import (saved for next time): " if path else "Using the Visible data saved from earlier imports: ") + visible["info"])
        except Exception as ex:
            log(f"Could not read the Visible file: {ex}")
            messagebox.showwarning("Visible export", f"Could not read that file, so the dashboard will use only what was saved before (if anything).\n\n{ex}", parent=progress.root)
            try:
                visible = load_visible_csv(None) if VISIBLE_CACHE.exists() else None
            except Exception:
                visible = None
        try:
            ask_flare_checkin(progress.root)
        except Exception as ex:
            log(f"Skipped the flare check-in: {ex}")
        try:
            ask_sleep_correction(progress.root, raw)
        except Exception as ex:
            log(f"Skipped the sleep check: {ex}")
        progress.update("Analyzing...", 95)
        page, f = build_report(raw, start, end, visible)
        if page is None:
            progress.destroy()
            show_error("No data", "Garmin returned no data.\n\n" + "\n".join(LOG[:6]))
            sys.exit(1)
        OUTPUT.write_text(page, encoding="utf-8")
        write_exports(f, raw.get("loc"))
        progress.destroy()
        webbrowser.open(OUTPUT.resolve().as_uri())
    except Exception as ex:
        progress.destroy()
        if "authentication" in type(ex).__name__.lower() or "401" in str(ex):
            show_error("Garmin login failed", "Garmin did not accept the login (401: invalid email or password).\n\n"
                       "- Check the email and password and try again (the password box hides what you type).\n"
                       "- If you just tried several times, wait a few minutes: Garmin can block repeated logins.\n"
                       "- To skip the login and use the data already saved, press \"Skip login: use saved data\" on the first window.\n"
                       f"- Your saved login (if any) lives in: {TOKEN_DIR}")
            sys.exit(1)
        show_error("Error", str(ex) + "\n\n" + traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
