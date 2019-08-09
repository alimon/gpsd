#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# clienthelpers.py - helper functions for xgps and test_maidenhead
# This duplicates gpsclient.c, but in python.  Keep the two files in
# sync.
#
# See gpsclient.c for code comments.
#
# SPDX-License-Identifier: BSD-2-Clause
"""GPSd client helpers submodule."""
import math
import os


GEOID_ROW = 37
GEOID_COL = 73
GEOID_SPAN = 5
GEOID_DELTA = [
    # -90
    [ -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015, -3015,
      -3015, -3015, -3015],
    # -85
    [ -3568, -3608, -3739, -3904, -4039, -4079, -4033, -3946, -3845, -3734,
      -3603, -3458, -3310, -3163, -2994, -2827, -2695, -2667, -2737, -2823,
      -2840, -2757, -2634, -2567, -2547, -2540, -2452, -2247, -1969, -1704,
      -1540, -1507, -1552, -1592, -1573, -1513, -1465, -1478, -1542, -1577,
      -1483, -1256, -1029,  -957, -1066, -1216, -1262, -1194, -1118, -1129,
      -1231, -1370, -1504, -1641, -1813, -2028, -2255, -2455, -2630, -2811,
      -3022, -3242, -3436, -3578, -3658, -3676, -3640, -3578, -3527, -3490,
      -3532, -3570, -3568],
    # -80
    [ -5232, -5276, -5275, -5301, -5286, -5276, -5218, -5001, -4775, -4580,
      -4319, -4064, -3854, -3691, -3523, -3205, -2910, -2608, -2337, -2355,
      -2417, -2445, -2471, -2350, -2230, -2136, -1869, -1689, -1732, -1748,
      -1540, -1236, -1048,  -794,  -569,  -603,  -501,  -305,  -166,    19,
        146,   274,   444,   510,   534,   550,   458,   373,   473,   575,
        607,   732,   562,   153,  -271,  -825, -1300, -1861, -2475, -2866,
      -3434, -4001, -4196, -4533, -4989, -5152, -5094, -4983, -4987, -5065,
      -5055, -5115, -5232],
    # -75
    [ -6155, -6339, -6266, -6344, -6282, -6100, -6009, -5492, -5088, -4547,
      -4187, -3901, -3586, -3234, -3051, -2886, -2577, -2289, -1981, -1655,
      -1435, -1096,  -557,  -617,  -998,  -961,  -655,  -464,  -170,    79,
       -103,   -64,   150,   223,   819,  1006,  1174,  1136,  1211,  1278,
       1467,  1686,  1783,  1706,  1833,  1721,  1653,  1580,  1267,   953,
        629,   807,   774,   607,   217,  -386,  -814, -1354, -2452, -3542,
      -3833, -3932, -4259, -4962, -4977, -5536, -5753, -5800, -6012, -5835,
      -5751, -5820, -6155],
    # -70
    [ -6218, -6432, -6333, -6150, -6021, -5948, -5705, -5480, -5213, -4789,
      -4365, -4003, -3757, -3514, -3250, -3000, -2672, -2541, -2138, -1220,
       -844,  -277,   249,   906,   458,    69,    26,    98,   166,   130,
        118,   253,   303,   437,  1010,  1341,  1423,  1558,  1682,  1825,
       1766,  1917,  2027,  2047,  2164,  2909,  2882,  2997,  3010,  2687,
       1749,  1703,  1799,  1438,  1099,   346,  -813, -1432, -2149, -2320,
      -2704, -3085, -3907, -4172, -4287, -4846, -5466, -5592, -5576, -5525,
      -5800, -5954, -6218],
    # -65
    [ -5152, -5115, -5049, -4943, -4858, -4714, -4580, -4369, -4202, -4060,
      -3806, -3454, -3210, -3007, -2749, -2484, -2264, -1928, -1501, -1113,
       -614,    31,   642,  1502,  1833,  1844,  1268,  1442,  1441,  1302,
       1164,  1041,   945,   874,   896,  1059,  1368,  1680,  1736,  1975,
       1891,  1979,  2131,  2338,  2672,  2861,  3114,  3097,  2801,  2695,
       2422,  2022,  1648,  1340,   713,   352,  -127,  -895, -1740, -2040,
      -2854, -3292, -3453, -3922, -4395, -4538, -4554, -4356, -4445, -4669,
      -4988, -5122, -5152],
    # -60
    [ -4598, -4449, -4278, -4056, -3732, -3417, -3205, -3094, -3008, -2876,
      -2669, -2478, -2350, -2272, -2218, -1969, -1660, -1381, -1123,  -716,
       -350,   247,   924,  1712,  2016,  2066,  2032,  1556,  2123,  2322,
       2384,  1034,  2121,  1923,  1720,  1571,  1517,  1668,  2008,  2366,
       2546,  2736,  2914,  3169,  3395,  3467,  3315,  3286,  3279,  3073,
       2930,  2727,  2502,  1783,   893,   311,  -328,  -778, -1364, -1973,
      -2467, -2833, -3143, -3283, -3311, -3120, -2956, -3027, -3485, -3972,
      -4454, -4679, -4598],
    # -55
    [ -3414, -3429, -3223, -3013, -2704, -2474, -2292, -2185, -1962, -1818,
      -1828, -1485, -1259, -1284, -1327, -1304, -1097, -1071,  -628,  -326,
        174,   340,  1331,  1217,  1712,  1441,  1467,  1578,  1654,  2179,
        764,  1486,  2074,  2245,  2462,  2655,  2720,  2581,  2423,  2731,
       3145,  3383,  3436,  3909,  4448,  4422,  4032,  3938,  3665,  3461,
       3465,  3317,  2487,  1908,  1311,   683,    52,  -582, -1196, -1798,
      -2158, -2450, -2475, -2429, -2277, -2011, -2140, -2306, -2551, -2726,
      -3016, -3319, -3414],
    # -50
    [ -1615, -1938, -1875, -1827, -1839, -1793, -1605, -1650, -1737, -1773,
      -1580, -1237, -1010,  -983, -1051, -1025,  -838,  -653,  -316,    48,
        502,  1382,  1186,  1114,  1264,   785,   231,   329,   353,   556,
       1084,  1597,  2065,  2475,  2744,  2701,  2518,  2545,  2584,  2963,
       3323,  3537,  3792,  4085,  4520,  4505,  4459,  4287,  3818,  4112,
       3975,  3293,  2748,  2043,  1272,   569,  -207,  -898, -1498, -1990,
      -2242, -2358, -2212, -1968, -1843, -1695, -1705, -1688, -1400, -1177,
      -1013, -1168, -1615],
    # -45
    [   338,   -20,  -606,  -849,  -777,  -838, -1123, -1322, -1485, -1503,
      -1413, -1203, -1077, -1004,  -960,  -829,  -662,  -371,   -88,   322,
        710,  1323,  1831,  1202,   908,    47,  -292,  -367,  -495,  -174,
        688,  1500,  2194,  2673,  2568,  2423,  2099,  2168,  2617,  2834,
       3254,  3328,  3443,  4442,  4639,  4588,  4524,  4223,  3575,  3187,
       3101,  2651,  2155,  1506,   774,   -55,  -961, -1719, -2355, -2719,
      -2731, -2670, -2430, -2026, -1715, -1477, -1144,  -901,  -646,  -303,
        871,   565,   338],
    # -40
    [  2048,  1283,   637,   317,   109,  -156,  -679, -1023, -1186, -1277,
      -1275, -1202, -1282, -1150, -1022,  -881,  -690,  -300,   -84,   130,
        694,   937,  2220,  1511,  1341,   558,  -266,  -623,  -670,  -209,
        643,  1459,  2101,  2385,  2307,  2000,  1765,  1992,  2496,  2733,
       2941,  3431,  3298,  3327,  3877,  4306,  4069,  3446,  2844,  2601,
       2333,  1786,  1318,   599,  -238, -1184, -2098, -2786, -3250, -3406,
      -3351, -3095, -2741, -2101, -1482,  -148,  -201,   221,   491,  1179,
       1877,  1206,  2048],
    # -35
    [  2833,  2556,  1700,  1059,   497,   -21,  -370,  -752,  -959, -1103,
      -1093, -1104, -1198, -1097,  -960,  -785,  -596,  -362,  -211,   103,
        739,  1300,  3029,  2021,  1712,  1269,   -23,  -616,  -701,  -255,
        684,  1237,  1701,  1903,  1696,  1789,  1795,  2034,  2398,  2561,
       3187,  2625,  2609,  2897,  2564,  3339,  3118,  3121,  2240,  2102,
       1529,   991,   387,  -559, -1464, -2380, -3138, -3999, -3899, -3446,
      -3473, -3300, -2823, -1043,   143,   970,  2058,  1555,  1940,  2621,
       3154,  3839,  2833],
    # -30
    [  4772,  3089,  2257,  1381,   566,    64,  -136,  -612,  -868, -1186,
      -1309, -1131, -1033,  -903,  -780,  -625,  -443,  -242,   100,   269,
        815,  1489,  3633,  2424,  1810,  1138,   297,  -720,  -847,    -2,
        347,   579,  1025,  1408,  1504,  1686,  2165,  2353,  2599,  3182,
       3332,  3254,  3094,  2042,  1369,  1945,  1468,  1487,  1505,  1048,
        613,    26,  -904, -1757, -2512, -3190, -3751, -3941, -3939, -2896,
      -2222, -1766, -1442,    70,  1262,  2229,  3189,  2910,  3371,  3608,
       4379,  4520,  4772],
    # -25
    [  4984,  2801,  2475,  1374,   798,   198,  -269,  -628, -1063, -1262,
      -1090,  -970,  -692,  -516,  -458,  -313,  -143,    19,   183,   403,
        837,  1650,  3640,  2990,  2084,   628,   422,  -597, -1130,  -712,
       -474,  -110,   446,  1043,  1349,  1571,  2008,  2572,  2405,  3175,
       2766,  2407,  2100,  1130,   367,   840,    89,   114,    49,   -25,
       -494, -1369, -2345, -3166, -3804, -4256, -4141, -3730, -3337, -1814,
       -901,  -388,   298,  1365,  2593,  3490,  4639,  4427,  4795,  4771,
       5325,  5202,  4984],
    # -20
    [  4994,  5152,  2649,  1466,   935,   427,  -115,  -518,  -838, -1135,
      -1134,  -917,  -525,  -280,  -218,  -310,  -396,  -306,  -137,   148,
        811,  1643,  3496,  4189,  1958,   358,  -784,  -684,  -740,  -800,
       -579,  -638,   -49,   704,  1221,  1358,  1657,  1957,  2280,  2639,
       2157,  1246,   728,  -364, -1021,  -586, -1098, -1055, -1032, -1244,
      -2065, -3158, -4028, -4660, -4802, -4817, -4599, -3523, -2561, -1260,
        446,  1374,  2424,  3310,  4588,  5499,  5724,  5479,  5698,  5912,
       6400,  6116,  4994],
    # -15
    [  4930,  4158,  2626,  1375,   902,   630,   150,  -275,  -667, -1005,
       -954,  -847,  -645,  -376,  -315,  -479,  -639,  -681,  -550,  -268,
        709,  2996,  4880,  2382,  1695,  -136,  -964, -1211, -1038, -1045,
       -695,  -595,    23,   733,  1107,  1318,  1348,  1376,  1630,  2240,
       1248,   454,  -737, -1252, -2001, -2513, -1416, -2169, -2269, -3089,
      -4063, -5194, -5715, -6105, -5700, -4873, -3919, -2834, -1393,  -112,
       1573,  3189,  3907,  4863,  5437,  6548,  6379,  6281,  6289,  5936,
       6501,  5794,  4930],
    # -10
    [  3525,  2747,  2135,  1489,  1078,   739,   544,   -39,  -268,  -588,
       -917, -1025, -1087,  -940,  -771,  -923, -1177, -1114,  -919,  -383,
       -108,  2135,  2818,  1929,   386, -1097, -1911, -1619, -1226, -1164,
       -952,  -583,   399,  1070,  1280,  1345,  1117,   993,  1306,  1734,
        538,  -463, -1208, -1602, -2662, -3265, -3203, -3408, -3733, -5014,
      -6083, -7253, -7578, -7096, -6418, -4658, -2647,  -586,   -87,  1053,
       3840,  3336,  5240,  6253,  6898,  7070,  7727,  7146,  6209,  5826,
       5068,  4161,  3525],
    # -5
    [  2454,  1869,  1656,  1759,  1404,  1263,  1012,   605,   108,  -511,
       -980, -1364, -1620, -1633, -1421, -1342, -1412, -1349, -1006,  -229,
       1711,  1293,  1960,   605,  -793, -2058, -2108, -2626, -1195,  -606,
       -513,  -108,   671,  1504,  1853,  1711,  1709,   940,   570,   296,
       -913, -1639, -1471, -1900, -3000, -4164, -4281, -4062, -5366, -6643,
      -7818, -8993, -9275, -8306, -6421, -4134, -1837,  1367,  2850,  4286,
       5551,  5599,  5402,  6773,  7736,  7024,  8161,  6307,  5946,  4747,
       3959,  3130,  2454],
    # 0
    [  2128,  1774,  1532,  1470,  1613,  1589,  1291,   783,    79,  -676,
      -1296, -1941, -2298, -2326, -2026, -1738, -1412, -1052,  -406,    82,
       1463,  1899,  1352,  -170, -1336, -2446, -2593, -2328, -1863,  -833,
        245,  1005,  1355,  1896,  1913,  1888,  1723,  1642,   940,  -127,
      -1668, -1919, -1078, -1633, -2762, -4357, -4885, -5143, -6260, -7507,
      -8947, -10042, -10259, -8865, -6329, -3424,  -692,  1445,  3354,  5132,
       5983,  4978,  7602,  7274,  7231,  6941,  6240,  5903,  4944,  4065,
       3205,  2566,  2128],
    # 5
    [  1632,  1459,  1243,  1450,  1643,  1432,   867,   283,  -420, -1316,
      -1993, -2614, -3012, -3016, -2555, -1933, -1256,  -688,  -133,   634,
       1369,  2095,   -92,  -858, -1946, -3392, -3666, -3110, -1839,  -371,
        674,  1221,  1657,  1994,  2689,  2577,  2020,  2126,  1997,   987,
       -739,  -989, -1107, -1369, -1914, -3312, -4871, -5365, -6171, -7732,
      -9393, -10088, -10568, -9022, -6053, -4104, -1296,   373,  2310,  4378,
       6279,  6294,  6999,  6852,  6573,  6302,  5473,  5208,  4502,  3445,
       2790,  2215,  1632],
    # 10
    [  1285,  1050,  1212,  1439,  1055,   638,   140,  -351, -1115, -2060,
      -2904, -3593, -3930, -3694, -2924, -2006, -1145,  -441,   164,  1059,
         91,  -440, -1043, -2791, -4146, -4489, -4259, -3218, -1691,  -683,
        306,  1160,  1735,  3081,  3275,  2807,  2373,  2309,  2151,  1245,
        207,  -132,  -507,  -564,  -956, -1917, -3167, -5067, -5820, -7588,
      -9107, -9732, -9732, -8769, -6308, -4585, -2512,  -891,  1108,  3278,
       5183,  6391,  5985,  5969,  6049,  5616,  4527,  4156,  3531,  2776,
       2456,  1904,  1285],
    # 15
    [   862,   804,   860,   969,   544,    89,  -417, -1008, -1641, -2608,
      -3607, -4234, -4482, -4100, -3232, -2092, -1105, -1092,   238,   330,
       -571, -1803, -2983, -3965, -5578, -4864, -3777, -2572, -1690,  -536,
        806,  2042,  2323,  3106,  3019,  2833,  2260,  2064,  2036,  1358,
       1030,   908,   391,   -54,  -377,  -885, -2172, -3359, -5309, -6686,
      -8058, -8338, -8695, -8322, -6404, -5003, -3420, -2060,  -255,  1833,
       4143,  4218,  4771,  5031,  5241,  5504,  4399,  3471,  2832,  2266,
       1643,  1190,   862],
    # 20
    [   442,   488,   986,   877,   757,  1175,  -696, -1473, -2285, -3128,
      -3936, -4520, -4739, -4286, -3350, -2092,  -747, -1894, -1083, -1508,
      -2037, -2528, -4813, -6316, -4698, -4222, -3279, -1814, -1001,   212,
       1714,  2273,  2535,  3367,  3112,  2736,  3086,  2742,  2679,  2071,
       1422,  1333,   922,   619,   183,  -945, -3070, -3680, -4245, -5461,
      -6064, -6652, -6806, -6210, -5947, -5177, -3814, -2589, -1319,   551,
       2150,  3262,  3799,  4177,  4898,  4658,  4149,  2833,  2148,  1410,
        899,   551,   442],
    # 25
    [  -248,    12,   716,   415,   327,  -187, -1103, -1729, -2469, -3296,
      -4040, -4545, -4642, -4232, -3466, -2064, -1667, -3232, -2660, -2685,
      -2789, -4262, -5208, -5084, -4935, -4077, -2622,  -804,   131,   946,
       1859,  2203,  3038,  3433,  3758,  3029,  2757,  3524,  3109,  2511,
       2300,  1554,  1316,  1114,   954,   -81, -2642, -3389, -3167, -4211,
      -4634, -5193, -6014, -6245, -5347, -5313, -3846, -3149, -2130,  -354,
       1573,  2760,  3310,  3713,  4594,  3862,  2827,  1939,  1019,   313,
       -142,  -378,  -248],
    # 30
    [  -720,  -717,  -528,  -573,  -867, -1224, -1588, -2135, -2796, -3432,
      -4036, -4329, -4246, -3464, -2996, -2389, -2323, -2844, -2744, -2884,
      -3238, -4585, -5164, -4463, -4064, -3238, -1751,   150,  1657,  2501,
       3023,  3007,  3404,  3976,  4354,  4648,  3440,  2708,  2813,  2968,
       2611,  2104,  1606,  1808,  1086,  -392, -1793,  -689, -1527, -2765,
      -3766, -4709, -3687, -2800, -3375, -3793, -3365, -4182, -2385, -1115,
        785,  2302,  3020,  3564,  4178,  2993,  1940,  1081,   331,  -364,
       -683,  -690,  -720],
    # 35
    [ -1004, -1222, -1315, -1304, -1463, -1680, -2160, -2675, -3233, -3746,
      -4021, -4053, -3373, -3012, -2447, -2184, -2780, -3219, -2825, -3079,
      -3181, -4284, -4548, -3867, -3123, -2302,  -785,   943,  2687,  4048,
       4460,  4290,  4118,  4585,  4282,  4437,  4898,  3818,  3696,  3414,
       2299,  2057,   627,  1915,  1833,   451,   678,  -876, -1602, -2167,
      -3344, -2549, -2860, -3514, -4043, -4207, -4005, -3918, -3121, -1521,
        471,  2023,  2980,  3679,  3465,  2405,  1475,   553,  -142,  -880,
      -1178,  -963, -1004],
    # 40
    [ -1223, -1218, -1076, -1116, -1298, -1541, -2085, -2648, -3120, -3473,
      -3679, -3342, -2334, -1912, -1787, -1756, -2482, -3182, -3322, -3429,
      -3395, -3374, -3372, -3341, -2654, -1509,   105,  1620,  3250,  4603,
       5889,  5776,  5198,  4840,  4903,  5370,  5086,  4536,  4519,  4601,
       3395,  4032,  3890,  3537,  3113,  2183, -1769, -1552, -2856, -3694,
      -4092, -3614, -5468, -6518, -6597, -5911, -5476, -4465, -2802, -1076,
        232,  1769,  2305,  3018,  3768,  1721,  1694,   667,  -154,  -799,
      -1068, -1196, -1223],
    # 45
    [  -634,  -460,  -330,  -267,  -413,  -818, -1310, -1763, -2352, -2738,
      -2632, -2685, -1929, -1340,  -737, -1441, -2254, -2685, -3358, -3488,
      -3635, -3187, -2665, -2142, -1515,  -124,  1727,  2798,  3965,  5065,
       6150,  6513,  6089,  5773,  5044,  4471,  4677,  5052,  3938,  4537,
       4425,  3652,  3063,  2178,  1267,    84, -1109, -1974, -2905, -3650,
      -4264, -4741, -4136, -6324, -5826, -5143, -4851, -4344, -3225, -1386,
          5,  1153,  2198,  2833,  2835,  2563,  1337,  1194,   503,  -329,
       -289,  -754,  -634],
    # 50
    [  -578,   -40,   559,   880,   749,   464,     0,  -516, -1140, -1655,
      -1818, -1589, -1555, -1337, -1769, -1919, -2372, -2981, -3485, -3976,
      -3941, -3565, -2614, -2223, -1253,   802,  2406,  3239,  4434,  5428,
       6265,  6394,  6180,  5690,  5855,  5347,  4506,  4685,  4799,  4445,
       3972,  3165,  2745,  1601,  1084,    41, -1170, -1701, -1916, -2914,
      -3305, -3790, -4435, -4128, -4163, -4535, -4190, -3891, -2951, -1869,
       -414,   851,  1494,  2097,  2268,  1939,  2031,  2460,   638,   578,
        325,    98,  -578],
    # 55
    [   -18,   482,   905,  1562,  1739,   983,  1097,   568,    34,  -713,
       -695, -1072, -1576, -1879, -2479, -2884, -3275, -3971, -4456, -4654,
      -4461, -3688, -2697, -1623,  -823,  1270,  2523,  3883,  4967,  5977,
       6049,  6149,  6095,  5776,  5820,  5575,  4642,  4099,  4025,  3462,
       2679,  2447,  1951,  1601,  1151,   663,   157,  -603,  -952, -1987,
      -2609, -3316, -3600, -3684, -3717, -3836, -4024, -3452, -2950, -1861,
       -903,    89,   975,  1499,  1560,  1601,  1922,  2031,  2326,   -58,
        506,  -177,   -18],
    # 60
    [    93,   673,   969,  1168,  1498,  1486,  1439,  1165,  1128,   720,
          5,  -689, -1610, -2409, -3094, -3585, -4193, -4772, -4678, -4521,
      -4184, -2955, -2252,  -834,   503,  1676,  2882,  4130,  4892,  5611,
       6390,  6338,  6069,  5974,  5582,  5461,  4788,  4503,  4080,  2957,
       1893,  1773,  1586,  1544,  1136,  1026,   622,    50,  -389, -1484,
      -2123, -2625, -3028, -3143, -3366, -3288, -3396, -3069, -2770, -2605,
      -1663,  -555,    25,   491,  1168,  1395,  1641,  1597,  1426,  1299,
        921,  -160,    93],
    # 65
    [   419,   424,   443,   723,   884,  1030,  1077,  1191,  1065,   734,
        265, -1052, -1591, -2136, -2773, -3435, -3988, -3978, -3698, -3509,
      -3370, -2490, -1347,  -263,  1647,  2582,  3291,  4802,  4447,  5609,
       5879,  6454,  6709,  6606,  5988,  5365,  5103,  4385,  3996,  3250,
       2526,  1766,  1817,  1751,  1275,   857,   636,    29,   -12,  -918,
      -1364, -1871, -2023, -2102, -2258, -2441, -2371, -2192, -1908, -1799,
      -1720, -1662,  -385,    86,   466,   880,   715,   834,  1010,  1105,
        877,   616,   419],
    # 70
    [   242,    93,    98,    62,   -54,   -25,  -127,  -156,  -253,  -412,
       -805, -1106, -1506, -1773, -2464, -2829, -2740, -2579, -2559, -2271,
      -1849,  -853,   294,  1055,  2357,  2780,  2907,  3909,  4522,  5272,
       5594,  5903,  5966,  5930,  5592,  5188,  4878,  4561,  4190,  3834,
       2963,  2451,  1981,  1525,  1064,   694,   253,   -70,  -318,  -781,
       -979, -1048, -1274, -1413, -1175, -1313, -1449, -1206,  -850, -1087,
       -828,  -933,  -540,  -301,   -35,    53,   279,   267,   345,   371,
        334,   289,   242],
    # 75
    [   128,   228,   376,    46,  -173,  -355,  -417,  -548,  -764,  -925,
       -419,  -950, -1185, -1102, -1293, -1355, -1075,  -713,  -365,   167,
        516,  1381,  1882,  1826,  1956,  2492,  3192,  3541,  3750,  4123,
       4462,  4592,  4472,  4705,  4613,  4559,  4340,  4392,  4144,  3973,
       3119,  2582,  2057,  1684,  1199,   834,   477,   325,   295,  -198,
       -459,  -670,  -706,  -677,  -766,  -852,  -939,  -905,  -637,  -601,
       -531,  -433,  -292,  -158,    88,    85,   118,   121,   147,   179,
        173,   149,   128],
    # 80
    [   342,   293,   244,   159,    38,    20,    15,   -15,  -109,  -119,
       -240,  -182,    16,   397,   550,   264,   350,   670,   865,   681,
       1188,  1136,   703,  1153,  1930,  2412,  2776,  3118,  3351,  3634,
       3653,  3272,  3177,  3161,  3354,  3671,  3615,  3572,  3522,  3274,
       2914,  2682,  2426,  2185,  1845,  1584,  1297,  1005,   809,   507,
        248,   314,   230,    96,   149,   240,   274,   297,   153,   109,
        164,    91,   104,    43,    12,   153,   243,   170,   184,    59,
         99,   158,   342],
    # 85
    [   912,   961,  1013,  1013,   997,  1032,  1026,  1050,  1072,  1132,
       1156,  1253,  1310,  1389,  1441,  1493,  1508,  1565,  1621,  1642,
       1768,  1888,  2036,  2089,  2117,  2106,  2010,  2120,  2276,  2376,
       2426,  2427,  2526,  2582,  2493,  2534,  2628,  2564,  2471,  2509,
       2407,  2332,  2214,  2122,  1987,  1855,  1714,  1619,  1517,  1474,
       1406,  1351,  1308,  1264,  1181,  1081,  1047,  1084,  1043,   964,
        851,   755,   732,   706,   697,   785,   864,   762,   686,   729,
        789,   856,   912],
    # 90
    [  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,  1490,
       1490,  1490,  1490]]


# "enum" for display units
unspecified = 0
imperial = 1
nautical = 2
metric = 3

# "enum" for deg_to_str() conversion type
deg_dd = 0
deg_ddmm = 1
deg_ddmmss = 2


def _non_finite(num):
    """Is this number not finite?"""
    return math.isnan(num) or math.isinf(num)


def deg_to_str(fmt, degrees):
    """String-format a latitude/longitude."""
    try:
        degrees = float(degrees)
    except ValueError:
        return ''

    if _non_finite(degrees):
        return ''

    if degrees >= 360:
        degrees -= 360
    if not math.fabs(degrees) <= 360:
        return ''

    if fmt is deg_dd:
        degrees += 1.0e-9
        return '%12.8f' % degrees

    degrees += 1.0e-8 / 36.0
    (fmin, fdeg) = math.modf(degrees)

    if fmt is deg_ddmm:
        return '%3d %09.6f\'' % (fdeg, math.fabs(60. * fmin))

    (fsec, fmin) = math.modf(60. * fmin)
    return '%3d %02d\' %08.5f\"' % (fdeg, math.fabs(fmin),
                                    math.fabs(60. * fsec))


def gpsd_units():
    """Deduce a set of units from locale and environment."""
    unit_lookup = {'imperial': imperial,
                   'metric': metric,
                   'nautical': nautical}
    if 'GPSD_UNITS' in os.environ:
        store = os.environ['GPSD_UNITS']
        if isinstance(store, (str)) and store in unit_lookup:
            return unit_lookup[store]
    for inner in ['LC_MEASUREMENT', 'LANG']:
        if inner in os.environ:
            store = os.environ[inner]
            if isinstance(store, (str)):
                if store in ['C', 'POSIX'] or store.startswith('en_US'):
                    return imperial
                return metric
    return unspecified


# Arguments are in signed decimal latitude and longitude. For example,
# the location of Montevideo (GF15vc) is: -34.91, -56.21166
# plagarized from https://ham.stackexchange.com/questions/221
# by https://ham.stackexchange.com/users/10/walter-underwood-k6wru
def maidenhead(dec_lat, dec_lon):
    """Convert latitude and longitude to Maidenhead grid locators."""
    try:
        dec_lat = float(dec_lat)
        dec_lon = float(dec_lon)
    except ValueError:
        return ''
    if _non_finite(dec_lat) or _non_finite(dec_lon):
        return ''

    if 90 < math.fabs(dec_lat) or 180 < math.fabs(dec_lon):
        return ''

    adj_lat = dec_lat + 90.0
    adj_lon = dec_lon + 180.0

    grid_lat_sq = chr(int(adj_lat / 10) + 65)
    if 'R' < grid_lat_sq:
        # A to R
        grid_lat_sq = 'R'

    grid_lon_sq = chr(int(adj_lon / 20) + 65)
    if 'R' < grid_lon_sq:
        # A to R
        grid_lon_sq = 'R'

    grid_lat_field = str(int(adj_lat % 10))
    grid_lon_field = str(int((adj_lon / 2) % 10))

    adj_lat_remainder = (adj_lat - int(adj_lat)) * 60
    adj_lon_remainder = ((adj_lon) - int(adj_lon / 2)*2) * 60

    grid_lat_subsq = chr(97 + int(adj_lat_remainder / 2.5))
    grid_lon_subsq = chr(97 + int(adj_lon_remainder / 5))

    return (grid_lon_sq + grid_lat_sq + grid_lon_field +
            grid_lat_field + grid_lon_subsq + grid_lat_subsq)


def wgs84_separation(lat, lon):
    # return geoid separation (MSL-WGS84) in meters, given a lat/lon in degrees
    """Return WGS84 geodetic separation in meters."""
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return ''
    if _non_finite(lat) or _non_finite(lon):
        return ''

    if math.fabs(lat) > 90 or math.fabs(lon) > 180:
        return ''

    row = int(math.floor((90.0 + lat) / GEOID_SPAN))
    column = int(math.floor((180.0 + lon) / GEOID_SPAN))

    if row < (GEOID_ROW - 1):
        grid_w = row
        grid_e = row + 1
    else:
        grid_w = row - 1
        grid_e = row
    if column < (GEOID_COL - 1):
        grid_s = column
        grid_n = column + 1
    else:
        grid_s = column - 1
        grid_n = column

    south = grid_s * GEOID_SPAN - 180
    north = grid_n * GEOID_SPAN - 180
    west = grid_w * GEOID_SPAN - 90
    east = grid_e * GEOID_SPAN - 90

    delta = GEOID_SPAN * GEOID_SPAN * 100
    from_west = lat - west
    from_south = lon - south
    from_east = east - lat
    from_north = north - lon

    result = GEOID_DELTA[grid_e][grid_n] * from_west * from_south
    result += GEOID_DELTA[grid_w][grid_n] * from_east * from_south
    result += GEOID_DELTA[grid_e][grid_s] * from_west * from_north
    result += GEOID_DELTA[grid_w][grid_s] * from_east * from_north
    return result / delta