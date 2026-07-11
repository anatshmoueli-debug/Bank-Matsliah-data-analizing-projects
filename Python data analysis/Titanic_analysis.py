
import pandas as pd #  ספריה לעבודה עם טלבלאות ונתונים
import random #ספריה בשביל לג'נרט מספרים אקראים לכרטיסים
import os # ספריה לעבודה עם קבצים ונתיבים במחשב

path = os.getcwd() #הפקודה מחזירה את התיקייה הנוכחית שהקובץ נמצא בה

df= pd.read_excel(f'{path}\\titanic.xls') #df קורא את הקובץ ומייצר דאטה פריים 


# Function 1 - get passengers name
def pass_name(): # הפונקציה שמקבלת שם של נוסע ממשתמש
   while True: # הלולאה רצה עד רגע שלא מכניסים שם של הנוסע תקין
        name = input('Enter passenger name please: ').strip() #מבקש להכניס שם של הנוסע ומסיר רווחים בהתחלה ובסוף השם  
       
        if len (name) == 0: #בדיקה אם השם ריק
            print('❌ Name is empty') 
        elif not all(char.isalpha() or char == " " for char in name): #בדיקה שכל התווים בשם הם אותיות או רווחים
            print('❌ Name must contain letters only')  
        else:
            print(f'Hello! Welcome {name}!') #אם השם תקין מופיע את הודעה 
            return name #הפקודה מחזירה את השם התקין


# Function 2 - get passengers age
def pass_age(): #  הפונקציה שמקבלת ממשתמש גיל של נוסע
    while True: #הלולאה רצה עד רגע שלא מכניסים גיל של הנוסע תקין
        try:
            age = float(input('Enter passenger age please: '))  # מבקש להכניס גיל של הנוסע וממיר אותו למספר עשרוני      
            if 0 < age < 120: #בדיקה שהגיל נמצא בטוות בין 0 ל-120
                print(f'Your age is {age}')
                return age  #הפקודה מחזירה את הגיל התקין
            else:
                print('❌ Invalid age')   # אם הגיל הוא לא בטוות בין 0 ל-120 מופעה הודעת שגיאה
        except ValueError: # בדיקה האם שהגיל הוא מספר
            print('❌ Age is not number')    # אם הכנסנו הגיל  לא מספר מופעה הודעת שגיאה


# Function 3 - get passengers gender
def pass_gender():  #M וF הפונקציה שמקבלת מין של נוסע וממיר ערך ל 
    while True: #  הלולאה רצה עד רגע שלא מכניסים מין של הנוסע תקין  
        
        gender = input('Enter passenger gender please: ').strip() #מבקש להכניס מין של הנוסע ומסיר רווחים בהתחלה ובסוף הערך
        if gender in ['m', 'M', 'male', 'Male', '1']: #רשימת ערכים החוקים למין זכר
            print('gender=' + 'M')
            return 'M' #'M' אם הוזן ערך מהרשימה הפקודה מחזירה 
                    
        elif gender in ['f', 'F', 'female', 'Female', '0']: #רשימת ערכים החוקים למין נקבה
            print('gender=' + 'F')
            return 'F' #'F' אם הוזן ערך מהרשימה הפקודה מחזירה
        else:
            print('❌ Invalid gender') # אם הכנסנו ערכים לא מהרשימה מופיעה הודעת שגיאה
        
       
# Function 4 - determinate passengers class
def determine_class_by_fare(): # הפונקציה שמקבלת מחיר הכרטיס ממשתמש ומחשבת את מחלקת נוסיעה
    while True: #    הלולאה רצה עד רגע שלא מכניסים מחיר תקין 
        try:
            fare = float(input('How much would you like to pay for the ticket? ')) # מבקש להכניס מחיר שהנוסע מעוניין לשלם וממיר אותו למספר עשרוני 
            if fare > 0: #  בדיקה עם המחיר שהכניס משתמש היא גדולה מ0
                break
            print('❌ Fare must be positive') # אם הכנסנו מחיר מספר שלילי מופעה הודעת שגיאה
        except ValueError: #   בדיקה עם המחיר שהכניס משתמש היא מספר
            print('❌ Fare must be numeric') # אם הכנסנו המחיר לא מספר מופעה הודעת שגיאה

    class_bounds = {} # יוצרים מילון ריק לשמירת גבולות מחירי הכרטיסים (רבעון ראשון ורבעון שלישי) עבור כל מחלקה  
    for pclass in [1, 2, 3]:  #  הלולאה העוברת על כל 3 מחלקות, מתבצעת שליפה וניתוח של מחירי הכרטיסים, לחישוב גבולות מחיר לכל מחלקה
        class_fares = df[df['pclass'] == pclass]['fare'].dropna() #  בודקים מחירי כרטיסים לפי מחלקה מסויימת ומסירים ערכים ריקים
        q1 = class_fares.quantile(0.25)  #מחושבים הרבעון הראשון (25%) של מחירי הכרטיסים עבור כל מחלקה
        q3 = class_fares.quantile(0.75)  #מחושבים הרבעון השלישי (75%) של מחירי הכרטיסים עבור כל מחלקה
     #ערכים אלו משמשים לזיהוי טווח המחירים בשביל לצמצם השפעת ערכים קיצוניים.        
        class_bounds[pclass] = (q1, q3) # שומרים במילון את גבולות המחירים (רבעון ראשון ושלישי) עבור כל מחלקה
    possible_classes = [] # יוצרים רשימה ריקה לאחסון מחלקות נסיעה אפשריות בהתאם למחיר שהוזן
    for pclass, (q1, q3) in class_bounds.items(): #לולאה העוברת על כל מחלקות ועל גבולות המחיר שנשמרו עבור כל מחלקה
        if q1 <= fare <= q3: # בדיקה האם מחיר הכרטיס שהוזן נמצא בטווח המחירים של מחלקה, בין הגבול התחתון וגבול העליון
            possible_classes.append(pclass) #מוסיפים את מחלקה לרשימת המחלקות המתאימות למחיר הכרטיס שהוזן
    medians_fare = { #  יוצרים מילון המכיל את מחיר הכרטיס החציוני עבור כל מחלקה
        pclass: df[df['pclass'] == pclass]['fare'].median() #חישוב חציון מחיר כרטיס לכל מחלקה
        for pclass in [1, 2, 3] # הלולאה עוברת על כל מחלקות לחישוב וניתוח נתונים עבור כל מחלקה
    }    
     
    if possible_classes: #בדיקה האם קיימות מחלקות שבהן מחיר הכרטיס שהוזן נמצא בטווח המחירים שלהן
        chosen_class = min(
            possible_classes,
            key=lambda c: abs(medians_fare[c] - fare) # חישוב ההפרש המוחלט בין המחיר החציוני של כל מחלקה לבין מחיר הכרטיס
        ) 
        #אם המחיר שהוזן נמצא בטווח המחירים של מחלקה מסויימת,
        #נבחרת המחלקה שמחירה החציוני הקרוב ביותר למחיר שהוזן,
        #על-ידי חישוב ההפרש המוחלט בין המחיר החציוני של כל מחלקה לבין מחיר הכרטיס.
    else:
        chosen_class = min(
            medians_fare,
            key=lambda c: abs(medians_fare[c] - fare) # חישוב ההפרש המוחלט בין המחיר החציוני של כל מחלקה לבין מחיר הכרטיס
        )
        # אם המחיר שהוזן לא נמצא בטווח המחירים של אף מחלקה,
        # נבחרת המחלקה שהמחיר החציוני שלה הכי קרוב למחיר שהוזן,
        #כדי להגדיר את המחלקה המתאימה בבחינה ההגיונית ביותר.
    print(f'Medians {medians_fare}')
    print(f'You paid {fare}, so your class is {chosen_class}')
    return fare, chosen_class # הפקודה מחזירה המחיר שהמשתמש הזין עבור הכרטיס והמחלקה שהוגדרה בהתאם למחיר שהנוסע שילם


# Function 5 - generate passengers ticket
def generate_ticket(issued_tickets):
     # הפונקציה שמג'נרטת כרטיס עם מספר אקראי בן 6 ספרות שלא קיים במאגר כרטיסים שהונפקו ומחזירה אותו
    existed_tickets = set(df['ticket']) #השורה יוצרת סט של כל מספרי הכרטיסים הקיימים במאגר כדי למנוע חזרות
    while True: #לולאה שרצה עד רגע שיווצר כרטיס עם המספר הייחודי
        
        new_ticket = random.randint(100000, 999999) #השורה יוצרת מספר הכרטיס האקראי בן 6 ספרות
        
        if new_ticket not in existed_tickets and new_ticket not in issued_tickets:
            #בדיקה האם הכרטיס החדש לא קיים במאגר ולא נוצר כבר במהלך הריצה הנוכחית.       
            print(new_ticket)
            return new_ticket #  הפקודה מחזירה את הכרטיס החדש לפונקציה
        else:
    #אם המספר הכרטיס כבר קיים, מופיעה הודעה שהכרטיס כבר קיים          
            print(f'The ticket exists {new_ticket}') 


# Function 6 - print passengers ticket
def print_ticket(ticket, name, age, gender, fare, pclass, survival):
   #  הפונקציה יוצרת קובץ טקסט בשם ticket.txt מכיל פרטי כרטיס של הנוסע החדש.  
      # מספר הכרטיס, שם, גיל, מגדר, מחיר הכרטיס, מחלקה, ואחוז הסתברות ההסרדות.
    with open('Titanic_ticket.txt', 'w', encoding='utf-8') as file: #  השורה פותחת קובץ טקסט חדש לכתיבה
        file.write('\n')
        file.write('**************** TITANIC BOARDING TICKET *******************\n')
        file.write('\n')
        file.write(f'Ticket Number: {ticket}\n')
        file.write(f'Name: {name}\n')
        file.write(f'Age: {age}\n')       
        file.write(f'Gender: {gender}\n')
        file.write(f'Fare: {fare}\n')
        file.write(f'Class: {pclass}\n')        
        file.write('\n')
        file.write(f'Welcome aboard {name}, your survival rate is {survival*100:.0f}%!\n')
        file.write('\n')
        file.write('************************************************************')
        

# Function 7 - determinate passengers survival
def pass_survival(age, pclass, sex):
    # הפונקציה שמחשבת את הסתברות ההישרדות של הנוסע בהתאם לגיל, מחלקה, ומגדר.
    #הפונקציה מחזירה ערך מספרי בין 0 ל‑1 שמייצג את אחוז הסתברות ההישרדות הצפוי.
    df_2=df.copy() #יוצרים עותק של מסד הנתונים המקורי
    print(df_2.isna().sum()) #השורה מציגה את מספר הערכים החסרים
    age_sex_mean=df_2.groupby('sex')['age'].mean() # השורה מחשבת את הגיל הממוצע של הנוסעים לפי מגדר
    print(age_sex_mean)
    df_2.loc[df_2['sex'] == 'male', 'age'] = (
    df_2.loc[df_2['sex'] == 'male', 'age'].fillna(age_sex_mean['male'])) 
    #השורה מבצעת מילוי ערכי גיל ריקים עבור גברים בלבד באמצעות ממוצע הגיל של גברים.
    df_2.loc[df_2['sex'] == 'female', 'age'] = (
    df_2.loc[df_2['sex'] == 'female', 'age'].fillna(age_sex_mean['female']))
 #השורה מבצעת מילוי ערכי גיל ריקים עבור נשים בלבד באמצעות ממוצע הגיל של נשים.
    print(df_2.isna().sum()) #age השורה מציגה את 0 הערכים ריקים בעמודה 
    
    surv_pclass = df_2.groupby('pclass')['survived'].sum() #השורה מחשבת את מספר הנוסעים ששרדו בכל מחלקת נסיעה
    q_pclass = df_2.groupby('pclass')['survived'].count() #השורה מחשבת את מספר הנוסעים בכל מחלקת נסיעה
    surv_pclass_percent=surv_pclass / q_pclass #השורה מחשבת את אחוז הניצולים בכל מחלקת נסיעה
    pclass_input_surv_percent=surv_pclass_percent.get(pclass) #השורה מחשבת את אחוז ההישרדות עבור מחלקת נסיעה מסוימת
    print(surv_pclass)
    print(q_pclass)
    print(surv_pclass_percent)
    print(pclass_input_surv_percent)
    
    surv_sex = df_2.groupby('sex')['survived'].sum() #השורה מחשבת את מספר הנוסעים ששרדו לפי מגדר
    q_sex = df_2.groupby('sex')['survived'].count() #השורה מחשבת את מספר הנוסעים לפי מגדר
    surv_sex_percent=surv_sex / q_sex #השורה מחשבת את אחוז הניצולים לפי מגדר
    sex_input_surv_percent=surv_sex_percent.get(sex) #השורה מחשבת את אחוז ההישרדות עבור המגדר שהוזן
    print(surv_sex)
    print(q_sex)
    print(surv_sex_percent)
    print(sex_input_surv_percent)   
    
    def categorize_age(age_2):
     #הפונקציה שמקבלת את גיל ממשתמש ומחזירה קטגוריה של גיל, בהתאם לטווחים מוגדרים מראש
        if age_2 < 1:
            return 'infant'
        elif age_2 <= 12:
            return 'child'
        elif age_2 <= 20:
            return 'teenager'
        elif age_2 <= 40:
            return 'young_adult'
        elif age_2 <= 60:
            return 'middle_aged'
        else:
            return 'senior'
    
    df_2['age_category'] = df_2['age'].apply(categorize_age) #age_category השורה ממירה את גיל הנוסעים לקטגוריות גיל ומכניסה את התוצאה בעמודה חדשה 
    
    
        
    age_cat_survival_percent = df_2.groupby('age_category')['survived'].mean() #השורה מחשבת את אחוז הניצולים לכל קטגוריית גיל    
    print(age_cat_survival_percent) 

    age_category=categorize_age(age) #categorize_age השורה שממירה את גיל הנוסע לקטגוריית גיל באמצעות הפונקציה 
    print(age_category)     
    
    age_input_surv_percent=age_cat_survival_percent.get(age_category) # השורה מחשבת את אחוז ההישרדות עבור קטגוריית הגיל של הנוסע
    print(age_input_surv_percent)
    
    weight_age=0.2 #השורה מגדירה את המשקל של גיל בחישוב הסתברות ההישרדות הסופית
    weight_pclass=0.3 #השורה מגדירה את המשקל של מחלקת הנוסע בחישוב הסתברות ההישרדות הסופית
    weight_sex=0.5 #השורה מגדירה את המשקל של מגדר בחישוב הסתברות ההישרדות הסופית
    
    survival=(  
            (weight_age*age_input_surv_percent) + 
            (weight_pclass*pclass_input_surv_percent) + 
            (weight_sex*sex_input_surv_percent)) #השורה מחשבת את הסתברות ההישרדות של הנוסע בהתאם לשלושה קריטריונים גיל, מחלקת נסיעה ומגדר
            
    print(survival)
    return(survival)# השורה מחזירה את הערך הסתברות ההישרדות

def new_passenger(function1, function2, function3, function4, function5, function6, function7):
    #הפונקציה שמקבלת ומפעילה את 7 פונקציות שמקבלות ממשתמש שם, גיל ומגדר ומבצעות תהליכי חישוב הסתברות ההסרדות  ויוצרים כרטיס לטיטניק לנוסע חדש 
    name=function1() # לתהליך חישוב הסתברות ההסרדות name השורה מעפילה את הפונקציה 1 ושומרת את הערך המוחזר ממנה במשתנה 
    age=function2() # לתהליך חישוב הסתברות ההסרדות age השורה מעפילה את הפונקציה 2 ושומרת את הערך המוחזר ממנה במשתנה 
    gender_code=function3() # לתהליך חישוב הסתברות ההסרדות gender_code השורה מעפילה את הפונקציה 3 ושומרת את הערך המוחזר ממנה במשתנה 
    gender = 'male' if gender_code == 'M' else 'female' # לתהליך חישוב הסתברות ההסרדות gender  ושומרת אותו במשתנה  male/female לערך  M/F השורה ממירה קוד מגדר  
    fare, pclass  = function4() # לתהליך חישוב הסתברות ההסרדות fare, pclass השורה מעפילה את הפונקציה 4 ושומרת את הערכים המוחזרים ממנה במשתנים 
    issued_tickets = [] # השורה יוצרת רשימה ריקה לאחסון מספרי כרטיסים שהונפקו כבר
    new_ticket = function5(issued_tickets) # issued_tickets השורה מעפילה את הפונקציה 5 ומעבירה אליה את הרשימה   
                                            # new_ticket ושומרת את הערך המוחזר ממנה במשתנה
    survival = function7(age, pclass, gender) #  השורה מעפילה את הפונקציה 7 ומעבירה אליה את גיל, מחלקת נסיעה ומגדר של הנוסע 
                                                # survival ושומרת את המוחזר ממנה  במשתנה  
    function6(new_ticket, name, age, gender, fare, pclass, survival) #   השורה מעפילה את הפונקציה 6 ומעבירה אליה את מספר הכרטיס, שם, גיל, מגדר, מחיר הכרטיס, מחלקת נסיעה, הסתברות ההסרדות
                                                                        # ושומרת אותם בקובץ 'ticket.txt'                                                                        
new_passenger(pass_name, pass_age, pass_gender, determine_class_by_fare, generate_ticket, print_ticket, pass_survival) # new_passenger השורה מפעילה את הפונקציה 