# CheatSheet

# Table of Contents
- [Getting Data](#getting-data)
  - [CSV file](#csv-file)
  - [Excel file](#excel-file)
  - [Table on webpage](#table-on-webpage)
  - [Google Sheet](#google-sheet)
- [Thinking about the Data](#thinking-about-the-data)
  - [What columns are there?](#what-columns-are-there)
  - [What's at the top of the data?](#whats-at-the-top-of-the-data)
  - [What's at the bottom of the data?](#whats-at-the-bottom-of-the-data)
- [Cleaning the data](#cleaning-the-data)
  - [Deleting rows](#deleting-rows)
  - [Fixing a multi-index](#fixing-a-multi-index)
  - [Renaming Columns](#renaming-columns)
- [Plotly Express](#plotly-express)
  - [Import the library](#import-the-library)
  - [Bar chart](#bar-chart)
  - [Comparison Operators](#comparison-operators)

# Getting Data

## CSV file

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/read-csv.png" alt="pd.read_csv()" width="45%">
</div>

## Excel file

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/read_excel.png" alt="pd.read_excel()" width="95%">
</div>

## Table on webpage

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/read_html.png" alt="pd.read_html()" width="90%">
</div>

## Google Sheet

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/google-sheet.png" alt="google sheet" width="90%">
</div>

# Thinking about the Data

## What columns are there?

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/columns.png" alt="columns" width="40%">
</div>

## What's at the top of the data?

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/head.png" alt="head()" width="40%">
</div>

## What's at the bottom of the data?

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/tail.png" alt="tail()" width="40%">
</div>

# Cleaning the data

## Deleting rows

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/drop.png" alt="df.drop()" width="40%">
</div>

## Fixing a multi-index

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/multi-index-fix.png" alt="df.columns.map('_'.join)" width="70%">
</div>

## Renaming Columns

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/rename.png" alt="rename columns" width="60%">
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/rename_2.png" alt="rename columns" width="70%">
</div>

# Plotly Express

Here are some cheat sheets or tutorials that might also help you. 

+ [kdnuggets.com](https://www.kdnuggets.com/publications/sheets/Plotly_Express_for_Data_Visualization_Cheat_Sheet_KDnuggets.pdf) (PDF)
+ [towardsdatascience.com](https://towardsdatascience.com/cheat-codes-to-better-visualisations-with-plotly-express-21caece3db01) 
+ [franzdiebold.github.io](https://franzdiebold.github.io/plotly-express-cheat-sheet/Plotly_Express_cheat_sheet.pdf) (PDF) (Also available in [Colab](https://colab.research.google.com/github/FranzDiebold/plotly-express-cheat-sheet/blob/main/plotly-express-cheat-sheet.ipynb))
+ [franzdiebold.github.io](https://images.franzdiebold.github.io/image/upload/v1668605954/Marketing/Blog/Plotly_Cheat_Sheet.pdf) (PDF)

## Import the library

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/import-plotly-express.png" alt="import plotly.express as px" width="65%">
</div>

## Bar chart

<div align="center">
<img src="https://raw.githubusercontent.com/pbeens/Data-Dunkers/main/Images/cheatsheet/plotly-express-bar-chart.png" alt="fig = px.bar()" width="75%">
</div>

## Comparison Operators

|Symbol|Meaning|
|-|-|
|>|greater than|
|<|less than|
|==|is equal to|
|!=|not equal to|
|>=|greater than or equal to|
|<=|less than or equal to|
|&|and|
|\||or|