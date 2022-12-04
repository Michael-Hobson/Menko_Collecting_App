<div align="center">
  <a href="https://github.com/Michael-Hobson/Menko_Collecting_App" name="readme-top">
    <h1>Menko Collecting Web App</h1>
  </a>
  
  <p align="center">
    Full-CRUD Python App for Building Your Own Menko Card Collection
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<p>
Menko collecting in the United States, and even in Japan, has not had the same kind of widespread collecting culture that other similar hobbies have. Sports cards, tobacco cards, Pokemon, Magic: The Gathering, and others have had a long history of collectors who have compiled information on all the cards in their respective genre. This app is an attempt to bring menko collectors together to begin building out a database of cards.

This project was built utilizing the agile development process. This included a planning meeting, daily stand-up meetings, and the development of user stories via Trello to build out the features. The planning process also included full visual concept wireframes designed in Excalidraw.
  
This full-CRUD application took advantage of Python’s concise, compact, and easy-to-read code to create an application in just five days. The user interface was built utilizing CSS and Bootstrap and allows collectors to easily create and manage a new database of cards.

I developed a complete login and registration system via RegEx, validations, and bcrypt to allow users to create accounts and easily build, track, and maintain their own Menko card collection over time. A MySQL database was utilized for a quick and reliable data storage solution. I also connected a third-party application called IMGBB to enable users to upload their own card photos and access them locally. This allowed for the storing of a URL within the MySQL database rather than the full image files.
  
This full-stack Python project was completed as part of my coding bootcamp Project Week with all work completed in five days and culminated with a full presentation of the final working app to my cohort.
</p>

![Main_Page_GIF](https://user-images.githubusercontent.com/109699879/205513217-afc38c1b-9beb-4616-93f1-84ca99b2c73a.gif)

![Create_Menko_GIF](https://user-images.githubusercontent.com/109699879/205513269-afc72837-99ba-43ea-a405-fad85dc8836c.gif)

![Dashboard_Show_GIF](https://user-images.githubusercontent.com/109699879/205513234-e63d89d1-79ba-4af9-92d5-009b78ba8cbe.gif)

![Delete_Logout_GIF](https://user-images.githubusercontent.com/109699879/205513242-9ac0886d-550d-439a-9409-ee4d3ca1770a.gif)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

This section lists any major frameworks/libraries used in our project.

* ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
* ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
* ![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
* ![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
* ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
* ![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites
* Install dependencies
  ```sh
  pipenv install flask pymysql flask-bcrypt
  ```

### Run the Project
Inside the project directory along side Pipefile & Pipefile.lock, got into the shell
* pipenv
  ```sh
  pipenv shell
  ```
Once in shell, run the server
* Python
  ```sh
  python server.py
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

* Michael Hobson - [@Linkedin](https://www.linkedin.com/in/michaelghobson/) - mikehobson@outlook.com

Project Link: [https://github.com/Michael-Hobson/Menko_Collecting_App](https://github.com/Michael-Hobson/Menko_Collecting_App)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

This ReadME page is created using the template below:

* [README_Template](https://github.com/othneildrew/Best-README-Template/blob/master/README.md)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
