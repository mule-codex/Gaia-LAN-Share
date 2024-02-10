import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
 
app = Flask(__name__)
 
app.config['gaialan'] = 'gaialan'

socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])   
def index():
    if request.method == 'POST':
        file = request.files['fileInput']
        filename = file.filename
        file_content = file.read()
        
        print(f"Received file: {filename}, content: {file_content}")
        
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        gaia_lan_share_path = os.path.join(desktop_path, 'gaia-lan-share')

         
        if not os.path.exists(gaia_lan_share_path):
            os.makedirs(gaia_lan_share_path)
 
        file_path = os.path.join(gaia_lan_share_path, filename)
        with open(file_path, 'wb') as f:
            f.write(file_content) 

        socketio.emit('file_saved', {'message': f"File '{filename}' has been saved to 'gaia-lan-share' folder on the desktop."})

   
    return render_template('index.html')
 
@socketio.on('file_upload')
def handle_file_upload(data):
    filename = data['filename']
    file_content = data['file_content']
    
    print(f"Received file: {filename}, content: {file_content}")
    
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    gaia_lan_share_path = os.path.join(desktop_path, 'gaia_lan_share')

    if not os.path.exists(gaia_lan_share_path):
        os.makedirs(gaia_lan_share_path)

    file_path = os.path.join(gaia_lan_share_path, filename)
    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    emit('file_saved', {'message': f"File '{filename}' has been saved to 'gaia_lan_share' folder on the desktop."})

    emit('file_received', {'filename': filename, 'file_content': file_content}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
