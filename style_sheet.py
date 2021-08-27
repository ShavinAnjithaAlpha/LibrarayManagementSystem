
dark_style_sheet = """
                
                QWidget#mainWidget {background-color : rgb(20, 20 ,20)}
                
                QWidget#stageArea {background-color : rgb(20, 20, 20);
                                    border : none}
                
                QScrollArea#mainScrollArea {border : none}
                
                QTabBar::tab {background-color : rgb(240, 0 ,0);
                                                border : none;
                                                padding : 10px;
                                                color : black;
                                                border-right : 1px solid black;
                                                font-size : 15px;
                                                width : 80px}
                QTabBar::tab:selected {background-color : rgb(240, 50, 5);
                                    color : black}
                                    
                QTabWidget#reminderTab::pane {border : 1px solid rgb(50, 50, 50);
                                        border-radius : 5px;}
                                                
                QWidget#statusWidget {background-color : rgb(0 ,0, 0);
                                    border : none}
                
                QWidget#barWidget {background-color : rgb(25, 25, 25);
                                    border : none;}
                                    
                QWidget#titleBarWidget {background-color : rgb(20, 20, 35);
                                        border : none;
                                    }
                                    
                QWidget#toolBarWidget {border-bottom : 1px solid rgb(0, 0, 30);
                                        background-color : rgb(25, 25, 25)}
                                    
                QWidget#reminderWidget {background-color : rgb(0, 0, 10)}
                                        
                QLabel#title_label {color : rgb(0, 50, 200);
                                    background : none;}
                                    
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
                                            background-color: rgb(240, 60, 6);
                                            border : none;
                                            padding : 10px;
                                            font-size : 18px;}
                                            
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
                                                                font-size : 16px;
                                                                padding : 5px;
                                                                border : none;
                                                                border-top-right-radius : 10px;
                                                                border-bottom-right-radius : 10px;
                                                                border-top-left-radius : 0px;
                                                                border-bottom-left-radius : 0px;}
                                                                                                    
                                QPushButton#switchButtonLeft:checked, QPushButton#switchButtonRight:checked {background-color : rgb(240, 60, 6);
                                                                                                                color  : black;
                                                                                                                font-weight : bold}
                                                                                                    
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
                                    QWidget#collectionBaseWidget {background-color : rgb(10, 10, 10);
                                                                    border : 1px solid rgb(240, 50, 6);
                                                                    border-radius : 5px;}
                                                                    
                                    QWidget#collectionBaseWidget:hover {background-color : rgb(30, 30, 30)}
                                                                    
                                    QLabel#collectionDescriptionLabel {color : rgb(70, 70, 70);
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
                                                            border : 1px solid rgb(240, 60, 6);
                                                            border-radius : 10px;
                                                            color : white}
                                                            
                                    QLabel#bookTitleLabel {background : none;
                                                            font-family : verdana;
                                                            font-size : 16px;
                                                            color : rgb(200, 200, 200)}
                                                            
                                    QPushButton#bookFavoriteButton:!checked {background : none;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 20px;
                                                                        max-height : 20px;
                                                                        border : 1px solid white;
                                                                        border-radius : 10px;}
                                                                        
                                    QPushButton#bookFavoriteButton:checked {background : white;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 20px;
                                                                        max-height : 20px;
                                                                        border : 1px solid white;
                                                                        border-radius : 10px;}
                                    
                                    """