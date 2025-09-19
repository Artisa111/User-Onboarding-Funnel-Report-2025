-- Cohort Analysis for User Retention and Behavior
-- Author: Data Analyst Portfolio Project 2024-2025
-- Purpose: Advanced cohort analysis to understand user retention patterns

-- ==============================================
-- USER COHORT DEFINITION AND RETENTION ANALYSIS
-- ==============================================

-- 1. Weekly Registration Cohorts with Retention Rates
WITH user_registration AS (
  SELECT 
    user_id,
    DATE_TRUNC('week', MIN(event_timestamp)) as cohort_week,
    MIN(event_timestamp) as first_session
  FROM user_events
  GROUP BY user_id
),

user_activity AS (
  SELECT 
    ur.user_id,
    ur.cohort_week,
    ur.first_session,
    ue.event_timestamp,
    DATE_TRUNC('week', ue.event_timestamp) as activity_week,
    EXTRACT(WEEK FROM ue.event_timestamp) - EXTRACT(WEEK FROM ur.first_session) as weeks_since_registration
  FROM user_registration ur
  JOIN user_events ue ON ur.user_id = ue.user_id
),

cohort_sizes AS (
  SELECT 
    cohort_week,
    COUNT(DISTINCT user_id) as cohort_size
  FROM user_registration
  GROUP BY cohort_week
),

retention_table AS (
  SELECT 
    ua.cohort_week,
    ua.weeks_since_registration,
    COUNT(DISTINCT ua.user_id) as active_users
  FROM user_activity ua
  WHERE ua.weeks_since_registration BETWEEN 0 AND 12  -- 12 weeks retention window
  GROUP BY ua.cohort_week, ua.weeks_since_registration
)

SELECT 
  rt.cohort_week,
  cs.cohort_size,
  rt.weeks_since_registration as week_number,
  rt.active_users,
  ROUND(rt.active_users * 100.0 / cs.cohort_size, 2) as retention_rate_percent
FROM retention_table rt
JOIN cohort_sizes cs ON rt.cohort_week = cs.cohort_week
ORDER BY rt.cohort_week, rt.weeks_since_registration;

-- ==============================================
-- BEHAVIORAL COHORTS ANALYSIS
-- ==============================================

-- 2. Cohorts Based on First Action Platform
WITH platform_cohorts AS (
  SELECT 
    user_id,
    platform as first_platform,
    MIN(event_timestamp) as registration_date
  FROM user_events
  WHERE event_type = 'landing_page_view'
  GROUP BY user_id, platform
),

cohort_behavior AS (
  SELECT 
    pc.first_platform as cohort_type,
    pc.user_id,
    COUNT(DISTINCT ue.event_type) as unique_actions_taken,
    MAX(CASE WHEN ue.event_type = 'purchase_completed' THEN 1 ELSE 0 END) as made_purchase,
    MAX(CASE WHEN ue.event_type = 'app_download' THEN 1 ELSE 0 END) as downloaded_app,
    COUNT(DISTINCT DATE(ue.event_timestamp)) as active_days,
    EXTRACT(EPOCH FROM (MAX(ue.event_timestamp) - MIN(ue.event_timestamp))) / 86400 as lifetime_days
  FROM platform_cohorts pc
  JOIN user_events ue ON pc.user_id = ue.user_id
  GROUP BY pc.first_platform, pc.user_id
)

SELECT 
  cohort_type,
  COUNT(*) as cohort_size,
  ROUND(AVG(unique_actions_taken), 2) as avg_actions_per_user,
  ROUND(SUM(made_purchase) * 100.0 / COUNT(*), 2) as conversion_rate_percent,
  ROUND(SUM(downloaded_app) * 100.0 / COUNT(*), 2) as app_adoption_rate_percent,
  ROUND(AVG(active_days), 2) as avg_active_days,
  ROUND(AVG(lifetime_days), 2) as avg_lifetime_days
FROM cohort_behavior
GROUP BY cohort_type
ORDER BY conversion_rate_percent DESC;

-- ==============================================
-- REVENUE COHORTS ANALYSIS
-- ==============================================

-- 3. Revenue Analysis by Registration Month
WITH monthly_cohorts AS (
  SELECT 
    user_id,
    DATE_TRUNC('month', MIN(event_timestamp)) as registration_month
  FROM user_events
  GROUP BY user_id
),

cohort_revenue AS (
  SELECT 
    mc.registration_month,
    mc.user_id,
    COUNT(CASE WHEN ue.event_type = 'purchase_completed' THEN 1 END) as purchases_made,
    -- Assume $50 average order value
    COUNT(CASE WHEN ue.event_type = 'purchase_completed' THEN 1 END) * 50 as estimated_revenue
  FROM monthly_cohorts mc
  JOIN user_events ue ON mc.user_id = ue.user_id
  GROUP BY mc.registration_month, mc.user_id
)

SELECT 
  registration_month,
  COUNT(*) as cohort_size,
  SUM(purchases_made) as total_purchases,
  SUM(estimated_revenue) as total_estimated_revenue,
  ROUND(AVG(purchases_made), 2) as avg_purchases_per_user,
  ROUND(AVG(estimated_revenue), 2) as avg_revenue_per_user,
  ROUND(SUM(estimated_revenue) / COUNT(*), 2) as revenue_per_cohort_user
FROM cohort_revenue
GROUP BY registration_month
ORDER BY registration_month;

-- ==============================================
-- ENGAGEMENT COHORTS
-- ==============================================

-- 4. High-Value User Cohorts (Users with 5+ Events)
WITH user_engagement AS (
  SELECT 
    user_id,
    COUNT(*) as total_events,
    COUNT(DISTINCT event_type) as unique_event_types,
    COUNT(DISTINCT DATE(event_timestamp)) as active_days,
    MIN(event_timestamp) as first_seen,
    MAX(event_timestamp) as last_seen,
    CASE 
      WHEN COUNT(*) >= 10 THEN 'High Engagement'
      WHEN COUNT(*) >= 5 THEN 'Medium Engagement'  
      ELSE 'Low Engagement'
    END as engagement_tier
  FROM user_events
  GROUP BY user_id
),

engagement_outcomes AS (
  SELECT 
    ue_eng.*,
    CASE WHEN purchase_events.user_id IS NOT NULL THEN 1 ELSE 0 END as converted_to_purchase,
    CASE WHEN app_events.user_id IS NOT NULL THEN 1 ELSE 0 END as downloaded_app
  FROM user_engagement ue_eng
  LEFT JOIN (
    SELECT DISTINCT user_id 
    FROM user_events 
    WHERE event_type = 'purchase_completed'
  ) purchase_events ON ue_eng.user_id = purchase_events.user_id
  LEFT JOIN (
    SELECT DISTINCT user_id 
    FROM user_events 
    WHERE event_type = 'app_download'
  ) app_events ON ue_eng.user_id = app_events.user_id
)

SELECT 
  engagement_tier,
  COUNT(*) as users_in_tier,
  ROUND(AVG(total_events), 2) as avg_events_per_user,
  ROUND(AVG(unique_event_types), 2) as avg_unique_actions,
  ROUND(AVG(active_days), 2) as avg_active_days,
  ROUND(SUM(converted_to_purchase) * 100.0 / COUNT(*), 2) as conversion_rate_percent,
  ROUND(SUM(downloaded_app) * 100.0 / COUNT(*), 2) as app_adoption_rate_percent
FROM engagement_outcomes
GROUP BY engagement_tier
ORDER BY 
  CASE engagement_tier 
    WHEN 'High Engagement' THEN 1
    WHEN 'Medium Engagement' THEN 2
    WHEN 'Low Engagement' THEN 3
  END;

-- ==============================================
-- GEOGRAPHIC COHORTS
-- ==============================================

-- 5. Country-Based User Performance
WITH country_cohorts AS (
  SELECT 
    country,
    user_id,
    MIN(event_timestamp) as registration_date,
    COUNT(*) as total_events,
    MAX(CASE WHEN event_type = 'purchase_completed' THEN 1 ELSE 0 END) as purchased
  FROM user_events
  GROUP BY country, user_id
)

SELECT 
  country,
  COUNT(*) as total_users,
  ROUND(AVG(total_events), 2) as avg_events_per_user,
  SUM(purchased) as converted_users,
  ROUND(SUM(purchased) * 100.0 / COUNT(*), 2) as conversion_rate_percent,
  -- Rank countries by performance
  RANK() OVER (ORDER BY SUM(purchased) * 100.0 / COUNT(*) DESC) as conversion_rank
FROM country_cohorts
GROUP BY country
HAVING COUNT(*) >= 50  -- Minimum sample size
ORDER BY conversion_rate_percent DESC;
