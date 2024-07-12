import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

from scipy.ndimage import gaussian_filter1d

def read_data_from_db(db_file):
    """
    Connect to the SQLite database and read the data into a Pandas DataFrame
    """
    conn = sqlite3.connect(db_file)
    query = "SELECT * FROM detections"
    df = pd.read_sql_query(query, conn)
    conn.close()
    print("Data read from database:")
    print(df.head())
    return df

def filter_bird_data(df):
    """
    Filter the DataFrame to include only rows where the class is 'bird'
    """
    print("Unique classes in the dataset:")
    print(df['class'].unique())
    
    bird_df = df[df['class'].str.lower() == 'bird']
    print("Filtered bird data:")
    print(bird_df.head())
    return bird_df

def convert_timestamp_to_seconds(df):
    """
    Convert the timestamp to seconds, handling both ':' and '.' separators
    """
    def convert_to_seconds(timestamp):
        # Split timestamp by ':' or '.' to handle both formats
        parts = timestamp.split(':') if ':' in timestamp else timestamp.split('.')
        if len(parts) == 3:
            # Convert to seconds
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])  # Use float to handle decimal seconds
                total_seconds = hours * 3600 + minutes * 60 + seconds
                return total_seconds
            except ValueError as e:
                print(f"Error converting timestamp {timestamp}: {e}")
                return None
        else:
            print(f"Invalid timestamp format: {timestamp}")
            return None
    
    df['seconds'] = df['timestamp'].apply(convert_to_seconds)
    print("Data with timestamps converted to seconds:")
    print(df[['timestamp', 'seconds']].head())
    return df

def examine_data_distribution(bird_df):
    """
    DEBUGGING: Print the distribution of timestamps to examine the data.
    """
    print("Timestamp distribution in the data:")
    print(bird_df['timestamp'].value_counts().sort_index().head(20))  # Print the first 20 timestamps and their counts

def plot_bird_detections_over_time(bird_df):
    """
    Produce a plot showing the number of birds detected over the duration of the video
    """
    # Convert timestamp to seconds
    bird_df = convert_timestamp_to_seconds(bird_df)
    
    # Group by second and count the number of birds detected
    bird_count_per_second = bird_df.groupby('seconds').size().reset_index(name='bird_count')
    print("Bird count per second:")
    print(bird_count_per_second.head())
    
    if bird_count_per_second.empty:
        print("No bird detections found for plotting.")
        return
    
    # Apply Gaussian smoothing to smooth the data
    bird_count_per_second['smoothed_bird_count'] = gaussian_filter1d(bird_count_per_second['bird_count'], sigma=2)
    
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    
    # Create a line plot of bird detections over time
    sns.lineplot(x='seconds', y='smoothed_bird_count', data=bird_count_per_second, marker='o')
    
    # Determine max values for setting plot limits
    max_seconds = bird_count_per_second['seconds'].max()
    max_birds = bird_count_per_second['smoothed_bird_count'].max()
    
    plt.title('Number of Birds Detected Over Video Duration')
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Number of Birds Detected (Smoothed)')
    plt.xlim(0, max_seconds)    
    plt.ylim(0, max_birds)
    plt.tight_layout()
    
    # Ensure the output directory exists
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save the plot
    plot_path = os.path.join(output_dir, 'bird_detections_over_time.png')
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")
    plt.show()

def main():
    db_file = 'detections.db'
    df = read_data_from_db(db_file)
    bird_df = filter_bird_data(df)
    examine_data_distribution(bird_df)
    plot_bird_detections_over_time(bird_df)

if __name__ == "__main__":
    main()
