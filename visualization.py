"""
Visualization Module for User Onboarding Funnel Analysis
Author: Data Analyst Portfolio Project 2024-2025
Purpose: Generate comprehensive visualizations for funnel analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
plt.style.use('default')
sns.set_palette("husl")

class FunnelVisualizer:
    """
    Comprehensive visualization class for funnel analysis.

    I created this class to generate publication-ready charts for my portfolio.
    All visualizations are designed to tell a clear story about user behavior.
    """

    def __init__(self, user_events_df, user_demographics_df, campaign_df):
        """
        Initialize visualizer with data.

        Args:
            user_events_df (pd.DataFrame): Cleaned user events data
            user_demographics_df (pd.DataFrame): User demographics data
            campaign_df (pd.DataFrame): Campaign performance data
        """
        self.events_df = user_events_df
        self.demographics_df = user_demographics_df
        self.campaign_df = campaign_df

        # Create processed datasets for analysis
        self._prepare_analysis_data()

    def _prepare_analysis_data(self):
        """Prepare data for visualization analysis."""

        # Calculate funnel metrics
        self.funnel_data = self._calculate_funnel_metrics()

        # Platform performance data
        self.platform_data = self._calculate_platform_metrics()

        # Time-based analysis data
        self.time_data = self._calculate_time_metrics()

    def _calculate_funnel_metrics(self):
        """Calculate core funnel conversion metrics."""

        funnel_events = [
            'landing_page_view', 'signup_page_view', 'email_verification',
            'profile_setup', 'first_product_view', 'add_to_cart',
            'checkout_start', 'payment_info_entered', 'purchase_completed'
        ]

        funnel_metrics = []

        for i, event in enumerate(funnel_events):
            users_at_step = self.events_df[self.events_df['event_type'] == event]['user_id'].nunique()

            if i == 0:
                step_conversion = 100.0
                overall_conversion = 100.0
            else:
                previous_users = funnel_metrics[i-1]['users_at_step']
                step_conversion = (users_at_step / previous_users) * 100 if previous_users > 0 else 0
                total_users = funnel_metrics[0]['users_at_step']
                overall_conversion = (users_at_step / total_users) * 100 if total_users > 0 else 0

            funnel_metrics.append({
                'step': i + 1,
                'event_type': event,
                'event_label': event.replace('_', ' ').title(),
                'users_at_step': users_at_step,
                'step_conversion_rate': step_conversion,
                'overall_conversion_rate': overall_conversion,
                'drop_off_rate': 100 - step_conversion if i > 0 else 0
            })

        return pd.DataFrame(funnel_metrics)

    def _calculate_platform_metrics(self):
        """Calculate platform-specific performance metrics."""

        platform_metrics = []

        for platform in self.events_df['platform'].unique():
            platform_events = self.events_df[self.events_df['platform'] == platform]

            visitors = platform_events[platform_events['event_type'] == 'landing_page_view']['user_id'].nunique()
            signups = platform_events[platform_events['event_type'] == 'signup_page_view']['user_id'].nunique()
            purchases = platform_events[platform_events['event_type'] == 'purchase_completed']['user_id'].nunique()

            platform_metrics.append({
                'platform': platform,
                'visitors': visitors,
                'signups': signups,
                'purchases': purchases,
                'signup_rate': (signups / visitors * 100) if visitors > 0 else 0,
                'conversion_rate': (purchases / visitors * 100) if visitors > 0 else 0
            })

        return pd.DataFrame(platform_metrics)

    def _calculate_time_metrics(self):
        """Calculate time-based performance metrics."""

        # Monthly trends
        monthly_data = self.events_df.groupby([
            self.events_df['event_timestamp'].dt.to_period('M'), 'event_type'
        ])['user_id'].nunique().reset_index()

        monthly_data['month'] = monthly_data['event_timestamp'].astype(str)

        return monthly_data

    def create_funnel_chart(self, save_path=None):
        """
        Create main funnel conversion chart.

        I designed this chart to show the classic funnel visualization
        that clearly demonstrates user drop-off at each stage.
        """

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

        # Funnel bar chart
        bars = ax1.barh(range(len(self.funnel_data)), self.funnel_data['users_at_step'], 
                       color=plt.cm.Blues(np.linspace(0.9, 0.4, len(self.funnel_data))))

        ax1.set_yticks(range(len(self.funnel_data)))
        ax1.set_yticklabels(self.funnel_data['event_label'])
        ax1.set_xlabel('Number of Users')
        ax1.set_title('User Onboarding Funnel - Absolute Numbers', fontsize=14, fontweight='bold')
        ax1.grid(axis='x', alpha=0.3)

        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax1.text(width + width*0.01, bar.get_y() + bar.get_height()/2, 
                    f'{int(width):,}', ha='left', va='center', fontweight='bold')

        # Conversion rate chart
        ax2.plot(range(len(self.funnel_data)), self.funnel_data['overall_conversion_rate'], 
                marker='o', linewidth=3, markersize=8, color='#2E86AB')
        ax2.fill_between(range(len(self.funnel_data)), self.funnel_data['overall_conversion_rate'], 
                        alpha=0.3, color='#2E86AB')

        ax2.set_xticks(range(len(self.funnel_data)))
        ax2.set_xticklabels(self.funnel_data['event_label'], rotation=45, ha='right')
        ax2.set_ylabel('Conversion Rate (%)')
        ax2.set_title('Cumulative Conversion Rates', fontsize=14, fontweight='bold')
        ax2.grid(alpha=0.3)

        # Add percentage labels
        for i, rate in enumerate(self.funnel_data['overall_conversion_rate']):
            ax2.annotate(f'{rate:.1f}%', 
                        (i, rate), 
                        textcoords="offset points", 
                        xytext=(0,10), 
                        ha='center', fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Saved funnel chart to {save_path}")

        plt.show()

        return fig

    def create_platform_comparison(self, save_path=None):
        """
        Create platform performance comparison charts.

        This visualization helps identify which platforms perform best
        for user acquisition and conversion.
        """

        fig, axes = plt.subplots(2, 2, figsize=(15, 12))

        # Visitors by platform
        axes[0,0].bar(self.platform_data['platform'], self.platform_data['visitors'], 
                     color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        axes[0,0].set_title('Visitors by Platform', fontweight='bold')
        axes[0,0].set_ylabel('Number of Visitors')
        axes[0,0].tick_params(axis='x', rotation=45)

        # Add value labels
        for i, v in enumerate(self.platform_data['visitors']):
            axes[0,0].text(i, v + v*0.02, f'{v:,}', ha='center', fontweight='bold')

        # Conversion rates by platform  
        axes[0,1].bar(self.platform_data['platform'], self.platform_data['conversion_rate'],
                     color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        axes[0,1].set_title('Conversion Rate by Platform', fontweight='bold')
        axes[0,1].set_ylabel('Conversion Rate (%)')
        axes[0,1].tick_params(axis='x', rotation=45)

        # Add percentage labels
        for i, v in enumerate(self.platform_data['conversion_rate']):
            axes[0,1].text(i, v + v*0.02, f'{v:.1f}%', ha='center', fontweight='bold')

        # Platform funnel comparison
        platform_funnel_data = []
        for platform in self.platform_data['platform'].unique():
            platform_events = self.events_df[self.events_df['platform'] == platform]

            for event_type in ['landing_page_view', 'signup_page_view', 'email_verification', 'purchase_completed']:
                count = platform_events[platform_events['event_type'] == event_type]['user_id'].nunique()
                platform_funnel_data.append({
                    'platform': platform,
                    'event_type': event_type.replace('_', ' ').title(),
                    'users': count
                })

        platform_funnel_df = pd.DataFrame(platform_funnel_data)
        pivot_data = platform_funnel_df.pivot(index='event_type', columns='platform', values='users')

        pivot_data.plot(kind='bar', ax=axes[1,0], width=0.8)
        axes[1,0].set_title('User Progression by Platform', fontweight='bold')
        axes[1,0].set_ylabel('Number of Users')
        axes[1,0].tick_params(axis='x', rotation=45)
        axes[1,0].legend(title='Platform')

        # Platform conversion funnel percentages
        conversion_matrix = pivot_data.div(pivot_data.iloc[0], axis=1) * 100
        conversion_matrix.plot(kind='line', ax=axes[1,1], marker='o', linewidth=2)
        axes[1,1].set_title('Conversion Rate Progression by Platform', fontweight='bold')
        axes[1,1].set_ylabel('Conversion Rate (%)')
        axes[1,1].tick_params(axis='x', rotation=45)
        axes[1,1].legend(title='Platform')
        axes[1,1].grid(alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Saved platform comparison to {save_path}")

        plt.show()

        return fig

    def create_cohort_heatmap(self, save_path=None):
        """
        Create cohort retention heatmap.

        This advanced visualization shows user retention patterns over time,
        which is crucial for understanding long-term user engagement.
        """

        # Prepare cohort data
        def get_period(df):
            return df['event_timestamp'].dt.to_period('W').dt.start_time

        # Get user's first session (cohort group)
        df_cohort = self.events_df.groupby('user_id')['event_timestamp'].min().reset_index()
        df_cohort.columns = ['user_id', 'cohort_group']
        df_cohort['cohort_group'] = df_cohort['cohort_group'].dt.to_period('W').dt.start_time

        # Get user activity periods
        df_user_activity = self.events_df.groupby('user_id')['event_timestamp'].apply(get_period).reset_index()
        df_user_activity = df_user_activity.drop_duplicates()
        df_user_activity.columns = ['user_id', 'period']

        # Merge cohort and activity data
        df_cohort_table = df_cohort.merge(df_user_activity, on='user_id')
        df_cohort_table['period_number'] = (
            df_cohort_table['period'] - df_cohort_table['cohort_group']
        ).dt.days / 7

        # Create cohort table
        cohort_table = df_cohort_table.groupby(['cohort_group', 'period_number'])['user_id'].nunique().reset_index()
        cohort_sizes = df_cohort.groupby('cohort_group')['user_id'].nunique()

        cohort_table = cohort_table.merge(cohort_sizes.reset_index().rename(columns={'user_id': 'cohort_size'}), 
                                         on='cohort_group')
        cohort_table['retention_rate'] = cohort_table['user_id'] / cohort_table['cohort_size']

        # Pivot for heatmap
        retention_table = cohort_table.pivot(index='cohort_group', 
                                           columns='period_number', 
                                           values='retention_rate')

        # Create heatmap
        fig, ax = plt.subplots(figsize=(15, 8))

        sns.heatmap(retention_table.iloc[:, :13],  # Show first 13 weeks
                   annot=True, 
                   fmt='.2%',
                   cmap='YlOrRd',
                   ax=ax,
                   cbar_kws={'label': 'Retention Rate'})

        ax.set_title('Weekly Cohort Retention Analysis', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Week Number')
        ax.set_ylabel('Cohort (Registration Week)')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Saved cohort heatmap to {save_path}")

        plt.show()

        return fig

    def create_time_trends(self, save_path=None):
        """
        Create time-based trend analysis.

        I built this to show how funnel performance changes over time,
        which is essential for identifying seasonal patterns and growth trends.
        """

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Monthly visitor trends
        monthly_visitors = self.time_data[self.time_data['event_type'] == 'landing_page_view']
        axes[0,0].plot(monthly_visitors['month'], monthly_visitors['user_id'], 
                      marker='o', linewidth=3, markersize=8, color='#2E86AB')
        axes[0,0].set_title('Monthly Visitor Trends', fontweight='bold')
        axes[0,0].set_ylabel('Unique Visitors')
        axes[0,0].tick_params(axis='x', rotation=45)
        axes[0,0].grid(alpha=0.3)

        # Monthly conversion trends
        monthly_purchases = self.time_data[self.time_data['event_type'] == 'purchase_completed']
        axes[0,1].plot(monthly_purchases['month'], monthly_purchases['user_id'], 
                      marker='o', linewidth=3, markersize=8, color='#F39C12')
        axes[0,1].set_title('Monthly Conversion Trends', fontweight='bold')
        axes[0,1].set_ylabel('Conversions')
        axes[0,1].tick_params(axis='x', rotation=45)
        axes[0,1].grid(alpha=0.3)

        # Day of week analysis
        dow_data = self.events_df.groupby([
            self.events_df['event_timestamp'].dt.day_name(), 'event_type'
        ])['user_id'].nunique().reset_index()

        dow_visitors = dow_data[dow_data['event_type'] == 'landing_page_view']
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_visitors = dow_visitors.set_index('event_timestamp').reindex(day_order).reset_index()

        axes[1,0].bar(dow_visitors['event_timestamp'], dow_visitors['user_id'], 
                     color='#E74C3C', alpha=0.7)
        axes[1,0].set_title('Visitors by Day of Week', fontweight='bold')
        axes[1,0].set_ylabel('Visitors')
        axes[1,0].tick_params(axis='x', rotation=45)

        # Hourly activity patterns
        hourly_data = self.events_df.groupby(
            self.events_df['event_timestamp'].dt.hour
        )['user_id'].nunique().reset_index()

        axes[1,1].plot(hourly_data['event_timestamp'], hourly_data['user_id'], 
                      marker='o', linewidth=2, color='#9B59B6')
        axes[1,1].set_title('Hourly Activity Patterns', fontweight='bold')
        axes[1,1].set_xlabel('Hour of Day')
        axes[1,1].set_ylabel('Active Users')
        axes[1,1].grid(alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Saved time trends to {save_path}")

        plt.show()

        return fig

    def create_campaign_performance(self, save_path=None):
        """
        Create campaign performance visualization.

        This chart shows ROI and performance metrics for different marketing campaigns.
        """

        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        # Campaign ROI
        axes[0,0].barh(self.campaign_df['campaign_name'], self.campaign_df['campaign_roi'],
                      color=['red' if x < 0 else 'green' for x in self.campaign_df['campaign_roi']])
        axes[0,0].set_title('Campaign ROI Performance', fontweight='bold')
        axes[0,0].set_xlabel('ROI (%)')
        axes[0,0].axvline(x=0, color='black', linestyle='--', alpha=0.7)

        # Budget vs Acquisitions
        scatter = axes[0,1].scatter(self.campaign_df['budget'], self.campaign_df['users_acquired'],
                                   s=self.campaign_df['conversions']*10, alpha=0.7, c=self.campaign_df['conversion_rate_percent'],
                                   cmap='viridis')
        axes[0,1].set_title('Budget vs User Acquisition', fontweight='bold')
        axes[0,1].set_xlabel('Campaign Budget ($)')
        axes[0,1].set_ylabel('Users Acquired')
        plt.colorbar(scatter, ax=axes[0,1], label='Conversion Rate (%)')

        # Channel Performance
        channel_data = self.campaign_df.groupby('channel').agg({
            'users_acquired': 'sum',
            'conversions': 'sum',
            'budget': 'sum'
        }).reset_index()
        channel_data['channel_conversion_rate'] = (channel_data['conversions'] / channel_data['users_acquired']) * 100

        axes[1,0].bar(channel_data['channel'], channel_data['channel_conversion_rate'],
                     color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        axes[1,0].set_title('Conversion Rate by Channel', fontweight='bold')
        axes[1,0].set_ylabel('Conversion Rate (%)')
        axes[1,0].tick_params(axis='x', rotation=45)

        # Cost metrics
        x = np.arange(len(self.campaign_df))
        width = 0.35

        axes[1,1].bar(x - width/2, self.campaign_df['cost_per_acquisition'], width, 
                     label='Cost per Acquisition', alpha=0.8)
        axes[1,1].bar(x + width/2, self.campaign_df['cost_per_conversion'], width, 
                     label='Cost per Conversion', alpha=0.8)

        axes[1,1].set_title('Campaign Cost Metrics', fontweight='bold')
        axes[1,1].set_ylabel('Cost ($)')
        axes[1,1].set_xticks(x)
        axes[1,1].set_xticklabels(self.campaign_df['campaign_name'], rotation=45, ha='right')
        axes[1,1].legend()

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"💾 Saved campaign performance to {save_path}")

        plt.show()

        return fig

    def generate_all_visualizations(self, output_dir):
        """
        Generate all visualizations and save to specified directory.

        This is the main method I use to create all charts for my portfolio presentation.
        """

        print("🎨 Generating comprehensive visualization suite...")

        # Create all visualizations
        self.create_funnel_chart(f"{output_dir}/funnel_analysis.png")
        self.create_platform_comparison(f"{output_dir}/platform_comparison.png") 
        self.create_cohort_heatmap(f"{output_dir}/cohort_retention_heatmap.png")
        self.create_time_trends(f"{output_dir}/time_trends_analysis.png")
        self.create_campaign_performance(f"{output_dir}/campaign_performance.png")

        print("✅ All visualizations generated successfully!")

        return {
            'funnel_chart': f"{output_dir}/funnel_analysis.png",
            'platform_comparison': f"{output_dir}/platform_comparison.png",
            'cohort_heatmap': f"{output_dir}/cohort_retention_heatmap.png", 
            'time_trends': f"{output_dir}/time_trends_analysis.png",
            'campaign_performance': f"{output_dir}/campaign_performance.png"
        }

def main():
    """
    Main visualization generation pipeline.

    I created this to demonstrate all visualization capabilities
    for potential employers and clients.
    """

    # Load processed data
    events_df = pd.read_csv('../data/user_events.csv')
    demographics_df = pd.read_csv('../data/user_demographics.csv')
    campaign_df = pd.read_csv('../data/campaign_data.csv')

    # Initialize visualizer
    visualizer = FunnelVisualizer(events_df, demographics_df, campaign_df)

    # Generate all visualizations
    visualizer.generate_all_visualizations('../visualizations')

    print("🎉 Visualization pipeline completed successfully!")

if __name__ == "__main__":
    main()
