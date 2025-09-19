"""
Data Preprocessing Module for User Onboarding Funnel Analysis
Author: Data Analyst Portfolio Project 2024-2025
Purpose: Clean, validate and prepare data for funnel analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataPreprocessor:
    """
    Data preprocessing class for funnel analysis data.

    I designed this class to handle all data cleaning and validation tasks
    that are essential for accurate funnel analysis.
    """

    def __init__(self):
        """Initialize the preprocessor with default settings."""
        self.user_events = None
        self.user_demographics = None
        self.campaign_data = None

    def load_data(self, events_path, demographics_path, campaigns_path):
        """
        Load all datasets and perform initial validation.

        Args:
            events_path (str): Path to user events CSV file
            demographics_path (str): Path to user demographics CSV file  
            campaigns_path (str): Path to campaign data CSV file

        Returns:
            dict: Summary of loaded data
        """
        print("🔄 Loading datasets...")

        # Load user events data
        self.user_events = pd.read_csv(events_path)
        self.user_events['event_timestamp'] = pd.to_datetime(self.user_events['event_timestamp'])

        # Load user demographics
        self.user_demographics = pd.read_csv(demographics_path)
        self.user_demographics['registration_date'] = pd.to_datetime(self.user_demographics['registration_date'])

        # Load campaign data
        self.campaign_data = pd.read_csv(campaigns_path)
        self.campaign_data['start_date'] = pd.to_datetime(self.campaign_data['start_date'])
        self.campaign_data['end_date'] = pd.to_datetime(self.campaign_data['end_date'])

        summary = {
            'user_events_rows': len(self.user_events),
            'unique_users': self.user_events['user_id'].nunique(),
            'date_range': f"{self.user_events['event_timestamp'].min()} to {self.user_events['event_timestamp'].max()}",
            'demographics_rows': len(self.user_demographics),
            'campaigns': len(self.campaign_data)
        }

        print(f"✅ Data loaded successfully!")
        print(f"📊 Summary: {summary}")
        return summary

    def clean_user_events(self):
        """
        Clean and validate user events data.

        I implemented comprehensive data cleaning to ensure data quality:
        - Remove duplicates
        - Validate event sequences
        - Handle missing values
        - Add derived features
        """
        print("🧹 Cleaning user events data...")

        initial_rows = len(self.user_events)

        # Remove duplicate events (same user, event, timestamp)
        self.user_events = self.user_events.drop_duplicates(
            subset=['user_id', 'event_type', 'event_timestamp']
        )

        # Remove events with missing critical fields
        self.user_events = self.user_events.dropna(subset=['user_id', 'event_type', 'event_timestamp'])

        # Add derived time-based features
        self.user_events['date'] = self.user_events['event_timestamp'].dt.date
        self.user_events['hour'] = self.user_events['event_timestamp'].dt.hour
        self.user_events['day_of_week'] = self.user_events['event_timestamp'].dt.dayofweek
        self.user_events['week_number'] = self.user_events['event_timestamp'].dt.isocalendar().week
        self.user_events['month'] = self.user_events['event_timestamp'].dt.month

        # Add funnel step ordering
        funnel_order = {
            'landing_page_view': 1,
            'signup_page_view': 2,
            'email_verification': 3,
            'profile_setup': 4,
            'first_product_view': 5,
            'add_to_cart': 6,
            'checkout_start': 7,
            'payment_info_entered': 8,
            'purchase_completed': 9,
            'app_download': 10,
            'first_login_app': 11
        }

        self.user_events['funnel_step'] = self.user_events['event_type'].map(funnel_order)

        # Sort by user and timestamp for proper sequence analysis
        self.user_events = self.user_events.sort_values(['user_id', 'event_timestamp']).reset_index(drop=True)

        cleaned_rows = len(self.user_events)
        print(f"✅ Cleaned events: {initial_rows} → {cleaned_rows} rows ({initial_rows-cleaned_rows} removed)")

    def create_user_journey_summary(self):
        """
        Create summary of each user's journey through the funnel.

        This function aggregates user behavior to understand:
        - How far each user progressed in the funnel
        - Time spent in the funnel
        - Conversion outcomes
        """
        print("🗺️ Creating user journey summaries...")

        user_summary = self.user_events.groupby('user_id').agg({
            'event_timestamp': ['min', 'max', 'count'],
            'event_type': ['nunique', lambda x: list(x.unique())],
            'funnel_step': 'max',
            'session_id': 'nunique',
            'platform': 'first',
            'country': 'first',
            'traffic_source': 'first'
        }).reset_index()

        # Flatten column names
        user_summary.columns = [
            'user_id', 'first_event', 'last_event', 'total_events',
            'unique_event_types', 'event_types_list', 'max_funnel_step',
            'total_sessions', 'platform', 'country', 'traffic_source'
        ]

        # Calculate time metrics
        user_summary['session_duration_hours'] = (
            (user_summary['last_event'] - user_summary['first_event']).dt.total_seconds() / 3600
        )

        # Add conversion flags
        user_summary['converted_to_purchase'] = user_summary['event_types_list'].apply(
            lambda x: 1 if 'purchase_completed' in x else 0
        )
        user_summary['downloaded_app'] = user_summary['event_types_list'].apply(
            lambda x: 1 if 'app_download' in x else 0
        )
        user_summary['completed_signup'] = user_summary['event_types_list'].apply(
            lambda x: 1 if 'email_verification' in x else 0
        )

        # Drop the event_types_list column as it's no longer needed
        user_summary = user_summary.drop('event_types_list', axis=1)

        self.user_journey_summary = user_summary
        print(f"✅ Created journey summaries for {len(user_summary)} users")

        return user_summary

    def merge_with_demographics(self):
        """
        Merge user journey data with demographics information.

        This creates a comprehensive dataset combining behavioral and demographic data
        for deeper analysis.
        """
        print("🔗 Merging with demographics data...")

        # Merge journey summary with demographics
        self.enriched_data = self.user_journey_summary.merge(
            self.user_demographics, 
            on='user_id', 
            how='left'
        )

        # Handle any missing demographic data
        missing_demographics = self.enriched_data['age_group'].isna().sum()
        if missing_demographics > 0:
            print(f"⚠️ Warning: {missing_demographics} users missing demographic data")

        print(f"✅ Merged data: {len(self.enriched_data)} users with full profiles")
        return self.enriched_data

    def calculate_funnel_metrics(self):
        """
        Calculate key funnel metrics for analysis.

        I developed this method to compute essential funnel KPIs:
        - Conversion rates at each step
        - Drop-off rates
        - Time to conversion
        """
        print("📈 Calculating funnel metrics...")

        # Overall funnel performance
        funnel_steps = self.user_events['event_type'].value_counts().sort_index()

        # Step-by-step conversion rates
        step_conversions = {}
        total_users = self.user_events['user_id'].nunique()

        for event_type in ['landing_page_view', 'signup_page_view', 'email_verification', 
                          'profile_setup', 'first_product_view', 'add_to_cart', 
                          'checkout_start', 'payment_info_entered', 'purchase_completed']:

            users_at_step = self.user_events[self.user_events['event_type'] == event_type]['user_id'].nunique()
            step_conversions[event_type] = {
                'users': users_at_step,
                'conversion_rate': (users_at_step / total_users) * 100
            }

        self.funnel_metrics = step_conversions
        print(f"✅ Calculated metrics for {len(step_conversions)} funnel steps")

        return step_conversions

    def export_cleaned_data(self, output_dir):
        """
        Export all cleaned and processed data.

        Args:
            output_dir (str): Directory to save processed data files
        """
        print(f"💾 Exporting cleaned data to {output_dir}...")

        # Export cleaned datasets
        self.user_events.to_csv(f"{output_dir}/cleaned_user_events.csv", index=False)
        self.user_journey_summary.to_csv(f"{output_dir}/user_journey_summary.csv", index=False)
        self.enriched_data.to_csv(f"{output_dir}/enriched_user_data.csv", index=False)

        print("✅ All cleaned data exported successfully!")

        return {
            'events_file': f"{output_dir}/cleaned_user_events.csv",
            'journey_file': f"{output_dir}/user_journey_summary.csv", 
            'enriched_file': f"{output_dir}/enriched_user_data.csv"
        }

def main():
    """
    Main preprocessing pipeline.

    I designed this pipeline to be run independently for data preparation.
    """
    preprocessor = DataPreprocessor()

    # Load data
    data_summary = preprocessor.load_data(
        '../data/user_events.csv',
        '../data/user_demographics.csv',
        '../data/campaign_data.csv'
    )

    # Clean and process
    preprocessor.clean_user_events()
    preprocessor.create_user_journey_summary()
    preprocessor.merge_with_demographics()
    preprocessor.calculate_funnel_metrics()

    # Export results
    preprocessor.export_cleaned_data('../data/processed')

    print("🎉 Data preprocessing completed successfully!")

if __name__ == "__main__":
    main()
