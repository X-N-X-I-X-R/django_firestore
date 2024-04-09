
Scikit-learn 
++++++++++++++++++++++++++ 
זוהי ספריית פייתון ללמידת מכונה פתוחה ופופולרית.
היא מכילה מודלים לכמה סוגים של למידת מכונה כגון סיווג,
ריגרסיה, ניתוח וכו'. 
כמו כן, הספרייה מכילה כלים להערכת ביצועים, 
ניתוח נתונים וכלים נוספים לעזרה בתהליך הלמידה.


תהליך העבודה 
++++++++++++++++++++++++++
1. ייבוא הספרייה
2. קריאת הנתונים
3. הכנת הנתונים לאלגוריתם
4. הכנת המודל
5. הכשרת המודל
6. בדיקת המודל
7. הערכת ביצועי המודל
8. הצגת תוצאות
9. הצגת גרף
10. הצגת גרף קווי רגרסיה
11. הצגת מטריצת ההתבדלות
******************************
התקנות : 
1. pip install scikit-learn  
2. pip install matplotlib
3. pip install pandas
4. pip install numpy
5. pip install seaborn
6. pip install scipy
7. pip install joblib
8. pip install xgboost
9. pip install lightgbm
10. pip install catboost
11. pip install statsmodels
12. pip install yellowbrick
13. pip install mlxtend
14. pip install imbalanced-learn
15. pip install scikit-plot
16. pip install scikit-learn-extra
17. pip install scikit-learn-intelex
18. pip install scikit-learn-extensions
19. pip install scikit-learn-quantile
20. pip install graphviz 



##########################
איך להתחיל עם Scikit-learn :

1. ייבוא הספרייה  
import sklearn

2. קריאת הנתונים
from sklearn.datasets import load_iris
data = load_iris()
X = data.data
y = data.target
* הסבר קריאת הנתונים: 
1- load_iris()- קריאת הנתונים ממסד הנתונים של scikit-learn
2- data.data- המאפיינים של הנתונים
3- data.target- החיזוי של הנתונים

3. הכנת הנתונים לאלגוריתם
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
* הסבר הכנת הנתונים לאלגוריתם:
1- train_test_split- פונקציה שמחלקת את הנתונים לקבוצת אימון ובדיקה
2- X_train, X_test, y_train, y_test- הקבוצות של המאפיינים והחיזוי
3- test_size- גודל הקבוצה של המידע שנשמר לבדיקה
4- random_state- גרעין רנדומלי

4. הכנת המודל
from sklearn.linear_model import LinearRegression
model = LinearRegression()
* הסבר הכנת המודל:
1- LinearRegression()- בחירת המודל שנבחר
2- model- המודל שנבחר

5. הכשרת המודל
model.fit(X_train, y_train)
* הסבר הכשרת המודל:
1- fit()- פונקציה שמכשירה את המודל על קבוצת האימון
2- X_train, y_train- קבוצת האימון

6. בדיקת המודל
y_pred = model.predict(X_test)
* הסבר בדיקת המודל:
1- predict()- פונקציה שמחזירה חיזוי של המודל על קבוצת הבדיקה
2- X_test- קבוצת הבדיקה

7. הערכת ביצועי המודל
model.score(X_test, y_test)
* הסבר הערכת ביצועי המודל:
1- score()- פונקציה שמחזירה את הביצועים של המודל על קבוצת הבדיקה
2- X_test, y_test- קבוצת הבדיקה

8. הצגת תוצאות
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))
* הסבר הצגת תוצאות:
1- classification_report()- פונקציה שמציגה דוח על ביצועי המודל
2- y_test, y_pred- קבוצת הבדיקה והחיזוי

9. הצגת גרף
import matplotlib.pyplot as plt
plt.scatter(X_test, y_test, color='red')
plt.plot(X_test, y_pred, color='blue')
plt.show()
* הסבר הצגת גרף:
1- scatter()- פונקציה שמציגה נקודות על הגרף
2- plot()- פונקציה שמציגה קו על הגרף
3- show()- פונקציה שמציגה את הגרף

10. הצגת גרף קווי רגרסיה
plt.scatter(X, y, color='red')
plt.plot(X, model.predict(X), color='blue')
plt.show()
* הסבר הצגת גרף קווי רגרסיה:
1- scatter()- פונקציה שמציגה נקודות על הגרף
2- plot()- פונקציה שמציגה קו על הגרף
3- show()- פונקציה שמציגה את הגרף

11. הצגת מטריצת ההתבדלות
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))
* הסבר הצגת מטריצת ההתבדלות:
1- confusion_matrix()- פונקציה שמציגה את מטריצת ההתבדלות
2- y_test, y_pred- קבוצת הבדיקה והחיזוי

##########################
סיכום:
הכנת הנתונים
X = המאפיינים
y = החיזוי
test_size = גודל הקבוצה של המידע שנשמר לבדיקה
random_state = גרעין רנדומלי

הכנת המודל
model = המודל שנבחר

הכשרת המודל
model.fit(X_train, y_train) = הכשרת המודל על קבוצת האימון

בדיקת המודל
model.predict(X_test) = חיזוי המודל על קבוצת הבדיקה

הערכת ביצועי המודל
model.score(X_test, y_test) = הערכת ביצועי המודל על קבוצת הבדיקה

הצגת תוצאות
print(classification_report(y_test, y_pred)) = הצגת דוח על ביצועי המודל

הצגת גרף
plt......

הצגת גרף קווי רגרסיה
plt......

הצגת מטריצת ההתבדלות
print(confusion_matrix(y_test, y_pred)) = הצגת מטריצת ההתבדלות

##########################



