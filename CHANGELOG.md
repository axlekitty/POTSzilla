# Changelog

Current version: **4.8.7**. The version number lives in `POTSzilla_dashboard_VERSION.pyw` (`VERSION`), is shown in window titles and on the dashboard, and is bumped on every change.

## 4.8.x
- **4.8.7** Calendar: the word for stability 1 is "lowest" so it no longer wraps in the day squares.
- **4.8.6** The mascot dino is the icon on the app's windows.
- **4.8.5** Period days in the Timeline events strip are a red circle instead of the blood-drop emoji (it did not show on some systems).
- **4.8.4** Calendar days show a small word next to the stability number (lowest, low, mid, good, great); the key below the calendar has a divider line.
- **4.8.3** Calendar days are square.
- **4.8.2** Calendar squares are all the same, smaller size.
- **4.8.1** Today cards: sleep cards sit in the Right now row; cycle cards share a row with other signals.
- **4.8.0** Today card graphs: dots on a shaded band of your usual range (ringed dot = today). Bars are a Settings choice.

## 4.7.x
- **4.7.9** Today cards no longer stretch across two columns. Fixed alert cards dropping out of their groups.
- **4.7.8** Today card graphs as up/down bars (replaced in 4.8.0).
- **4.7.7** Alert-level cards get an emoji, WATCH / HIGH / ALERT tag, light tint and thicker border. A Settings checkbox turns the tint and emoji off.
- **4.7.0 to 4.7.6** (summarised; these were not logged one by one) Dashboard-estimated sleep score on the Sleep tab and as a Today card, with movement overlaid on the sleep-stage graph. Intensity-minutes gauge on the Pace tab and amber intensity dots on the resting heart rate chart. Today tab regrouped with Flare status first. Red teardrop for period days. Reworded "far from usual: rest". Mascot: flare pose with meteors, straining pose, slower and safer animation, working animation toggle. Barometric-pressure fetch retries. Settings button to change today's check-in answers.

## 4.6.0 to 4.0.0
- **4.6.0** Pixel-art mascot in the banner that reacts to your day; pixel-style tab menu; animation can be switched off in Settings.
- **4.5.3** Sleep and pace chart legends moved above the plot.
- **4.5.2** HRV on days with no Visible reading is estimated from overnight watch data when the two clearly agree.
- **4.5.1** Pink is only for period/cycle data; collapsible "How it works" cards; rounder panels.
- **4.5.0** Modernised top banner with pills, a status dot and key-fact tiles.
- **4.4.x** Settings window: cycle data on/off and permanent deletion of period data; larger login window; "Skip login: use saved data"; plain-language message for a rejected Garmin login.
- **4.3.x** Page split into tabs; Garmin cycle calendar fetched in 90-day pieces; histamine background reworded as evidence only.
- **4.2.x** Cycle tracker moved to the top; top cards use hover text for explanations; pace-point names match Visible's.
- **4.1.x** Garmin cycle parser reads the reported cycle start date; version number added.
- **4.0.0** Visible CSV import and cache, flare detection, pace points, colourblind-safe palette, events strip, cycle tracker, Garmin cycle/steps pulls, saved-data option, before/after comparisons, low-HRV and low-step cards, and the flare-prediction backtest.

## 3.0 and earlier
- **3.0** Visible CSV import; 60-day flare-resistant baseline on log-HRV; direction-aware stability (1 to 5); active-flare and nap detection.
- **2.0** Garmin sleep stages and overnight HRV; shared date axis; 28-day baselines; plain-language summary; reused login tokens.
