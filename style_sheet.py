
dark_style_sheet = """

                QMenuBar {background-color : rgb(0, 0, 100);
                            color : white;
                            font-size : 18px;
                            padding : 0px;
                            margin : 0px;}
                            
                QMenuBar::item:hover{background-color : blue;}
                
                QAction::indicator:checked {background-image url(images/sys_images/check_box2.png)}
                
                
                
                QWidget#mainWindowWidget {padding : 0px;
                                        background-image : url(images/sys_images/taskProfile.jpg);}
                                
                QWidget#mainWidget {background-color : rgb(20, 20 ,20);
                                    padding : 0px;}
                
                QWidget#stageArea {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(10, 10, 10), stop : 1 rgb(50, 50, 50));
                                    background-position : center center;
                                    background-image : url(images/sys_images/black_wallpaper.jpg);
                                    border : none;
                                     margin : 0px;}
                
                QScrollArea#mainScrollArea {
                                            border : none;
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
                
                QWidget#rootCollectionTitleWidget {background-image : url(images/sys_images/black_wallpaper.jpg);
                                                    background-position : center center;}
                             
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
                                                                        width  :25px;
                                                                        max-width : 25px;
                                                                        max-height : 25px;
                                                                        min-width : 25px;
                                                                        height : 25px;
                                                                        border-radius : 12px;}
                
                QRadioButton#searchOptionRadioButton::indicator:checked {background-color : rgb(240, 60, 6);
                                                                        width : 25px;
                                                                        height : 25px;
                                                                        border-radius : 12px;}
                
                QGroupBox {border : 1px solid rgb(50, 50, 50);
                            background : none;
                            border-radius : 5px;
                            }
                            
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
                                            
                                            
                QPushButton#backwardButton {border : none;
                                            icon  :url(images/sys_images/backward_icon.png)}
                
                QPushButton#backwardButton:hover:enabled {
                                                        border-radius : 20px;
                                                        icon : url(images/sys_images/backward_hover_icon.png)}
                
                QPushButton#forwardButton {border : none;
                                            icon  :url(images/sys_images/forward_icon.png)}
                
                QPushButton#forwardButton:hover:enabled {
                                                        border-radius : 20px;
                                                        icon : url(images/sys_images/forward_hover_icon.png)}
                                                        
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
                                                icon  :url(images/sys_images/up_arrow.png);
                                                border : none;
                                                font-size : 17px;
                                                color : white;}
                                                
                QPushButton#toolBarHideButton:hover {color : blue;
                                                    icon  :url(images/sys_images/up_arrow_hover.png);}  
                                                    
                QPushButton#toolBarShowButton {background : none;
                                                icon  :url(images/sys_images/down_arrow.png);
                                                border : none;
                                                font-size : 17px;
                                                color : white;}   
                                                
                QPushButton#toolBarShowButton:hover {color : blue;
                                                    icon  :url(images/sys_images/down_arrow_hover.png);} 

                                
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
                QPushButton#collectionToolBarButton:hover {background-color : rgb(40, 40, 40);}
                                                                                                        
                QPushButton#stackChangeButton {icon : url(images/sys_images/right_arrow.png);
                                                border : none;
                                                font-size : 18px;
                                                max-width : 30px;}
                                                
                QPushButton#stackChangeButton:hover {icon : url(images/sys_images/right_arrow_hover.png);}
                
                QPushButton#stackChangeButton:hover {color : blue;}
                
                QPushButton#homeButton {background : none;
                                        icon : url(images/sys_images/homeIcon.png);
                                        border : none;
                                        font-size : 18px;
                                        padding : 5px;
                                        }
                QPushButton#homeButton:hover {icon : url(images/sys_images/homeIconHover.png);}
                
                QPushButton#navigateButton {background : none;
                                            color : white;
                                            text-orientation : vertical;
                                            border : none;
                                            border-right : 2px solid blue;
                                            min-height : 120px;
                                            border-radius : 0px;
                                            margin : 0px;
                                            padding-top : 20px;
                                            font-size : 17px;}
                                            
                QPushButton#navigateButton:checked {background-color : rgb(0, 0, 100);}
                
                QPushButton#barHideButton {background : none;
                                            padding : 5px;
                                            border : none;}
                                              
                
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
                                
                                QDialog  QPushButton {background : none;
                                                            border : 1px solid rgb(100,100, 100);
                                                            border-radius : 2px;
                                                            padding : 3px;
                                                            color : white;
                                                            font-size : 15px;}
                                                            
                                QDialog  QPushButton:hover {background-color : rgb(240, 60, 6);
                                                            color : black;}
                                      
                                QCheckBox {font-size : 15px;}
                                
                                QCheckBox::indicator:checked {background-image : url(images/sys_images/check_box2.png);
                                                            width : 25px;
                                                            height : 25px;
                                                            background-position : center center;
                                                            icon-size : 10px 10px;}  
                                
                                QCheckBox::indicator:!checked {background-image : url(images/sys_images/unchecked_box.png);
                                                                width: 25px;
                                                                height : 25px;}
                                
                                                    
                                
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
                                                            
                                    QWidget#bookBaseWidget:hover {background: QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(100, 0, 0), stop : 0.5 rgb(100, 0, 120) ,stop : 1 rgb(20, 0, 180)); }
                                                            
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
                                    border-top : 1px solid rgb(0, 6, 2);
                                    margin : 0px}
                            
                            QWidget#historyWidget {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 30), stop :0.5 rgb(0, 0, 80) ,stop : 1 rgb(0, 0, 150));
                                                    border : none;
                                                    border-left : 1px solid rgb(0, 0, 2);
                                                    margin : 0px}
                                                    
                            QWidget#historyWidget2 {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 30), stop :0.5 rgb(0, 0, 80) ,stop : 1 rgb(0, 0, 120));;
                                                    border : none;}
                            
                            QWidget#bookmarkWidget {background-color : rgb(40, 40, 240);
                                                    border : 1px solid rgb(0, 0, 2)}
                            
                            
                            QPushButton#pageAddButton {background-color : rgb(40, 40, 40);
                                                        border : none;
                                                        color : white;
                                                        padding : 5px;
                                                        }        
                                                        
                            QPushButton#pageAddButton:hover {
                                                        color : rgb(200, 200,200);
                                                    
                                                        }        
                            
                            QLabel#pageTitleLabel {color  :rgb(0, 200, 250);
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
                                                        color : rgb(220, 220, 220);
                                                        border-bottom : 1px solid black;
                                                        background-color : rgb(50, 50, 50);
                                                        }
                                                        
                            QPushButton#commentAddButton {padding : 10px;
                                                        margin : 0px;
                                                        border : none;
                                                        border-bottom : 1px solid blue;
                                                        background-color : rgb(50, 50, 50)
                                                        }
                                                        
                            QWidget#bookStatusWidget {background-color : rgb(40, 40, 200);
                                                        border-right : 1px solid black;
                                                        border-left : 1px solid black}
                                                        
                            QWidget#pageStatusWidget {background-color  : rgb(30, 30, 30)}
                            
                            QLabel#statusTitleLabel {background : rgb(50, 50, 50);
                                                    border : none;
                                                    margin : 0px;
                                                    color : rgb(230, 230, 230);
                                                    border-bottom : 1px solid black;
                                                    padding : 12px;
                                                    }
                                                    
                            QLabel#pdfLabel {background : none;
                                            font-size : 25px;
                                            color : blue;}
                                                    
                            QWidget#pageBase {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 25), stop : 1 rgb(0, 0, 150));;
                                            margin : 0px;
                                            border-radius : 0px;
                                            border : none;
                                            border : 4px solid rgb(100, 0, 200);
                                            border-left : 4px solid rgb(100, 0, 200);
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
                                                        color : rgb(250, 250, 250);
                                                        background : none;
                                                        font-size : 14px;
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
                            
                            QLabel#bookmarkTitleLabel {background-color : rgb(0, 5, 55);
                                                        padding : 3px;}
                                                        
                            QLabel#bookmarkIndexLabel {background-color : blue;
                                                    color  :white;
                                                    padding : 5px;
                                                    max-width : 60px;
                                                    border : none}
                                                    
                            QPushButton#bookmarkPageLabel {background-color : black;
                                                    color  : white;
                                                    border : none;
                                                    border-bottom : 1px solid blue;
                                                    padding : 5px;
                                                    min-width : 50px;}
                                                    
                            QPushButton#bookmarkPageLabel:hover {background-color : rgb(0, 0, 40);}
                                                    
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
                                                    
                            QWidget#bookCommentWidget {background : QLinearGradient(x1 : 0, y1 : 0, x2 : 1, y2 : 1, stop : 0 rgb(0, 0, 10), stop : 1 rgb(0, 0, 100));}
                            
                            QDialog {font-size : 16px;
                                    color : white;}
                            
                            QDialog QLabel {color : rgb(200, 200, 200);
                                            font-size : 16px;}
                                            
                            QDialog QPushButton {background-color : blue;
                                                padding : 10px;
                                                font-size : 16px;
                                                color : white;
                                                border : none;
                                                width : 60px;
                                                height : 30px;
                                                border-radius : 5px;}
                                                
                            QDialog QPushButton:hover {border : 3px solid blue;
                                                        background-color : rgb(0, 0, 200);}
                                                        
                            QDialog QLineEdit {color : white;
                                                background-color : rgb(50, 50, 50);
                                                padding : 5px;
                                                font-size : 17px;
                                                selection-color : white;}
                                                
                            QDialog QSpinBox {color : white;
                                        font-size : 17px;}
                                                
                            QDialog QTextEdit {font-size : 16px;
                                            background-color  :rgb(50, 50, 50);
                                            color : white;}
                                            
                            QInputDialog QLineEdit {background-color : rgb(50, 50, 50);
                                                margin : 10px;}
                                                
                            QInputDialog QTextBrowser {background-color  :rgb(50, 50, 50)}                            
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

dark_theme_for_task = """
                
                QLabel#imageLabel {background-image : url(images/sys_images/taskProfile.jpg);
                                background-position : center center;
                                font-size : 40px;
                                font-weight : bold;}
                
                QLabel#reminderLabel {color : rgb(200, 200, 200);
                                    font-family : Hack;
                                    font-size : 20px;}

                QWidget#mainWidget {background-color : rgb(30,30, 30);
                                    border-radius : 50px;}
                QLabel {color : white;
                        font-size : 18px;
                        padding : 5px;}
                        
                QPushButton {background-color : red;
                                border : none;
                                padding : 10px;}
                                
                                
                QRadioButton::indicator:!checked {background-image : url(images/sys_images/unchecked_box.png);}
                QRAdioButton::indicator:checked {background-image : url(images/sys_images/check_box2.png);}
                
                QRadioButton#radioButton {color : rgb(200, 200, 200);
                                            background : none;
                                            margin : 10px;
                                            margin-left : 20px;
                                            font-size : 19px;
                                            font-family : Hack}
                
                QLineEdit#newEdit {border : 1px solid rgb(100, 100, 100);
                                    padding : 10ppx;
                                    color : white;
                                    font-size : 18px;
                                    border-radius : 5px;}
                
                QPushButton#navButton {border : none;
                                        background-color : rgb(0, 0, 150);
                                        font-size : 17px;
                                        
                                        }
                                        
                QPushButton#navButton:hover {background-color  :rgb(0, 0, 200);}
                                        
                QPushButton#openButton {background-color : rgb(50, 0, 100);
                                        background-image : url(images/sys_images/close.png);
                                        font-size : 17px;
                                        color : white;}
                                        
                QPushButton#openButton:hover {border : 1px solid rgb(100, 0, 100);
                                                background-color : rgb(150, 0, 200)}
                                        
                QWidget#taskWidget {background-color : rgb(40, 40, 40);
                                        margin : 0px;}
                                        
                QWidget#reminderWidget {background-color : rgb(30, 30, 30)}

"""