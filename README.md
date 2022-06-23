<!-- PROJECT SUMMARY -->
<p align="center">
  <h1 align="center">AcadeMe</h1>
  <p align="center">
    { A Wellness Support Made for Students }
  </p>
</p>

<!-- TABLE OF CONTENT -->
<details open="open">
  <summary><h2 style="display: inline-block">🕹 Table of Content</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Documentation</a>
    </li>
    <li><a href="#team">Team</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## :star: About The Project
AcadeMe is a web platform built to make wellness support for students more accessible and enjoyable.

<!-- CONTENT -->
## :clipboard: Documentation

### :round_pushpin: Dependencies

#### Frontend
Must have **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) with commands:
```
npm init -y
npm install bootstrap@3
```
#### Backend
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```
### :round_pushpin: Structure
  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app.
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py 
  ├── requirements.txt 
  ├── static
  │   ├── css
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

### :round_pushpin: Setup
1. **Download the project locally**
```
git clone https://github.com/TheAMTeam/AcadeMe
cd AcadeMe
```

2. **Initialize and activate a virtualenv using:**
```
python -m virtualenv env
source env/bin/activate
```

3. **Install the dependencies:**
```
pip install -r requirements.txt
```

4. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```

5. **Verify in the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000)

<!-- TEAM -->
## :sunflower: Team
- [Wenjia](https://github.com/wenjialu)
- [Jenny](https://github.com/JennyHWAN)
- [Sarah](https://github.com/procrasprincess)
- [Mitali](https://github.com/MitaliO)
