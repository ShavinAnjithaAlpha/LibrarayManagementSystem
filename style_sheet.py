
dark_style_sheet = """
                
                QWidget#mainWidget {background-color : rgb(20, 20 ,20)}
                
                QWidget#stageArea {background-color : rgb(30, 30, 30);
                                    border : none}
                
                QScrollArea#mainScrollArea {border : none}
                
                QTabBar::tab {background-color : rgb(240, 0 ,0);
                                                border : none;
                                                padding : 13px;
                                                color : black;
                                                border-right : 1px solid black;
                                                font-size : 15px;
                                                width : 93px}
                QTabBar::tab:selected {background-color : rgb(240, 50, 5);
                                    color : black}
                                    
                QTabWidget#reminderTab::pane {border : 1px solid rgb(50, 50, 50);
                                        border-radius : 5px;
                                        margin : 0px;}
                                                
                QWidget#statusWidget {background-color : rgb(0 ,0, 0);
                                    border : none;
                                    margin : 0px;}
                
                QWidget#barWidget {background-color : rgb(25, 25, 25);
                                    border : none;}
                                    
                QWidget#titleBarWidget {background-color : rgb(20, 20, 35);
                                        border : none;
                                    }
                                    
                QWidget#toolBarWidget {border-bottom : 1px solid rgb(0, 0, 30);
                                        background-color : rgb(25, 25, 25)}
                                    
                QWidget#reminderWidget {background-color : rgb(0, 0, 10);
                                        margin : 0px;}
                                        
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
                                        
                QInputDialog QPushButton {background : none;
                                        color: white;
                                        border : 1px solid rgb(100,100, 100);
                                        border-radius : 2px;
                                        padding : 5px;
                                        font-size : 17px;}
                                        
                     
                QInputDialog QLineEdit {border : 1px solid rgb(100, 100, 100);
                                        border-radius : 5px;
                                        font-size : 16px;
                                        color : white;
                                        padding : 10px;
                                        min-width : 300px;}
                                        
                                
                                         
                QInputDialog QPushButton:hover {background-color : rgb(240, 60, 6);
                                                border : none;
                                                color : black}
                                                
                QPushButton#toolBarHideButton {background : none;
                                                border : none;
                                                font-size : 17px;
                                                color : white;}
                                                
                QPushButton#toolBarHideButton:hover {color : blue} 
                
                QComboBox#sortingComboBox:pane {border-radius : 5px;}
                
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
                                        
                                    QInputDialog QLabel {font-size : 18px;}
                                        
                                    QInputDialog QPushButton {background : none;
                                        color: white;
                                        border : 1px solid rgb(100,100, 100);
                                        border-radius : 2px;
                                        padding : 5px;
                                        font-size : 17px;}
                                        
                                
                                         
                                    QInputDialog QPushButton:hover {background-color : rgb(240, 60, 6);
                                                border : none;
                                                color : black}
                                    
                                    QWidget#collectionBaseWidget {background-color : rgb(10, 10, 10);
                                                                    border : 1px solid rgb(240, 50, 6);
                                                                    border-left : 8px solid rgb(0, 240, 66);
                                                                    border-radius : 5px;}
                                                                    
                                    QWidget#collectionBaseWidgetSelected {background-color : rgb(100, 10, 100);
                                                                    border : 1px solid rgb(240, 50, 6);
                                                                    border-left : 8px solid rgb(0, 240, 66);
                                                                    border-radius : 5px;}
                                                                    
                                   
                                                                    
                                    QWidget#collectionBaseWidget:hover {background-color : rgb(30, 30, 30)}
                                                                    
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
                                    
                                    
                                    
                                    """

status_style_sheet_dark = """
                        
                        QLabel#sepLabel {background-color : rgb(150, 150, 150);
                                        max-height : 2px;
                                        min-height : 2px;
                                        border : none;
                                        }
                                        
                        QLabel#dataLabel  {font-size : 15px;
                                            font-family : Hack;
                                            color : rgb(0, 100, 240);
                                            alignment : right}
                                            
                        QLabel#titleLabel {font-size : 17px;
                                            color : white;
                                            alignment : left}
                                            
                        QLabel {font-size : 16px;
                                alignment : left}
                        
                        """


root_collection_dark_style_sheet = """
                                    QLabel#titleLabel {color : rgb(0, 150, 200);
                                                        font-size : 20px;
                                                        margin : 0px;}
                                                        
                                    QLabel#descriptionLabel {font-size : 16px;}
                                    
                                    
                                    """