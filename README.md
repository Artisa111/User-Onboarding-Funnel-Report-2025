# User Onboarding Funnel Analysis 2024-2025
## Data Analytics Portfolio Project
<!-- === START: V5 MULTI-LINGUAL NAV CAPSULE BUTTONS (WITH LOGOS) === -->
<p align="center">
  <a href="#-project-overview"><img src="https://img.shields.io/badge/Overview-ANALYSIS-0C4D8A?style=for-the-badge&labelColor=0C4D8A&logo=readme&logoColor=white" alt="Overview"></a>
  <a href="#-business-problem"><img src="https://img.shields.io/badge/Problem-FOCUS-F0706A?style=for-the-badge&labelColor=0C4D8A&logo=target&logoColor=white" alt="Business Problem"></a>
  <a href="#-my-analysis-approach"><img src="https://img.shields.io/badge/Approach-METHOD-33A6C5?style=for-the-badge&labelColor=1D669F&logo=googleanalytics&logoColor=white" alt="Analysis Approach"></a>
  <a href="#-key-findings--insights"><img src="https://img.shields.io/badge/Insights-DATA-4EC7BF?style=for-the-badge&labelColor=1D669F&logo=googleanalytics&logoColor=white" alt="Key Findings"></a>
  <a href="#-technical-implementation"><img src="https://img.shields.io/badge/Tech-STACK-1D669F?style=for-the-badge&labelColor=0C4D8A&logo=postgresql&logoColor=white" alt="Technical Implementation"></a>
  <a href="#-how-to-run-this-project"><img src="https://img.shields.io/badge/Run-STEPS-33A6C5?style=for-the-badge&labelColor=1D669F&logo=geeksforgeeks&logoColor=white" alt="Run Project"></a>
  <a href="#-business-recommendations"><img src="https://img.shields.io/badge/Recommendations-ACTION-F0706A?style=for-the-badge&labelColor=0C4D8A&logo=target&logoColor=white" alt="Recommendations"></a>
  <a href="#hebrew-version--גרסה-בעברית"><img src="https://img.shields.io/badge/Hebrew_Version-RTL-6BA892?style=for-the-badge&labelColor=0C4D8A&logo=googletranslate&logoColor=white" alt="Hebrew Version"></a>
</p>

<p align="center">
  <a href="./funnel_analysis.ipynb"><img src="https://img.shields.io/badge/Jupyter-NOTEBOOK-F0706A?style=for-the-badge&labelColor=424242&logo=jupyter&logoColor=white" alt="Notebook"></a>
  <a href="./visualization.py"><img src="https://img.shields.io/badge/Visualization-SCRIPT-33A6C5?style=for-the-badge&labelColor=1D669F&logo=python&logoColor=white" alt="Visualization Script"></a>
  <a href="./sql/"><img src="https://img.shields.io/badge/SQL-QUERIES-0C4D8A?style=for-the-badge&labelColor=1D669F&logo=postgresql&logoColor=white" alt="SQL Queries"></a>
  <a href="./data/"><img src="https://img.shields.io/badge/Data-FILES-1D669F?style=for-the-badge&labelColor=424242&logo=databricks&logoColor=white" alt="Data Files"></a>
  <a href="#-sample-insights-dashboard"><img src="https://img.shields.io/badge/Dashboard-INSIGHTS-4EC7BF?style=for-the-badge&labelColor=1D669F&logo=googleanalytics&logoColor=white" alt="Sample Insights Dashboard"></a>
</p>


### 📊 Project Overview

I developed this comprehensive user onboarding funnel analysis as a portfolio project to showcase my data analytics skills. This project examines user behavior patterns on an e-commerce/SaaS platform, identifying optimization opportunities and providing actionable business recommendations.

### 🎯 Business Problem

As a data analyst, I identified the critical need to understand user drop-off patterns in the onboarding funnel. The main challenges I addressed were:

- **High User Abandonment**: Understanding where users exit the funnel
- **Platform Performance Variations**: Comparing conversion rates across web, mobile, and app platforms  
- **Campaign ROI Optimization**: Measuring marketing campaign effectiveness
- **Geographic Performance Differences**: Analyzing conversion patterns by country
- **Cohort Retention Analysis**: Understanding long-term user engagement patterns

### 🔍 My Analysis Approach

I used a multi-faceted analytical approach combining:

1. **SQL Analysis**: Complex queries for funnel metrics and cohort analysis
2. **Python Data Processing**: Advanced data cleaning and feature engineering
3. **Statistical Analysis**: Conversion rate calculations and trend analysis  
4. **Data Visualization**: Professional charts and dashboards
5. **Business Intelligence**: Actionable recommendations based on findings

### 📈 Key Findings & Insights

Through my analysis, I discovered several critical insights:

#### Funnel Performance Metrics:
- **Overall Conversion Rate**: 3.08% (landing page to purchase)
- **Biggest Drop-off Point**: Signup to email verification (55% drop-off)
- **Best Converting Platform**: Web platform (3.3% conversion rate)
- **Highest Volume Month**: November 2024 (Black Friday impact)

#### Platform Analysis:
- **Web Platform**: Highest conversion rate but lower signup rate
- **Mobile Web**: Best for initial engagement, moderate conversion
- **iOS App**: Premium user segment with high lifetime value
- **Android App**: Growing segment with optimization potential

#### Campaign Performance:
- **Best ROI Campaign**: Referral Program (positive ROI)
- **Highest Volume**: Black Friday 2024 campaign  
- **Most Efficient Channel**: Email campaigns (lowest cost per acquisition)
- **Geographic Winners**: US and UK markets show strongest performance

### 🛠️ Technical Implementation

#### Data Pipeline:
```
Raw Data → SQL Analysis → Python Processing → Visualization → Business Insights
```

#### Technologies Used:
- **SQL**: PostgreSQL for complex funnel queries
- **Python**: pandas, NumPy for data manipulation
- **Visualization**: matplotlib, seaborn, Plotly for charts
- **Analytics**: Statistical analysis and cohort studies

#### Key SQL Queries I Developed:
1. **Funnel Analysis**: Step-by-step user progression tracking
2. **Conversion Rates**: Platform and geographic performance metrics
3. **Cohort Analysis**: User retention and engagement patterns
4. **Campaign Attribution**: Marketing ROI calculations

### 📊 Data Sources & Methodology

I generated realistic datasets simulating:
- **User Events**: 20,752 events from 8,000 users over 6 months
- **Demographics**: Age, gender, income, device preferences  
- **Campaign Data**: 8 marketing campaigns with budget and performance metrics
- **Geographic Data**: 8 countries with varying conversion patterns

### 🎨 Visualizations

#### 1. Main Funnel Chart
![Funnel Analysis](./images/funnel_analysis.png) 
*Figure 1. User drop-off across funnel stages.*

#### 2. Platform Comparison
![Platform Comparison](./images/platform_comparison.png)  
*Figure 2. Conversion performance across Web, Mobile Web, iOS, Android.*

### 💡 Business Recommendations

Based on my analysis, I recommend:

#### Immediate Actions:
1. **Optimize Email Verification Process**: Reduce 55% drop-off rate
2. **Invest in Web Platform**: Capitalize on highest conversion rate
3. **Expand Referral Program**: Only campaign with positive ROI
4. **Focus on US/UK Markets**: Highest performing geographies

#### Long-term Strategy:
1. **Mobile App Development**: Improve iOS/Android conversion rates
2. **Seasonal Campaign Planning**: Leverage November performance patterns
3. **Cohort-based Marketing**: Target high-retention user segments
4. **Geographic Expansion**: Replicate success in similar markets

### 📁 Project Structure

```
user-onboarding-funnel-project/
├── data/
│   ├── user_events.csv          # Raw user interaction data
│   ├── user_demographics.csv    # User profile information
│   └── campaign_data.csv        # Marketing campaign metrics
├── sql/
│   ├── funnel_analysis.sql      # Core funnel queries
│   ├── conversion_rates.sql     # Conversion calculations
│   └── cohort_analysis.sql      # Retention analysis
├── python/
│   ├── data_preprocessing.py    # Data cleaning pipeline
│   ├── visualization.py         # Chart generation
│   └── funnel_analysis.ipynb    # Main analysis notebook
├── visualizations/
│   ├── funnel_analysis.png
│   ├── platform_comparison.png
│   ├── cohort_retention_heatmap.png
│   ├── time_trends_analysis.png
│   ├── campaign_performance.png
└── README.md
```

### 🚀 How to Run This Project

1. **Clone the repository**:
```bash
git clone <repository-url>
cd user-onboarding-funnel-project
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run SQL analysis**:
```sql
-- Execute queries in your preferred SQL environment
-- Start with funnel_analysis.sql for core metrics
```

4. **Execute Python analysis**:
```bash
python python/data_preprocessing.py
python python/visualization.py
jupyter notebook python/funnel_analysis.ipynb
```

### 📊 Sample Insights Dashboard

The analysis reveals that I successfully identified:
- **3.08% overall conversion rate** with clear optimization opportunities
- **55% email verification drop-off** as the primary bottleneck
- **Web platform superiority** for conversion optimization
- **Geographic concentration** in English-speaking markets
- **Seasonal patterns** with November peaks

### 🔧 Technical Skills Demonstrated

Through this project, I showcased:
- **Advanced SQL**: Complex window functions, CTEs, cohort analysis
- **Python Proficiency**: Data manipulation, statistical analysis
- **Data Visualization**: Professional charts and storytelling
- **Business Analysis**: Converting data insights into recommendations
- **Project Management**: End-to-end analytics project delivery

###  Contact Information
**Artur** - Data Analyst  

<p align="center">
  <a href="mailto:artursim779@gmail.com"><img src="https://img.shields.io/badge/Email-ARTUR-6BA892?style=for-the-badge&labelColor=424242&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://www.linkedin.com/in/artur-pais-848491352" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-ARTUR__PAIS-1D669F?style=for-the-badge&labelColor=424242&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://github.com/Artisa111" target="_blank"><img src="https://img.shields.io/badge/GitHub-ARTISA111-000000?style=for-the-badge&labelColor=424242&logo=github&logoColor=white" alt="GitHub"></a>
</p>

---

*This project demonstrates my ability to conduct comprehensive funnel analysis, generate actionable business insights, and communicate findings effectively to stakeholders. I'm actively seeking data analyst opportunities where I can apply these skills to drive business growth.*
### 📄 License

This project is created for portfolio demonstration purposes. Feel free to use the methodologies and adapt for your own analysis needs.

---

## Hebrew Version / גרסה בעברית
<div dir="rtl" align="right">

# ניתוח משפך הטמעת משתמשים <span dir="ltr">2024–2025</span>
## פרויקט תיק עבודות בניתוח נתונים

### 📊 סקירת הפרויקט

אני פיתחתי את הניתוח המקיף הזה של משפך ההכשרה של משתמשים כפרויקט תיק עבודות כדי להציג את כישורי האנליזה שלי. הפרויקט בוחן דפוסי התנהגות של משתמשים בפלטפורמת מסחר אלקטרוני/SaaS, מזהה הזדמנויות לאופטימיזציה ומספק המלצות עסקיות מעשיות

### 🎯 הבעיה העסקית

כאנליסט נתונים, זיהיתי את הצורך הקריטי להבין דפוסי נטישה של משתמשים במשפך ההטמעה. האתגרים העיקריים שטיפלתי בהם היו:


- **נטישה גבוהה של משתמשים**: הבנת המקום בו משתמשים יוצאים מהמשפך
- **שונות בביצועי פלטפורמות**: השוואת שיעורי המרה בין אתר, מובייל ואפליקציות
- **אופטימיזציית ROI של קמפיינים**: מדידת יעילות קמפיינים שיווקיים
- **הבדלים גיאוגרפיים בביצועים**: ניתוח דפוסי המרה לפי מדינה
- **ניתוח retention של קוהורט**: הבנת דפוסי מעורבות לטווח ארוך

### 🔍 הגישה האנליטיקית שלי

השתמשתי בגישה אנליטית רב-פנית המשלבת:

1. **ניתוח SQL**: שאילתות מורכבות למדדי משפך וניתוח קוהורט
2. **עיבוד נתונים ב<span dir="ltr">Python</span>**: ניקוי נתונים מתקדם והנדסת תכונות
3. **ניתוח סטטיסטי**: חישוב שיעורי המרה וניתוח טרנדים
4. **הדמיה של נתונים**: תרשימים ומחוונים מקצועיים
5. **מודיעין עסקי**: המלצות מעשיות על בסיס הממצאים

### 📈 ממצאים ותובנות מרכזיות

#### מדדי ביצועי המשפך:
- **שיעור המרה כללי**: <span dir="ltr">3.08%</span> (מעמוד נחיתה לרכישה)
- **נקודת הנטישה הגדולה ביותר**: הרשמה לאימות אימייל (<span dir="ltr">55%</span> נטישה)
- **הפלטפורמה הכי טובה להמרה**: פלטפורמת אינטרנט (<span dir="ltr">3.3%</span> המרה)
- **החודש עם הכי הרבה נפח**: נובמבר <span dir="ltr">2024</span> (השפעת שישי השחור)

#### ניתוח פלטפורמות:
- **פלטפורמת אינטרנט**: שיעור המרה הגבוה ביותר אך שיעור הרשמה נמוך יותר
- **אינטרנט מובייל**: הכי טוב למעורבות ראשונית, המרה בינונית
- **אפליקציית <span dir="ltr">iOS</span>**: סגמנט משתמשים פרימיום עם ערך חיים גבוה
- **אפליקציית <span dir="ltr">Android</span>**: סגמנט צומח עם פוטנציאל אופטימיזציה

#### ביצועי קמפיינים:
- **קמפיין עם <span dir="ltr">ROI</span> הכי טוב**: תוכנית הפניות (<span dir="ltr">ROI</span> חיובי)
- **הנפח הגבוה ביותר**: קמפיין שישי השחור <span dir="ltr">2024</span>
- **הערוץ הכי יעיל**: קמפיינים באימייל (עלות נמוכה ביותר לרכישה)
- **שווקי ביצועים מובילים**: ארצות הברית ובריטניה

### 🛠️ יישום טכני

#### צינור נתונים:
```
נתונים גולמיים → ניתוח SQL → עיבוד Python → הדמיה → תובנות עסקיות
```

#### טכנולוגיות:
- **SQL**: <span dir="ltr">PostgreSQL</span> לשאילתות משפך מורכבות
- **Python**: pandas, NumPy למניפולציה של נתונים
- **הדמיה**: matplotlib, seaborn, Plotly
- **אנליטיקס**: ניתוח סטטיסטי ומחקרי קוהורט

#### שאילתות SQL מרכזיות:
1. **ניתוח משפך**: מעקב התקדמות משתמשים
2. **שיעורי המרה**: פלטפורמה וגיאוגרפיה
3. **ניתוח קוהורט**: דפוסי שמירה
4. **ייחוס קמפיינים**: חישוב ROI שיווקי

### 📊 מקורות נתונים ומתודולוגיה

יצרתי מערכי נתונים ריאליסטיים המדמים:
- **אירועי משתמשים**: <span dir="ltr">20,752</span> אירועים מ-<span dir="ltr">8,000</span> משתמשים על פני <span dir="ltr">6</span> חודשים
- **דמוגרפיה**: גיל, מגדר, הכנסה, העדפות מכשיר
- **נתוני קמפיינים**: <span dir="ltr">8</span> קמפיינים עם תקציב ומדדים
- **נתונים גיאוגרפיים**: <span dir="ltr">8</span> מדינות עם דפוסי המרה משתנים

### 🎨 ויזואליזציה

#### 1. משפך ראשי
![התנהגות משתמשים במשפך](./images/funnel_analysis.png) 
*איור 1. נטישת משתמשים בכל שלבי ההטמעה.*

#### 2. השוואת פלטפורמות
![השוואת ביצועי פלטפורמות](./images/platform_comparison.png)   
*איור 2. שיעורי המרה לפי פלטפורמה (<span dir="ltr">Web</span>, <span dir="ltr">Mobile Web</span>, <span dir="ltr">iOS</span>, <span dir="ltr">Android</span>).*

### 💡 המלצות עסקיות

על בסיס הניתוח שלי, אני ממליץ:

#### פעולות מיידיות:
1. **אופטימיזציה של תהליך אימות אימייל**: הפחתת נטישה של <span dir="ltr">55%</span>
2. **השקעה בפלטפורמת אינטרנט**: מינוף שיעור המרה גבוה
3. **הרחבת תוכנית הפניות**: הקמפיין היחיד עם <span dir="ltr">ROI</span> חיובי
4. **התמקדות בארה"ב/בריטניה**: שווקי ביצועים מובילים

#### אסטרטגיה לטווח ארוך:
1. **פיתוח אפליקציות מובייל**: שיפור המרות <span dir="ltr">iOS</span>/<span dir="ltr">Android</span>
2. **תכנון קמפיינים עונתיים**: מינוף דפוסי נובמבר
3. **שיווק מבוסס קוהורט**: מיקוד בסגמנטים עם שמירה גבוהה
4. **התרחבות גיאוגרפית**: שכפול הצלחה בשווקים דומים

### 📁 מבנה הפרויקט
```
user-onboarding-funnel-project/
├── data/
│   ├── user_events.csv
│   ├── user_demographics.csv
│   └── campaign_data.csv
├── sql/
│   ├── funnel_analysis.sql
│   ├── conversion_rates.sql
│   └── cohort_analysis.sql
├── python/
│   ├── data_preprocessing.py
│   ├── visualization.py
│   └── funnel_analysis.ipynb
├── visualizations/
│   ├── funnel_analysis.png
│   ├── platform_comparison.png
│   ├── cohort_retention_heatmap.png
│   ├── time_trends_analysis.png
│   ├── campaign_performance.png
└── README.md
```

### 🚀 איך להריץ את הפרויקט הזה
1. **שיבוט המאגר**:
```bash
git clone <repository-url>
cd user-onboarding-funnel-project
```
2. **התקנת תלויות**:
```bash
pip install -r requirements.txt
```
3. **הרצת ניתוח SQL**:
```sql
-- הרץ שאילתות בסביבת SQL המועדפת עליך
-- התחל עם funnel_analysis.sql למדדים מרכזיים
```
4. **הרצת ניתוח Python**:
```bash
python python/data_preprocessing.py
python python/visualization.py
jupyter notebook python/funnel_analysis.ipynb
```

### 📊 מחוון תובנות לדוגמה
הניתוח מגלה שזיהיתי בהצלחה:
- **שיעור המרה כללי של <span dir="ltr">3.08%</span>** עם הזדמנויות אופטימיזציה
- **<span dir="ltr">55%</span> נטישה באימות אימייל** כצוואר בקבוק
- **עליונות פלטפורמת אינטרנט** בהמרה
- **ריכוז גיאוגרפי** בשווקים דוברי אנגלית
- **דפוסים עונתיים** עם שיאים בנובמבר

### 🔧 כישורים טכניים שהדגמתי
- **SQL מתקדם**: פונקציות חלון מורכבות, CTEs, ניתוח קוהורט
- **מיומנות <span dir="ltr">Python</span>**: מניפולציה וניתוח סטטיסטי
- **הדמיית נתונים**: תרשימים מקצועיים וסיפור
- **ניתוח עסקי**: הפיכת נתונים לתובנות
- **ניהול פרויקטים**: מסירה מקצה לקצה

###  פרטי יצירת קשר
**ארתור** - דאטה אנליסט   
<p align="center" dir="rtl">
  <a href="mailto:artursim779@gmail.com"><img src="https://img.shields.io/badge/%D7%90%D7%99%D7%9E%D7%99%D7%99%D7%9C-ARTUR-6BA892?style=for-the-badge&labelColor=424242&logo=gmail&logoColor=white" alt="Email"></a>
  <a href="https://www.linkedin.com/in/artur-pais-848491352" target="_blank"><img src="https://img.shields.io/badge/LinkedIn-%D7%A4%D7%A8%D7%95%D7%A4%D7%99%D7%9C-1D669F?style=for-the-badge&labelColor=424242&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
  <a href="https://github.com/Artisa111" target="_blank"><img src="https://img.shields.io/badge/GitHub-ARTISA111-000000?style=for-the-badge&labelColor=424242&logo=github&logoColor=white" alt="GitHub"></a>
</p>

---

*הפרויקט הזה מדגים את היכולת שלי לבצע ניתוח משפך מקיף, ליצור תובנות עסקיות מעשיות ולתקשר ממצאים ביעילות לבעלי עניין. אני מחפש בפעילות הזדמנויות אנליסט נתונים שבהן אוכל ליישם את הכישורים האלה כדי להניע צמיחה עסקית.*
### 📄 רישיון

הפרויקט הזה נוצר למטרות הדגמת תיק עבודות. אפשר להשתמש במתודולוגיות ולהתאים לצרכים שלך.


<div align="center">
</div>

</div>

<div align="center">

### 🌟 Thank you for viewing my portfolio project! | תודה על צפייה בפרויקט התיק שלי! 🌟

[![GitHub stars](https://img.shields.io/github/stars/Artisa111/User-Onboarding-Funnel-Report-2025?style=social)](https://github.com/Artisa111/User-Onboarding-Funnel-Report-2025) 
[![Data Analytics](https://img.shields.io/badge/Portfolio-Data%20Analytics-blue?style=flat-square&logo=chartdotjs)](https://github.com/Artisa111)

**Seeking Data Analyst Opportunities | מחפש הזדמנויות אנליסט נתונים**

[🔝 Back to Top | חזרה למעלה](#user-onboarding-funnel-analysis-2024-2025--ניתוח-משפך-הטמעת-משתמשים-2024-2025)

---

<div align="center">

**💜 נוצר באהבה לאנליטיקת נתונים**

</div>
