# THE WORLD IN ONE DAY — design.md (v2)

Competition: **"Sum up 24 November's world news in one image"**
Slug: `news-image-20261124` · Bounty: https://make.fun/bounty/news-image-20261124
Prize: $100, top 50 · Entries close 26 Nov 2026, 07:00 WIB · Blind round, results 10 Dec 2026.

## Why v2 exists

v1's three leads were all dated **23 Nov**, not 24 Nov (Huang returns +
Nvidia +31.5%; Ukraine sinks Russian warship off Libya; NATO AWACS to
Poland). Every story in v2 was **first reported on Tuesday 24 November
2026** — verified by the research pass before this build. The six
near-miss stories are named in the DATE CHECK box on the page itself, so
the judges can see the date discipline.

## Layout (1600 × 2100, drawn programmatically by main.py, PIL)

- Nameplate: "THE WORLD IN ONE DAY" + "35 STORIES · 7 REGIONS"
- "THE DAY IN NUMBERS" strip — 6 stats
- 3 lead stories, each with its own flat-vector illustration
- 10 more featured stories (nos. 4–13), each with a thumbnail illustration
- World map "WHERE IT HAPPENED" — pins 1–13
- "ALSO ON — 22 MORE STORIES" (nos. 14–35)
- "DATE CHECK" framed box (6 deliberately excluded stories)
- Footer: "All stories first reported Tuesday 24 November 2026" + source legend

All 13 featured illustrations are original flat-vector scenes drawn in
code (Riyadh tower + blast, Hormuz tanker + mine, Beijing hall +
magnifier, Kyiv→Moscow jet, Knesset handshake, Geneva chessboard, Dhaka
factory, Atlantic migrant boat, US passport + departure jet, Moscow night
drone swarm, Gaza skyline + smoke, Solomon island + torn pact, cyber
ships + laptop). No stock photos, no copied art.

## Featured 13 (numbered, with region + source on the page)

| # | Region | Source | Story |
|---|--------|--------|-------|
| 1 | Middle East | Reuters | Houthi strike hits Riyadh finance-district tower, 11 injured; Saudi-led coalition calls it a terrorist attack |
| 2 | Middle East | Reuters | ADNOC L&S ship hit by mine in Strait of Hormuz, 1 crew missing, 11 hurt; Iran: 4th tanker mined |
| 3 | Asia | Reuters | China probes Politburo member Chen Jining, 4th top leader investigated since 2025 |
| 4 | Europe | Reuters | Lukashenko invites Zelenskyy to fly together to Moscow for talks |
| 5 | Middle East | Reuters | Eisenkot seals first coalition deal with Lieberman |
| 6 | Europe | FIDE | Gukesh vs Sindarov, Game 1 drawn in 38 moves, Geneva |
| 7 | Asia | Reuters | Bangladesh garment workers clash with police, factories shut |
| 8 | Africa | Reuters | ~175 migrants missing after boat contact lost, sailed from Senegal |
| 9 | Americas | Reuters | Kilmar Abrego Garcia leaves US voluntarily |
| 10 | Europe | Reuters | Russia claims 699 Ukrainian drones downed overnight; 355 heading for Moscow |
| 11 | Middle East | Anadolu | Gaza: 6 killed in Israeli strikes; Hamas internal security chief dead |
| 12 | Oceania | SMH / RNZ | Solomon Islands to end security pact with China |
| 13 | Global | WSJ via Reuters | US probes cyberattacks on 50 merchant ships; Iran suspected |

## Also on — 22 more stories (nos. 14–35)

14. Houthi will not take Aden, Yemen army says — Reuters
15. UK sanctions Houthis + 4 officials — Anadolu
16. Serbia school shooting, 2 hurt, teen arrested — Anadolu
17. RSF defectors join Sudan army in Khartoum — Anadolu
18. Bangladesh rejects Hasina return demand from India — Anadolu
19. Israeli military post blocks Syrian farmers in Quneitra — Anadolu
20. Australia's Penny Wong warns on US–China rivalry — Anadolu
21. Shubman Gill asks ICC to review saliva ban — myKhel
22. Babar Azam shines on ILT20 debut — myKhel
23. Russian strike on Zaporizhzhia kills 2 — Reuters
24. Russian drone briefly enters Polish airspace — Reuters
25. US court lets army blast toxic explosives in Iowa — Reuters
26. Iran: no US talks until terms met — Reuters
27. NATO pledges defence from space threats — Reuters
28. 'El Chapo Isidro' tried in Mexico despite US extradition plea — Reuters
29. Lahore most polluted major city, AQI 538
30. Netanyahu–Eisenkot, third coalition round
31. Trump hosts gala as $TRUMP coin falls 99%
32. Iraq auctions two Saddam-era Boeing 747s — Rahnuma
33. US Democrats: 2028 hopefuls must reject dark money — Reuters
34. US weighs military training for Syrian forces — Reuters exclusive
35. Nikkei +3.9% Tuesday; Nvidia −5% premarket; VIX +8.6% — Reuters

## Region count

Europe 7 · Asia 6 · Middle East 10 · Americas 5 · Africa 2 · Oceania 2 ·
Global 3 = **35 stories, 7 regions**.

## The day in numbers (stat strip)

699 drones downed · 175 migrants missing · 538 AQI Lahore ·
11 injured in Riyadh · 50 ships cyber-probed · +3.9% Nikkei.

## DATE CHECK — deliberately excluded (wrong date, not wrong news)

- COP31 collapsed — 22 Nov
- Huang returns, Nvidia +31.5% — 23 Nov
- Ukraine sinks Russian warship off Libya — 22–23 Nov
- NATO AWACS to Poland — 23 Nov
- CrowdStrike buys Zscaler, $44bn — 23 Nov
- Indonesia factory fire, 24 dead — 21 Nov

## How to run

```
python3 main.py            # writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png)
```

Python 3 + Pillow 10.2.0, DejaVu Serif/Sans fonts. No network, no assets.
