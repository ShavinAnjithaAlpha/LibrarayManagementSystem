import sys
from PyQt5.QtWidgets import QTextBrowser, QApplication, QWidget

# create the htmo code
html_code = """
                <img  src="images/sys_images/coll_img1.png" width="200" height="200" alt="image lock" align="center"/>

    <h2 align="center">Title Title Title TItle</h2>

    <p align="center">afkjhfjahfjkhskjhdsh s hhdsgh ksg hkjshkjgh khghsh hshkghk j
    sg kjhkhjs hghshg hsgh kshgkhsgfoehgh katuoe h hw hh hhgo rg
     ew ghewtikuwey iuwthrwet uhu rt r


    </p>



    <h3>Cretation Day</h3>
    2020 Aug 22

    <h3>Creation time</h3>
    45:12 AM

    <div id="line">
        <h2>s</h2>
    </div>

    <h5>History</h5>


    <style>

        h5 {color : blue;
            font-size : 25px;
            font-family : verdana}

        img {align : center;
        padding-left : 230px;}

        div#line {background-color : blue}

        h1 {background-color : rgb(0, 10, 150);
            color : rgb(200, 200, 200);
            padding : 30px;
            margin : 20px;
            font-family : verdana;
            font-size : 40px;}

        h2 {background-color : rgb(0, 0, 0);
            color : rgb(200, 200, 200);
            padding : 30px;
            margin : 20px;
            font-family : verdana;
            font-size : 40px;
            align : center}


        p {font-size : 19px;
            color : white;
            font-family : verdana}

        body {background-color : rgb(10, 10, 10);
            color : white}
        h3 {background-color : rgb(0, 0,150);
            padding : 10px;
            align : left;
            width : 250px;
            font-family : hack}
    </style>
                """

# create the text editor
app = QApplication([])
window = QTextBrowser()
with open("test.html") as file:
    html = file.read()
window.setHtml(html)

window.show()

app.exec_()