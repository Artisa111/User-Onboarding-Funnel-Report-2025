-- User Onboarding Funnel Analysis
-- Author: Data Analyst Portfolio Project 2024-2025
-- Purpose: Comprehensive funnel analysis for e-commerce user onboarding

-- ==============================================
-- FUNNEL ANALYSIS - Core Metrics
-- ==============================================

-- 1. Overall Funnel Performance
WITH funnel_steps AS (
  SELECT 
    event_type,
    CASE event_type
      WHEN 'landing_page_view' THEN 1
      WHEN 'signup_page_view' THEN 2
      WHEN 'email_verification' THEN 3
      WHEN 'profile_setup' THEN 4
      WHEN 'first_product_view' THEN 5
      WHEN 'add_to_cart' THEN 6
      WHEN 'checkout_start' THEN 7
      WHEN 'payment_info_entered' THEN 8
      WHEN 'purchase_completed' THEN 9
      WHEN 'app_download' THEN 10
      WHEN 'first_login_app' THEN 11
    END as step_order,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(*) as total_events
  FROM user_events 
  WHERE event_type IN (
    'landing_page_view', 'signup_page_view', 'email_verification',
    'profile_setup', 'first_product_view', 'add_to_cart', 
    'checkout_start', 'payment_info_entered', 'purchase_completed',
    'app_download', 'first_login_app'
  )
  GROUP BY event_type, step_order
),

funnel_with_conversion AS (
  SELECT 
    step_order,
    event_type,
    unique_users,
    total_events,
    LAG(unique_users) OVER (ORDER BY step_order) as previous_step_users,
    ROUND(
      (unique_users * 100.0 / LAG(unique_users) OVER (ORDER BY step_order)), 2
    ) as step_conversion_rate,
    ROUND(
      (unique_users * 100.0 / FIRST_VALUE(unique_users) OVER (ORDER BY step_order)), 2
    ) as overall_conversion_rate
  FROM funnel_steps
)

SELECT 
  step_order,
  event_type as funnel_step,
  unique_users,
  total_events,
  COALESCE(step_conversion_rate, 100.0) as step_conversion_rate_percent,
  overall_conversion_rate as cumulative_conversion_rate_percent,
  COALESCE(previous_step_users - unique_users, 0) as users_dropped_off
FROM funnel_with_conversion
ORDER BY step_order;

-- ==============================================
-- PLATFORM PERFORMANCE ANALYSIS
-- ==============================================

-- 2. Funnel Performance by Platform
SELECT 
  platform,
  COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END) as landing_users,
  COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END) as signup_users,
  COUNT(DISTINCT CASE WHEN event_type = 'email_verification' THEN user_id END) as verified_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) as converted_users,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END), 0), 2
  ) as signup_conversion_rate,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END), 0), 2
  ) as overall_conversion_rate

FROM user_events
GROUP BY platform
ORDER BY converted_users DESC;

-- ==============================================
-- TIME-BASED ANALYSIS
-- ==============================================

-- 3. Monthly Funnel Performance Trends
SELECT 
  DATE_TRUNC('month', event_timestamp) as month,
  COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END) as visitors,
  COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END) as signups,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) as purchases,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END), 0), 2
  ) as signup_rate,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END), 0), 2
  ) as conversion_rate

FROM user_events
WHERE event_timestamp >= '2024-06-01'
GROUP BY DATE_TRUNC('month', event_timestamp)
ORDER BY month;

-- ==============================================
-- GEOGRAPHIC ANALYSIS
-- ==============================================

-- 4. Country Performance Analysis
SELECT 
  country,
  COUNT(DISTINCT user_id) as total_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) as converters,
  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 100.0 /
    COUNT(DISTINCT user_id), 2
  ) as conversion_rate,
  AVG(
    CASE WHEN event_type = 'purchase_completed' 
    THEN EXTRACT(EPOCH FROM (event_timestamp - 
      MIN(event_timestamp) OVER (PARTITION BY user_id))) / 3600 
    END
  ) as avg_time_to_purchase_hours
FROM user_events
GROUP BY country
HAVING COUNT(DISTINCT user_id) >= 50  -- Minimum sample size
ORDER BY conversion_rate DESC;
