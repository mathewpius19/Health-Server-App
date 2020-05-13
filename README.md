This is a website made with Flask Library used to determine your remote server's health using psutil library and python.


prerequisites are:
        
        python3 
        linux remote server

Log onto your linux remote server and git clone this repository:

        git clone https://github.com/mathewpius19/Health-Server-App.git
Move into the Health-Server-App and change necessary permissions of requirements.py and report.py
        
        sudo chmod 777 report.py
        sudo chmod 777 requirements.py

Run requirements.py file to generate the report on your remote server.
        
        sudo python3 requirements.py
MIT License

Copyright (c) 2020 Mathew

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
