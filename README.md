# CBVWGAI-Final-Project-Pedro-Osorio
Creating business value with generative AI final project by Pedro Henrique Gutierrez Osorio
# Excel Data Analysis Tool

A Python-based tool for comprehensive analysis of Excel survey data, featuring sentiment analysis, response rate tracking, and automated visualization generation.

## Features

- **Comprehensive Column Analysis**:
  - Analysis of categorical data (Column F)
  - Yes/No response analysis
  - Free-text response analysis
  - Response rate calculations
  - Sentiment analysis of text responses

- **Visualization Generation**:
  - Combined visualization dashboard
  - Bar charts for categorical data
  - Pie charts for Yes/No responses
  - Response rate visualizations
  - All visualizations saved as high-resolution PNG files

- **Sentiment Analysis**:
  - Text polarity calculation (-1 to 1)
  - Subjectivity measurement (0 to 1)
  - Sentiment distribution (Positive/Negative/Neutral)
  - Average sentiment metrics per column

## Requirements

- Python 3.x
- Required Python packages:
  - pandas
  - matplotlib
  - textblob
  - openpyxl (for .xlsx files)
  - xlrd (for .xls files)

## Installation

1. Clone this repository or download the script
2. Install required packages:
```bash
pip install pandas matplotlib textblob openpyxl xlrd
```

## Usage

1. Place your Excel file (.xlsx or .xls) in the same directory as the script
2. Run the script:
```bash
python data_analyzer.py
```
3. If multiple Excel files are present, select the desired file when prompted
4. The script will create an output directory with:
   - Complete analysis text file
   - Combined visualization image
   - Analysis timestamp for reference

## Output

The tool generates two main outputs:

1. **Text Analysis** (`complete_analysis.txt`):
   - Detailed statistics for each column
   - Response rates and distributions
   - Sentiment analysis results
   - Category breakdowns

2. **Visual Analysis** (`combined_analysis.png`):
   - Multi-panel visualization
   - Color-coded charts and graphs
   - Response distribution visualizations
   - Easy-to-interpret data representations

## Analysis Components

### Column F Analysis
- Categorizes and counts responses
- Generates distribution statistics
- Creates bar chart visualization

### Yes/No Columns Analysis (G, I, K, M, O)
- Response distribution analysis
- Percentage calculations
- Pie chart visualizations

### Response Columns Analysis (H, J, L, N, P, Q)
- Response rate tracking
- Empty cell analysis
- Content presence verification

### Sentiment Analysis
- Text polarity measurement
- Subjectivity analysis
- Sentiment categorization
- Average sentiment calculations

## Error Handling

The tool includes comprehensive error handling for:
- Missing files
- Invalid data formats
- Empty responses
- Data processing errors

## Output Directory Structure

```
analysis_output_[timestamp]/
├── complete_analysis.txt
└── combined_analysis.png
```

## Limitations

- Designed for specific Excel format with columns F through Q
- Requires text content for sentiment analysis
- Memory usage may increase with large Excel files

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
