import cgi
from wsgiref.simple_server import make_server

sum = ''
form = '''
<html>
    <head>
        <title>Task2</title>
    </head>
    <body>
    <form method = "post">
        <label for="x">x: </label> <input type="text" name="x" id="x" value="{value_x}"> <br><br>
        <label for="y">y:</label> <input type="text" name="y" id="y" value="{value_y}"> <br><br>
        
        <input type="submit">
    
       <p>Sum={sum}</p>
    
    </form>
    </body>
</html>
'''

def app(environ, start_response):
    global sum
    x = ''
    y = ''
    
    html = form

    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        
        x = post['x'].value if post['x'].value else 0
        y = post['y'].value if post['y'].value else 0
        sum = int(x) + int(y)
        
    start_response('200 OK', [('Content-Type', 'text/html')])
    
    html = html.format(sum=sum, value_x=x, value_y=y)
    html = html.encode('utf-8')
    
    return [html]

if __name__ == '__main__':
    try:
        httpd = make_server('127.0.0.1', 8080, app)
        print('Serving on port 8080...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Goodbye')