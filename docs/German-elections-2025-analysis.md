# Game-theoretic analysis of the German federal election 2025

The German federal election of 2025 represents an interesting case for game-theoretic analysis because the parties agreed to exclude the second-largest party (AfD) from any coalition.  
This had a few notable side effects:
1. The SPD, previously the strongest party, was able to retain a strong power position even though it lost more than a third of its votes.  
2. One party (BSW) narrowly failed to pass the 5% threshold, missing it by just 0.02%. This significantly (not marginally) re-distributed power.  

In what follows, we briefly review the theory behind the analysis, present the data, and then dive into the outcomes.  
This analysis is purely *mechanical*: it does not take into account political positions.

## Quick overview of the theory on power indices

Power distribution is not only about the number of votes you get, but also about how the votes are distributed. For example, if one party gets 49% and another gets 51%, the smaller one has zero power in a simple majority system. However, if there are 10 other parties with 5% each, the 49% party holds almost all the power. Thus, depending on the distribution of votes, a party’s power can range anywhere between 0% and 100%.  

How do we measure it? The common approach is to count the number of coalitions in which a party is pivotal. There are different ways of doing this ([Banzhaf index](https://en.wikipedia.org/wiki/Banzhaf_power_index), [Shapley–Shubik index](https://en.wikipedia.org/wiki/Shapley–Shubik_power_index)). While they can differ in extreme cases, they usually produce similar results in practice. The most common measures are the Banzhaf and the Shapley–Shubik indices.

## German elections – data

First, here are the election results:

| Party | 2021  | 2025  |
|-------|-------|-------|
| Union | 24.1% | 28.5% |
| SPD   | 25.7% | 16.4% |
| AfD   | 10.3% | 20.8% |
| Green | 14.7% | 11.6% |
| BSW   | –     | 4.98% |
| Left  | 8.8%  | 4.9%  |
| FDP   | 11.4% | 4.3%  |

Which led to the following distribution of seats (the last column shows the hypothetical distribution if BSW had passed the 5% threshold):

| Party | 2021 | 2025 | *2025+BSW |
|-------|------|------|-----------|
| Union | 197  | 208  | 221       |
| SPD   | 206  | 120  | 127       |
| AfD   | 83   | 152  | 162       |
| FDP   | 91   | 0    | 0         |
| Green | 118  | 85   | 90        |
| Left  | 39   | 64   | 68        |
| SSW   | 1    | 1    | 1         |
| BSW   | 0    | 0    | 39        |
|-------|------|------|-----------|
| sum   | 735  | 630  | 708       |
| maj   | 368  | 316  | 355       |

*Side note:* German election rules are relatively complicated. The number of seats depends on the vote distribution, Bavaria has a special system, the SSW always gets one seat, and there is a mixed system of candidate votes and party votes. We abstract from these details here.

## German elections – power distribution

With theory and data in hand, we can calculate the power distribution. We use the Python package [powerindex](https://github.com/maxlit/powerindex).  

```bash
# 2021 
> px -w Union:197 SPD:206 AfD:83 FDP:91 Left:39 SSW:1 -q 368 --csv -r 3
Union,0.333
SPD,0.333
AfD,0.167
FDP,0.167
Left,0.0
SSW,0.0
```

Note the 0% power for the Left, despite its 39 seats, since it does not contribute to any winning coalition.

```bash
# 2025
> px -w Union:208 SPD:120 AfD:152 FDP:0 Green:85 Left:64 SSW:1 -q 316 --csv -r 3
Union,0.4
SPD,0.233
AfD,0.233
FDP,0.0
Green,0.067
Left,0.067
SSW,0.0
```

```bash
# 2025+BSW 
> px -w Union:221 SPD:127 AfD:162 Green:90 Left:68 SSW:1 BSW:39 -q 355 --csv -r 3
Union,0.333
SPD,0.167
AfD,0.267
Green,0.1
Left,0.1
SSW,0.0
BSW,0.033
```

However, once AfD is excluded, the picture changes.  
Technically, we keep the same threshold and set the excluded party’s seats to zero.

```bash
# 2025 excl AfD
> px -w Union:208 SPD:120 AfD:0 FDP:0 Green:85 Left:64 SSW:1 -q 316 --csv -r 3
Union,0.583
SPD,0.25
AfD,0.0
FDP,0.0
Green,0.083
Left,0.083
SSW,0.0
```

Putting it all together:

| Party | 2021 | 2025   | *2025+BSW | *2025–AfD | 
|-------|-------|-------|-----------|-----------|
| Union | 33.3% | 40%   | 33.3%     | 58.3%     |
| SPD   | 33.3% | 23.3% | 16.7%     | 25%       |
| AfD   | 16.7% | 23.3% | 26.7%     | 0%        |
| FDP   | 16.7% | 0%    | 0%        | 0%        |
| Green | 0%    | 6.7%  | 10%       | 8.3%      |
| Left  | 0%    | 6.7%  | 10%       | 8.3%      |
| SSW   | 0%    | 0%    | 0%        | 0%        |
| BSW   | 0%    | 0%    | 3.3%      | 0%        |

## Conclusion

From a game-theoretic perspective, we can observe two effects on power distribution:
1. Ignoring a party is **very** beneficial for the remaining players.  
2. Exclusion due to the 5% barrier is also quite beneficial.  

## P.S. Further analysis

A few directions that might be interesting for further exploration:  
1. Some parliamentary decisions require a two-thirds majority, where the effects could be even more extreme.  
2. One can analyze the effects of lowering the barrier from 5% to 4%.
3. One could measure the difference in power between the current parliament and current opinion polls.  

## P.P.S.

(This comment doesn’t sound political to me, but it might be perceived that way, so I’ve moved it here.)  
One might ask: what’s the point of calculating the “+BSW” scenarios? Yes, they missed the threshold by only 0.02%, but rules are rules — there’s no room to rig the election, so nothing can be done about it. Two counterarguments:  
1. Future elections matter as well — it’s a multi-period game. In almost every German federal election, one or two parties end up between 4% and 5%. Lowering the threshold from 5% to 4% would essentially change the power distribution.  
2. One can act even on a 0.02% gap. For example, part of the federal election 2021 had to be repeated in Berlin due to organizational issues, which led to changes in seat allocation. Administrative processes, court rulings, or delays can influence outcomes at the margins — and the major parties have their say in these matters, from shaping procedures (and the zeal to act upon them) to influencing judicial appointments. Thus, even without manipulation and bad will, the outcome has a small accuracy tolerance - not exact down to a single vote. 
