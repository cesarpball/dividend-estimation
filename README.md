# Dividend Estimation Tool

## Quick Start Guide
At the moment, only Spain taxes are supported..


### Installing Dependencies

1. Create a virtual environment:

```bash
python -m venv venv
```
2. Install the required dependencies:
```bash
source venv/bin/activate  # On Linux/Mac
pip install -r requirements.txt
````
3. Run the application:
```bash
python python3 dividend_calculator.py --portfolio portfolio.json
```

The result would be like
```
Dividend Payment Schedule:
------------------------------------------------------------------------------------------
Stock  Payment Date Shares   Per Share  Total USD  Total EUR 
------------------------------------------------------------------------------------------

February 2025
------------------------------------------------------------------------------------------
O      2025-02-28   100      $0.26      $25.70     €24.52
ADC    2025-02-28   100      $0.25      $24.70     €23.56
MCD    2025-02-28   100      $1.67      $167.00    €159.32

March 2025
------------------------------------------------------------------------------------------
KO     2025-03-14   100      $0.48      $48.50     €46.27
ADC    2025-03-27   100      $0.25      $24.70     €23.56
O      2025-03-28   100      $0.26      $25.70     €24.52

April 2025
------------------------------------------------------------------------------------------
ADC    2025-04-29   100      $0.25      $25.00     €23.85
O      2025-04-30   100      $0.26      $25.70     €24.52

May 2025
------------------------------------------------------------------------------------------
ADC    2025-05-31   100      $0.25      $25.00     €23.85

June 2025
------------------------------------------------------------------------------------------
O      2025-06-03   100      $0.26      $26.30     €25.09
MCD    2025-06-03   100      $1.67      $167.00    €159.32
KO     2025-06-14   100      $0.48      $48.50     €46.27
ADC    2025-06-28   100      $0.25      $25.00     €23.85

July 2025
------------------------------------------------------------------------------------------
O      2025-07-01   100      $0.26      $26.30     €25.09
ADC    2025-07-31   100      $0.25      $25.00     €23.85

August 2025
------------------------------------------------------------------------------------------
O      2025-08-01   100      $0.26      $26.30     €25.09
ADC    2025-08-30   100      $0.25      $25.00     €23.85

September 2025
------------------------------------------------------------------------------------------
O      2025-09-03   100      $0.26      $26.30     €25.09
MCD    2025-09-03   100      $1.67      $167.00    €159.32
KO     2025-09-13   100      $0.48      $48.50     €46.27
ADC    2025-09-30   100      $0.25      $25.00     €23.85

October 2025
------------------------------------------------------------------------------------------
O      2025-10-01   100      $0.26      $26.40     €25.19
ADC    2025-10-31   100      $0.25      $25.30     €24.14

November 2025
------------------------------------------------------------------------------------------
O      2025-11-01   100      $0.26      $26.40     €25.19
ADC    2025-11-29   100      $0.25      $25.30     €24.14
KO     2025-11-29   100      $0.48      $48.50     €46.27

December 2025
------------------------------------------------------------------------------------------
O      2025-12-02   100      $0.26      $26.40     €25.19
MCD    2025-12-02   100      $1.77      $177.00    €168.86
ADC    2025-12-31   100      $0.25      $25.30     €24.14

January 2026
------------------------------------------------------------------------------------------
O      2026-01-02   100      $0.26      $26.40     €25.19
ADC    2026-01-31   100      $0.25      $25.30     €24.14

February 2026
------------------------------------------------------------------------------------------
O      2026-02-03   100      $0.26      $26.40     €25.19

Monthly Expected Totals:
----------------------------------------
February 2025 $217.40 | €207.40
March 2025   $98.90 | €94.35
April 2025   $50.70 | €48.37
May 2025     $25.00 | €23.85
June 2025    $266.80 | €254.53
July 2025    $51.30 | €48.94
August 2025  $51.30 | €48.94
September 2025 $266.80 | €254.53
October 2025 $51.70 | €49.32
November 2025 $100.20 | €95.59
December 2025 $228.70 | €218.18
January 2026 $51.70 | €49.32
February 2026 $26.40 | €25.19

Yearly Expected Totals:
----------------------------------------
2025         $1408.80 | €1344.00
2026         $78.10 | €74.51

Yearly Tax Calculations:
------------------------------------------------------------
2025         Gross: €1344.00 | Tax: €255.36 | Net: €1088.64
2026         Gross: €74.51 | Tax: €14.16 | Net: €60.35
```

# License

MIT License

Copyright (c) 2024 Dividend Estimation Tool

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
