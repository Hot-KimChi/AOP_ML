def func_viewer_database():
    try:
        global iteration
        iteration = 0

        def func_1st_load():
            try:

                def func_tree_update(df=None, selected_input=None):
                    try:

                        ## tree table안에 있는 데이터를 선택해서 제일 앞에 있는 데이터를 (x1, x2, x3) 형태로 변수 update.
                        def func_click_item(event):
                            ## multiple selection
                            global sel_param_click, str_sel_param
                            selectedItem = my_tree.selection()

                            # 딕셔너리의 값 중에서 제일 앞에 있는 element 값 추출. ex) measSSId 추출.
                            # sel_param_click = my_tree.item(selectedItem).get('values')[0]
                            sel_param_click = []
                            for i in selectedItem:
                                sel_param_click.append(my_tree.item(i).get('values')[0])
                            str_sel_param = '(' + ','.join(str(x) for x in sel_param_click) + ')'

                        # tree_scroll_y = Scrollbar(frame2, orient="vertical")
                        # tree_scroll_y.pack(side=RIGHT, fill=Y)
                        # tree_scroll_x = Scrollbar(frame2, orient="horizontal")
                        # tree_scroll_x.pack(side=BOTTOM, fill=X)

                        if iteration == 1 and selected_input == None:
                            global my_tree, tree_scroll_y, tree_scroll_x
                            tree_scroll_y = Scrollbar(frame2, orient="vertical")
                            tree_scroll_y.pack(side=RIGHT, fill=Y)
                            tree_scroll_x = Scrollbar(frame2, orient="horizontal")
                            tree_scroll_x.pack(side=BOTTOM, fill=X)

                            my_tree = ttk.Treeview(frame2, height=20, yscrollcommand=tree_scroll_y.set,
                                                   xscrollcommand=tree_scroll_x.set, selectmode="extended")
                            my_tree.pack(padx=20, pady=20, side='left')
                        else:
                            my_tree.destroy()
                            tree_scroll_y.destroy()
                            tree_scroll_x.destroy()

                            tree_scroll_y = Scrollbar(frame2, orient="vertical")
                            tree_scroll_y.pack(side=RIGHT, fill=Y)
                            tree_scroll_x = Scrollbar(frame2, orient="horizontal")
                            tree_scroll_x.pack(side=BOTTOM, fill=X)

                            my_tree = ttk.Treeview(frame2, height=20, yscrollcommand=tree_scroll_y.set,
                                                   xscrollcommand=tree_scroll_x.set, selectmode="extended")
                            my_tree.pack(padx=20, pady=20, side='left')
                            # for i in my_tree.get_children():
                            #     my_tree.delete(i)


                        # event update시, func_click_item 수행.
                        my_tree.bind('<ButtonRelease-1>', func_click_item)

                        tree_scroll_y.config(command=my_tree.yview)
                        tree_scroll_x.config(command=my_tree.xview)

                        my_tree["column"] = list(df.columns)
                        my_tree["show"] = "headings"

                        # Loop thru column list for headers
                        for column in my_tree["column"]:
                            my_tree.column(column, width=100, minwidth=100)
                            my_tree.heading(column, text=column)

                        my_tree.tag_configure('oddrow', background="lightblue")
                        my_tree.tag_configure('evenrow', background="white")

                        # Put data in treeview
                        df_rows = df.round(3)
                        df_rows = df_rows.to_numpy().tolist()

                        global count
                        count = 0
                        for row in df_rows:
                            if count % 2 == 0:
                                my_tree.insert(parent='', index='end', iid=count, text="", values=row,
                                               tags=('evenrow',))
                            else:
                                my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
                            count += 1

                    except():
                        print("Error: func_tree_update")


                global selected_probeId, selected_DBtable, selected_probename, iteration   #, combo_SSId, combo_probesn

                iteration += 1
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])
                selected_DBtable = combo_DBtable.get()

                ## selected_probeId에 선택 & 선택된 DBtable에서 데이터 가져오기.
                df = func_sql_get(server_address, ID, password, database, 0)

                ''' 선택한 table treeview update'''
                func_tree_update(df)

                ''' parameter list from SQL table '''
                list_params = df.columns.values.tolist()

                ''' SQL DB에서 받은 데이터의 선택된 column(ex: meas_person_name)에서 선택된 datas(HIS, others)를 추출하는 algorithm'''
                def func_on_selected(event):

                    def func_sel_update(event):
                        global sel_data
                        sel_data = combo_sel_datas.get()
                        table = func_sql_get(server_address, ID, password, database, 3)
                        func_tree_update(df=table, selected_input=sel_data)

                    global selected_param
                    # parameter 중 한개를 선정하게 되면 filter 기능.
                    selected_param = event.widget.get()
                    list_datas = df[f'{selected_param}'].values.tolist()
                    # list에서 unique한 데이터를 추출하기 위해 set으로 변경하여 고유값으로 변경 후, 다시 list로 변경.
                    set_datas = set(list_datas)
                    filtered_datas = list(set_datas)

                    label_sel_data = Label(frame2, text='Selection')
                    label_sel_data.place(x=5, y=25)

                    combo_sel_datas = ttk.Combobox(frame2, value=filtered_datas, height=0, state='readonly')
                    combo_sel_datas.place(x=115, y=25)
                    combo_sel_datas.bind('<<ComboboxSelected>>', func_sel_update)


                ''' 선택된 columns을 combobox형태로 생성 & binding event통해 선택 시, func_on_selected 실행.'''
                label_filter = Label(frame2, text='filter Column')
                label_filter.place(x=5, y=5)

                combo_list_columns = ttk.Combobox(frame2, value=list_params, height=0, state='readonly')
                combo_list_columns.place(x=115, y=5)
                combo_list_columns.bind('<<ComboboxSelected>>', func_on_selected)

                btn_view = Button(frame2, width=15, height=2, text='Select & View', command=func_select_view)
                btn_view.place(x=350, y=5)


            except():
                print("Error: func_1st_load")


        def func_select_view():
            try:
                global selected_probeId, selected_DBtable, selected_probename
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])
                selected_DBtable = combo_DBtable.get()

                df = func_sql_get(server_address, ID, password, database, 2)
                func_show_table(selected_DBtable, df=df)

            except():
                print("Error: func_select_view")


        root_view = tkinter.Toplevel()
        root_view.title(f"{database}" + ' / Viewer')
        root_view.geometry("1720x800")
        root_view.resizable(False, False)

        frame1 = Frame(root_view, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)
        frame2 = Frame(root_view, relief="solid", bd=2)
        frame2.pack(side="bottom", fill="both", expand=True)

        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        combo_probename = ttk.Combobox(frame1, value=list_probe, height=0, state='readonly')
        combo_probename.place(x=115, y=5)

        label_DB_table = Label(frame1, text='SQL Table Name')
        label_DB_table.place(x=5, y=25)
        combo_DBtable = ttk.Combobox(frame1, value=list_M3_table, height=0, state='readonly')
        combo_DBtable.place(x=115, y=25)

        btn_view = Button(frame1, width=15, height=2, text='Detail from SQL', command=func_1st_load)
        btn_view.place(x=350, y=5)

        # if combo_DBtable == 'SSR_table':
        #     combo_list = ttk.Combobox(frame2, value=df.columns, height=0, state='readonly')
        #     combo_list.place(x=115, y=5)
        #     # combo_probename = ttk.Combobox(frame2, value=list_probe, height=0, state='readonly')
        #     # combo_probename.place(x=115, y=5)


        # Add some style
        style = ttk.Style()
        # Pick a theme
        style.theme_use("default")

        # Configure our treeview colors
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3"
                        )
        # Change selected color
        style.map('Treeview',
                  background=[('selected', '#347083')])


        root_view.mainloop()

    except:
        print("Error: func_viewer_database")

