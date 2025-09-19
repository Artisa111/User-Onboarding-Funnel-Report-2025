-- Conversion Rate Analysis
-- Author: Data Analyst Portfolio Project 2024-2025
-- Purpose: Detailed conversion rate calculations and optimization insights

-- ==============================================
-- CONVERSION RATE CALCULATIONS
-- ==============================================

-- 1. Step-by-Step Conversion Rates
WITH user_journey AS (
  SELECT 
    user_id,
    MAX(CASE WHEN event_type = 'landing_page_view' THEN 1 ELSE 0 END) as reached_landing,
    MAX(CASE WHEN event_type = 'signup_page_view' THEN 1 ELSE 0 END) as reached_signup,
    MAX(CASE WHEN event_type = 'email_verification' THEN 1 ELSE 0 END) as reached_verification,
    MAX(CASE WHEN event_type = 'profile_setup' THEN 1 ELSE 0 END) as reached_profile,
    MAX(CASE WHEN event_type = 'first_product_view' THEN 1 ELSE 0 END) as reached_product_view,
    MAX(CASE WHEN event_type = 'add_to_cart' THEN 1 ELSE 0 END) as reached_cart,
    MAX(CASE WHEN event_type = 'checkout_start' THEN 1 ELSE 0 END) as reached_checkout,
    MAX(CASE WHEN event_type = 'payment_info_entered' THEN 1 ELSE 0 END) as reached_payment,
    MAX(CASE WHEN event_type = 'purchase_completed' THEN 1 ELSE 0 END) as reached_purchase,
    MAX(CASE WHEN event_type = 'app_download' THEN 1 ELSE 0 END) as reached_app_download,
    MAX(CASE WHEN event_type = 'first_login_app' THEN 1 ELSE 0 END) as reached_app_login
  FROM user_events
  GROUP BY user_id
)

SELECT 
  'Landing → Signup' as conversion_step,
  SUM(reached_landing) as numerator_users,
  SUM(reached_signup) as denominator_users,
  ROUND(SUM(reached_signup) * 100.0 / SUM(reached_landing), 2) as conversion_rate_percent
FROM user_journey

UNION ALL

SELECT 
  'Signup → Verification',
  SUM(reached_signup),
  SUM(reached_verification),
  ROUND(SUM(reached_verification) * 100.0 / SUM(reached_signup), 2)
FROM user_journey

UNION ALL

SELECT 
  'Verification → Profile Setup',
  SUM(reached_verification),
  SUM(reached_profile),
  ROUND(SUM(reached_profile) * 100.0 / SUM(reached_verification), 2)
FROM user_journey

UNION ALL

SELECT 
  'Profile → Product View',
  SUM(reached_profile),
  SUM(reached_product_view),
  ROUND(SUM(reached_product_view) * 100.0 / SUM(reached_profile), 2)
FROM user_journey

UNION ALL

SELECT 
  'Product View → Add to Cart',
  SUM(reached_product_view),
  SUM(reached_cart),
  ROUND(SUM(reached_cart) * 100.0 / SUM(reached_product_view), 2)
FROM user_journey

UNION ALL

SELECT 
  'Cart → Checkout',
  SUM(reached_cart),
  SUM(reached_checkout),
  ROUND(SUM(reached_checkout) * 100.0 / SUM(reached_cart), 2)
FROM user_journey

UNION ALL

SELECT 
  'Checkout → Payment',
  SUM(reached_checkout),
  SUM(reached_payment),
  ROUND(SUM(reached_payment) * 100.0 / SUM(reached_checkout), 2)
FROM user_journey

UNION ALL

SELECT 
  'Payment → Purchase',
  SUM(reached_payment),
  SUM(reached_purchase),
  ROUND(SUM(reached_purchase) * 100.0 / SUM(reached_payment), 2)
FROM user_journey;

-- ==============================================
-- TRAFFIC SOURCE CONVERSION ANALYSIS
-- ==============================================

-- 2. Conversion Rates by Traffic Source
SELECT 
  traffic_source,
  COUNT(DISTINCT user_id) as total_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) as converted_users,
  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 100.0 /
    COUNT(DISTINCT user_id), 2
  ) as conversion_rate_percent,

  -- Average time to conversion
  ROUND(
    AVG(
      CASE WHEN event_type = 'purchase_completed' 
      THEN EXTRACT(EPOCH FROM (event_timestamp - 
        MIN(event_timestamp) OVER (PARTITION BY user_id))) / 3600 
      END
    ), 2
  ) as avg_time_to_conversion_hours,

  -- Revenue potential (assuming $50 average order value)
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 50 as estimated_revenue

FROM user_events
GROUP BY traffic_source
ORDER BY conversion_rate_percent DESC;

-- ==============================================
-- DEVICE/PLATFORM CONVERSION DEEP DIVE  
-- ==============================================

-- 3. Platform Conversion Performance with Funnel Breakdown
SELECT 
  platform,

  -- Funnel step counts
  COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END) as visitors,
  COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END) as signup_viewers,
  COUNT(DISTINCT CASE WHEN event_type = 'email_verification' THEN user_id END) as verified_users,
  COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) as cart_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) as purchasers,

  -- Conversion rates
  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END), 0), 2
  ) as landing_to_signup_rate,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'email_verification' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'signup_page_view' THEN user_id END), 0), 2
  ) as signup_to_verification_rate,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'email_verification' THEN user_id END), 0), 2
  ) as verification_to_cart_rate,

  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 100.0 /
    NULLIF(COUNT(DISTINCT CASE WHEN event_type = 'landing_page_view' THEN user_id END), 0), 2
  ) as overall_conversion_rate

FROM user_events
GROUP BY platform
ORDER BY overall_conversion_rate DESC;

-- ==============================================
-- TIME-BASED CONVERSION PATTERNS
-- ==============================================

-- 4. Day-of-Week Conversion Analysis
SELECT 
  EXTRACT(DOW FROM event_timestamp) as day_of_week,
  CASE EXTRACT(DOW FROM event_timestamp)
    WHEN 0 THEN 'Sunday'
    WHEN 1 THEN 'Monday'
    WHEN 2 THEN 'Tuesday'
    WHEN 3 THEN 'Wednesday'
    WHEN 4 THEN 'Thursday'
    WHEN 5 THEN 'Friday'
    WHEN 6 THEN 'Saturday'
  END as day_name,

  COUNT(DISTINCT user_id) as total_users,
  COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) as conversions,
  ROUND(
    COUNT(DISTINCT CASE WHEN event_type = 'purchase_completed' THEN user_id END) * 100.0 /
    COUNT(DISTINCT user_id), 2
  ) as conversion_rate_percent

FROM user_events
GROUP BY EXTRACT(DOW FROM event_timestamp)
ORDER BY day_of_week;

-- ==============================================
-- COHORT CONVERSION ANALYSIS
-- ==============================================

-- 5. Weekly Registration Cohorts
WITH user_cohorts AS (
  SELECT 
    user_id,
    DATE_TRUNC('week', MIN(event_timestamp)) as cohort_week,
    MAX(CASE WHEN event_type = 'purchase_completed' THEN 1 ELSE 0 END) as converted
  FROM user_events
  GROUP BY user_id
)

SELECT 
  cohort_week,
  COUNT(*) as cohort_size,
  SUM(converted) as conversions,
  ROUND(SUM(converted) * 100.0 / COUNT(*), 2) as cohort_conversion_rate
FROM user_cohorts
GROUP BY cohort_week
ORDER BY cohort_week;
