import cgi, cgitb 
import os
import http.cookies

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

checkbox_choices = ['maths', 'biology', 'chemistry', 'history']


first_text = form.getvalue('first_text')
second_text  = form.getvalue('second_text')
checkbox_choices = [i for i in checkbox_choices if form.getvalue(i)]
radio_choice = form.getvalue('lang')



cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
form_filled = cookie['form_filled'].value

if form_filled is None:
    print("Set-cookie: form_filled=1")
else:
    form_filled = int(form_filled)+1
    print(f"Set-cookie: form_filled={form_filled}")

html_response = f"""Content-type:text/html\r\n\r\n
<html>
    <head>
        <title>Task1</title>
    </head>
    <body>
        <h1>Обробка даних форм!</h1>

        <p>First text: {first_text} </p>
        <p>Second text: {second_text} </p>

        <p>So, your choice...: {', '.join(checkbox_choices)}</p>
    
        <p>You want to study: {radio_choice}</p>
        
        <p>The form has been filled out {form_filled} times</p>

        
        
    </body>
</html>
"""
print(html_response)