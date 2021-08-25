
dark_style_sheet = """
                
                QWidget#mainWidget {background-color : rgb(20, 20 ,20)}
                
                QWidget#stageArea {background-color : rgb(20, 20, 20);
                                    border : none}
                
                QScrollArea#mainScrollArea {border : none}
                
                QTabWidget#reminderTab::tab-bar::tab:clicked {background-color : rgb(200, 50, 50);
                                                border : none}
                                                
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
                                                    background : none}
                                                    
                QRadioButton#searchOptionRadioButton::indicator:checked {background-color : rgb(240, 60, 6);
                                                                        width : 30px;
                                                                        height : 30px;
                                                                        border-radius : 15px;}
                
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
                
                """

dark_style_sheet_for_widgets = """
                                
                                QPushButton#switchButtonLeft, QPushButton#switchButtonRight {background-color : rgb(60, 60, 60);
                                                                                                            color : white;
                                                                                                            font-size : 15px;
                                                                                                            padding : 5px;
                                                                                                            border : none;
                                                                                                    border-radius : 0px;}
                                                                                                    
                                QPushButton#switchButtonLeft:checked, QPushButton#switchButtonRight:checked {background-color : rgb(240, 60, 6);
                                                                                                            color : white;
                                                                                                            padding : 5px;
                                                                                                            border : none;
                                                                                                    border-radius : 0px;}
                                                                                                    
                                QLineEdit#titleEdit {background : none;
                                                    border : 1px solid rgb(100, 100, 100);
                                                    padding : 5px;
                                                    color : white
                                                    }
                                
                                QTextEdit#descriptionEdit {background : none;
                                                            border : 1px solid rgb(100, 100, 100);
                                                            border-radius : 2px;}
                                                            
                                QLineEdit#imageDirEdit {background : none;
                                                        border : 1px solid rgb(100, 100, 100);
                                                        padding : 2px;
                                                        font-size : 12px;}
                                                            
                                QDialog QLabel {font-size : 15px;}
                                
                                QDialog QPushButton {background : none;
                                                            border : 1px solid rgb(100,100, 100);
                                                            border-radius : 2px;
                                                            padding : 3px;
                                                            color : white;
                                                            font-size : 15px;}
                                                            
                                QDialog QPushButton:hover {background-color : rgb(240, 60, 6);
                                                            color : black;}
                                                            
                                
                                """

dark_style_sheet_for_Collection = """
                                    QWidget#collectionBaseWidget {background-color : rgb(10, 10, 10);
                                                                    border : 1px solid rgb(240, 50, 6);
                                                                    border-radius : 5px;}
                                                                    
                                    QWidget#collectionBaseWidget:hover {background-color : rgb(30, 30, 30)}
                                                                    
                                    QLabel#collectionDescriptionLabel {color : rgb(70, 70, 70);
                                                                        alignment : center}
                                                                        
                                    QLabel#collectionTitleLabel {color : rgb(200, 200, 200)}
                                    
                                    QPushButton#favoriteButton:!checked {background : none;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 20px;
                                                                        max-height : 20px;
                                                                        border : 1px solid white;
                                                                        border-radius : 10px;}
                                                                        
                                    QPushButton#favoriteButton:checked {background : white;
                                                                        min-width : 20px;
                                                                        min-height : 20px;
                                                                        max-width : 20px;
                                                                        max-height : 20px;
                                                                        border : 1px solid white;
                                                                        border-radius : 10px;}
                                                                        
                                    QWidget#bookBaseWidget {background-color : rgb(0, 0, 10);
                                                            border : 1px solid rgb(240, 60, 6);
                                                            border-radius : 10px;
                                                            color : white}
                                                            
                                    QLabel#bookTitleLabel {background : none;
                                                            font-size : 15px;
                                                            font-family : verdana;
                                                            color : rgb(200, 0, 150)}
                                                            
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