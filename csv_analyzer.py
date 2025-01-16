import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
from textblob import TextBlob

class DataAnalyzer:
    def analyze_sentiment(self, text):
        """
        Analyze sentiment of text using TextBlob
        Returns polarity (-1 to 1) and subjectivity (0 to 1)
        """
        if pd.isna(text) or not isinstance(text, str):
            return None, None
        
        analysis = TextBlob(str(text))
        return analysis.sentiment.polarity, analysis.sentiment.subjectivity
    
    def analyze_column_sentiment(self, column_data, column_name):
        """
        Analyze sentiment for all responses in a column
        """
        sentiments = []
        for text in column_data:
            polarity, subjectivity = self.analyze_sentiment(text)
            if polarity is not None:
                sentiments.append({
                    'polarity': polarity,
                    'subjectivity': subjectivity
                })
        
        if not sentiments:
            return None
        
        # Calculate average sentiment metrics
        avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
        avg_subjectivity = sum(s['subjectivity'] for s in sentiments) / len(sentiments)
        
        # Count sentiment categories
        positive = sum(1 for s in sentiments if s['polarity'] > 0)
        negative = sum(1 for s in sentiments if s['polarity'] < 0)
        neutral = sum(1 for s in sentiments if s['polarity'] == 0)
        
        return {
            'column_name': column_name,
            'responses_analyzed': len(sentiments),
            'avg_polarity': avg_polarity,
            'avg_subjectivity': avg_subjectivity,
            'sentiment_distribution': {
                'positive': positive,
                'negative': negative,
                'neutral': neutral
            }
        }

    def analyze_all_columns(self, df, output_dir):
        """
        Analyze all columns and create a single combined visualization
        """
        try:
            # Calculate total number of subplots needed
            # 1 for Column F + 5 for Yes/No columns + 6 for response columns = 12 total
            total_plots = 12
            
            # Create a figure with a grid of subplots
            fig = plt.figure(figsize=(20, 25))  # Increased figure size for better visibility
            
            # Add a main title to the figure
            fig.suptitle('Complete Analysis of All Columns', fontsize=16, y=0.95)
            
            # Current plot position
            plot_pos = 1
            
            # Analyze Column F (categories)
            print("\nAnalyzing Column F categories...")
            column_f = df.iloc[:, 5]
            column_name_f = df.columns[5]
            cleaned_responses = column_f.fillna("No Answer").astype(str).str.strip()
            response_counts = cleaned_responses.value_counts()
            
            # Create subplot for Column F
            plt.subplot(4, 3, plot_pos)
            bars = plt.bar(range(len(response_counts)), response_counts.values)
            plt.title(f'Column F:\n{column_name_f}', fontsize=10)
            plt.xticks(range(len(response_counts)), response_counts.index, rotation=45, ha='right', fontsize=8)
            plt.ylabel('Number of Responses', fontsize=8)
            
            # Add value labels on top of each bar
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)
            
            f_stats = {
                'column_name': column_name_f,
                'category_counts': response_counts.to_dict(),
                'category_percentages': (response_counts / len(column_f) * 100).to_dict()
            }
            
            plot_pos += 1
            
            # Analyze Yes/No columns (G, I, K, M, O)
            yes_no_columns = [6, 8, 10, 12, 14]
            yes_no_stats = []
            
            print("\nAnalyzing Yes/No columns...")
            for col_index in yes_no_columns:
                if col_index < len(df.columns):
                    column_data = df.iloc[:, col_index]
                    column_name = df.columns[col_index]
                    
                    # Clean and standardize responses
                    cleaned_responses = column_data.fillna('No Response').astype(str).str.strip().str.lower()
                    
                    # Count Yes/No responses
                    yes_count = sum(cleaned_responses == 'yes')
                    no_count = sum(cleaned_responses == 'no')
                    no_response_count = len(cleaned_responses) - (yes_count + no_count)
                    
                    response_counts = {
                        'Yes': yes_count,
                        'No': no_count,
                        'No Response': no_response_count
                    }
                    
                    # Create subplot
                    plt.subplot(4, 3, plot_pos)
                    colors = ['#2ecc71', '#e74c3c', '#95a5a6']
                    plt.pie(response_counts.values(),
                           labels=[f"{k}\n({v})" for k, v in response_counts.items()],
                           colors=colors,
                           autopct='%1.1f%%',
                           textprops={'fontsize': 8})
                    plt.title(f'{column_name}', fontsize=10)
                    
                    stats = {
                        'column_name': column_name,
                        'counts': response_counts,
                        'percentages': {k: (v/len(column_data))*100 for k, v in response_counts.items()}
                    }
                    yes_no_stats.append(stats)
                    
                    plot_pos += 1
            
            # Analyze response columns (H, J, L, N, P, Q)
            response_columns = [7, 9, 11, 13, 15, 16]
            response_stats = []
            sentiment_stats = []  # Add sentiment_stats list
            
            print("\nAnalyzing response columns...")
            for col_index in response_columns:
                if col_index < len(df.columns):
                    column_data = df.iloc[:, col_index]
                    column_name = df.columns[col_index]
                    
                    # Count responses
                    has_content = []
                    for value in column_data:
                        if pd.isna(value) or value is None:
                            has_content.append(False)
                        else:
                            str_value = str(value).strip()
                            has_content.append(len(str_value) > 0 and str_value.lower() != 'nan')
                    
                    response_counts = {
                        'Answered': sum(has_content),
                        'Not Answered': len(column_data) - sum(has_content)
                    }
                    
                    # Create subplot
                    plt.subplot(4, 3, plot_pos)
                    colors = ['#2ecc71', '#e74c3c']
                    plt.pie([response_counts['Answered'], response_counts['Not Answered']],
                           labels=[f"Answered\n({response_counts['Answered']})",
                                  f"Not Answered\n({response_counts['Not Answered']})"],
                           colors=colors,
                           autopct='%1.1f%%',
                           textprops={'fontsize': 8})
                    plt.title(f'{column_name}', fontsize=10)
                    
                    stats = {
                        'column_name': column_name,
                        'total_cells': len(column_data),
                        'answered': response_counts['Answered'],
                        'not_answered': response_counts['Not Answered'],
                        'response_rate': (response_counts['Answered'] / len(column_data) * 100)
                    }
                    response_stats.append(stats)
                    
                    # Add sentiment analysis
                    sentiment_result = self.analyze_column_sentiment(column_data, column_name)
                    if sentiment_result:
                        sentiment_stats.append(sentiment_result)
                    
                    plot_pos += 1
            
            # Adjust layout and save the combined figure
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plot_path = output_dir / 'combined_analysis.png'
            plt.savefig(plot_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            return str(plot_path), f_stats, yes_no_stats, response_stats, sentiment_stats
            
        except Exception as e:
            print(f"Error in analyze_all_columns: {str(e)}")
            return None, None, None, None, None

    def analyze_excel(self, file_path):
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return "Error: File not found", None
            
            print("Reading Excel file...")
            df = pd.read_excel(file_path)
            
            print("Creating visualizations...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = file_path.parent / f"analysis_output_{timestamp}"
            output_dir.mkdir(exist_ok=True)
            
            # Analyze all columns and create combined visualization
            plot_path, f_stats, yes_no_stats, response_stats, sentiment_stats = self.analyze_all_columns(df, output_dir)
            
            if all([plot_path, f_stats, yes_no_stats, response_stats]):
                # Create comprehensive analysis text
                analysis_text = "COMPLETE ANALYSIS RESULTS:\n\n"
                
                # Add Yes/No analysis
                analysis_text += "YES/NO COLUMNS ANALYSIS:\n"
                analysis_text += "=" * 50 + "\n\n"
                for stats in yes_no_stats:
                    analysis_text += f"Column: {stats['column_name']}\n"
                    for category, count in stats['counts'].items():
                        percentage = stats['percentages'][category]
                        analysis_text += f"{category}: {count} responses ({percentage:.1f}%)\n"
                    analysis_text += "\n"
                
                # Add Column F analysis
                analysis_text += "\nCOLUMN F ANALYSIS:\n"
                analysis_text += "=" * 50 + "\n\n"
                analysis_text += f"Column: {f_stats['column_name']}\n"
                analysis_text += "Category Distribution:\n"
                for category, count in f_stats['category_counts'].items():
                    percentage = f_stats['category_percentages'][category]
                    analysis_text += f"{category}: {count} responses ({percentage:.1f}%)\n"
                analysis_text += "\n"
                
                # Add other columns analysis
                analysis_text += "\nRESPONSE COLUMNS ANALYSIS:\n"
                analysis_text += "=" * 50 + "\n\n"
                for stats in response_stats:
                    analysis_text += f"""Column: {stats['column_name']}
Total Cells: {stats['total_cells']}
Answered Cells: {stats['answered']}
Empty Cells: {stats['not_answered']}
Response Rate: {stats['response_rate']:.1f}%

"""
                # Add sentiment analysis section
                if sentiment_stats:
                    analysis_text += "\nSENTIMENT ANALYSIS:\n"
                    analysis_text += "=" * 50 + "\n\n"
                    for stats in sentiment_stats:
                        analysis_text += f"Column: {stats['column_name']}\n"
                        analysis_text += f"Responses Analyzed: {stats['responses_analyzed']}\n"
                        analysis_text += f"Average Sentiment (Polarity): {stats['avg_polarity']:.2f} "
                        # Add interpretation
                        if stats['avg_polarity'] > 0:
                            analysis_text += "(Generally Positive)\n"
                        elif stats['avg_polarity'] < 0:
                            analysis_text += "(Generally Negative)\n"
                        else:
                            analysis_text += "(Generally Neutral)\n"
                        
                        analysis_text += f"Average Subjectivity: {stats['avg_subjectivity']:.2f}\n"
                        analysis_text += "Sentiment Distribution:\n"
                        dist = stats['sentiment_distribution']
                        total = sum(dist.values())
                        for category, count in dist.items():
                            percentage = (count / total) * 100
                            analysis_text += f"  - {category.title()}: {count} responses ({percentage:.1f}%)\n"
                        analysis_text += "\n"
                
                analysis_text += "\nA combined visualization has been saved as 'combined_analysis.png'"
                
                # Save analysis to a text file
                analysis_path = output_dir / "complete_analysis.txt"
                with open(analysis_path, "w") as f:
                    f.write(analysis_text)
                
                return analysis_text, str(output_dir)
            
            return "Analysis failed to generate results.", None
            
        except Exception as e:
            return f"Error: {str(e)}", None

if __name__ == "__main__":
    current_dir = Path(__file__).parent
    excel_files = list(current_dir.glob("*.xlsx")) + list(current_dir.glob("*.xls"))
    
    if not excel_files:
        print("No Excel files found in the current directory!")
        print(f"Please place an Excel file (.xlsx or .xls) in: {current_dir}")
        exit()
    
    if len(excel_files) > 1:
        print("\nFound multiple Excel files:")
        for i, file in enumerate(excel_files, 1):
            print(f"{i}. {file.name}")
        choice = input("\nEnter the number of the file to analyze: ")
        try:
            excel_file = excel_files[int(choice) - 1]
        except:
            print("Invalid choice. Please run the script again.")
            exit()
    else:
        excel_file = excel_files[0]
    
    analyzer = DataAnalyzer()
    print(f"\nAnalyzing file: {excel_file.name}")
    print("Starting analysis...")
    result, output_dir = analyzer.analyze_excel(excel_file)
    
    if output_dir:
        print(f"\nAnalysis complete! Check the output folder: {output_dir}")
        print("\nAnalysis Result:")
        print(result)
    else:
        print("\nAnalysis failed:", result)