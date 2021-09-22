
dark_style_sheet = """

                QMenuBar {background-color : rgb(0, 0, 100);
                            color : white;
                            font-size : 18px;
                            padding : 0px;
                            margin : 0px;}
                            
                QMenuBar::item:hover{background-color : blue;}
                
                QWidget#mainWindowWidget {padding : 0px;}
                                
                QWidget#mainWidget {background-color : rgb(20, 20 ,20);
                                    padding : 0px;}
                
                QWidget#stageArea {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(10, 10, 10), stop : 1 rgb(50, 50, 50));;
                                    border : none;
                                    margin : 0px;}
                
                QScrollArea#mainScrollArea {border : none;
                                            padding : 0px;
                                            margin : 0px;}
                
                QTabBar::tab {background : none;
                                                color : white;
                                                border : none;
                                                padding : 10px;
                                                border-right : 1px solid black;
                                                border-top-right-radius : 3px;
                                                border-top-left-radius : 3px;
                                                font-size : 15px;
                                                width : 93px}
                                                
                QTabBar::tab:hover {background-color : rgb(50, 50, 50)}
                
                QTabBar::tab:selected {border-bottom : 2px solid blue;
                                    color : white}
                                    
                QTabWidget#reminderTab::pane {border : 1px solid rgb(50, 50, 50);
                                        border-radius : 5px;
                                        margin : 0px;
                                        padding : 0px;}
                                        
                QTabWidget#stageTab:pane {background : none;
                                            border : none;
                                            padding  : 0px;
                                            margin : 0px;}
                                            
                QTabBar#stageTabBar::tab {
                                    background : none;
                                    color : white;
                                    border : none;
                                    max-height : 15px;
                                    border-right : 1px solid black;
                                    border-top-right-radius : 3px;
                                    border-top-left-radius : 3px;
                                    font-size : 15px;
                                    width : 93px}
                                    
                
                                    
                QTabBar#stageTabBar::tab:selected {
                                    border-bottom : 2px solid blue;
                                    
                                    }
                                                
                QWidget#statusWidget {background-color : rgb(0 ,0, 0);
                                    border : none;
                                    margin : 0px;
                                    padding : 0px;}
                
                QWidget#barWidget {background-color : rgb(25, 25, 25);
                                    border : none;
                                    padding : 0px;
                                    margin : 0px;}
                                    
                QWidget#titleBarWidget {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 120), stop :0.5 rgb(0, 0, 80)  ,stop : 1 rgb(0, 0,30));
                                        border : none;
                                        color : white;
                                        margin : 0px;
                                        padding : 0px;
                                    }
                                    
                QWidget#toolBarWidget {border-bottom : 1px solid rgb(0, 0, 30);
                                        background-color : rgb(25, 25, 25);
                                        margin : 0px;
                                        padding : 0px;}
                                    
                QWidget#reminderWidget {background-color : rgb(0, 0, 10);
                                        margin : 0px;
                                        padding : 0px;}
                                        
                QLabel#title_label {color : white;
                                    background : none;
                                    margin : 0px;}
                                    
                QLineEdit#searchBar {background-color : rgb(40, 40, 40);
                                        padding : 6px;
                                        border : none;
                                        color : rgb(200, 200, 200);
                                        font-size : 24px;
                                        margin : 0px 0px 0px 0px;}
                                        
                QRadioButton#searchOptionRadioButton {color : rgb(200, 200, 200);
                                                    background : none;
                                                    font-size : 16px}
                
                QRadioButton#searchOptionRadioButton::indicator:!checked {background-color : rgb(60, 60, 60);
                                                                        max-width : 25px;
                                                                        max-height : 25px;
                                                                        min-width : 25px;
                                                                        height : 25px;
                                                                        border-radius : 12px;}
                
                QRadioButton#searchOptionRadioButton::indicator:checked {background-color : rgb(240, 60, 6);
                                                                         max-width : 25px;
                                                                        max-height : 25px;
                                                                        min-width : 25px;
                                                                        min-height : 25px;
                                                                        border-radius : 12px;}
                
                QGroupBox {border : none;
                            background : none}
                            
                QPushButton#addButton {background-color : rgb(0, 40, 250);
                                        border : none;
                                        padding : 5px;
                                        width : 50px;
                                        height : 50px;
                                        border-radius : 25px;
                                        max-width : 50px}
                                        
                QPushButton#addButton:hover , QPushButton#addButton:pressed {background-color : rgb(0, 100, 200)}
                                        
                QPushButton#selectButton {color : black;
                                            background-color: blue;
                                            border : 2px solid rgb(0, 0, 220);
                                            padding : 10px;
                                            border-radius : 8px;
                                            font-size : 18px;}
                                            
                QPushButton#selectButton:hover {background-color  rgb(0, 0, 180);}
                                            
                QDialog#selectedDialog {background : none;}
                                            
                QLabel#favoriteTitleLabel , QLabel#recentTitleLabel {background-color : rgb(40, 40, 40);
                                            font-size : 16px;
                                            padding : 5px;}
                                            
                                            
                QPushButton#backwardButton {border : none;}
                
                QPushButton#backwardButton:hover:enabled {background-color : rgb(50, 50, 50);
                                                        border-radius : 20px;}
                
                QPushButton#forwardButton {border : none;}
                
                QPushButton#forwardButton:hover:enabled {background-color : rgb(50, 50, 50);
                                                        border-radius : 20px;}
                                                        
                QPushButton#refreshButton {background : none;
                                        border : none;
                                        max-width : 50px;
                                        min-width : 50px;}
                                        
                QPushButton#refreshButton:hover {background-color : rgb(50, 50, 50);
                                                max-width : 50px;
                                                min-width : 50px;
                                                border-radius : 20px;}
                                                
                QPushButton#showButton , QPushButton#hideButton {background : none;
                                                                color : white;
                                                                border : none;
                                                                padding : 10px;
                                                                font-size : 25px;}
                                                                
                QPushButton#showButton:hover , QPushButton#hideButton:hover {background : none;
                                                                color : blue;}
                                                                
                QListWidgetItem {background-color : rgb(50, 50, 50)}
                
                QScrollBar:vertical, QScrollBar:horizontal {background-color : rgb(20, 20 ,20);
                                                max-width : 10px;
                                                border-radius : 5px}
                QScrollBar::handle:vertical {background-color : rgb(50, 50 ,50);
                                                border-radius : 5px;
                                                margin-top : 0px;
                                                margin-bottom : 0px}
                                                
                QScrollBar::handle:horizontal {background-color : rgb(50, 50 ,50);
                                                border-radius : 5px;
                                                margin-left : 0px;
                                                margin-right : 0px}
                                                
                QScrollBar::handle:vertical:hover {background-color : rgb(0, 120, 240)}
                
                QScrollBar::handle:horizontal:hover {background-color  :rgb(0, 120, 240)}
                
                QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal 
                                                        {background : none;
                                                        border : none}
                                                        
                QScrollBar::sub-line:horizontal, QScrollBar::add-line:horizontal {background : none;
                                                        border : none}
                
                QScrollBar::up-arrow:vertical , QScrollBar::down-arrow:vertical
                                                {background : none;
                                                border : none}
                                                
                QScrollBar::right-arrow:horizontal , QScrollBar::left-arrow:horizontal
                                                {background : none;
                                                border : none}
                                                
                QListWidget {
                            border-left : 2px solid rgb(240, 0 ,0);
                            background : none}
                            
                QInputDialog QPlainTextEdit {border : 1px solid rgb(100, 100, 100);
                                        border-radius : 5px;
                                        font-size : 16px;
                                        color : white;
                                        min-width : 700px;
                                        padding : 10px;
                                        min-height : 350px;}
                                        
                QInputDialog QLabel {font-size : 18px;}
                                        
                QInputDialog QPushButton {background : rgb(0, 0, 200);
                                        color: white;
                                        border : none;
                                        border-radius :0px;
                                        padding : 5px;
                                        font-size : 17px;
                                        width : 120px;}
                                        
                     
                QInputDialog QLineEdit {border : 1px solid rgb(100, 100, 100);
                                        border-radius : 5px;
                                        font-size : 16px;
                                        color : white;
                                        padding : 10px;
                                        min-width : 300px;}
                                        
                                
                                         
                QInputDialog QPushButton:hover {background-color : blue;
                                                border : none;
                                                color : white}
                                                
                QPushButton#toolBarHideButton {background : none;
                                                border : none;
                                                font-size : 17px;
                                                color : white;}
                                                
                QPushButton#toolBarHideButton:hover {color : blue} 
                
                QComboBox#sortingComboBox:pane {border-radius : 5px;}
                
                QMessageBox {min-width : 250px;}
                            
                QMessageBox QLabel {font-size : 20px;}
                
                
                QMessageBox QPushButton {background : rgb(0,0, 200);
                                        border : 3px solid rgb(0, 0, 255);
                                        color : white;
                                        padding : 5px;
                                        font-size : 18px;
                                        height  : 35px;
                                        width : 75px;
                                        margin : 15px;
                                        border-radius : 10px;
                                        }
                
                QMessageBox QPushButton:hover {background : rgb(0, 0, 255);
                                        border : none}
                                        
        
                
                QMessageBox#closeMessage QPushButton {background-color : blue;
                                                    padding : 20px;
                                                    font-size : 21px;
                                                    border : none;
                                                    width : 100px;
                                                    max-height : 50px;
                                                    margin : 15px;}
                                                    
                QMessageBox#closeMessage QPushButton:hover {background-color : rgb(0, 0, 150);
                                                            border : 2px solid blue;}
                                                            
                QPushButton#reminderAddButton {background-color : blue;
                                                border : none;
                                                padding : 5px;
                                                color : white;
                                                }
                QTextEdit#reminderNote {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(150, 150, 0), stop : 1 rgb(250, 250, 0));
                                        border : none;
                                        padding : 5px;
                                        color : black;
                                        font-size : 19px;
                                        border-top : 20px solid rgb(0, 200, 50);
                                        min-height : 250px;}
                                        
                QPushButton#collectionToolBarButton {background : none;
                                                    border : none;
                                                    padding : 10px;
                                                    font-size : 18px;
                                                    text-align : top;
                                                    }
                QPushButton#collectionToolBarButton:hover {background-color : rgb(40, 40, 40);
                                                                                                        }
                                                                                                        
                QPushButton#stackChangeButton {background : none;
                                                border : none;
                                                font-size : 18px;
                                                max-width : 30px;}
                
                QPushButton#stackChangeButton:hover {color : blue;}
                                                    
                                    
                
                """

dark_style_sheet_for_widgets = """
                                
                                QPushButton#switchButtonLeft {background-color : rgb(60, 60, 60);
                                                                color : white;
                                                                font-size : 16px;
                                                                padding : 5px;
                                                                border : none;
                                                                max-width : 220px;
                                                                border-top-right-radius : 0px;
                                                                border-bottom-right-radius : 0px;
                                                                border-top-left-radius : 10px;
                                                                border-bottom-left-radius : 10px;}
                                                                                                    
                                QPushButton#switchButtonRight {
                                                                background-color : rgb(60, 60, 60);
                                                                color : white;
                                                                max-width : 220px;
                                                                font-size : 14px;
                                                                padding : 5px;
                                                                border : none;
                                                                border-top-right-radius : 10px;
                                                                border-bottom-right-radius : 10px;
                                                                border-top-left-radius : 0px;
                                                                border-bottom-left-radius : 0px;}
                                                                                                    
                                QPushButton#switchButtonLeft:checked, QPushButton#switchButtonRight:checked {background-color : blue;
                                                                                                                color  : white}
                                                                                                    
                                QLineEdit#titleEdit {background : none;
                                                    border : 1px solid rgb(100, 100, 100);
                                                    padding : 5px;
                                                    color : white
                                                    }
                                
                                QLineEdit#titleEdit:focus , QTextEdit:focus {border : 1px solid rgb(240, 65, 5)}
                                
                                QTextEdit#descriptionEdit {background : none;
                                                            border : 1px solid rgb(100, 100, 100);
                                                            border-radius : 2px;}
                                                            
                                QLineEdit#imageDirEdit {background : none;
                                                        border : 1px solid rgb(100, 100, 100);
                                                        padding : 2px;
                                                        font-size : 12px;}
                                                            
                                QDialog QLabel {font-size : 15px;}
                                
                                QDialog > QPushButton {background : none;
                                                            border : 1px solid rgb(100,100, 100);
                                                            border-radius : 2px;
                                                            padding : 3px;
                                                            color : white;
                                                            font-size : 15px;}
                                                            
                                QDialog > QPushButton:hover {background-color : rgb(240, 60, 6);
                                                            color : black;}
                                      
                                QCheckBox {font-size : 15px;}
                                QCheckBox::indicator:!checked {background-image : url(images/sys_images/unchecked_box.png);}
                                
                                QCheckBox::indicator:checked {background-image : url(images/sys_images/check_box.png)}                      
                                
                                """

dark_style_sheet_for_Collection = """
                                    
                                    QInputDialog QPlainTextEdit {border : 1px solid rgb(100, 100, 100);
                                        border-radius : 5px;
                                        font-size : 16px;
                                        color : white;
                                        min-width : 700px;
                                        padding : 10px;
                                        min-height : 350px;}
                                        
                                    QInputDialog QLineEdit {border : 1px solid rgb(100, 100, 100);
                                        border-radius : 5px;
                                        font-size : 16px;
                                        color : white;
                                        padding : 10px;
                                        min-width : 300px;}
                                        
                                    QInputDialog QLabel {font-size : 22px;}
                                        
                                    QInputDialog QPushButton {background : rgb(0, 0, 200);
                                        color: white;
                                        border : none;
                                        margin : 5px;
                                        border-radius : 5px;
                                        padding : 5px;
                                        font-size : 17px;}
                                        
                                
                                         
                                    QInputDialog QPushButton:hover {background-color : blue;
                                                border : none;
                                                color : white}
                                    
                                    QWidget#collectionBaseWidget {background-color : rgb(10, 10, 10);
                                    background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 20), stop : 1 rgb(0, 0, 100));
                                                                    border : 1px solid rgb(240, 50, 6);
                                                                    border : none;
                                                                    border-left : 8px solid rgb(0, 240, 66);
                                                                    border-radius : 5px;}
                                                                    
                                    QWidget#collectionBaseWidgetSelected {background-color : rgb(0, 50, 200);
                                    background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 100), stop : 1 rgb(0, 0, 240));
                                                                    border-left : 8px solid rgb(0, 240, 66);
                                                                    widget-animation-duration : 1000;
                                                                    border-radius : 5px;
                                                                    color  : white}
                                                                    
                                   
                                                                    
                                    QWidget#collectionBaseWidget:hover {background-color : rgb(30, 30, 30);
                                                                        widget-animation-duration : 1000ms;
                                                                        background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 30), stop : 1 rgb(0, 0, 130));}
                                                                    
                                    QLabel#collectionDescriptionLabel {color : rgb(150, 150, 150);
                                                                        alignment : center}
                                                                        
                                    
                                                                        
                                    QLabel#collectionTitleLabel {color : rgb(200, 200, 200)}
                                    
                                    QPushButton#favoriteButton:!checked {
                                                                        background : none;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 50px;
                                                                        max-height : 50px;
                                                                        
                                                                        border-radius : 10px;}
                                                                        
                                    QPushButton#favoriteButton:checked {
                                                                        background : none;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 50px;
                                                                        max-height : 50px;
                                                                        border-radius : 10px;}
                                                                        
                                    QWidget#bookBaseWidget {background-color : rgb(0, 0, 10);
                                                            border-left : 5px solid rgb(240, 60, 6);
                                                            border-top-right-radius : 20px;
                                                            border-bottom-right-radius : 20px;
                                                            border-top-left-radius : 0px;
                                                            border-bottom-left-radius : 0px;
                                                            color : white}
                                                            
                                    QWidget#bookBaseWidget:hover {background-color : rgb(20, 20, 30)}
                                                            
                                    QLabel#bookTitleLabel {background : none;
                                                            font-family : verdana;
                                                            font-size : 16px;
                                                            color : rgb(200, 200, 200)}
                                                            
                                    QPushButton#bookFavoriteButton:!checked {background : none;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 30px;
                                                                        max-height : 30px;
                                                                        border : none;
                                                                        border-radius : 10px;}
                                                                        
                                    QPushButton#bookFavoriteButton:checked {background : none;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 30px;
                                                                        max-height : 30px;
                                                                        border : none;
                                                                        border-radius : 10px;}
                                                                        
                                    QPushButton#menuButton {max-width : 50px;
                                                            border : none}
                                                            
                                    QPushButton::menu-indicator {background : orange;
                                                                border-radius : 5px;
                                                                border : 1px solid  orange}
                                    QPushButton::menu-indicator:hover {background : red;
                                                                border-radius : 5px;
                                                                border : 1px solid  red}
                                    
                                    
                                    QPushButton#collection_role_button {background : none;
                                                                        color : rgb(100, 100, 100);
                                                                        border : none;
                                                                        max-width : 20px;}
                                                                        
                                    QPushButton#collection_role_button:hover {background : none;
                                                                        color : rgb(0, 50, 150);
                                                                        border : none}
                                    
                                    """

status_style_sheet_dark = """
                        
                        QLabel#sepLabel {background-color : rgb(150, 150, 150);
                                        max-height : 2px;
                                        min-height : 2px;
                                        border : none;
                                        }
                                        
                        QLabel#dataLabel  {font-size : 15px;
                                            font-family : Hack;
                                            color : white;
                                            alignment : right}
                                            
                        QLabel#titleLabel {font-size : 18px;
                                            color : blue;
                                            alignment : left}
                                            
                        QLabel {font-size : 16px;
                                alignment : left}
                                
                        QWidget#plainTextEdit {background : none;
                                        border : none}
                        
                        """


root_collection_dark_style_sheet = """
                                    QLabel#titleLabel {color : rgb(0, 0 , 255);
                                                        font-size : 20px;
                                                        margin : 0px;}
                                                        
                                    QLabel#descriptionLabel {font-size : 16px;}
                                    
                                    QLabel#rootLabel {background-color : rgb(0, 0, 150);
                                                    padding  10px;
                                                    margin : 0px;
                                                    border-radius : 3px;
                                                    }
                                    
                                    
                                    """

dark_style_sheet_for_status = """
                                
                                
                                QPushButton#closeButton {background-color : rgb(250, 50, 0);
                                                        padding : 5px;
                                                        alignment : center;
                                                        color : white;
                                                        border : none;
                                                        font-size : 16px;
                                                        width : 100px;
                                                        }
                                                        
                                QPushButton#closeButton:hover {background-color : rgb(200, 0, 0)}
                                
                                QLabel#historyLabels {color : rgb(150, 150, 150)}
                                
                                QLabel#historyReferLabel {background-color : rgb(30, 30, 30);
                                                        padding : 10px;
                                                        width : 80px;
                                                        font-size : 17px;}
                                
                                """


style_sheet_dark_for_book = """

                            QWidget {background-color : rgb(10, 10, 10);
                                    color : white;
                                    border-top : 1px solid rgb(0, 60, 200);
                                    margin : 0px}
                            
                            QWidget#historyWidget {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 30), stop :0.5 rgb(0, 0, 80) ,stop : 1 rgb(0, 0, 150));
                                                    border : none;
                                                    border-left : 1px solid rgb(0, 0, 200);
                                                    margin : 0px}
                                                    
                            QWidget#historyWidget2 {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 30), stop :0.5 rgb(0, 0, 80) ,stop : 1 rgb(0, 0, 120));;
                                                    border : none;}
                            
                            QWidget#bookMarkWidget {background-color : rgb(150,0, 0);
                                                    border : 1px solid rgb(0, 0, 200)}
                            
                            
                            QPushButton#pageAddButton {background-color : rgb(40, 40, 40);
                                                        border : none;
                                                        color : white;
                                                        padding : 5px;
                                                        }        
                                                        
                            QPushButton#pageAddButton:hover {
                                                        color : rgb(200, 200,200);
                                                    
                                                        }        
                            
                            QLabel#pageTitleLabel {color  :rgb(0, 0, 200);
                                                    border: none;
                                                    background-color : rgb(40, 40, 40);
                                                    padding : 5px;}
                                                    
                            QLabel#topTitleLabel {color : rgb(200, 200, 200);
                                                border : none;}
                            QLabel#descriptionLabel {color : rgb(150, 150, 150);
                                                    border : none}
                            
                            QPushButton#openButton {padding : 10px;
                                                    min-width : 200px;
                                                    margin-left : 100px;
                                                    margin-right : 100px;
                                                    background-color : rgb(0, 0, 200);
                                                    border : none;
                                                    color : white}
                                                    
                            QPushButton#openButton:hover , QPushButton#openButton:pressed {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 100), stop : 1 rgb(0, 0, 250));}
                                                    
                            QLabel#coverImage {background-color  :rgb(40, 40, 40);
                                                border : none;
                                                border-left : 3px solid rgb(0, 0, 200);
                                                border-radius : 0px;
                                                border-top-right-radius : 20px;
                                                border-bottom-right-radius : 20px;
                                                margin-left : 20px;}
                                                
                            QLabel#commentTitleLabel {padding : 10px;
                                                        margin : 0px;
                                                        border : none;
                                                        color : rgb(150, 150, 150);
                                                        border-bottom : 1px solid blue;
                                                        }
                                                        
                            QPushButton#commentAddButton {padding : 10px;
                                                        margin : 0px;
                                                        border : none;
                                                        border-bottom : 1px solid blue;
                                                        }
                                                        
                            QWidget#bookStatusWidget {background-color : rgb(20, 20, 20);
                                                        border-right : 1px solid blue;
                                                        border-left : 1px solid blue}
                            
                            QLabel#statusTitleLabel {background : none;
                                                    border : none;
                                                    margin : 0px;
                                                    color : rgb(200, 200, 200);
                                                    border-bottom : 1px solid blue;
                                                    padding : 12px;
                                                    }
                                                    
                            QWidget#pageBase {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 250), stop : 1 rgb(0, 0, 100));;
                                            margin : 10px;
                                            border-radius : 10px;
                                            border : none;
                                            padding : 20px;}
                                                    
                            QLabel {color : white}
                            
                            QLabel#pageNumberLabel {color  :rgb(240, 240, 240);
                                                    border : none;
                                                    padding : 5px;
                                                    background : none;
                                                    padding : 5px;}
                                                    
                            QLabel#pageCommentLabel {color : rgb(230, 230,230);
                                                    border : none;
                                                    background : none;
                                                    padding : 5px;}
                            
                            QLabel#pageDateTimeLabel {border : none;
                                                        color : rgb(200, 200, 200);
                                                        background : none;
                                                        padding : 10px;}
                                                        
                            QLabel#keyLabel {border : none;
                                            background : none;
                                            font-family : verdana;
                                            font-size : 21px;
                                            }
                                            
                            QLabel#valueLabel {border : none;
                                            background : none;
                                            font-family : verdana;
                                            font-size : 16px;
                                            }
                                            
                            QLabel#PDFLabel {color : blue;
                                            font-size : 30px;
                                            border : none}
                                            
                            QPushButton#bookmarkAddButton {background-color : blue;
                                                            padding : 5px;
                                                            color : white;
                                                            border : none;
                                                            max-width : 50px;}
                                                            
                            QPushButton#bookmarkAddButton:hover {background-color : rgb(0, 0, 200)}
                            
                            QLabel#bookmarkTitleLabel {background-color : rgb(25, 25, 25);
                                                        padding : 3px;}
                                                        
                            QLabel#bookmarkIndexLabel {background-color : blue;
                                                    color  :white;
                                                    padding : 5px;
                                                    max-width : 60px;
                                                    border : none}
                                                    
                            QLabel#bookmarkPageLabel {background-color : black;
                                                    color  : white;
                                                    border : none;
                                                    border-bottom : 1px solid blue;
                                                    padding : 5px;
                                                    min-width : 50px;}
                                                    
                            QLabel#bookmarkCommentLabel {background-color : rgb(0, 50, 200);
                                                        border : none;
                                                        border-bottom : 1px solid rgb(0, 0, 100);
                                                        padding : 5px;
                                                        min-width : 300px;
                                                        min-height : 35px;
                                                        }
                                                        
                            QLabel#bookmarkDateLabel {background-color : black;
                                                    border : none;
                                                    border-bottom : 1px solid blue;
                                                    padding : 5px;}
                                                    
                            QWidget#bookCommentWidget {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 50), stop : 1 rgb(0, 0, 200));}

"""

dark_theme_for_table = """
                        QLineEdit {border : 1px solid rgb(50, 50, 50);
                                background-color : rgb(10, 10, 10);
                                padding : 5px;
                                border-radius : 0px;
                                margin : 5px;}
                                
                        QLabel {font-size : 15px;}
                        
                        QHeaderView {background-color : rgb(0, 0, 200);
                                    border  : none;
                                    border-right : 1px solid rgb(50, 50, 50)}
                      
                        
                            """

dark_theme_for_pathWidget = """
                            QWidget#pathWidgetBase {background-color : rgb(10, 10, 10);
                                            border : 1px solid rgb(100, 100, 100);
                                            padding : 10px;}
                                            
                            QPushButton#pathWidgetButton {background : none;
                                                border : none;
                                                padding : 10px;
                                                margin : 2px;
                                                font-size : 16px;
                                                }
                            QPushButton#pathWidgetButton:hover , QPushButton#pathWidgetButton:pressed {background-color : rgb(40, 40, 50);}
                            
                            """