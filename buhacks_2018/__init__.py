"""
Praesidium project to analyses the IMP
"""
import os
import json
from datetime import datetime
from flask import (
    Flask, render_template, request, session, flash, url_for, redirect, jsonify
)

app = Flask(__name__)



@app.route('/')
@app.route('/api/v1.0/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
