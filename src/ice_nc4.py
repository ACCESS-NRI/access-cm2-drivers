#!/usr/bin/env python3

# Convert CICE history to netCDF4 and combine separate daily files
# into a single monthly file.

# Note that adding shuffle actually increases the size of the
# monthly files.

# Should be run in the CICE history output directory

import os, glob, re, subprocess, warnings
from collections import defaultdict
from calendar import monthrange

# Expect that all files have prefix iceh

# Check for end of string so as not to match nc4 files etc.
# Rename to iceh_m and iceh_d so that they don't match.
verbose = True
re_monthly = re.compile(r"iceh\.\d{4}-\d{2}\.nc")
re_daily = re.compile(r"iceh\.\d{4}-\d{2}-\d{2}\.nc")

monthly = []
daily = []
for f in glob.glob('iceh.*.nc'):
    if re_monthly.match(f):
        monthly.append(f)
    elif re_daily.match(f):
        daily.append(f)
    else:
        warnings.warn(f"Unexpected file '{f}'.")

# Convert monthly data to netCDF4 format and compress
if monthly:
    for f in monthly:
        cmd = ["nccopy", "-k3", "-d4", f, f"iceh_m{f[4:]}"]
        if verbose:
            print(cmd)
        subprocess.check_call(cmd, stderr=subprocess.STDOUT)
else:
    print("No monthly data to process.")

# Combine separate daily data in the same netCDF4 file
if daily:
    daily.sort()
    # Group files with same year and month
    grouped = defaultdict(list)
    for filename in daily:
        year, month, _ = filename[5:-3].split("-")
        grouped[(year, month)].append(filename)
    
    # Combine data if all days are present for each year-month group
    for (year, month), files in grouped.items():
        days_in_month = monthrange(int(year), int(month))[1]
        available_days = [int(f[-5:-3]) for f in files]
        if all(day in available_days for day in range(1, days_in_month + 1)):
            cmd = ["ncrcat", "-4", "--deflate", "4", *files, f"iceh_d.{year}-{month}.nc"]
            if verbose:
                print(cmd)
            subprocess.check_call(cmd, stderr=subprocess.STDOUT)
        else:
            raise Exception(f"Missing daily data for {year}-{month}. Available files: {files}")
else:
    print("No daily data to process.")