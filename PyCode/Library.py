from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import sys
from datetime import datetime
from DBHelper import DBManger

MainUi, _ = loadUiType('UI\\MainWindow.ui')
LoginUi, _ = loadUiType('UI\\login.ui')

DBM = DBManger(r'DB\library.db')
my_date = datetime(2000, 1, 1)


class Main(QMainWindow, MainUi):
    def __init__(self, parent=None) -> None:
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.emp = None
        self.setupUi(self)
        self.UI_changes()
        self.handle_login()
        self.handle_main_system_buttons()
        self.Handle_today_tab()
        self.Handle_books_tab()
        self.Handle_clients_tab()
        self.Handle_history_tab()
        self.Handle_setting_tab()
         
    def handle_login(self):
        self.login_btn.clicked.connect(self.login_action)
        self.reset_password_btn.clicked.connect(self.reset_pass)
 
    def vaildate_login(self, mail, pasw):
        result = DBM.selectStatement('login', f"mail = '{mail}' and password = '{pasw}'", 'id')
        if result:
            return result[0][0]
        else:
            return False
    
    def login_action(self):
        
        mail = self.mail_input.text().strip()
        passw = self.password_input.text().strip()
        if mail and passw:
            if emp_id :=self.vaildate_login(mail, passw):
                result = DBM.selectStatement('employee', f"id = '{emp_id}'", 'id, name, branchid') 
                self.emp = list(result[0])
                self.mail_input.setText("")
                self.password_input.setText("")
                self.system_service.setCurrentIndex(0)
                self.groupBox_6.setEnabled(True)
                self.add_to_hist(' ', 'Login', my_date.now())
                
            else:
                print("incorrect name or pass!") 
        else:
            print("should fill all feild")
      
    def reset_pass(self):
        pass

    def UI_changes(self):
        self.system_service.setCurrentIndex(7)
        self.system_service.tabBar().setVisible(False)
        self.enable_disableupdate_employee()
        self.get_category()
        self.get_branch()
        self.get_location()
        BOOK_STATUS = ('New', 'Used', 'Old')
        self.book_status.addItems(BOOK_STATUS)
        self.get_publisher()
        self.get_author()
        self.get_books()
        self.show_all_clients()
        #self.get_available_books()
        self.get_clients()
        self.cate_today.currentTextChanged.connect(self.get_available_books)
        self.show_dialy_table()
        self.show_history()
        self.get_employee()
        self.hist_branch.currentTextChanged.connect(self.get_branch_emp)

    def get_publisher(self):  # finished(yes but somtimes no)
        self.book_publisher.clear()
        publishers = DBM.selectStatement(
            'publisher', condition=True, columns='name')
        pub_list = []
        for pub in publishers:
            pub_list.append(pub[0])
        self.book_publisher.addItems(pub_list)

    def get_author(self):  # finished(yes but somtimes no)
        self.book_author.clear()
        authors = DBM.selectStatement('author', condition=True, columns='name')
        author_list = []
        for auth in authors:
            author_list.append(auth[0])
        self.book_author.addItems(author_list)

    def get_category(self):  # finished(yes but somtimes no)
        self.cate_parent.clear()
        self.book_category.clear()
        self.all_book_cate.clear()
        self.cate_today.clear()
        categories = DBM.selectStatement(
            'category', condition=True, columns='name')
        cate_list = []
        for cate in categories:
            cate_list.append(cate[0])
        self.cate_parent.addItems(cate_list)
        self.book_category.addItems(cate_list)
        self.all_book_cate.addItems(cate_list)
        self.cate_today.addItems(cate_list)
        self.get_available_books()

    def get_branch(self):
        self.e_emp_branch.clear()
        self.a_emp_branch.clear()
        self.hist_branch.clear()
        branch_info = DBM.selectStatement(
            'branch', condition=True, columns='name')
        branch_list = []
        for branch_name in branch_info:
            branch_list.append(branch_name[0])
        self.a_emp_branch.addItems(branch_list)
        self.e_emp_branch.addItems(branch_list)
        self.hist_branch.addItems(branch_list)

    def get_location(self):
        self.location_list.clear()
        self.location_list_2.clear()
        location_info = DBM.selectStatement(
            'location', condition=True, columns='location')
        loc_list = []
        for loc_name in location_info:
            loc_list.append(loc_name[0])
        self.location_list.addItems(loc_list)
        self.location_list_2.addItems(loc_list)

    def get_books(self):
        self.book_search_list.clear()
        book_info = DBM.selectStatement(
            'book', condition=True, columns='id, title')
        b_list = []
        for book in book_info:
            bbs = f"{book[0]}- {book[1]}"
            if book == (0, ' '):
                bbs = " "
            b_list.append(bbs)
        self.book_search_list.addItems(b_list)

    def show_all_clients(self, data=None):
        self.all_client_table.clearContents()
        self.all_client_table.setRowCount(0)
        result = []
        if data:
            result = data
        else:
            result = DBM.selectStatement('clients', condition=True, columns='*')
        if result:
            for row_i, row_data in enumerate(result):
                if self.all_client_table.rowCount() <= len(result):
                    self.all_client_table.insertRow(row_i)
                for col_i, col_data in enumerate(row_data):
                    self.all_client_table.setItem(
                        row_i, col_i, QTableWidgetItem(str(col_data)))
        else:

            self.all_client_table.clearContents()
            self.all_client_table.setRowCount(0)

    def get_available_books(self):
        self.book_list_today.clear()
        cate = self.cate_today.currentText()
        condition = True
        if cate:
            condition = f"category_id = (SELECT id from category where name = '{cate}')"
        book_info = DBM.selectStatement(
            'book', condition=condition, columns='id, title')
        b_list = []
        for book in book_info:
            bbs = f"{book[0]}- {book[1]}"
            if book == (0, ' '):
                bbs = " "
            b_list.append(bbs)
        self.book_list_today.addItems(b_list)
    
    def get_clients(self):
        self.client_today.clear()
        clients = DBM.selectStatement(
            'clients', condition=True, columns='id, name')
        client_list = []
        for cl in clients:
            bbs = f"{cl[0]}- {cl[1]}"
            if cl == (0, ' '):
                bbs = " "
            client_list.append(bbs)
        self.client_today.addItems(client_list)
             
    def show_dialy_table(self):
        
        self.daily_operation_table.clearContents()
        self.daily_operation_table.setRowCount(0)
        result = []
        dialy_info = DBM.selectStatement('dialymovement', condition=True, columns='*')
        raw_books = DBM.selectStatement('book', True, 'id, code, title,  category_id')
        clients = dict(DBM.selectStatement('clients', True, 'id, name'))
        cate = dict(DBM.selectStatement('category', True, 'id, name'))
        books = dict()
        for book_inf in raw_books:
            books[book_inf[0]] = [book_inf[1], book_inf[2], cate[book_inf[3]]]
        for day in dialy_info:
            code, title, category = books[day[1]]
            day = (code, title, category, clients[day[2]], day[6], day[7], day[3])
            result.append(day)
        if result:
            for row_i, row_data in enumerate(result):
                if self.daily_operation_table.rowCount() <= len(result):
                    self.daily_operation_table.insertRow(row_i)
                for col_i, col_data in enumerate(row_data):
                    self.daily_operation_table.setItem(
                        row_i, col_i, QTableWidgetItem(str(col_data)))
        else:

            self.daily_operation_table.clearContents()
            self.daily_operation_table.setRowCount(0)
            
    def get_branch_emp(self):
        name = self.hist_branch.currentText().strip()
        cond = True
        if name:
            cond = f"branchid in (SELECT id FROM branch WHERE name = '{name}' or name = ' ')"
        self.get_employee(cond)
    def get_employee(self, cond=True):
        self.hist_emp.clear()
        emp_inf = DBM.selectStatement('employee', cond, 'id, name')

        b_list = []
        for emp in emp_inf:
            bbs = f"{emp[0]}- {emp[1]}"
            if emp == (0, ' '):
                bbs = " "
            b_list.append(bbs)
        self.hist_emp.addItems(b_list)
    # *********************************************************
    # ********************************************************************************************
    def handle_main_system_buttons(self):  # finished
        """
        Manage All Buttons in The Left side that switches the Screan or the main tab widget
        called 'system_service'
        """
        self.dialy_service.clicked.connect(self.open_today_tab)
        self.book_service.clicked.connect(self.open_book_tab)
        self.client_service.clicked.connect(self.open_client_tab)
        self.dashboard_service.clicked.connect(self.open_dashboard_tab)
        self.history_service.clicked.connect(self.open_history_tab)
        self.report_service.clicked.connect(self.open_report_tab)
        self.setting_service.clicked.connect(self.open_setting_tab)
        self.logout_btn.clicked.connect(self.logout_action)
        self.setting_service_operation.setCurrentIndex(0)

    def logout_action(self):
        self.system_service.setCurrentIndex(7)
        self.add_to_hist(' ', 'Logout', my_date.now())
        self.groupBox_6.setEnabled(False)
    def open_today_tab(self):  # finished
        self.system_service.setCurrentIndex(0)

    def open_book_tab(self):  # finished
        self.system_service.setCurrentIndex(1)
        self.book_service_operation.setCurrentIndex(0)

    def open_client_tab(self):  # finished
        self.system_service.setCurrentIndex(2)

    def open_dashboard_tab(self):  # finished
        self.system_service.setCurrentIndex(3)

    def open_history_tab(self):  # finished
        self.system_service.setCurrentIndex(4)

    def open_report_tab(self):  # finished
        self.system_service.setCurrentIndex(5)
        self.report_service_operation.setCurrentIndex(0)

    def open_setting_tab(self):  # finished
        self.system_service.setCurrentIndex(6)
        self.setting_service_operation.setCurrentIndex(0)
    # *********************************************************
    # ********************************************************************************************

    # *******************************************************************************************
    # ********************************************************************************************

    def Handle_today_tab(self):
        self.add_operation_today_btn.clicked.connect(self.add_today_action)
    
    def add_today_action(self):
        #cate = self.cate_today.currentText()
        book_inf = tuple(map(str.strip, self.book_list_today.currentText().split('-')))
        client_inf = tuple(map(str.strip,self.client_today.currentText().split('-')))
        op = self.operation_today.currentText()
        from_date = self.from_date_today.date().toString('d-M-yyyy')
        to_date = self.to_date_today.date().toString('d-M-yyyy')
        emp_id = 0
        branch_id = 0
        add_date = my_date.now()
        if len(book_inf) > 1 and len(client_inf) > 1:
            book_id, title = book_inf
            c_id, c_name = client_inf
            operation_id = DBM.insertStatement('dialymovement', book_id=f"'{book_id}'", client_id=f"'{c_id}'", 
                                operation=f"'{op}'", branch_id=f"'{branch_id}'", date=f"'{add_date}'", 
                                from_date=f"'{from_date}'", to_date=f"'{to_date}'", employee_id=f"'{emp_id}'")
            self.show_dialy_table()
            self.add_to_hist('DailyMovement', 'Add', add_date)
        else:
            print("choose book and user")
        
        
    # *******************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************

    def Handle_books_tab(self):
        self.all_books_tab()
        self.add_del_update_books_tab()

    def all_books_tab(self):
        self.get_all_books_info_base_category()
        self.all_book_serach_btn.clicked.connect(self.show_all_books)

    def get_all_books_info_base_category(self, category=False, book_code=False):
        self.all_book_table.clearContents()
        self.all_book_table.setRowCount(0)
        search_condition = True
        cate_id = True
        cate_info = []
        if bool(category) and bool(book_code):
            search_condition = f"name = '{category}'"
            cate_info = dict(DBM.selectStatement(
                'category', search_condition, 'id, name'))
            cate_id = f"category_id = {list(cate_info.keys())[0]} and code = '{book_code}'"

        elif bool(category) and not bool(book_code):
            search_condition = f"name = '{category}'"
            cate_info = dict(DBM.selectStatement(
                'category', search_condition, 'id, name'))
            cate_id = f"category_id = '{list(cate_info.keys())[0]}'"
        elif not bool(category) and bool(book_code):
            cate_info = dict(DBM.selectStatement(
                'category', search_condition, 'id, name'))
            cate_id = f"code = '{book_code}'"
        else:
            cate_info = dict(DBM.selectStatement(
                'category', search_condition, 'id, name'))

        b_info = DBM.selectStatement(
            'book', cate_id, 'code, title, publisher_id, author_id, price, category_id, date')
        if b_info:
            pub_info = dict(DBM.selectStatement('publisher', True, 'id, name'))
            autor_info = dict(DBM.selectStatement('author', True, 'id, name'))

            for row_i, b in enumerate(b_info):
                row_data = (b[0], b[1], pub_info[b[2]],
                            autor_info[b[3]], b[4], cate_info[b[5]], b[6])
                if self.all_book_table.rowCount() <= len(b_info):
                    self.all_book_table.insertRow(row_i)
                for col_i, col_data in enumerate(row_data):
                    self.all_book_table.setItem(
                        row_i, col_i, QTableWidgetItem(str(col_data)))
        else:
            self.all_book_table.clearContents()
            self.all_book_table.setRowCount(0)

    def show_all_books(self):
        cate_str = self.all_book_cate.currentText().strip()
        book_code = self.all_book_code.text().strip()

        self.get_all_books_info_base_category(cate_str, book_code)

    # ********************************************************************************************

    def get_book_info(self):

        title = self.book_title.text().strip()
        code = self.book_code.text().strip()
        desc = self.book_description.toPlainText().strip()
        cate = self.book_category.currentText().strip()
        status = self.book_status.currentText().strip()
        publisher = self.book_publisher.currentText().strip()
        author = self.book_author.currentText().strip()
        price = self.book_price.text().strip()
        part_num = self.book_part.text().strip()
        image_path = ''
        return title, code, desc, cate, status, publisher, author, price, part_num, image_path

    def add_del_update_books_tab(self):
        self.book_add_btn.clicked.connect(self.add_book_info)
        self.book_update_btn.clicked.connect(self.update_book_info)
        self.book_delete_btn.clicked.connect(self.delete_book_info)
        self.book_search_btn.clicked.connect(self.search_book_info)

    def add_book_info(self):
        title, code, desc, cate, status, publisher, author, price, part_num, image_path = self.get_book_info()
        cate_id = author_id = publisher_id = 0
        if cate:
            rs1 = DBM.selectStatement('category', f"name = '{cate}'", 'id')
            cate_id = rs1[0][0]
        if author:
            rs2 = DBM.selectStatement('author', f"name = '{author}'", 'id')
            author_id = rs2[0][0]
        if publisher:
            rs3 = DBM.selectStatement(
                'publisher', f"name = '{publisher}'", 'id')
            publisher_id = rs3[0][0]

        if not title or not desc:
            print("fill all nessery feilds")
        else:
            # today = date.today()
            # dd/mm/YY
            # t_date = today.strftime("%d/%m/%Y")
            t_date = my_date.now()

            book_id = DBM.insertStatement('book', title=f"'{title}'", code=f"'{code}'",
                                          description=f"'{desc}'", category_id=f"'{cate_id}'",
                                          part_order=f"'{part_num}'", publisher_id=f"'{publisher_id}'",
                                          author_id=f"'{author_id}'", price=f"'{price}'",
                                          status=f"'{status}'", image=f"'{image_path}'", date=f"'{t_date}'")
            self.get_books()
            self.get_all_books_info_base_category()
            self.add_to_hist('Books', 'Add', t_date)

    def update_book_info(self):
        book_str = self.book_search_list.currentText().strip()
        if book_str:
            id, title = map(str.strip, book_str.split('-'))
            title, code, desc, cate, status, publisher, author, price, part_num, image_path = self.get_book_info()
            cate_id = author_id = publisher_id = 0

            if cate:
                rs1 = DBM.selectStatement('category', f"name = '{cate}'", 'id')
                cate_id = rs1[0][0]
            if author:
                rs2 = DBM.selectStatement('author', f"name = '{author}'", 'id')
                author_id = rs2[0][0]
            if publisher:
                rs3 = DBM.selectStatement(
                    'publisher', f"name = '{publisher}'", 'id')
                publisher_id = rs3[0][0]
            if not title or not desc:
                print("fill all nessery feilds")
            else:
                DBM.updateStatement('book', f"id = '{id}'", title=f"'{title}'", code=f"'{code}'",
                                            description=f"'{desc}'", category_id=f"'{cate_id}'",
                                            part_order=f"'{part_num}'", publisher_id=f"'{publisher_id}'",
                                            author_id=f"'{author_id}'", price=f"'{price}'",
                                            status=f"'{status}'", image=f"'{image_path}'",)
                self.get_books()
                self.get_all_books_info_base_category()
                self.add_to_hist('Books', 'Update', my_date.now())

        else:
            print("should select book")

    def delete_book_info(self):
        book_str = self.book_search_list.currentText().strip()
        if book_str:
            id, title = map(str.strip, book_str.split('-'))
            DBM.deleteStatement('book', f"id = '{id}'")
            self.book_title.setText("")
            self.book_code.setText("")
            self.book_description.setPlainText("")

            self.book_category.setCurrentText(' ')
            self.book_publisher.setCurrentText(" ")
            self.book_author.setCurrentText(" ")
            self.book_price.setValue(0000.0000)
            self.book_part.setValue(0)
            self.get_books()
            self.get_all_books_info_base_category()
            self.add_to_hist('Books', 'Delete', my_date.now())
        else:
            print("should select book")

    def search_book_info(self):

        book_str = self.book_search_list.currentText().strip()
        if not book_str:
            self.book_title.setText("")
            self.book_code.setText("")
            self.book_description.setPlainText("")
            self.book_category.setCurrentText(" ")
            self.book_publisher.setCurrentText(" ")
            self.book_author.setCurrentText(" ")
            self.book_price.setValue(0000.0000)
            self.book_part.setValue(0)
        else:

            id, title = map(str.strip, book_str.split('-'))
            info = DBM.selectStatement('book', f"id = '{id}'", '*')
            if info:
                id, title, desc, cate_id, code, part_num, price, pub_id, author_id, img_path, status, b_date = info[
                    0]

                cate_name = author_name = publisher_name = ' '

                if cate_id:
                    rs1 = DBM.selectStatement(
                        'category', f"id = '{cate_id}'", 'name')
                    cate_name = rs1[0][0]

                if author_id:
                    rs2 = DBM.selectStatement(
                        'author', f"id = '{author_id}'", 'name')
                    author_name = rs2[0][0]

                if pub_id:
                    rs3 = DBM.selectStatement(
                        'publisher', f"id = '{pub_id}'", 'name')
                    publisher_name = rs3[0][0]

                self.book_title.setText(title)
                self.book_code.setText(code)
                self.book_description.setPlainText(desc)
                self.book_category.setCurrentText(cate_name)
                self.book_status.setCurrentText(status)
                self.book_publisher.setCurrentText(publisher_name)
                self.book_author.setCurrentText(author_name)
                self.book_price.setValue(price)
                self.book_part.setValue(part_num)

            else:
                print("no such book")

    # ********************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************

    def Handle_clients_tab(self):
        self.search_client_btn.clicked.connect(self.serach_clients)
        self.add_client_btn.clicked.connect(self.add_clients_action)
        self.update_client_btn.clicked.connect(self.update_clients_action)
        self.delete_client_btn.clicked.connect(self.delete_clients_action)

    def get_client_info(self):

        name = self.client_name.text().strip()
        mail = self.client_mail.text().strip()
        phone = self.client_phone.text().strip()
        nid = self.client_nid.text().strip()

        return name, mail, phone, nid

    def serach_clients(self):
        name, mail, phone, nid = self.get_client_info()
        search_based = self.search_by.currentIndex()
        # 1 = name
        # 2 = National id
        # 3 = phone
        condition = True
        if search_based == 1:
            condition = f"name = '{name}'"
        elif search_based == 2:
            condition = f"nat_id = '{nid}'"
        elif search_based == 3:
            condition = f"phone = '{phone}'"
            
        result = DBM.selectStatement('clients', condition, '*')
        if result:
            self.show_all_clients(result)
        else:
            self.all_client_table.clearContents()


    def add_clients_action(self):
        name, mail, phone, nid = self.get_client_info()
        if mail and nid:
            
            c_date = my_date.now()
            nid_exist = DBM.selectStatement('clients', f"nat_id = '{nid}'", 'id')
            print(nid_exist)
            if not bool(nid_exist):
                c_id = DBM.insertStatement('clients', nat_id=f"'{nid}'", name=f"'{name}'",
                                        mail=f"'{mail}'", phone=f"'{phone}'", date=f"'{c_date}'")

                self.add_to_hist('Clients', 'Add', c_date)
                row_i = self.all_client_table.rowCount()
                self.all_client_table.insertRow(row_i)
                for col_i, col_data in enumerate([c_id, name, mail, phone, nid, c_date]):
                    self.all_client_table.setItem(
                        row_i, col_i, QTableWidgetItem(str(col_data)))
                    
            else:
                print("National id are exist!")
        else:
            print("fill all nesecry feild")

    def update_clients_action(self):
        name, mail, phone, nid = self.get_client_info()
        if name and mail and phone and nid:
            nid_exist = DBM.selectStatement('clients', f"nat_id = '{nid}'", 'id')
            if nid_exist:
                DBM.updateStatement('clients', f"nat_id = '{nid}'", nat_id=f"'{nid}'", name=f"'{name}'",
                                            mail=f"'{mail}'", phone=f"'{phone}'")
                self.show_all_clients()
                self.add_to_hist('Clients', 'Update', my_date.now())
            else:
                print("no such user:", name)
        else:
            print("fill all feilds!")

    def delete_clients_action(self):
        name, mail, phone, nid = self.get_client_info()
        if nid:
            DBM.deleteStatement('clients', f"nat_id = '{nid}'", nat_id=f"'{nid}'")
            self.show_all_clients()
            self.add_to_hist('Clients', 'Delete', my_date.now())
        else:
            print("no client to delete!")

    # ********************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************

    def Handle_dashBoard_tab(self):
        pass
    # ********************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************

    def Handle_history_tab(self):
        self.search_hist_btn.clicked.connect(self.hist_action)
    
    def show_history(self, branch="", emp="", tab="", action=""):
        self.hist_table.clearContents()
        self.hist_table.setRowCount(0)
        
        branch_info = dict(DBM.selectStatement('branch', True, 'id, name'))
        for id, name in branch_info.items():
            if name == branch:
                branch = id
                break
        
         
        emp_condition = True
        argue = [branch, emp, tab, action]
        
        ddddd = {
            0: ("branch_id ="),
            1: ("employee_id ="),
            2: ("tabl ="),
            3: ("action =")
                
            
        }
        try:
            if not emp == "":
                emp, _ = map(str.strip, emp.split('-'))
                argue[1] = emp
                emp_condition = f"id = '{emp}'"
            for tt, arr in zip(ddddd.items(),argue):
                i, val = tt
                if not arr == "":
                    argue[i] = f"{val} '{arr}'"
                else:
                    argue[i] = f"True"
        except Exception as e:
            print(e)
        search_condition = " and ".join(argue)
        print("====",search_condition)
        
        hist_info = DBM.selectStatement('history', search_condition, '*')
        
        if hist_info:
            emp_info = dict(DBM.selectStatement('employee', emp_condition, 'id, name'))

            for row_i, inf in enumerate(hist_info):
                if self.hist_table.rowCount() <= len(hist_info):
                    self.hist_table.insertRow(row_i)
                row_data = [branch_info[inf[5]], emp_info[inf[1]], inf[3], inf[2], inf[4]]
                for col_i, col_data in enumerate(row_data):
                    self.hist_table.setItem(row_i, col_i, QTableWidgetItem(str(col_data)))
        else:
            self.hist_table.clearContents()
            self.hist_table.setRowCount(0)
    
    def add_to_hist(self, table, action, date):
        try:
            DBM.insertStatement('history', employee_id=f"'{self.emp[0]}'" , action=f"'{action}'",
                                tabl=f"'{table}'", date=f"'{str(date)}'", branch_id=f"'{self.emp[2]}'")
        except Exception as e:
            print(e)
        self.show_history()
    
    def hist_action(self):
        branch = self.hist_branch.currentText().strip()
        emp = self.hist_emp.currentText().strip()
        tab = self.hist_tab.currentText().strip()
        action = self.hist_ac.currentText().strip()
        self.show_history(branch, emp, tab, action)
        
        
    
    # ********************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************

    def Handle_report_tab(self):
        self.handle_books_report_tab()
        self.handle_clients_report_tab()
        self.handle_monthly_report_tab()
        pass

    def handle_books_report_tab(self):
        pass
    # ********************************************************************************************

    def handle_clients_report_tab(self):
        pass
    # ********************************************************************************************

    def handle_monthly_report_tab(self):
        pass

    # ********************************************************************************************
    # ********************************************************************************************

    # ********************************************************************************************
    # ********************************************************************************************
    def Handle_setting_tab(self):  # finished(yes but somtimes no)
        """
        """
        self.handle_add_data()
        self.handle_employee_setting()
        self.handle_permission()

    def handle_add_data(self):  # finished
        self.add_branch_btn.clicked.connect(self.add_branch_action)
        self.add_publisher_btn.clicked.connect(self.add_publisher_action)
        self.add_author_btn.clicked.connect(self.add_author_action)
        self.add_cate_btn.clicked.connect(self.add_category_action)

    def add_branch_action(self):  # finished(yes but somtimes no)
        name = self.add_branch_name.text()
        code = self.add_branch_code.text()
        location = self.add_branch_loc.text().strip()
        selected_location = str(self.location_list_2.currentText())
        location_info = DBM.selectStatement(
              'location', condition=True, columns='location')
        loc_list = []
        for loc_name in location_info:
            loc_list.append(loc_name[0])
        if not location and not selected_location:
            print("should add location")
        else:
            location_id = 0
            if location in loc_list or (selected_location and not location):
                if not location:
                    location = selected_location
                result = DBM.selectStatement(
                    'location', f"location = '{location}'", 'id')
                location_id = result[0][0]
            else:
                location_id = DBM.insertStatement(
                    'location', location=f"'{location}'")
                self.get_location()
                self.add_to_hist('Location', 'Add', my_date.now())
            branch_id = DBM.insertStatement(
                'branch', name=f"'{name}'", code=f"'{code}'", location_id=f"'{location_id}'")
            self.get_branch()
            self.add_to_hist('Branch', 'Add', my_date.now())

            print(branch_id)

    def add_publisher_action(self):  # finished(yes but somtimes no)
        name = self.add_pub_name.text().strip()
        location = self.add_pub_loc.text().strip()
        selected_location = str(self.location_list.currentText()).strip()
        location_info = DBM.selectStatement(
            'location', condition=True, columns='location')
        loc_list = []
        for loc_name in location_info:
            loc_list.append(loc_name[0])
        if not location and not selected_location:
            print("should add location")
        else:
            location_id = 0
            if location in loc_list or (selected_location and not location):
                if not location:
                    location = selected_location
                result = DBM.selectStatement(
                    'location', f"location = '{location}'", 'id')
                location_id = result[0][0]
            else:
                location_id = DBM.insertStatement(
                    'location', location=f"'{location}'")
                self.get_location()
                self.add_to_hist('Location', 'Add', my_date.now())

            publisher_id = DBM.insertStatement(
                'publisher', name=f"'{name}'", location_id=f"'{location_id}'")
            self.get_publisher()
            self.add_to_hist('Publisher', 'Add', my_date.now())

    def add_author_action(self):  # finished(yes but somtimes no)
        name = self.add_author_name.text()
        mail = self.add_author_mail.text()
        if name and mail:
            author_id = DBM.insertStatement(
                'author', name=f"'{name}'", mail=f"'{mail}'")
            self.get_author()
            self.add_to_hist('Author', 'Add', my_date.now())

    def add_category_action(self):  # finished(yes but somtimes no)
        name = self.add_cate_name.text()
        parent_name = str(self.cate_parent.currentText()).strip()
        parent_id = 0
        if parent_name:
            result = DBM.selectStatement(
                "category", condition=f"name = '{parent_name}'", columns='id')
            parent_id = result[0][0]

        cate_id = DBM.insertStatement(
            'category', name=f"'{name}'", parent=f"'{parent_id}'")
        self.add_to_hist('Category', 'Add', my_date.now())

        self.get_category()

    # ********************************************************************************************
    def handle_employee_setting(self):
        """
        """
        self.emp_add_btn.clicked.connect(self.add_employee_action)
        self.c_emp_check_btn.clicked.connect(self.validate_login)
        self.emp_update_btn.clicked.connect(self.edit_employee_action)

    def add_employee_action(self):
        name = self.a_emp_name.text().strip()
        mail = self.a_emp_mail.text().strip()
        phone = self.a_emp_phone.text().strip()
        branch = str(self.a_emp_branch.currentText())
        nid = self.a_emp_nid.text().strip()
        password = self.a_emp_pass.text().strip()
        cPassword = self.a_emp_cpass.text().strip()

        if name and nid and password and cPassword:
            if password == cPassword:

                # today = date.today()
                # dd/mm/YY
                # emp_date = today.strftime("%d/%m/%Y")
                emp_date = my_date.now()
                
                branch_info = DBM.selectStatement(
                    'branch', condition=f'name = "{branch}"', columns='id')
                emp_id = DBM.insertStatement(
                    'employee', nat_id=str(nid), name=f"'{name}'", phone=str(phone), date=f"'{emp_date}'", branchid=str(branch_info[0][0]))
                login_id = DBM.insertStatement(
                    'login', id=f"'{emp_id}'", mail=f"'{mail}'", password=f"'{password}'")
                print(branch_info, emp_id)
                self.add_to_hist('Employee', 'Add', emp_date)
                self.a_emp_name.setText("")
                self.a_emp_mail.setText("")
                self.a_emp_phone.setText("")
                self.a_emp_nid.setText("")
                self.a_emp_pass.setText("")
                self.a_emp_cpass.setText("")

    def enable_disableupdate_employee(self, option=False):
        self.e_emp_name.setEnabled(option)
        self.e_emp_mail.setEnabled(option)
        self.e_emp_phone.setEnabled(option)
        self.e_emp_nid.setEnabled(option)
        self.e_emp_pass.setEnabled(option)
        self.e_emp_cpass.setEnabled(option)
        self.e_emp_branch.setEnabled(option)
        self.emp_update_btn.setEnabled(option)

    def validate_login(self):

        mail = self.c_emp_mail.text().strip()
        password = self.c_emp_pass.text().strip()
        if mail and password:
            id = DBM.selectStatement(
                'login', condition=f"mail = '{mail}' and password = '{password}'", columns='id')

            if id:
                self.enable_disableupdate_employee(True)
                result = DBM.selectStatement(
                    'employee', condition=f'loginid = {id[0][0]}', columns='nat_id, name, phone, branchid')
                nid, name, phone, branch_id = result[0]
                branch_info = DBM.selectStatement(
                    'branch', condition=f'id = {branch_id}', columns='name')
                self.e_emp_name.setText(name)
                self.e_emp_mail.setText(mail)
                self.e_emp_phone.setText(phone)
                self.e_emp_nid.setText(str(nid))
                self.e_emp_branch.setCurrentText(branch_info[0][0])
            else:
                print('invalid mail or password')
                self.enable_disableupdate_employee()
                self.e_emp_name.setText('')
                self.e_emp_mail.setText('')
                self.e_emp_phone.setText('')
                self.e_emp_nid.setText('')
                self.e_emp_pass.setText('')
                self.e_emp_cpass.setText('')
                self.e_emp_branch.setCurrentText('')
        else:
            print("empty mail or password")

    def edit_employee_action(self):
        old_mail = self.c_emp_mail.text().strip()
        old_password = self.c_emp_pass.text().strip()
        name = self.e_emp_name.text().strip()
        mail = self.e_emp_mail.text().strip()
        phone = self.e_emp_phone.text().strip()
        nid = self.e_emp_nid.text().strip()
        branch_name = str(self.e_emp_branch.currentText())
        password = self.e_emp_pass.text().strip()
        cPassword = self.e_emp_cpass.text().strip()
        if name and nid and password and cPassword:
            if password == cPassword:
                id = DBM.selectStatement(
                    'login', condition=f"mail = '{old_mail}' and password = '{old_password}'", columns='id')
                print(id)

                if id:
                    DBM.updateStatement(
                        'login', condition=f"id = {id[0][0]}", mail=f"'{mail}'", password=f"'{password}'")
                    branch_id = DBM.selectStatement(
                        'branch', condition=f"name = '{branch_name}'", columns='id')
                    DBM.updateStatement(
                        'employee', condition=f'loginid = {id[0][0]}', nat_id=nid, name=f"'{name}'", phone=f"'{phone}'", branchid=branch_id[0][0])
                    self.add_to_hist('Employee', 'Update', my_date.now())
            else:
                print("passsword not match")
        else:
            print('empty feild!')

    # ********************************************************************************************
    def handle_permission(self):
        pass
    # ********************************************************************************************
    # ********************************************************************************************





def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
